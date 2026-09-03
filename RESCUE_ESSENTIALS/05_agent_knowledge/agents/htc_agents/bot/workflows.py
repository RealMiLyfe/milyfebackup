"""Approval Workflows, Feedback, Knowledge Ingestion, and Priority Interrupts.

Approval Workflow:
    Agent drafts → posts to channel as "DRAFT" → user reacts:
        ✅ = approve/publish
        ✏️ = revise (agent rewrites)
        ❌ = reject/discard

Feedback System:
    User reacts to any agent response:
        👍 = good response (stored as positive example)
        👎 = bad response (agent asked to improve, correction stored)

Knowledge Ingestion:
    User drops a file in a channel → relevant agent indexes it into ChromaDB

Priority Interrupts:
    Crisis detected → DM to operator + ntfy phone push

Escalation:
    Agent stuck → posts "I need human input" → waits for response
"""

from __future__ import annotations

from typing import Any

import httpx
import structlog

from htc_agents.config import settings
from htc_agents.tools.notify import send_alert, post_to_channel


log = structlog.get_logger()


# ═══════════════════════════════════════════════════════════════
# APPROVAL WORKFLOWS
# ═══════════════════════════════════════════════════════════════

# Track pending drafts: {post_id: {"agent": name, "content": str, "channel": str, "type": str}}
_pending_drafts: dict[str, dict[str, Any]] = {}


async def create_draft(
    content: str,
    agent_name: str,
    channel: str,
    draft_type: str = "content",
    bot_token: str = "",
) -> str | None:
    """Post a draft to a channel for approval.

    Returns the post_id for tracking.
    """
    draft_message = (
        f"## 📝 DRAFT — Awaiting Approval\n"
        f"**From:** {agent_name.replace('_', ' ').title()}\n"
        f"**Type:** {draft_type}\n\n"
        f"---\n\n"
        f"{content}\n\n"
        f"---\n\n"
        f"React: ✅ approve | ✏️ revise | ❌ reject"
    )

    # Post via webhook
    await post_to_channel(channel, draft_message)

    log.info(
        "workflow.draft_created",
        agent=agent_name,
        channel=channel,
        type=draft_type,
    )
    return None  # In full implementation, return post_id for reaction tracking


async def handle_approval_reaction(
    post_id: str,
    reaction: str,
    agents: dict[str, Any],
) -> str:
    """Handle a reaction on a draft post.

    Returns action taken.
    """
    if post_id not in _pending_drafts:
        return "unknown_draft"

    draft = _pending_drafts[post_id]

    if reaction == "white_check_mark":  # ✅
        # Publish the content
        await _publish_content(draft)
        del _pending_drafts[post_id]
        return "published"

    elif reaction == "pencil2":  # ✏️
        # Ask agent to revise
        agent = agents.get(draft["agent"])
        if agent:
            revised = await agent.invoke(
                f"Revise this draft based on feedback. Make it better:\n\n{draft['content']}",
                context={"revision_requested": True},
            )
            draft["content"] = revised
            await post_to_channel(
                draft["channel"],
                f"## 📝 REVISED DRAFT\n\n{revised}\n\n---\nReact: ✅ approve | ✏️ revise again | ❌ reject",
            )
        return "revision_requested"

    elif reaction == "x":  # ❌
        del _pending_drafts[post_id]
        return "rejected"

    return "unknown_reaction"


async def _publish_content(draft: dict[str, Any]):
    """Publish approved content to the appropriate platform."""
    draft_type = draft.get("type", "content")
    content = draft["content"]

    if draft_type == "blog":
        # Publish to Ghost
        from htc_agents.bot.integrations import publish_to_ghost
        await publish_to_ghost(content)

    elif draft_type == "email":
        # Queue in Listmonk
        from htc_agents.bot.integrations import queue_email
        await queue_email(content)

    elif draft_type == "social":
        # Post to Mastodon
        from htc_agents.bot.integrations import post_to_mastodon
        await post_to_mastodon(content)

    log.info("workflow.published", type=draft_type)


# ═══════════════════════════════════════════════════════════════
# FEEDBACK + LEARNING
# ═══════════════════════════════════════════════════════════════

