# THE ULTIMATE INTEGRATION DESIGN
## Three Systems, One Nervous System

---

## THE VISION

Three systems that operate as ONE organism:

```
                    ┌─────────────────────────────┐
                    │     THE PUBLIC              │
                    │  (Jacksonville Citizens)    │
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────────┐
              │                │                    │
              ▼                ▼                    ▼
   ┌──────────────────┐ ┌──────────────┐ ┌─────────────────┐
   │    MIJAXX.FUN    │ │  MILYFE.FUN  │ │ PUBLIC DASHBOARD│
   │  (Campaign Door) │ │ (The Proof)  │ │ (/illuminate)   │
   └────────┬─────────┘ └──────┬───────┘ └────────┬────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │  CAMPAIGN API (:8200) │
                    │  (The Nerve Center)   │
                    └───────────┬───────────┘
                                │
           ┌────────────────────┼──────────────────────┐
           │                    │                       │
           ▼                    ▼                       ▼
   ┌───────────────┐  ┌─────────────────┐  ┌────────────────────┐
   │ 26 AI AGENTS  │  │  MATTERMOST     │  │  PUBLISHING STACK  │
   │ (Intelligence)│  │  (Operations)   │  │  Ghost/Listmonk/   │
   │               │  │                 │  │  Postiz/Owncast    │
   └───────────────┘  └─────────────────┘  └────────────────────┘
```

---

## THE THREE ROLES

### System 1: The Time Chamber = THE BRAIN
Everything that thinks, researches, decides, and produces content lives here.
- Intelligence gathering (SearXNG, research, OSINT)
- Content creation (Ghost → blog, Postiz → social, Listmonk → email)
- Agent coordination (Mattermost channels)
- Strategy (opposition research, media monitoring)
- Operations (CRM, volunteer management, petition tracking)
- Compliance (filing deadlines, ethics)

### System 2: MiJaxx.fun = THE MOUTH
Everything the public sees from the CAMPAIGN lives here.
- The campaign story (who, why, platform)
- Petition collection (public form → HTC)
- Volunteer recruitment (public form → HTC)
- Email list growth (form → Listmonk)
- Published content (from Ghost/HTC)
- Live petition counter (from Campaign API)
- Accountability dashboard (/illuminate — from research)
- Blog feed (from Ghost)
- Event announcements
- Video embed (from Owncast)

### System 3: MiLyfe.fun = THE PROOF
Everything that demonstrates the governance model lives here.
- The working platform (wallet, governance, learn, safety, etc.)
- Real citizens using it
- Real $MLY circulating
- Real proposals being voted on
- Real resources being found
- Real community forming
- This is NOT the campaign. This IS the proof the campaign points at.

---

## THE DATA FLOWS (What Connects To What)

### FLOW 1: Platform Activity → Campaign Intelligence

**Current:** Campaign API reads Supabase for citizen count + treasury.
**Ultimate:** EVERY meaningful platform event feeds the campaign brain.

| Platform Event | → Campaign Action |
|---|---|
| New citizen signs up | → CRM auto-creates contact (if they opt in) |
| Proposal created | → Analyst agent summarizes for morning brief |
| Proposal passes | → Content Producer drafts announcement |
| $MLY transaction milestone | → Storyteller crafts "economy is alive" content |
| New resource added by community | → Community Liaison notes neighborhood activity |
| Forum post about city issue | → Scout flags for research queue |
| Learning module completed | → Platform metrics update in Campaign OS |
| Governance vote reaches quorum | → Commander notified for strategy consideration |

**Implementation:**
- Supabase webhooks (database triggers) → POST to Campaign API `/intake/platform`
- Campaign API processes event type → routes to appropriate agent channel in Mattermost
- Agent responds automatically (generates content, updates research, or just logs)

### FLOW 2: Campaign Research → Public Accountability

**Current:** Research lives in knowledge base files. Not public.
**Ultimate:** Verified research publishes to a public accountability dashboard.

