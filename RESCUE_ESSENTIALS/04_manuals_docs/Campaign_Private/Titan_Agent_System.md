# Titan Agent System — Campaign AI Staff

**PRIVATE. Not part of the platform.**

---

## Overview

The Titan system is a 25-agent AI campaign staff connected via Mattermost, managed by the Titan Bridge API (FastAPI, port 8099), backed by Ollama with multiple models. Each agent has a specific role, model assignment, Mattermost channel, and campaign duties.

This is SEPARATE from the 25 named platform helpers (Sam, Nia, Rue, etc.) which serve citizens. Titan serves the campaign.

---

## The 25 Campaign Agents

| # | Name | Role | Model | Channel |
|---|---|---|---|---|
| 1 | Aegis | Legal Defense Network | deepseek-r1:14b | #legal-defense |
| 2 | Atlas | Infrastructure Intelligence | deepseek-r1:14b | #infrastructure-intel |
| 3 | Calvin | Fundraising & Donor Management | qwen2.5:14b | #daily-ops |
| 4 | Cipher | Security & Privacy | deepseek-r1:14b | #security-ops |
| 5 | Dex | Communications Director | qwen2.5:14b | #communications |
| 6 | Echo | Media & Content Production | mistral:latest | #content-studio |
| 7 | Flux | Economic Modeling | qwen2.5:32b | #economic-modeling |
| 8 | Forge | Campaign Commander | qwen2.5:32b | #campaign-command |
| 9 | Frank | Budget Analysis & Policy Research | qwen2.5:32b | #daily-ops |
| 10 | Harbor | Humanitarian Response | qwen2.5:14b | #humanitarian-ops |
| 11 | Ian | Platform Resource Tracking | qwen2.5:14b | #daily-ops |
| 12 | Iris | Document Analysis & Evidence | llava:13b | #daily-ops |
| 13 | Leo | Platform Builder | qwen2.5:14b | #daily-ops |
| 14 | Lia | Legal, FEC Compliance & Ballot Access | qwen2.5:14b | #compliance |
| 15 | Mirror | Digital Twin Operations | qwen2.5:14b | #twin-ops |
| 16 | Nexus | Integration & API Intelligence | qwen2.5-coder:32b | #api-ecosystem |
| 17 | Nova | Digital Twin Lead | qwen2.5:32b | #digital-twins |
| 18 | Oracle | Predictive Intelligence | llama3.1:70b | #predictions |
| 19 | Paula | Donor Management & Wave Outreach | qwen2.5:14b | #daily-ops |
| 20 | Prism | Data Science & Analytics | deepseek-r1:14b | #data-intelligence |
| 21 | Sage | Wisdom & Learning | qwen2.5:14b | #milearn-hub |
| 22 | Sam | Citizen Response & Mi AI | qwen2.5:14b | #daily-ops |
| 23 | Serena | Research & Opposition Director | qwen2.5:14b | #research-intel |
| 24 | Terra | Environmental Intelligence | qwen2.5:14b | #earth-systems |
| 25 | Verse | Arts & Culture | mistral:latest | #culture-hub |

---

## 7 Brain Role Modes

The master brain activates different modes via bracket commands in Open WebUI:

| Mode | Model | Activation | Purpose |
|---|---|---|---|
| Campaign Commander | qwen2.5:32b | `[Strategy]` `[Priorities]` | Decisions, priorities, web search, n8n |
| Research Director | deepseek-r1:14b + llama3.1:70b | `[Research]` `[Analyze]` | Deep analysis, SearXNG, RAG |
| Communications Director | mistral + qwen2.5:32b | `[Write]` `[Draft]` | Brand, writing, scheduling |
| Policy Director | deepseek-r1:14b | `[Policy]` `[Legal]` | cOS White Paper, legal research |
| Rapid Response | llama3.1:8b | `[Urgent]` `[Breaking]` | Talking points, quick drafts |
| Platform Builder | qwen2.5-coder:32b | `[Build]` `[Code]` | Docker, git, code execution |
| Mi (Citizen AI) | qwen2.5:14b | `[Mi]` `[Citizen]` | Platform features, citizen DB |

---

## Titan Bridge API (FastAPI, Port 8099)

**File:** `OtherMilyfeBuilds/MiCity/core/miforge/agent_api.py`

