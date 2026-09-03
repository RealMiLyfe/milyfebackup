"""Guarded write-authority — lets agents DO things, not just talk.

Until now, agents produced text that landed in a Mattermost channel. Nothing changed
in the world. This layer lets an agent emit an *action intent* that is executed through
the existing tools, but only after passing two gates:

    1. Guardrails  — the existing GuardrailsEngine.check_action() veto. Anything that
                     touches the sovereign MiLyfe platform is hard-blocked here.
    2. Approval    — high-risk actions require an explicit human ✅ before they run.
                     They sit in WAITING until approved (or expire).

Actions map ONLY to campaign-ops surfaces the system already owns:
    - schedule_social_post  → Postiz (content is queued, not blasted instantly)
    - track_published       → campaign-api /content/published
    - store_brief           → campaign-api /api/store-brief
    - notify_operator       → ntfy push
    - post_channel          → Mattermost channel post

The platform-sovereignty boundary is preserved: there is deliberately no action that
writes to Supabase, the platform DB, or production. Those remain in BLOCKED_ACTIONS.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Awaitable, Callable

import structlog

from htc_agents.guardrails.rails import guardrails


log = structlog.get_logger()


class ActionStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    COMMITTED = "committed"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    FAILED = "failed"


# Actions that must never auto-run — they change the outside world in a public,
# hard-to-reverse way, so a human confirms first.
HIGH_RISK_ACTIONS = {
    "schedule_social_post",   # publishes to the public timeline (even if delayed)
    "track_published",        # records something as officially published
}

# Low-risk actions may commit immediately once guardrails pass.
LOW_RISK_ACTIONS = {
    "store_brief",
    "notify_operator",
    "post_channel",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ActionRequest:
    """An action an agent wants to take, moving through the guard/approval pipeline."""

    action: str
    params: dict[str, Any] = field(default_factory=dict)
    agent: str = ""
    reason: str = ""
    status: str = ActionStatus.PENDING_APPROVAL.value
    result: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionExecutor:
    """Executes guarded agent actions against the existing campaign-ops tools."""

    def __init__(self):
        self._pending: dict[str, ActionRequest] = {}
        self._handlers: dict[str, Callable[[dict[str, Any]], Awaitable[str]]] = {}
        self._job_store = None
        self._register_builtin_handlers()

    def bind(self, job_store: Any = None):
        self._job_store = job_store

    # ─── Handler registry ─────────────────────────────────────

    def register(self, action: str, handler: Callable[[dict[str, Any]], Awaitable[str]]):
        self._handlers[action] = handler

    def _register_builtin_handlers(self):
        self.register("schedule_social_post", self._h_schedule_social_post)
        self.register("track_published", self._h_track_published)
        self.register("store_brief", self._h_store_brief)
        self.register("notify_operator", self._h_notify_operator)
        self.register("post_channel", self._h_post_channel)

    # ─── Public API ───────────────────────────────────────────

    async def request(
        self,
        action: str,
        params: dict[str, Any],
        agent: str = "",
        reason: str = "",
    ) -> ActionRequest:
        """Submit an action. Runs guardrails, then either commits or waits for approval."""
        req = ActionRequest(action=action, params=params, agent=agent, reason=reason)

        # Gate 1: guardrails (hard platform-sovereignty veto lives here)
        allowed, why = await guardrails.check_action(action, params)
        if not allowed:
            req.status = ActionStatus.BLOCKED.value
            req.result = why
            log.warning("action.blocked", action=action, agent=agent, reason=why)
            await self._announce(req)
            return req

        # Unknown action → block rather than silently do nothing.
        if action not in self._handlers:
            req.status = ActionStatus.BLOCKED.value
            req.result = f"Unknown action '{action}'."
            log.warning("action.unknown", action=action, agent=agent)
            return req

        # Gate 2: approval for high-risk actions.
        if action in HIGH_RISK_ACTIONS:
            req.status = ActionStatus.PENDING_APPROVAL.value
            self._pending[req.id] = req
            await self._record_job(req, waiting=True)
            await self._announce(req)
            log.info("action.awaiting_approval", action=action, agent=agent, id=req.id)
            return req

        # Low-risk → commit now.
        return await self._commit(req)

    async def approve(self, action_id: str) -> ActionRequest | None:
        """Human approves a pending high-risk action; it commits immediately."""
        req = self._pending.get(action_id)
        if not req:
            log.warning("action.approve_not_found", id=action_id)
            return None
        req.status = ActionStatus.APPROVED.value
        req.updated_at = _now()
        log.info("action.approved", id=action_id, action=req.action)
        return await self._commit(req)

    async def reject(self, action_id: str, reason: str = "") -> ActionRequest | None:
        """Human rejects a pending action; it never runs."""
        req = self._pending.pop(action_id, None)
        if not req:
            return None
        req.status = ActionStatus.REJECTED.value
        req.result = reason or "Rejected by operator."
        req.updated_at = _now()
        log.info("action.rejected", id=action_id)
        return req

    def pending(self) -> list[dict[str, Any]]:
        """The approval queue — actions waiting on a human."""
        return [r.to_dict() for r in self._pending.values()]

    # ─── Commit + bookkeeping ─────────────────────────────────

    async def _commit(self, req: ActionRequest) -> ActionRequest:
        handler = self._handlers[req.action]
        job = await self._record_job(req, waiting=False)
        try:
            result = await handler(req.params)
            req.status = ActionStatus.COMMITTED.value
            req.result = result
            req.updated_at = _now()
            self._pending.pop(req.id, None)
            if self._job_store and job:
                await self._job_store.mark_done(job.id, result=result[:2000])
            log.info("action.committed", action=req.action, agent=req.agent)
            await self._announce(req)
        except Exception as e:
            req.status = ActionStatus.FAILED.value
            req.result = str(e)
            req.updated_at = _now()
            if self._job_store and job:
                await self._job_store.mark_failed(job.id, error=str(e))
            log.error("action.failed", action=req.action, error=str(e))
        return req

    async def _record_job(self, req: ActionRequest, waiting: bool):
        if not self._job_store:
            return None
        job = await self._job_store.create(
            kind="action",
            agent=req.agent,
            trigger=req.action,
            payload={"reason": req.reason, "params_keys": list(req.params.keys())},
        )
        if waiting:
            await self._job_store.mark_waiting(job.id, reason="awaiting operator approval")
        else:
            await self._job_store.mark_running(job.id)
        return job

    async def _announce(self, req: ActionRequest):
        """Best-effort event emission so the action shows up on the bus."""
        try:
            from htc_agents.kernel.events import event_bus, EventType

            etype = (
                EventType.ACTION_COMMITTED
                if req.status == ActionStatus.COMMITTED.value
                else EventType.ACTION_REQUESTED
            )
            await event_bus.emit(
                etype,
                payload={"id": req.id, "action": req.action, "status": req.status, "agent": req.agent},
                source="action_executor",
            )
        except Exception:
            pass

    # ─── Built-in action handlers (map to existing tools) ─────

    async def _h_schedule_social_post(self, params: dict[str, Any]) -> str:
        from htc_agents.tools.postiz_client import publish_approved_content

        content = params.get("content", "")
        platforms = params.get("platforms") or ["mastodon", "linkedin"]
        minutes = int(params.get("schedule_minutes_from_now", 5))
        if not content:
            raise ValueError("schedule_social_post requires 'content'")
        ok = await publish_approved_content(content, platforms, minutes)
        if not ok:
            raise RuntimeError("Postiz did not accept the post.")
        return f"Scheduled to {', '.join(platforms)} in {minutes}m."

    async def _h_track_published(self, params: dict[str, Any]) -> str:
        import httpx
        from htc_agents.config import settings

        title = params.get("title", "")
        platform = params.get("platform", "")
        if not title:
            raise ValueError("track_published requires 'title'")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{settings.CAMPAIGN_API_URL}/content/published",
                json={"title": title, "platform": platform},
            )
            resp.raise_for_status()
        return f"Recorded '{title}' as published on {platform or 'unknown'}."

    async def _h_store_brief(self, params: dict[str, Any]) -> str:
        import httpx
        from htc_agents.config import settings

        body = params.get("brief") or params.get("content", "")
        if not body:
            raise ValueError("store_brief requires 'brief'")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{settings.CAMPAIGN_API_URL}/api/store-brief",
                json={"brief": body},
            )
            resp.raise_for_status()
        return "Brief stored for dashboard display."

    async def _h_notify_operator(self, params: dict[str, Any]) -> str:
        from htc_agents.tools.notify import send_alert

        message = params.get("message", "")
        if not message:
            raise ValueError("notify_operator requires 'message'")
        await send_alert(
            message=message,
            title=params.get("title", "Campaign Alert"),
            priority=params.get("priority", "default"),
            tags=params.get("tags"),
        )
        return "Operator notified."

    async def _h_post_channel(self, params: dict[str, Any]) -> str:
        from htc_agents.tools.notify import post_to_channel

        channel = params.get("channel", "")
        message = params.get("message", "")
        if not channel or not message:
            raise ValueError("post_channel requires 'channel' and 'message'")
        await post_to_channel(channel, message)
        return f"Posted to #{channel}."


# Singleton
action_executor = ActionExecutor()
