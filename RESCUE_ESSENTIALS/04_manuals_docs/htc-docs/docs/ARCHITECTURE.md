# Hyperbolic Time Chamber — Architecture

## What This Is

A single campaign operations platform that runs 24/7 with $0. It outworks every other campaign because software doesn't take breaks.

## How It's Organized

```
hyperbolic-time-chamber/
├── docker-compose.yml       ← One file defines the entire system
├── start.sh                 ← One command brings everything online
├── .env                     ← Secrets (auto-generated on first run)
│
├── brain/                   ← AI identity and voice
│   ├── SYSTEM_PROMPT.md     ← Who the AI is (campaign intelligence)
│   ├── ROLES.md             ← How to route different tasks to different models
│   └── CONTENT_VOICE.md     ← How we talk publicly (value, story, never sell)
│
├── knowledge/
│   ├── internal/            ← Platform architecture (for accurate demos/support)
│   └── external/            ← Campaign story, numbers, opponents (for public content)
│
├── workflows/               ← n8n automation (morning brief, opponent watch, content pipeline)
├── content/                 ← Ready-to-publish content (blog, linkedin, twitter, facebook)
├── services/
│   ├── campaign-api/        ← Petition, CRM, Volunteers, Compliance, Scoreboard
│   └── chamber-bot/         ← Routes events from all services to Mattermost channels
│
├── scripts/
│   ├── init-dbs.sh          ← Creates all databases on first PostgreSQL boot
│   ├── self-repair.sh       ← Runs every 5 min, auto-restarts dead services
│   └── crontab.txt          ← Scheduled jobs (install with: crontab scripts/crontab.txt)
│
├── config/                  ← Service configurations (SearXNG engines, etc.)
├── data/                    ← Runtime data (SQLite databases, logs)
├── vault/presidential/      ← Sealed until mayoral win. Do not reference.
└── docs/                    ← This file + PORT-MAP.md
```

## The Daily Cycle

| Time | What Happens | Where It Shows Up |
|------|-------------|-------------------|
| 6:00 AM | Morning brief auto-generates | Mattermost #morning-brief + phone (ntfy) |
| 8:00 AM | Opponent watch (first scan) | Mattermost #opponent-watch |
| All day | You create content, talk to people, collect signatures | — |
| Anytime | Log contacts, signatures, hours | Campaign API → scoreboard |
| 2:00 PM | Opponent watch (second scan) | Mattermost #opponent-watch |
| 8:00 PM | Opponent watch (third scan) | Mattermost #opponent-watch |
| Evening | Check scoreboard | Campaign API /metrics/scoreboard |
| Every 5 min | Self-repair checks all services | Auto-restart + Mattermost #service-health |
| Overnight | Social monitoring continues | n8n + SearXNG |

## How To Use It

**Start everything:** `./start.sh`
**Stop everything:** `./start.sh stop`
**Check scoreboard:** `curl localhost:8200/metrics/scoreboard`
**Add petition signature:** `curl -X POST localhost:8200/petition/add -H "Content-Type: application/json" -d '{"signer_name":"Name","neighborhood":"Area","collector":"Who"}'`
**Add voter contact:** `curl -X POST localhost:8200/crm/contacts -H "Content-Type: application/json" -d '{"name":"Name","support_level":"strong"}'`
**Track published content:** `curl -X POST localhost:8200/content/published -H "Content-Type: application/json" -d '{"title":"Title","platform":"ghost"}'`
**Check compliance:** `curl localhost:8200/compliance/upcoming`
**Open the ops hub:** http://localhost:8065 (Mattermost)
**Open AI chat:** http://localhost:3010 (Open WebUI)
**Open automation:** http://localhost:5678 (n8n)
**Open blog:** http://localhost:2370 (Ghost)
**Open monitoring:** http://localhost:3012 (Uptime Kuma)

## What Makes This Different

- They have staff that works 8 hours. This works 24.
- They check news when they wake up. This already analyzed it.
- They track contacts in a spreadsheet. This projects petition completion dates.
- They pay consultants for opposition research. This scrapes automatically 3x/day.
- They go home at 5. This never stops.

## Resource Usage

- RAM: ~10-12GB (of 64GB available)
- CPU: ~20-30% idle
- Disk: ~25GB
- GPU: GTX 1660 SUPER (6GB) for Ollama inference
- Cost: $0

## Services (18 containers)

See docs/PORT-MAP.md for the full port listing.
