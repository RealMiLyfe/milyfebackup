# CAMPAIGN OS — Full Build Plan
## The Operating System for a $0 Mayoral Campaign

**This is not a dashboard. This is the single interface where the entire campaign is run.**

You open ONE app. From it you can: research, write, publish, track petitions, manage contacts, assign agents, schedule events, monitor opponents, review compliance, go live, send email blasts, check the platform, and command the war room. Everything else is infrastructure hidden behind this one surface.

---

## TECH STACK

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | **SvelteKit** | Fastest to build, lightest bundle, file-based routing, SSR optional. Alternatives: Next.js (heavier), Astro (less dynamic) |
| Styling | **Tailwind CSS** | Consistent with MiLyfe platform. Fast iteration. |
| State | **Svelte stores** + polling/SSE | No need for Redux complexity. Reactive by default. |
| Canvas | **HTML5 Canvas** (constellation) | Lightweight. No Three.js needed for 2D orbital. |
| Charts | **Chart.js** or **uPlot** | Lightweight, animated, responsive |
| Maps | **MapLibre GL** | Already in platform. Free. Offline tiles optional. |
| Icons | **Lucide** | Already in platform. Consistent. |
| Build | **Vite** (bundled with SvelteKit) | Fast dev, fast build |
| Deploy | **Docker container** (in HTC stack) | Port 8200 replaces current static files. Or build static + serve from existing campaign-api. |

**Alternative (fastest path):** Build as static SPA served by the existing campaign-api FastAPI. SvelteKit builds to static HTML/JS/CSS. Drop into `/static/`. Zero new infrastructure.

---

## INFORMATION ARCHITECTURE

### The Navigation Model

```
┌─────────────────────────────────────────────────────────────────┐
│ [COMMAND BAR — always visible, works from any view]             │
├──────────┬──────────────────────────────────────────────────────┤
│          │                                                      │
│  SIDEBAR │  MAIN CONTENT AREA                                   │
│  (nav)   │  (changes per selected module)                       │
│          │                                                      │
│  ● Home  │                                                      │
│  ● CRM   │                                                      │
│  ● Petition│                                                    │
│  ● Research│                                                    │
│  ● Content │                                                    │
│  ● Intel   │                                                    │
│  ● Calendar│                                                    │
│  ● Agents  │                                                    │
│  ● Tools   │                                                    │
│  ● Settings│                                                    │
│          │                                                      │
├──────────┴──────────────────────────────────────────────────────┤
│ [STATUS BAR — system health, tunnels, last activity]            │
└─────────────────────────────────────────────────────────────────┘
```

---

## MODULE 1: HOME (The Command Center)

**Purpose:** At-a-glance war room. The "desktop" of the OS.

**What you see:**
- Threat bar (critical items needing attention NOW)
- 5 velocity cards (petition, contacts, research, volunteers, compliance) with trend arrows
- Agent constellation (animated, interactive — click node to jump to Agent view)
- Active task queue (what agents are doing right now)
- Mini intelligence feed (last 10 items)
- Quick action buttons: "New Contact" / "Log Petition" / "Start Research" / "Draft Content"

**Data sources:**
- GET /metrics/scoreboard
- GET /health (agents)
- GET /petition/status
- GET /crm/stats
- GET /compliance/status

---

## MODULE 2: CRM (Contact Relationship Manager)

**Purpose:** Every person the campaign interacts with lives here.

### Views:

**2A. Contact List**
- Table/card view of all contacts
- Columns: Name, Organization, Tags, Support Level, Last Contact, Follow-Up Date
- Filters: by tag, by support level, by priority, by follow-up status
- Search (instant, via Meilisearch)
- Bulk actions: tag, assign priority, export

**2B. Contact Detail**
- Full profile: name, email, phone, neighborhood, org, tags, notes
- Interaction timeline: every touchpoint logged chronologically
- Support level tracker: undecided → warm → strong supporter → endorsement
- Follow-up scheduler: set next action + date + reminder
- Related contacts (same org, same neighborhood)

**2C. Add/Edit Contact**
- Form: name, email, phone, neighborhood, organization, tags, support level, notes
- Auto-tag suggestions based on organization
- Duplicate detection

**2D. Follow-Up Queue**
- All contacts with follow_up_needed = true, sorted by urgency
- One-click: "mark contacted" with a note + next follow-up date

