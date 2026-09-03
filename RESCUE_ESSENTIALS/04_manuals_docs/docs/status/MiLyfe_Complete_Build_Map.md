# MiLyfe — COMPLETE BUILD MAP

**Date:** August 19, 2026  
**What this is:** The single combined map of everything that needs to happen — every gap, every feature, every module, every alive element — organized into executable phases. This is the roadmap from dead static TypeScript to a living, breathing platform.

**Source truth:** `MiLyfe_COMPLETE.md` wins. `MiLyfe_Interactive_Design_Spec.md` is the build blueprint. This map is the execution plan.

---

# CURRENT STATE (What We Have)

```
============================================
     BRAIN (Keep — Platform-Agnostic TypeScript)
============================================
43 services in milyfe-app/src/services/
7,624 lines of typed business logic
16 test suites, 223 assertions passing
All in-memory (no persistence across reloads)
All local-scope (no federation/elevation)
All silent (no real-time, no animations, no life)
============================================

     OLD BUILDS (Port Features From)
============================================
MiCity-master:     80+ Docker containers, full media/social/governance
Bldg-main:        Governance UI, circles, petition, trust, live counters
MiLyfe-OS-arena:  Particle field, dock nav, journey visualization
MiLyfe-Platform:  Federation APIs, globe pulse, treaties, commons, passports
============================================

     SCREENS (Dead)
============================================
54 screen routes defined (Expo Router)
0 screens with live data
0 screens with animation
0 screens with interactivity beyond tapping
============================================
```

---

# TARGET STATE (What We're Building)

```
============================================
     ALIVE PLATFORM (Next.js 14 + Supabase)
============================================
Real-time activity feeds on every screen
Customizable drag-drop home per person
25 named AI helpers (not generic "Mi")
Full marketplace (7 categories, 10-second post)
Quests (claim/do/verify/reward)
Care exchange (time banking)
Rides coordination
Media creation (post/audio/photo/live/write)
Particle field breathing in background
Celebrations on good events
Live counters ticking every 10 seconds
Animated citizen cards with standing orbs
Visual learning journeys
Kids interactive (games/sandbox/vault/stickers)
Federation: Local → City → Nation → Globe
$MLY Credits moving in real-time
Everything works offline
Everything is customizable
A grandmother can read every screen aloud
============================================
```

---

# PHASE -1: DESIGN DOCUMENTS (Before Any Code)

**Goal:** The 12 mandatory specifications that must exist as written documents before implementation begins. Code without these creates contradictions.

## -1.1 — Filled Role-Permission Matrix
- [ ] Every role × every resource: who can create/read/update/delete/approve/appeal
- [ ] 15+ roles: visitor, neighbor, member, citizen, steward, keeper, helper, guardian, youth, mediator, auditor, shop-staff, teacher, admin, provisional
- [ ] 12+ resources: profile, message, proposal, ballot, pocket, story, quest, shop, resource, lesson, case, device

## -1.2 — Canonical Object Model
- [ ] Define shared objects and lifecycle states for: Person, Place, Household, Role, Relationship, Audience, Consent, Source, Resource, Message, Action, Receipt, Case, Appeal, Lesson, Class, Shop, Item, Jar, Proposal, Ballot, Story, Pulse, Device, Export
- [ ] Each object: fields, states, transitions, audiences, retention rules

## -1.3 — Service Blueprints (Backstage Maps)
- [ ] Recovery flow (lost phone → stolen phone → zero friends → hostile home)
- [ ] Leave-now flow (trigger → freeze → hide → shelter → aftermath)
- [ ] Personhood flow (3 intros → hello-day → verification → appeal)
- [ ] Child report flow (detection → report → human review → action)
- [ ] Human handoff flow (Mi → routing → human → closure)
- [ ] Offline pocket flow (send → walk → conflict → resolve)
- [ ] Shop dispute flow (complaint → response → escalation → resolution)
- [ ] Binding proposal flow (idea → deliberation → vote → implementation → sunset)

