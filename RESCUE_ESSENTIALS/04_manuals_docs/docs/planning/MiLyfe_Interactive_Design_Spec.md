# MiLyfe Interactive Design Specification — THE MERGE

**Date:** August 19, 2026  
**Purpose:** Unified design merging the 41-service brain (current build) with the living energy (old builds). Everything alive. Nothing static. One platform.  
**Rule:** This is the real thing. No "practice." No "fake." $MLY Credits are real from day one.  
**Merge Philosophy:** The new doesn't dominate the old. The old doesn't dominate the new. They become ONE thing that breathes.

---

# 1. The Energy Principles

The app must feel like walking into a neighborhood where things are already happening.

1. **Alive:** Real-time activity. Numbers moving. People doing things NOW.
2. **Personal:** YOUR layout. YOUR journey. YOUR home screen. Not one template for everyone.
3. **Interactive:** Post in 10 seconds. Claim in one tap. Help in two taps. Not "read about how to help."
4. **Visual:** Standing GROWS visually. Journey has DEPTH. Celebrations are FELT. Not text labels.
5. **Immediate:** Useful in 60 seconds. No tutorial. No onboarding carousel. Value NOW.

---

# 2. Technology Selections (Premium/Free, Agent-Configurable)

## Frontend Framework

| Need | Selection | License | Why |
|---|---|---|---|
| Runtime | **Next.js 14** (App Router) | MIT | SSR, real-time, faster than Expo web. Previous builds used it successfully. |
| UI Library | **shadcn/ui** + **Radix Primitives** | MIT | Headless, accessible, beautiful. Used in Bldg build already. |
| Animations | **Framer Motion** | MIT | Smooth, spring-based, gesture-aware. Makes the UI breathe. |
| Canvas/Particles | **HTML5 Canvas** (custom, from MiLyfe-OS) | — | Ambient particle field. Already built in previous version. |
| State | **Zustand** | MIT | Simpler than Context for real-time updates across many components. |
| Real-time | **Socket.IO** or **Supabase Realtime** | MIT/Apache-2.0 | Live feed, live counters, presence. |
| Styling | **Tailwind CSS 4** | MIT | Fast iteration, responsive, dark mode built-in. |
| Icons | **Lucide React** | ISC | Consistent, accessible, tree-shakeable. |
| Charts | **Recharts** or **Tremor** | MIT | Community stats, Pulse, pot spending visuals. |
| Maps | **MapLibre GL JS** | BSD | Privacy-first, no Google dependency, offline tiles. |
| Forms | **React Hook Form** + **Zod** | MIT | Fast, validated, accessible forms. |
| PWA | **next-pwa** | MIT | Installable, offline-capable, push notifications. |
| Mobile | **Capacitor** (from Next.js) | MIT | Same codebase → native iOS/Android when ready. |

## Backend / Services

| Need | Selection | License | Why |
|---|---|---|---|
| Database | **Supabase** (Postgres + Realtime + Auth + Storage) | Apache-2.0 | Free tier. Real-time subscriptions. Row-level security. Auth built in. Self-hostable. |
| Auth | **Supabase Auth** + **WebAuthn** | Apache-2.0 | Passkeys, magic links, social. No passwords. |
| Real-time | **Supabase Realtime** | Apache-2.0 | WebSocket subscriptions for feed, counters, presence. |
| File Storage | **Supabase Storage** | Apache-2.0 | Media uploads, lesson packs, documents. |
| AI / LLM | **Ollama** (self-hosted) or **OpenRouter** (API) | MIT/— | Mi conversations. Local when possible, API fallback. |
| Messaging | **Matrix** (Element/Synapse) or **Supabase + WebSockets** | Apache-2.0 | Start with Supabase realtime chat, migrate to Matrix when federation needed. |
| Push Notifications | **ntfy** (self-hosted) or **Web Push API** | Apache-2.0/— | Free, no vendor lock-in. |
| Background Jobs | **Trigger.dev** or **BullMQ** | Apache-2.0/MIT | UBI delivery, quest verification, freshness checks. |
| Search | **Supabase Full Text** or **MeiliSearch** | — / MIT | Local resource search, lessons, people. |
| Edge Functions | **Supabase Edge Functions** (Deno) | Apache-2.0 | Serverless logic. Runs anywhere. |

## Infrastructure

