"""Florida Campaign Finance Scraper — pulls opponent donor data from FL Division of Elections.

Scrapes the Florida Secretary of State's campaign finance database for:
- Candidate contributions (who's giving to opponents)
- Expenditure reports (how they're spending)
- PAC connections and independent expenditures

Source: https://dos.elections.myflorida.com/campaign-finance/
"""

from __future__ import annotations

from typing import Any
from datetime import date

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()

# Florida Division of Elections campaign finance search
FL_FINANCE_BASE = "https://dos.elections.myflorida.com/campaign-finance"
FL_FINANCE_API = "https://dos.elections.myflorida.com/cgi-bin/contrib.exe"


async def search_fl_contributions(
    candidate_name: str = "",
    committee_name: str = "",
    date_from: str = "",
    date_to: str = "",
    amount_min: float = 0,
    office: str = "MYR",  # MYR = Mayor
    county: str = "DUV",  # DUV = Duval County (Jacksonville)
) -> list[dict[str, Any]]:
    """Search Florida campaign finance contributions.

    This queries the FL Division of Elections public records database.
    Useful for tracking opponent donor networks.
    """
    today = date.today()
    if not date_to:
        date_to = today.strftime("%m/%d/%Y")
    if not date_from:
        date_from = "01/01/2024"

    # Use SearXNG as a proxy to search FL election data
    # (Direct scraping of FL DoE requires complex form submission)
    from htc_agents.tools.search import search_web

    query_parts = []
    if candidate_name:
        query_parts.append(candidate_name)
    if committee_name:
        query_parts.append(committee_name)
    query_parts.append("Florida campaign finance contribution Jacksonville mayor")

    query = " ".join(query_parts)
    results = await search_web(query, max_results=10)

    log.info(
        "fl_finance.search",
        candidate=candidate_name,
        results=len(results),
    )
    return results


async def get_opponent_finance_summary(
    opponent_name: str = "Donna Deegan",
) -> dict[str, Any]:
    """Get a summary of opponent's campaign finance activity.

    Searches multiple sources for contribution and expenditure data.
    """
    from htc_agents.tools.search import search_web

    # Search for recent finance filings
    results = await search_web(
        f"{opponent_name} Jacksonville campaign finance contributions 2026 2027",
        max_results=10,
    )

    # Search for PAC connections
    pac_results = await search_web(
        f"{opponent_name} Jacksonville PAC political committee support",
        max_results=5,
    )

    return {
        "candidate": opponent_name,
        "contribution_sources": results,
        "pac_connections": pac_results,
        "note": "Data from public search — verify against official FL DoE filings",
    }


async def search_jacksonville_political_committees() -> list[dict[str, Any]]:
    """Find active political committees related to Jacksonville mayoral race."""
    from htc_agents.tools.search import search_web

    results = await search_web(
        "Jacksonville Florida political committee PAC mayor 2027 registered",
        max_results=10,
    )
    return results


async def get_deegan_donor_network() -> dict[str, Any]:
    """Specifically track Deegan's donor network and top contributors."""
    from htc_agents.tools.search import search_web

    # Top donors
    donors = await search_web(
        "Donna Deegan mayor Jacksonville top donors contributors campaign finance",
        max_results=10,
    )

    # Endorsements (often tied to money)
    endorsements = await search_web(
        "Donna Deegan Jacksonville endorsements 2024 2025 2026",
        max_results=5,
    )

    # PAC spending for/against
    pacs = await search_web(
        "Jacksonville mayor PAC independent expenditure 2026 2027",
        max_results=5,
    )

    return {
        "candidate": "Donna Deegan",
        "top_donors": donors,
        "endorsements": endorsements,
        "pac_activity": pacs,
        "last_updated": date.today().isoformat(),
    }