**2E. Pipeline View**
- Kanban: Identified → Contacted → Meeting Scheduled → Met → Active Partner
- Drag to move contacts between stages

**Data sources:**
- GET /crm/contacts (list, filter, search)
- POST /crm/contacts (create)
- PATCH /crm/contacts/{id} (update)
- GET /crm/follow-ups
- GET /crm/stats

---

## MODULE 3: PETITION

**Purpose:** Track every signature from collection to verification.

### Views:

**3A. Scoreboard**
- Big number: collected / target
- Progress bar with pace indicator
- Daily rate needed vs. actual
- Trend chart (signatures per day over time)
- Projection: "At current pace, completion in X days"

**3B. Collection Points (Map)**
- MapLibre map of Jacksonville
- Pins for every collection location (churches, businesses, orgs)
- Color-coded by performance (green = producing, grey = inactive)
- Click pin → see location details, signatures collected, contact person
- Add new collection point

**3C. By Neighborhood**
- Bar chart: signatures per neighborhood/ZIP
- Shows which areas are underrepresented
- Links to Ground Game for canvassing priority

**3D. By Collector**
- Leaderboard: which volunteers/locations are producing the most
- Recognition for top collectors

**3E. Log Signatures**
- Form: batch add signatures (collector name, count, location, date)
- Single add: signer name, neighborhood, registered voter checkbox

**3F. Daily Log**
- Calendar view showing daily collection numbers
- Highlights days above/below pace

**Data sources:**
- GET /petition/status
- POST /petition/add
- POST /petition/add-batch
- GET /petition/by-collector
- GET /petition/by-neighborhood
- GET /petition/daily

---

## MODULE 4: RESEARCH

**Purpose:** The entire intelligence pipeline — from raw collection to verified, publishable findings.

### Views:

**4A. Pipeline (Kanban)**
```
QUEUED → IN PROGRESS → VERIFYING → VERIFIED → READY TO PUBLISH
```
- Each card = a research topic or claim being investigated
- Shows: topic, assigned agent, source being used, confidence level
- Drag between columns as status changes
- Click card → full detail with sources and verification stamps

**4B. Knowledge Base Browser**
- Tree view of all files in `knowledge/internal/` and `knowledge/external/`
- Click to read any document
- Search across all knowledge (Meilisearch)
- Metadata: when ingested, source, word count, entities mentioned

**4C. Research Queue**
- Add new research topics
- Assign to agents (Researcher, Analyst, Investigator)
- Priority levels: urgent, high, medium, background
- Track: who's working on it, estimated completion, blockers

**4D. Verified Claims Database**
- Every fact that has passed the Fact Checker
- Searchable by topic, keyword, chapter
- Each entry shows: claim, source, confidence, date verified, safe to publish
- Export for use in content

**4E. Contradictions Register**
- Every contradiction found between sources
- Status: unresolved, investigating, resolved
- Links to both conflicting records

**4F. Public Records Tracker**
- Every FOIA/Sunshine request submitted
- Status: drafted, submitted, acknowledged, received, denied, appealed
- Deadline tracking (FL law response requirements)
- Link received documents to knowledge base

**4G. Research Library (PDFs/Documents)**
- Uploaded documents (budget PDFs, reports, studies)
- Organized by domain (fiscal, safety, infrastructure, opponent)
- Full-text search within documents (via Meilisearch indexing)

**Data sources:**
- Local filesystem: knowledge/internal/, knowledge/external/, data/research/
- Meilisearch for search
- Custom SQLite tables (research_queue, verified_claims, contradictions, public_records_requests)
- New API endpoints needed: /research/queue, /research/verified, /research/contradictions

---

## MODULE 5: CONTENT

**Purpose:** Create, review, approve, and publish all campaign content from one place.

### Views:

**5A. Content Pipeline (Kanban)**
```
IDEA → DRAFTING → FACT CHECK → REVIEW → SCHEDULED → PUBLISHED
```
- Each card = a piece of content (blog post, social thread, newsletter, video script)
- Platform tag: Ghost, Mastodon, Social (Postiz), Email (Listmonk), Video (Owncast)
- Click card → editor

