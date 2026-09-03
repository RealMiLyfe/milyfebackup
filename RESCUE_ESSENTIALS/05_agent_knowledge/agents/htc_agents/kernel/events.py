"""Event bus + kernel loop — the reason the system runs without being asked.

This is the single biggest change that turns the dashboard into an OS. Instead of
only waking up when a human types in Mattermost, the system now has a long-running
loop that listens for events and reacts. Agents publish events ("signature logged",
"opponent moved", "deadline near") and subscribers react by dispatching agent work.

Transport: Redis pub/sub (Redis is already in the compose stack). If Redis is
unavailable, the bus degrades to an in-process asyncio broker so the system still
runs in dev/offline mode.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Awaitable, Callable

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


CHANNEL = "htc:events"  # single Redis pub/sub channel; filtering happens in-process


class EventType(str, Enum):
    """Canonical event types the kernel understands.

    Keep these stable — they are the system's public "syscall" surface. Agents and
    services emit these; subscribers react to them.
    """

    # ─── Field / petition ────────────────────────────────────
    SIGNATURE_LOGGED = "signature.logged"
    PETITION_PACE_BEHIND = "petition.pace_behind"
    PETITION_PACE_ON_TRACK = "petition.pace_on_track"

    # ─── Intelligence ────────────────────────────────────────
    OPPONENT_ACTIVITY = "opponent.activity"
    NEWS_BREAKING = "news.breaking"
    SENTIMENT_SHIFT = "sentiment.shift"

    # ─── Compliance ──────────────────────────────────────────
    DEADLINE_NEAR = "deadline.near"
    DEADLINE_URGENT = "deadline.urgent"

    # ─── Content / outreach ──────────────────────────────────
    CONTENT_DRAFTED = "content.drafted"
    CONTENT_PUBLISHED = "content.published"
    CONTACT_LOGGED = "contact.logged"

    # ─── Crisis ──────────────────────────────────────────────
    ATTACK_DETECTED = "crisis.attack_detected"

    # ─── Scheduler heartbeats (replace hardcoded cron prompts) ─
    RHYTHM_MORNING_BRIEF = "rhythm.morning_brief"
    RHYTHM_OPPONENT_SCAN = "rhythm.opponent_scan"
    RHYTHM_DAILY_SCHEDULE = "rhythm.daily_schedule"
    RHYTHM_PETITION_PACE = "rhythm.petition_pace"
    RHYTHM_DAILY_WRAP = "rhythm.daily_wrap"
    RHYTHM_WEEKLY_RETRO = "rhythm.weekly_retro"
    RHYTHM_WEEK_PLAN = "rhythm.week_plan"
    RHYTHM_DEADLINE_CHECK = "rhythm.deadline_check"

    # ─── System / kernel ─────────────────────────────────────
    AGENT_COMPLETED = "agent.completed"
    ACTION_REQUESTED = "action.requested"
    ACTION_COMMITTED = "action.committed"
    JOB_STATE_CHANGED = "job.state_changed"


@dataclass
class Event:
    """A single event flowing through the bus."""

    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    priority: str = "normal"  # normal | high | urgent
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, raw: str) -> "Event":
        data = json.loads(raw)
        return cls(**data)


# A subscriber handler receives an Event and does work (usually async).
Handler = Callable[[Event], Awaitable[None]]


class EventBus:
    """Publish/subscribe event bus backed by Redis, with in-process fallback.

    Subscribers register a handler for an EventType (or "*" for all events).
    Publishing an event fans it out to every matching handler.
    """

    def __init__(self):
        self._pub = None              # publisher client (bound per running loop)
        self._pub_loop = None
        self._pubsub = None           # subscriber, created on the loop run() uses
        self._handlers: dict[str, list[Handler]] = {}
        self._local_queue: asyncio.Queue[Event] | None = None
        self._running = False
        self._use_redis = False

    async def initialize(self):
        """Probe Redis. We do NOT keep the connection here — the async redis client
        binds to the loop it is created on, and this app runs the API and the kernel
        loop on separate threads/loops. Publisher connects lazily per loop; the
        subscriber is created inside run() on the kernel loop."""
        try:
            import redis.asyncio as aioredis

            probe = aioredis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            await probe.ping()
            await probe.aclose()
            self._use_redis = True
            log.info("eventbus.redis_ready", url=settings.REDIS_URL)
        except Exception as e:
            self._use_redis = False
            self._local_queue = asyncio.Queue()
            log.warning("eventbus.redis_unavailable_local_mode", error=str(e))

    def subscribe(self, event_type: EventType | str, handler: Handler):
        """Register a handler for an event type. Use '*' to catch every event."""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        self._handlers.setdefault(key, []).append(handler)
        log.info("eventbus.subscribed", event_type=key, handler=getattr(handler, "__name__", str(handler)))

    async def _publisher(self):
        """Return a redis publisher client bound to the current running loop."""
        if not self._use_redis:
            return None
        import redis.asyncio as aioredis

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if self._pub is None or self._pub_loop is not loop:
            self._pub = aioredis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            self._pub_loop = loop
        return self._pub

    async def publish(self, event: Event):
        """Publish an event to all subscribers."""
        log.info("eventbus.publish", type=event.type, source=event.source, priority=event.priority)
        if self._use_redis:
            client = await self._publisher()
            if client is not None:
                await client.publish(CHANNEL, event.to_json())
                return
        if self._local_queue is not None:
            await self._local_queue.put(event)

    async def emit(
        self,
        event_type: EventType | str,
        payload: dict[str, Any] | None = None,
        source: str = "system",
        priority: str = "normal",
    ):
        """Convenience helper to build and publish an event in one call."""
        etype = event_type.value if isinstance(event_type, EventType) else event_type
        await self.publish(
            Event(type=etype, payload=payload or {}, source=source, priority=priority)
        )

    async def _dispatch(self, event: Event):
        """Fan an event out to matching handlers, isolating handler failures."""
        handlers = list(self._handlers.get(event.type, []))
        handlers += list(self._handlers.get("*", []))
        if not handlers:
            log.debug("eventbus.no_handlers", type=event.type)
            return

        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                log.error(
                    "eventbus.handler_failed",
                    type=event.type,
                    handler=getattr(handler, "__name__", str(handler)),
                    error=str(e),
                )

    async def _run_redis(self):
        """Consume messages from the Redis pubsub subscription.

        The subscriber client is created here, on whatever loop run() executes on
        (the kernel loop), so it stays bound to a live loop for its whole lifetime.
        """
        import redis.asyncio as aioredis

        sub_client = aioredis.from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )
        self._pubsub = sub_client.pubsub()
        await self._pubsub.subscribe(CHANNEL)
        log.info("eventbus.subscribed_channel", channel=CHANNEL)

        async for msg in self._pubsub.listen():
            if not self._running:
                break
            if msg is None or msg.get("type") != "message":
                continue
            try:
                event = Event.from_json(msg["data"])
            except Exception as e:
                log.error("eventbus.decode_failed", error=str(e))
                continue
            await self._dispatch(event)

    async def _run_local(self):
        """Consume events from the in-process queue."""
        while self._running:
            try:
                event = await asyncio.wait_for(self._local_queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            await self._dispatch(event)

    async def run(self):
        """Run the delivery loop. This is the piece that keeps listening forever."""
        self._running = True
        log.info("eventbus.running", transport="redis" if self._use_redis else "local")
        if self._use_redis:
            await self._run_redis()
        else:
            await self._run_local()

    async def stop(self):
        self._running = False
        if self._pubsub:
            try:
                await self._pubsub.unsubscribe(CHANNEL)
            except Exception:
                pass
        log.info("eventbus.stopped")


class KernelLoop:
    """The kernel loop — wires events to agent reactions and keeps running.

    This is the OS scheduler analogue: it owns the mapping from "something happened"
    to "an agent does work about it", dispatches that work as durable jobs, and never
    stops listening. Agents no longer need a human to speak first.
    """

    def __init__(self, bus: EventBus, agents: dict[str, Any], memory: Any = None):
        self.bus = bus
        self.agents = agents
        self.memory = memory
        self._task: asyncio.Task | None = None
        # Lazily imported to avoid a circular import at module load time.
        self._job_store = None
        self._orchestrator = None

    def bind(self, job_store: Any = None, orchestrator: Any = None):
        """Attach the job store and orchestrator the loop dispatches through."""
        self._job_store = job_store
        self._orchestrator = orchestrator

    # ─── Reaction registration ────────────────────────────────

    def install_reactions(self):
        """Subscribe the standard event → agent reactions.

        Each reaction turns an event into a durable agent job so the work shows up
        in the process table and survives handler-local failures.
        """
        R = self._react  # noqa: N806

        # Field / petition
        self.bus.subscribe(EventType.SIGNATURE_LOGGED, R("ground_game",
            "A new petition signature was logged. Update the running pace estimate. "
            "If we have fallen behind the required daily rate, say so plainly and name "
            "the zones that need reinforcement.", post_channel="field-ops",
            follow_up=EventType.PETITION_PACE_BEHIND))
        self.bus.subscribe(EventType.PETITION_PACE_BEHIND, R("commander",
            "Petition collection is behind pace. Give one decisive reallocation decision "
            "for tomorrow: where do we send collectors and why.", post_channel="ops",
            priority="high"))

        # Intelligence
        self.bus.subscribe(EventType.OPPONENT_ACTIVITY, R("oppo_tracker",
            "New opponent activity was detected. Assess whether it is actionable and, "
            "if so, what our response window is.", post_channel="opponent-watch"))
        self.bus.subscribe(EventType.NEWS_BREAKING, R("scout",
            "Breaking news relevant to the race just landed. Summarize what happened and "
            "whether it demands a same-day response.", post_channel="opponent-watch",
            priority="urgent"))
        self.bus.subscribe(EventType.SENTIMENT_SHIFT, R("pollster",
            "Public sentiment appears to be shifting. Identify the issue moving and which "
            "neighborhoods it is moving in.", post_channel="pulse"))

        # Compliance
        self.bus.subscribe(EventType.DEADLINE_NEAR, R("sentinel",
            "A compliance deadline is approaching. State exactly what must be filed, by "
            "when, and what is still outstanding.", post_channel="compliance",
            priority="high"))
        self.bus.subscribe(EventType.DEADLINE_URGENT, R("sentinel",
            "A compliance deadline is URGENT (within 3 days). List the exact remaining "
            "steps in order.", post_channel="compliance", priority="urgent"))

        # Crisis
        self.bus.subscribe(EventType.ATTACK_DETECTED, R("crisis_manager",
            "An attack on the campaign was detected. Draft a counter-narrative and a "
            "recommended response posture.", post_channel="crisis-response",
            priority="urgent"))

        # Scheduler heartbeats (the old cron prompts, now event-driven)
        self.bus.subscribe(EventType.RHYTHM_MORNING_BRIEF, R("commander",
            "Generate today's morning brief: key priorities, overnight developments, "
            "petition status, upcoming deadlines, and recommended focus.",
            post_channel="morning-brief"))
        self.bus.subscribe(EventType.RHYTHM_OPPONENT_SCAN, R("scout",
            "Scan for opponent activity in the last 8 hours. Report only actionable intel.",
            post_channel="opponent-watch"))
        self.bus.subscribe(EventType.RHYTHM_DAILY_SCHEDULE, R("scheduler",
            "Build today's optimal schedule around petition priority, events, and energy.",
            post_channel="scheduling"))
        self.bus.subscribe(EventType.RHYTHM_PETITION_PACE, R("ground_game",
            "Check petition pace against the deadline. What zones need reinforcement?",
            post_channel="field-ops"))
        self.bus.subscribe(EventType.RHYTHM_DAILY_WRAP, R("analyst",
            "Generate the end-of-day summary and one recommendation for tomorrow.",
            post_channel="ops"))
        self.bus.subscribe(EventType.RHYTHM_DEADLINE_CHECK, R("sentinel",
            "Check all deadlines within 7 days. Flag anything within 3 days as URGENT.",
            post_channel="compliance"))

        log.info("kernel.reactions_installed", count=len(self.bus._handlers))

    def _react(
        self,
        agent_name: str,
        instruction: str,
        post_channel: str | None = None,
        priority: str = "normal",
        follow_up: EventType | None = None,
    ) -> Handler:
        """Build an event handler that dispatches a durable agent job."""

        async def handler(event: Event):
            # Merge any event payload context into the instruction the agent sees.
            ctx_note = ""
            if event.payload:
                ctx_note = f"\n\nEvent context: {json.dumps(event.payload)[:1000]}"

            await self._dispatch_agent_job(
                agent_name=agent_name,
                message=instruction + ctx_note,
                source_event=event,
                post_channel=post_channel,
                priority=priority,
                follow_up=follow_up,
            )

        handler.__name__ = f"react_{event_or_name(agent_name)}"
        return handler

    async def _dispatch_agent_job(
        self,
        agent_name: str,
        message: str,
        source_event: Event,
        post_channel: str | None,
        priority: str,
        follow_up: EventType | None,
    ):
        """Run an agent as a durable job and route its output."""
        from htc_agents.tools.notify import post_to_channel

        agent = self.agents.get(agent_name)
        if agent is None:
            log.warning("kernel.agent_missing", agent=agent_name, event=source_event.type)
            return

        job = None
        if self._job_store:
            job = await self._job_store.create(
                kind="event_reaction",
                agent=agent_name,
                trigger=source_event.type,
                payload={"priority": priority, "channel": post_channel},
            )
            await self._job_store.mark_running(job.id)

        try:
            response = await agent.invoke(message=message, context={"event": source_event.payload})

            if self._job_store and job:
                await self._job_store.mark_done(job.id, result=response[:2000])

            if post_channel and response:
                await post_to_channel(post_channel, f"## ⚙️ {agent_name.title()} (auto)\n\n{response}")

            await self.bus.emit(
                EventType.AGENT_COMPLETED,
                payload={"agent": agent_name, "trigger": source_event.type, "job_id": job.id if job else None},
                source="kernel",
            )

            # Simple chaining: if this reaction can escalate, emit its follow-up when
            # the agent's own text signals it (keeps the escalation grounded in output).
            if follow_up and _looks_negative(response):
                await self.bus.emit(follow_up, payload={"from": agent_name}, source="kernel", priority="high")

        except Exception as e:
            log.error("kernel.reaction_failed", agent=agent_name, error=str(e))
            if self._job_store and job:
                await self._job_store.mark_failed(job.id, error=str(e))

    async def start(self):
        """Install reactions and start the bus delivery loop as a background task."""
        self.install_reactions()
        self._task = asyncio.create_task(self.bus.run())
        log.info("kernel.started")

    async def stop(self):
        await self.bus.stop()
        if self._task:
            self._task.cancel()
        log.info("kernel.stopped")


def event_or_name(name: str) -> str:
    return name.replace(".", "_").replace(":", "_")


def _looks_negative(text: str) -> bool:
    """Heuristic: did the agent report a problem worth escalating?"""
    if not text:
        return False
    lowered = text.lower()[:600]
    signals = ["behind", "off pace", "off-pace", "short of", "at risk", "urgent", "falling"]
    return any(s in lowered for s in signals)


# Singleton bus (the kernel loop is constructed at startup with live agents).
event_bus = EventBus()
