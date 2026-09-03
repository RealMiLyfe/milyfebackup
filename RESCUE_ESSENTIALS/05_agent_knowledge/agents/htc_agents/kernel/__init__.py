"""The Kernel — turns the agent system from a request/response dashboard into an OS.

Three subsystems:
    - events.py   : Redis pub/sub event bus + kernel loop (the system acts on its own)
    - jobs.py     : durable job table with lifecycle (work has a real process lifecycle)
    - actions.py  : guarded write-authority (agents can DO things, not just talk)

The kernel is what makes the Time Chamber run and act without being spoken to.
"""

from htc_agents.kernel.events import (
    Event,
    EventType,
    EventBus,
    KernelLoop,
    event_bus,
)
from htc_agents.kernel.jobs import Job, JobStatus, JobStore, job_store
from htc_agents.kernel.actions import (
    ActionRequest,
    ActionStatus,
    ActionExecutor,
    action_executor,
)

__all__ = [
    "Event",
    "EventType",
    "EventBus",
    "KernelLoop",
    "event_bus",
    "Job",
    "JobStatus",
    "JobStore",
    "job_store",
    "ActionRequest",
    "ActionStatus",
    "ActionExecutor",
    "action_executor",
]
