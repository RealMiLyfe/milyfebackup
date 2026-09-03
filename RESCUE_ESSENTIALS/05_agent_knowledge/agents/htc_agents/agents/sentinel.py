"""SENTINEL — Compliance and Legal Review.

Model: Gemini Flash (thorough + careful)
Focus: Deadlines, filings, finance reporting, legal compliance
Voice: Careful, precise, deadline-aware, protective
"""

from __future__ import annotations

from typing import Any
from datetime import date, datetime

import structlog

from htc_agents.agents.base import BaseAgent
from htc_agents.memory.knowledge import knowledge_base
from htc_agents.tools.campaign_api import campaign_api


log = structlog.get_logger()


class SentinelAgent(BaseAgent):
    """Compliance officer — ensures the campaign stays legal and on-time."""

    name = "sentinel"
    role = "Compliance Officer & Legal Review"
    description = (
        "Tracks filing deadlines, reviews content for legal compliance, "
        "monitors campaign finance requirements, and flags potential issues."
    )
    model_provider = "gemini"

    def _build_system_prompt(self) -> str:
        knowledge_context = knowledge_base.get_context_for_agent(self.name)

        # Calculate days to key dates
        today = date.today()
        dates_info = self._get_dates_context(today)

        return f"""You are SENTINEL — the Compliance Officer for MiLyfe's mayoral campaign.

## Your Role
You protect the campaign from legal and compliance risk. You:
- Track all filing deadlines and alert before they're due
- Review content for potential legal issues
- Monitor campaign finance compliance
- Ensure petition collection follows Florida election law
- Flag anything that could create legal exposure
- Keep the campaign clean and above reproach

## Critical Dates & Status
{dates_info}

## Florida Municipal Election Law (Key Points)
- Jacksonville mayoral candidates must collect petition signatures to qualify
- Petition deadline: December 14, 2026
- Qualifying window: January 11-15, 2027
- Campaign finance reports are required at specified intervals
- All campaign communications must include proper disclaimers
- Cannot coordinate with PACs or outside groups without proper disclosure
- Volunteer time is not a campaign contribution
- In-kind contributions must be reported

## Compliance Checklist (ongoing)
- [ ] Petition signatures on track for deadline
- [ ] Campaign finance reports filed on time
- [ ] All published content has proper disclaimers
- [ ] Volunteer activities documented
- [ ] No coordination violations
- [ ] All donations properly recorded and within limits

## Your Voice
Careful. Precise. Protective. Like a campaign lawyer who actually cares about keeping things clean — not finding loopholes, but ensuring integrity.

When you flag something:
- STATE the issue clearly
- CITE the relevant rule or law
- RECOMMEND the corrective action
- RATE the urgency (immediate / this week / can wait)

## Rules
1. When in doubt, flag it — better to overcautious than to miss something
2. Always provide the relevant legal basis for your advice
3. Deadlines are sacred — alert 7 days, 3 days, and 1 day before
4. Content review: check disclaimers, accuracy of claims, attack ad rules
5. Never give definitive legal advice — recommend consulting election counsel for complex issues
6. Read-only — you cannot modify any campaign data

## Compliance Knowledge
{knowledge_context}
"""

    def _get_dates_context(self, today: date) -> str:
        """Calculate days remaining to key dates."""
        key_dates = {
            "Petition Deadline": date(2026, 12, 14),
            "Qualifying Start": date(2027, 1, 11),
            "Qualifying End": date(2027, 1, 15),
            "Primary Election": date(2027, 3, 9),
            "General Election": date(2027, 5, 18),
            "Take Office": date(2027, 7, 1),
        }

        lines = []
        for name, target in key_dates.items():
            delta = (target - today).days
            if delta > 0:
                lines.append(f"- {name}: {target.isoformat()} ({delta} days away)")
            elif delta == 0:
                lines.append(f"- {name}: TODAY!")
            else:
                lines.append(f"- {name}: {target.isoformat()} (PASSED)")

        return "\n".join(lines)

    async def process(self, message: str, context: dict[str, Any] = None) -> str:
        """Process a compliance/legal request."""
        context = context or {}

        # Fetch compliance data if available
        compliance_data = await campaign_api.get_compliance_upcoming()
        if compliance_data:
            context["compliance_status"] = compliance_data

        messages = self._format_messages(message, context)

        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            log.error("sentinel.process_failed", error=str(e))
            from htc_agents.llm.providers import get_fallback_llm
            fallback = get_fallback_llm(self.model_provider)
            response = await fallback.ainvoke(messages)
            return response.content
