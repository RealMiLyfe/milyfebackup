# MI Research & Intelligence Framework

## Architecture Summary

The intelligence system follows this lifecycle for every piece of information:
COLLECT → PROCESS → ENRICH → STORE → INDEX → QUERY → ACT

## Collection Sources (Active)
- SearXNG (running, port 8080) — scheduled web search
- Playwright MCP — structured scraping
- Campaign API intake endpoints — citizen/volunteer submissions

## Collection Sources (To Add)
- SpiderFoot — deep OSINT recon (Docker, free)
- Recon-ng — scriptable precision collection

## Processing Pipeline
Every document: Acquire → Extract text → Chunk (512 tokens, 64 overlap) → Entity extraction → Confidence scoring → Dual storage

## Storage Systems
- Weaviate — vector/semantic search (TO ADD)
- Graphiti — temporal knowledge graph (TO ADD)
- SQLite — structured relational data (campaign.db EXISTS)
- Meilisearch — full-text keyword search (RUNNING, port 7700)
- ChromaDB — episodic agent memory (RUNNING, port 8000)

## Intelligence Domains
1. FISCAL — Jacksonville budget, JEA, pension, contracts, federal money
2. OPPONENT — Statements, contradictions, donor networks, voting records
3. POLICY — Research evidence for each campaign pillar
4. DEMOGRAPHIC — Census, voter data, neighborhood profiles, dormant voters
5. MEDIA — Coverage tracking, sentiment, narrative shifts

## Agent Query Protocol
Before external search: Meilisearch → Weaviate → Graphiti → SQLite → Only then SearXNG

## Confidence Scoring
- Source credibility (40%): Official doc 0.95, Major media 0.80, Secondary 0.65, Unverified 0.40
- Corroboration (40%): 3+ sources 1.0, 2 sources 0.85, 1 source 0.70, None 0.50
- Recency (20%): 30 days 1.0, 6 months 0.90, 2 years 0.75

## Contradiction Engine Types
1. Factual (same claim, different values) → flag for review
2. Temporal (same actor, changed position) → store both, HIGH intelligence value
3. Logical (same facts, incompatible conclusions) → derived contradiction record
4. Source (two credible sources disagree) → store both, active corroboration request

## Implementation Order
Week 1: Weaviate + txtai pipeline + SQLite schema
Week 2: SpiderFoot + document ingestion pipeline + budget ingest
Week 3: Policy research corpus + opponent statements + census data
Week 4: intelligence.ts MCP server + agent prompt updates + continuous ingestion