| Need | Selection | License | Why |
|---|---|---|---|
| Hosting | **Vercel** (free tier to start) → **K3s** (self-hosted later) | — / Apache-2.0 | Deploy in 30 seconds. Migrate when ready. |
| Database hosting | **Supabase Cloud** (free tier) → self-hosted Supabase | Apache-2.0 | 500MB free. Then own hardware. |
| Media CDN | **Cloudflare R2** (free egress) or **Supabase Storage** | — | Free bandwidth. No surprise bills. |
| CI/CD | **GitHub Actions** (free) or **Woodpecker** (self-hosted) | — / Apache-2.0 | Free for open source. |
| Monitoring | **Sentry** (free tier) or **GlitchTip** (OSI) | — / MIT | Error tracking without data export. |
| DNS | **Cloudflare** (free tier) | — | Global, fast, free. |

---

# 3. Interactive Features Design

## 3.1 Live Activity Feed (The Heartbeat)

**What:** Real-time stream of anonymized community activity. Always running. Makes the app feel alive the moment you open it.

**Shows:**
- "Someone thanked a neighbor for watching kids" (no names unless they opt to show)
- "A quest was completed: 'Verify pantry hours'"
- "The shade proposal just got funded"
- "3 people joined Riverside this week"
- "Harbor Bakery posted surplus: 8 bread bags"

**Tech:** Supabase Realtime subscriptions → WebSocket → Zustand store → animated list with Framer Motion enter/exit.

**UX:** Scrollable stream. Filterable by: All, Street, Pocket, Voice, People. Items appear with gentle slide animation. Timestamp relative ("2 min ago"). Can interact (thank back, claim surplus, support proposal).

## 3.2 Customizable Home Layout

**What:** Everyone's home screen reflects THEIR life. Not one layout for all.

**Tech:** 
- Zustand persisted store for layout configuration
- Drag-and-drop widget system (using `@dnd-kit/sortable`)
- Widget catalog: Balance, Weekly Share, Feed, Quests, Nearby, Classes, Messages, Pulse, Standing, Journey

**Widgets available:**
- Balance widget (your $MLY credits)
- Activity stream widget (live feed)
- Quest widget (active/available quests)
- Nearby widget (food, help, rides)
- Messages widget (unread count + preview)
- Journey widget (learning progress)
- Standing widget (visual facets)
- Pulse widget (street weather)
- Calendar widget (deadlines, classes, check-ins)
- Quick actions widget (thank, post, quest)

**First-time:** Intelligent default based on profile. If homeless → emphasize resources. If parent → emphasize kid stuff + schedule. If reentry → emphasize deadlines + jobs. Member customizes from there.

## 3.3 Quests System

**What:** Real tasks that improve the community. Earn $MLY Credits. Build standing. Not gamification for engagement — real work that matters.

**Quest types:**
- 🧹 Cleanup: "Pick up trash on Oak & Main" — take a photo to verify
- 🔍 Verify: "Confirm Northside Pantry is still open Tue-Fri" — check and report
- 🤝 Care: "Check on elder at 412 Pine" — they confirm you showed up
- 📚 Teach: "Host a 30-min reading circle" — learners confirm attendance
- 🏪 Support: "Buy something from a local shop with $MLY" — receipt generated
- 🗳️ Civic: "Read the shade proposal and vote" — participation tracked
- 🌱 Build: "Plant something in the community garden" — photo verify
- 🚶 Safety: "Walk the block at 7 PM" — presence logged, not a patrol

**Rewards:** $MLY Credits + Standing attestation. Caps per day. Can't farm.

**Tech:** Supabase table `quests`. Edge functions for verification. Photo upload to Storage. Geolocation optional (for location-based quests). Claim → Do → Verify → Reward pipeline.

## 3.4 Marketplace (Post in 10 Seconds)

**What:** Goods, services, rides, needs. Your neighbors are the economy.

**Categories:**
- 🍽️ Food (surplus, meals, produce)
- 🔧 Services (repair, haircut, tutoring, babysitting)
- 🚗 Rides (going to VA Thursday? Take someone)
- 📦 Goods (furniture, clothes, tools — give/trade/sell)
- 📚 Education (tutoring, classes, study groups)
- 🏠 Housing (room, sublease, temporary)
- 💼 Jobs (gig work, part-time, apprenticeship)

**Post flow:** Category → Title → Price in $MLY (or free/trade) → Photo optional → Post. 10 seconds max.

**Claim flow:** "I want this" → Coordinate in messages → Exchange → Both confirm → Standing attestation.

**Tech:** Supabase table. Real-time feed. Geolocation for "near me" sorting. Expiry dates. Claimed/available states.

