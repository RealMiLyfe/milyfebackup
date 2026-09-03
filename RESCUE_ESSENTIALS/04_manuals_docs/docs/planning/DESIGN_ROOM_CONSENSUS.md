# MiLyfe — National Design Room Consensus

**Date:** August 21, 2026
**Present:** Every stakeholder in the United States — represented by role, need, and expertise.
**Purpose:** Design the optimal platform architecture that scales itself.

---

## THE ROOM

### Citizens (330 million voices distilled)

**Maria, single mom in Jacksonville** — "I need to open this on my phone at 6 AM, find food for my kids, check if my court date moved, and get out. No tutorial. No signup that takes 10 minutes. Useful in 60 seconds or I'm gone."

**DeShawn, 23, just released from county** — "I need my ID situation, a job today, and to not miss my PO date. Don't make me learn a whole system. Tell me what to do FIRST."

**Gloria, 74, arthritis, lives alone** — "Make the words big. Let me check in so my daughter knows I'm okay. Don't track me without asking."

**James, owns a barbershop** — "I'll accept your credits if my customers have them. Don't make the register complicated. I don't have time for a whole POS system."

**Keisha, DV survivor** — "If my ex can find me through this app I will never forgive you. One tap to disappear. No notification that tells him I left."

**Marcus, street leader in Riverside** — "Pay me for peace, not for territory. I'll keep the block quiet if the system actually pays out."

**Officer Daniels, JSO** — "I don't want this. But if it reduces my calls, fine. Don't pretend to be the police. Don't interfere with lawful process."

**Council Member Torres** — "Show me the data. If this reduces 911 calls and doesn't cost the city money, I'll back it publicly."

**Pastor Williams, Northside church** — "My people need this. But if you make it feel like the government is watching, nobody will touch it."

---

### Technical Team (The Builders)

**Systems Architect** — "One runtime. One database. One auth. One deployment. Stop splitting across 5 builds."

**Frontend Lead** — "Next.js 14. Server components for speed. Client components for interactivity. PWA for offline. One codebase ships web + mobile."

**Backend Lead** — "Supabase for auth + realtime + storage. Edge functions for logic. PostgreSQL Row Level Security for privacy. No custom auth system — it always breaks."

**DevOps** — "Vercel for web. GitHub Actions for CI. Supabase Cloud to start, self-host when we hit scale. Total cost: $0 until 50K users."

**Security Engineer** — "RLS on every table. No admin backdoor. Encryption at rest. Service role key NEVER in the client. Env vars on the server only."

**AI/ML Engineer** — "Ollama for local Mi. OpenRouter as fallback. System prompts per helper personality. NEVER let the model spend money, publish content, or change safety settings."

**Accessibility Lead** — "44px touch targets. Atkinson Hyperlegible. WCAG 2.2 AA minimum. Screen reader testing before EVERY deploy. RTL ready. If Gloria can't use it, we failed."

**Mobile Engineer** — "PWA first — installable, offline-capable, push notifications via Web Push. Capacitor for native wrapper later. Same codebase."

---

### Product Designers

**UX Lead** — "Five tabs. Home is the landing. Everything lives under Pocket/Learn/Street/Voice/You. Mi floats. NO module explosion. NO settings hell. The grandmother test decides everything."

**Visual Designer** — "Deep Harbor navy for trust. Living Teal for community. $MLY Gold for money. Paper white background 70% of the time. The gradient is reserved for the logo and moments of celebration. Dark mode breathes — it's not inverted, it's designed."

**Content Designer** — "Every word is plain language. If you can't say it to a person on the street in one breath, rewrite it. 'Your share arrived' not 'UBI emission finalized.' Banned word list enforced in CI."

**Interaction Designer** — "Something moves on every screen. Something you can DO on every screen. Context visible at all times (time, place, balance, connection). Speed: <1 second every page. Skeletons before content."

---

## THE CONSENSUS

After hearing every voice, here is what the room agreed on:

---

## 1. ONE APP. ONE STACK. ONE TRUTH.

