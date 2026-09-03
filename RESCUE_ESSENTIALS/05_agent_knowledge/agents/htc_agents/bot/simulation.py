"""Simulation Mode — autonomous drills and tabletop exercises.

Agents work TOGETHER without human in the loop:
- Debate simulations: DEBATE_COACH attacks, SPEECHWRITER defends, both score
- Crisis tabletops: CRISIS_MANAGER presents scenario, agents respond as a team
- Content sprints: STORYTELLER + MEDIA_COACH produce a week of content
- Strategy war games: COMMANDER makes decisions, ANALYST evaluates outcomes

Results are posted as transcripts for human review.
"""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.tools.notify import post_to_channel


log = structlog.get_logger()


async def run_debate_simulation(
    topic: str,
    rounds: int = 3,
    agents: dict[str, Any] = None,
    memory: Any = None,
) -> str:
    """Run autonomous debate simulation.

    DEBATE_COACH throws attacks → SPEECHWRITER crafts answers → DEBATE_COACH scores.
    """
    if not agents:
        return "No agents available."

    debate_coach = agents.get("debate_coach")
    speechwriter = agents.get("speechwriter")

    if not debate_coach or not speechwriter:
        return "Need both debate_coach and speechwriter for simulation."

    transcript = f"## 🎯 Debate Simulation: {topic}\n\n"

    for round_num in range(1, rounds + 1):
        transcript += f"### Round {round_num}\n\n"

        # Coach throws an attack
        attack_prompt = (
            f"You're simulating an opponent in a debate about: {topic}. "
            f"This is round {round_num} of {rounds}. "
            f"Throw a challenging question or attack that a Jacksonville mayoral opponent would use. "
            f"Make it HARD. One question only, 2 sentences max."
        )
        attack = await debate_coach.invoke(message=attack_prompt, context={})
        transcript += f"**🎤 Opponent:** {attack}\n\n"

        # Speechwriter crafts the response
        response_prompt = (
            f"You're MiLyfe in a debate. The opponent just said:\n\n\"{attack}\"\n\n"
            f"Craft a 60-second response. Use the formula: acknowledge → pivot → proof → close strong."
        )
        answer = await speechwriter.invoke(message=response_prompt, context={})
        transcript += f"**💬 MiLyfe:** {answer}\n\n"

        # Coach scores
        score_prompt = (
            f"Score this debate answer on 5 criteria (1-10 each):\n"
            f"Question: \"{attack}\"\n"
            f"Answer: \"{answer}\"\n\n"
            f"Score: CLARITY | PERSUASION | BREVITY | PIVOT | STORY\n"
            f"Give scores and one sentence of feedback. Be tough."
        )
        score = await debate_coach.invoke(message=score_prompt, context={})
        transcript += f"**📊 Score:** {score}\n\n---\n\n"

    # Post transcript to debate-prep channel
    await post_to_channel("debate-prep", transcript)

    log.info("simulation.debate_complete", topic=topic, rounds=rounds)
    return transcript


async def run_crisis_tabletop(
    scenario: str,
    agents: dict[str, Any] = None,
    memory: Any = None,
) -> str:
    """Run a crisis tabletop exercise.

    CRISIS_MANAGER presents scenario → each relevant agent responds with their action.
    """
    if not agents:
        return "No agents available."

    crisis = agents.get("crisis_manager")
    if not crisis:
        return "Need crisis_manager for tabletop."

    transcript = f"## 🚨 Crisis Tabletop: {scenario}\n\n"

    # Crisis manager assesses
    assessment = await crisis.invoke(
        f"A crisis has hit the campaign: {scenario}\n\n"
        f"Assess the threat level (1-4), identify the attack vector, "
        f"and outline the immediate response protocol.",
        context={},
    )
    transcript += f"**🛡️ Crisis Manager Assessment:**\n{assessment}\n\n---\n\n"

    # Each relevant agent responds
    responders = [
        ("storyteller", "Draft the public response statement for this crisis."),
        ("media_coach", "How do we handle media inquiries about this? Who do we call first?"),
        ("sentinel", "Are there any legal/compliance concerns with our response?"),
        ("coalition_builder", "Which allies should we activate? Who calls whom?"),
    ]

    for agent_name, prompt in responders:
        agent = agents.get(agent_name)
        if agent:
            response = await agent.invoke(
                f"CRISIS SCENARIO: {scenario}\n\n"
                f"Crisis Manager says: {assessment[:500]}\n\n"
                f"Your job: {prompt}",
                context={"crisis_mode": True},
            )
            display_name = agent_name.replace("_", " ").title()
            transcript += f"**{display_name}:**\n{response}\n\n---\n\n"

    # Post to crisis channel
    await post_to_channel("crisis-response", transcript)

    log.info("simulation.tabletop_complete", scenario=scenario[:50])
    return transcript


async def run_content_sprint(
    theme: str,
    platforms: list[str] = None,
    agents: dict[str, Any] = None,
    memory: Any = None,
) -> str:
    """Run a content sprint — produce multiple platform posts on a theme.

    STORYTELLER drafts → SENTINEL reviews → MEDIA_COACH formats for distribution.
    """
    if not agents:
        return "No agents available."

    platforms = platforms or ["linkedin", "twitter", "blog"]
    storyteller = agents.get("storyteller")
    sentinel = agents.get("sentinel")
    media_coach = agents.get("media_coach")

    transcript = f"## ✍️ Content Sprint: {theme}\n\n"

    for platform in platforms:
        transcript += f"### {platform.title()}\n\n"

        # Storyteller drafts
        if storyteller:
            draft = await storyteller.invoke(
                f"Write a {platform} post about: {theme}. "
                f"Follow the content voice guide exactly. One post only.",
                context={"platform": platform},
            )
            transcript += f"**Draft:**\n{draft}\n\n"

            # Sentinel reviews
            if sentinel:
                review = await sentinel.invoke(
                    f"Review this {platform} post for compliance issues:\n\n{draft}\n\n"
                    f"Check: disclaimers needed? Claims verifiable? Any legal risk?",
                    context={},
                )
                transcript += f"**Compliance:** {review}\n\n"

        transcript += "---\n\n"

    # Media coach wraps up with distribution plan
    if media_coach:
        plan = await media_coach.invoke(
            f"We just produced content on '{theme}' for {', '.join(platforms)}. "
            f"What's the optimal posting schedule and any media pitch angles?",
            context={},
        )
        transcript += f"### Distribution Plan\n{plan}\n\n"

    await post_to_channel("content", transcript)
    log.info("simulation.content_sprint", theme=theme, platforms=platforms)
    return transcript