| Research Finding | → Public Output |
|---|---|
| Budget fact verified by Fact Checker | → Posted to /illuminate on mayor site |
| Opponent contradiction found | → Stored for debate prep + published if appropriate |
| JSO data verified | → Public safety section of /illuminate |
| Infrastructure promise tracked | → Promise tracker on /illuminate |
| Federal money audit | → "Where did the money go?" public dashboard |

**Implementation:**
- Fact Checker stamps claim as VERIFIED
- Content Producer formats for public consumption
- Campaign API stores in `verified_claims` table
- Mayor site `/illuminate` page pulls from Campaign API `/research/verified`
- Public can browse all verified claims with source citations

### FLOW 3: Campaign Content → Multi-Platform Publishing

**Current:** Manual — write in Ghost, copy to Postiz, send via Listmonk.
**Ultimate:** One-click publish cascade from Campaign OS.

```
Content Editor (Campaign OS)
    │
    ├── Fact Checker approves ✓
    │
    ├── "Publish" clicked
    │
    ├───→ Ghost API (blog post)
    ├───→ Postiz API (scheduled social posts — Twitter, Facebook, LinkedIn)
    ├───→ Listmonk API (newsletter to subscribers)
    ├───→ Mastodon API (federated social)
    ├───→ Mayor site blog page (auto-pulls from Ghost RSS)
    └───→ Platform /news or /forum (cross-post notification)
```

**Implementation:**
- Campaign API `/publish/cascade` endpoint
- Accepts: title, body, platforms[] (ghost, social, email, mastodon, platform)
- Calls each service API in parallel
- Logs results to content_published table
- n8n workflow handles the cascade automation

### FLOW 4: Petition Progress → Everywhere

**Current:** Petition count shows on mayor site only.
**Ultimate:** Real-time petition progress visible on ALL surfaces.

| Surface | How It Shows |
|---|---|
| Mayor site (index.html) | Live counter + progress bar (already done) |
| Campaign OS (Home) | Velocity card + scoreboard (already done) |
| MiLyfe Platform (/voter-journey) | "Help us get on the ballot" banner with count |
| 3D Office | Visual indicator — more agents working as count grows |
| Email footer | "X/1000 signatures collected — help us qualify" |
| Ghost blog sidebar | Running petition widget |

**Implementation:**
- All surfaces poll Campaign API `/petition/status`
- Platform adds a banner component that calls the campaign-api tunnel URL
- Email templates include dynamic petition count via Listmonk merge tags
- Ghost theme includes API call to petition status

### FLOW 5: Citizens → Campaign Pipeline

**Current:** Platform citizens and campaign contacts are separate databases.
**Ultimate:** Platform citizens who opt in become campaign supporters with zero friction.

| Citizen Action | → Campaign Pipeline |
|---|---|
| Signs up on milyfe.fun | → Option: "Support the campaign?" → adds to CRM |
| Uses /voter-journey | → Tracks voter registration status in campaign |
| Governance vote on campaign-related proposal | → Logged as engagement signal |
| Shares platform to social media | → Tracked as organic amplification |
| Completes "Know Your Rights" course | → Tagged as civically engaged |

**Implementation:**
- MiLyfe platform adds optional "Support the Campaign" toggle in settings
- If opted in: platform sends events to Campaign API `/intake/platform`
- Campaign API creates contact with tags: `platform-citizen`, `opted-in`
- Ground Game agent prioritizes these contacts for petition collection
- PRIVACY: opt-in only, revocable, transparent about what's shared

### FLOW 6: Agent Intelligence → Platform Content

**Current:** Agents research → findings sit in knowledge base.
**Ultimate:** Agent research enriches the PLATFORM directly.

| Agent Output | → Platform Enhancement |
|---|---|
| Researcher finds new Jacksonville resource | → Seeds into platform resources DB |
| Analyst generates budget breakdown | → Wiki page on platform auto-updated |
| Justice Tracker documents new JSO incident | → Safety module knows about it |
| Community Liaison logs neighborhood event | → Platform events calendar |
| Fact Checker verifies a claim | → Platform wiki gets cited reference |

**Implementation:**
- Agents with Supabase write access (service role key) via Campaign API proxy
- Campaign API `/platform/seed` endpoint — accepts resource/wiki/event data
- Writes directly to Supabase tables
- Platform shows fresh content without manual intervention

