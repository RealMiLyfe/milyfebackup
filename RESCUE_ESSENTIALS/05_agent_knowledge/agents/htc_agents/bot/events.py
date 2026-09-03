"""Websocket event handler — captures reactions, file uploads, and other events.

Mattermost sends these events over the websocket:
- reaction_added / reaction_removed — for feedback + approval workflows
- posted (with file_ids) — for knowledge ingestion
- user_added / channel_viewed — for context

This module hooks into mmpy_bot's event system to capture non-message events.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import structlog

from htc_agents.config import settings
from htc_agents.bot.workflows import (
    handle_feedback,
    handle_approval_reaction,
    ingest_file,
    priority_interrupt,
)


log = structlog.get_logger()


# Track which posts came from agents (for feedback routing)
_agent_posts: dict[str, str] = {}  # post_id → agent_name


def register_agent_post(post_id: str, agent_name: str):
    """Register a post as coming from a specific agent (for feedback routing)."""
    _agent_posts[post_id] = agent_name
    # Keep only last 1000 posts to prevent memory leak
    if len(_agent_posts) > 1000:
        keys = list(_agent_posts.keys())
        for k in keys[:500]:
            del _agent_posts[k]


async def handle_websocket_event(event: dict[str, Any], memory: Any = None):
    """Process a raw Mattermost websocket event.

    Called from a custom event handler wired into mmpy_bot.
    """
    event_type = event.get("event", "")

    if event_type == "reaction_added":
        await _handle_reaction(event, memory)
    elif event_type == "posted":
        await _handle_posted(event, memory)


async def _handle_reaction(event: dict[str, Any], memory: Any):
    """Handle emoji reaction events.

    Routes to:
    - Feedback system (👍/👎 on agent responses)
    - Approval workflow (✅/✏️/❌ on drafts)
    """
    try:
        data = event.get("data", {})
        reaction_data = json.loads(data.get("reaction", "{}"))

        post_id = reaction_data.get("post_id", "")
        user_id = reaction_data.get("user_id", "")
        emoji_name = reaction_data.get("emoji_name", "")

        if not post_id or not emoji_name:
            return

        # Don't react to bot's own reactions
        bot_user_id = _get_bot_user_id()
        if user_id == bot_user_id:
            return

        log.info(
            "events.reaction",
            post_id=post_id[:8],
            emoji=emoji_name,
            user=user_id[:8],
        )

        # Check if this is a feedback reaction on an agent post
        if emoji_name in ("thumbsup", "+1", "thumbsdown", "-1"):
            agent_name = _agent_posts.get(post_id, "unknown")
            post_content = await _get_post_content(post_id)
            await handle_feedback(
                post_id=post_id,
                reaction=emoji_name,
                agent_name=agent_name,
                message_content=post_content,
                memory=memory,
            )

        # Check if this is an approval reaction on a draft
        elif emoji_name in ("white_check_mark", "pencil2", "x"):
            from htc_agents.bot.main import _agents
            await handle_approval_reaction(post_id, emoji_name, _agents)

        # Check for crisis escalation trigger (🚨 on any post)
        elif emoji_name in ("rotating_light", "sos", "warning"):
            post_content = await _get_post_content(post_id)
            await priority_interrupt(
                message=f"Manual escalation triggered on post: {post_content[:200]}",
                level=3,
                source_agent="human_escalation",
            )

    except Exception as e:
        log.error("events.reaction_failed", error=str(e))


async def _handle_posted(event: dict[str, Any], memory: Any):
    """Handle new post events — detect file uploads for knowledge ingestion."""
    try:
        data = event.get("data", {})
        post_data = json.loads(data.get("post", "{}"))

        # Check for file attachments
        file_ids = post_data.get("file_ids", [])
        if not file_ids:
            return

        # Don't process bot's own posts
        bot_user_id = _get_bot_user_id()
        if post_data.get("user_id") == bot_user_id:
            return

        channel_id = post_data.get("channel_id", "")
        channel_name = await _get_channel_name(channel_id)

        log.info(
            "events.file_uploaded",
            channel=channel_name,
            file_count=len(file_ids),
        )

        # Ingest each file
        for file_id in file_ids:
            file_info = await _get_file_info(file_id)
            if file_info:
                filename = file_info.get("name", "unknown")
                file_url = f"{settings.MATTERMOST_URL}/api/v4/files/{file_id}"
                await ingest_file(
                    file_url=file_url,
                    filename=filename,
                    channel_name=channel_name,
                    memory=memory,
                    bot_token=settings.MATTERMOST_BOT_TOKEN,
                )

    except Exception as e:
        log.error("events.posted_failed", error=str(e))


# ─── Helper Functions ────────────────────────────────────────

_bot_user_id_cache: str = ""


def _get_bot_user_id() -> str:
    """Get the bot's user ID (cached)."""
    global _bot_user_id_cache
    if not _bot_user_id_cache:
        # Will be set during bot initialization
        _bot_user_id_cache = ""
    return _bot_user_id_cache


def set_bot_user_id(user_id: str):
    """Set the bot user ID (called during init)."""
    global _bot_user_id_cache
    _bot_user_id_cache = user_id


async def _get_post_content(post_id: str) -> str:
    """Fetch post content by ID."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(
                f"{settings.MATTERMOST_URL}/api/v4/posts/{post_id}",
                headers={"Authorization": f"Bearer {settings.MATTERMOST_BOT_TOKEN}"},
            )
            if resp.status_code == 200:
                return resp.json().get("message", "")
    except Exception:
        pass
    return ""


async def _get_channel_name(channel_id: str) -> str:
    """Fetch channel name by ID."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(
                f"{settings.MATTERMOST_URL}/api/v4/channels/{channel_id}",
                headers={"Authorization": f"Bearer {settings.MATTERMOST_BOT_TOKEN}"},
            )
            if resp.status_code == 200:
                return resp.json().get("name", "unknown")
    except Exception:
        pass
    return "unknown"


async def _get_file_info(file_id: str) -> dict[str, Any] | None:
    """Fetch file metadata."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(
                f"{settings.MATTERMOST_URL}/api/v4/files/{file_id}/info",
                headers={"Authorization": f"Bearer {settings.MATTERMOST_BOT_TOKEN}"},
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return None