**5B. Editor**
- Rich text editor (TipTap — already in MiLyfe platform)
- Markdown support
- Sidebar: research claims library (drag verified facts into the draft)
- Sidebar: voice guide (from CONTENT_VOICE.md)
- Save draft locally
- Submit for fact check
- Publish to platform (Ghost API, Postiz API, Listmonk API)

**5C. Ghost Blog Manager** (embedded)
- Iframe of Ghost admin at :2370/ghost
- Or native integration via Ghost Content/Admin API
- See all posts, drafts, scheduled
- One-click publish from the Content pipeline

**5D. Social Scheduler** (Postiz integration)
- Embedded Postiz at :5200
- Or native integration: draft posts, set schedule, preview per platform
- Cross-post: one piece → multiple platforms

**5E. Email Campaigns** (Listmonk integration)
- Embedded Listmonk at :9001
- Or native: compose newsletter, select list, schedule, send
- See subscriber count, open rates

**5F. Video/Livestream Prep** (Owncast)
- Link to go live (:8095)
- Pre-stream checklist
- Talking points builder (pulls from research)
- Embed stream preview when live

**5G. Content Calendar**
- Calendar view: what's scheduled where, on which platform, on which day
- Drag to reschedule
- See gaps (days with no content planned)

**Data sources:**
- POST /publish/ (log published content)
- GET /publish/status
- Ghost Admin API (localhost:2370)
- Listmonk API (localhost:9001)
- Postiz API (localhost:5200)
- Custom: content_drafts table in SQLite

---

## MODULE 6: INTELLIGENCE (Opposition & Media)

**Purpose:** Track opponents, monitor media, detect threats.

### Views:

**6A. Opponent Board**
- Card per candidate: photo/avatar, party, warchest, approval, last statement, contradictions found
- Click card → full opponent profile
- Timeline of their public statements
- Donor network visualization (from campaign finance data)
- Contradiction tracker: positions that have shifted

**6B. Media Monitor**
- Feed of all Jacksonville political media mentions (from SearXNG scheduled searches)
- Sentiment indicator per article
- Filter by: outlet, candidate mentioned, topic
- Flag important stories for response

**6C. Threat Detection**
- Active threats/attacks detected by Sentinel
- Response status: unaddressed, drafted, published
- Link to Crisis Manager agent for rapid response drafting

**6D. The Hunt Dashboard**
- Visual tracker of all 10 investigation targets from hunt-targets.md
- Progress per target: data collected, gaps remaining, public records pending
- Priority ranking
- Link each target to its evidence in the research library

**6E. Social Monitor**
- Track opponent social media accounts
- GET /social/targets (managed accounts)
- GET /social/scrape/{handle} (latest posts from any handle)
- Sentiment analysis on community posts (Reddit, NextDoor mentions)

**Data sources:**
- GET /social/targets, /social/scrape/{handle}, /social/scan-all
- knowledge/internal/opposition-portfolio.md
- knowledge/internal/hunt-targets.md
- SearXNG results (localhost:8080)
- Custom: opponent_statements, media_mentions tables

---

## MODULE 7: CALENDAR

**Purpose:** Every deadline, meeting, event, and scheduled action in one timeline.

### Views:

**7A. Month View**
- Traditional calendar grid
- Color-coded events: red = deadline, blue = meeting, green = event, gold = content scheduled
- Click day → see all items

**7B. Week View**
- Hourly breakdown
- Shows: meetings, canvassing shifts, events, deadlines

**7C. Timeline View**
- Horizontal campaign timeline (Aug 2026 → Jul 2027)
- Major milestones marked: petition deadline, qualifying, primary, general, office
- Events overlaid on the timeline

**7D. Deadline Tracker**
- All compliance deadlines from /compliance/filings
- All public records request deadlines
- Petition deadline with pace indicator
- Countdown visual that gets more urgent as deadlines approach

**7E. Event Manager**
- Create community events
- Assign volunteers
- Link to petition collection (every event = signature opportunity)
- Post-event: log attendance, signatures collected, contacts made

**Data sources:**
- GET /compliance/filings, /compliance/upcoming
- Custom: events table
- Google Calendar sync (optional future)

---

## MODULE 8: AGENTS

**Purpose:** See what every agent is doing. Assign tasks. Review output. The direct agent management interface.

### Views:

**8A. Agent Grid**
- 26 agents displayed as cards grouped by function
- Each card shows: name, status (active/idle/waiting), current task, last output
- Click card → Agent Detail

