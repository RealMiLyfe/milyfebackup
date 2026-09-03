# MiLyfe — BUILD ROADMAP

**The execution plan. Phase by phase. What gets built, in what order, and why.**

---

## HOW TO READ THIS

Each phase has:
- **Goal** — what's true when this phase is done
- **Depends on** — what must be complete first
- **Delivers** — tangible outputs
- **Done when** — acceptance criteria

Phases are sequential where noted. Some sub-tasks within a phase run in parallel.

---

# PHASE 1: SCAFFOLD

**Goal:** Next.js app runs locally and on Vercel. Design system tokens loaded. Services ported. One page renders with real styling.

**Depends on:** Nothing. This is day one.

**Delivers:**
- [ ] Next.js 14 (App Router) initialized with TypeScript strict
- [ ] Turborepo monorepo: `apps/web/`, `packages/services/`, `packages/types/`, `packages/ui/`
- [ ] Tailwind CSS 4 + shadcn/ui + Radix configured
- [ ] Design tokens loaded: colors (`#071E40`, `#0B668C`, `#087F73`, `#078B5B`), typography (Atkinson Hyperlegible + Noto), 4-point spacing scale
- [ ] Framer Motion installed and verified
- [ ] Zustand store scaffolded (auth, layout, pocket, notifications)
- [ ] All 43 TypeScript services copied to `packages/services/`, imports adapted (no AsyncStorage)
- [ ] All type definitions in `packages/types/`
- [ ] All test suites ported to `__tests__/` with Vitest
- [ ] `tsc` compiles with zero errors
- [ ] Tests pass
- [ ] Deployed to Vercel — live URL returns a styled page
- [ ] Supabase project created (free tier)
- [ ] Supabase client configured in the app
- [ ] `.env.example` with all required variables documented
- [ ] ESLint + Prettier configured
- [ ] Git repo initialized (local, not pushed until you say)

**Done when:** `pnpm dev` shows a styled page locally AND the Vercel URL loads the same page. Tests pass in CI.

---

# PHASE 2: DATABASE + AUTH

**Goal:** A person can sign up, authenticate, and have a persistent profile stored in Supabase. Data survives a reload.

**Depends on:** Phase 1 complete.

**Delivers:**
- [ ] Supabase schema created:
  - `profiles` (id, name, avatar, languages, place, accessibility, created_at)
  - `devices` (id, user_id, name, last_active, is_shared)
  - `settings` (user_id, layout, theme, notifications, privacy)
- [ ] Row Level Security enabled on all tables
- [ ] Supabase Auth configured: passkeys (WebAuthn) + magic links
- [ ] 7-step onboarding flow built (per UI/UX Blueprint §6.3):
  1. Language and access
  2. Name and face
  3. Home place
  4. Device type (private/shared/child)
  5. Recovery (simplified — friends or paper words)
  6. Privacy starting point ("Quiet start" default)
  7. Truth and control (three check statements)
- [ ] Profile persists to Supabase after onboarding
- [ ] Session management (login, logout, device sessions)
- [ ] Shared-device awareness (badge, neutral notifications)
- [ ] Welcome screen: wordmark, tagline, "Get started" / "Look around first"
- [ ] Visitor mode: public learning, street resources, emergency info visible without signup

**Done when:** A real person can sign up on the live URL, close the browser, reopen it, and their profile persists. A visitor can browse without signing up.

---

# PHASE 3: THE HEARTBEAT

**Goal:** The app feels alive. Something is moving, something you can do, real data flowing.

**Depends on:** Phase 2 complete.

**Delivers:**
- [ ] **Live Activity Feed** — Supabase Realtime → Zustand → animated list (Framer Motion enter/exit)
  - Anonymized community events
  - Filterable: All / Street / Pocket / Voice / People
  - Relative timestamps, tap to interact
- [ ] **Customizable Home** — drag-drop widgets (@dnd-kit/sortable)
  - Widget catalog: Balance, Feed, Quests, Nearby, Messages, Journey, Standing, Pulse, Calendar, Quick Actions
  - Intelligent defaults by profile situation
  - Layout persists to Supabase
- [ ] **Live Counters** — materialized views + WebSocket
  - Members active / $MLY circulating / quests today / surplus posted
  - Animated number transitions (spring)
  - Visible on guest landing
