"""MI Gateway Bridge — connects HTC agents to the mi-extension capabilities.

The mi-extension at /home/milyfe/milyfe-ai-workspace/mi-extension provides:
- snscrape: Social media scraping (Twitter/X handles, timelines)
- web-interact: Browser automation via DevTools protocol
- whisper: Speech-to-text transcription
- tts-clone: Text-to-speech with voice cloning
- wiki: Private knowledge wiki with embeddings
- ocr: Optical character recognition for documents
- mediapipe: Vision/gesture recognition
- screencapture: Screen capture and monitoring

This module provides a client interface that HTC agents can use to access
these capabilities either via the gateway HTTP server (if running) or by
spawning the tools directly as subprocesses.
"""

from __future__ import annotations

import asyncio
import subprocess
import json
from typing import Any

import httpx
import structlog


log = structlog.get_logger()

# Gateway URL if running as a server
MI_GATEWAY_URL = "http://localhost:3100"

# Direct paths for subprocess fallback
MI_EXTENSION_PATH = "/home/milyfe/milyfe-ai-workspace/mi-extension"
SNSCRAPE_BIN = "snscrape"


class MIGateway:
    """Client for mi-extension capabilities."""

    def __init__(self):
        self._gateway_available: bool | None = None

    async def _check_gateway(self) -> bool:
        """Check if the MI gateway HTTP server is running."""
        if self._gateway_available is not None:
            return self._gateway_available

        try:
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.get(f"{MI_GATEWAY_URL}/health")
                self._gateway_available = resp.status_code == 200
        except Exception:
            self._gateway_available = False

        return self._gateway_available

    # ═══════════════════════════════════════════════════════════
    # SNSCRAPE — Social Media Scraping
    # ═══════════════════════════════════════════════════════════

    async def scrape_twitter_user(
        self,
        handle: str,
        since: str = "",
        max_tweets: int = 20,
    ) -> list[dict[str, Any]]:
        """Scrape tweets from a Twitter/X user.

        Args:
            handle: Twitter handle (with or without @)
            since: Date filter YYYY-MM-DD
            max_tweets: Maximum tweets to return

        Used by: POLLSTER, OPPO_TRACKER, SCOUT
        """
        handle = handle.lstrip("@")

        # Try gateway first
        if await self._check_gateway():
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.post(
                        f"{MI_GATEWAY_URL}/snscrape",
                        json={"handle": handle, "since": since},
                    )
                    if resp.status_code == 200:
                        return resp.json().get("tweets", [])
            except Exception as e:
                log.warning("mi_gateway.snscrape_http_failed", error=str(e))

        # Fallback: run snscrape directly as subprocess
        return await self._run_snscrape_subprocess(handle, since, max_tweets)

    async def _run_snscrape_subprocess(
        self, handle: str, since: str, max_tweets: int
    ) -> list[dict[str, Any]]:
        """Run snscrape as a subprocess for Twitter scraping."""
        query = f"from:{handle}"
        if since:
            query += f" since:{since}"

        cmd = [SNSCRAPE_BIN, "--jsonl", "--max-results", str(max_tweets), "twitter-search", query]

        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=30)

            tweets = []
            for line in stdout.decode().strip().split("\n"):
                if line:
                    try:
                        data = json.loads(line)
                        tweets.append({
                            "content": data.get("content", data.get("rawContent", "")),
                            "date": data.get("date", ""),
                            "url": data.get("url", ""),
                            "likes": data.get("likeCount", 0),
                            "retweets": data.get("retweetCount", 0),
                        })
                    except json.JSONDecodeError:
                        continue

            log.info("mi_gateway.snscrape_subprocess", handle=handle, tweets=len(tweets))
            return tweets

        except FileNotFoundError:
            log.warning("mi_gateway.snscrape_not_installed")
            return []
        except asyncio.TimeoutError:
            log.warning("mi_gateway.snscrape_timeout", handle=handle)
            return []
        except Exception as e:
            log.error("mi_gateway.snscrape_failed", error=str(e))
            return []

    async def scrape_twitter_search(
        self,
        query: str,
        max_tweets: int = 20,
    ) -> list[dict[str, Any]]:
        """Search Twitter/X for a query.

        Used by: POLLSTER (sentiment), SCOUT (breaking news)
        """
        cmd = [SNSCRAPE_BIN, "--jsonl", "--max-results", str(max_tweets), "twitter-search", query]

        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(result.communicate(), timeout=30)

            tweets = []
            for line in stdout.decode().strip().split("\n"):
                if line:
                    try:
                        data = json.loads(line)
                        tweets.append({
                            "content": data.get("content", data.get("rawContent", "")),
                            "user": data.get("user", {}).get("username", ""),
                            "date": data.get("date", ""),
                            "url": data.get("url", ""),
                        })
                    except json.JSONDecodeError:
                        continue

            return tweets

        except Exception as e:
            log.error("mi_gateway.twitter_search_failed", error=str(e))
            return []

    # ═══════════════════════════════════════════════════════════
    # OCR — Document Reading
    # ═══════════════════════════════════════════════════════════

    async def ocr_file(self, file_path: str) -> str:
        """Run OCR on an image or PDF file.

        Used by: Knowledge ingestion, OPPO_TRACKER (campaign mailers)
        """
        # Try tesseract directly (commonly available)
        try:
            result = await asyncio.create_subprocess_exec(
                "tesseract", file_path, "-", "--oem", "3",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(result.communicate(), timeout=30)
            text = stdout.decode().strip()
            log.info("mi_gateway.ocr_complete", file=file_path, chars=len(text))
            return text
        except FileNotFoundError:
            log.warning("mi_gateway.tesseract_not_installed")
            return ""
        except Exception as e:
            log.error("mi_gateway.ocr_failed", error=str(e))
            return ""

    # ═══════════════════════════════════════════════════════════
    # WHISPER — Speech-to-Text
    # ═══════════════════════════════════════════════════════════

    async def transcribe_audio(self, file_path: str) -> str:
        """Transcribe an audio file using Whisper via Ollama or local binary.

        Used by: MEDIA_COACH (interview transcripts), DEBATE_COACH (practice recordings)
        """
        # Try whisper via Ollama (if model pulled)
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                # Check if whisper model exists
                resp = await client.get("http://host.docker.internal:11434/api/tags")
                if resp.status_code == 200:
                    models = [m["name"] for m in resp.json().get("models", [])]
                    if any("whisper" in m for m in models):
                        # Use Ollama whisper
                        # (implementation depends on Ollama whisper interface)
                        pass
        except Exception:
            pass

        # Fallback: whisper CLI if installed
        try:
            result = await asyncio.create_subprocess_exec(
                "whisper", file_path, "--model", "base", "--output_format", "txt",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(result.communicate(), timeout=300)
            return stdout.decode().strip()
        except FileNotFoundError:
            log.warning("mi_gateway.whisper_not_installed")
            return "[Whisper not available — install with: pip install openai-whisper]"
        except Exception as e:
            log.error("mi_gateway.transcribe_failed", error=str(e))
            return ""

    # ═══════════════════════════════════════════════════════════
    # WEB INTERACTION — Browser Automation
    # ═══════════════════════════════════════════════════════════

    async def fetch_page_text(self, url: str) -> str:
        """Fetch and extract text content from a URL.

        Simpler than web-interact — just gets readable text.
        Used by: SCOUT, OPPO_TRACKER, FUNDRAISER (public records)
        """
        try:
            async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
                resp = await client.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; CampaignResearchBot/1.0)"
                })
                resp.raise_for_status()

                # Basic HTML to text extraction
                from html.parser import HTMLParser

                class TextExtractor(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.text = []
                        self._skip = False

                    def handle_starttag(self, tag, attrs):
                        if tag in ("script", "style", "nav", "footer", "header"):
                            self._skip = True

                    def handle_endtag(self, tag):
                        if tag in ("script", "style", "nav", "footer", "header"):
                            self._skip = False

                    def handle_data(self, data):
                        if not self._skip:
                            text = data.strip()
                            if text:
                                self.text.append(text)

                extractor = TextExtractor()
                extractor.feed(resp.text)
                return " ".join(extractor.text)[:10000]

        except Exception as e:
            log.error("mi_gateway.fetch_page_failed", url=url, error=str(e))
            return ""


# Singleton
mi_gateway = MIGateway()
