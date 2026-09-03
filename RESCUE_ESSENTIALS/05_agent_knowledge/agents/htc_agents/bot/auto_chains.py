"""Auto-triggered agent chains — fire on events without human intervention.

These chains activate when specific conditions are detected:
- Crisis detection: opponent attack → crisis_manager → storyteller → sentinel
- Content pipeline: scheduled content → storyteller → sentinel → publish queue
- Intel cycle: social scan → scout + oppo_tracker → commander briefing
- Performance loop: weekly metrics → analyst → commander recommendations
"""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.bot.chains import run_chain, run_predefined_chain
from htc_agents.bot.workflows import create_draft, priority_interrupt
from htc_agents.tools.notify import post_to_channel
from htc_agents.tools.social_monitor import run_full_social_scan, store_scan_results


log = structlog.get_logger()


async def auto_crisis_detection(
    message: str,
    agents: dict[str, Any],
    memory: Any = None,
) -> bool:
    """Detect if a message indicates a crisis and auto-trigger the chain.

    Returns True if crisis was detected and chain was triggered.
    """
    crisis_keywords = [
        "attack", "hit piece", "arrest", "scandal", "accusation",
        "negative ad", "opposition research", "smear", "exposed",
        "breaking:", "they're saying", "attack ad",
    ]

    lower = message.lower()
    is_crisis = any(kw in lower for kw in crisis_keywords)

    if not is_crisis:
        return False

    log.info("auto_chain.crisis_detected", trigger=message[:100])

    # Run rapid response chain
    result = await run_predefined_chain(
        "rapid_response",
        message,
        agents,
        memory,
    )

    # Post results to crisis channel
    if result.get("success"):
        response = result["final_response"]
        await post_to_channel(
            "crisis-response",
            f"## 🚨 Auto-Triggered Rapid Response\n\n"
            f"**Trigger:** {message[:200]}\n\n"
            f"**Chain:** scout → crisis_manager → storyteller → sentinel\n\n"
            f"---\n\n{response}",
        )

        # Level 3 interrupt
        await priority_interrupt(
            message=f"Crisis chain auto-triggered: {message[:100]}",
            level=3,
            source_agent="auto_crisis",
        )

    return True


async def auto_content_pipeline(
    topic: str,
    platform: str = "linkedin",
    agents: dict[str, Any] = None,
    memory: Any = None,
):
    """Auto-trigger content pipeline: draft → compliance → queue for approval.

    Called by the scheduler when it's content creation time.
    """
    if not agents:
        return

    log.info("auto_chain.content_pipeline", topic=topic, platform=platform)

    # Storyteller drafts
    storyteller = agents.get("storyteller")
    if not storyteller:
        return

    draft = await storyteller.invoke(
        f"Write a {platform} post about: {topic}. Follow the content voice guide.",
        context={"platform": platform},
    )

    # Sentinel reviews
    sentinel = agents.get("sentinel")
    if sentinel:
        review = await sentinel.invoke(
            f"Review this {platform} post for compliance:\n\n{draft}",
            context={},
        )
        if "block" in review.lower() or "violation" in review.lower():
            await post_to_channel(
                "content",
                f"## ⚠️ Content Blocked by Compliance\n\n"
                f"**Topic:** {topic}\n**Issue:** {review}\n\n"
                f"Draft needs revision before publishing.",
            )
            return

    # Post as draft for approval
    await create_draft(
        content=draft,
        agent_name="storyteller",
        channel="content",
        draft_type=platform,
    )


async def auto_intel_cycle(
    agents: dict[str, Any],
    memory: Any = None,
):
    """Run the full intelligence gathering cycle.

    Triggers: social scan → store results → alert on significant findings.
    Called by DailyRhythm during opponent scan times.
    """
    log.info("auto_chain.intel_cycle")

    # Run full social scan
    scan_data = await run_full_social_scan()

    # Store in memory for POLLSTER
    await store_scan_results(scan_data, memory)

    # Check for significant opponent activity
    opponent_activity = scan_data.get("opponent_social", [])
    if len(opponent_activity) > 3:
        # Notable opponent activity — post summary
        titles = [r.get("title", "") for r in opponent_activity[:5]]
        summary = "\n".join(f"- {t}" for t in titles if t)
        await post_to_channel(
            "opponent-watch",
            f"## 📡 Opponent Activity Detected\n\n{summary}",
        )

    # Check for campaign mentions (could be good or bad)
    mentions = scan_data.get("campaign_mentions", [])
    if mentions:
        titles = [r.get("title", "") for r in mentions[:3]]
        summary = "\n".join(f"- {t}" for t in titles if t)
        await post_to_channel(
            "ops",
            f"## 📢 Campaign Mentions\n\n{summary}",
        )

    return scan_data


async def auto_performance_loop(
    agents: dict[str, Any],
    memory: Any = None,
):
    """Weekly performance analysis → strategic recommendations.

    Runs as part of the Sunday retro cycle.
    """
    log.info("auto_chain.performance_loop")

    result = await run_predefined_chain(
        "weekly_retro",
        "Run the full weekly performance analysis: petition pace, content engagement, "
        "volunteer activity, opponent movements, and strategic recommendations.",
        agents,
        memory,
    )

    if result.get("success"):
        await post_to_channel(
            "ops",
            f"## 📊 Weekly Performance Analysis (Auto-Generated)\n\n"
            f"{result['final_response']}",
        )