- [ ] **Particle Field** — HTML5 Canvas ambient background
  - Activity-responsive density
  - Pulse state color shifts
  - prefers-reduced-motion fallback
- [ ] **Celebrations** — Framer Motion + Canvas confetti
  - Credits arrive → green pulse
  - Quest complete → confetti (3s)
  - Milestone → special animation
  - Auto-dismiss, never blocks interaction
- [ ] **Connection Chip** — persistent status (Online / Neighbor net / Sending later / Offline)
- [ ] **Dark Mode** — independently designed (not inverted), particles glow, cards have depth

**Done when:** Opening the app shows visible motion, live data, and a personalized home layout. The particle field breathes. Counters tick.

---

# PHASE 4: POCKET (Real $MLY)

**Goal:** $MLY Credits work. Earn, send, receive, save. Persistent. Real from day one.

**Depends on:** Phase 2 (auth + profiles).

**Delivers:**
- [ ] Supabase schema:
  - `transactions` (id, from_id, to_id, amount, memo, status, created_at)
  - `jars` (id, owner_id, name, purpose, target_amount, balance, members, approval_threshold)
  - `ubi_schedule` (user_id, last_delivered, amount, frequency)
- [ ] **Pocket overview** — animated balance, three pots (Weekly / Thanks / Place)
- [ ] **UBI delivery** — Edge Function on schedule (weekly credits to verified members)
- [ ] **Thank someone** — select person → amount → memo → confirm → "Arrived" or "Still walking"
- [ ] **Shared jars** — create, contribute, approval flow (N-of-M must agree)
- [ ] **Transaction history** — real-time, sentence-based ("You thanked Mara 12 for the kids")
- [ ] **Receipts** — every action generates human-readable receipt (MiReceipt pattern)
- [ ] **Freeze pocket** — one-tap from safety context
- [ ] **No-deprivation guard** — can't go negative
- [ ] **Walking animation** — credits in transit visualized
- [ ] **Balance does NOT look like an investment chart** — no gain/loss graph, no APY

**Done when:** A person receives weekly credits, thanks another person, sees the receipt, and the balance persists across sessions. Jars require approval before spending.

---

# PHASE 5: STREET (Marketplace + Quests + Resources)

**Goal:** People can DO something. Post, claim, verify, help. The neighborhood is alive.

**Depends on:** Phase 3 (live feed) + Phase 4 (pocket for rewards).

**Delivers:**
- [ ] **Marketplace** — 7 categories (Food / Services / Rides / Goods / Education / Housing / Jobs)
  - 10-second post flow: Category → Title → Price ($MLY/free/trade) → Photo → Post
  - Claim flow → Messages → Exchange → Both confirm → Standing
  - Real-time feed, "Near me" sorting, expiry dates
- [ ] **Quests** — real community tasks
  - Types: Cleanup, Verify, Care, Teach, Support, Civic, Build, Safety
  - Pipeline: Claim → Do → Verify (photo/confirmation) → Reward ($MLY + Standing)
  - Daily caps (anti-farming)
  - Geolocation optional
- [ ] **Resources** — shelters, food, legal aid, clinics
  - MiSource freshness dates ("Last verified: Aug 12, 2026")
  - Report incorrect information
  - Stale behavior: "Not recently verified — call to confirm"
- [ ] **Rides** — post destination + time + seats → claim → coordinate → confirm
- [ ] **Care Exchange** — time banking (hours, not $MLY)
  - Post offer/need → match → exchange → confirm → Standing
- [ ] **Surplus** — shops post food/goods that will spoil → neighbors see → claim
- [ ] **Quick Post** — floating action button, 10-second posting from any screen
- [ ] **Shop profiles** — pin on street, hours, accessibility, $MLY/cash/card, surplus, hire board, complaint button (7-day response or standing drops)

**Done when:** A person can post surplus food, another person claims it, both confirm, Standing grows for both. A quest can be claimed, completed with a photo, and $MLY rewards are issued.

---

# PHASE 6: LEARN

**Goal:** Education paths work. Lessons playable. Offline packs downloadable. Progress persists.

**Depends on:** Phase 2 (auth + persistence).

**Delivers:**
- [ ] Supabase schema: `learning_progress`, `lessons`, `badges`, `classes`
- [ ] **Journey visualization** — SVG landscape path, milestones as landmarks, scrolls with progress
- [ ] **10 learning paths** with real content:
  1. Rights and papers (Florida-specific)
  2. Parenting
  3. Reentry
  4. Peace
  5. Food and first aid
  6. Repair
  7. Money (not a casino)
  8. Read/write/numbers/languages
  9. The trade this place said it lacks
  10. How to run a street