**8B. Agent Detail**
- Full profile: name, role, description, model provider, channel
- Current task with progress
- Output history (last 20 responses)
- Performance: tasks completed today, avg response time, contradictions found
- Manual task assignment: type a prompt, send to this specific agent

**8C. Constellation View**
- The animated orbital visualization (from current dashboard)
- Interactive: click node → opens agent detail
- Shows data flow between agents in real-time

**8D. Agent Chat (Direct)**
- Select an agent from dropdown
- Chat directly with that one agent
- Useful for: asking Researcher a specific question, having Debate Coach prep a topic, asking Analyst for a comparison

**8E. Mattermost Embed**
- Embedded Mattermost (:8065) for when you want the full multi-channel ops view
- Shows all agent channels in one scrollable view

**Data sources:**
- GET /health (agent list + status)
- POST /chat (route to specific agent or auto-route)
- Mattermost API (localhost:8065/api/v4)
- Custom: agent_tasks, agent_outputs tables

---

## MODULE 9: TOOLS (Embedded Services)

**Purpose:** Quick access to all operational tools without switching browser tabs.

### Views (each is an embedded iframe or linked tool):

| Tool | URL | Purpose |
|------|-----|---------|
| **Mattermost** | :8065 | Full ops hub (already used via Module 8) |
| **Ghost Admin** | :2370/ghost | Blog post management |
| **Listmonk** | :9001 | Email list management |
| **Postiz** | :5200 | Social media scheduling |
| **n8n** | :5678 | Workflow automation builder |
| **Owncast** | :8095 | Livestream admin |
| **SearXNG** | :8080 | Privacy-respecting web search |
| **Uptime Kuma** | :3012 | System monitoring |
| **Umami** | :3001 | Website analytics |
| **Phoenix** | :6006 | AI observability/tracing |
| **MiLyfe Platform** | milyfe.fun | The platform itself |
| **Mayor Site** | tunnel URL | Campaign website |

Each tool opens in a full-content-area iframe with:
- A toolbar above showing: tool name, direct link (open in new tab), refresh button
- Remembers last-used view per tool

---

## MODULE 10: SETTINGS

**Purpose:** Configure the OS itself.

### Views:

**10A. System Status**
- All Docker containers with health status
- All Cloudflare tunnels with URLs
- All API endpoints with response times
- One-click restart for any service

**10B. Agent Configuration**
- View/edit agent system prompts
- Change model provider per agent
- Enable/disable agents
- View knowledge base file list

**10C. Notification Settings**
- ntfy alerts: what triggers them, where they go
- Sound preferences: enable/disable audio cues
- Threat bar: configure what shows as critical/warning/opportunity

**10D. API Keys & Secrets**
- View which keys are configured (never show values — just "✓ configured" or "✗ missing")
- Link to where to get missing keys

**10E. Tunnel Management**
- Current tunnel URLs
- One-click restart tunnels
- View tunnel health/uptime

**10F. Backup & Export**
- Export CRM contacts as CSV
- Export research database
- Export petition data
- Backup campaign.db

---

## THE PERSISTENT COMMAND BAR

**Always visible at the top of every module. Works from anywhere.**

```
┌─────────────────────────────────────────────────────────────────┐
│ ⟩ [                    type anything...                       ] │
└─────────────────────────────────────────────────────────────────┘
```

### Commands (/ prefix):
| Command | Action |
|---------|--------|
| `/brief` | Generate today's intelligence brief |
| `/research [topic]` | Queue a research task |
| `/verify [claim]` | Send to Fact Checker |
| `/scout [name]` | Run opponent scan |
| `/status` | Full system status report |
| `/contact [name]` | Search CRM, jump to contact |
| `/petition` | Jump to petition scoreboard |
| `/publish [platform]` | Start content creation for that platform |
| `/event [name]` | Create new event |
| `/deadline` | Show upcoming deadlines |
| `/hunt [target]` | Jump to investigation target |

### Natural Language (no prefix):
- "What has Deegan said about pensions?" → routes to Analyst agent
- "Draft a blog post about the budget" → opens Content editor with Speechwriter pre-loaded
- "How many petition signatures this week?" → returns data from /petition/status
- "Schedule a meeting with ICARE" → opens Calendar with new event form

