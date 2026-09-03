"""Knowledge loader — loads brain/ and knowledge/ files for agent context."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


class KnowledgeBase:
    """Loads and provides access to the campaign knowledge base.

    Directories:
        brain/: System prompts, roles, content voice
        knowledge/internal/: Platform architecture, design laws, terminology
        knowledge/external/: Campaign story, numbers, opponents, dates
    """

    def __init__(self):
        self._brain: dict[str, str] = {}
        self._internal: dict[str, str] = {}
        self._external: dict[str, str] = {}

    def load(self):
        """Load all knowledge files into memory."""
        brain_path = settings.brain_path
        knowledge_path = settings.knowledge_path

        # Load brain files
        if brain_path.exists():
            for f in brain_path.glob("*.md"):
                self._brain[f.stem] = f.read_text(encoding="utf-8")
            log.info("knowledge.brain_loaded", count=len(self._brain))

        # Load internal knowledge
        internal_path = knowledge_path / "internal"
        if internal_path.exists():
            for f in internal_path.glob("*.md"):
                self._internal[f.stem] = f.read_text(encoding="utf-8")
            log.info("knowledge.internal_loaded", count=len(self._internal))

        # Load external knowledge
        external_path = knowledge_path / "external"
        if external_path.exists():
            for f in external_path.glob("*.md"):
                self._external[f.stem] = f.read_text(encoding="utf-8")
            log.info("knowledge.external_loaded", count=len(self._external))

    @property
    def system_prompt(self) -> str:
        """The master system prompt from brain/."""
        return self._brain.get("SYSTEM_PROMPT", "")

    @property
    def roles(self) -> str:
        """Role routing guide."""
        return self._brain.get("ROLES", "")

    @property
    def content_voice(self) -> str:
        """Content voice guide."""
        return self._brain.get("CONTENT_VOICE", "")

    def get_external(self, key: str) -> str:
        """Get an external knowledge document by stem name."""
        return self._external.get(key, "")

    def get_internal(self, key: str) -> str:
        """Get an internal knowledge document by stem name."""
        return self._internal.get(key, "")

    def get_all_external(self) -> dict[str, str]:
        """Get all external knowledge documents."""
        return dict(self._external)

    def get_all_internal(self) -> dict[str, str]:
        """Get all internal knowledge documents."""
        return dict(self._internal)

    def get_context_for_agent(self, agent_name: str) -> str:
        """Build a knowledge context block for a specific agent.

        Different agents get different slices of knowledge.
        """
        contexts = {
            "commander": self._commander_context,
            "scout": self._scout_context,
            "storyteller": self._storyteller_context,
            "sentinel": self._sentinel_context,
            "connector": self._connector_context,
            "builder": self._builder_context,
            "guardian": self._guardian_context,
            "analyst": self._analyst_context,
        }

        builder = contexts.get(agent_name, lambda: "")
        return builder()

    def _commander_context(self) -> str:
        parts = [
            self.system_prompt,
            self.get_external("the-argument"),
            self.get_external("the-dates"),
            self.get_external("the-numbers"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _scout_context(self) -> str:
        parts = [
            self.get_external("the-opponent"),
            self.get_external("the-numbers"),
            self.get_external("the-dates"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _storyteller_context(self) -> str:
        parts = [
            self.content_voice,
            self.get_external("the-story"),
            self.get_external("the-platform-human"),
            self.get_external("the-argument"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _sentinel_context(self) -> str:
        parts = [
            self.get_external("the-dates"),
            self.get_external("the-numbers"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _connector_context(self) -> str:
        parts = [
            self.get_external("founding-ten"),
            self.get_external("the-platform-human"),
            self.get_external("the-story"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _builder_context(self) -> str:
        parts = [
            self.get_internal("platform-architecture"),
            self.get_internal("design-laws"),
            self.get_internal("terminology"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)

    def _guardian_context(self) -> str:
        return "System monitoring agent. No campaign knowledge needed."

    def _analyst_context(self) -> str:
        parts = [
            self.get_external("the-numbers"),
            self.get_external("the-dates"),
        ]
        return "\n\n---\n\n".join(p for p in parts if p)


# Singleton
knowledge_base = KnowledgeBase()