## -1.4 — Human Operating Model
- [ ] Who verifies shelters and legal resources? (answer: volunteers with verification dates)
- [ ] Who responds to "I need a person"? (answer: trained members + professional partners)
- [ ] Who reviews child reports? (answer: mandatory reporters where law requires, plus platform safety team)
- [ ] Who funds after-hours coverage? (answer: community pot allocation)
- [ ] Who handles appeal when all local reviewers conflict? (answer: cross-place reviewer pool)
- [ ] What response times are honest? (answer: documented SLAs that aren't promises)

## -1.5 — Data Classification & Retention Table
- [ ] Every object: classification level (public / neighbors / household / private / sealed)
- [ ] Storage location, encryption requirements, replication rules
- [ ] Retention period (7 days → 7 years → permanent depending on type)
- [ ] Export format, deletion mechanics, legal-hold protocol
- [ ] Incident response per classification level

## -1.6 — Federation & Fork Compatibility Protocol
- [ ] Can two forks still message? (yes, via federation protocol)
- [ ] How does a person move? (export → import with standing cooling)
- [ ] What happens to $MLY, receipts, standing, consent? (defined per object)
- [ ] How are harmful/incompatible instances blocked? (community vote + criteria)
- [ ] Which protocol versions interoperate? (semantic versioning + compatibility matrix)

## -1.7 — Place-Level Failure Recovery
- [ ] What if local instance disappears? (federated backup, export recovery)
- [ ] What if keepers collude? (cross-place audit, emergency freeze, appeal to commons)
- [ ] What if signing keys are lost? (recovery ceremony, provisional governance)
- [ ] What if place is physically destroyed? (distributed replicas, mesh backup)

## -1.8 — Economic Abuse & Coercion Patterns
- [ ] Forced transfers (detection: unusual patterns + victim flag + freeze option)
- [ ] Household financial control (detection: single-sender pot drain + defense circle alert)
- [ ] Employer pressure to accept $MLY (warning: "Your employer cannot require this")
- [ ] Vote buying (detection: unusual delegation patterns + anonymous ballot enforcement)
- [ ] Peace-reward coercion (protection: victim controls verification, not perpetrator)
- [ ] Shop collusion (detection: standing manipulation patterns + audit)
- [ ] Predatory public doorways (protection: transparent exchange rates + community reporting)

## -1.9 — Model & Content Update Governance
- [ ] Changed helper models: review → staged rollout → rollback capability
- [ ] Changed law packs: signed OPA bundles, community notification, grace period
- [ ] Withdrawn content: reason visible, replacement suggested, offline cache expires
- [ ] Translation corrections: attribution, version, correction history
- [ ] Security updates: emergency path vs normal path, offline device reconnection sync

## -1.10 — Accessibility Ownership Model
- [ ] Stop-ship authority: designated accessibility lead (paid or volunteer)
- [ ] Disabled reviewers: compensated from community ops pot
- [ ] Fork prevention: core accessibility patterns in MiCompat gate (forks cannot weaken)
- [ ] Testing cadence: every sprint includes screen reader + keyboard + high-contrast pass

## -1.11 — Brand Architecture Registry
- [ ] Every Mi* name classified as: member-facing / role-facing / builder-facing / protocol-internal / retired-alias
- [ ] Members ONLY see: Pocket, Learn, Street, Voice, You, Mi
- [ ] All other Mi* names are internal builder vocabulary
- [ ] Registry prevents module explosion in UI

## -1.12 — Hardware & Radio Interaction Design
- [ ] Member experience for: adding a node, sharing access, repairing, retiring, transferring, disposing
- [ ] Legal requirements per jurisdiction for radio equipment
- [ ] Safety: no silent tracking, no hidden microphones, explicit consent for sensors

---

# PHASE 0: FOUNDATION (Week 1)

**Goal:** Next.js project scaffolded, Supabase connected, services ported, one page loads with live data.

## 0.1 — Project Setup
- [ ] Initialize Next.js 14 (App Router) + TypeScript
- [ ] Install: shadcn/ui, Radix, Tailwind CSS 4, Framer Motion, Zustand, Lucide React
- [ ] Configure: ESLint, Prettier, path aliases
- [ ] Set up Supabase project (free tier — DB + Auth + Realtime + Storage)
- [ ] Deploy skeleton to Vercel (live URL immediately)

## 0.2 — Port the Brain
- [ ] Copy all 43 services from `milyfe-app/src/services/` → `src/services/`
- [ ] Copy all type definitions → `src/types/`
- [ ] Copy all test suites → `__tests__/`
- [ ] Adapt imports (React Native → web-compatible)
- [ ] Replace AsyncStorage with Supabase client + localStorage fallback
- [ ] Verify: `tsc` compiles clean, tests pass

## 0.3 — Database Schema
- [ ] Create Supabase tables: profiles, transactions, proposals, quests, marketplace, messages, celebrations, attendance, standing_scores, delegations, circles, resources, learning_progress
- [ ] Enable Row Level Security on all tables
- [ ] Enable Realtime on: transactions, proposals, quests, marketplace, messages, celebrations
- [ ] Create Edge Functions for: UBI delivery, quest verification, freshness checks

## 0.4 — Auth + Identity
- [ ] Supabase Auth with passkeys (WebAuthn) + magic links
- [ ] One signup → one profile → whole life together
- [ ] Device-bound session with shared-device awareness
- [ ] Profile creation: name, photo, languages, place, accessibility needs

---

# PHASE 0.5: THE COORDINATION LAYER (Week 1-2, parallel with Phase 0)

**Goal:** Build the P0 systems that EVERY module depends on. Without these, each feature invents its own draft/approval/consent/expiry/appeal behavior and they contradict each other.

## 0.5.1 — MiAction (Common Human-Action Protocol)
- [ ] Every consequential action carries ONE envelope:
  - Actor + role
  - Place + jurisdiction
  - Intended audience
  - Purpose
  - Data sensitivity level
  - State: draft / sent / walking / arrived / failed
  - Required human approvals
  - Consent receipt
  - Source and policy version
  - Expiration date
  - Reversal rules (reversible/irreversible/time-limited)
  - Appeal route
  - Offline conflict rule
  - Human-readable explanation
- [ ] Tech: Temporal (workflow) + OPA (policy) + CloudEvents (envelope format)
- [ ] Result: every screen consistently says what happened, who sees it, how to challenge it

## 0.5.2 — MiScope (Relationship, Permission & Consent Graph)
- [ ] Purpose-bound permission graph:
  - Person-to-person and person-to-place relationships
  - Object-level audiences (who can see THIS thing)
  - Time-limited roles
  - Required second-person approvals
  - Youth assent + guardian permission
  - Emergency exceptions
  - Conflict-of-interest markers
  - Revocation and appeal
  - "What can this person see?" preview
  - Local/offline policy cache
- [ ] Tech: OpenFGA (relationship auth) + OPA (policy evaluation)
- [ ] Build: MiLyfe relationship vocabulary, youth assent, guardian limits, abuse-safe separation, visibility previews

## 0.5.3 — MiReceipt (Understandable Proof)
- [ ] One human-readable receipt format for:
  - Thanks and jar movements
  - Private-ballot participation (proof you voted, NOT how)
  - Story publication and removal
  - Consent given/withdrawn
  - Role assignment/expiry
  - Recovery request
  - Helper-to-human handoff
  - Moderation decision
  - Data access log
  - Export/leave
- [ ] Every receipt answers: What happened? Who sees it? Can it be undone? When does it expire? How do I appeal?
- [ ] Portable, printable, translatable, cryptographically verifiable
- [ ] Tech: W3C Verifiable Credentials (TrustBloc VCS) + Sigstore concepts
- [ ] NEVER put health, child, abuse, location, ballot choice, or private messages in public transparency log

## 0.5.4 — MiSource (Provenance, Freshness & Correction)
- [ ] Every resource/fact carries a provenance envelope:
  - Source and responsible maintainer
  - Place/jurisdiction
  - Verification method
  - Checked date + expiration
  - Confidence level
  - Language/translation source
  - Accessibility status
  - Correction history
  - Safe behavior when stale (e.g., "Last verified 8 months ago — call to confirm")
- [ ] Feeds: Street resources, Mi helper citations, Learn content, law packs, shop pages, emergency info
- [ ] Tech: OpenLineage vocabulary + custom MiSource service

## 0.5.5 — MiHandoff (Helper-to-Human Case Routing)
- [ ] Matches requests to available humans by:
  - Need + urgency
  - Human role/license (where required)
  - Language + accessibility needs
  - Place/jurisdiction
  - Availability (time, capacity)
  - Conflicts of interest
  - Minimum necessary context (don't expose full profile)
  - Consent to share
  - Response target time
  - Escalation path + closure
- [ ] Works WITHOUT giving Mi or any admin full profile access
- [ ] Tech: Zammad (case handling) + Temporal (workflow) + consent graph from MiScope

## 0.5.6 — MiAppeal (Due-Process Correction Engine)
- [ ] Unified case flow for ALL appeals:
  - Notice + reason (what happened, why)
  - Evidence available to each side
  - Translation/accessibility support
  - Reviewer independence (no conflicts)
  - Conflict disclosure
  - Time limits (reviewer must respond within X days)
  - Interim restrictions (proportional, not punitive)
  - Member response
  - Decision + remedy
  - Escalation path (local → cross-place → real courts always available)
  - Retention/forgetting rule
  - Export works DURING the case
- [ ] Applies to: personhood denial, moderation action, place ban, helper action, shop dispute, standing scar, money review, child-safety decision

## 0.5.7 — MiStage (Capability Readiness Gate)
- [ ] Capability manifest: what's active now vs what's pending community vote to activate
- [ ] Gate enforcement: external exchange (cash-out, peer-swap outside platform) requires community vote + legal review
- [ ] Fail-closed: if readiness is uncertain, deny (not allow)
- [ ] Activation requirements clearly defined per capability (legal review, community vote threshold, operational readiness)
- [ ] $MLY Credits are REAL from day one — the gate controls EXTERNAL CONVERTIBILITY, not the credits themselves
- [ ] Tech: OpenFeature + Flipt + signed capability metadata (TUF)

---

# PHASE 1: THE HEARTBEAT (Weeks 2-3)

**Goal:** The app feels alive the moment you open it. Something is moving. Something you can do. Real data flowing.

## 1.1 — Live Activity Feed
- [ ] Supabase Realtime subscription → Zustand store
- [ ] Animated feed items (Framer Motion enter/exit with slide)
- [ ] Content: thanks, quest completions, surplus posts, proposals, new members
- [ ] Anonymized by default (names only if opted in)
- [ ] Filterable: All / Street / Pocket / Voice / People
- [ ] Relative timestamps ("2 min ago")
- [ ] Tap to interact (thank back, claim surplus, support proposal)

## 1.2 — Customizable Home Layout
- [ ] Drag-drop widget system (@dnd-kit/sortable)
- [ ] Zustand persisted layout store
- [ ] Widget catalog:
  - Balance widget ($MLY credits with animated number)
  - Activity stream widget (live feed)
  - Quest widget (active/available)
  - Nearby widget (food, help, rides)
  - Messages widget (unread + preview)
  - Journey widget (learning progress)
  - Standing widget (visual facets)
  - Pulse widget (street weather)
  - Calendar widget (deadlines, classes, check-ins)
  - Quick actions widget (thank, post, quest)
- [ ] Intelligent defaults by situation:
  - Homeless → resources, nearby, quick actions prominent
  - Parent → kids, schedule, rides prominent
  - Reentry → deadlines, jobs, learn prominent
  - Elder → check-ins, messages, safety prominent
- [ ] Layout persists to Supabase profile

## 1.3 — Live Counters
- [ ] Supabase materialized views for aggregates
- [ ] WebSocket subscription for real-time tick
- [ ] Animated number transitions (Framer Motion spring)
- [ ] Counters: members active / $MLY circulating / quests today / resources verified / proposals active / surplus posted / rides shared
- [ ] Visible on landing page (guest can see life before signup)
- [ ] Update every 10 seconds

## 1.4 — Particle Field (Port from MiLyfe-OS)
- [ ] HTML5 Canvas ambient background
- [ ] Particles increase with community activity level
- [ ] Color shifts with Pulse state (green = good, amber = attention needed)
- [ ] Responds to mouse/touch (avoids cursor gently)
- [ ] 60fps target, 30fps fallback
- [ ] prefers-reduced-motion: static gradient instead
- [ ] Subtle — never distracts from content

## 1.5 — Celebration System
- [ ] Celebration state in Zustand
- [ ] Triggers:
  - Credits arrive → gentle green pulse on balance
  - Quest complete → confetti burst (3 seconds)
  - Proposal passes → community banner
  - Milestone reached → special animation
  - Thanks received → warm glow
- [ ] Canvas confetti (lightweight)
- [ ] Auto-dismiss after 3 seconds, never blocks interaction
- [ ] Haptic feedback (optional)

---

# PHASE 2: DO SOMETHING (Weeks 4-5)

**Goal:** Every screen has something you can DO. Not just read. Post. Claim. Thank. Vote. Verify. Help.

## 2.1 — Quests System
- [ ] Quest types:
  - Cleanup: "Pick up trash on Oak & Main" — photo verify
  - Verify: "Confirm Northside Pantry still open Tue-Fri" — check and report
  - Care: "Check on elder at 412 Pine" — they confirm you showed up
  - Teach: "Host a 30-min reading circle" — learners confirm
  - Support: "Buy from local shop with $MLY" — receipt generated
  - Civic: "Read the shade proposal and vote" — participation tracked
  - Build: "Plant something in community garden" — photo verify
  - Safety: "Walk the block at 7 PM" — presence logged (not a patrol)
- [ ] Claim → Do → Verify → Reward pipeline
- [ ] Rewards: $MLY Credits + Standing attestation
- [ ] Caps per day (can't farm)
- [ ] Geolocation optional for location-based quests
- [ ] Photo upload to Supabase Storage

## 2.2 — Full Marketplace (7 Categories)
- [ ] Categories: Food / Services / Rides / Goods / Education / Housing / Jobs
- [ ] 10-second post flow: Category → Title → Price ($MLY/free/trade) → Photo optional → Post
- [ ] Claim flow: "I want this" → Messages → Exchange → Both confirm → Standing
- [ ] Supabase table with real-time feed
- [ ] "Near me" geolocation sorting
- [ ] Expiry dates, claimed/available states
- [ ] Dual pricing ($MLY and/or cash)
- [ ] Hire board: neighbors first, then town

## 2.3 — Rides Coordination
- [ ] Post: destination + time + seats available
- [ ] Claim: "I need a seat" → coordinate in messages
- [ ] Both confirm → Standing attestation
- [ ] Time-based expiry
- [ ] Map visualization (MapLibre, optional)
- [ ] Messages integration for coordination

## 2.4 — Care Exchange (Time Banking)
- [ ] Post offer ("I can do X") or need ("I need Y")
- [ ] Unit: Hours (separate from $MLY — different kind of wealth)
- [ ] Match → Exchange → Both confirm → Standing grows
- [ ] Categories: childcare, repair, tutoring, rides, cooking, errands
- [ ] Skills matching algorithm

## 2.5 — Media Creation
- [ ] Post types:
  - Text + photo (intentional feed post)
  - Audio message (Web Audio API voice note)
  - Photo story (Camera API documentation)
  - Live stream (OwnCast/Jitsi integration — later phase)
  - Long-form write (Markdown community journalism)
- [ ] Supabase Storage for all media
- [ ] Source protection for journalism (MiPress)
- [ ] Community moderation flow

## 2.6 — Quick Post (10-Second Content)
- [ ] Floating action button on every screen
- [ ] Modal: What are you posting? (Surplus / Need / Offer / Question / Celebration)
- [ ] Minimal fields, immediate post
- [ ] Shows in live feed instantly

---

# PHASE 3: FEEL SOMETHING (Weeks 6-7)

**Goal:** Your identity is visual, alive, and YOURS. Standing grows visually. Journey has depth.

## 3.1 — Animated Citizen Card
- [ ] Photo/avatar, name, home place, member-since date
- [ ] Standing facets as glowing orbs that grow over time
- [ ] Subtle gradient shift animation
- [ ] Flip animation to show QR code (for receiving $MLY)
- [ ] SVG for facets, Canvas for standing visualization
- [ ] Card is the centerpiece of "You" section

## 3.2 — Visual Standing System
- [ ] 8 facets: neighbor / carer / maker / teacher / keeper / voice / shop / helper
- [ ] Each facet visualized as growing element (garden rings, light orbs)
- [ ] Growth animation when attestation received
- [ ] Decay visible (subtle dimming over time if inactive)
- [ ] Portability indicators (what follows you if you move)
- [ ] Scars visible with expiry countdown
- [ ] Privacy: you choose which facets to show publicly

## 3.3 — Journey Visualization
- [ ] SVG landscape/path that scrolls as you progress
- [ ] Milestones are landmarks
- [ ] Completed lessons behind you
- [ ] Next lesson ahead
- [ ] Branches visible (non-linear paths)
- [ ] Framer Motion for scroll and reveal
- [ ] Data from learning-content service

## 3.4 — Pocket Alive
- [ ] Animated $MLY balance (springs when changing)
- [ ] "Walking" animation when money is in transit
- [ ] Three-pot visualization (Weekly / Thanks / Place)
- [ ] UBI arrival celebration (Saturday delivery with green pulse)
- [ ] Transaction history with real-time updates
- [ ] Send-thanks with double-spend protection (from existing service)
- [ ] Round-up to street pot option

## 3.5 — Messages Alive
- [ ] Thread state visualization: walking / sent / delivered / read
- [ ] Typing indicators
- [ ] Delivery receipts visible
- [ ] Real-time via Supabase Realtime (migrate to Matrix when federation needed)
- [ ] Youth protection (from messaging-engine.ts)
- [ ] Cross-surface blocking (from messaging-engine.ts)

## 3.6 — Privacy Live Display
- [ ] "Right now, 0 people can see your location"
- [ ] "Only Mara and Sam can message you"
- [ ] Real-time privacy state visible
- [ ] Granular controls (opt-in only — handle, district, standing, badges, quests, balance)
- [ ] "What MiLyfe Knows About You" radical trust display
- [ ] One-tap data export (JSON)
- [ ] Deletion request flow

---

# PHASE 4: GOVERNANCE ALIVE (Weeks 8-9)

**Goal:** A small group can propose, deliberate, and decide — with real votes, real delegation, and real results. Local governance ladders up to city → nation → globe.

## 4.1 — Proposal Lifecycle (Port + Wire)
- [ ] Stages: Idea → Talk → Try it first → Decide → What happened
- [ ] AI-assisted drafting with constitutional compliance screening
- [ ] 15% quorum rule with 48-hour low-quorum extension
- [ ] 67% supermajority for charter changes
- [ ] Sunset date enforcement
- [ ] Version history on proposals
- [ ] Arweave permaweb archival

## 4.2 — Zero-Knowledge Voting
- [ ] Semaphore ZK proofs (one citizen, one vote — NOT token-weighted)
- [ ] Pseudonymous + $MLY reward for participation
- [ ] Constitutional kernel: 8 unamendable rights block any vote
- [ ] Private ballot (commit-reveal as minimum)
- [ ] Vote weight display (from standing, not from money)

## 4.3 — Delegation Engine (Extend)
- [ ] Port existing delegation-engine.ts logic
- [ ] Topic-specific, time-limited, instantly revocable
- [ ] Up to 3 hops (liquid democracy from MiLyfe-OS kernel)
- [ ] Cycle detection (from OS kernel governance.py)
- [ ] Privacy-preserving concentration warnings
- [ ] Visual delegation momentum (aggregate, not who-to-who)
- [ ] No re-delegation

## 4.4 — Circles System
- [ ] Three types: Geographic, Thematic, Special
- [ ] 500-member cap per circle
- [ ] 90-day rotating Steward elections (sortition at Standing >= 50)
- [ ] Micro-treasuries in $MLY per circle
- [ ] Live deliberation rooms
- [ ] Participatory budgeting within circles
- [ ] District linking

## 4.5 — Federation / Scale Elevation (PORT from Platform-arena)
- [ ] MiFederate: Circles (7-13) → MiCity Councils (49-91) → Globe Mesh
- [ ] `/api/federation/elevate` — council formation
- [ ] SSE broadcasts for `micity_council_formed`
- [ ] Multi-scale attendance check-in:
  - LOCAL_CIRCLE: 10 Standing
  - MICITY_COUNCIL: 20 Standing
  - MINATION_ASSEMBLY: 30 Standing
  - MIGLOBE_SUMMIT: 50 Standing

## 4.6 — Mi Nation (MiNation)
- [ ] Federation adapters to real government systems
- [ ] X-Road interop (Estonia government data exchange)
- [ ] MOSIP interop (modular open-source identity)
- [ ] Fineract adapters (financial systems)
- [ ] Helios adapters (digital voting verification)
- [ ] DHIS2 adapters (health information)
- [ ] OSM integration (geographic data)
- [ ] Constraint: "Not a nation" — client adapters only, no unauthorized passports

## 4.7 — Mi Globe (MiGlobe / MiPlanet)
- [ ] MiPulse: Planetary emergency mutual aid alerts
  - Target city + initiative + $MLY allocation
  - Zero-knowledge attestation verification
  - SSE broadcast: `miglobe_pulse_active`
- [ ] Globe donation routing: zero-fee contributions to active pulses
  - Level 3+ MiStanding required (Standing >= 50)
  - ZK attestation signatures
- [ ] Climate/ocean/SDG coordination
  - CESM (climate modeling)
  - Argo (ocean data)
  - Open SDG (sustainable development goals)
  - SatNOGS (ground stations)

## 4.8 — MiTreaty (Inter-Circle Diplomacy)
- [ ] Create diplomatic accords between circles
- [ ] Mutual defense activation
- [ ] Multiple signatory circles
- [ ] Treaty registry visible to all members

## 4.9 — MiCommons (Sovereign Infrastructure Registry)
- [ ] Register community assets (solar arrays, tool libraries, community gardens)
- [ ] Ownership tracking per asset
- [ ] Steward circle assignment
- [ ] Asset types: OFF_GRID_INFRASTRUCTURE, TOOL_LIBRARY, COMMUNITY_SPACE, etc.

## 4.10 — MiStewardship (Democratic Leadership Rotation)
- [ ] Sortition-based 13-week rotating selection
- [ ] Standing >= 50 eligibility gate
- [ ] Elder mentorship handshake (+15 Standing to both)
- [ ] Previous steward → new steward transition ceremony
- [ ] Fibonacci half-life anti-stagnation decay
- [ ] 34% treasury circuit breaker with 80% supermajority guard

## 4.11 — Petition / Voter (Port from Bldg)
- [ ] DS-DE 104 candidate petition tracker (Florida ballot access)
- [ ] District-by-district signature breakdown
- [ ] Live counters to 10,000 target
- [ ] Voter registration expansion metrics
- [ ] Two-track wizard (petition vs voter reg)

---

# PHASE 5: SAFETY & DEFENSE (Weeks 10-11)

**Goal:** A DV survivor, child, or person in danger can use this for real. DV-expert tested.

## 5.1 — Leave-Now Flow (Wire Existing Service)
- [ ] Actually freezes jars (calls pocket-ledger.freeze())
- [ ] Actually hides location (removes from all public surfaces)
- [ ] Actually removes devices (invalidates sessions via identity.ts)
- [ ] One-tap execution from any screen
- [ ] Quick-exit neutral page (clears screen, honest about browser history limits)
- [ ] Shelter directory (real Jacksonville: Hubbard House, etc.)

## 5.2 — Walking-Home Timer (Wire Existing Service)
- [ ] Real countdown visible to chosen contacts
- [ ] "I arrived" tap to cancel
- [ ] Auto-alert if timer expires without arrival
- [ ] Contacts see: "They're walking. Expected 12 min. 8 min left."
- [ ] No location sharing unless explicitly opted in

## 5.3 — Rights Card
- [ ] Jurisdiction-aware (US/FL for Jacksonville)
- [ ] Print as PDF/HTML
- [ ] Offline-available
- [ ] Real phone numbers and resources
- [ ] "You have the right to remain silent. Say: I want a lawyer."

## 5.4 — Witness Mode
- [ ] One-tap recording
- [ ] Timestamped
- [ ] Stored encrypted
- [ ] After-action writing option
- [ ] Cannot be deleted by anyone except you (and only after 72 hours)

## 5.5 — Legal Resources (Wire Existing Service)
- [ ] Real Jacksonville organizations (JALA, Three Rivers Legal, Hubbard House)
- [ ] Real addresses, phone numbers, hours
- [ ] Verification dates visible
- [ ] MiSource freshness tracking
- [ ] FOIA/public records builder
- [ ] Court paper forms (Docassemble-style)

## 5.6 — Mental Health Crisis
- [ ] Direct 988 Suicide & Crisis Lifeline link
- [ ] Context-aware: "You seem to be looking at crisis resources. Here's 988."
- [ ] Never blocks, never judges
- [ ] Rue helper personality for safety interactions

## 5.7 — Mutual Defense Circles
- [ ] 5-12 neighbors who agree to show up
- [ ] Types: rides, childcare, witness, food, translation
- [ ] NOT a militia, NOT weapons
- [ ] Common pot for bail gifts or lawyer funds (gifts, not a bond business)
- [ ] Skill list: "I can translate Spanish at the courthouse"
- [ ] Training: de-escalation, first aid, rights

## 5.8 — Shared Device Safety (MiShared)
- [ ] Per-person local vault separation
- [ ] Kiosk timeout and handoff
- [ ] Neutral notifications (no content on lock screen)
- [ ] Child/adult switching without shared secrets
- [ ] Session clearing that works
- [ ] Cached location removal
- [ ] Panic freeze from any screen

---

# PHASE 6: EVERYONE'S LIFE (Weeks 12-14)

**Goal:** Every person described in Book A §V can use this for their specific situation.

## 6.1 — Mi Kids (Full Interactive)
- [ ] Separate route with own navigation (not restricted adult mode)
- [ ] Mini-games via Canvas:
  - Counting at the market
  - Matching (memory game)
  - Reading adventures (interactive)
  - Problem-solving puzzles
- [ ] Drawing/sandbox creative space (saved to profile)
- [ ] Vault: savings jar with visual fill animation + goal-setting
- [ ] Achievements as STICKERS (visual, collectible, fun — not scores)
- [ ] Interactive stories (choose-your-own-adventure branching)
- [ ] Safety ALWAYS one tap away (even if everything else restricted)
- [ ] No money movement, no adult contact (hardcoded in MiChildGate)
- [ ] Guardian link on profile
- [ ] Kim helper personality (only kid-safe content)

## 6.2 — Mi Work (MiWork)
- [ ] Job boards (local-first: neighbors → town → broader)
- [ ] Hire board on every shop profile
- [ ] Hour logs / timesheets
- [ ] Co-op membership and contribution tracking
- [ ] Wage-law warnings (minimum wage violations flagged)
- [ ] No unpaid "contribution" coercion protection
- [ ] Scheduling / shift coordination
- [ ] Skill matching (post skills, find needs)
- [ ] Gig work coordination
- [ ] Wren helper personality for work questions
- [ ] Jo helper for job/hire matching

## 6.3 — Mi Home (MiHome — Household)
- [ ] Household dashboard: members, kids (hidden from strangers), steward
- [ ] Shared jar management
- [ ] Chores (optional — if they want them)
- [ ] Home automation stubs: lights status, leak alerts, air quality
- [ ] Home Assistant integration pathway (later: MQTT spine)
- [ ] Liv helper personality for home issues

## 6.4 — Mi Media (MiPress + Media Hub)
- [ ] Community journalism (source protection, correction paths)
- [ ] Audio messages / voice notes (Web Audio API)
- [ ] Photo stories / documentation
- [ ] Long-form writing (Markdown editor, publishable)
- [ ] Live streaming integration (OwnCast → Supabase for coordination)
- [ ] RSS/news aggregation (community curated)
- [ ] Book club features (reading groups, reviews)
- [ ] Podcast hosting/listening
- [ ] Music (community radio playlist coordination)
- [ ] Pia helper for press, Dex for media creation

## 6.5 — Education Complete (MiGrowth)
- [ ] 10 staffed learning paths:
  1. Rights and papers
  2. Parenting
  3. Reentry
  4. Peace
  5. Food and first aid
  6. Repair
  7. Money (not a casino)
  8. Read/write/numbers/languages
  9. The trade this place said it lacks
  10. How to run a street
- [ ] Real lesson content (not placeholder)
- [ ] Interactive exercises (not just text)
- [ ] Downloadable offline packs (real mechanism)
- [ ] Open Badges (verifiable credentials that leave with you)
- [ ] Class hosting/publishing system
- [ ] Teach mode (create and run a class)
- [ ] Non-linear branching paths (MiLearnPath)
- [ ] Bea helper personality for learning

## 6.6 — Elder Care (MiCare)
- [ ] Check-ins THEY set (not surveillance)
- [ ] Frequency: daily, twice-daily, weekly
- [ ] Grace period before alerting contacts
- [ ] Rides coordination
- [ ] Story-keeping (their voice, their history)
- [ ] Oli helper personality for older years

## 6.7 — Reentry Support
- [ ] Day-one pocket (first-month jar)
- [ ] Real ID help (resources for getting documents)
- [ ] Job board (immediate, local)
- [ ] Calendar with probation dates, appointments
- [ ] Weekly credits after handshake
- [ ] Offline lesson packs (downloadable before release)
- [ ] Family contact where facility allows

## 6.8 — Peace System (Port + Extend)
- [ ] Peace Table mediation (consent flow, abuse screening, victim control)
- [ ] Peace Rewards: 30/90/180 days verified peace
  - No new harm (victims + keepers verify, not rumor)
  - Weapons turned in to lawful takebacks
  - Kids in school
  - Restitution started
  - A peace job
- [ ] Exit pathways (work, art, sport, parenting)
- [ ] Pax helper personality for peace mediation

## 6.9 — Single Parents
- [ ] Kid hours coordination
- [ ] Babysit swaps (mutual aid, not marketplace)
- [ ] Rides to school/activities
- [ ] Night class compatibility
- [ ] Food coordination
- [ ] Emergency childcare network

## 6.10 — Homeless / No-Address
- [ ] Profile does NOT require an address
- [ ] "Where do you spend time?" instead of "Where do you live?"
- [ ] Library/kiosk mode
- [ ] Nearby resources prominent (shelters, food, water, charging)
- [ ] Day-one pocket on signup

---

# PHASE 6.5: MISSING LIFE MODULES (Weeks 14-15)

**Goal:** The remaining 19 life/civic modules that complete the full MiLyfe experience.

## 6.5.1 — MiStory (The Organism Tells Itself)
- [ ] Three books, nobody drafted:
  - Street book: public events (pot spent, class held, surplus, peace table) — ON by default, no faces unless opted
  - People pages: "I'm in this story" tap — OFF by default
  - Commons chronicle: rolled-up facts, no names — ON by default
- [ ] Mi narrates from the RECORD, not gossip
- [ ] Same day, four voices: you, the street, the place, the commons
- [ ] MiStoryLive: living chronicle that updates in real-time

## 6.5.2 — MiPulse (Street Weather / Block Health)
- [ ] Weather of the block — NOT a wanted board:
  - Dark radios (mesh nodes offline)
  - Missed elder check-in
  - Empty food pin (pantry low)
  - Peace window thinning (conflict indicators)
- [ ] Helpers restart radios. Humans knock on doors.
- [ ] Shown as ambient "weather" — not surveillance, not alarm
- [ ] Feeds into home dashboard widget

## 6.5.3 — MiLegacy (Death, Incapacity, Digital Succession)
- [ ] Death: steward takes over, UBI stops, pocket + stories pass, card becomes memory page (if wanted)
- [ ] Incapacity: steward + delay + two-friend confirm
- [ ] Multi-jurisdiction probate HANDOFF (not DIY probate — links to real legal process)
- [ ] Profile closure options: memory page, full deletion, archive
- [ ] Export of all data to designated steward

## 6.5.4 — MiGuard (Whistleblowing, Anonymous Reporting)
- [ ] Protected reporting channel where statutes exist
- [ ] Anonymous submission (no identity required)
- [ ] NOT a channel for threats or CSAM
- [ ] Source protection (MiPress integration)
- [ ] Routing to appropriate authority (internal or external)

## 6.5.5 — MiOrg (Organizations, Cooperatives, Entities)
- [ ] Entity creation: cooperative, community organization, working group
- [ ] Multi-member governance (internal to the org)
- [ ] Shared treasury/jar
- [ ] Member roles within org
- [ ] Entity Kit templates: Swiss Verein, US nonprofit, EU AISBL

## 6.5.6 — MiFood (Food Safety, Kitchens, Allergens, Recalls)
- [ ] Allergen tracking on all food-related marketplace posts
- [ ] Cottage-food law profiles by jurisdiction
- [ ] Recall alerts for community
- [ ] Kitchen safety information
- [ ] Val helper personality for food questions

## 6.5.7 — MiSign (Electronic Signatures)
- [ ] eIDAS / ESIGN / UETA compliant where applicable
- [ ] Verifiable signatures on agreements, contracts, treaties
- [ ] Timestamps + audit trail
- [ ] Integration with MiReceipt for proof

## 6.5.8 — MiTime (Trusted Timestamping)
- [ ] Evidence admissibility timestamps
- [ ] "Write what happened while it's fresh" — timestamped (MiDefense integration)
- [ ] Witness mode recordings timestamped
- [ ] Ballot submissions timestamped
- [ ] Offline-created timestamps verified on reconnection

## 6.5.9 — MiTax (Filing Assistance + Export)
- [ ] Year file export (all $MLY transactions in tax-friendly format)
- [ ] Reminders for filing deadlines
- [ ] NOT a tax authority — just data export + deadline awareness
- [ ] Tax helper personality for questions
- [ ] Integration with real CPA/tax aid organizations

## 6.5.10 — MiInsure (Mutual Aid with Insurance-Law Tripwires)
- [ ] Mutual aid pools (funeral funds, emergency funds)
- [ ] Tripwire detection: "This looks like insurance — STOP"
- [ ] Warning before crossing into regulated territory
- [ ] Node-operator liability awareness
- [ ] Ira helper personality: never gives insurance advice

## 6.5.11 — MiIP (Copyright, License Compatibility, Attribution)
- [ ] Content posted by members: clear licensing (CC-BY default, chooseable)
- [ ] Attribution tracking for shared/remixed content
- [ ] License compatibility checking for contributed code
- [ ] Integration with MiCompat for software dependencies

## 6.5.12 — MiTrade (Sanctions, Export Control, Customs Awareness)
- [ ] Screening where money or dual-use path exists
- [ ] Warning: "This transaction may cross jurisdictional boundaries"
- [ ] NOT enforcement — awareness and documentation
- [ ] Integration with MiLegal jurisdiction profiles

## 6.5.13 — MiLang (Language Justice — Beyond i18n)
- [ ] Full module with plain-language DUTY (not just translation)
- [ ] 10+ languages as a roadmap commitment
- [ ] RTL as a first-class layout, not a patch
- [ ] Plain-language linting (MiPlain CI integration)
- [ ] Tess helper for real-time translation assistance
- [ ] Community translator network (human, not just AI)

## 6.5.14 — MiArchive (Retention vs Right-to-Be-Forgotten)
- [ ] Retention law compliance (what MUST be kept)
- [ ] Right-to-erasure compliance (what MUST be deletable)
- [ ] Conflict resolution between the two
- [ ] Cultural memory preservation (opt-in community history)
- [ ] Scribe helper handles records/retention questions

## 6.5.15 — MiAid (Humanitarian Ops, IHL-Aware Disaster Response)
- [ ] Medical neutrality (no targeting data to armed actors)
- [ ] IHL (International Humanitarian Law) awareness
- [ ] Disaster coordination (CAP alerts + MiQoS priority)
- [ ] Emergency roles auto-sunset in 30 days
- [ ] Integration with MiEmergency cross-domain coordination

## 6.5.16 — MiBridge (Transition from Legacy Systems)
- [ ] Dual-system guides (use MiLyfe alongside existing tools)
- [ ] Data import from: email, social media, banking apps, contacts
- [ ] Gradual onramp (don't force full adoption at once)
- [ ] "You don't have to delete anything else — this works alongside"

## 6.5.17 — MiSandbox (Simulation Before Rule Changes)
- [ ] Compact changes require 75% vote + time-lock + MiSandbox simulation
- [ ] Emergency governance roles tested in sandbox before activation
- [ ] "Try it first" stage for proposals (existing governance engine stage)
- [ ] Impact preview: "If this passes, here's what changes for you"

## 6.5.18 — MiRecord (Evidence, Outcomes, Research)
- [ ] Consented data for community research
- [ ] Outcome tracking (did the proposal actually help?)
- [ ] Evidence collection for appeals and disputes
- [ ] Anonymized aggregates for community health metrics
- [ ] Opt-in only, revocable, exportable

## 6.5.19 — MiPlacePlan + Season Method
- [ ] MiNeed listens for 14 days (what's missing, what's hurting)
- [ ] MiStory publishes the weather (no names — just patterns)
- [ ] MiPlacePlan writes one-page season: "This season: Learn X, Safe Y, Share Z"
- [ ] Street keepers accept or rewrite the plan
- [ ] MiGit opens tickets ONLY for that page (nothing else)
- [ ] MiHeal applies what is safe (automated). Humans apply the rest.
- [ ] Season ends. Story says what changed. Repeat.
- [ ] Jacksonville Season 1: Learn (rights, GED, parenting) + StreetGoods (one bakery, one pantry) + Reentry pack + Pulse on one block

## 6.5.20 — Shop Profiles (First-Class Product)
- [ ] Pin on the STREET (not a global feed — local first)
- [ ] Hours, ramp/step accessibility, languages spoken
- [ ] Whether they take: $MLY / cash / card
- [ ] Today's surplus (food that will spoil → neighbors notification)
- [ ] Hire board: neighbors first, then town, then broader
- [ ] Complaint button: MUST be answered in 7 days or standing says "doesn't answer"
- [ ] Community day toggle: tools, water, shade, charging available
- [ ] Staff list with person cards
- [ ] Books: simple till, dual price, tax export
- [ ] No unauthorized crypto-register until exchange gate is voted open

## 6.5.21 — Personhood Verification
- [ ] Three paths (any one works):
  1. Introduced by 3 members in good standing (web of trust)
  2. In-person "hello-day" at library/shop/church (staff stamps)
  3. Optional government-ID check (NEVER required for basic card)
- [ ] Hello-day event coordination (schedule, invite, verify)
- [ ] Appeal path if denied
- [ ] Privacy proof-of-person option (verify without revealing identity)

## 6.5.22 — The Living Compact (Interactive Constitution)
- [ ] Tap any rule → see: when made, what vote passed it, how to change it
- [ ] Hard votes: private ballot
- [ ] Cannot be amended (the unamendable items):
  - The Oath (all 24 clauses)
  - Article 0 (sovereignty of individual)
  - Bodily autonomy
  - Childhood protections (MiChildGate)
  - Exit (freedom to leave with your data)
  - MiLegal fail-closed (default deny)
  - Kill-switch / pause is human-only
- [ ] Dispute path: L1 MiPeace AI → L2 peer panel → L3 community jury → L4 opt-in arbitration → L5 compact review → real courts always
- [ ] Bootstrap: 90-day comment, provisional stewards, SUNSET, no founder keys

## 6.5.23 — MiScenario (Rights/Failure Simulator)
- [ ] Test packs that simulate failure before it happens:
  - Abusive recovery person test
  - Child contacted by unknown adult
  - Conflicting offline money
  - Stale shelter information
  - Helper hallucinated deadline
  - Captured vote attempt
  - Supply-chain attack
  - Place-level key loss
- [ ] Run before every release (part of CI/CD)
- [ ] Cucumber + Playwright + Conftest + LitmusChaos

## 6.5.24 — MiLifecycle (Data Retention, Migration, Deletion)
- [ ] Data-purpose registry (why is this stored?)
- [ ] Retention period enforcement (auto-delete when expired)
- [ ] Legal hold mechanism (pause deletion for legal process)
- [ ] Death/stewardship coordinator (trigger MiLegacy flows)
- [ ] Schema migration system (data evolves without breaking old records)
- [ ] Export always works, even during dispute or deletion

## 6.5.25 — MiCompat (OSI Purity CI Gate)
- [ ] Every dependency checked: exact commit, package, transitive licenses
- [ ] BSL / SSPL / Commons Clause → FAIL the build
- [ ] Security advisories, telemetry detection, accessibility baseline, maintenance status
- [ ] Replacement path documented for every dependency
- [ ] Tools: ScanCode + ORT + Syft + OSV-Scanner + Grype/Trivy + Dependency-Track + Cosign

## 6.5.26 — MiPlain (Banned-Word CI Linting)
- [ ] Dictionary of banned jargon (technical terms that exclude people)
- [ ] CI lint on all user-facing text in `apps/`
- [ ] Release blocker (same as accessibility)
- [ ] Grandmother test automated: reading level > 6th grade → flag it

---

# PHASE 7: NAMED HELPERS (Weeks 15-16)

**Goal:** Mi isn't one generic bot. It's 25 named personalities who show up contextually and DO things.

## 7.1 — Helper Infrastructure
- [ ] Ollama connection (CPU-only models: llama3.2:3b or smaller)
- [ ] Cloud API fallback (OpenRouter) when local unavailable
- [ ] System prompt per helper (personality, skills, tools, escalation path)
- [ ] Rail enforcement: labeled, logged, no child/health/legal without human, no money alone
- [ ] "I'm not a person, not a lawyer, not the police" always labeled
- [ ] Instant stop word
- [ ] "Humans only" mode toggle

## 7.2 — Front-Door Helpers (Members See These)
- [ ] **Sam** — Guide (onboarding, plain speech) → escalates to human greeter
- [ ] **Nia** — Pocket (UBI, thanks, jars) → escalates to treasurer
- [ ] **Rue** — Safety/defense (rights, freeze, leave-now) → escalates to lawyer/911
- [ ] **Sol** — Health info (symptoms info, records you hold) → escalates to clinician
- [ ] **Bea** — Learn (lessons, offline classes) → escalates to teacher
- [ ] **Pax** — Peace (listen, restate, schedule circle) → escalates to mediator
- [ ] **Liv** — Home (lights, leaks, air) → escalates to electrician
- [ ] **Cal** — Day (calendar, habits, rest) → escalates to friend/clinician
- [ ] **Ada** — Access (captions, plain, screen-reader) → escalates to access lead
- [ ] **Kim** — Kids' desk (only kid-safe) → escalates to guardian
- [ ] **Oli** — Older years (meds reminders you set, rides) → escalates to family/nurse
- [ ] **Val** — Food (leftovers, allergens, kitchens) → escalates to inspector
- [ ] **Roo** — House/roof (listings, repair crews) → escalates to housing org
- [ ] **Ned** — Neighbor net ("is my radio up?") → escalates to radio keeper
- [ ] **Ivo** — Ideas (write proposals clearly) → escalates to facilitator
- [ ] **Tess** — Translate (10+ languages, plain) → escalates to human translator
- [ ] **Moss** — Earth (air, heat, flood alerts) → escalates to emergency mgmt
- [ ] **Gia** — Grow (garden/farm tips) → escalates to agronomist
- [ ] **Wren** — Work (hours, co-op ownership, wage warnings) → escalates to labor clinic
- [ ] **Pia** — Press (source box, public notes) → escalates to editor
- [ ] **Jo** — Job/hire (local hire first) → escalates to human HR
- [ ] **Dex** — Shop till (sales, surplus, community day) → escalates to owner
- [ ] **Tax** — Year file (export, reminders) → escalates to CPA
- [ ] **Ira** — Insure-aware ("this looks like insurance — stop") → escalates to counsel
- [ ] **Quinn** — Questions (search the commons) → escalates to topic owner

## 7.3 — Ambient Behavior
- [ ] Contextual surfacing (not a panel you open)
- [ ] Notices deadlines and offers help
- [ ] Sees food nearby and mentions it
- [ ] Learns your patterns ("You usually check on Gran at 10 AM...")
- [ ] Sources visible, confidence shown
- [ ] "I don't know" when uncertain
- [ ] "Ask a person" always available
- [ ] DOES things: drafts quests, posts marketplace, finds rides, looks up resources

---

# PHASE 8: OFFLINE & MESH (Weeks 17-19)

**Goal:** Core features work when the internet is gone. For 48 hours minimum.

## 8.1 — Local-First Data (Automerge/CRDT)
- [ ] Automerge for pocket data (local-first, syncs when connected)
- [ ] SQLite for structured local storage
- [ ] Conflict resolution rules (from miwalk.ts):
  - Money: reservation wins, human review if conflict
  - Ballots: hold until deadline, first-valid wins
  - Role changes: human review always
  - Resource updates: last-wins for non-critical, human-review for critical
- [ ] Never auto-resolve money, guardianship, or binding ballots

## 8.2 — Service Worker + PWA
- [ ] next-pwa for installable web app
- [ ] Offline page with cached content
- [ ] Background sync for queued actions
- [ ] Push notifications via Web Push API / ntfy
- [ ] Lesson packs downloadable for offline use
- [ ] Resource packs cached (shelters, food, legal)

## 8.3 — Mesh Transport (When Ready)
- [ ] BLE peer discovery (Web Bluetooth API where available)
- [ ] WiFi-Direct for larger payloads
- [ ] DTN store-and-forward routing
- [ ] QoS: voice and life-safety bundles first
- [ ] Spectrum legal envelope enforcement per jurisdiction
- [ ] LoRa integration for long-range (requires hardware)
- [ ] MiESP ($5 ESP32 density nodes) for community mesh

## 8.4 — Offline Ballots
- [ ] Hold ballot near deadline
- [ ] Submit when connectivity returns
- [ ] Clear visual: "Your vote is saved. It will submit when connected."
- [ ] Time-stamped proof of intent

---

# PHASE 9: FEDERATION & SOVEREIGNTY (Weeks 20-22)

**Goal:** A community can run their own instance, federate with others, and survive on their own hardware.

## 9.1 — Self-Hosted Supabase
- [ ] Documentation for self-hosting Supabase
- [ ] Migration scripts from cloud to self-hosted
- [ ] Data export always works (even during dispute)

## 9.2 — MiGit (Forgejo)
- [ ] Community-owned code repository
- [ ] MiCompat OSI purity gate (reject non-OSI dependencies)
- [ ] Two-person merge requirement

## 9.3 — Federation Protocol
- [ ] Places can fork and still communicate
- [ ] Profile portability between instances
- [ ] Standing portability rules (cooling period on move)
- [ ] Law-pack differences preview before moving
- [ ] ActivityPub or custom federation for inter-instance messaging

## 9.4 — K3s Deployment
- [ ] OpenTofu infrastructure management
- [ ] Container-based deployment
- [ ] Place-level key management
- [ ] Continuity recovery drills

## 9.5 — IoT Spine (First Devices)
- [ ] FIWARE Orion + MQTT bus
- [ ] First integration: home energy monitoring
- [ ] Second: community garden sensors
- [ ] Two-person actuation gates (safety rule)
- [ ] Digital twin visualization via Ditto/CesiumJS

---

# PHASE 10: POLISH & SHIP (Weeks 23-24)

**Goal:** Accessible. Fast. Beautiful. Deployed. The internet door is open.

## 10.1 — Accessibility Audit
- [ ] WCAG 2.2 AA compliance on all screens
- [ ] Screen reader testing (NVDA, VoiceOver)
- [ ] Keyboard navigation complete
- [ ] High contrast mode
- [ ] RTL language support
- [ ] MiPlain: banned jargon enforcement (CI linting)
- [ ] Grandmother test: can she read every screen aloud and know what to tap?

## 10.2 — Performance
- [ ] Every screen loads in under 1 second
- [ ] Skeleton loaders show structure immediately
- [ ] Real data fills in progressively
- [ ] Images lazy-loaded and optimized
- [ ] Bundle analysis and code splitting

## 10.3 — Internationalization
- [ ] 10+ languages (start with English, Spanish, Arabic — from existing locales)
- [ ] Plain language in all languages
- [ ] RTL layout support
- [ ] Tess helper for translation assistance

## 10.4 — Deployment
- [ ] Vercel free tier (immediate)
- [ ] Custom domain (milyfe.fun or similar)
- [ ] Cloudflare DNS (free)
- [ ] Supabase Cloud (free tier: 500MB DB, 2GB storage, 50k auth)
- [ ] Monitoring: GlitchTip or Sentry free tier
- [ ] CI/CD: GitHub Actions

## 10.5 — Guest Experience
- [ ] Landing page with live counters (proof of life)
- [ ] Guest can see: activity feed, counters, marketplace, resource list
- [ ] Guest cannot: post, claim, vote, message
- [ ] One-tap signup from any guest screen
- [ ] No tutorial carousel — value visible in 60 seconds

---

# PHASE 11: ADVANCED SYSTEMS (Weeks 25-30)

**Goal:** Port the advanced features from old builds — content production, AI vision bounties, on-device AI, and infrastructure independence.

## 11.1 — MiStory Studios (Autonomous Content Production)
- [ ] Content pipeline kanban: Ideation → Scripting → Production → Post-Production → Publishing
- [ ] Autonomous content loop: SENSE → THINK → CREATE → PUBLISH → LEARN
- [ ] AI Voice/TTS integration (Piper for offline, Coqui for quality)
- [ ] AI Music generation (AudioCraft/MusicGen)
- [ ] Video editing tools integration (Remotion for programmatic, Kdenlive for manual)
- [ ] Multi-language auto-publishing (20+ languages via LibreTranslate/Argos)
- [ ] Multi-platform distribution (all social platforms simultaneously)
- [ ] Community radio automation (AzuraCast)
- [ ] Podcast hosting (Castopod)
- [ ] Photo sharing (Pixelfed, federated)
- [ ] "Create" button on every screen (post text/photo/audio/video in 10 seconds)

## 11.2 — Vanguard Protocol (Gangs to Guilds)
- [ ] Coordinape-style guild system (form circle, peer-review, divide bounty)
- [ ] $MLY protection bounties for block stewardship
- [ ] Digital Truces with $MLY escrow and 30-day timers
- [ ] Peace Bonus payout mechanism (truce holds → massive reward)
- [ ] Loomio/Matrix mediation rooms with Community Elders
- [ ] BigBlueButton mentorship matching (verified survivors → current)
- [ ] Youth sandbox (Godot/Scratch projects → Youth Credits)

## 11.3 — Eco-Bounties (AI-Verified Environmental)
- [ ] YOLOv8 photo analysis for hazard classification and bounty pricing
- [ ] LLaVA multimodal verification (before/after cleanup photos)
- [ ] OpenLitterMap integration for geographic hazard mapping
- [ ] ChirpStack IoT sensors for smart waste bins (capacity alerts)
- [ ] Haul gigs when bins full (alert → claim → complete → $MLY)
- [ ] EAS cryptographic badges for Spotter/Sweeper reputation
- [ ] Anti-farming: daily caps, AI verification, community dispute

## 11.4 — Word-to-Math Engine
- [ ] Natural language parser → Formula AST generation
- [ ] Constitutional compliance screening on every formula
- [ ] No-deprivation guard (can't go negative)
- [ ] Formula Card UI (inspectable before signing)
- [ ] Explicit signature requirement before execution
- [ ] Formula types: ALLOCATE, TRANSFER, SAVE, PROPOSE, MANDATE
- [ ] Mandate rules (recurring automated actions with conditions)
- [ ] Formula breeding (combine two → hybrid, requires Circle vote)

## 11.5 — SLM Pipeline (On-Device AI)
- [ ] llama.cpp compiled to WASM for browser/offline inference
- [ ] Base models: TinyLlama, Phi-3-mini, Gemma-2B, Qwen-1.5B (all MIT/Apache)
- [ ] Ring routing: Device (Ring 0, <500ms) → Mesh (Ring 1) → Cloud (Ring 2, consent required)
- [ ] Personal LoRA training on device from user interactions
- [ ] LoRA breeding via Chiasm (consent-based cross-user learning)
- [ ] Constellation Debate (fan request across multiple SLMs, merge votes)
- [ ] Inbreeding detector + size caps on LoRA fragments
- [ ] Mi works fully offline with on-device models

## 11.6 — Sovereign Safety (Advanced)
- [ ] Traffic Stop Protocol with IPFS/Arweave tamper-proof anchoring
- [ ] Jitsi emergency crisis streaming to designated contacts
- [ ] Ushahidi crisis mapping for neighborhood incidents
- [ ] Emergency Resilience Mining (10x $MLY multiplier during grid failures)

## 11.7 — Hybrid Node (Desktop/Home Server)
- [ ] Tauri desktop app for cross-platform node operation
- [ ] Iroh storage vault with hot/warm/cold twin replication
- [ ] Althea bandwidth relay for community mesh
- [ ] Perception Fabric for hardware sensor integration
- [ ] Dual Telemetry: private nerve (encrypted) + public nerve (ZK proofs)
- [ ] $MLY earning for node uptime

---

# PHASE 12: INFRASTRUCTURE INDEPENDENCE (Weeks 31-36)

**Goal:** Full MiCloud stack operational. Community owns its own infrastructure. No corporate dependency.

## 12.1 — MiCloud Core Services
- [ ] MiCompute (container orchestration — K3s)
- [ ] MiBase SQL (Postgres with Supabase interface)
- [ ] MiBase Pulse (real-time subscriptions)
- [ ] MiFlash (Redis cache layer)
- [ ] MiFind (search — MeiliSearch)
- [ ] MiGate (API gateway — Traefik/Caddy)
- [ ] MiQueue (message queue — NATS/RabbitMQ)
- [ ] MiSignal (WebSocket — Supabase Realtime)
- [ ] MiWatch (monitoring — OpenObserve + GlitchTip)
- [ ] MiShield (security — CrowdSec + Wazuh)

## 12.2 — Media Infrastructure
- [ ] PeerTube (video hosting, 4K, WebTorrent P2P)
- [ ] AzuraCast (radio automation)
- [ ] Castopod (podcast hosting)
- [ ] Navidrome/Funkwhale (music library)
- [ ] Jellyfin (cinema/video library)
- [ ] Audiobookshelf (audiobooks/podcasts)
- [ ] Ghost (news/journalism platform)
- [ ] WriteFreely (federated blogging)
- [ ] Pixelfed (photo sharing, federated)

## 12.3 — Social Infrastructure
- [ ] Matrix Synapse (federated messaging + E2EE)
- [ ] Jitsi (video calls)
- [ ] Rocket.Chat or equivalent (team/circle chat)
- [ ] Mastodon (federated social feed)
- [ ] BookWyrm (book club, federated)

## 12.4 — Governance Infrastructure
- [ ] Decidim (participatory democracy platform)
- [ ] Polis (opinion mining / AI consensus)
- [ ] Loomio (group decision-making)

## 12.5 — Commerce Infrastructure
- [ ] Medusa (headless marketplace)
- [ ] TimeOverflow (time banking)
- [ ] hledger (double-entry community accounting)

## 12.6 — AI Infrastructure
- [ ] Ollama (model serving, CPU-only)
- [ ] LiteLLM (model router)
- [ ] AnythingLLM (RAG + memory)
- [ ] Flowise (AI workflow builder)
- [ ] Open WebUI (Mi interface)

## 12.7 — Telecom (Future Phase)
- [ ] eSIM provisioning via SGP.22
- [ ] Open5GS core network (when scale demands)
- [ ] CBRS small cells (shared spectrum)
- [ ] Starlink backhaul for remote coverage
- [ ] Community ISP model (MiNetwork)

---

# THE $MLY LEGAL FRAMEWORK

**What $MLY is:**
- A community credit issued by public rules within the MiLyfe platform
- Real from day one. Earned through contribution, received as UBI, spent locally, traded voluntarily
- No CEO. No founder mint. No APY. No "investment in our team."

**What people can do with $MLY (from day one):**
- Earn it: UBI (weekly credits to every verified member), quests, contributions, teaching, care
- Spend it: marketplace purchases, shop payments, service exchange, thank someone
- Trade it: voluntary peer-to-peer swap with anyone who consents (cash, goods, labor, BTC — anywhere two people agree)
- Donate it: mutual aid, emergency pulses, community projects, circle treasuries
- Save it: personal jars, household shared jars, goal-based saving

**What MiLyfe does NOT do:**
- We do not run an exchange (no order book, no market-making, no listing)
- We do not custody other people's money (your credits, your keys, your export)
- We do not sell $MLY (no ICO, no token sale, no investor allocation, no pre-mine beyond UBI)
- We do not pitch $MLY as an investment (no APY, no yield, no dividends, no appreciation promise)
- We do not set the price (peer swaps happen at whatever rate two people agree to)

**The peer-swap legal basis:**
- Two people can voluntarily exchange anything they both consent to — this is basic commerce/barter
- If someone runs a public cash-out booth or exchange desk, THEY are the exchange — they follow MSB/MiCA/local rules. MiLyfe does not operate that booth.
- MiLyfe may list self-declared community doorways (places that accept $MLY) — listing is not operating

**What requires community vote + legal review to ACTIVATE:**
- Public exchange listing (Uniswap, CEX, etc.) — requires securities/money-transmission analysis
- Cross-border automated exchange — requires compliance with local regulations
- Merchant POS integration with fiat settlement — requires payment processor compliance

**What NEVER requires permission:**
- Earning credits through participation
- Spending credits within the platform
- Voluntary peer-to-peer trading between two consenting people
- Exporting your transaction history
- Leaving with your data

**Legal nature (said plainly):**
$MLY is a community credit. It is not a security (no expectation of profit from others' efforts). It is not a commodity (no underlying asset). It is not a currency (not issued by a government). It is a voluntary medium of exchange within a community — same legal category as arcade tokens, airline miles, or co-op store credit — except members can freely trade them peer-to-peer because we don't restrict that right.

---

# THE STAGES (From MiLyfe_COMPLETE.md §XX — Renamed: No "Practice" Language)

Same profile, same five tabs, across all stages. $MLY Credits are real at every stage.

| Stage | What | Milestone |
|---|---|---|
| **Lab** | Identity + pocket + UBI drip in a room. US-FL and EU law packs. No public sale. No founder keys. | 1 person, 1 flow works |
| **First Street** | Recovery, voice, mesh P0s, child gate, Mi, Learn paths 1-8, Pulse, defense leave-now. Real $MLY circulating internally. | 10 people govern together |
| **Roots** | StreetGoods, peace table, reentry pack, $MLY peer-swap (voluntary, legal), first 100 ratify compact | 100 ratify |
| **Canopy** | All ten paths, languages, offline AI, shops on the street | Full community |
| **Forest** | $MLY exchange amounts voted by community; external convert open; still no "investment" pitch | Open economy |
| **Ecosystem** | Protocol + SDK + mesh-in-a-box. Born anywhere → lawful subset → leave with the box | Fork and federate |

**Key:** The difference between stages is NOT "real vs fake money." $MLY is real from Lab. The difference is SCALE (how many people) and CAPABILITY GATES (external exchange requires community vote + legal review). Nothing resets between stages. Your credits, standing, history — all carry forward because they were always real.

---

# THE $0 STACK (Everything Free)

| Service | Free Tier | Self-Host Later |
|---|---|---|
| Vercel | 100GB bandwidth/mo | Own server |
| Supabase | 500MB DB, 2GB storage, 50k auth | Self-hosted |
| Ollama | Unlimited local (CPU) | Just hardware |
| Cloudflare DNS | Unlimited | Already free |
| GitHub | Unlimited public repos | Forgejo |
| ntfy push | 250 messages/day | Self-hosted |
| MapLibre | Unlimited | Already free |
| MeiliSearch | 100k docs | Self-hosted |
| Framer Motion | MIT, unlimited | Already free |
| shadcn/ui | MIT, unlimited | Already free |

**Total deployment cost: $0.**

---

# THE ALIVE RULES (Every Screen, Every Time)

1. **Something is MOVING** — animation, live data, counter, timer, pulse
2. **Something you can DO** — post, claim, thank, vote, verify, help
3. **Context is VISIBLE** — connection state, greeting, place, $MLY balance
4. **Mi is REACHABLE** — one gesture away from any screen
5. **Celebration is POSSIBLE** — any screen can celebrate good events
6. **Dark mode is ALIVE** — particles glow, cards have depth
7. **It's YOURS** — customizable, rearrangeable, your layout
8. **Speed** — under 1 second, skeletons show structure
9. **Sound** (optional) — subtle haptic + optional sound for key events
10. **The whole thing BREATHES** — ambient motion, like a resting heartbeat

---

# THE RULES (Non-Negotiable)

- Never say "practice" or "fake" — $MLY Credits are real and can be legally and voluntarily swapped from day one
- Never mention political strategy in the platform
- The Oath (24 items) cannot be changed by any vote
- OSI open source or it doesn't ship
- If a grandmother can't read the screen aloud and know what to tap, the screen fails
- Export always works, even during a dispute
- Mi is a helper, not a person, not a lawyer, not the police — always labeled
- One signup, one profile, the whole life together
- People own it by running it — not a charity, not a company
- Constitutional kernel: 8 unamendable rights that no vote can remove
- Default deny for regulated capabilities — stricter jurisdiction wins
- Children are protected by MiChildGate — non-optional, cannot be voted off
- Standing cannot gate rights — it cannot become a social credit score
- Helpers at 5% chorus cap maximum — AI never runs the place

---

# MODULE COUNT

| Category | Count | Status |
|---|---|---|
| Pre-Code Design Documents | 12 | 0 written |
| P0 Coordination Layer Systems | 7 | 0 implemented |
| Life/Civic Modules | 44 | ~8 have logic, ~36 need building |
| Smart Universe Modules | 32 | 0 implemented (Phase 9+) |
| Custom Systems (P0-P3) | 24 | 0 implemented |
| Named Helpers | 25 front + 18 back | 0 implemented (generic Mi only) |
| Alive Features | 10 rules x every screen | 0 implemented |
| Old Build Features to Port | 42+ distinct features | 0 ported |
| Missing Life Modules (Phase 6.5) | 26 | 0 implemented |
| MiStory Studios (Phase 11) | 130+ production tools | MiStory-Studios app exists (port) |
| Vanguard + Eco-Bounties (Phase 11) | 2 major systems | Hostinger UI existed (port) |
| Word-to-Math + SLM (Phase 11) | 2 major engines | milyfe-mvp specs exist (build) |
| MiCloud Infrastructure (Phase 12) | 46 services | Docker containers existed (redeploy) |
| Wire Protocols (Phase 11-12) | 8 protocols | Specified in milyfe-mvp (build) |

---

# WHAT WINS

This map is the execution plan. But if anything conflicts:

1. `MiLyfe_Ultimate_Manual.md` — the V1 official manual, wins over everything
2. `MiLyfe_Complete_Build_Map.md` — this document, the implementation plan
3. `MiLyfe_Blueprint_Gap_and_New_Tech_Audit.md` — what to build vs adopt
4. `MiLyfe_Interactive_Design_Spec.md` — alive design patterns
5. `MiLyfe_COMPLETE.md` — historical reference only (contains outdated language)
2. `MiLyfe_Interactive_Design_Spec.md` — the build blueprint
3. `MiLyfe_Blueprint_Gap_and_New_Tech_Audit.md` — what to build vs adopt
4. `MiLyfe_Build_Audit_and_Roadmap.md` — phase priorities
5. This document — combines all four into action

---

*This is the map. 11 years of vision. $0 budget. Everything open source. Let's build it alive.*
