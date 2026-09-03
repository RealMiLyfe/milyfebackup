"""Mattermost bot — connects the 18-agent system to Mattermost.

Features:
- Channel-aware routing (post in #debate-prep → routes to DEBATE_COACH)
- Threaded conversations (replies in-thread, maintains context per thread)
- DM orchestrator mode (DMs go through the full orchestrator for multi-agent routing)
- Proactive posting (agents can post to channels without being asked)
- File ingestion (documents dropped in channels get indexed)
- Reaction-based feedback (👍/👎 trains the system)
- Approval workflows (✅ to publish, ✏️ to revise)
- Priority interrupts (crisis → DM + phone push)
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any

import httpx
import structlog
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Monkey-patch httpx to ignore removed 'proxies' kwarg
# (mattermostautodriver hasn't updated for httpx>=0.28)
_orig_async_client_init = httpx.AsyncClient.__init__
_orig_sync_client_init = httpx.Client.__init__


def _patched_async_client_init(self, *args, **kwargs):
    kwargs.pop("proxies", None)
    return _orig_async_client_init(self, *args, **kwargs)


def _patched_sync_client_init(self, *args, **kwargs):
    kwargs.pop("proxies", None)
    return _orig_sync_client_init(self, *args, **kwargs)


httpx.AsyncClient.__init__ = _patched_async_client_init
httpx.Client.__init__ = _patched_sync_client_init

from mmpy_bot import Bot, Settings as BotSettings, Plugin, listen_to, Message  # noqa: E402

from htc_agents.config import settings
from htc_agents.memory.manager import MemoryManager
from htc_agents.memory.knowledge import knowledge_base
from htc_agents.guardrails.rails import guardrails
from htc_agents.orchestrator.graph import Orchestrator
from htc_agents.agents import AGENTS
from htc_agents.kernel.events import event_bus, KernelLoop, Event, EventType
from htc_agents.kernel.jobs import job_store
from htc_agents.kernel.actions import action_executor


log = structlog.get_logger()


# ═══════════════════════════════════════════════════════════════
# CHANNEL → AGENT ROUTING MAP
# ═══════════════════════════════════════════════════════════════

CHANNEL_AGENT_MAP = {
    "ops": None,  # Orchestrator decides
    "morning-brief": "commander",
    "opponent-watch": "scout",
    "content": "storyteller",
    "compliance": "sentinel",
    "petition": "connector",
    "service-health": "guardian",
    "debate-prep": "debate_coach",
    "fundraising": "fundraiser",
    "field-ops": "ground_game",
    "media-press": "media_coach",
    "crisis-response": "crisis_manager",
    "coalition": "coalition_builder",
    "scheduling": "scheduler",
    "pulse": "pollster",
    "oppo-research": "oppo_tracker",
    "speechwriting": "speechwriter",
}


# ═══════════════════════════════════════════════════════════════
# THREAD CONTEXT STORE (in-memory, per-thread conversation history)
# ═══════════════════════════════════════════════════════════════

_thread_contexts: dict[str, list[dict[str, str]]] = {}
_thread_agents: dict[str, str] = {}  # Which agent owns each thread

MAX_THREAD_HISTORY = 20


def _get_thread_history(thread_id: str) -> list[dict[str, str]]:
    """Get conversation history for a thread."""
    return _thread_contexts.get(thread_id, [])


def _add_to_thread(thread_id: str, role: str, content: str):
    """Add a message to thread history."""
    if thread_id not in _thread_contexts:
        _thread_contexts[thread_id] = []
    _thread_contexts[thread_id].append({"role": role, "content": content})
    # Trim to max history
    if len(_thread_contexts[thread_id]) > MAX_THREAD_HISTORY:
        _thread_contexts[thread_id] = _thread_contexts[thread_id][-MAX_THREAD_HISTORY:]


# ═══════════════════════════════════════════════════════════════
# FastAPI Health + Webhook + Direct API
# ═══════════════════════════════════════════════════════════════

api = FastAPI(title="HTC Agents — 18-Agent Campaign Intelligence")


class WebhookEvent(BaseModel):
    channel: str
    message: str
    priority: str = "default"


@api.get("/")
def api_root():
    return {
        "service": "HTC Multi-Agent System",
        "version": "0.2.0",
        "status": "online",
        "agents": list(AGENTS.keys()),
        "channels": list(CHANNEL_AGENT_MAP.keys()),
    }


@api.get("/health")
def api_health():
    return {"status": "healthy", "agents_loaded": len(AGENTS)}


@api.get("/llm/health")
def api_llm_health():
    """Live LLM provider health — for the dashboard/monitor.

    Shows each provider's status (healthy / cooling_down / dead / recovering),
    success/failure counts, last error, and cooldown remaining. This is how you
    see the agents' nervous system at a glance.
    """
    from htc_agents.llm.providers import provider_health
    health = provider_health()
    any_up = any(h["status"] in ("healthy", "recovering", "unknown") for h in health.values())
    return {"overall": "ok" if any_up else "degraded", "providers": health}


@api.post("/agent/invoke")
async def invoke_agent(request: dict[str, Any]):
    """Direct agent invocation API."""
    message = request.get("message", "")
    channel = request.get("channel", "")
    agent_name = request.get("agent", None)

    if not message:
        return {"error": "No message provided"}

    if agent_name and agent_name in _agents:
        # Direct agent call, bypass orchestrator
        response = await _agents[agent_name].invoke(message=message, context={})
        return {"response": response, "agent": agent_name}

    # Route through orchestrator
    response = await _orchestrator.process(
        message=message,
        source_channel=channel,
        user_id="api",
    )
    return {"response": response}


@api.post("/agent/chain")
async def invoke_chain(request: dict[str, Any]):
    """Multi-agent chain invocation.

    Body:
        message: str
        chain: list[str] — ordered list of agent names to run through
    """
    message = request.get("message", "")
    chain = request.get("chain", [])

    if not message or not chain:
        return {"error": "Need message and chain (list of agent names)"}

    from htc_agents.bot.chains import run_chain
    result = await run_chain(message, chain, _agents, _memory)
    return result


# ═══════════════════════════════════════════════════════════════
# KERNEL CONTROL API — the OS control surface
# (process table, event injection, action approval)
# ═══════════════════════════════════════════════════════════════


@api.get("/jobs")
async def list_jobs(limit: int = 50, status: str | None = None):
    """The process table — what the system is doing / recently did (`ps`)."""
    return {"jobs": await job_store.list(limit=limit, status=status)}


@api.get("/jobs/summary")
async def jobs_summary():
    """Counts by status — one-glance health of the process table."""
    return await job_store.summary()


@api.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await job_store.get(job_id)
    if not job:
        return {"error": "not found"}
    from dataclasses import asdict
    return asdict(job)


@api.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    job = await job_store.cancel(job_id)
    return {"cancelled": job is not None}


@api.post("/event")
async def emit_event(event: WebhookEvent):
    """Backward-compatible: also emit onto the kernel bus if it matches a known type.

    Existing callers post {channel, message} to notify a channel. We keep that behavior
    and, when the 'channel' names an event type, we additionally fan it onto the bus so
    the system can react.
    """
    from htc_agents.tools.notify import post_to_channel

    # Preserve the original notify-a-channel behavior.
    await post_to_channel(event.channel, event.message)

    # If the channel string is a recognized event type, inject it as an event too.
    try:
        etype = EventType(event.channel)
        await event_bus.emit(
            etype,
            payload={"message": event.message},
            source="webhook",
            priority=event.priority if event.priority != "default" else "normal",
        )
        return {"routed": True, "channel": event.channel, "event_emitted": etype.value}
    except ValueError:
        return {"routed": True, "channel": event.channel, "event_emitted": None}


@api.post("/event/emit")
async def emit_named_event(request: dict[str, Any]):
    """Inject an arbitrary kernel event. Body: {type, payload?, source?, priority?}."""
    type_str = request.get("type", "")
    try:
        etype = EventType(type_str)
    except ValueError:
        return {"error": f"Unknown event type '{type_str}'", "known": [e.value for e in EventType]}
    await event_bus.emit(
        etype,
        payload=request.get("payload", {}),
        source=request.get("source", "api"),
        priority=request.get("priority", "normal"),
    )
    return {"emitted": etype.value}


@api.get("/actions/pending")
async def actions_pending():
    """The approval queue — high-risk actions waiting on a human ✅."""
    return {"pending": action_executor.pending()}


@api.post("/actions/request")
async def actions_request(request: dict[str, Any]):
    """Submit an action intent through the guarded pipeline."""
    req = await action_executor.request(
        action=request.get("action", ""),
        params=request.get("params", {}),
        agent=request.get("agent", "api"),
        reason=request.get("reason", ""),
    )
    return req.to_dict()


@api.post("/actions/{action_id}/approve")
async def actions_approve(action_id: str):
    req = await action_executor.approve(action_id)
    if not req:
        return {"error": "not found or already resolved"}
    return req.to_dict()


@api.post("/actions/{action_id}/reject")
async def actions_reject(action_id: str, request: dict[str, Any] | None = None):
    reason = (request or {}).get("reason", "") if request else ""
    req = await action_executor.reject(action_id, reason=reason)
    if not req:
        return {"error": "not found"}
    return req.to_dict()


# ═══════════════════════════════════════════════════════════════
# SYSTEM INITIALIZATION
# ═══════════════════════════════════════════════════════════════

_memory: MemoryManager | None = None
_orchestrator: Orchestrator | None = None
_agents: dict[str, Any] = {}
_kernel: KernelLoop | None = None


async def initialize_system():
    """Initialize the full agent system + the kernel that makes it run on its own."""
    global _memory, _orchestrator, _agents, _kernel

    log.info("system.initializing")

    # Load knowledge base
    knowledge_base.load()

    # Initialize memory
    _memory = MemoryManager()
    await _memory.initialize()

    # Initialize guardrails
    await guardrails.initialize()

    # Initialize orchestrator
    _orchestrator = Orchestrator(memory=_memory)

    # Create and register all agents
    for name, agent_cls in AGENTS.items():
        _agents[name] = agent_cls(memory=_memory)
        log.info("system.agent_loaded", agent=name)

    _orchestrator.register_agents(_agents)
    _orchestrator.build_graph()

    # ─── Kernel: event bus, durable jobs, guarded actions ────
    # This is what turns the system from a dashboard (waits to be asked) into an OS
    # (runs and acts on its own).
    await event_bus.initialize()
    await job_store.initialize()
    action_executor.bind(job_store=job_store)

    _kernel = KernelLoop(bus=event_bus, agents=_agents, memory=_memory)
    _kernel.bind(job_store=job_store, orchestrator=_orchestrator)

    log.info("system.ready", agents_count=len(_agents))


async def start_kernel():
    """Start the kernel loop (call after initialize_system, inside a running loop)."""
    if _kernel is None:
        raise RuntimeError("initialize_system() must run before start_kernel()")
    await _kernel.start()
    log.info("system.kernel_online")


# ═══════════════════════════════════════════════════════════════
# mmpy_bot PLUGIN — Channel-Aware, Threaded, Smart Routing
# ═══════════════════════════════════════════════════════════════

class CampaignPlugin(Plugin):
    """Main bot plugin — routes messages based on channel, thread, and content."""

    @listen_to(r".*", needs_mention=True)
    async def handle_mention(self, message: Message):
        """Handle @mentions in any channel."""
        await self._process_message(message, is_dm=False)

    @listen_to(r".*", direct_only=True)
    async def handle_direct(self, message: Message):
        """DMs go through the full orchestrator."""
        await self._process_message(message, is_dm=True)

    async def _process_message(self, message: Message, is_dm: bool = False):
        """Route a message with full channel/thread awareness."""
        text = message.text.strip()
        if not text:
            return

        # Get context
        channel_name = self._get_channel_name(message)
        thread_id = message.reply_id or message.id
        user_id = message.user_id if hasattr(message, "user_id") else ""

        log.info(
            "bot.message",
            channel=channel_name,
            thread=thread_id,
            is_dm=is_dm,
            length=len(text),
        )

        # Add user message to thread history
        _add_to_thread(thread_id, "user", text)

        # Determine which agent should handle this
        agent_name = self._resolve_agent(channel_name, thread_id, text, is_dm)

        # Build context with thread history
        context = {
            "history": _get_thread_history(thread_id),
            "channel": channel_name,
            "is_dm": is_dm,
        }

        try:
            if agent_name and agent_name in _agents:
                # Direct to specific agent with thread context
                response = await _agents[agent_name].invoke(
                    message=text,
                    context=context,
                )
                # Remember which agent owns this thread
                _thread_agents[thread_id] = agent_name
            else:
                # Full orchestrator routing
                response = await _orchestrator.process(
                    message=text,
                    source_channel=channel_name,
                    user_id=user_id,
                )

            # Add response to thread history
            _add_to_thread(thread_id, "assistant", response[:500])

            # Reply in thread
            self._reply_threaded(message, response)

        except Exception as e:
            log.error("bot.process_failed", error=str(e), agent=agent_name)
            self._reply_threaded(
                message,
                f"⚠️ Error: {str(e)[:200]}\n\nTry rephrasing or use a prefix like `strategy:` or `health:`"
            )

    def _resolve_agent(
        self, channel_name: str, thread_id: str, text: str, is_dm: bool
    ) -> str | None:
        """Determine which agent should handle this message.

        Priority:
        1. Thread continuity — if this thread belongs to an agent, keep it there
        2. Channel mapping — channel determines the agent
        3. DM / orchestrator — let the orchestrator decide
        """
        # 1. Thread continuity
        if thread_id in _thread_agents:
            return _thread_agents[thread_id]

        # 2. Channel-based routing
        if channel_name in CHANNEL_AGENT_MAP:
            agent = CHANNEL_AGENT_MAP[channel_name]
            if agent is not None:
                return agent

        # 3. DM or unmapped channel → orchestrator decides
        return None

    def _get_channel_name(self, message: Message) -> str:
        """Extract channel name from message."""
        try:
            if hasattr(message, "channel") and hasattr(message.channel, "name"):
                return message.channel.name
            # Fallback: get from channel_id via driver
            channel_info = self.driver.channels.get_channel(message.channel_id)
            return channel_info.get("name", "unknown")
        except Exception:
            return "unknown"

    def _reply_threaded(self, message: Message, response: str):
        """Reply in-thread (creates thread if needed), handles long messages."""
        # Use the original message's root_id for threading
        root_id = message.reply_id or message.id

        if len(response) > 3900:
            parts = self._split_response(response, 3900)
            for part in parts:
                self.driver.reply_to(message, part, props={"root_id": root_id})
        else:
            self.driver.reply_to(message, response, props={"root_id": root_id})

    @staticmethod
    def _split_response(text: str, max_length: int) -> list[str]:
        """Split long responses at natural break points."""
        parts = []
        while text:
            if len(text) <= max_length:
                parts.append(text)
                break
            split_at = text.rfind("\n\n", 0, max_length)
            if split_at == -1:
                split_at = text.rfind("\n", 0, max_length)
            if split_at == -1:
                split_at = text.rfind(" ", 0, max_length)
            if split_at == -1:
                split_at = max_length
            parts.append(text[:split_at])
            text = text[split_at:].lstrip()
        return parts


# ═══════════════════════════════════════════════════════════════
# BOT FACTORY
# ═══════════════════════════════════════════════════════════════

def create_mattermost_bot() -> Bot | None:
    """Create the mmpy_bot instance (without initialization — called from __main__)."""
    from urllib.parse import urlparse
    import os

    parsed = urlparse(settings.MATTERMOST_URL)
    mm_host = f"{parsed.scheme}://{parsed.hostname}"
    mm_port = parsed.port or 8065

    # Prevent mmpy_bot from reading env vars that conflict
    os.environ["LOG_LEVEL"] = "20"
    os.environ.pop("MATTERMOST_PORT", None)
    os.environ.pop("MATTERMOST_URL", None)

    if not settings.MATTERMOST_BOT_TOKEN:
        log.warning("system.no_bot_token", msg="API-only mode. Set MM_BOT_TOKEN.")
        return None

    bot_kwargs = {
        "MATTERMOST_URL": mm_host,
        "MATTERMOST_PORT": mm_port,
        "BOT_TOKEN": settings.MATTERMOST_BOT_TOKEN,
        "BOT_TEAM": settings.MATTERMOST_TEAM,
        "SSL_VERIFY": False,
        "WEBHOOK_HOST_ENABLED": False,
        "LOG_LEVEL": 20,
    }

    bot_settings = BotSettings(**bot_kwargs)

    try:
        bot = Bot(settings=bot_settings, plugins=[CampaignPlugin()])
        log.info("system.bot_created")
        return bot
    except Exception as e:
        log.warning("system.bot_failed", error=str(e))
        return None


def create_bot() -> Bot | None:
    """Legacy entry — initialize + create bot (backward compat)."""
    asyncio.run(initialize_system())

    def run_api():
        uvicorn.run(api, host="0.0.0.0", port=8067, log_level="warning")

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    log.info("system.api_started", port=8067)

    return create_mattermost_bot()
