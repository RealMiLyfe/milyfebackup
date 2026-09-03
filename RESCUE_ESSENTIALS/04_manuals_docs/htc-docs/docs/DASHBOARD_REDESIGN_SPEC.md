# HYPERBOLIC TIME CHAMBER — Dashboard Redesign Spec
## Full UX/UI Overhaul with Agent Visualization

**Current state:** Single-page HTML dashboard at port 8200 with scoreboard, service health dots, Mattermost feed, and chat. Functional but flat — no sense of the 26 agents being alive.

**Target state:** An animated command center where you can SEE your agents working, SEE the research pipeline moving, SEE petition progress growing, and SEE threats emerging — all in real-time.

---

## THE VISION: A LIVING WAR ROOM

When you open the dashboard, you should feel like you're looking into a machine that's running 24/7 even when you're not watching. The 26 agents aren't just names in a list — they're visualized entities with state, activity, and personality.

---

## LAYOUT — THREE-ZONE ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────────────────┐
│ HEADER: Countdown Ticker │ Status Badges │ Quick Actions              │
├────────────────────┬─────────────────────────┬───────────────────────────┤
│                    │                         │                           │
│   LEFT ZONE        │    CENTER ZONE          │    RIGHT ZONE             │
│   (260px)          │    (flex)               │    (360px)                │
│                    │                         │                           │
│   Navigation       │    Main Content         │    Intelligence Feed      │
│   Agent Roster     │    (switches views)     │    + Chat                 │
│   Status Dots      │                         │                           │
│                    │                         │                           │
├────────────────────┴─────────────────────────┴───────────────────────────┤
│ FOOTER: System health │ Tunnel status │ Last agent activity            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ZONE 1: LEFT SIDEBAR — The Agent Roster

### Agent List (always visible)
Each of the 26 agents displayed as a compact card:

```
┌─────────────────────────┐
│ ● COMMANDER      [idle] │  ← dot color = state
│   Strategy & Decisions  │  ← role in small text
├─────────────────────────┤
│ ◉ RESEARCHER   [active] │  ← pulsing dot = working
│   Primary Sources       │
├─────────────────────────┤
│ ○ FACT CHECKER [waiting]│  ← hollow dot = waiting for input
│   Verification Gate     │
├─────────────────────────┤
│ ● SENTINEL      [idle]  │
│   Threat Monitor        │
└─────────────────────────┘
```

### Agent States (animated)
| State | Visual | Meaning |
|-------|--------|---------|
| **Active** | Pulsing green dot + subtle glow | Currently processing a task |
| **Idle** | Solid dim dot (grey-green) | Ready, waiting for input |
| **Waiting** | Hollow amber dot, slow pulse | Blocked on another agent's output |
| **Alert** | Red dot, fast pulse | Something needs attention |
| **Error** | Red X, no animation | Failed, needs intervention |

### Agent Groups (collapsible)
- **Command** (3): Commander, Guardian, Compliance Officer
- **Intelligence** (5): Analyst, Researcher, Investigator, Oppo Tracker, Fact Checker
- **Content** (4): Speechwriter, Storyteller, Content Producer, Media Coach
- **Operations** (5): Ground Game, Coalition Builder, Community Liaison, Connector, Scheduler
- **Systems** (4): Sentinel, Data Engineer, Builder, Crisis Manager
- **Strategy** (5): Scout, Debate Coach, Pollster, Fundraiser, Justice Tracker

### Clicking an Agent → Opens their detail in Center Zone

---

## ZONE 2: CENTER — Main Content Area (View Switching)

### VIEW 1: Command Center (Default)

The "war room at a glance" view:

**Top Row — The Big Numbers (animated counters)**
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PETITION    │  │  CONTACTS    │  │  RESEARCH    │  │  COMPLIANCE  │
│              │  │              │  │              │  │              │
│    0/1000    │  │     24       │  │   3 docs     │  │  ⚠ DS-DE 9   │
│              │  │              │  │   verified   │  │    OVERDUE   │
│  ▓░░░░ 0%   │  │  +0 today    │  │   7 pending  │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

