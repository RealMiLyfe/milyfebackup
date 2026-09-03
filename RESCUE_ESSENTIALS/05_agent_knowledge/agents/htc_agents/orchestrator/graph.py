"""LangGraph orchestrator — the central state machine that coordinates all agents."""

from __future__ import annotations

from typing import Any, TypedDict

import structlog
from langgraph.graph import StateGraph, END

from htc_agents.orchestrator.state import (
    AgentRole,
    OrchestratorState,
    TaskPriority,
    TaskStatus,
)
from htc_agents.orchestrator.router import classify_intent
from htc_agents.guardrails.rails import guardrails
from htc_agents.memory.manager import MemoryManager
from htc_agents.memory.knowledge import knowledge_base


log = structlog.get_logger()


class GraphState(TypedDict):
    """TypedDict for LangGraph state."""

    message: str
    source_channel: str
    user_id: str
    primary_agent: str | None
    secondary_agents: list[str]
    priority: str
    intent: str
    status: str
    agent_responses: dict[str, str]
    current_agent: str
    final_response: str
    actions_taken: list[str]
    guardrail_flags: list[str]
    requires_human_review: bool
    error: str
    context: dict[str, Any]


class Orchestrator:
    """The central orchestrator — LangGraph state machine.

    Flow:
        1. INTAKE → receive message, check guardrails
        2. ROUTE → classify intent, select agent(s)
        3. EXECUTE → invoke primary agent
        4. REVIEW → check output guardrails, invoke secondary agents if needed
        5. SYNTHESIZE → combine responses, resolve conflicts
        6. DELIVER → format and return final response
    """

    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self._agents: dict[str, Any] = {}
        self._graph = None

    def register_agents(self, agents: dict[str, Any]):
        """Register all agent instances."""
        self._agents = agents
        log.info("orchestrator.agents_registered", count=len(agents))

    def build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(GraphState)

        # Add nodes
        workflow.add_node("intake", self._node_intake)
        workflow.add_node("route", self._node_route)
        workflow.add_node("execute_primary", self._node_execute_primary)
        workflow.add_node("execute_secondary", self._node_execute_secondary)
        workflow.add_node("synthesize", self._node_synthesize)
        workflow.add_node("deliver", self._node_deliver)
        workflow.add_node("error_handler", self._node_error_handler)

        # Set entry point
        workflow.set_entry_point("intake")

        # Add edges
        workflow.add_edge("intake", "route")
        workflow.add_conditional_edges(
            "route",
            self._should_proceed,
            {
                "proceed": "execute_primary",
                "blocked": "error_handler",
            },
        )
        workflow.add_conditional_edges(
            "execute_primary",
            self._needs_secondary,
            {
                "yes": "execute_secondary",
                "no": "synthesize",
                "error": "error_handler",
            },
        )
        workflow.add_edge("execute_secondary", "synthesize")
        workflow.add_edge("synthesize", "deliver")
        workflow.add_edge("deliver", END)
        workflow.add_edge("error_handler", END)

        self._graph = workflow.compile()
        log.info("orchestrator.graph_compiled")
        return self._graph

    async def process(
        self,
        message: str,
        source_channel: str = "",
        user_id: str = "",
    ) -> str:
        """Process a message through the full orchestrator pipeline.

        Args:
            message: The incoming message
            source_channel: Which Mattermost channel it came from
            user_id: Who sent it

        Returns:
            The final response string
        """
        if not self._graph:
            self.build_graph()

        initial_state: GraphState = {
            "message": message,
            "source_channel": source_channel,
            "user_id": user_id,
            "primary_agent": None,
            "secondary_agents": [],
            "priority": "normal",
            "intent": "",
            "status": "pending",
            "agent_responses": {},
            "current_agent": "",
            "final_response": "",
            "actions_taken": [],
            "guardrail_flags": [],
            "requires_human_review": False,
            "error": "",
            "context": {},
        }

        try:
            result = await self._graph.ainvoke(initial_state)
            return result.get("final_response", "I couldn't process that request.")
        except Exception as e:
            log.error("orchestrator.process_failed", error=str(e))
            return f"System error: {str(e)}. The Guardian agent has been notified."

    # ─── Graph Nodes ──────────────────────────────────────────

    async def _node_intake(self, state: GraphState) -> GraphState:
        """Intake node — receive and validate the message."""
        message = state["message"]
        log.info("orchestrator.intake", message_length=len(message))

        # Check input guardrails
        allowed, reason = await guardrails.check_input(message, "orchestrator")
        if not allowed:
            state["status"] = "failed"
            state["error"] = reason
            state["guardrail_flags"].append(reason)

        state["status"] = "routing"
        return state

    async def _node_route(self, state: GraphState) -> GraphState:
        """Route node — classify intent and select agents."""
        message = state["message"]

        # Classify
        primary, priority, intent, secondary = classify_intent(message)

        state["primary_agent"] = primary.value
        state["secondary_agents"] = [a.value for a in secondary]
        state["priority"] = priority.value
        state["intent"] = intent
        state["status"] = "in_progress"

        log.info(
            "orchestrator.routed",
            primary=primary.value,
            secondary=[a.value for a in secondary],
            priority=priority.value,
            intent=intent,
        )

        return state

    async def _node_execute_primary(self, state: GraphState) -> GraphState:
        """Execute the primary agent."""
        agent_name = state["primary_agent"]
        message = state["message"]

        if agent_name not in self._agents:
            state["error"] = f"Agent '{agent_name}' not found"
            state["status"] = "failed"
            return state

        agent = self._agents[agent_name]
        state["current_agent"] = agent_name

        try:
            response = await agent.invoke(
                message=message,
                context=state["context"],
            )

            # Check output guardrails
            response = await guardrails.check_output(response, agent_name)

            state["agent_responses"][agent_name] = response
            state["actions_taken"].append(f"primary:{agent_name}")

            log.info(
                "orchestrator.primary_complete",
                agent=agent_name,
                response_length=len(response),
            )

        except Exception as e:
            log.error(
                "orchestrator.primary_failed",
                agent=agent_name,
                error=str(e),
            )
            state["error"] = f"Agent '{agent_name}' failed: {str(e)}"
            state["status"] = "failed"

        return state

    async def _node_execute_secondary(self, state: GraphState) -> GraphState:
        """Execute secondary agents for additional context or review."""
        for agent_name in state["secondary_agents"]:
            if agent_name not in self._agents:
                continue

            agent = self._agents[agent_name]

            try:
                # Give secondary agents the original message plus primary response
                primary_response = state["agent_responses"].get(
                    state["primary_agent"], ""
                )
                context = {
                    **state["context"],
                    "primary_agent": state["primary_agent"],
                    "primary_response": primary_response,
                }

                response = await agent.invoke(
                    message=state["message"],
                    context=context,
                )

                response = await guardrails.check_output(response, agent_name)
                state["agent_responses"][agent_name] = response
                state["actions_taken"].append(f"secondary:{agent_name}")

                log.info(
                    "orchestrator.secondary_complete",
                    agent=agent_name,
                )

            except Exception as e:
                log.warning(
                    "orchestrator.secondary_failed",
                    agent=agent_name,
                    error=str(e),
                )
                # Secondary failures are non-fatal

        return state

    async def _node_synthesize(self, state: GraphState) -> GraphState:
        """Synthesize responses from all agents into a final answer."""
        responses = state["agent_responses"]

        if not responses:
            state["final_response"] = "No agents produced a response."
            state["status"] = "failed"
            return state

        # Single agent — just use their response directly
        if len(responses) == 1:
            state["final_response"] = list(responses.values())[0]
            state["status"] = "complete"
            return state

        # Multiple agents — combine with attribution
        primary = state["primary_agent"]
        primary_response = responses.get(primary, "")

        # Build combined response
        parts = [primary_response]

        for agent_name, response in responses.items():
            if agent_name == primary:
                continue
            # Only add secondary if it provides distinct value
            if response and response != primary_response:
                parts.append(f"\n\n**[{agent_name.title()} adds]:** {response}")

        state["final_response"] = "\n".join(parts)
        state["status"] = "complete"

        log.info(
            "orchestrator.synthesized",
            agents_used=list(responses.keys()),
        )

        return state

    async def _node_deliver(self, state: GraphState) -> GraphState:
        """Final delivery — format and prepare the response."""
        # Store the interaction in memory
        if self.memory:
            await self.memory.store(
                content=(
                    f"Channel: {state['source_channel']}\n"
                    f"Message: {state['message']}\n"
                    f"Intent: {state['intent']}\n"
                    f"Agent: {state['primary_agent']}\n"
                    f"Response: {state['final_response'][:500]}"
                ),
                agent_name="orchestrator",
                metadata={
                    "intent": state["intent"],
                    "primary_agent": state["primary_agent"],
                    "priority": state["priority"],
                },
            )

        state["status"] = "complete"
        return state

    async def _node_error_handler(self, state: GraphState) -> GraphState:
        """Handle errors gracefully."""
        error = state.get("error", "Unknown error")

        state["final_response"] = (
            f"⚠️ I couldn't complete that request.\n\n"
            f"**Reason:** {error}\n\n"
            f"If this is urgent, tag the specific agent directly "
            f"(e.g., 'strategy: ...' or 'scout: ...')."
        )
        state["status"] = "failed"

        log.error("orchestrator.error", error=error)
        return state

    # ─── Conditional Edge Functions ───────────────────────────

    def _should_proceed(self, state: GraphState) -> str:
        """Check if routing should proceed or is blocked."""
        if state.get("error") or state["status"] == "failed":
            return "blocked"
        return "proceed"

    def _needs_secondary(self, state: GraphState) -> str:
        """Check if secondary agents should be invoked."""
        if state.get("error") or state["status"] == "failed":
            return "error"
        if state.get("secondary_agents"):
            return "yes"
        return "no"
