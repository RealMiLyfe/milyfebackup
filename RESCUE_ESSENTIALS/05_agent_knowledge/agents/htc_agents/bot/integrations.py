"""External Integrations — Ghost, Listmonk, Mastodon, Calendar.

These allow agents to PUBLISH (with approval) rather than just draft.
All behind approval workflows — nothing auto-publishes without human ✅.
"""

from __future__ import annotations

from typing import Any

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()


# ═══════════════════════════════════════════════════════════════
# GHOST (Blog Publishing)
# ═══════════════════════════════════════════════════════════════

async def publish_to_ghost(
    content: str,
    title: str = "",
    status: str = "draft",  # draft or published
) -> dict[str, Any] | None:
    """Publish content to Ghost blog.

    Default status is 'draft' — requires manual publish from Ghost admin
    unless explicitly set to 'published' (only after approval workflow).
    """
    ghost_url = settings.CAMPAIGN_API_URL.replace(":8200", ":2368")
    api_key = getattr(settings, "GHOST_ADMIN_API_KEY", "")

    if not api_key:
        log.warning("integrations.ghost_no_key")
        return None

    # Ghost Admin API requires JWT from the API key
    try:
        import jwt
        import time

        key_id, secret = api_key.split(":")
        iat = int(time.time())
        header = {"alg": "HS256", "typ": "JWT", "kid": key_id}
        payload = {"iat": iat, "exp": iat + 300, "aud": "/admin/"}
        token = jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)

        # Extract title from content if not provided
        if not title:
            lines = content.strip().split("\n")
            title = lines[0].lstrip("#").strip() if lines else "Campaign Update"
            content = "\n".join(lines[1:]).strip()

        post_data = {
            "posts": [{
                "title": title,
                "html": f"<p>{content.replace(chr(10), '</p><p>')}</p>",
                "status": status,
            }]
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{ghost_url}/ghost/api/admin/posts/",
                json=post_data,
                headers={"Authorization": f"Ghost {token}"},
            )
            resp.raise_for_status()
            result = resp.json()
            log.info("integrations.ghost_published", status=status, title=title)
            return result

    except Exception as e:
        log.error("integrations.ghost_failed", error=str(e))
        return None


# ═══════════════════════════════════════════════════════════════
# LISTMONK (Email Campaigns)
# ═══════════════════════════════════════════════════════════════

async def queue_email(
    content: str,
    subject: str = "",
    list_id: int = 1,
    send_immediately: bool = False,
) -> dict[str, Any] | None:
    """Queue an email campaign in Listmonk.

    Default: creates draft campaign (requires manual send from Listmonk admin).
    """
    listmonk_url = "http://htc-listmonk:9000"

    if not subject:
        lines = content.strip().split("\n")
        subject = lines[0][:80] if lines else "Campaign Update"

    try:
        campaign_data = {
            "name": subject,
            "subject": subject,
            "body": f"<html><body><p>{content.replace(chr(10), '</p><p>')}</p></body></html>",
            "content_type": "html",
            "lists": [list_id],
            "type": "regular",
            "tags": ["campaign", "automated"],
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{listmonk_url}/api/campaigns",
                json=campaign_data,
                auth=("admin", "admin"),  # Default Listmonk credentials
            )
            resp.raise_for_status()
            result = resp.json()

            campaign_id = result.get("data", {}).get("id")

            # If approved for immediate send
            if send_immediately and campaign_id:
                await client.put(
                    f"{listmonk_url}/api/campaigns/{campaign_id}/status",
                    json={"status": "running"},
                    auth=("admin", "admin"),
                )

            log.info("integrations.email_queued", subject=subject, immediate=send_immediately)
            return result

    except Exception as e:
        log.error("integrations.email_failed", error=str(e))
        return None


# ═══════════════════════════════════════════════════════════════
# MASTODON (Social Posting)
# ═══════════════════════════════════════════════════════════════

async def post_to_mastodon(
    content: str,
    visibility: str = "public",
) -> dict[str, Any] | None:
    """Post to Mastodon instance.

    Visibility: public, unlisted, private, direct
    """
    mastodon_url = getattr(settings, "MASTODON_API_URL", "http://htc-mastodon:3000")
    access_token = getattr(settings, "MASTODON_ACCESS_TOKEN", "")

    if not access_token:
        log.warning("integrations.mastodon_no_token")
        return None

    try:
        # Mastodon has a 500 char limit
        if len(content) > 500:
            content = content[:497] + "..."

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{mastodon_url}/api/v1/statuses",
                data={"status": content, "visibility": visibility},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            resp.raise_for_status()
            result = resp.json()
            log.info("integrations.mastodon_posted", visibility=visibility)
            return result

    except Exception as e:
        log.error("integrations.mastodon_failed", error=str(e))
        return None


# ═══════════════════════════════════════════════════════════════
# SEARXNG (Enhanced Search for Agents)
# ═══════════════════════════════════════════════════════════════

async def search_social_mentions(
    query: str,
    max_results: int = 10,
) -> list[dict[str, Any]]:
    """Search social media mentions via SearXNG — for POLLSTER sentiment tracking."""
    from htc_agents.tools.search import search_web
    return await search_web(
        query,
        categories=["social media"],
        max_results=max_results,
    )


# ═══════════════════════════════════════════════════════════════
# CAMPAIGN API (Enhanced — for Dashboard Data)
# ═══════════════════════════════════════════════════════════════

async def get_dashboard_data() -> dict[str, Any]:
    """Get all metrics for agent dashboards."""
    from htc_agents.tools.campaign_api import campaign_api

    data = {}
    data["scoreboard"] = await campaign_api.get_scoreboard()
    data["petition"] = await campaign_api.get_petition_status()
    data["compliance"] = await campaign_api.get_compliance_upcoming()
    data["content"] = await campaign_api.get_content_stats()
    data["contacts"] = await campaign_api.get_contacts_summary()
    data["volunteers"] = await campaign_api.get_volunteer_count()

    return {k: v for k, v in data.items() if v is not None}