**Middle — Agent Activity Visualization (THE CENTERPIECE)**

An animated orbital/constellation view showing all 26 agents as nodes:
- Center: The Commander (largest node)
- Inner ring: Intelligence agents (Analyst, Researcher, Investigator, Fact Checker, Oppo Tracker)
- Middle ring: Content + Operations agents
- Outer ring: Systems + Strategy agents
- Connections: Lines between agents that are currently passing data to each other (animated particles flowing along the line)
- Active agents: Brighter, slightly larger, with a gentle pulse
- Idle agents: Dimmer, smaller, static

When an agent is processing:
- Their node brightens and grows slightly
- A particle trail flows from them to the knowledge base (center bottom)
- If they're waiting on another agent, a dotted line shows the dependency

**Bottom — Morning Brief + Research Status**

Two side-by-side panels:
- Left: Today's brief (text, from the morning-brief workflow)
- Right: Research pipeline status (which documents are being processed, which claims are being verified)

---

### VIEW 2: Agent Detail (When you click an agent)

Full page for one agent:
```
┌──────────────────────────────────────────────────────────────┐
│ ◉ RESEARCHER                                    [ACTIVE]     │
│ Primary Source Research & Data Extraction                     │
│ Provider: Gemini │ Channel: #investigations                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ CURRENT TASK                                                 │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Extracting JSO budget line items from FY26-27 budget     │ │
│ │ Source: jacksonville_fy2627_budget_highlights.pdf         │ │
│ │ Progress: ████████░░ 80%                                 │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ RECENT OUTPUT (last 5 items)                                 │
│ ─────────────────────────────────────────────────────────── │
│ • Verified: JSO FY26-27 operating budget = $XXX,XXX,XXX     │
│ • Verified: General Fund total = $2,026,502,015              │
│ • Pending: Pension contribution exact figure (searching)     │
│                                                              │
│ PERFORMANCE                                                  │
│ Tasks completed today: 3 │ Avg response time: 2.4s          │
│ Verifications passed: 3/3 │ Contradictions found: 0         │
│                                                              │
│ [Assign Task] [View History] [View Channel]                  │
└──────────────────────────────────────────────────────────────┘
```

---

### VIEW 3: Research Pipeline

Visual Kanban-style board showing the research workflow:

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   QUEUED     │  │  RESEARCHING │  │  VERIFYING   │  │  REVIEWED    │  │  READY       │
│              │  │              │  │              │  │              │  │              │
│ Ch.3 Afford  │  │ Ch.2 Budget  │  │ JSO budget # │  │ Pension #    │  │ (none yet)   │
│ Ch.7 Transit │  │ Ch.4 Safety  │  │ Septic count │  │              │  │              │
│ Ch.9 River   │  │              │  │              │  │              │  │              │
│ Ch.10 Machine│  │              │  │              │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
         ↓                ↓                 ↓                 ↓                ↓
    Researcher →    Researcher →    Fact Checker →    Compliance →    Content Producer
