# MiLyfe — Master Build Roadmap (The Fractal of Fractals, in Phases)

**One roadmap that gathers every design and gap we've produced** — the live platform,
MiJustice, the media/Vibe player, the economy (contributions/rewards/treasury), the
shell/header/right-rail UX, and the trust-and-coordination layer — into a single phased
plan. No code here; this is the map.

## Non-negotiable constraints (apply to every phase)
- **No payment processors, ever.** No Stripe/PayPal/any gateway. $MLY is internal, earned
  through participation, moved peer-to-peer via the wallet + community treasury.
- **No ads, ever.** No banner/audio/video ads, no AdSense/AdMob, no paid boosts, no
  sponsored listings. "Boost/feature" mechanics, if any, use $MLY only.
- **No dark theme.** Light MiLyfe design language everywhere (white/glass surfaces, teal
  primary, gold `mly` accent, harbor text, `rounded-xl`, `animate-fade-in`).
- **Free & open-source, self-hostable, offline-capable, accessible (WCAG 2.2 AA), multilingual + RTL.**
- **Guardrails first** for anything touching law, money, safety, or minors: human review
  gates, receipts, consent, appeal paths.

## The fractal (why this holds together)
The whole platform is one loop repeated at every zoom level: **create → share → discover →
transact (in $MLY) → govern → account**, wrapped in **consent + receipt + appeal**. Each
surface (Learn, Street, Media, Voice, Justice, Care, Pocket) is a smaller copy of the whole;
each object (a track, course, listing, case, post) repeats it again. The job of this roadmap
is to bring every surface to the same depth and tie them together with one identity, one
wallet, one standing, one Mi, one consent graph.

---

## Where we are today (baseline — already built)
- ~45 route surfaces: Home dashboard, Pocket/Wallet (3 pots + transfers), Learn (paths→modules),
  Street (marketplace/quests/surplus), Voice/Governance (proposals+votes), Mi assistant,
  Connect (chat), Forum, News, Health, Safety (journal + walk-home timer + leave-now),
  Standing (8 facets + decay), Rewards, Treasury (public ledger), Transparency, Wiki, Profile,
  Apps, Bounties.
- **Economy engines live:** weekly UBI (100 $MLY) + welcome grant (50), daily standing decay
  (1%), treasury ledger, quest/proposal/attestation/mastery rewards. All atomic, audited.
- **MiJustice suite shipped** (branch `feat/mijustice-phase1`, PR #13): public tier (landing,
  Know Your Rights, Constitution) + gated tier (Encounter Mode, Defender, case workspace,
  ICE shield, class actions, liberation, expungement, knowledge, coalition, pressure, tracker,
  board review) + self-healing AI fleet + guardrails.
- **Shell upgraded this session:** desktop header (search pill, $MLY chip, quick-create, Mi,
  bell, avatar) + contextual right rail + three-column layout.
- **Security/enterprise baseline:** Next 16/React 19, audit logging, RLS everywhere, rate
  limiting, secret-scan, observability, CI.

---

# THE PHASES

Each phase lists **what ships**, the **surfaces touched**, and **new OSS frameworks** likely
needed. Phases are ordered so trust/economy foundations land before the things that depend on
them, and so the biggest engagement driver (Media) lands once its guardrails exist.

---

## PHASE 0 — Trust & Coordination Foundation *(before scaling anything with money/law/safety)*
The layer no existing product provides; everything else rides on it.
- **MiAction** — one action envelope (actor, role, audience, purpose, consent, draft/sent/
  walking/arrived state, approvals, expiry, reversal, appeal, offline rule, plain-English why).
- **MiScope** — relationship/permission/consent graph (household, guardian, care, delegation,
  attorney, temporary roles; "what can this person see?" preview; revocable).