No more 5 builds. One fresh Next.js 14 app. One Supabase project. One deployment.

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                       │
│  Next.js 14 (App Router) + TypeScript + Tailwind │
│  Framer Motion + Zustand + Lucide + Canvas       │
│  PWA (offline, installable, push notifications)  │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│                   BACKEND                        │
│  Supabase: Postgres + Auth + Realtime + Storage  │
│  Edge Functions (Deno) for server logic          │
│  Ollama (local) or OpenRouter (fallback) for Mi  │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│                INFRASTRUCTURE                    │
│  Vercel (free tier) → K3s when scaling          │
│  GitHub Actions (CI/CD + accessibility gate)     │
│  Cloudflare (DNS + R2 for media)                │
│  Total cost to operate: $0                       │
└─────────────────────────────────────────────────┘
```

**Why Supabase won the room:**
- Auth works cross-device out of the box (we PROVED this — user signed in successfully)
- Realtime WebSocket subscriptions for live feed
- Row Level Security means the database enforces privacy, not the app code
- Free tier: 500MB DB, 50K monthly active users, 2GB storage
- Self-hostable when ready
- The publishable key (`sb_publishable_...`) works for auth — CONFIRMED in this session

**Why not localStorage:**
- Maria has a phone AND a library computer. Her data must be on BOTH.
- DeShawn's phone might get stolen. His profile must survive.
- Gloria's grandson set her up on his tablet. She bought her own phone later. Same account.

---

## 2. AUTH THAT NEVER FAILS

The room's consensus on auth (the #1 thing that blocks everything):

```
SIGNUP:     Email + Password (simple, everyone understands)
ALSO:       Magic link (for people who forget passwords)
ALSO:       Passkeys/WebAuthn (for power users, one-tap login)
SESSIONS:   Supabase cookies (SSR-safe, cross-device)
MIDDLEWARE: Refreshes token on every request (already built: middleware.ts)
CALLBACK:   /auth/callback route for magic links (already built)
FALLBACK:   If Supabase is unreachable, show cached data with "sync when online" banner
```

**What the room rejected:**
- localStorage-only auth (single device = broken)
- Custom password hashing (we're not a security company)
- Any auth that requires a database password we can't auto-provision

**What's already proven working:**
- `sb_publishable_WXgf0Mdvw93AGTcW7nDB8w_oH0P5OYn` — signs up users ✓
- `sb_secret_UoVf5_0HICz6q03yIDu8DA_-lDbMgS4` — admin operations (confirm users, reset passwords) ✓
- User created: `carnell@milyfe.fun` / password reset and sign-in confirmed ✓

---

## 3. THE DATABASE (What Lives in Supabase)

The room designed one schema that serves all 330 million:

```sql
-- Auth (automatic via Supabase)
auth.users → email, password, metadata (name, place)

-- Core tables (with Row Level Security)
profiles         → name, avatar, place, standing facets, personhood
transactions     → from_id, to_id, amount, type, status, memo
jars             → owner, name, balance, goal, members, approvals
activity_feed    → event_type, title, actor, place, anonymous flag
proposals        → title, stage, votes, sunset, circle
circles          → name, type, members, treasury
quests           → title, type, reward, status, claimed_by
marketplace      → title, category, price, author, status
messages         → thread, from, to, text, read status
resources        → name, category, phone, hours, verified date
learn_progress   → user, path, lesson, progress percentage
```

**RLS Rules (privacy enforced at database level):**
- You can only read YOUR transactions (from or to you)
- You can only read YOUR messages (you're a participant)
- Profiles are visible to authenticated users (name + standing only)
- Activity feed is readable by all authenticated users (it's the heartbeat)
- Quests/marketplace/resources are public to all members

**Realtime subscriptions (live updates via WebSocket):**
- `activity_feed` — new events appear instantly
- `transactions` — balance updates in real time
- `messages` — chat is live

---

## 4. THE FIVE TABS (Agreed by everyone)

```
┌─────┬─────┬─────┬─────┬─────┐
│  💰 │  📚 │  🏘️ │  🗳️ │  👤 │
│Pocket│Learn│Street│Voice│ You │
└─────┴─────┴─────┴─────┴─────┘
          + Mi (floating helper)