## 3.5 Live Counters & Momentum

**What:** Visible numbers that show the community growing and moving. Not vanity metrics — real proof things are happening.

**Counters:**
- Members active this week
- $MLY Credits circulating
- Quests completed today
- Resources verified this week
- Proposals in progress
- Surplus items posted
- Rides shared

**Tech:** Supabase materialized views or edge function aggregation. WebSocket for real-time tick. Animated number transitions (Framer Motion spring).

**Placement:** Visible on landing/guest view. Updated every 10 seconds. Shows life.

## 3.6 Visual Citizen Card

**What:** YOUR identity. Animated. Personal. Shows your standing. Feels real and valuable.

**Shows:** Avatar/photo, name, home place, standing facets (visual: glowing orbs that grow), member since date, QR for receiving $MLY.

**Animation:** Card has subtle gradient shift. Standing orbs pulse gently. Can flip to show QR code.

**Tech:** Framer Motion for card animation. Canvas for standing visualization. SVG for facets.

## 3.7 Celebrations

**What:** When good things happen, the app acknowledges it. Not fake. Real joy.

**Triggers:**
- Weekly share arrives → gentle green pulse on balance
- Quest completed → confetti burst (short, respectful)
- Proposal passes → community celebration banner
- Milestone reached (30 days peace, first class taught, etc.) → special animation
- Someone thanks you → warm glow on notification

**Tech:** Framer Motion + Canvas confetti (lightweight). Celebration state in Zustand. Auto-dismiss after 3 seconds. Never blocks interaction.

## 3.8 Media Creation

**What:** People create and share their own content. Stories. Live streams. Audio. Writing.

