"""Memory Manager — Combines Mem0 (short/long term) with ChromaDB (episodic/vector)."""

from __future__ import annotations

from typing import Any

import structlog

from htc_agents.config import settings


log = structlog.get_logger()


class MemoryManager:
    """Unified memory interface for all agents.

    Layers:
        - Short-term: Recent conversation context (in-memory ring buffer)
        - Long-term: Persistent facts and learnings (Mem0)
        - Episodic: Searchable interaction history (ChromaDB)
    """

    def __init__(self):
        self._mem0 = None
        self._chroma_client = None
        self._collections: dict[str, Any] = {}
        self._short_term: dict[str, list[dict]] = {}

    async def initialize(self):
        """Initialize memory backends."""
        await self._init_mem0()
        await self._init_chromadb()
        log.info("memory.initialized")

    async def _init_mem0(self):
        """Initialize Mem0 for long-term memory."""
        try:
            from mem0 import Memory

            config = {
                "llm": {
                    "provider": "groq",
                    "config": {
                        "model": "llama-3.1-8b-instant",
                        "api_key": settings.GROQ_API_KEY,
                    },
                },
                "embedder": {
                    "provider": "huggingface",
                    "config": {
                        "model": "sentence-transformers/all-MiniLM-L6-v2",
                    },
                },
                "vector_store": {
                    "provider": "chroma",
                    "config": {
                        "collection_name": "htc_mem0",
                        "path": settings.CHROMA_PERSIST_DIR,
                    },
                },
            }

            self._mem0 = Memory.from_config(config)
            log.info("memory.mem0_ready")
        except Exception as e:
            log.warning("memory.mem0_failed", error=str(e))
            self._mem0 = None

    async def _init_chromadb(self):
        """Initialize ChromaDB for episodic memory."""
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings

            self._chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                ),
            )
            log.info("memory.chromadb_ready")
        except Exception as e:
            log.warning("memory.chromadb_failed", error=str(e))
            self._chroma_client = None

    def _get_collection(self, agent_name: str):
        """Get or create a ChromaDB collection for an agent."""
        if agent_name not in self._collections and self._chroma_client:
            self._collections[agent_name] = (
                self._chroma_client.get_or_create_collection(
                    name=f"htc_{agent_name}",
                    metadata={"agent": agent_name},
                )
            )
        return self._collections.get(agent_name)

    async def store(
        self,
        content: str,
        agent_name: str,
        metadata: dict[str, Any] = None,
    ):
        """Store a memory across all layers.

        Args:
            content: The content to memorize
            agent_name: Which agent generated this
            metadata: Additional metadata tags
        """
        metadata = metadata or {}

        # Short-term: ring buffer per agent (last 20 interactions)
        if agent_name not in self._short_term:
            self._short_term[agent_name] = []
        self._short_term[agent_name].append(
            {"content": content, "metadata": metadata}
        )
        if len(self._short_term[agent_name]) > 20:
            self._short_term[agent_name] = self._short_term[agent_name][-20:]

        # Long-term: Mem0
        if self._mem0:
            try:
                self._mem0.add(
                    content,
                    user_id=agent_name,
                    metadata=metadata,
                )
            except Exception as e:
                log.warning("memory.mem0_store_failed", error=str(e))

        # Episodic: ChromaDB
        collection = self._get_collection(agent_name)
        if collection:
            try:
                import uuid
                doc_id = str(uuid.uuid4())
                collection.add(
                    documents=[content],
                    ids=[doc_id],
                    metadatas=[metadata],
                )
            except Exception as e:
                log.warning("memory.chroma_store_failed", error=str(e))

    async def recall(
        self,
        query: str,
        agent_name: str,
        limit: int = 5,
    ) -> list[str]:
        """Recall relevant memories for a query.

        Combines results from all memory layers.
        """
        results = []

        # Short-term: check recent interactions
        recent = self._short_term.get(agent_name, [])[-5:]
        for item in recent:
            results.append(item["content"])

        # Episodic: ChromaDB semantic search
        collection = self._get_collection(agent_name)
        if collection:
            try:
                search_results = collection.query(
                    query_texts=[query],
                    n_results=min(limit, 5),
                )
                if search_results and search_results["documents"]:
                    for doc in search_results["documents"][0]:
                        if doc not in results:
                            results.append(doc)
            except Exception as e:
                log.warning("memory.chroma_recall_failed", error=str(e))

        # Long-term: Mem0
        if self._mem0:
            try:
                mem0_results = self._mem0.search(query, user_id=agent_name)
                for mem in mem0_results.get("results", [])[:limit]:
                    text = mem.get("memory", "")
                    if text and text not in results:
                        results.append(text)
            except Exception as e:
                log.warning("memory.mem0_recall_failed", error=str(e))

        return results[:limit]

    async def get_agent_context(self, agent_name: str) -> str:
        """Get a summary of what an agent knows from short-term memory."""
        recent = self._short_term.get(agent_name, [])[-5:]
        if not recent:
            return ""
        lines = [item["content"] for item in recent]
        return "\n---\n".join(lines)
