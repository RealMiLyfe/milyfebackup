# MiLyfe Platform Architecture (Internal Reference)

This is the CURRENT platform. Not the old MiJaxx/MiCity system. Everything here reflects the actual codebase at /home/milyfe/Documents/MiLyfe/milyfe-app/.

## What It Is

A local-first, offline-capable community lifestyle platform built with React Native/Expo. Data lives on the device. The server is optional for sync. Works via BLE, WiFi-Direct, LoRa mesh when no internet.

## Tech Stack

- Runtime: React Native + Expo (iOS, Android, Web)
- State: React Context + useReducer
- Persistence: AsyncStorage + SQLite (on-device)
- Messaging: Matrix protocol (Synapse, E2E encrypted)
- AI: On-device Ollama (llama3.2:3b) with pre-written fallbacks
- Auth: WebAuthn / Passkeys (no passwords)
- Mesh: BLE + WiFi-Direct + LoRa + DTN
- Backend: PostgreSQL, Temporal (workflows), OpenFGA (permissions)

## The 5 Tabs (User Sees)

1. **Today** — home overview, pulse, what matters right now
2. **Pocket** — money: weekly share, send thanks, jars, contributions
3. **Learn** — education paths: welcome → find your feet → craft → role → teach
4. **Street** — resources: food, shelter, help, rides, shops, classes, events
5. **Voice** — governance: proposals (idea → talk → try it → decide → what happened)

Plus: **You** (profile, safety, privacy, devices), **Keeper** (admin), **Youth** (child mode)

## Core Protocols (The Foundation Everything Shares)

### MiAction
Every consequential action wrapped in one envelope: actor, place, audience, state, approvals, consent, reversal, appeal, offline rule. State machine: draft → sent → walking → arrived → failed → expired.

### MiScope
Permission system (OpenFGA + OPA style). Answers "can this person do this thing in this context?" Enforces: child safety, emergency exceptions, stage-gating, required approvals.

### MiWalk
Offline-first money and actions. Reservation-based double-spend prevention. Critical rule: money, guardianship, moderation, and ballots ALWAYS require human review on conflict — system never auto-resolves these.

### MiReceipt
Human-readable proof of every action. What happened, who saw it, can it be undone, how to appeal. Ballot receipts prove participation but NOT choice (secret ballot preserved).

### MiStage
Practice ("credits") vs Live (real value). Hard boundary at service layer. Practice can NEVER become live. Live requires: legal counsel, security audit, community vote, 100+ members.

## Economy ($MLY)

- Unit: $MLY ("shares" or "credits")
- Weekly Share (UBI): 100 $MLY/week to every personhood-verified human. Same for all. Cannot be taken away.
- Thanks: Peer-to-peer payments
- Jars: Shared community pots with N-of-M approval
- Contribution cap: 200 $MLY/week max beyond UBI
- No founder cut. No APY. No exchange. No investment.
- "Issuance is a faucet with a heartbeat, not a market maker."

## Standing (Reputation)

NOT a social credit score. Cannot take: profile, voice, weekly share, messages, emergency help.

- 8 Facets: Neighbor, Carer, Maker, Teacher, Keeper, Voice, Shop, Helper
- Levels: new → growing (3+) → active (10+) → established (20+)
- Based on peer attestations ("that happened"), not algorithms
- Decays over time (halves every 6 months — forgiveness built in)
- Portable facets (Carer, Maker, Teacher) travel when you move
- Local facets (Neighbor, Keeper, Voice, Shop) reset when you move
- Scars: only from closed due process, fade in 18 months

## Governance (Voice)

Pipeline: Idea → Talk (14 days) → Try it first → Decide (secret ballot) → What happened
- Every decision has a sunset (6 months default)
- Helper-drafted proposals need human second
- Helper voting weight: 0% default, 5% cap
- Liquid democracy (delegated voice, instantly revocable)
- Edits restart the affected stage

## Safety

- Leave-now: actually freezes jars, hides location, removes devices
- Walking-home timer with contact alerts
- Quick-exit: clears screen (honest about what it can't clear)
- Rights cards: downloadable, jurisdiction-specific
- Shared device mode with session timeout

## Mi (The Helper)

- Always labeled as helper, never pretends to be human
- Specialized: Nia (money), Rue (safety), Bea (learning)
- Cannot: send money, vote, publish, change safety settings alone
- Cannot: access health/child/legal files without open human ticket
- Always offers "Ask a person" for consequential decisions
- Uses MiPlain language (banned: blockchain, wallet, DID, token, agent, node)

## Places and Jurisdiction

- Each place = geographic community with its own law pack
- Law packs add duties, never remove rights
- Stricter jurisdiction wins
- Feature flags per place (shares enabled, binding votes, helper chorus cap, etc.)
- First place: Riverside, Jacksonville. Stage: credits (practice).

## Identity and Membership

Progression: Visitor → Neighbor → Member → Citizen (of the commons, not a nation)
Personhood ladder: none → pending → local-intro → hello-day → id-check → privacy-proof → complete
Recovery: 2-of-3 key splitting with recovery friends (not passwords)
