"""Postiz Client — publish content to all social platforms via the Postiz API.

Postiz (self-hosted at port 5200) handles:
- X/Twitter
- LinkedIn
- Mastodon
- Threads
- Facebook
- Reddit
- YouTube (community posts)
- TikTok (descriptions)
- Bluesky
- And 20+ more

This client is used by the approval workflow:
    STORYTELLER drafts → SENTINEL reviews → User approves (✅) → Postiz publishes
"""

from __future__ import annotations

from typing import Any
from datetime import datetime, timedelta

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()

POSTIZ_URL = "http://htc-postiz:5000"  # Internal docker network
POSTIZ_EXTERNAL = "http://localhost:5200"  # For browser access


class PostizClient:
    """Client for the Postiz social media scheduling API."""

    def __init__(self):
        self.base_url = POSTIZ_URL
        self._token: str = ""

    async def _get_token(self) -> str:
        """Authenticate with Postiz and get a session token."""
        if self._token:
            return self._token

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                # Try to login with default admin credentials
                resp = await client.post(
                    f"{self.base_url}/api/auth/login",
                    json={"email": "admin@campaign.local", "password": "campaign2027"},
                )
                if resp.status_code == 200:
                    self._token = resp.json().get("token", "")
                    return self._token
        except Exception as e:
            log.warning("postiz.auth_failed", error=str(e))

        return ""

    async def schedule_post(
        self,
        content: str,
        platforms: list[str] = None,
        schedule_at: datetime | None = None,
        media_urls: list[str] = None,
    ) -> dict[str, Any] | None:
        """Schedule a post across multiple platforms.

        Args:
            content: The post text
            platforms: List of platform names (twitter, linkedin, mastodon, etc.)
            schedule_at: When to publish (None = immediately)
            media_urls: Optional image/video URLs to attach
        """
        platforms = platforms or ["mastodon"]

        if not schedule_at:
            schedule_at = datetime.now() + timedelta(minutes=5)

        token = await self._get_token()
        if not token:
            log.warning("postiz.no_token", msg="Cannot schedule without auth")
            return None

        try:
            payload = {
                "content": content,
                "platforms": platforms,
                "scheduledAt": schedule_at.isoformat(),
            }
            if media_urls:
                payload["media"] = media_urls

            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    f"{self.base_url}/api/posts",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"},
                )
                if resp.status_code in (200, 201):
                    result = resp.json()
                    log.info(
                        "postiz.scheduled",
                        platforms=platforms,
                        schedule_at=schedule_at.isoformat(),
                    )
                    return result
                else:
                    log.error(
                        "postiz.schedule_failed",
                        status=resp.status_code,
                        body=resp.text[:200],
                    )
        except Exception as e:
            log.error("postiz.request_failed", error=str(e))

        return None

    async def get_analytics(self, days: int = 7) -> dict[str, Any] | None:
        """Get posting analytics for the last N days."""
        token = await self._get_token()
        if not token:
            return None

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self.base_url}/api/analytics?days={days}",
                    headers={"Authorization": f"Bearer {token}"},
                )
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            log.error("postiz.analytics_failed", error=str(e))

        return None

    async def get_scheduled_posts(self) -> list[dict[str, Any]]:
        """Get all currently scheduled (pending) posts."""
        token = await self._get_token()
        if not token:
            return []

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self.base_url}/api/posts?status=scheduled",
                    headers={"Authorization": f"Bearer {token}"},
                )
                if resp.status_code == 200:
                    return resp.json().get("posts", [])
        except Exception as e:
            log.error("postiz.get_scheduled_failed", error=str(e))

        return []


# Singleton
postiz = PostizClient()


async def publish_approved_content(
    content: str,
    platforms: list[str] = None,
    schedule_minutes_from_now: int = 5,
) -> bool:
    """Publish approved content via Postiz.

    Called after a user reacts ✅ on a draft in the approval workflow.
    """
    platforms = platforms or ["mastodon", "linkedin"]

    schedule_at = datetime.now() + timedelta(minutes=schedule_minutes_from_now)
    result = await postiz.schedule_post(
        content=content,
        platforms=platforms,
        schedule_at=schedule_at,
    )

    return result is not None