```

Each card shows: claim being verified, source being used, which agent owns it, confidence level.

---

### VIEW 4: Petition Map

A map of Jacksonville showing:
- Collection points (churches = cross icon, businesses = shop icon, orgs = star icon)
- Heat coloring by signatures collected per location
- Sidebar: ranked list of top-performing locations
- Running total counter with daily trend line

---

### VIEW 5: Opposition Board

One card per candidate:
```
┌────────────────────────────┐
│ 📷 DONNA DEEGAN            │
│ Democrat (Incumbent)       │
│ War Chest: $1.4M+          │
│ Approval: 62%              │
│ Contradictions found: 0    │
│ Last statement: [date]     │
│ [Full Profile] [Tracker]   │
└────────────────────────────┘
```

---

### VIEW 6: Intelligence Feed (The Hunt)

Chronological feed of every intelligence finding, grouped by domain:
- Fiscal findings
- Opponent moves
- Media mentions
- Public records responses
- Contradiction alerts

Each item shows: finding, source, verification level, which agent found it, timestamp.

---

## ZONE 3: RIGHT PANEL — Live Feed + Chat

### Top Half: Live Activity Stream
Real-time feed from Mattermost showing what agents are posting:
```
[10:03] #investigations INVESTIGATOR: Downloading FY26-27 full budget PDF...
[10:05] #investigations RESEARCHER: Extracting JSO allocation from page 47...
[10:07] #compliance FACT_CHECKER: VERIFIED — General Fund = $2,026,502,015
[10:08] #justice-watch JUSTICE_TRACKER: New in-custody death report found (News4Jax)
```

Color-coded by urgency:
- Green: routine activity
- Amber: needs attention
- Red: critical finding or threat

### Bottom Half: Chat (Commander Interface)
Direct chat with the intelligence system. Ask any question, it routes to the right agent and returns a grounded answer.

---

## THE AGENT CONSTELLATION ANIMATION — Detailed Spec

This is the centerpiece visual. It's inspired by:
- Network topology diagrams
- Solar system orbital views
- Neural network visualizations

### Technical Approach
- HTML5 Canvas or Three.js (for smooth 60fps animation)
- WebSocket connection to the agent health endpoint for real-time state
- Particle system for data flow visualization

### Node Design (Each Agent)
- Circle with agent's initial letter
- Size: proportional to current activity level
- Color: based on group (Intelligence = blue, Content = green, Operations = amber, Systems = grey, Strategy = purple, Command = gold)
- Ring: solid when active, dashed when idle
- Glow: subtle pulsing glow when processing

### Connection Lines (Data Flow)
- When Researcher sends data to Fact Checker: animated dot flows along the line between them
- When Fact Checker approves: green flash on the connection
- When Fact Checker rejects: red flash
- Lines are only visible when there's active data flow (not always connected)

### Center Hub (Knowledge Base)
- Represented as a glowing core in the center
- Every time data gets stored, a particle flows FROM an agent INTO the center
- The core gets slightly brighter each time knowledge is added (visual compounding)

### Interaction
- Hover over a node: shows agent name, current task, status
- Click a node: navigates to Agent Detail view
- Hover over a connection: shows what data is flowing

---

## HEADER — Always Visible

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Logo] HYPERBOLIC TIME CHAMBER  │  PET: 109d │ QUAL: 138d │ PRI: 208d │
│                                 │  26 agents │ 32 docs   │ 3 verified │
└──────────────────────────────────────────────────────────────────────────┘
```

- Countdown timers tick in real-time (update every minute)
- Agent count shows how many are currently loaded
- Doc count shows knowledge base size
- Verified count shows Fact Checker approved items

---