### Keyboard Shortcut:
- `Cmd+K` or `Ctrl+K` → focuses the command bar from anywhere
- `Escape` → closes/blurs

---

## THE STATUS BAR (Footer — Always Visible)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🟢 19 containers │ 🟢 4 tunnels │ 🟢 26 agents │ 32 docs │    │
│                                  Last: RESEARCHER · 10:05       │
└─────────────────────────────────────────────────────────────────┘
```

- Green dots = healthy. Red = broken. Click any → jumps to Settings/System Status.
- Last activity shows which agent did what, when.

---

## THE SIDEBAR (Navigation — Always Visible)

```
┌──────────┐
│ [logo]   │
│           │
│ ● Home    │  ← constellation + velocity
│ ● CRM     │  ← contacts + pipeline
│ ● Petition│  ← signatures + map
│ ● Research│  ← pipeline + library
│ ● Content │  ← drafts + publish
│ ● Intel   │  ← opponents + media
│ ● Calendar│  ← events + deadlines
│ ● Agents  │  ← 26 agents + assign
│ ● Tools   │  ← embedded services
│ ● Settings│  ← config + system
│           │
│ ─────────│
│ [avatar]  │  ← your profile
│ MiLyfe    │
└──────────┘
```

- Icons + short labels
- Active module highlighted
- Collapsible to icon-only on small screens
- Badge indicators: red dot on CRM if follow-ups overdue, red dot on Compliance if deadline approaching

---

## DATA ARCHITECTURE

### Existing (Campaign API SQLite — campaign.db):
- petition_signatures
- contacts
- volunteers
- compliance_filings
- contributions
- activity_log
- content_published
- social_targets

### New Tables Needed:
| Table | Purpose |
|-------|---------|
| `research_queue` | Topics queued for research (id, topic, priority, assigned_agent, status, created_at) |
| `verified_claims` | Fact-checked claims (id, claim, source, source_url, confidence, verified_by, verified_at, safe_to_publish) |
| `contradictions` | Detected contradictions (id, claim_a, claim_b, type, status, detected_at) |
| `public_records_requests` | FOIA tracking (id, agency, description, date_submitted, response_deadline, status, documents_received) |
| `opponent_statements` | Logged statements (id, candidate, statement, source, date, contradicts_id) |
| `media_mentions` | Tracked media (id, outlet, headline, url, sentiment, candidate_mentioned, date) |
| `events` | Campaign events (id, name, date, location, type, volunteers_assigned, signatures_collected, notes) |
| `content_drafts` | Unpublished content (id, title, body, platform, status, assigned_agent, fact_check_status, created_at) |
| `agent_tasks` | Task assignments (id, agent_name, task, status, progress_pct, started_at, completed_at) |

### New API Endpoints Needed:
| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/research/queue` | Manage research queue |
| GET/POST | `/research/verified` | Verified claims database |
| GET | `/research/contradictions` | Contradiction register |
| GET/POST | `/records/requests` | Public records tracking |
| PATCH | `/records/requests/{id}` | Update request status |
| GET/POST | `/intel/statements` | Opponent statement log |
| GET | `/intel/media` | Media mention feed |
| GET/POST | `/events` | Event management |
| PATCH | `/events/{id}` | Update event |
| GET/POST | `/content/drafts` | Content draft management |
| PATCH | `/content/drafts/{id}` | Update draft status |
| GET/POST | `/agents/tasks` | Agent task management |
| PATCH | `/agents/tasks/{id}` | Update task progress |

---

## REAL-TIME DATA FLOW

| Source | Method | Refresh |
|--------|--------|---------|
| Scoreboard metrics | Polling GET /metrics/scoreboard | Every 15s |
| Agent health | Polling GET /health | Every 10s |
| Agent activity feed | Mattermost WebSocket API | Real-time |
| Platform metrics | Polling GET /platform/metrics | Every 60s |
| Tunnel health | Polling metrics endpoints | Every 30s |
| Compliance deadlines | Polling GET /compliance/upcoming | Every 5 min |
| Media mentions | SearXNG + store | Every 15 min (background) |

For true real-time: Mattermost's WebSocket API streams all channel messages. The OS subscribes to all agent channels and displays activity as it happens in the feed.

---

## NOTIFICATION SYSTEM