- [ ] **Lesson player** — text, audio, transcript, images, interactive exercises, quizzes
- [ ] **Offline packs** — downloadable via Service Worker, playable offline
- [ ] **Progress persistence** — resume where you left off across devices
- [ ] **Open Badges** — verifiable credentials that leave with you
- [ ] **Class hosting** — create and run a class, manage enrollment, track attendance (private to host)
- [ ] **Kids learning** — play, safety, literacy (Canvas games, interactive stories, sandbox)

**Done when:** A person can start a learning path, complete lessons with interactive exercises, download for offline, resume on another device, and earn a verifiable badge.

---

# PHASE 7: VOICE (Governance)

**Goal:** A group of people can propose, deliberate, vote, and implement — with real delegation and constitutional constraints.

**Depends on:** Phase 4 (pocket for treasury), Phase 2 (auth for identity).

**Delivers:**
- [ ] Supabase schema: `proposals`, `votes`, `delegations`, `circles`, `circle_members`, `circle_treasuries`
- [ ] **Proposal lifecycle** — Idea → Talk → Try it first (simulation) → Decide → What happened
  - AI-assisted drafting with constitutional compliance screening
  - Version history
  - Sunset dates (every rule dies unless renewed)
  - Arweave archival of final votes
- [ ] **Voting** — private ballot (commit-reveal minimum), one citizen one vote
  - 15% quorum rule with 48-hour extension
  - 67% supermajority for compact changes
  - Constitutional kernel blocks votes that touch unamendable items
- [ ] **Delegation** — topic-specific, time-limited, instantly revocable, 3-hop max
  - Cycle detection, no re-delegation
  - Concentration warnings (aggregate, not who-to-who)
- [ ] **Circles** — Geographic / Thematic / Special
  - 500-member cap, 90-day rotating Steward (sortition at Standing >= 50)
  - Micro-treasuries in $MLY
  - Live deliberation rooms
- [ ] **The Living Compact** — tap any rule → see history, vote that made it, how to change
- [ ] **Quorum progress bars** — visual participation tracking
- [ ] **Constitutional screening badges** on every proposal

**Done when:** 10 people can create a proposal, deliberate, vote privately, reach quorum, pass or fail it, and see the result archived. Delegation works. Constitutional screening blocks invalid proposals.

---

# PHASE 8: SAFETY & DEFENSE

**Goal:** A DV survivor, child, or person in danger can use this for real. Expert-tested.

**Depends on:** Phase 2 (auth), Phase 4 (pocket freeze).

**Delivers:**
- [ ] **Leave-Now** — one tap: freeze jars, hide location, invalidate sessions, shelter directory
- [ ] **Walking-Home Timer** — countdown visible to chosen contacts, "I arrived" to cancel, auto-alert on expiry
- [ ] **Rights Card** — jurisdiction-aware (US/FL), printable PDF, offline-available
- [ ] **Witness Mode** — one-tap recording, timestamped, encrypted, 72-hour delete lock
- [ ] **Legal Resources** — real Jacksonville orgs (JALA, Hubbard House), verified, with freshness dates
- [ ] **Court Paper Flow** — photo/type the paper → Rue identifies type + deadline → calendar + legal aid links
- [ ] **Mental Health Crisis** — direct 988 link with context
- [ ] **Defense Circles** — 5-12 neighbors (rides, childcare, witness, food), skill lists, training
- [ ] **Quick Exit** — neutral page, honest about browser limits
- [ ] **Shared Device Safety** — per-person vault, kiosk timeout, neutral notifications, panic freeze
- [ ] **Youth Mode** — navigation changes (Learn / Nearby / Ask a grown-up / Me), no adult contact, no public location, safety always accessible

**Done when:** The leave-now flow actually freezes everything in under 3 seconds. Walking-home timer notifies real contacts. Rights card renders offline. A DV expert reviews and approves the flow.

---

# PHASE 9: MESSAGES + MI HELPER

**Goal:** People can message each other. Mi shows up contextually and helps.

**Depends on:** Phase 2 (auth), Phase 3 (real-time infrastructure).

