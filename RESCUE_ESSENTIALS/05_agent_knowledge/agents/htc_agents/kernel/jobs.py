"""Durable job table — gives agent work a real process lifecycle.

Before this, an agent invocation was a fire-and-forget function call: it ran, returned
text, and vanished. There was no process table you could inspect, no lifecycle, no
retry, no record of what the system was doing right now.

A Job is the OS-process analogue for agent work. Every event reaction, scheduled task,
and orchestrated request becomes a Job with a status you can query
(queued → running → waiting → done | failed). Jobs persist to Redis so they survive a
restart, with an in-process fallback for dev/offline mode.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


JOB_KEY_PREFIX = "htc:job:"
JOB_INDEX_KEY = "htc:jobs:index"  # sorted set: job_id -> created ts (for the process table)
MAX_INDEX = 1000  # keep the most recent N jobs queryable


class JobStatus(str, Enum):
    """Job lifecycle states — the process table's status column."""

    QUEUED = "queued"       # created, not yet started
    RUNNING = "running"     # actively executing
    WAITING = "waiting"     # blocked on something (e.g. human approval)
    DONE = "done"           # completed successfully
    FAILED = "failed"       # errored out
    CANCELLED = "cancelled"  # killed before completion


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Job:
    """A single unit of durable work in the process table."""

    kind: str                       # event_reaction | scheduled | orchestrated | action
    agent: str = ""                 # which agent owns the work (if any)
    trigger: str = ""               # event type / schedule name / "user" etc.
    status: str = JobStatus.QUEUED.value
    payload: dict[str, Any] = field(default_factory=dict)
    result: str = ""
    error: str = ""
    attempts: int = 0
    max_attempts: int = 1
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, raw: str) -> "Job":
        return cls(**json.loads(raw))


