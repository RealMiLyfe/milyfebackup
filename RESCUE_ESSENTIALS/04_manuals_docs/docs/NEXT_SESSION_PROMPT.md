# MiLyfe Platform — Next Session Prompt

Paste this to continue:

---

Continue building MiLyfe Platform.

**Live:** https://milyfe-platform.vercel.app  
**Repo:** /home/milyfe/Documents/MiLyfe/milyfe-platform  
**GitHub:** https://github.com/RealMiLyfe/MiLyfe-Platform  
**Stack:** Next.js 14 + Supabase + Tailwind + MapLibre + Recharts + Dexie + Upstash + Sentry + PostHog  
**Domain:** milyfe.fun (not yet pointed to Vercel)

## Current State

96 compiled routes. 145 Supabase tables. 125 course modules. Deployed and live.  
Responsive 3-zone layout (sidebar + content + right panel for desktop).  
Bilingual (EN/ES). PWA with push notifications + offline queue.  
Mi AI with 6 specialized agents + RAG + function calling.

## What Was Done This Session

Built all 5 expansion phases (0-5):
- Phase 0: DB migration (50+ tables), notifications, background jobs, content moderation, distributed rate limiting, standing enforcement, analytics, voice→AI integration
- Phase 1: Emergency broadcast, accountability system, transparency dashboards, interactive constitution, community recordings, 25 real courses (125 modules), wiki, gamification, tokenomics
- Phase 2: MiForum (reddit-style), MiSocial (feed/stories/reels), MiNews, voice/video calls (WebRTC), MiAcademia
- Phase 3: MiMarket (unified marketplace), MiCity GitHub-style civic ops, MiNav (MapLibre + JTA transit), MiAuto
- Phase 4+5: AI expansion (agents + RAG + functions), Dev Portal, Digital Twin (DiceBear avatars), media pipeline, privacy/GDPR, infrastructure (Redis/flags/health), PWA, ActivityPub federation, accessibility
- Gap fixes: Updated navigation, JTA Transitland integration, WebRTC signaling, forum detail page, social profile page, MapLibre interactive map, push SW handler, ActivityPub inbox/outbox, admin dashboard, onboarding expansion, background sync
- Responsive shell: Desktop sidebar, right context panel, 3-zone layout

## What's NOT Done — The Deep Build

The platform has 96 routes but most are SURFACE-LEVEL (single page with a form). They need production depth — multiple sub-pages, real workflows, loading states, error handling, empty states, validation, pagination, and state persistence.

### Priority Build Order:

**1. Add MiHome app** (NOT redesign /home — ADD a new /mihome route for actual home/living management: smart home integration, home maintenance, household management, roommate coordination, home security, utilities tracking, home improvement projects)

**2. Media Network Expansion:**
- MiTV (live streaming, channels, scheduling, DVR, live chat, tips)
- MiBlog (rich text editor, series, newsletter, comments)
- MiVlog (daily video format)
- Podcast hosting (RSS generation, analytics)
- Radio DJ system (scheduling, requests, genres)
- Creator analytics dashboard

**3. Build 7 Detail Pages:**
- /learn/[id] — course viewer with module navigation
- /forum/[slug]/[id] — post detail + nested comments
- /news/[id] — article detail + discussion
- /market/[id] — listing detail + purchase flow
- /social/[id] — other user's profile
- /auto/[id] — vehicle detail
- /academia/[id] — project detail

**4. Build 10 Financial Services (Phase A — no filings, no permission):**
- Savings circles (tandas)
- Peer micro-lending
- Emergency fund + committee
- Bill splitting
- Will/POA template builder
- Community credit score
- Health sharing pool
- Risk sharing pool
- Predatory lender database
- Financial coaching

**5. Build 10 Population Services:**
- /reentry (formerly incarcerated)
- /shelter (unhoused)
- /elders (aging/isolated)
- /youth (foster youth aging out)
- /safety-mode (DV/trafficking survivors)
- /recovery (addiction)
- /veterans
- /access (disability)
- /immigrant
- /parents (single parents)

**6. Deepen ALL existing features** to production quality (see Deep Build Plan for full list of what each feature is missing)

**7. Set Vercel env vars:** GROQ_API_KEY, UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN, QSTASH_TOKEN, RESEND_API_KEY, VAPID keys, SENTRY_DSN, POSTHOG_KEY

## Critical Design Principles

- **No Stripe. No corporate payment processors.** $MLY is earned through participation, exchanged peer-to-peer. The community IS the financial system.
- **No filing paperwork. No asking permission.** Voluntary mutual aid between consenting adults, protected by the U.S. Constitution (1st, 9th, 10th, 14th amendments).
- **Everything open-source.** No proprietary dependencies.
- **Every feature must have:** loading skeletons, error handling, empty states, validation, mobile+tablet+desktop layouts, $MLY integration, standing impact, notification triggers.
- **The standard:** Each feature should feel like a full app (3+ sub-pages, real workflows), not a demo page.

## Reference Documents (READ THESE FIRST)

All at /home/milyfe/Documents/MiLyfe/:

1. **MiLyfe_DEEP_BUILD_PLAN.md** — The 87-item remaining work list with depth requirements for every feature
2. **MiLyfe_Community_Services_Design.md** — Health sharing, risk sharing, trusts, banking, credit (the financial services design)
3. **MiLyfe_Repos_and_People_Services.md** — 30 repos needed + 10 underserved population services with full details
4. **MiLyfe_Expansion_Design.md** — Original expansion design (phases, architecture, decision points)
5. **MiLyfe_COMPLETE_STATUS.md** — Full inventory of what exists and what doesn't

## Supabase Access

- Project: zoallvovubchvxllglbs
- Supabase CLI is linked and authenticated
- DB queries work via: `npx supabase db query --linked "SQL HERE"`
- Access token saved at ~/.config/supabase/access-token

## Build & Deploy

```bash
cd /home/milyfe/Documents/MiLyfe/milyfe-platform
npx next build  # verify
git add -A && git commit -m "message" && git push origin main  # auto-deploys to Vercel
```

---

[Then tell the agent what to build first]