**Delivers:**
- [ ] **Real-time messaging** — Supabase Realtime (migrate to Matrix when federation needed)
  - Thread states: walking / sent / delivered / read
  - Typing indicators, delivery receipts
  - Youth protection (no unknown adult contact)
  - Cross-surface blocking
  - Offline: "Still walking" with honest explanation
- [ ] **Inbox** — three tabs: Needs you / Messages / Updates
  - No engagement manipulation
  - Neutral lock-screen previews
- [ ] **Mi Helper** — ambient, contextual, not a chatbot panel
  - Ollama connection (CPU models: llama3.2:3b or Qwen 1.5B)
  - Cloud fallback (OpenRouter) when local unavailable
  - 25 named personalities (Sam, Nia, Rue, Bea, Pax, etc.)
  - System prompt per helper (personality, skills, tools, escalation)
  - Rails enforced: labeled, no money alone, no child/health/legal without human, instant stop
  - "I need a person" always available
  - Sources visible, confidence shown, "I don't know" when uncertain
  - Context-aware: notices deadlines, nearby food, patterns
  - DOES things: drafts quests, posts marketplace, finds rides, looks up resources
- [ ] **Search** — scoped (Mine → People → Place → Public), no people-finder for children/survivors, offline results, voice input

**Done when:** Two people can message, see delivery states, and Mi can answer a question with a cited source and offer to draft a marketplace post.

---

# PHASE 10: IDENTITY COMPLETE

**Goal:** Full identity lifecycle — personhood, recovery, household, standing, export, leave.

**Depends on:** Phase 2 (basic auth), Phase 4 (pocket), Phase 7 (voice eligibility).

**Delivers:**
- [ ] **Personhood verification** — 3 paths (3 member intros / hello-day stamp / optional gov ID)
  - Status: Not started → Waiting → Appointment → Under review → Complete → Appealed
  - Appeal path for denial
- [ ] **Recovery** — 2-of-3 friend recovery, keeper+delay route, paper words
  - Request timeline: request → notify → delay → approvals → review → complete
  - Abusive recovery person protection
  - Zero-friends fallback: keeper + longer delay
- [ ] **Household** — consented coordination layer (not owned by a "head")
  - Members, children (hidden), shared jar, calendar, devices, invitations, separation
  - Abuse-safe split (hide, freeze, no auto-transfer)
- [ ] **Standing** — 8 facets (neighbor/carer/maker/teacher/keeper/voice/shop/helper)
  - Visual growth (orbs/garden/rings)
  - Decay over inactivity (Fibonacci half-life)
  - Scars with expiry and response
  - Portability rules (craft/care travels, local standing cools)
- [ ] **Animated Citizen Card** — gradient shift, standing orbs pulse, QR flip for receiving $MLY
- [ ] **Privacy Center** — who can find me, what my street sees, location, story, helpers, children, devices, data kept
- [ ] **Export** — full data in JSON + readable HTML, works during disputes
- [ ] **Leave MiLyfe** — export everything, explain what stays (public records), close profile, rejoin flow

**Done when:** A person goes through personhood, sets up recovery friends, creates a household, sees their standing grow visually, exports their data, and can leave cleanly.

---

# PHASE 11: FEDERATION & SCALE

**Goal:** Governance ladders up from circles to city to globe. Multiple places can interoperate.

**Depends on:** Phase 7 (governance working locally).

**Delivers:**
- [ ] **Federation elevation** — Circles (7-13) → City Councils (49-91) → Nation Assembly → Globe Summit
- [ ] **Multi-scale attendance** — Standing rewards by scale (10/20/30/50)
- [ ] **MiTreaty** — inter-circle diplomatic accords with mutual defense
- [ ] **MiCommons** — community asset registry (solar, tools, gardens)
- [ ] **MiPulse** — street weather (dark radios, missed check-ins, empty pantry)
- [ ] **MiStory** — three books (street/people/commons), auto-narrated from community activity
- [ ] **Season Method** — MiNeed listens → weather published → one-page plan → tickets → build → review
- [ ] **MiNation adapters** — X-Road, MOSIP interop (client adapters, not a nation)
- [ ] **MiGlobe** — planetary emergency mutual aid (MiPulse alerts, zero-fee donations, ZK attestation)
- [ ] **Place transitions** — visit/spend time/move, show effects before confirming, standing cools

