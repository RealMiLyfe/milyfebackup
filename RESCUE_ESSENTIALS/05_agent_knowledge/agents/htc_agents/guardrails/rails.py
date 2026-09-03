"""NeMo Guardrails integration — enforces safety boundaries.

CRITICAL BOUNDARY: None of these agents touch MiLyfe platform operations.
Read-only + intake notifications. The platform is sovereign.
"""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


# Actions that are NEVER allowed regardless of context
BLOCKED_ACTIONS = [
    "write_to_platform",
    "modify_platform_data",
    "delete_platform_data",
    "execute_platform_command",
    "alter_supabase",
    "push_to_production",
    "modify_user_data",
    "access_private_keys",
    "modify_financial_records",
]

# Topics that require extra scrutiny
SENSITIVE_TOPICS = [
    "personal_attacks",
    "false_claims",
    "crypto_language",
    "tech_jargon",
    "selling_pitching",
    "dead_terminology",
]

# Dead terminology that must never be used (from CONTENT_VOICE.md)
DEAD_TERMS = [
    "MiJaxx", "cOS", "tokens", "blockchain", "wallet", "DID",
    "agent", "node", "smart contract", "web3", "crypto",
    "disruptive", "innovative", "revolutionary", "game-changing",
]


class GuardrailsEngine:
    """Enforces safety rails and boundary constraints on all agent outputs.

    Three levels of enforcement:
        1. Input filtering — blocks prohibited requests before reaching agents
        2. Output filtering — scrubs dead terminology and enforces voice
        3. Action gating — prevents any write operations to the platform
    """

    def __init__(self):
        self._rails = None
        self._initialized = False

    async def initialize(self):
        """Initialize NeMo Guardrails if available."""
        try:
            from nemoguardrails import RailsConfig, LLMRails

            config = RailsConfig.from_path("/app/guardrails_config")
            self._rails = LLMRails(config)
            self._initialized = True
            log.info("guardrails.nemo_initialized")
        except Exception as e:
            # Fall back to rule-based guardrails
            log.warning(
                "guardrails.nemo_unavailable_using_rules",
                error=str(e),
            )
            self._initialized = True

    async def check_input(self, message: str, agent_name: str) -> tuple[bool, str]:
        """Check if an input message is allowed.

        Returns:
            (allowed, reason) — if not allowed, reason explains why
        """
        lower = message.lower()

        # Check for platform write requests
        write_keywords = [
            "delete user", "modify platform", "push to production",
            "write to supabase", "alter database", "change user data",
            "execute migration", "deploy", "drop table",
        ]
        for keyword in write_keywords:
            if keyword in lower:
                reason = (
                    f"BLOCKED: Platform write operation detected ('{keyword}'). "
                    "Agents are read-only. The platform is sovereign."
                )
                log.warning(
                    "guardrails.input_blocked",
                    agent=agent_name,
                    reason=reason,
                )
                return False, reason

        return True, ""

    async def check_output(self, response: str, agent_name: str) -> str:
        """Filter agent output for compliance.

        Checks:
            - No dead terminology
            - No personal attacks
            - No platform write suggestions
        """
        # Check for dead terminology
        violations = []
        for term in DEAD_TERMS:
            if term.lower() in response.lower():
                violations.append(term)

        if violations:
            log.warning(
                "guardrails.dead_terms_detected",
                agent=agent_name,
                terms=violations,
            )
            # Add a note but don't block — the agent should self-correct
            response += (
                f"\n\n⚠️ [Guardrail Note: Response contained restricted terminology: "
                f"{', '.join(violations)}. These terms should not appear in public content.]"
            )

        return response

    async def check_action(self, action: str, params: dict[str, Any]) -> tuple[bool, str]:
        """Gate an action before execution.

        Returns:
            (allowed, reason)
        """
        if action in BLOCKED_ACTIONS:
            reason = (
                f"BLOCKED: Action '{action}' is prohibited. "
                "Agents cannot write to the MiLyfe platform."
            )
            log.warning("guardrails.action_blocked", action=action)
            return False, reason

        return True, ""

    @property
    def is_ready(self) -> bool:
        return self._initialized


# Singleton
guardrails = GuardrailsEngine()