- **MiReceipt** — human-readable proof for every consequential action (what happened, what
  didn't, who can see it, can it be undone, when it expires, how to appeal).
- **Canonical object + role/permission matrix** filled (Person, Place, Household, Role,
  Consent, Source, Resource, Message, Action, Receipt, Case, Appeal, Jar, Proposal, Ballot,
  Story, Item, Device, Export).
- **Sybil/identity depth** — verification ladder (auto / peer-attested / steward-reviewed) so
  UBI + rewards can't be farmed. This is the #1 economic risk; fix before scale.
- **Frameworks:** OpenFGA (relationships) + OPA/Conftest (policy), Temporal (durable action
  workflows), CloudEvents (envelope), Keycloak + WebAuthn/passkeys (identity/session),
  TrustBloc VCS + in-toto/Cosign (receipts/attestations).

## PHASE 1 — Economy Deepening: Contributions ↔ Rewards ↔ Treasury (the governed loop)
Connective tissue for the economy that already exists.
- **`/contributions` — "Your Impact" hub** (new): the 8 standing facets as a live actionable
  board, a receipted contribution feed, and a "ways to contribute / earn" grid. Makes decay
  actionable, not punishing.
- **Rewards → engine:** three zones (Claim with celebration animation / Earn menu / History),
  streaks + gentle multipliers, milestone badges, transparent governed reward values.
- **Treasury → living public bank:** runway/health gauge (weeks of UBI funded), inflow-vs-
  outflow chart, allocation breakdown, per-facet payout view; new no-ads inflows (premium-
  content $MLY share, unclaimed-reward reclamation, decay sink, voluntary commons tithe).
- **Governed loop:** Treasury parameter changes (UBI amount, reward values, fees, community
  spending) become proposals in **Voice**, enacted from Treasury, logged in the ledger.
- **Anti-abuse + dispute/appeal:** no self-dealing / circular attestation / spam-contribution;
  fair appeal via MiAppeal.
- **Right-rail economy mini-card** platform-wide (your $MLY + standing + streak + "1 reward to claim").
- **Frameworks:** builds on Phase 0 (OPA rules, receipts); recharts (already in) for gauges.

## PHASE 2 — Media Vertical + the Persistent "Vibe Bar" *(the shine)*
The biggest engagement + contribution engine. Audio + Video + Live + Radio, ad-free, $MLY-only.
- **Global Vibe Bar player:** docks into the shell (bottom of content column on desktop, above
  bottom-nav on mobile), glass + on-brand; collapsed bar + expanded "Now Playing"; video
  shrinks to a mini/PiP thumbnail and keeps playing across every surface; resume-from-position,
  queue, waveform, offline downloads, keyboard + reduced-motion support.
- **Media Home** (bento dashboard): continue-listening, featured Station, trending, live now,
  radio "on air" mini-card, genre chips.
- **Audio (RKHM face):** artist/album/track/playlist pages, "Station" auto-queue, collaborative
  playlists, browse filters.
- **Video (PlayTube face):** videos + **Shorts** (vertical swipe mode) + long-form, channels,
  subscriptions, watch history/later, privacy modes, age gate, creator Studio analytics.
- **Live + Radio (OnAir2 face):** go-live with live chat (reuse Connect chat), non-stop radio
  player, **show schedule** ("Now On Air / Coming Next"), listener-voted charts, podcast series.
- **Creator flow:** upload wizard → metadata → publish; earnings via $MLY tips + optional
  $MLY-priced premium + royalty-by-engagement pool from treasury. No ads. No processor.
- **Frameworks:** FFmpeg (transcode/waveform/thumbnails), HLS.js + Shaka (adaptive playback),
  Vidstack/Plyr (player UI), WaveSurfer.js (waveforms), LiveKit or Owncast (live/radio),
  BullMQ (transcode/import jobs), Uppy (chunked uploads), S3-compatible storage.

## PHASE 3 — Social & Content Depth (the Connect/Forum/News/Profile face)
Bring social to reference-platform depth, ad-free.
- **Newsfeed:** composer, **Stories/Reels strip** ("add yours"), multi-image slider, post-action
  menu (edit/delete/report/pin/feature/schedule), rich reactions, threaded comments with
  reply-level likes, saved posts, hashtags/trending, memories.
- **Rich profile shell:** tabbed (Timeline/About/Friends/Photos/Videos/Groups/Analytics),
  "complete your profile," verification badges, multi-account switching.
- **Groups / Pages / Events:** group types (public/private/hidden) + group chat, pages with
  reviews, **events + calendar** (going/interested, countdowns, maps), birthdays.
- **Long-form (MiBlog):** WYSIWYG, series, newsletter, cross-post to forum.
- **Reddit-style + Q&A** discovery surfaces.
- **Nearby discovery / people suggestions / who-to-follow.**
- **Frameworks:** Tiptap (composer/blog/rich posts), Uppy (media), Supabase Realtime (feeds),
  MapLibre (already in) for events/nearby.

## PHASE 4 — Learn → full LMS (WPLMS face)
- **Assessments:** 8 question types, question bank, timed quizzes, retakes, auto + manual
  grading, practice quizzes; **assignments** (upload → review → graded return).
- **Certificates & badges** (unique validation codes, PDF download from profile).
- **Structure:** prerequisites, drip release, expiration, announcements; **cohorts/batches**
  (start/end, attendance), leaderboards, streaks/XP.
- **Instructor tools:** front-end course builder, gradebook, per-student performance,
  verification workflow. **Learner:** progress, notes, "ask instructor," bookmarks, reviews.
- **Interactive + live:** SCORM/xAPI/H5P; live classes (Jitsi/BBB) with the shared chat panel.
- **AI:** question generator into the bank (behind guardrails).
- **Frameworks:** H5P + scorm-again (xAPI/SCORM), BigBlueButton/Jitsi (live class),
  Tiptap (authoring), React-PDF/pdf-lib (certificates).

## PHASE 5 — Commerce & Services Depth (Street → eMart-class, $MLY-only)
- **Catalog:** products with variants/attributes, categories, reviews/ratings, detail pages;
  digital-goods store (sell files/licenses in $MLY).
- **Cart & orders:** persistent multi-item cart, cart drawer, scheduled orders, multiple saved
  addresses, order history, reorder, refunds.
- **Vendor surface:** store pages + dashboard (order lifecycle, prep time, catalog CRUD, bulk
  import), store QR, employee management, POS.
- **Fulfillment/logistics:** real-time order/delivery tracking on a MapLibre map, courier flow,
  zone management, status lifecycle.
- **Service verticals** as configurable "sections" (on-demand services booking, parcel, rides/
  rental) — each with its own flow, all $MLY, wallet payouts, coupons, referral rewards. **No
  sponsored listings.**
- **Frameworks:** MapLibre + OSM/Nominatim + OSRM/Valhalla (maps/geocoding/routing), Medusa
  (optional headless commerce engine reference), Uppy (product media), Supabase Realtime (tracking).

## PHASE 6 — Cross-Cutting Depth (applies to all surfaces)
- **Notifications:** granular per-event prefs + web push (PWA) + native push; privacy-aware
  routing (neutral previews on shared devices).
- **Realtime chat depth:** group chats, item-sharing into DMs, media messages, reply-to, read
  receipts, typing, voice notes, (later) audio/video calls (self-hosted WebRTC/LiveKit).
- **Universal comment/like/report** on every object with replies + moderation.
- **Search & discovery:** unified cross-vertical index with filters + ranking (Meilisearch/Typesense).
- **Events & Maps as shared primitives** used by Learn cohorts, Live shows, commerce, safety.
- **PWA/offline depth:** install prompts, shortcuts, background sync, share-target, offline content.
- **Moderation/admin depth:** scoped moderators, bulk CRUD, approval queues, report handling — extended to media/commerce/social.
- **Frameworks:** Meilisearch (in env) or Typesense, web-push (VAPID in env), FCM (only if native apps), Presidio (PII redaction assist), ClamAV/YARA (upload scanning).

## PHASE 7 — Continuity & Community Trust (the rest of the coordination layer)
- **MiWalk** (offline conflict engine — never auto-merges money/guardianship/ballots),
  **MiSource** (resource freshness/provenance for Street/Justice/Learn/Mi),
  **MiHandoff** (helper→human routing), **MiAppeal** (due-process case flow),
  **MiShared** (shared-device/kiosk safety), **MiNotify**, **MiRender** (one content package
  across app/print/SMS/voice/offline), **MiModerate**, **MiDelegate** (liquid democracy for Voice),
  **MiKinship** (household/guardian/care lifecycle), **MiPlaceShift** (portable profile across
  jurisdictions), **MiStage** (Practice vs Live isolation), **MiScenario** (rights/failure test packs).
- **Frameworks:** Automerge/SQLite (local-first), Zammad (cases behind MiHandoff UI), Matrix
  Synapse (federation/rooms), ntfy + Apprise (notifications), Pandoc + WeasyPrint + Piper +
  Argos/LibreTranslate (render/translate), Decidim/Helios (governance/voting), OpenFeature/Flipt (stage flags),
  Playwright + Cucumber + LitmusChaos (scenario tests), the MiCompat supply-chain pipeline
  (ScanCode + ORT + Syft + OSV-Scanner + Grype/Trivy + Dependency-Track + Cosign).

## PHASE 8 — Mobile & Federation
- **Mobile-ready API contract** (own version, no PaymentEndpoint/AdsEndpoint) covering auth,
  feeds, media, chat, wallet, learn, commerce, justice.
- **Native apps** (React Native/Expo) with background media playback, push, offline-first.
- **Federation/fork compatibility:** how forks message, how a person moves between them, what
  happens to $MLY/receipts/standing/consent, how harmful instances are blocked.
- **Place-level recovery** drill (instance loss, key loss, keeper collusion).
- **Frameworks:** Expo/React Native + React Aria patterns, ActivityPub/Matrix for federation.

---

## Bounties to REMOVE (we're launching these — pull from the board)
Already shipped or in active scope this roadmap:
- **P7-03 Rights Card**, **P7-02 Walking-Home Timer** — shipped (MiJustice + Safety).
- **P13-01 Mi**, **P13-05 RAG over community knowledge** — shipped/deepening.
- **P4-07 Petition/Referendum** — shipped (MiJustice Pressure + Voice).
- **P2-02 Three Pots**, **P2-08 Rich Transaction History** — shipped (Wallet).
- **P5-02 Quests** — shipped (Street).
- **P14-02 PWA Enhancements**, **P1-10 Guest Experience** — partially shipped.
- **P0-01/02/03 MiAction/MiScope/MiReceipt** — become **Phase 0** (remove as building starts).
- **P2-01 Pocket Alive**, **P3-03 Quick Post**, **P3-04 Live Feed**, **P3-05 Celebrations**,
  **P6-01/03 Media/MiBlog**, **P8-01 Learn Alive** — fold into Phases 1–4 and remove as each starts.
As a rule: when a phase's work begins, its matching bounties come off the board so the roadmap
and the bounty list never disagree.

## What is intentionally EXCLUDED (recorded so it's never re-added)
- Every payment gateway (Stripe/PayPal/Braintree/Razorpay/Paystack/Flutterwave/Coinbase/etc.).
- Every ad system (banner/audio/video/AdSense/AdMob/adblock-blocker/sponsored/boosted-for-pay).
- Dark theme. NFT/crypto-gateway framing. Fake-user generators, fake views/likes. Any external
  session-replay/analytics that leaks sensitive pages.

## Sequencing logic (why this order)
Phase 0 makes money/law/safety safe to scale → Phase 1 makes the economy self-sustaining and
honest → Phase 2 (Media) is the biggest draw and creator/contribution engine, now that
guardrails + economy exist → Phases 3–5 deepen the remaining faces (social, learn, commerce),
each feeding contributions/rewards → Phase 6 unifies cross-cutting depth → Phase 7 completes the
trust/continuity layer → Phase 8 takes it mobile and federated. Every phase stays free,
ad-free, processor-free, light-themed, and receipted.
