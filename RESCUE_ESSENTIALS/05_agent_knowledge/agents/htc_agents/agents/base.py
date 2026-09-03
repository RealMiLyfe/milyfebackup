"""Base agent class — shared behavior for all HTC agents."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import structlog
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from htc_agents.config import settings
from htc_agents.memory.manager import MemoryManager


log = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all campaign agents."""

    # Override in subclass
    name: str = "base"
    role: str = "Base Agent"
    description: str = ""
    model_provider: str = ""  # nvidia, gemini, groq, anthropic, ollama

    def __init__(self, memory: MemoryManager | None = None):
        self.memory = memory
        self._llm = None
        self._system_prompt = self._build_system_prompt()

    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build the system prompt for this agent."""
        ...

    @abstractmethod
    async def process(self, message: str, context: dict[str, Any] = None) -> str:
        """Process a message and return a response."""
        ...

    @property
    def llm(self):
        """Lazy-load the LLM for this agent."""
        if self._llm is None:
            self._llm = self._create_llm()
        return self._llm

    def _create_llm(self):
        """Create the LLM instance based on provider."""
        from htc_agents.llm.providers import get_llm
        return get_llm(self.model_provider)

    async def invoke(self, message: str, context: dict[str, Any] = None) -> str:
        """Full invocation with memory recall and storage."""
        context = context or {}

        # Recall relevant memories
        memories = []
        if self.memory:
            memories = await self.memory.recall(
                query=message,
                agent_name=self.name,
                limit=5,
            )

        # Add memory context
        if memories:
            context["memories"] = memories

        # Process
        response = await self.process(message, context)

        # Store interaction in memory
        if self.memory:
            await self.memory.store(
                content=f"User: {message}\nAgent ({self.name}): {response}",
                agent_name=self.name,
                metadata={"role": self.role},
            )

        log.info(
            "agent.invoked",
            agent=self.name,
            message_length=len(message),
            response_length=len(response),
        )

        return response

    def _format_messages(
        self, message: str, context: dict[str, Any] = None
    ) -> list:
        """Format messages for LLM invocation."""
        # Truncate system prompt for token-limited providers (Groq free tier = 8K TPM)
        system_prompt = self._system_prompt
        if self.model_provider == "groq":
            # ~4 chars per token, keep system prompt under 4000 tokens
            max_chars = 12000
            if len(system_prompt) > max_chars:
                system_prompt = system_prompt[:max_chars] + "\n\n[Context truncated for token limits]"

        messages = [SystemMessage(content=system_prompt)]

        # Add memory context if available
        if context and context.get("memories"):
            memory_text = "\n".join(
                f"- {m}" for m in context["memories"]
            )
            messages.append(
                SystemMessage(
                    content=f"Relevant context from previous interactions:\n{memory_text}"
                )
            )

        # Add conversation history if provided
        if context and context.get("history"):
            for msg in context["history"]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=message))
        return messages