### Endpoints

| Method | Path | What It Does |
|---|---|---|
| GET | /health | Ollama connection + model status |
| GET | /health/models | Check expected models loaded |
| GET | /agents/status | List all agents with roles/channels |
| POST | /agents/standup | Trigger daily standup |
| POST | /agents/retrospective | Weekly retrospective |
| POST | /agents/invoice-report | Daily invoice report |
| POST | /agents/announce | All agents announce in channels |
| POST | /agents/serena/research | Opposition/company research |
| POST | /agents/serena/monitor | Vendor landscape monitoring |
| POST | /agents/frank/summary | Client financial summary (hledger) |
| POST | /agents/frank/all-clients | Consolidated financial overview |
| POST | /agents/leo/errors | Error log analysis |
| POST | /agents/leo/retrospective | Learning retrospective |
| POST | /agents/dex/draft-email | Vendor email drafting |
| POST | /agents/ian/recurring | Recurring vendor check |
| POST | /agents/sam/status | Support desk status |
| POST | /ollama/generate | Direct model access |
| POST | /clients/onboard | New client setup |
| GET | /clients/list | List all clients |
| GET | /clients/{name}/ledger | Client balance/register |

### Auth
Bearer token from `/opt/milyfe/secrets/bridge-token.txt`

### Integration
- Mattermost for all agent output
- hledger for double-entry accounting per client
- Ollama (local) for all AI inference
- CORS allowed: localhost:7800, localhost:3000, milyfe.fun, *.vercel.app

---

## 11 Core Titan Bots (Runtime)

| Bot Key | Channel |
|---|---|
| forge-supervisor | #campaign-command |
| serena-research | #research-intel |
| dex-ops | #communications |
| lia-legal | #compliance |
| calvin-ar | #daily-ops |
| frank-finance | #daily-ops |
| paula-payroll | #daily-ops |
| ian-inventory | #daily-ops |
| sam-support | #daily-ops |
| iris-vision | #daily-ops |
| leo-learning | #daily-ops |

---

## Key Dates

- Qualifying: January 11, 2027
- Primary: March 9, 2027
- Presidency target: July 1, 2027

---

## Identity Voice (Shared Across All 25 Agents)

"We not I. Always. We are the next President. The platform is the proof."

---

## Campaign Documents (from old builds)

Located at `OtherMilyfeBuilds/MiLyfe-repo/campaign_docs/` and `OtherMilyfeBuilds/MiCity/campaign_docs/`:

1. **01_MASTER_CONTEXT.md** — Full candidate profile, argument, 5 policy pillars, key dates, opponent brief
2. **02_RESEARCH_INDEX.md** — Research index
3. **03_ZERO_DOLLAR_PROOF.md** — Technical stack breakdown (80+ containers, 21 AI models, $0)
4. **04_OPPOSITION_FILE.md** — Donna Deegan analysis, contrast strategy, attack rules
5. **05_THE_HUMAN_STORY.md** — Full timeline 1986-2026, turning point, campaign lines
6. **FOUNDING_TEN_MESSAGES.md** / **FOUNDING_TWELVE_MESSAGES.md** — Wave messaging
7. **MERCHANT_PLEDGE_SHEET.md** — Local business onboarding

MiCity also has subdirs: `legal/`, `opposition/`, `personal/`, `policy/`, `research/`

---

## How This Relates to the Platform

The platform (MiLyfe) and the campaign (Titan) are SEPARATE:
- MiLyfe serves ALL citizens regardless of politics
- Titan serves the campaign strategy
- They share infrastructure (same Ollama models, same servers)
- They do NOT share identity, branding, or purpose in any public-facing way
- The platform works whether the run succeeds or not
- The platform IS the proof — it demonstrates the governance model works

### Campaign Brand Line (for the Communications Director and any agent producing public copy)

- The campaign slogan is **"We The People."** Use it in campaign headers, hero eyebrows, page titles, meta/OG/Twitter, and footers across `campaign-website/` and `public_html/`.
- It is a CAMPAIGN slogan only. Never attach it to the product. The product taglines stay as-is: "Your life, together — privately." (app) and "Add Value. Raise Quality of Life." (platform).
- See `Strategy.md` → "Campaign Slogan / Brand Line" for the canonical definition and usage rules.