## FOOTER — System Health Bar

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 🟢 19 containers │ 🟢 4 tunnels │ 🟢 26 agents │ Last: 10:08 RESEARCHER│
└──────────────────────────────────────────────────────────────────────────┘
```

Green dots for each system. If anything goes red, it's immediately visible.

---

## GITHUB REPOS TO CLONE/REFERENCE FOR IMPLEMENTATION

| Repo | What It Provides | URL |
|------|-----------------|-----|
| **claude-agent-monitor** | 2D Canvas dashboard with animated characters and task tracking | github.com/pacho-h/claude-agent-monitor |
| **ai-agent-session-center** | 3D robots representing agents with live terminals | github.com/coding-by-feng/ai-agent-session-center |
| **openclaw-jarvis-ui** | Three.js orb with real-time state visualization (thinking/responding/idle) | github.com/jincocodev/openclaw-jarvis-ui |
| **openclaw-virtual-office** | Pixel-art office with animated walking agents | github.com/thx0701/openclaw-virtual-office |
| **openclaw-monitor** | 3D continents with minion agents, physics, thinking bubbles | github.com/ccperdst-lab/openclaw-monitor |
| **agent-swarm-dashboard** | Multi-agent missions with streaming timeline and Mermaid graph | github.com/Smilkoski/agent-swarm-dashboard |
| **openclaw-pixel-agents-dashboard** | Pixel art agents with activity bubbles and service controls | github.com/jaffer1979/openclaw-pixel-agents-dashboard |
| **opencampaign** | Open source political campaign software | github.com/c3o/opencampaign |
| **Petitions** | Browser app for processing petition signatures against voter directory | github.com/will292929/Petitions |
| **hermes-office-main** (already in workspace) | 3D agent office with Three.js | /home/milyfe/milyfe-ai-workspace/virtual-office/hermes-office-main |

---

## COLOR SYSTEM (Dark Theme — Campaign Brand)

| Token | Value | Use |
|-------|-------|-----|
| --bg-primary | #0F1A2E | Main background |
| --bg-card | #1A2840 | Cards, panels |
| --bg-hover | #243350 | Hover states |
| --text-primary | #E8F0F8 | Main text |
| --text-secondary | #9AABAB | Subtitles, labels |
| --text-dim | #6B7F7F | Tertiary info |
| --teal | #087F73 | Primary brand, success, active agents |
| --gold | #FFC107 | Warnings, petition counter, highlights |
| --danger | #B4232D | Errors, alerts, critical |
| --civic-blue | #0B668C | Links, interactive elements |
| --intelligence-blue | #3B82F6 | Intelligence domain agents |
| --content-green | #10B981 | Content domain agents |
| --ops-amber | #F59E0B | Operations domain agents |
| --strategy-purple | #8B5CF6 | Strategy domain agents |
| --command-gold | #F5C518 | Command group agents |

---

## ANIMATION PRINCIPLES

1. **Subtle, continuous motion** — Nothing is ever fully static. Even idle agents have a very subtle breathing pulse (opacity 0.8 → 1.0, 3s cycle).
2. **State transitions are smooth** — When an agent goes from idle to active, it fades in brightness over 300ms, not instantly.
3. **Data flow is visible** — Particles move along connection lines at a readable speed (not too fast to see, not too slow to be boring).
4. **Notifications don't interrupt** — New findings slide in from the right feed, they don't pop up as modals.
5. **Performance first** — Use requestAnimationFrame for canvas. Keep DOM updates batched. The dashboard must be smooth on your desktop even with 19 Docker containers running.

---

## DATA SOURCES (What the Dashboard Pulls)

| Endpoint | Data | Refresh Rate |
|----------|------|--------------|
| GET /health (agents) | Agent count, status per agent | Every 10s |
| GET /metrics/scoreboard | Petition, contacts, volunteers, content, compliance | Every 30s |
| GET /platform/metrics | MiLyfe citizens, treasury, voters | Every 60s |
| WebSocket /ws/feed | Real-time Mattermost activity | Live stream |
| GET /petition/status | Petition detailed stats | Every 30s |
| Docker API (local) | Container health status | Every 30s |
| Tunnel metrics (localhost:2024x) | Tunnel connectivity | Every 60s |

---

## IMPLEMENTATION APPROACH

1. **Phase 1:** Replace current static HTML with a React/Vite SPA (or Svelte for lighter weight)
2. **Phase 2:** Build the agent constellation canvas animation
3. **Phase 3:** Add the view switching (Command Center, Agent Detail, Research Pipeline, etc.)
4. **Phase 4:** Connect real-time data via WebSocket to Mattermost
5. **Phase 5:** Add the petition map and opposition board

**Recommended stack:**
- Svelte or React (whichever the Builder agent is faster with)
- Three.js or HTML5 Canvas for the constellation
- Chart.js or D3 for the petition progress and trend lines
- Mapbox/MapLibre for the petition collection map (you already have MapLibre in the platform)

---

## THE FEELING

When you open this dashboard, you should feel like Tony Stark looking at JARVIS. Not because it's flashy — because it's ALIVE. You see 26 nodes gently orbiting. You see particles flowing between them. You see the knowledge base core glowing brighter as research accumulates. You see the petition counter ticking. You see threats highlighted in red before they become problems.

This is not a reporting tool. This is a window into an intelligence machine that never sleeps.
