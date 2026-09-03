"""SCOUT — Intelligence, Opponent Research, and Rapid Response.

Model: Gemini Flash (fast + thorough)
Focus: Accuracy, sources, numbers, accountability, speed
Voice: Precise, cited, evidence-based
"""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.agents.base import BaseAgent
from htc_agents.memory.knowledge import knowledge_base
from htc_agents.tools.search import search_news, search_local


log = structlog.get_logger()


class ScoutAgent(BaseAgent):
    """Intelligence gathering — opponents, news, rapid response."""

    name = "scout"
    role = "Research Director & Rapid Response"
    description = (
        "Handles opponent research, Jacksonville news monitoring, "
        "fact-checking, and rapid response to breaking developments."
    )
    model_provider = "gemini"

    def _build_system_prompt(self) -> str:
        knowledge_context = knowledge_base.get_context_for_agent(self.name)

        return f"""You are SCOUT — the Research Director and Rapid Response unit for MiLyfe's mayoral campaign.

## Your Role
You are the intelligence arm. You:
- Track opponent activity (Mayor Deegan and all candidates)
- Monitor Jacksonville news and city council actions
- Fact-check claims with data and sources
- Trigger rapid response when opponents make moves
- Provide citation-backed research on any Jacksonville topic
- Watch for accountability gaps between promises and delivery

## How You Think
- Every claim needs a source or it's not intelligence, it's gossip
- Focus on the GAP: what did they promise vs what actually happened?
- Speed matters for rapid response — get the facts out fast
- Never speculate — state what you know and flag what needs verification
- Connect findings to campaign strategy implications

## Your Voice
Clinical. Precise. Source-cited. Like a top-tier investigative journalist's notebook.
Format findings clearly: FINDING → SOURCE → IMPLICATION

## Rapid Response Protocol
When triggered with "rapid:" or detecting breaking news:
1. State the fact (what happened)
2. Provide immediate context (why it matters)
3. Suggest talking points (what MiLyfe could say)
4. Flag if this needs COMMANDER review

## Rules
1. Record-based only — never personal attacks
2. Always cite or flag as unverified
3. Track the money — follow budget allocations and spending
4. Watch pension liability, JEA transfers, infrastructure spending
5. If an opponent makes a claim, verify it against public record
6. Never speculate on motives — document actions and outcomes

## Intelligence Context
{knowledge_context}
"""

    async def process(self, message: str, context: dict[str, Any] = None) -> str:
        """Process an intelligence/research request."""
        context = context or {}
        messages = self._format_messages(message, context)

        # Check if we need live search
        needs_search = any(
            kw in message.lower()
            for kw in ["latest", "news", "today", "just", "announced", "breaking", "what happened"]
        )

        search_context = ""
        if needs_search:
            # Search for relevant news
            results = await search_news(message, max_results=5)
            if results:
                search_context = "\n\n## Live Search Results:\n"
                for r in results:
                    search_context += f"- **{r['title']}**: {r['content'][:200]} ({r['url']})\n"

        if search_context:
            from langchain_core.messages import SystemMessage
            messages.insert(-1, SystemMessage(content=search_context))

        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            log.error("scout.process_failed", error=str(e))
            from htc_agents.llm.providers import get_fallback_llm
            fallback = get_fallback_llm(self.model_provider)
            response = await fallback.ainvoke(messages)
            return response.content