**Done when:** A proposal that affects multiple circles escalates to city level. Two places can federate and still message. A planetary mutual aid pulse can be triggered and donated to.

---

# PHASE 12: CONTENT CREATION (MiStory Studios)

**Goal:** People can create and share media — text, audio, photo, video, live — in multiple languages.

**Depends on:** Phase 3 (real-time feed), Phase 5 (marketplace posting).

**Delivers:**
- [ ] **Create button** on every screen (10-second posting)
- [ ] **Post types:** text+photo, audio message (Web Audio), photo story, long-form write (Markdown)
- [ ] **Community radio** — AzuraCast automation
- [ ] **Podcast hosting** — Castopod integration
- [ ] **AI Voice/TTS** — Piper (offline) for content narration
- [ ] **Multi-language auto-publishing** — LibreTranslate/Argos for 20+ languages
- [ ] **Content pipeline** — Ideation → Scripting → Production → Post-Production → Publishing
- [ ] **Autonomous content loop** — SENSE → THINK → CREATE → PUBLISH → LEARN (for community storytelling)
- [ ] **Source protection** — journalism with source boxes, no forced disclosure (Pia helper)
- [ ] **Community moderation** — proportional, transparent, appeal path

**Done when:** A person can record an audio message, post it to the street, have it auto-translated to Spanish, and it shows up in the live feed with a source label.

---

# PHASE 13: ADVANCED SYSTEMS

**Goal:** Word-to-Math, on-device AI, eco-bounties, Vanguard Protocol operational.

**Depends on:** Phase 4 (pocket), Phase 5 (quests), Phase 9 (Mi helper).

**Delivers:**
- [ ] **Word-to-Math** — natural language → Formula AST → constitutional check → signature → execute
  - Formula types: ALLOCATE, TRANSFER, SAVE, PROPOSE, MANDATE
  - No-deprivation guard, no auto-execution
- [ ] **SLM Pipeline** — on-device AI via llama.cpp WASM
  - Ring routing: device (<500ms) → mesh → cloud (consent required)
  - Personal LoRA on device from interactions
  - Mi works fully offline
- [ ] **Eco-Bounties** — YOLOv8 hazard detection + LLaVA cleanup verification
  - Spot → AI prices bounty → Sweep → AI verifies → $MLY released
  - ChirpStack IoT sensors for smart waste bins
- [ ] **Vanguard Protocol** — Coordinape guilds, $MLY protection bounties, digital truces with escrow, peace bonus
- [ ] **Sovereign Safety** — traffic stop protocol (IPFS anchoring), emergency streaming (Jitsi), Ushahidi crisis mapping
- [ ] **Hybrid Node** — Tauri desktop app, Iroh storage vault, Althea bandwidth relay

**Done when:** A formula "Allocate 150 $MLY for community garden" parses, screens constitutionally, requires a signature, and executes on the ledger. Mi answers a question offline. An eco-bounty pays out after LLaVA verifies a cleanup photo.

---

# PHASE 14: OFFLINE & MESH

**Goal:** Core features work when the internet is gone. For 48 hours minimum.

**Depends on:** Phase 4 (pocket), Phase 6 (learn), Phase 8 (safety).

**Delivers:**
- [ ] **PWA** — installable, offline page, background sync, push notifications
- [ ] **Local-first data** — Automerge CRDT for pocket, SQLite for structured storage
- [ ] **Offline conflict resolution** — per MiWalk rules (money=reservation, ballots=hold, roles=human-review)
  - "Two saved actions used the same available credits. Nothing else will move until this is reviewed."
- [ ] **Offline lessons** — downloadable packs, playable without connection
- [ ] **Offline resources** — cached shelters, food, legal aid
- [ ] **Offline ballots** — hold until deadline, submit on reconnection, timestamped proof of intent
- [ ] **Service Worker** — intelligent caching, queued actions indicator
- [ ] **BLE/WiFi-Direct** — peer discovery for mesh (when Web Bluetooth available)
- [ ] **Connection chip** — always visible, tappable for queue status

**Done when:** A person can thank someone, vote on a proposal, and continue a lesson — all while airplane mode is on. When connection returns, everything syncs correctly with conflict resolution.

---

# PHASE 15: INFRASTRUCTURE INDEPENDENCE

**Goal:** Community owns its infrastructure. No corporate dependency. Self-hostable.

**Depends on:** All prior phases stable.

