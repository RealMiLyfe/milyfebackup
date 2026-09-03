"""Notification tools — ntfy push alerts and Mattermost webhook posting."""

from __future__ import annotations

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()


async def send_alert(
    message: str,
    title: str = "Campaign Alert",
    priority: str = "default",
    tags: list[str] = None,
):
    """Send a push notification via ntfy to the operator's phone.

    Priority levels: min, low, default, high, urgent
    """
    headers = {
        "Title": title,
        "Priority": priority,
    }
    if tags:
        headers["Tags"] = ",".join(tags)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                f"{settings.NTFY_URL}/{settings.NTFY_TOPIC}",
                content=message,
                headers=headers,
            )
        log.info("notify.alert_sent", title=title, priority=priority)
    except Exception as e:
        log.error("notify.alert_failed", error=str(e))


async def post_to_channel(channel: str, message: str):
    """Post a message to a Mattermost channel via webhook.

    Channels: ops, morning-brief, opponent-watch, content,
              petition, compliance, service-health
    """
    webhook_map = {
        "ops": settings.MM_WEBHOOK_OPS,
        "morning-brief": settings.MM_WEBHOOK_BRIEF,
        "opponent-watch": settings.MM_WEBHOOK_OPPONENT,
        "content": settings.MM_WEBHOOK_CONTENT,
        "petition": settings.MM_WEBHOOK_PETITION,
        "compliance": settings.MM_WEBHOOK_COMPLIANCE,
        "service-health": settings.MM_WEBHOOK_HEALTH,
    }

    webhook_url = webhook_map.get(channel)
    if not webhook_url:
        log.warning("notify.no_webhook", channel=channel)
        return

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(webhook_url, json={"text": message})
        log.info("notify.posted", channel=channel)
    except Exception as e:
        log.error("notify.post_failed", channel=channel, error=str(e))