```

**What each tab MUST do on Day 1:**

### POCKET (Maria needs this)
- See balance (big number, animated)
- Receive weekly 100 $MLY (Saturday)
- Send thanks (pick a person, amount, memo)
- See transaction history (sentence-based: "You thanked Mara 12 for watching the kids")
- Create a jar (goal + name + save into it)
- Freeze (one tap for safety)

### LEARN (DeShawn needs this)
- See 10 paths (titles, progress, estimated time)
- Open a lesson (real content, not placeholder)
- Complete a lesson (progress saves, badge at end)
- Download for offline (Service Worker caches it)
- Audio read-aloud (Web Speech API)

### STREET (James needs this)
- See marketplace posts (food, services, rides, goods, education, housing, jobs)
- Post something in 10 seconds (category + title + price type + post)
- Claim something ("I want this" → coordinates in messages)
- See quests (community tasks with $MLY rewards)
- Claim + complete quests (standing grows)
- See verified resources (phone numbers, hours, freshness dates)

### VOICE (Council Member Torres needs this)
- See active proposals with stages (Idea → Talk → Try → Decide → What happened)
- Create a proposal (title, description, cost, who's affected, sunset date)
- Vote (private ballot, one person one vote, equal weight)
- Delegate voice (topic-specific, time-limited, instantly revocable)
- See circles (join, treasury, steward)

### YOU (Keisha needs this)
- Profile (name, place, avatar)
- Standing (8 facets shown visually — not a score, growth)
- Privacy controls (who sees what — enforced at database level)
- Safety (one tap → leave-now, walking-home, freeze, rights card)
- Export (download all your data as JSON, works even during disputes)
- Sign out / Leave MiLyfe (take everything and go)

### MI (Gloria needs this)
- Floating button, one tap from anywhere
- "What should I do today?" → context-aware suggestions
- "Find food near me" → pulls from resources + marketplace
- "I have a court date" → pulls from legal resources, adds to calendar
- Always labeled "a helper, not a person"
- "I need a real person" → escalation path

---

## 5. SCALING ITSELF (The Architecture That Grows)

The room's consensus on self-scaling:

**Principle:** The platform scales by people using it, not by engineers deploying it.

```
1 PERSON     → localStorage works fine for demo
10 PEOPLE    → Supabase free tier handles everything
1,000 PEOPLE → Supabase free tier still handles it
50,000 MAU   → Supabase free tier STILL handles it (their stated limit)
100,000+     → Self-host Supabase on K3s ($20/month VPS)
1,000,000+   → Managed Postgres + CDN + Edge functions
```

**What scales automatically:**
- Vercel: scales to millions of requests (serverless, auto-scaling)
- Supabase: connection pooling, read replicas when needed
- Cloudflare R2: unlimited bandwidth for media
- Realtime: Supabase handles WebSocket connections at scale
- Edge Functions: run in every region, <50ms latency globally

**What scales by community:**
- Content: users post marketplace items, users complete quests, users verify resources
- Education: teachers create classes, learners confirm attendance
- Governance: proposals come from members, votes come from members
- Safety: defense circles are 5-12 neighbors, not a central team
- Economy: $MLY circulates because people thank each other

**No human bottleneck for growth:**
- Signup is open (no wave codes, no approval needed)
- UBI is automatic (Saturday delivery, no admin action)
- Quests are community-created (propose → keeper approves → live)
- Standing grows from real actions (no admin can give or take it)
- Proposals follow the pipeline (no gatekeeper)
- Resources are community-verified (anyone can report inaccurate info)

---

## 6. WHAT GETS BUILT FIRST (The Room's Priority Order)

Everyone agreed: **build what saves a life, then what feeds a family, then what grows a community.**

### Sprint 1: EXIST (1 week)
- [ ] Fresh Next.js 14 app (clean repo, no old code)
- [ ] Supabase wired (auth + database + realtime)
- [ ] Signup works on any device
- [ ] Login works on any device (magic link + password)
- [ ] One page loads after login (Home with greeting)
- [ ] Deploy to Vercel (live URL, anyone can reach it)
- [ ] **TEST: Maria signs up on her phone, logs in on library computer. Same account.**

### Sprint 2: SAFE (1 week)
- [ ] Leave-now works (freeze + hide + show shelters)
- [ ] Walking-home timer works (countdown + alert)
- [ ] Rights card exists (printable, offline)
- [ ] Quick exit works (neutral page, one tap)
- [ ] Crisis numbers always visible (988, Hubbard House, 911)
- [ ] **TEST: Keisha hits leave-now. Her ex cannot find her through the platform.**

### Sprint 3: EARN (1 week)
- [ ] Balance shows (real number from Supabase)
- [ ] Weekly 100 $MLY arrives Saturday (Edge Function cron)
- [ ] Send thanks works (pick person, amount, memo)
- [ ] Transaction history shows (sentence-based)
- [ ] Jars work (create, save into, progress bar)
- [ ] **TEST: DeShawn signs up Monday, gets 500 welcome + 100 Saturday = 600 $MLY by end of week.**

### Sprint 4: FIND (1 week)
- [ ] Marketplace shows posts (7 categories)
- [ ] Post in 10 seconds (category + title + price + done)
- [ ] Claim works ("I want this" → message thread)
- [ ] Resources show (phone, hours, freshness dates)
- [ ] Quests show (community tasks with rewards)
- [ ] **TEST: James posts "haircut 15 $MLY." Marcus claims it. They coordinate in messages.**

### Sprint 5: LEARN (1 week)
- [ ] 10 paths show (titles, progress)
- [ ] Lessons load (real content for Path 1: Know Your Rights)
- [ ] Progress saves (complete a lesson → bar grows)
- [ ] Offline works (Service Worker caches lessons)
- [ ] **TEST: DeShawn does Lesson 1 on the bus with no signal. Progress is there when he gets home.**

### Sprint 6: GOVERN (1 week)
- [ ] Proposals show (5 stages visible)
- [ ] Create a proposal works (form → saved → appears for others)
- [ ] Vote works (private ballot, equal weight)
- [ ] Circles show (join, treasury)
- [ ] **TEST: Pastor Williams proposes "shade at bus stop." 15 people vote. It passes. Pot funds it.**

### Sprint 7: BREATHE (1 week)
- [ ] Live feed (realtime events appearing)
- [ ] Live counters (members, $MLY circulating, quests today)
- [ ] Particle field (ambient canvas, responds to activity)
- [ ] Celebrations (credits arrive = green pulse, quest done = confetti)
- [ ] Mi helper (contextual, scripted, honest about limits)
- [ ] **TEST: Gloria opens the app and sees things MOVING. It feels alive. She taps Mi and says "check on me at 10 AM."**

### Sprint 8: EVERYONE (1 week)
- [ ] Shop profiles (accept $MLY, surplus, hours)
- [ ] Youth mode (no money, no adult DMs, games)
- [ ] Elder mode (large text, simple nav, check-ins)
- [ ] Music/Listen (community radio player)
- [ ] Search (your data → place → commons)
- [ ] **TEST: The whole room can use it. Grandmother. Teenager. Shop owner. Just-released. Council member.**

---

## 7. THE SELF-SCALING RULES (Why It Grows Without Us)

1. **Every action feeds the feed.** Thank someone → event appears. Post surplus → event appears. Complete quest → event appears. The app gets more alive as more people use it.

2. **Every person gets $MLY.** Signing up guarantees value (500 welcome + 100/week). This means every new user brings purchasing power. Shops accept because customers have credits.

3. **Every problem becomes a quest.** Trash on the block? Quest. Pantry hours unknown? Quest. Elder needs a check-in? Quest. The community self-heals through incentivized tasks.

4. **Every rule has a sunset.** Nothing is permanent except the 23 Oath principles. Bad proposals die automatically. Expired quests archive. Stale resources show their age.

5. **Every person can teach.** Host a class → earn teacher standing. Knowledge multiplies. The platform gets smarter as people teach.

6. **Every shop brings customers.** A shop accepting $MLY is a reason for people to earn. More shops = more reason to participate = more people = more shops.

7. **Every neighborhood is autonomous.** Circles govern themselves. A proposal in Riverside doesn't need approval from Northside. Scale is fractal, not centralized.

8. **The code is open.** Any city can fork it. Any community can run their own. The protocol spreads by being useful, not by marketing.

---

## 8. WHAT THE ROOM REJECTED

- ❌ Wave codes / invite gates (people should join freely)
- ❌ Blockchain on Day 1 (PostgreSQL does everything needed; chain comes later IF voted)
- ❌ Multiple codebases (one app, one deployment, one truth)
- ❌ Custom auth (Supabase Auth, period — it works, we proved it)
- ❌ Admin dashboards before user flows (build what people use first)
- ❌ AI that acts alone (Mi suggests, humans decide)
- ❌ Engagement tricks (no streaks, no "people waiting for you," no FOMO)
- ❌ "Practice" mode (credits are real from day one)
- ❌ Complex onboarding (name + email + password + place = done)
- ❌ Module explosion (5 tabs + Mi, nothing else on the main nav)

---

## 9. SUCCESS METRICS (How We Know It Worked)

| Metric | Meaning | Target |
|--------|---------|--------|
| Time to first value | Signup → something useful | < 60 seconds |
| Cross-device login | Works on phone + laptop | 100% |
| Weekly UBI delivery | Credits arrive Saturday | 100% reliability |
| Safety response time | Leave-now → fully hidden | < 5 seconds |
| Community self-creation | Posts, quests, classes without admin | > 90% user-generated |
| Shop acceptance | Local businesses taking $MLY | 1 in first month |
| Proposal passed | Real decision executed by community | 1 in first month |
| Offline capability | Core features without internet | Learn + Safety + Cached balance |
| Grandmother test | Gloria can read every screen aloud | 100% pass |
| 911 calls from users | Reduced need for emergency services | Measurable decrease |

---

## 10. THE DECLARATION

Every person in this room — the single mom, the returning citizen, the elder, the shop owner, the survivor, the street leader, the officer, the council member, the pastor, the architect, the designer, the engineer — agrees:

**Build the thing that works on a Tuesday. Ship it. Let people use it. Let the community grow it. Stop talking. Start building.**

---

*Signed by the room. August 21, 2026.*
*One app. One stack. One truth. 330 million people. $0.*
*The house is ready. Open the door.*