**Types:**
- 📝 Post (text + photo, like the feed but intentional)
- 🎙️ Audio message (voice note to the street)
- 📸 Photo story (document what's happening)
- 📡 Live (go live for the street — OwnCast/Jitsi integration later)
- 📰 Write (longer form — community journalism)

**Tech:** Supabase Storage for media. Web Audio API for recording. Camera API for photos. Markdown for writing.

## 3.9 Care Exchange (Time Banking)

**What:** Trade time and skills. Not just money. "I'll watch your kids for 2 hours if you help me move."

**How:** Post an offer ("I can do X") or a need ("I need Y"). Match. Exchange. Both confirm. Standing grows.

**Unit:** Hours. Not $MLY. Separate from money. Builds a different kind of wealth.

**Tech:** Supabase table. Matching algorithm. Confirmation flow. Standing attestation on completion.

## 3.10 Ambient Animation (Particle Field)

**What:** The background BREATHES. Subtle, beautiful, alive. Not decorative — communicative.

**Behavior:**
- Particles increase when community is active (more people online = more particles)
- Color shifts with Pulse state (green = good, amber = attention)
- Responds to mouse/touch (particles avoid cursor gently)
- Reduced motion: static gradient instead

**Tech:** HTML5 Canvas. Exactly as built in MiLyfe-OS. 60fps on modern hardware, 30fps fallback. Disabled if `prefers-reduced-motion`.

## 3.11 Journey Visualization

**What:** Your learning path is spatial and visual. Not a linear progress bar — a WORLD you move through.

**Visual:** A landscape/path that scrolls as you progress. Milestones are landmarks. Completed lessons are behind you. Next lesson is ahead. Branches visible.

**Tech:** SVG + Framer Motion. Data from learning content service.

## 3.12 Kids Interactive

**What:** Not a restricted adult app. A genuinely FUN kid experience.

**Features:**
- 🎮 Mini-games (counting, matching, reading)
- 🎨 Drawing/sandbox creative space
- 💰 Vault (savings jar with visual fill animation)
- 🏆 Achievements (stickers, not scores)
- 📚 Stories (interactive, choice-based)

**Tech:** Canvas for games/drawing. Separate route with own nav. No money movement. No adult contact.

## 3.13 Rides

**What:** "I'm going to [place] at [time]. Room for [N] people."

**Flow:** Post a ride (destination, time, seats) → Someone claims a seat → Coordinate in messages → Both confirm → Standing.

**Tech:** Supabase table. Time-based expiry. Map visualization optional. Messages integration for coordination.

## 3.14 Circles

**What:** Groups within the community. Interest-based, defense-based, learning-based.

**Types:**
- Learning circles (study groups)
- Defense circles (rides, childcare, witness)
- Interest circles (gardening, repair, cooking)
- Street circles (your block)
- Peace circles (mediation groups)

**Tech:** Supabase groups with membership. Group chat (realtime). Group quests. Group pot.

## 3.15 Guest Explorer

**What:** Before signup, feel the energy. See the feed (anonymized). See counters. Browse resources. THEN decide.

**Shows:** Live counters, anonymized activity feed, public resources, learning paths preview, the energy of the community.

**Tech:** Public routes with read-only Supabase subscriptions. No auth required. Convert to member with one click.

---

# 4. GitHub Repositories & Libraries

## Core Framework
- `vercel/next.js` — MIT — App router, SSR, edge
- `shadcn/ui` — MIT — Headless UI components
- `radix-ui/primitives` — MIT — Accessible primitives beneath shadcn
- `tailwindlabs/tailwindcss` — MIT — Utility CSS
- `framer/motion` — MIT — Animation library
- `pmndrs/zustand` — MIT — State management
- `lucide-icons/lucide` — ISC — Icon set
- `clauderic/dnd-kit` — MIT — Drag and drop for layout customization
- `colinhacks/zod` — MIT — Schema validation
- `react-hook-form/react-hook-form` — MIT — Forms

## Real-time & Backend
- `supabase/supabase` — Apache-2.0 — Database + Auth + Realtime + Storage + Edge Functions
- `supabase/realtime` — Apache-2.0 — WebSocket subscriptions
- `triggerdotdev/trigger.dev` — Apache-2.0 — Background jobs (UBI delivery, quest verification)
- `meilisearch/meilisearch` — MIT — Fast search

## Media & Content
- `owncast/owncast` — MIT — Self-hosted live streaming (when ready)
- `PeerTube` — AGPL-3.0 — Video hosting (federation-ready)
- `AzuraCast/AzuraCast` — Apache-2.0 — Community radio

## Maps & Location
- `maplibre/maplibre-gl-js` — BSD — Privacy-first maps
- `openstreetmap` — ODbL — Map data

## AI
- `ollama/ollama` — MIT — Local LLM hosting
- `vercel/ai` — Apache-2.0 — AI SDK for streaming responses in UI

## Mobile (Phase 2)
- `ionic-team/capacitor` — MIT — Web → Native bridge
- `nicklockwood/iVersion` — MIT — iOS distribution

## Mesh (Phase 3)
- `reticulum/reticulum` — MIT — Mesh networking protocol
- `meshtastic/firmware` — GPL-3.0 — LoRa mesh

---

# 5. Database Schema (Supabase/Postgres)

```sql
-- Core tables that make it ALIVE

CREATE TABLE profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  display_name TEXT NOT NULL,
  avatar_url TEXT,
  home_place TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  personhood_status TEXT DEFAULT 'none',
  layout_config JSONB DEFAULT '{}',
  standing_data JSONB DEFAULT '{}'
);

CREATE TABLE feed_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type TEXT NOT NULL, -- 'thank', 'quest_complete', 'surplus', 'proposal_pass', 'join'
  actor_id UUID REFERENCES profiles(id),
  content JSONB NOT NULL,
  anonymous BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE quests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,
  reward_mly NUMERIC DEFAULT 0,
  status TEXT DEFAULT 'open', -- open, claimed, completed, expired
  claimed_by UUID REFERENCES profiles(id),
  place TEXT,
  verification_type TEXT, -- 'photo', 'confirmation', 'geolocation', 'self'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

CREATE TABLE marketplace_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  seller_id UUID REFERENCES profiles(id) NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,
  price_mly NUMERIC,
  price_type TEXT DEFAULT 'fixed', -- fixed, trade, free
  status TEXT DEFAULT 'active', -- active, claimed, completed, expired
  claimed_by UUID REFERENCES profiles(id),
  photo_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

CREATE TABLE rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id UUID REFERENCES profiles(id) NOT NULL,
  destination TEXT NOT NULL,
  departure_time TIMESTAMPTZ NOT NULL,
  seats_available INT DEFAULT 1,
  passengers UUID[] DEFAULT '{}',
  status TEXT DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE care_exchanges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  offerer_id UUID REFERENCES profiles(id),
  type TEXT NOT NULL, -- 'offer' or 'need'
  skill TEXT NOT NULL,
  hours NUMERIC,
  matched_with UUID REFERENCES profiles(id),
  status TEXT DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE circles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- learning, defense, interest, street, peace
  members UUID[] DEFAULT '{}',
  place TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE celebrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL,
  user_id UUID REFERENCES profiles(id),
  data JSONB,
  dismissed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

# 6. Gap Fill: What the Current Build Is Missing

| Gap | Feature | Priority |
|---|---|---|
| No real-time anything | Live feed + WebSocket subscriptions | P0 |
| Static home screen | Customizable widget layout | P0 |
| No interactivity | Quests (claim/do/verify) | P0 |
| No marketplace | Post/claim/exchange in 10 seconds | P0 |
| No visible momentum | Live counters on every screen | P0 |
| No celebrations | Visual feedback for good events | P1 |
| No media creation | Post, record, photo, write | P1 |
| No care exchange | Time banking / skill swaps | P1 |
| No ambient life | Particle field background | P1 |
| No visual identity | Animated citizen card | P1 |
| No rides | Ride coordination | P1 |
| No circles | Interest/defense groups | P1 |
| No kid interactivity | Games, sandbox, stories | P2 |
| No journey visual | Spatial learning landscape | P2 |
| No guest energy | Live preview before signup | P2 |
| "Practice" language | REMOVED. $MLY Credits are real. | DONE |

---

# 7. Implementation Order

## Sprint 1: The Heartbeat (Week 1-2)
1. Set up Next.js 14 + shadcn/ui + Tailwind + Framer Motion
2. Connect Supabase (database + auth + realtime)
3. Build live activity feed with real-time subscriptions
4. Build customizable home with drag-drop widgets
5. Deploy to Vercel (live on internet immediately)

## Sprint 2: Do Something (Week 3-4)
6. Build quest system (post/claim/verify/reward)
7. Build marketplace (post/claim/coordinate)
8. Build live counters (WebSocket, animated)
9. Build celebration system (confetti, glow, banner)
10. Build quick-post (10-second content creation)

## Sprint 3: Feel Something (Week 5-6)
11. Build animated citizen card
12. Build particle field (ambient background)
13. Build care exchange (time banking)
14. Build rides coordination
15. Build circles (groups)

## Sprint 4: Safety & Depth (Week 7-8)
16. Port all safety flows (leave-now, walking-home, rights card)
17. Port governance (proposals, voting, delegation)
18. Build Mi helper with real LLM connection
19. Build kids interactive section
20. Build journey visualization

---

# 8. What Stays from Current Build

Everything in `src/services/` stays. The 41 services are the BRAIN. We're rebuilding the BODY to be alive.

Keep:
- All service logic (MiAction, MiScope, MiReceipt, MiWalk, etc.)
- All type definitions
- All test suites
- Legal resources
- Learning content
- Safety engine
- Recovery engine

Replace:
- Expo/React Native → Next.js (web-first, then Capacitor for mobile)
- Static screens → Interactive real-time screens
- Text-only UI → Animated, visual, alive UI
- Single layout → Customizable per person
- Read-only → Do-something (quests, marketplace, rides, exchanges)

---

# 9. The $0 Stack

Everything above is free or self-hostable:

| Service | Free Tier | Self-Host Cost |
|---|---|---|
| Vercel | 100GB bandwidth/mo | $0 on own server |
| Supabase | 500MB DB, 2GB storage, 50k auth | $0 self-hosted |
| Ollama | Unlimited local | $0 (just hardware) |
| Cloudflare DNS | Unlimited | $0 |
| GitHub | Unlimited public repos | $0 |
| ntfy push | 250 messages/day | $0 self-hosted |
| MapLibre | Unlimited | $0 |
| MeiliSearch | 100k docs | $0 self-hosted |

**Total cost to deploy a living, breathing MiLyfe: $0.**

Hardware needed: one computer with internet. That's it. Scale when needed.

---

*This design is the blueprint for the rebuild. No code until this is reviewed and approved.*


---

# 10. THE MERGE: Current Build + Old Builds = One Living Thing

## What We're Merging

**Current Build (147 files, 41 services):** The brain. Complete type system. Every P0/P1/P2 protocol from the Gap Audit. Safety engine. Recovery. Legal resources. Governance. Offline conflict resolution. Middleware pipeline. 21 test suites. Architectural perfection. **But it reads like a government manual.**

**MiCity Build:** The LIFE. Live feed. Quests. Marketplace (goods/services/rides). Media (radio/TV/news). Kids (sandbox/vault). Care exchange. Peace table. Standing page. DePIN. Guilds. Waves. Cleanup coordination. **But it was scattered and technically incomplete.**

**Bldg Build:** The ENERGY. Live counters. Celebration banners. Activity feed. Citizen pass card. Petition dashboard. Trust/transparency. Vibe lab. PWA install. Matrix messaging. Web3 identity. **But it was governance-focused only.**

**MiLyfe-OS Build:** The PRESENCE. Particle field. Dock navigation. Journey page. OS-like feel. Something you LIVE inside, not visit. **But it was minimal.**

## The Unified Structure: Everything Alive

### Home (Today) — ALIVE, not a list of cards

**Current:** Static priority stack cards (text only)  
**Old (MiCity):** Live feed + quests + marketplace activity  
**Merged:**

The home screen is a LIVING DASHBOARD that the user customizes:

- **Activity stream** running in the background (real-time, from Supabase/WebSocket)
- **Widgets** that the person arranges: Balance, Active Quests, Nearby Now, Messages, My Journey, Pulse, Quick Post
- **Live counter bar** at the top: "47 members active · 12 quests today · 340 $MLY moving"
- **Particle field** ambient behind content (subtle, responds to activity level)
- **"What would make today easier?" becomes interactive**: tap "Find food" → immediately shows live results, not a new screen. Tap "Do a quest" → shows available quests inline.
- **Celebrations** appear organically: share arrives, quest done, proposal passes → brief visual joy

### Pocket — ALIVE, not a balance sheet

**Current:** Balance + static activity list  
**Old (MiCity):** Wallet with claim UBI button, quest rewards, merchant payments, vault  
**Merged:**

- **Balance is animated** — grows visibly when share arrives, shrinks when you thank
- **Weekly share arrival is an EVENT** — not a line item. Green pulse, amount animates in, "Your share arrived."
- **Thank someone** — scan, tap, swipe. 3 seconds. Animation shows it leaving your pocket and "walking" to them.
- **Vault** (from MiCity kids/wallet) — a savings goal with visual fill. "Rent jar is 80% full."
- **Marketplace integration** — "Harbor Bakery: 8 bread bags, 3 $MLY each" shows HERE not in a separate screen
- **Quest rewards appear here** — "You earned 10 $MLY for verifying pantry hours ✓"
- **History is a timeline** — visual, scrollable, alive. Not a table.

### Learn — ALIVE, not a textbook

**Current:** Journey progress + static lesson text  
**Old (MiCity):** Kids sandbox, FreeCodeCamp, Moodle, Oppia integrations  
**Merged:**

- **Journey is SPATIAL** — a visual landscape/map you travel through. Not a progress bar.
- **Lessons are INTERACTIVE** — quiz answers, tap-to-reveal, drag exercises. Not walls of text.
- **"I need a person"** — live connection to a tutor/mentor, not just a button
- **Class hosting is instant** — "I can teach X" → posted to street in 10 seconds
- **Badges are VISUAL trophies** — not text labels. They glow. They stack. They show your growth.
- **Kid mode is PLAY** — games, drawing, interactive stories. From MiCity's sandbox concept.
- **Offline packs work like downloaded podcasts** — visual progress, resume exactly where you stopped

### Street — ALIVE, not a directory

**Current:** Static resource list + Pulse text  
**Old (MiCity):** Marketplace, rides, cleanup coordination, DePIN, care exchange  
**Merged:**

- **The street is a LIVE MAP** — animated pins showing what's available RIGHT NOW. Pins appear/disappear as things are posted/claimed.
- **"Post something"** — surplus food, need a ride, offering a service. 10-second post. Photo optional. Goes live immediately on the map and feed.
- **Quests appear on the map** — "Verify this resource" shows as a pin you walk to.
- **Rides are here** — "Going to VA at 9 AM, room for 2" — claim a seat in one tap.
- **Care exchange is here** — "I'll babysit 2hr if you help me move Saturday"
- **Pulse is VISUAL** — not text. Animated weather-like conditions. Colors shift. The street FEELS different when things are good vs need attention.
- **Cleanup/events coordination** — "Street cleanup Sunday 9 AM — 7 people signed up" with live RSVP
- **Shops are ACTIVE** — "Taking $MLY today ✓" with live inventory, surplus countdown timers

### Voice — ALIVE, not a pipeline diagram

**Current:** Proposal cards with stage labels  
**Old (Bldg):** Petition dashboard, voter page, governance with real counts  
**Old (MiCity):** Governance with circles, Decidim/Polis-style discussion  
**Merged:**

- **Proposals are CONVERSATIONS** — not documents. Real-time discussion thread. Reactions. Questions.
- **Voting is an EVENT** — countdown timer, live participation counter (not results until close), energy around it
- **"What needs attention"** — from MiNeed, but shown as a PULSE. The community's needs rising to the surface live.
- **Results are CELEBRATED** — when something passes, the app shows it happening. Confetti. Banner. "This is going to happen because you decided."
- **Delegation is VISIBLE** — you can see (in aggregate) momentum building. Not who delegated to who.
- **The compact is LIVING** — not a document to read. Interactive. Tap a rule to see: when it was made, what vote, how to change it.

### You — ALIVE, not a settings page

**Current:** Tile grid linking to sub-pages  
**Old (Bldg):** Profile with citizen pass card, trust display  
**Old (MiLyfe-OS):** Profile + journey in one view  
**Merged:**

- **Your card is ANIMATED** — the citizen card from Bldg, but alive. Standing orbs glow and grow. Card flips for QR.
- **Standing is VISUAL GROWTH** — not "Neighbor: known on this street." A GARDEN that grows. Or RINGS that expand. Something you SEE getting bigger over time.
- **Journey integration** — your full life journey in one visual. Where you came from, where you're going. Milestones visible.
- **Privacy is LIVE** — you can see in real-time: "Right now, 0 people can see your location. Only Mara and Sam can message you."
- **Safety is ONE TAP AWAY** — leave-now, walking-home, freeze — not buried under tiles. Prominent. Fast.
- **Messages are HERE** — not hidden. Real-time threads with typing indicators, read receipts, delivery states visible.

### Mi — ALIVE, not a chatbot

**Current:** Half-sheet with starter actions  
**Old (MiCity):** `/mi` page with full AI interaction  
**Merged:**

- **Mi is AMBIENT** — not a panel you open. Mi surfaces information contextually. Notices when you're on a deadline screen and offers help. Sees you looking at food and says "3 bags at Harbor Bakery right now."
- **Mi has PERSONALITY** — warm, short, helpful. Not a generic AI. Named helpers show up: "Nia here — your share just arrived, you have 347 $MLY" ... "Rue: I see you have a court date in 5 days. Want me to help prep?"
- **Mi DOES things** — drafts a quest, drafts a marketplace post, finds a ride, looks up a resource. Not just explains.
- **Mi learns YOUR patterns** — "You usually check in with Gran around 10 AM. It's 10:30 — want me to remind you?"
- **Mi is HONEST** — sources visible. Confidence shown. "I don't know" when uncertain. "Ask a person" always available.

### Youth — ALIVE, not restricted adult mode

**Current:** Static text with different nav labels  
**Old (MiCity):** Kids sandbox, vault, interactive pages  
**Merged:**

- **Games** — real interactive games. Counting, matching, reading, problem-solving. Not worksheets.
- **Sandbox** — creative space. Draw, build, design. Saved to their profile.
- **Vault** — savings visualization. Watch it GROW. Set goals. "12 more $MLY until my book goal!"
- **Stories** — interactive choose-your-own-adventure. Not read-along text.
- **Safety ALWAYS accessible** — one tap, even if everything else is restricted
- **Badges are STICKERS** — visual, collectible, fun. Not text awards.

---

# 11. What EVERY Screen Must Have (The Alive Rules)

Every single screen in the merged app follows these rules:

1. **Something is MOVING** — animation, live data, counter, timer, pulse. Nothing is completely static.
2. **Something you can DO** — not just read. Post. Claim. Thank. Vote. Verify. Help.
3. **Context is VISIBLE** — connection state, time of day greeting, place, $MLY balance in corner.
4. **Mi is REACHABLE** — not a separate screen. One gesture away from any context.
5. **Celebration is POSSIBLE** — any screen can burst into a brief celebration when something good happens.
6. **Dark mode is ALIVE too** — not just inverted colors. Particles glow. Cards have depth. The dark version has its own beauty.
7. **It's YOURS** — customizable. Rearrangeable. Your layout. Your widgets. Your emphasis.
8. **Speed** — everything loads in under 1 second. Skeletons show structure immediately. Real data fills in.
9. **Sound** (optional) — subtle haptic + optional sound cues for: share arrived, quest complete, message received.
10. **The whole thing BREATHES** — ambient motion. Not frantic. Not still. Like a resting heartbeat.

---

# 12. Complete Merged Feature Map

## Features from Current Build (KEEP — the protocols and safety)
All 41 services remain. They become the engine beneath the alive UI:
- MiAction, MiScope, MiReceipt, MiWalk, MiSource, MiStage, MiAppeal, MiModerate, MiHandoff
- Safety engine, recovery engine, legal resources
- Governance engine, delegation engine, membership engine
- Pocket ledger, contribution engine, standing service
- Offline engine, mesh, CRDT sync, DTN routing
- Identity, WebAuthn, notifications, persistent store
- Learning content (3 real paths), life services, sovereign

## Features from Old Builds (ADD — the life and interactivity)
- Live activity feed (MiCity `/feed`)
- Quests system (MiCity `/quests`)
- Marketplace: goods + services + rides + post (MiCity `/marketplace/*`)
- Media creation: posts, audio, photos, streaming (MiCity `/media/*`)
- Care exchange / time banking (MiCity `/care/exchange`)
- Kids interactive: sandbox + vault + games (MiCity `/kids/*`)
- Peace table interactive flow (MiCity `/peace`)
- Wave / momentum / invite visualization (MiCity `/wave`)
- Cleanup / community event coordination (MiCity `/cleanup`)
- Live counters (Bldg `live-counters`)
- Celebration banners (Bldg `celebration-banner`)
- Activity feed real-time (Bldg `activity-feed`)
- Citizen card animated (Bldg `citizen-pass-card`)
- Circles browser (Bldg `circles-browser`)
- Petition/petition dashboard (Bldg `petition-dashboard`)
- Trust transparency display (Bldg `radical-trust-transparency-display`)
- PWA install prompt (Bldg `install-prompt`)
- Particle field ambient (MiLyfe-OS `ParticleField`)
- Dock/customizable nav (MiLyfe-OS `Dock`)
- Journey spatial view (MiLyfe-OS `/journey`)

## Features NEITHER Build Had (NEW — filling gaps)
- Customizable widget home layout (drag-drop)
- Visual standing garden/growth system
- Interactive lesson exercises (not just text)
- Contextual Mi (ambient, not panel-only)
- "Do something" quick actions on every screen
- Animated state transitions for $MLY movement
- Sound design (optional, subtle)
- Guest explorer with live energy visible
- Unified search across all content types (resources + marketplace + lessons + people + proposals)

---

# 13. Tech Stack: THE MERGE DECISION

**Keep Expo/React Native? Or switch to Next.js?**

**Decision: BOTH. Progressive Web App (Next.js) + Native (Capacitor) from same codebase.**

Why:
- Web is the internet door (SEO, instant access, no app store)
- Native feels better (animations, haptics, notifications)
- Same React components work in both via shared design system
- Services layer (41 services) is platform-agnostic — works in either

**Stack:**
- **Next.js 14** — web primary, SSR for SEO, edge functions
- **Capacitor** — same web code → native iOS/Android
- **Supabase** — database + auth + realtime + storage (free tier, self-hostable)
- **shadcn/ui + Radix** — accessible components (merge current design tokens)
- **Framer Motion** — animations that make it breathe
- **Zustand** — fast state (replaces React Context for real-time)
- **Canvas** — particle field, standing visualization, kid games
- **Tailwind** — styling (fast iteration)

**What migrates from current build:**
- All 41 services (TypeScript, platform-agnostic) → `src/services/`
- All type definitions → `src/types/`
- All test suites → `__tests__/`
- Theme tokens (colors, spacing, typography) → Tailwind config
- Learning content → `src/content/`
- Legal resources → `src/data/`

**What gets rebuilt with life:**
- Every screen (54 screens → interactive versions)
- All components (22 → alive versions with animation)
- Navigation (tabs → customizable dock)
- Home (static cards → living dashboard)

---

# 14. The Freedom Principle

Everyone doesn't have the same life. Everyone gets freedom of how the UI sets up for them.

**Layout customization levels:**
1. **Auto** — intelligent default based on your situation (parent? elder? reentry? youth?)
2. **Choose** — pick a preset ("Safety first" / "Learner" / "Shop owner" / "Community builder")
3. **Build** — full widget drag-drop. Put anything anywhere. Hide what you don't need.
4. **Save** — your layout syncs across devices. Private. Yours.

**Navigation customization:**
- Choose which tabs show in your bottom nav (max 5)
- Add shortcuts to your dock for frequent actions
- Reorder everything
- The five default areas (Pocket, Learn, Street, Voice, You) are always REACHABLE but don't have to be your PRIMARY tabs

**Content customization:**
- Choose your feed: All activity / Just my street / Just people I know / Just proposals
- Choose your quest categories: Cleanup / Verify / Care / Teach / All
- Choose your notifications: granular per type, not just on/off

---

*This is the design. Everything in it is alive. Everything in it is real. Everything in it is free. Review it and say go.*
