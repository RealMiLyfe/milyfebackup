"""Campaign API client — READ-ONLY access to campaign operations data.

CRITICAL: This is READ-ONLY. The platform is sovereign.
Agents can observe but never modify.
"""

from __future__ import annotations

from typing import Any

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()


class CampaignAPIClient:
    """Read-only client for the Campaign API at port 8200."""

    def __init__(self):
        self.base_url = settings.CAMPAIGN_API_URL

    async def _get(self, path: str) -> dict[str, Any] | None:
        """Make a GET request to the campaign API."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{self.base_url}{path}")
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            log.error("campaign_api.request_failed", path=path, error=str(e))
            return None

    async def get_scoreboard(self) -> dict[str, Any] | None:
        """Get the campaign scoreboard metrics."""
        return await self._get("/metrics/scoreboard")

    async def get_petition_status(self) -> dict[str, Any] | None:
        """Get petition signature count and projection."""
        return await self._get("/petition/status")

    async def get_compliance_upcoming(self) -> dict[str, Any] | None:
        """Get upcoming compliance deadlines."""
        return await self._get("/compliance/upcoming")

    async def get_content_stats(self) -> dict[str, Any] | None:
        """Get content publishing statistics."""
        return await self._get("/content/stats")

    async def get_contacts_summary(self) -> dict[str, Any] | None:
        """Get CRM contact summary (aggregates only, no PII)."""
        return await self._get("/crm/summary")

    async def get_volunteer_count(self) -> dict[str, Any] | None:
        """Get volunteer enrollment numbers."""
        return await self._get("/volunteers/count")


# Singleton
campaign_api = CampaignAPIClient()
