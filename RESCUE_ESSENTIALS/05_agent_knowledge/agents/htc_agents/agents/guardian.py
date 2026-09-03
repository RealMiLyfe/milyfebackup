"""GUARDIAN — Self-Repair and Ops Monitoring.

Model: Groq (cloud, fast, always-on)
Focus: System health, service monitoring, auto-recovery
Voice: Terse, status-report style, action-oriented
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
import structlog

from htc_agents.agents.base import BaseAgent
from htc_agents.tools.notify import send_alert, post_to_channel
from htc_agents.config import settings


log = structlog.get_logger()

# Services to monitor
MONITORED_SERVICES = {
    "mattermost": {"url": "http://mattermost:8065/api/v4/system/ping", "critical": True},
    "campaign-api": {"url": "http://htc-campaign-api:8200/health", "critical": True},
    "n8n": {"url": "http://htc-n8n:5678/healthz", "critical": False},
    "ghost": {"url": "http://htc-ghost:2368/ghost/api/v4/admin/site/", "critical": False},
    "searxng": {"url": "http://htc-searxng:8080/healthz", "critical": False},
    "ntfy": {"url": "http://htc-ntfy:80/v1/health", "critical": False},
    "uptime-kuma": {"url": "http://htc-uptime:3001/api/status-page/heartbeat", "critical": False},
}


class GuardianAgent(BaseAgent):
    """System health monitor — keeps the chamber running."""

    name = "guardian"
    role = "Operations Monitor & Self-Repair"
    description = (
        "Monitors all Time Chamber services, detects failures, "
        "reports health status, and provides recovery guidance."
    )
    model_provider = "groq"

    def _build_system_prompt(self) -> str:
        return """You are GUARDIAN — the Operations Monitor for the Hyperbolic Time Chamber.

## Your Role
You keep the system alive. You:
- Monitor all services for health and availability
- Report system status clearly and concisely
- Provide troubleshooting guidance when things break
- Track resource usage (CPU, RAM, disk)
- Alert the operator when critical services go down

## Services You Watch
- Mattermost (8065) — CRITICAL: ops hub
- Campaign API (8200) — CRITICAL: all campaign data
- n8n (5678) — automation workflows
- Ghost (2370) — blog publishing
- SearXNG (8080) — research/search
- Cloud LLMs (Groq/Gemini/NIM) — AI inference (no local dependency)
- ntfy (9091) — push alerts
- Uptime Kuma (3012) — monitoring dashboard
- PostgreSQL — shared database
- Redis — cache/queues

## Your Voice
Terse. Status-report style. Like a systems engineer during an incident.
- OK: "All services green. 12GB RAM, 25% CPU."
- Issue: "⚠️ n8n unresponsive. Last healthy: 5m ago. Attempting restart."
- Critical: "🚨 Campaign API DOWN. Immediate attention required."

## Health Check Response Format
```
SERVICE STATUS — [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━━
✅ service-name: healthy (Xms response)
⚠️ service-name: degraded (slow response / high error rate)
❌ service-name: DOWN (no response for X min)
━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: X/Y services healthy
```

## Rules
1. Never modify services yourself — report and recommend
2. Critical services down = immediate phone alert via ntfy
3. Non-critical down = Mattermost #service-health post only
4. Include recovery suggestions when reporting issues
5. Track patterns — if something keeps dying, flag the root cause
"""

    async def process(self, message: str, context: dict[str, Any] = None) -> str:
        """Process a health/status request."""
        lower = message.lower()

        # Direct health check request
        if any(kw in lower for kw in ["health", "status", "check", "alive", "running"]):
            health_report = await self._run_health_checks()
            # Use LLM to format and contextualize
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [
                SystemMessage(content=self._system_prompt),
                SystemMessage(content=f"Current health check results:\n{health_report}"),
                HumanMessage(content=message),
            ]
            try:
                response = await self.llm.ainvoke(messages)
                return response.content
            except Exception:
                # If LLM fails, return raw health report
                return health_report

        # General ops question
        messages = self._format_messages(message, context)
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            log.error("guardian.process_failed", error=str(e))
            return f"Guardian LLM unavailable. Running raw health check:\n{await self._run_health_checks()}"

    async def _run_health_checks(self) -> str:
        """Run health checks against all monitored services."""
        from datetime import datetime

        results = []
        healthy_count = 0
        total = len(MONITORED_SERVICES)

        async with httpx.AsyncClient(timeout=5) as client:
            for name, config in MONITORED_SERVICES.items():
                try:
                    resp = await client.get(config["url"])
                    if resp.status_code < 400:
                        results.append(f"✅ {name}: healthy ({resp.elapsed.total_seconds()*1000:.0f}ms)")
                        healthy_count += 1
                    else:
                        results.append(f"⚠️ {name}: degraded (HTTP {resp.status_code})")
                except httpx.TimeoutException:
                    results.append(f"❌ {name}: TIMEOUT")
                    if config["critical"]:
                        await self._alert_critical(name, "timeout")
                except Exception as e:
                    results.append(f"❌ {name}: DOWN ({type(e).__name__})")
                    if config["critical"]:
                        await self._alert_critical(name, str(e))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"SERVICE STATUS — {timestamp}\n{'━' * 40}"
        footer = f"{'━' * 40}\nSummary: {healthy_count}/{total} services healthy"

        return f"{header}\n" + "\n".join(results) + f"\n{footer}"

    async def _alert_critical(self, service: str, reason: str):
        """Alert when a critical service is down."""
        await send_alert(
            message=f"🚨 CRITICAL: {service} is DOWN — {reason}",
            title="Service Down",
            priority="high",
            tags=["warning", "server"],
        )
        await post_to_channel(
            "service-health",
            f"🚨 **CRITICAL**: `{service}` is DOWN. Reason: {reason}. Immediate attention required.",
        )
