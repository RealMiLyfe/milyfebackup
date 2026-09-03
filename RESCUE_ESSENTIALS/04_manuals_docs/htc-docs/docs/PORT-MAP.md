# Port Map — Hyperbolic Time Chamber

| Port | Service | What It Does |
|------|---------|-------------|
| 80 | Traefik | Front door (reverse proxy) |
| 1935 | Owncast RTMP | Live stream ingestion |
| 2370 | Ghost | Campaign blog — publishes the story |
| 3001 | Mastodon | Social feed — 24/7 presence |
| 3010 | Open WebUI | AI chat — ask anything, get answers |
| 3012 | Uptime Kuma | Service monitor — keeps itself alive |
| 3022 | AnythingLLM | Campaign memory — knows everything |
| 5678 | n8n | Automation — morning brief, pipelines, alerts |
| 8065 | Mattermost | OPS HUB — all events route here |
| 8067 | HTC Agents | Multi-agent campaign intelligence system |
| 8080 | SearXNG | Research — private search for intelligence |
| 8095 | Owncast | Live streaming — town halls, Q&A |
| 8200 | Campaign API | Petition tracker, CRM, compliance, scoreboard |
| 8888 | Traefik Dashboard | Proxy admin |
| 9001 | Listmonk | Email campaigns — newsletter, updates |
| 9091 | ntfy | Phone alerts — push to your device |
| 11434 | Ollama | AI fallback — local model on GPU |

## Internal Only (no port exposed)

| Service | Role |
|---------|------|
| PostgreSQL | Shared database for all services |
| Redis | Caching and job queues |
| Ghost DB (MySQL) | Ghost content database |
| Mastodon Sidekiq | Background job worker |