### FLOW 7: Mayor Site → Platform (The Conversion)

**Current:** Mayor site links to milyfe.fun generically.
**Ultimate:** Every mayor site interaction has a path INTO the platform.

| Mayor Site Page | → Platform Conversion |
|---|---|
| Homepage CTA | → "See the platform working: milyfe.fun/home" |
| Platform page (5 pillars) | → Each pillar links to the corresponding platform feature |
| Get Involved | → "Join MiLyfe to earn $MLY and help govern: milyfe.fun" |
| Blog post about budget | → "See the full budget analysis on the platform: milyfe.fun/wiki/city-budget" |
| Petition form (after signing) | → "Now join the community: milyfe.fun" |
| /illuminate (accountability) | → "This data powers the platform: milyfe.fun/transparency" |

**Implementation:**
- Strategic CTAs on every mayor site page that link to specific platform routes
- After petition signature: redirect to milyfe.fun/onboarding with campaign context
- Ghost blog posts include embed links to relevant platform wiki/governance pages

### FLOW 8: 3D Office → Real Operations

**Current:** 3D office is visual only — shows agents but can't trigger work.
**Ultimate:** 3D office is an OPERATIONAL interface.

| 3D Action | → Real Effect |
|---|---|
| Click agent → assign task | → Posts to that agent's Mattermost channel |
| Agent completes task at desk | → Event appears in Campaign OS feed |
| Agent goes to "meeting room" | → Multiple agents collaborating (chain invoke) |
| Agent at "publishing desk" | → Content getting pushed to Ghost/social |
| New desk appears | → New agent was loaded |
| Agent goes red/error | → Real failure in the agent system |
| Agent celebrates (confetti) | → Milestone hit (petition threshold, research verified) |

**Implementation:**
- 3D office already has task assignment via chat
- Add: Mattermost webhook that triggers 3D events (new post → agent goes to desk)
- Add: Milestone detection in Campaign API → push celebration event to 3D
- Add: Error detection → push error state to 3D

### FLOW 9: The Feedback Loop (Platform → Intelligence → Content → Platform)

The ultimate integration is a **self-reinforcing cycle**:

```
1. Platform citizens use the system
   ↓
2. Their activity generates data (proposals, votes, resource usage)
   ↓
3. HTC agents analyze that data (Analyst, Researcher)
   ↓
4. Verified findings become content (Content Producer, Speechwriter)
   ↓
5. Content publishes to mayor site + social (Ghost, Postiz, Listmonk)
   ↓
6. New people discover the campaign from the content
   ↓
7. They visit mayor site → sign petition → join platform
   ↓
8. Platform grows → more data → more intelligence → more content
   ↓
   CYCLE REPEATS
```

This is the **compounding effect**. Every new citizen makes the platform more valuable. Every piece of research makes the content more credible. Every piece of content brings more citizens. The three systems ACCELERATE each other.

---

## THE UNIFIED API LAYER

All three systems communicate through the Campaign API. It becomes the nervous system:

### Endpoints by System

**For Mayor Site (public):**
```
GET  /petition/status          → live petition count
POST /petition/add             → submit signature
POST /intake/volunteer         → volunteer signup  
GET  /research/verified        → public accountability data
GET  /platform/metrics         → citizen count, treasury
```

**For Platform (authenticated):**
```
POST /intake/platform          → platform events (new citizen, proposal, etc.)
GET  /petition/status          → show ballot access progress
GET  /research/verified        → feed into wiki/news
```

**For 3D Office (internal):**
```
POST /api/chat                 → talk to agents
POST /api/chat/stream          → streaming agent responses
GET  /api/events               → agent activity feed
POST /api/events               → push new events
GET  /api/health               → system status
```

**For Campaign OS (internal):**
```
GET  /metrics/scoreboard       → everything at a glance
GET  /crm/contacts             → contact management
GET  /compliance/status        → filing deadlines
GET  /volunteers/stats         → volunteer metrics
POST /publish/cascade          → multi-platform publish (NEW)
POST /platform/seed            → write to platform DB (NEW)
GET  /research/contradictions  → contradiction register (NEW)
```