class JobStore:
    """Persistent job table backed by Redis with an in-process fallback.

    This is the queryable process table. `list()` gives you the equivalent of `ps` —
    everything the system is doing or recently did.
    """

    def __init__(self):
        self._redis = None
        self._redis_loop = None       # the event loop the client is bound to
        self._use_redis = False
        self._local: dict[str, Job] = {}
        self._local_order: list[str] = []
        self._lock = asyncio.Lock()

    async def initialize(self):
        # Probe Redis availability, but DON'T hold the connection — the async redis
        # client binds to the loop it was created on, and this app starts subsystems
        # across several threads/loops. We connect lazily per running loop instead.
        try:
            import redis.asyncio as aioredis

            probe = aioredis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            await probe.ping()
            await probe.aclose()
            self._use_redis = True
            log.info("jobstore.redis_ready")
        except Exception as e:
            self._use_redis = False
            log.warning("jobstore.redis_unavailable_local_mode", error=str(e))

    async def _client(self):
        """Return a redis client bound to the CURRENT running loop.

        If the loop changed since the client was created (different thread/loop), we
        rebuild it. This avoids 'Event loop is closed' when the API and kernel run on
        separate loops.
        """
        if not self._use_redis:
            return None
        import redis.asyncio as aioredis

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if self._redis is None or self._redis_loop is not loop:
            self._redis = aioredis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            self._redis_loop = loop
        return self._redis

    # ─── Persistence helpers ──────────────────────────────────

    async def _save(self, job: Job):
        job.updated_at = _now()
        client = await self._client()
        if client is not None:
            pipe = client.pipeline()
            pipe.set(f"{JOB_KEY_PREFIX}{job.id}", job.to_json())
            pipe.zadd(JOB_INDEX_KEY, {job.id: datetime.fromisoformat(job.created_at).timestamp()})
            # Trim the index so it does not grow without bound.
            pipe.zremrangebyrank(JOB_INDEX_KEY, 0, -(MAX_INDEX + 1))
            await pipe.execute()
        else:
            async with self._lock:
                if job.id not in self._local:
                    self._local_order.append(job.id)
                self._local[job.id] = job
                if len(self._local_order) > MAX_INDEX:
                    evicted = self._local_order[:-MAX_INDEX]
                    self._local_order = self._local_order[-MAX_INDEX:]
                    for jid in evicted:
                        self._local.pop(jid, None)

    async def _emit_state(self, job: Job):
        """Announce a lifecycle change on the event bus (best-effort)."""
        try:
            from htc_agents.kernel.events import event_bus, EventType

            await event_bus.emit(
                EventType.JOB_STATE_CHANGED,
                payload={"job_id": job.id, "status": job.status, "agent": job.agent, "kind": job.kind},
                source="jobstore",
            )
        except Exception:
            # The bus may not be running yet during early startup — that's fine.
            pass

    # ─── Lifecycle API ────────────────────────────────────────

    async def create(
        self,
        kind: str,
        agent: str = "",
        trigger: str = "",
        payload: dict[str, Any] | None = None,
        max_attempts: int = 1,
    ) -> Job:
        job = Job(
            kind=kind,
            agent=agent,
            trigger=trigger,
            payload=payload or {},
            max_attempts=max_attempts,
        )
        await self._save(job)
        log.info("job.created", job_id=job.id, kind=kind, agent=agent, trigger=trigger)
        return job

    async def get(self, job_id: str) -> Job | None:
        client = await self._client()
        if client is not None:
            raw = await client.get(f"{JOB_KEY_PREFIX}{job_id}")
            return Job.from_json(raw) if raw else None
        return self._local.get(job_id)

    async def _transition(self, job_id: str, status: JobStatus, **fields) -> Job | None:
        job = await self.get(job_id)
        if not job:
            log.warning("job.not_found", job_id=job_id)
            return None
        job.status = status.value
        for k, v in fields.items():
            setattr(job, k, v)
        await self._save(job)
        log.info("job.transition", job_id=job_id, status=status.value)
        await self._emit_state(job)
        return job

    async def mark_running(self, job_id: str) -> Job | None:
        job = await self.get(job_id)
        attempts = (job.attempts + 1) if job else 1
        return await self._transition(job_id, JobStatus.RUNNING, attempts=attempts)

    async def mark_waiting(self, job_id: str, reason: str = "") -> Job | None:
        return await self._transition(job_id, JobStatus.WAITING, error=reason)

    async def mark_done(self, job_id: str, result: str = "") -> Job | None:
        return await self._transition(job_id, JobStatus.DONE, result=result, error="")

    async def mark_failed(self, job_id: str, error: str = "") -> Job | None:
        return await self._transition(job_id, JobStatus.FAILED, error=error)

    async def cancel(self, job_id: str) -> Job | None:
        return await self._transition(job_id, JobStatus.CANCELLED)

    # ─── Query API (the `ps` for the campaign OS) ─────────────

    async def list(self, limit: int = 50, status: str | None = None) -> list[dict[str, Any]]:
        """Return the most recent jobs, newest first, optionally filtered by status."""
        jobs: list[Job] = []

        client = await self._client()
        if client is not None:
            ids = await client.zrevrange(JOB_INDEX_KEY, 0, limit * 2)
            if ids:
                raws = await client.mget([f"{JOB_KEY_PREFIX}{i}" for i in ids])
                jobs = [Job.from_json(r) for r in raws if r]
        else:
            for jid in reversed(self._local_order):
                job = self._local.get(jid)
                if job:
                    jobs.append(job)

        if status:
            jobs = [j for j in jobs if j.status == status]
        return [asdict(j) for j in jobs[:limit]]

    async def summary(self) -> dict[str, int]:
        """Counts by status — a one-glance health view of the process table."""
        counts: dict[str, int] = {s.value: 0 for s in JobStatus}
        for job in await self.list(limit=MAX_INDEX):
            counts[job["status"]] = counts.get(job["status"], 0) + 1
        return counts


# Singleton
job_store = JobStore()
