# MiJustice — Build Status

Branch: `feat/mijustice-phase1` in `milyfe-platform`. Built locally, not pushed.
All work verified with `npm run typecheck` and a full `npm run build` (green).

## What is built and working

### Data layer
- `supabase/migrations/015_justice_schema.sql` — jurisdictions, statutes,
  constitution, rights guides, agencies (public read) + cases, consent
  (owner RLS). Seeds Florida/Duval + priority statutes + Duval agencies.
- `supabase/migrations/016_justice_expansion.sql` — violations, templates +
  template_reviews (attorney sign-off gate), filings, 20 class actions +
  members, partners, referrals, agent_logs, knowledge graph (nodes/edges),
  outcomes, rapid-response contacts, case shares, petitions + signatures.
  Public aggregate view `justice_impact_stats` (no PII). Seeds the 20 lawsuits,
  coalition partners, the FL expungement template (disabled), and petitions.

### Public tier (signed-out, offline-cacheable)
- `/justice` — branded landing (MiLyfe design system).
- `/justice/rights` — Know Your Rights hub.
- `/justice/rights/[situation]` — traffic stop, ICE, arrest, plea, search.
- `/justice/rights/constitution` — Bill of Rights decoded.
- `/justice/about`.

### Gated tier (MiLyfe login)
- `/justice/app/home` — war-room launcher, all 24 modules grouped by status.
- `/justice/app/encounter` — Encounter Mode: offline rights scripts, Record Now
  (device capture), Alert My People (SMS + geolocation), triple-tap duress exit.
- `/justice/app/defender` — intake wizard + consent gate + grounded scan +
  report (verified citations only, confidence-labeled, attorney match, save).
- `/justice/app/case/[id]` — tabbed case workspace (RLS-scoped).
- `/justice/app/contacts` — rapid-response contacts.
- `/justice/app/ice-shield` — warrant checker (judicial vs. administrative).
- `/justice/app/class-actions` — the 20 lawsuits + Rule 23.
- `/justice/app/liberation` — four-layer engine.
- `/justice/app/expungement` — FL sealing/expunge flow.
- `/justice/app/knowledge` — weapons + 23 manipulations + rights.
- `/justice/app/coalition` — partner directory.
- `/justice/app/pressure` — petitions (sign) + 18 legislative demands.
- `/justice/app/tracker` — aggregate impact dashboard (no PII).
- `/justice/app/admin/review` — board-only advisory review console.
- `/justice/app/[module]` — catch-all for specialized shields (10-23) via scaffold.

### AI + guardrails
- `src/lib/justice/defender.ts` — deterministic, rules-grounded scan; emits only
  verified citations (anti-hallucination).
- `src/lib/justice/agents.ts` — 8 agent roles, complianceScan (UPL + crisis),
  requiresHumanReview gate, logAgentAction audit.
- Persistent `LegalDisclaimer` (not-legal-advice) on every legal surface.
- Filing generation gated behind `justice_template_reviews` (attorney sign-off).

### MiLyfe integration
- Sidebar: `Justice` entry (`Scale` icon) → `/justice/app/home`.
- Cross-links from Pressure → `/governance`, Knowledge/Defender → rights + tracker.
- Same auth, same Supabase project, same design system, same PWA/offline layer.

## Intentionally NOT enabled (by design, not incomplete)
These require real human/legal commitments and are gated in the product logic:
- Auto-generated legal FILINGS that a user could submit — gated behind the
  advisory-board sign-off (`justice_template_reviews.enabled`).
- Live model enrichment of legal analysis — must pass CitationVerifier +
  ComplianceMonitor before reaching users.
- Live external data ingestion (CourtListener/MFJ/Recidiviz) into the knowledge
  graph — schema is ready; ingestion needs API keys + terms review.
- Real attorney/partner routing — directory + referral schema built; routing
  turns on as partners are onboarded and verified.

## Verify locally
```
cd milyfe-platform
npm run typecheck   # green
npm run build       # green (all /justice routes present)
```
Requires Supabase env for live data; pages render and degrade gracefully without it.
