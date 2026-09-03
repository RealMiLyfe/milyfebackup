"""Agent Chain System — multi-agent pipelines with handoffs.

Chains allow agents to build on each other's work in sequence.
Each agent in the chain receives the original message PLUS all prior agent outputs.

Example chains:
    - Rapid Response: scout → crisis_manager → storyteller → sentinel
    - Morning Brief: scout + analyst → commander → storyteller
    - Content Pipeline: storyteller → sentinel → media_coach
    - Debate Prep: oppo_tracker → debate_coach → speechwriter
    - Field Strategy: ground_game → scheduler → connector
"""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.memory.manager import MemoryManager


log = structlog.get_logger()


# ═══════════════════════════════════════════════════════════════
# PREDEFINED CHAINS
# ═══════════════════════════════════════════════════════════════

PREDEFINED_CHAINS = {
    "rapid_response": {
        "description": "Breaking news → crisis assessment → response draft → compliance check",
        "agents": ["scout", "crisis_manager", "storyteller", "sentinel"],
    },
    "morning_brief": {
        "description": "Intel gathering → performance data → strategic synthesis",
        "agents": ["scout", "analyst", "commander"],
    },
    "content_pipeline": {
        "description": "Draft content → compliance check → media formatting",
        "agents": ["storyteller", "sentinel", "media_coach"],
    },
    "debate_prep": {
        "description": "Opponent intel → attack simulation → answer crafting",
        "agents": ["oppo_tracker", "debate_coach", "speechwriter"],
    },
    "field_strategy": {
        "description": "Precinct analysis → schedule optimization → volunteer assignment",
        "agents": ["ground_game", "scheduler", "connector"],
    },
    "fundraise_campaign": {
        "description": "Donor research → ask email draft → compliance review",
        "agents": ["fundraiser", "storyteller", "sentinel"],
    },
    "endorsement_push": {
        "description": "Org mapping → outreach strategy → talking points",
        "agents": ["coalition_builder", "connector", "speechwriter"],
    },
    "opponent_deep_dive": {
        "description": "Network mapping → vulnerability analysis → counter-narrative",
        "agents": ["oppo_tracker", "scout", "crisis_manager"],
    },
    "weekly_retro": {
        "description": "Performance metrics → trend analysis → strategic recommendations",
        "agents": ["analyst", "ground_game", "commander"],
    },
    "speech_prep": {
        "description": "Issue research → speech draft → debate scoring",
        "agents": ["pollster", "speechwriter", "debate_coach"],
    },
}


async def run_chain(
    message: str,
    chain: list[str],
    agents: dict[str, Any],
    memory: MemoryManager | None = None,
) -> dict[str, Any]:
    """Execute a multi-agent chain.

    Each agent receives:
        - The original message
        - All prior agent outputs as context
        - A directive explaining their role in the chain

    Returns:
        {
            "chain": ["agent1", "agent2", ...],
            "steps": [{"agent": "name", "output": "response"}, ...],
            "final_response": "last agent's output",
            "success": bool
        }
    """
    steps = []
    accumulated_context = []

    for i, agent_name in enumerate(chain):
        if agent_name not in agents:
            log.warning("chain.agent_not_found", agent=agent_name)
            continue

        agent = agents[agent_name]

        # Build chain context for this agent
        context = {
            "chain_position": f"Step {i + 1} of {len(chain)}",
            "chain_agents": chain,
            "prior_outputs": accumulated_context.copy(),
        }

        # Build the enhanced message with chain context
        if accumulated_context:
            chain_prompt = (
                f"[CHAIN MODE — You are step {i + 1} of {len(chain)} in a multi-agent pipeline]\n"
                f"[Chain: {' → '.join(chain)}]\n"
                f"[Prior agent outputs below — build on their work, don't repeat it]\n\n"
            )
            for prior in accumulated_context:
                chain_prompt += f"--- {prior['agent'].upper()} said ---\n{prior['output'][:1000]}\n\n"
            chain_prompt += f"--- Original request ---\n{message}\n\n"
            chain_prompt += f"[Your job as {agent_name}: add YOUR unique expertise to this chain]"
            enhanced_message = chain_prompt
        else:
            enhanced_message = message

        try:
            response = await agent.invoke(message=enhanced_message, context=context)
            steps.append({"agent": agent_name, "output": response})
            accumulated_context.append({"agent": agent_name, "output": response})

            log.info(
                "chain.step_complete",
                agent=agent_name,
                step=i + 1,
                total=len(chain),
            )

        except Exception as e:
            log.error("chain.step_failed", agent=agent_name, error=str(e))
            steps.append({"agent": agent_name, "output": f"[FAILED: {str(e)}]"})

    # Store the chain interaction in memory
    if memory and steps:
        await memory.store(
            content=f"Chain: {' → '.join(chain)}\nMessage: {message}\nResult: {steps[-1]['output'][:500]}",
            agent_name="chain_orchestrator",
            metadata={"chain": chain, "steps": len(steps)},
        )

    return {
        "chain": chain,
        "steps": steps,
        "final_response": steps[-1]["output"] if steps else "Chain produced no output.",
        "success": len(steps) == len(chain),
    }


async def run_predefined_chain(
    chain_name: str,
    message: str,
    agents: dict[str, Any],
    memory: MemoryManager | None = None,
) -> dict[str, Any]:
    """Run a predefined chain by name."""
    if chain_name not in PREDEFINED_CHAINS:
        return {
            "error": f"Unknown chain: {chain_name}",
            "available": list(PREDEFINED_CHAINS.keys()),
        }

    chain_config = PREDEFINED_CHAINS[chain_name]
    return await run_chain(message, chain_config["agents"], agents, memory)
