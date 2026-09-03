"""Social Monitoring Feed — real-time sentiment and mention tracking.

Uses SearXNG + scheduled scraping to provide POLLSTER with actual data:
- Reddit r/jacksonville monitoring
- Local news sentiment
- Social media mentions (via SearXNG social category)
- Nextdoor-style neighborhood buzz (via news proxies)
- Opponent social media activity tracking

Runs on schedule via DailyRhythm — results stored in ChromaDB for POLLSTER.
"""

from __future__ import annotations

from typing import Any
from datetime import datetime

import structlog

from htc_agents.config import settings
from htc_agents.tools.search import search_web, search_news, search_local


log = structlog.get_logger()


async def scan_jacksonville_reddit() -> list[dict[str, Any]]:
    """Scan r/jacksonville for trending topics and sentiment."""
    results = await search_web(
        "site:reddit.com/r/jacksonville",
        categories=["general"],
        max_results=15,
    )
    log.info("social_monitor.reddit_scan", results=len(results))
    return results


async def scan_local_news_sentiment() -> list[dict[str, Any]]:
    """Scan Jacksonville local news for trending stories."""
    sources = [
        "Jacksonville news today local",
        "Jacksonville city council budget 2026",
        "Duval County Florida news",
    ]

    all_results = []
    for query in sources:
        results = await search_news(query, max_results=5)
        all_results.extend(results)

    log.info("social_monitor.news_scan", results=len(all_results))
    return all_results


async def scan_opponent_social() -> list[dict[str, Any]]:
    """Track opponent social media activity."""
    queries = [
        "Donna Deegan Jacksonville mayor tweet post",
        "Donna Deegan announcement statement 2026",
        "Jacksonville mayor office statement",
    ]

    all_results = []
    for query in queries:
        results = await search_web(query, max_results=5)
        all_results.extend(results)

    log.info("social_monitor.opponent_social", results=len(all_results))
    return all_results


async def scan_campaign_mentions() -> list[dict[str, Any]]:
    """Track mentions of MiLyfe campaign across the web."""
    queries = [
        "MiLyfe Jacksonville mayor",
        "Carnell Lee Jacksonville candidate",
        "Jacksonville mayor 2027 candidates",
    ]

    all_results = []
    for query in queries:
        results = await search_web(query, max_results=5)
        all_results.extend(results)

    log.info("social_monitor.campaign_mentions", results=len(all_results))
    return all_results


async def scan_issue_sentiment(issue: str) -> list[dict[str, Any]]:
    """Track sentiment around a specific issue in Jacksonville.

    Example issues: "JEA rates", "property taxes", "crime", "flooding"
    """
    results = await search_local(f"{issue} Jacksonville residents opinion", max_results=10)
    log.info("social_monitor.issue_scan", issue=issue, results=len(results))
    return results


async def run_full_social_scan() -> dict[str, Any]:
    """Run a complete social monitoring cycle.

    Called by DailyRhythm scheduler.
    Returns structured data for POLLSTER to analyze.
    """
    timestamp = datetime.now().isoformat()

    reddit = await scan_jacksonville_reddit()
    news = await scan_local_news_sentiment()
    opponent = await scan_opponent_social()
    mentions = await scan_campaign_mentions()

    # Key issues to track
    hot_issues = [
        "JEA rates Jacksonville",
        "Jacksonville property tax insurance",
        "Jacksonville crime public safety",
        "Jacksonville roads infrastructure",
        "Jacksonville flooding septic",
    ]

    issue_data = {}
    for issue in hot_issues:
        results = await scan_issue_sentiment(issue)
        issue_data[issue] = results

    full_scan = {
        "timestamp": timestamp,
        "reddit": reddit,
        "local_news": news,
        "opponent_social": opponent,
        "campaign_mentions": mentions,
        "issue_tracking": issue_data,
        "summary": {
            "total_signals": len(reddit) + len(news) + len(opponent) + len(mentions),
            "opponent_activity": len(opponent),
            "our_mentions": len(mentions),
        },
    }

    log.info(
        "social_monitor.full_scan_complete",
        total_signals=full_scan["summary"]["total_signals"],
    )

    return full_scan


async def store_scan_results(scan_data: dict[str, Any], memory: Any):
    """Store social scan results in memory for POLLSTER to access."""
    if not memory:
        return

    # Store summary in POLLSTER's memory
    summary = (
        f"[SOCIAL SCAN {scan_data['timestamp']}]\n"
        f"Reddit signals: {len(scan_data.get('reddit', []))}\n"
        f"News stories: {len(scan_data.get('local_news', []))}\n"
        f"Opponent activity: {len(scan_data.get('opponent_social', []))}\n"
        f"Campaign mentions: {len(scan_data.get('campaign_mentions', []))}\n"
    )

    # Add top stories
    for item in scan_data.get("local_news", [])[:3]:
        summary += f"- {item.get('title', 'untitled')}\n"

    await memory.store(
        content=summary,
        agent_name="pollster",
        metadata={"type": "social_scan", "timestamp": scan_data["timestamp"]},
    )

    log.info("social_monitor.results_stored")
