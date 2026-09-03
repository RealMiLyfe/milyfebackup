"""Resilient LLM provider layer.

Every agent invokes through a single rotating pool. When a provider fails at
invoke time (429 quota, 401/403 auth, 5xx, timeout), it is marked unhealthy for
a cooldown window and the pool automatically rotates to the next provider. A
local Ollama model is always last in the chain as a $0, rate-limit-free anchor
so the agents NEVER fully go dark.

Live health is exposed via provider_health() for the dashboard/monitor.

Verified working model names (checked live 2026-09):
  - openrouter : nvidia/nemotron-3.5-lightning:free (free tier)
  - gemini     : gemini-3.6-flash
  - groq       : openai/gpt-oss-120b   (free tier, resets daily)
  - cerebras   : gpt-oss-120b          (free tier, resets)
  - ollama     : qwen2.5:3b            (local, unlimited)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

import structlog
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from htc_agents.config import settings

log = structlog.get_logger()


# ── Provider pool, in priority order ──────────────────────────────────────────
# Cloud free tiers first (fast, high quality), local Ollama anchor last.
@dataclass
class ProviderSpec:
    name: str
    model: str
    build: str  # which get_llm branch to use
    cooldown_s: int = 900  # how long to skip after a failure (rate limits reset)


POOL: list[ProviderSpec] = [
    ProviderSpec("openrouter", "nvidia/nemotron-3.5-lightning:free", "openrouter"),
    ProviderSpec("groq", "openai/gpt-oss-120b", "groq"),
    ProviderSpec("gemini", "gemini-3.6-flash", "gemini"),
    ProviderSpec("cerebras", "gpt-oss-120b", "cerebras"),
    ProviderSpec("ollama", settings.OLLAMA_MODEL, "ollama", cooldown_s=60),
]


# ── Live health state (read by the monitor/dashboard) ─────────────────────────
@dataclass
class Health:
    status: str = "unknown"      # healthy | cooling_down | dead | unknown
    last_error: str = ""
    last_success_ts: float = 0.0
    last_failure_ts: float = 0.0
    cooldown_until: float = 0.0
    successes: int = 0
    failures: int = 0


_HEALTH: dict[str, Health] = {p.name: Health() for p in POOL}


def _has_key(spec: ProviderSpec) -> bool:
    keymap = {
        "openrouter": settings.OPENROUTER_API_KEY,
        "groq": settings.GROQ_API_KEY,
        "gemini": settings.GEMINI_API_KEY,
        "cerebras": settings.CEREBRAS_API_KEY,
        "ollama": settings.OLLAMA_URL,  # always "present"
    }
    val = keymap.get(spec.name, "")
    return bool(val) and not val.startswith("your_")


def _build(spec: ProviderSpec) -> BaseChatModel:
    """Construct a langchain chat model for a provider spec."""
    if spec.build == "openrouter":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model=spec.model, temperature=0.7, max_tokens=2048, timeout=45, max_retries=0,
        )
    if spec.build == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=settings.GROQ_API_KEY, model=spec.model,
            temperature=0.7, max_tokens=2048, max_retries=0,
        )
    if spec.build == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GEMINI_API_KEY, model=spec.model,
            temperature=0.7, max_output_tokens=2048, max_retries=0,
        )
    if spec.build == "cerebras":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=settings.CEREBRAS_API_KEY,
            base_url="https://api.cerebras.ai/v1",
            model=spec.model, temperature=0.7, max_tokens=2048, timeout=45, max_retries=0,
        )
    if spec.build == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            base_url=settings.OLLAMA_URL, model=spec.model,
            temperature=0.5, num_predict=2048,
        )
    raise ValueError(f"Unknown provider build: {spec.build}")


def _mark_success(name: str):
    h = _HEALTH[name]
    h.status = "healthy"; h.last_success_ts = time.time(); h.successes += 1; h.cooldown_until = 0.0


def _mark_failure(name: str, err: str, cooldown_s: int):
    h = _HEALTH[name]
    h.last_error = err[:200]; h.last_failure_ts = time.time(); h.failures += 1
    h.cooldown_until = time.time() + cooldown_s
    h.status = "cooling_down"


def _available(spec: ProviderSpec) -> bool:
    if not _has_key(spec):
        _HEALTH[spec.name].status = "dead"
        _HEALTH[spec.name].last_error = "no api key"
        return False
    return time.time() >= _HEALTH[spec.name].cooldown_until


class ResilientLLM:
    """Invoke across the provider pool with automatic failover + health tracking.

    Drop-in for langchain chat models: supports .invoke() and .ainvoke() with a
    list of messages, returns an object with a .content attribute.
    """

    def __init__(self, preferred: Optional[str] = None):
        # If an agent has a preferred provider, try it first, then the rest.
        self._order = POOL
        if preferred:
            self._order = (
                [p for p in POOL if p.name == preferred]
                + [p for p in POOL if p.name != preferred]
            )

    async def ainvoke(self, messages: list[BaseMessage]):
        return await self._run(messages, is_async=True)

    def invoke(self, messages: list[BaseMessage]):
        import asyncio
        return asyncio.get_event_loop().run_until_complete(self._run(messages, is_async=True))

    async def _run(self, messages, is_async: bool):
        last_err = None
        for spec in self._order:
            if not _available(spec):
                continue
            try:
                llm = _build(spec)
                resp = await llm.ainvoke(messages) if is_async else llm.invoke(messages)
                _mark_success(spec.name)
                log.info("llm.ok", provider=spec.name, model=spec.model)
                return resp
            except Exception as e:  # 429/401/403/5xx/timeout — rotate
                msg = str(e)
                _mark_failure(spec.name, msg, spec.cooldown_s)
                log.warning("llm.rotate", provider=spec.name, error=msg[:120])
                last_err = e
                continue
        # Everything failed (including local). Surface a clear error.
        raise RuntimeError(f"All LLM providers unavailable. Last error: {last_err}")


def get_resilient_llm(preferred: Optional[str] = None) -> ResilientLLM:
    return ResilientLLM(preferred=preferred)


def provider_health() -> dict:
    """Snapshot of every provider's health — consumed by the monitor/dashboard."""
    now = time.time()
    out = {}
    for p in POOL:
        h = _HEALTH[p.name]
        status = h.status
        if status == "cooling_down" and now >= h.cooldown_until:
            status = "recovering"
        out[p.name] = {
            "status": status,
            "model": p.model,
            "successes": h.successes,
            "failures": h.failures,
            "last_error": h.last_error,
            "cooldown_remaining_s": max(0, int(h.cooldown_until - now)),
            "last_success_age_s": int(now - h.last_success_ts) if h.last_success_ts else None,
        }
    return out


# ── Backwards-compatible shims (old code calls these) ─────────────────────────
def get_llm(provider: str, **kwargs) -> ResilientLLM:
    """Legacy entrypoint — now returns the resilient pool preferring `provider`."""
    return ResilientLLM(preferred=provider if provider in _HEALTH else None)


def get_fallback_llm(primary: str) -> ResilientLLM:
    return ResilientLLM(preferred=None)
