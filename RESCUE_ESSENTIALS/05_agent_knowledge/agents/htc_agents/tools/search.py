"""SearXNG search tool — private web search for intelligence gathering."""

from __future__ import annotations

from typing import Any

import httpx
import structlog

from htc_agents.config import settings


log = structlog.get_logger()


async def search_web(
    query: str,
    categories: list[str] = None,
    max_results: int = 10,
) -> list[dict[str, Any]]:
    """Search the web using SearXNG (private, no tracking).

    Args:
        query: Search query
        categories: SearXNG categories (general, news, social media, etc.)
        max_results: Maximum results to return
    """
    params = {
        "q": query,
        "format": "json",
        "engines": "google,bing,duckduckgo",
    }
    if categories:
        params["categories"] = ",".join(categories)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{settings.SEARXNG_URL}/search",
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()

        results = []
        for item in data.get("results", [])[:max_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "engine": item.get("engine", ""),
            })

        log.info("tools.search", query=query, results=len(results))
        return results

    except Exception as e:
        log.error("tools.search_failed", query=query, error=str(e))
        return []


async def search_news(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Search news specifically — for rapid response and opponent watch."""
    return await search_web(query, categories=["news"], max_results=max_results)


async def search_local(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Search with Jacksonville focus."""
    return await search_web(
        f"{query} Jacksonville Florida",
        categories=["general", "news"],
        max_results=max_results,
    )