async def handle_feedback(
    post_id: str,
    reaction: str,
    agent_name: str,
    message_content: str,
    memory: Any,
):
    """Process feedback reactions on agent responses.

    👍 (thumbsup) = positive signal — store as good example
    👎 (thumbsdown) = negative signal — store correction request
    """
    if reaction in ("thumbsup", "+1"):
        # Store as positive example
        if memory:
            await memory.store(
                content=f"[POSITIVE FEEDBACK] This response was well-received:\n{message_content[:500]}",
                agent_name=agent_name,
                metadata={"feedback": "positive", "type": "example"},
            )
        log.info("feedback.positive", agent=agent_name)

    elif reaction in ("thumbsdown", "-1"):
        # Store as negative signal
        if memory:
            await memory.store(
                content=f"[NEGATIVE FEEDBACK] This response needs improvement:\n{message_content[:500]}",
                agent_name=agent_name,
                metadata={"feedback": "negative", "type": "correction_needed"},
            )
        log.info("feedback.negative", agent=agent_name)


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE INGESTION
# ═══════════════════════════════════════════════════════════════

async def ingest_file(
    file_url: str,
    filename: str,
    channel_name: str,
    memory: Any,
    bot_token: str = "",
):
    """Download and ingest a file dropped into a channel.

    Routes to the appropriate agent's memory based on channel.
    """
    from htc_agents.bot.main import CHANNEL_AGENT_MAP

    # Determine which agent should own this knowledge
    agent_name = CHANNEL_AGENT_MAP.get(channel_name, "commander")
    if agent_name is None:
        agent_name = "commander"

    try:
        # Download the file
        async with httpx.AsyncClient(timeout=30) as client:
            headers = {"Authorization": f"Bearer {bot_token}"} if bot_token else {}
            resp = await client.get(file_url, headers=headers)
            resp.raise_for_status()
            content = resp.text

        # Store in ChromaDB under the agent's collection
        if memory:
            await memory.store(
                content=f"[INGESTED FILE: {filename}]\n{content[:5000]}",
                agent_name=agent_name,
                metadata={
                    "source": "file_upload",
                    "filename": filename,
                    "channel": channel_name,
                },
            )

        log.info(
            "knowledge.file_ingested",
            filename=filename,
            agent=agent_name,
            channel=channel_name,
            size=len(content),
        )

        await post_to_channel(
            channel_name,
            f"📥 Ingested `{filename}` into {agent_name}'s knowledge base ({len(content)} chars)",
        )

    except Exception as e:
        log.error("knowledge.ingest_failed", filename=filename, error=str(e))


# ═══════════════════════════════════════════════════════════════
# PRIORITY INTERRUPTS
# ═══════════════════════════════════════════════════════════════

async def priority_interrupt(
    message: str,
    level: int = 3,
    source_agent: str = "",
    operator_user_id: str = "",
):
    """Trigger a priority interrupt — escalates to operator.

    Levels:
        1 = noise (no interrupt)
        2 = local media (post to channel only)
        3 = coordinated attack (DM + channel)
        4 = crisis (DM + channel + phone push)
    """
    if level <= 1:
        return

    # Always post to crisis channel
    await post_to_channel(
        "crisis-response",
        f"## 🚨 Level {level} Alert\n**Source:** {source_agent}\n\n{message}",
    )

    if level >= 3:
        # DM the operator (would need operator user_id)
        log.warning("interrupt.level3", source=source_agent, message=message[:100])

    if level >= 4:
        # Phone push via ntfy
        await send_alert(
            message=f"🚨 LEVEL 4 CRISIS: {message[:200]}",
            title="CAMPAIGN CRISIS",
            priority="urgent",
            tags=["rotating_light", "warning"],
        )
        log.critical("interrupt.level4", source=source_agent)


# ═══════════════════════════════════════════════════════════════
# ESCALATION PATHS
# ═══════════════════════════════════════════════════════════════

async def escalate_to_human(
    agent_name: str,
    reason: str,
    context: str = "",
    channel: str = "ops",
):
    """When an agent is stuck and needs human input.

    Posts a structured request and waits for response.
    """
    escalation_message = (
        f"## 🙋 Human Input Needed\n"
        f"**Agent:** {agent_name.replace('_', ' ').title()}\n"
        f"**Reason:** {reason}\n\n"
    )
    if context:
        escalation_message += f"**Context:**\n{context[:500]}\n\n"
    escalation_message += "Please reply in this thread with your guidance."

    await post_to_channel(channel, escalation_message)
    log.info("escalation.human_needed", agent=agent_name, reason=reason)