### In-App Notifications:
- Threat bar items (always visible)
- Toast notifications for: new petition signature, task completed, threat detected, deadline approaching
- Badge indicators on sidebar modules

### Push Notifications (ntfy):
- Critical: DS-DE 9 still unfiled (daily until resolved)
- Critical: petition pace below 50% of needed daily rate
- Warning: compliance deadline within 7 days
- Alert: new opponent activity detected
- Info: research task completed, content published

### Sound Cues (optional):
- Soft chime: new verified fact
- Low tone: petition signature logged
- Alert: threat detected
- Completion: task finished

---

## BUILD ORDER (Implementation Phases)

### Phase 0: Foundation (2-3 days)
1. Scaffold SvelteKit project with Tailwind
2. Build the layout shell: sidebar, command bar, status bar, content area
3. Implement routing for all 10 modules
4. Build the polling data layer (scoreboard, health, metrics)
5. Deploy as Docker container replacing current static files at :8200

### Phase 1: Core Operations (3-4 days)
6. Module 1: Home (constellation + velocity + threat bar + task queue)
7. Module 2: CRM (full CRUD — list, detail, add, edit, pipeline, follow-ups)
8. Module 3: Petition (scoreboard, log signatures, map, by-neighborhood)
9. Command bar: implement all / commands + natural language routing

### Phase 2: Intelligence (3-4 days)
10. Module 4: Research (pipeline kanban, knowledge browser, verified claims, public records tracker)
11. Module 6: Intelligence (opponent board, media monitor, hunt dashboard)
12. Add new API endpoints + SQLite tables for research/intel
13. Wire up SearXNG for background collection

### Phase 3: Content & Publishing (2-3 days)
14. Module 5: Content (pipeline kanban, editor with TipTap, Ghost/Listmonk/Postiz integration)
15. Content calendar view
16. Module 7: Calendar (month/week/timeline, deadline tracker, event manager)

### Phase 4: Agents & Tools (2-3 days)
17. Module 8: Agents (grid, detail, constellation, direct chat, Mattermost embed)
18. Module 9: Tools (iframe wrappers for all services)
19. Module 10: Settings (system status, agent config, tunnel management)

### Phase 5: Polish (2-3 days)
20. Animations: constellation interactions, view transitions, loading states
21. Notifications: toast system, badge indicators, ntfy integration
22. Sound cues (optional toggle)
23. Ambient mode for the home constellation
24. Mobile responsive: sidebar collapses, content stacks
25. Keyboard shortcuts: Cmd+K (command bar), Cmd+1-9 (jump to module), Escape
26. Performance: code splitting per module, lazy loading, caching

---

## TOTAL ESTIMATED BUILD TIME

| Phase | Time | What |
|-------|------|------|
| Phase 0 | 2-3 days | Foundation, routing, layout |
| Phase 1 | 3-4 days | Home, CRM, Petition, Command bar |
| Phase 2 | 3-4 days | Research, Intelligence |
| Phase 3 | 2-3 days | Content, Calendar |
| Phase 4 | 2-3 days | Agents, Tools, Settings |
| Phase 5 | 2-3 days | Polish, animations, notifications |
| **TOTAL** | **14-20 days** | Full campaign OS |

---

## WHAT THIS REPLACES

| Before | After |
|--------|-------|
| Open Mattermost in tab 1 | Agents module in the OS |
| Open Ghost in tab 2 | Content module → Ghost embedded |
| Open Listmonk in tab 3 | Content module → Email section |
| Open campaign API in tab 4 | Home + CRM + Petition modules |
| Open Postiz in tab 5 | Content module → Social section |
| Open n8n in tab 6 | Tools module |
| Open SearXNG in tab 7 | Research module + background collection |
| Open Uptime Kuma in tab 8 | Settings → System Status |
| Manually check agent health | Agents module + status bar |
| Manually track petition pace | Petition module + Home velocity |
| Manually log contacts | CRM module |
| Manually check compliance | Calendar → Deadline tracker |

**Result: 8+ browser tabs → 1 app. Everything in one window. Nothing gets forgotten because everything is visible.**

---

## THE FEELING

When you open this app in the morning:

1. You see the constellation showing agents already working (they ran overnight research)
2. The threat bar tells you what needs YOU today (not what's happening automatically)
3. The velocity cards show if you're on pace or behind
4. You hit Cmd+K, type "/brief" — Commander generates today's priorities
5. You click into CRM, see 5 contacts due for follow-up, make your calls, log them
6. You click into Research, see Fact Checker verified 3 new claims overnight — drag them to "Ready to Publish"
7. You click into Content, open the editor, pull verified claims from the sidebar, draft a blog post, submit for fact check
8. You click into Petition, see the map, note which collection points need fresh forms
9. You click into Calendar, see ICARE meeting Tuesday, EWU speaking engagement Thursday
10. You click Home, check the constellation one more time, see everything flowing. Close the laptop. The machine keeps running.

**That's an operating system. Not a dashboard.**

---

## FILE STRUCTURE (Project Scaffold)

```
hyperbolic-time-chamber/
└── dashboard/                    ← NEW: The Campaign OS
    ├── package.json
    ├── svelte.config.js
    ├── tailwind.config.js
    ├── vite.config.js
    ├── Dockerfile
    ├── src/
    │   ├── app.html
    │   ├── app.css              (Tailwind base + custom)
    │   ├── lib/
    │   │   ├── api.js           (all fetch wrappers)
    │   │   ├── stores.js        (reactive state)
    │   │   ├── constants.js     (agent list, colors, endpoints)
    │   │   └── components/
    │   │       ├── CommandBar.svelte
    │   │       ├── Sidebar.svelte
    │   │       ├── StatusBar.svelte
    │   │       ├── ThreatBar.svelte
    │   │       ├── VelocityCard.svelte
    │   │       ├── Constellation.svelte
    │   │       ├── TaskQueue.svelte
    │   │       ├── AgentCard.svelte
    │   │       ├── ContactCard.svelte
    │   │       ├── PetitionMap.svelte
    │   │       ├── ResearchCard.svelte
    │   │       ├── ContentEditor.svelte
    │   │       ├── OpponentCard.svelte
    │   │       ├── CalendarView.svelte
    │   │       ├── IframeEmbed.svelte
    │   │       └── Toast.svelte
    │   └── routes/
    │       ├── +layout.svelte    (shell: sidebar + command bar + status bar)
    │       ├── +page.svelte      (Module 1: Home)
    │       ├── crm/
    │       │   ├── +page.svelte  (contact list)
    │       │   └── [id]/+page.svelte (contact detail)
    │       ├── petition/
    │       │   ├── +page.svelte  (scoreboard)
    │       │   └── map/+page.svelte
    │       ├── research/
    │       │   ├── +page.svelte  (pipeline)
    │       │   ├── library/+page.svelte
    │       │   └── verified/+page.svelte
    │       ├── content/
    │       │   ├── +page.svelte  (pipeline)
    │       │   ├── editor/+page.svelte
    │       │   └── calendar/+page.svelte
    │       ├── intel/
    │       │   ├── +page.svelte  (opponent board)
    │       │   ├── media/+page.svelte
    │       │   └── hunt/+page.svelte
    │       ├── calendar/
    │       │   └── +page.svelte
    │       ├── agents/
    │       │   ├── +page.svelte  (grid + constellation)
    │       │   └── [name]/+page.svelte (detail)
    │       ├── tools/
    │       │   └── +page.svelte  (iframe grid)
    │       └── settings/
    │           └── +page.svelte
    └── static/
        └── logo.png
```

---

## DOCKER INTEGRATION

Add to `docker-compose.yml`:
```yaml
campaign-os:
  build:
    context: ./dashboard
    dockerfile: Dockerfile
  container_name: htc-campaign-os
  restart: unless-stopped
  networks: [chamber]
  ports:
    - "8300:3000"
  depends_on:
    - campaign-api
```

Or simpler: build SvelteKit as static site → copy output to campaign-api's `/static/` directory. Zero new containers.

---

## WHAT'S NOT IN THIS OS (By Design)

- The MiLyfe citizen platform (milyfe.fun) — that's a separate product for citizens. The OS is for the operator.
- Public-facing petition form — that stays on mijaxx.fun. The OS is internal.
- Detailed financial accounting — no double-entry bookkeeping. Just compliance tracking.
- Voter file management — too complex for v1. Use the dormant voter analysis from research instead.

---

*This is the full build plan. Every module. Every view. Every endpoint. Every data source. Every interaction. Nothing missing.*

*When this is built, you never open another tab. The campaign runs from one window.*