---

## THE /ILLUMINATE PAGE (The Weapon)

This is the public-facing intelligence output. A page on mijaxx.fun where any citizen can:

1. **Type their ZIP code** → see their neighborhood's actual data
   - JSO response times in their area
   - Infrastructure investment (or lack thereof)
   - Active proposals affecting them
   - Nearest community resources

2. **Browse the budget** → plain-language breakdown
   - Where every dollar goes
   - Year-over-year comparisons
   - Department by department
   - All data from verified research

3. **See the promise tracker** → what was promised vs. delivered
   - Better Jacksonville Plan status
   - Campaign promises by all candidates
   - Infrastructure project timelines

4. **View the donor-contract map** → who gives, who gets
   - Campaign finance records (public)
   - City contract awards (public)
   - Cross-referenced relationships

**Data source:** Campaign API `/research/verified` + `/intel/public`
**Powered by:** The research pipeline running 24/7 in the Time Chamber

This page is the campaign's most powerful weapon because:
- It demonstrates transparency BEFORE taking office
- It shows the governance model working (data-driven accountability)
- It's built from verified research (Fact Checker approved)
- It makes opponents explain why THEY don't have one
- It drives media coverage ("candidate builds accountability dashboard before winning")

---

## THE SHARED IDENTITY SYSTEM

All three systems share visual identity but serve different purposes:

| Element | Mayor Site | Platform | Campaign OS |
|---------|-----------|----------|-------------|
| Logo | MiLyfe mayor wordmark | MiLyfe platform mark | HTC mark |
| Colors | Harbor blue + teal | Same | Dark theme (war room) |
| Font | Atkinson Hyperlegible | Same | Same |
| Tone | Campaign (we, proof) | Community (your, together) | Operational (direct, concise) |
| Audience | Public voters | Citizens/members | Operator (you) |
| Purpose | Convince | Demonstrate | Execute |

The public never sees the Campaign OS or 3D office. They see:
- The mayor site (the campaign's public face)
- The platform (the proof in action)
- The /illuminate page (the accountability output)

---

## IMPLEMENTATION PRIORITY

### Phase 1: Wire the Basics (This Week)
1. Platform → Campaign API: Supabase webhook on new citizen signup
2. Mayor site /illuminate: skeleton page that pulls from `/research/verified`
3. Petition count on platform: banner component calling petition status
4. Content cascade: n8n workflow (Ghost + Postiz + Listmonk in one trigger)

### Phase 2: Intelligence Flows (Next Week)
5. Agent → Platform: Seed new resources/wiki from research
6. Platform → Morning Brief: Include platform activity in daily brief
7. 3D Office milestone events: celebrate petition thresholds
8. Mayor site blog: auto-pull from Ghost RSS

### Phase 3: The Feedback Loop (This Month)
9. Platform opt-in: "Support the campaign" toggle → CRM
10. /illuminate full build: ZIP code lookup, budget browser, promise tracker
11. Content Editor → multi-platform cascade (one-click publish)
12. Agent research → auto-seed platform wiki

### Phase 4: The Weapon (Before Qualifying)
13. Donor-contract map on /illuminate (from research)
14. Neighborhood profiles on /illuminate (from census + city data)
15. Media coverage tracker (public view of what's being said)
16. Platform governance informing campaign strategy

---

## THE PRINCIPLE

**The Time Chamber THINKS.** It researches, analyzes, verifies, and produces.

**The Mayor Site SPEAKS.** It publishes findings, collects supporters, and recruits.

**The Platform PROVES.** It demonstrates that the model works, right now, for real people.

All three feed each other. The more the platform is used, the more the research has to work with. The more the research produces, the more the campaign can publish. The more the campaign publishes, the more people join the platform. The cycle compounds.

No other candidate has this architecture. They have a website and a checking account. You have a living system that gets smarter and more credible every day it runs.

---

*Three systems. One nervous system. The brain thinks. The mouth speaks. The body proves. Jacksonville goes first.*
