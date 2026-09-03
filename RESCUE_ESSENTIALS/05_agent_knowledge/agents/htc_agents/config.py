"""Configuration for the HTC multi-agent system."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration pulled from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ─── LLM Providers ────────────────────────────────────────
    NVIDIA_NIM_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    CEREBRAS_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    OLLAMA_URL: str = "http://host.docker.internal:11434"
    # Local model used as the always-available $0 fallback (no rate limits).
    OLLAMA_MODEL: str = "qwen2.5:3b"

    # ─── Mattermost ──────────────────────────────────────────
    MATTERMOST_URL: str = "http://mattermost:8065"
    MATTERMOST_BOT_TOKEN: str = ""
    MATTERMOST_TEAM: str = "campaign"
    MATTERMOST_USERNAME: str = "milyfe"
    MATTERMOST_PASSWORD: str = ""

    # ─── Memory ──────────────────────────────────────────────
    MEM0_API_KEY: str = ""
    MEM0_STORAGE: str = "local"

    # ─── ChromaDB ────────────────────────────────────────────
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8100
    CHROMA_PERSIST_DIR: str = "/app/data/chromadb"

    # ─── Redis ───────────────────────────────────────────────
    REDIS_URL: str = "redis://redis:6379/1"

    # ─── Campaign API ────────────────────────────────────────
    CAMPAIGN_API_URL: str = "http://htc-campaign-api:8200"

    # ─── Supabase (Read-Only) ────────────────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""

    # ─── SearXNG ─────────────────────────────────────────────
    SEARXNG_URL: str = "http://htc-searxng:8080"

    # ─── ntfy ────────────────────────────────────────────────
    NTFY_URL: str = "http://htc-ntfy:80"
    NTFY_TOPIC: str = "chamber"

    # ─── System ──────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"
    KNOWLEDGE_PATH: str = "/app/knowledge"
    BRAIN_PATH: str = "/app/brain"

    # ─── Webhooks (from parent .env) ─────────────────────────
    MM_WEBHOOK_OPS: str = ""
    MM_WEBHOOK_BRIEF: str = ""
    MM_WEBHOOK_OPPONENT: str = ""
    MM_WEBHOOK_CONTENT: str = ""
    MM_WEBHOOK_PETITION: str = ""
    MM_WEBHOOK_COMPLIANCE: str = ""
    MM_WEBHOOK_HEALTH: str = ""

    @property
    def knowledge_path(self) -> Path:
        return Path(self.KNOWLEDGE_PATH)

    @property
    def brain_path(self) -> Path:
        return Path(self.BRAIN_PATH)


settings = Settings()