**Delivers:**
- [ ] **Self-hosted Supabase** documentation + migration scripts
- [ ] **MiGit (Forgejo)** — community code ownership, MiCompat OSI gate
- [ ] **K3s deployment** — OpenTofu managed, container orchestration
- [ ] **Media infrastructure** — PeerTube, AzuraCast, Navidrome, Jellyfin, Ghost, WriteFreely (all Dockerized)
- [ ] **Social infrastructure** — Matrix Synapse (federated messaging + E2EE), Jitsi (video)
- [ ] **Governance infrastructure** — Decidim (participatory democracy)
- [ ] **Commerce infrastructure** — Medusa (marketplace), TimeOverflow (time banking)
- [ ] **AI infrastructure** — Ollama, LiteLLM, AnythingLLM, Open WebUI
- [ ] **Monitoring** — OpenObserve + GlitchTip + CrowdSec
- [ ] **MiCompat CI** — every dependency checked for OSI purity, security, accessibility
- [ ] **MiPlain CI** — banned-word linting on all user-facing text

**Done when:** The entire platform can run on community-owned hardware with zero cloud dependency. A fork can be deployed by anyone with a server.

---

# SUMMARY TABLE

| Phase | Name | Weeks | Key Outcome |
|---|---|---|---|
| 1 | Scaffold | 1 | App runs locally + Vercel, services ported, tests pass |
| 2 | Database + Auth | 1-2 | Signup works, profile persists, visitor mode |
| 3 | Heartbeat | 2-3 | Live feed, widgets, particles, counters, celebrations |
| 4 | Pocket | 2-3 | $MLY works: earn, send, receive, jars, UBI delivery |
| 5 | Street | 3-4 | Marketplace, quests, resources, rides, care exchange |
| 6 | Learn | 2-3 | 10 paths, offline packs, badges, class hosting |
| 7 | Voice | 3-4 | Proposals, voting, delegation, circles, compact |
| 8 | Safety | 2-3 | Leave-now, walking-home, rights card, defense circles |
| 9 | Messages + Mi | 2-3 | Real-time chat, 25 helpers, search |
| 10 | Identity Complete | 2-3 | Personhood, recovery, household, standing, export |
| 11 | Federation | 3-4 | Multi-scale governance, treaties, globe, seasons |
| 12 | Content Creation | 2-3 | Media posting, radio, translation, content pipeline |
| 13 | Advanced Systems | 3-4 | Word-to-Math, SLM, eco-bounties, Vanguard, nodes |
| 14 | Offline & Mesh | 2-3 | PWA, CRDT sync, offline everything, conflict resolution |
| 15 | Infrastructure | 3-4 | Self-hosted, MiGit, K3s, full Docker stack, CI gates |

**Total: ~35-45 weeks from start to full infrastructure independence.**

**But usable from Phase 5.** After Phases 1-5, people can: sign up, get credits, post marketplace items, complete quests, earn $MLY, and see a living community. That's the MVP.

---

# PARALLEL TRACKS

Some phases can overlap:

```
Phase 1 ─────┐
Phase 2 ─────┤
              ├── Phase 3 + Phase 4 (parallel — both need auth)
              │
              ├── Phase 5 + Phase 6 (parallel — street + learn)
              │
              ├── Phase 7 + Phase 8 (parallel — voice + safety)
              │
              ├── Phase 9 + Phase 10 (parallel — messages + identity)
              │
              ├── Phase 11 + Phase 12 (parallel — federation + content)
              │
              └── Phase 13 + Phase 14 + Phase 15 (parallel — advanced)
```

With parallelization, realistic timeline: **~24-30 weeks to full platform.**

---

# FIRST MILESTONE: "A PERSON CAN USE THIS" (Phases 1-5)

After ~10-12 weeks:
- Sign up in 7 steps
- See a living dashboard with particles, counters, feed
- Receive weekly $MLY credits
- Thank someone with credits
- Post food surplus for neighbors to claim
- Complete a quest (verify a resource) and earn credits
- See shops on the street with hours and surplus
- Find verified local resources (shelters, food, legal aid)
- Everything persists across sessions
- Guest can browse without signing up
- Works on mobile and desktop
- Deployed and live on the internet

That's the door. Everything after makes it deeper.

---

*This is the roadmap. One phase at a time. Done well. Done optimally. Let's go.*
