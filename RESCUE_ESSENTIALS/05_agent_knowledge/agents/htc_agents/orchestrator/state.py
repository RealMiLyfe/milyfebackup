"""Orchestrator state — defines the shared state passed through the graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentRole(str, Enum):
    """Available agent roles for routing."""

    COMMANDER = "commander"
    SCOUT = "scout"
    STORYTELLER = "storyteller"
    SENTINEL = "sentinel"
    CONNECTOR = "connector"
    BUILDER = "builder"
    GUARDIAN = "guardian"
    ANALYST = "analyst"
    DEBATE_COACH = "debate_coach"
    FUNDRAISER = "fundraiser"
    SCHEDULER = "scheduler"
    POLLSTER = "pollster"
    MEDIA_COACH = "media_coach"
    OPPO_TRACKER = "oppo_tracker"
    GROUND_GAME = "ground_game"
    CRISIS_MANAGER = "crisis_manager"
    SPEECHWRITER = "speechwriter"
    COALITION_BUILDER = "coalition_builder"


class TaskPriority(str, Enum):
    """Task priority levels."""

    URGENT = "urgent"       # Rapid response, breaking news
    HIGH = "high"           # Strategy decisions, deadlines
    NORMAL = "normal"       # Standard workflow
    LOW = "low"             # Background tasks, learning


class TaskStatus(str, Enum):
    """Task lifecycle status."""

    PENDING = "pending"
    ROUTING = "routing"
    IN_PROGRESS = "in_progress"
    NEEDS_REVIEW = "needs_review"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class OrchestratorState:
    """State object that flows through the LangGraph orchestrator.

    This is the shared memory for a single request lifecycle.
    """

    # Input
    message: str = ""
    source_channel: str = ""
    user_id: str = ""

    # Routing
    primary_agent: AgentRole | None = None
    secondary_agents: list[AgentRole] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.NORMAL
    intent: str = ""

    # Execution
    status: TaskStatus = TaskStatus.PENDING
    agent_responses: dict[str, str] = field(default_factory=dict)
    current_agent: str = ""

    # Output
    final_response: str = ""
    actions_taken: list[str] = field(default_factory=list)

    # Metadata
    guardrail_flags: list[str] = field(default_factory=list)
    requires_human_review: bool = False
    error: str = ""
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize state for LangGraph."""
        return {
            "message": self.message,
            "source_channel": self.source_channel,
            "user_id": self.user_id,
            "primary_agent": self.primary_agent.value if self.primary_agent else None,
            "secondary_agents": [a.value for a in self.secondary_agents],
            "priority": self.priority.value,
            "intent": self.intent,
            "status": self.status.value,
            "agent_responses": self.agent_responses,
            "current_agent": self.current_agent,
            "final_response": self.final_response,
            "actions_taken": self.actions_taken,
            "guardrail_flags": self.guardrail_flags,
            "requires_human_review": self.requires_human_review,
            "error": self.error,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrchestratorState":
        """Deserialize state from LangGraph."""
        state = cls()
        state.message = data.get("message", "")
        state.source_channel = data.get("source_channel", "")
        state.user_id = data.get("user_id", "")
        state.primary_agent = (
            AgentRole(data["primary_agent"])
            if data.get("primary_agent")
            else None
        )
        state.secondary_agents = [
            AgentRole(a) for a in data.get("secondary_agents", [])
        ]
        state.priority = TaskPriority(data.get("priority", "normal"))
        state.intent = data.get("intent", "")
        state.status = TaskStatus(data.get("status", "pending"))
        state.agent_responses = data.get("agent_responses", {})
        state.current_agent = data.get("current_agent", "")
        state.final_response = data.get("final_response", "")
        state.actions_taken = data.get("actions_taken", [])
        state.guardrail_flags = data.get("guardrail_flags", [])
        state.requires_human_review = data.get("requires_human_review", False)
        state.error = data.get("error", "")
        state.context = data.get("context", {})
        return state
