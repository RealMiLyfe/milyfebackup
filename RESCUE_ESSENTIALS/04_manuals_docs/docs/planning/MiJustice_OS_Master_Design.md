# MiJustice — The People's Constitutional Justice OS

## Master Design Document (Extension of the MiLyfe Platform)

> *"We The People are not asking. We are REMEMBERING who we are."*

**Status:** Design / architecture spec. No code in this document.
**Companion:** see `MiJustice_OS_Expansion_v2.md` for legal/ethical guardrails, Encounter Mode, the Florida/Duval County launch localization, the resource & partnership network, MiLyfe injection points, and the pattern-detection knowledge base. See `MiJustice_OS_Expansion_v3.md` for incarcerated access, family/proxy accounts, user-safety hardening, content provenance, the last-mile filing reality, and governance/operations. See `MiJustice_OS_Expansion_v4.md` for the AI Legal Advisory Board (agents assist a human board), the board recruitment plan, and the full UI/UX design spec.
**Scope:** MiJustice is a new module-suite that lives *inside* the existing MiLyfe platform (Next.js 14/16 + Supabase + Tailwind). It reuses MiLyfe accounts, branding, and infrastructure. Signed-out visitors get a public get.milyfe-style landing page; everything operational sits behind MiLyfe sign-in. People without a MiLyfe account can create one directly from MiJustice.

---

## 0. Naming — replacing "get.milyfe" with a distinct MiJustice identity

The original vision used `get.milyfe.fun`. That domain/name is already the platform's public landing. MiJustice needs its own front door so it reads as a distinct product while still being *the same platform, same login*.

**Recommended primary name/URL options (pick one):**

| Option | Domain | Why |
|---|---|---|
| **MiJustice** (recommended) | `justice.milyfe.fun` | Clean subdomain, matches `get.milyfe.fun` sibling pattern, obviously part of MiLyfe |
| MiJustice | `mijustice.fun` | Standalone brand, easy to say, matches `mijaxx.fun` sibling |
| The War Room | `warroom.milyfe.fun` | Punchier, but less discoverable |

**Decision for this doc:** product name **MiJustice**, public URL **`justice.milyfe.fun`**, in-app route base **`/justice`**. Nothing references `get.milyfe.fun` — that stays the platform's own landing.

**Tagline:** *The People's Constitutional War Room.*
**Sub-tagline:** *24 tools. 20 lawsuits. Every right. 100% free. Owned by the people.*

---

## 1. How MiJustice fits the existing platform

MiJustice is **not** a separate app. It is a route group and a set of Supabase tables added to the current `milyfe-platform` Next.js project. This keeps one login, one brand system, one deployment.

**What it reuses (no reinvention):**

- **Framework:** Next.js App Router (already `next ^16`), React 19, server components.
- **Auth:** existing Supabase auth (`@supabase/ssr`), the same `createClient()` helpers in `src/lib/supabase/`, and the existing `middleware.ts` → `updateSession()` gate.
- **Brand tokens:** the Tailwind theme already defines `harbor` (deep blue), `teal` (#00C1AE), `mly` (gold #FFC107), plus semantic tokens. MiJustice uses these exact colors — no new palette.
- **Font:** Atkinson Hyperlegible (already the platform default — an accessibility-first choice that fits a justice product perfectly).
- **Shell:** the platform `Sidebar`, `BottomNav`, `TopBar`, `AuthProvider`, `MiBubble`, and `CommandSearch` all wrap MiJustice pages automatically because it lives under the `(platform)` shell (or a sibling group that imports the same shell).
- **UI kit:** existing `@/components/ui/*` (Button with `harbor` variant, Input, dialogs via Radix), `sonner` toasts, `framer-motion`, `recharts` for dashboards, `maplibre-gl` for the violation maps.
- **Offline + PWA:** the platform already ships a service worker, `DataCacher`, IndexedDB (`dexie`). MiJustice's Know-Your-Rights content is cached offline so it works during an actual police/ICE encounter with no signal.

**What it adds:**

- A `(justice)` route group (or `(platform)/justice`) for the 24 modules.
- A public marketing route for signed-out visitors (the landing page).
- New Supabase tables (all namespaced `justice_*`) with Row-Level Security.
- New sidebar/nav entries and a top-level "Justice" launcher.
- New open-source repositories for the legal-content and document-generation engines.

---

## 2. Branding — MiLyfe-themed, not a clone

MiJustice inherits MiLyfe's visual language but carries a distinct accent so users know they've entered the "war room."

| Token | Source | MiJustice usage |
|---|---|---|
| `harbor-800/900` deep blue | existing | Primary surfaces, hero background, headers |
| `teal-500` (#00C1AE) | existing | Actions, links, "protected right" highlights |
| `mly-500` (#FFC107) gold | existing | Emphasis, CTAs, "the people" accent, seals |
| Atkinson Hyperlegible | existing | All type (accessibility-first) |
| `shadow-glow-teal` / `-mly` | existing | Card and CTA glows |

**MiJustice accent layer (additive, still on-brand):**

- A subtle constitutional motif: thin gold rule lines under section headers, a "We the People" wordmark treatment, and a scales-of-justice glyph rendered in `teal` used only as the MiJustice mark.
- Landing page reuses the exact CSS structure and color variables of `public_html/get-milyfe.html` (blue→teal brand gradient, gold CTAs, Atkinson font) so it feels like a sibling of the existing get.milyfe page — same family, new face.

**Logo/mark:** `MiJustice` lockup = MiLyfe logo + "Justice" set in the display font, with the scales glyph. Stored at `public/justice/logo.svg` and reused in the sidebar entry and landing hero (same badge treatment as the get.milyfe circular brandmark badge).

---

## 3. Authentication & access model

**Core rule (from the ask): MiLyfe-account holders sign in and get access; non-members can sign up right here; the operational OS is never exposed to the public.**

### 3.1 Route tiers

| Tier | Routes | Who sees it |
|---|---|---|
| **Public** | `/justice` (landing), `/justice/rights` (read-only Know-Your-Rights + Constitution decoded), `/justice/about` | Everyone, signed in or not |
| **Gated (MiLyfe account required)** | `/justice/app/**` — all 24 operational modules, intake, case tracking, document generation, dashboards | Signed-in MiLyfe users only |

Rationale: the *educational* layer (Constitution decoded, jury nullification guide, know-your-rights-by-situation) is intentionally public and offline-cacheable because someone facing ICE at the door or a traffic stop needs it *without* logging in. The *operational* layer (case intake, auto-generated legal motions, liberation tracking, asset-recovery filings) requires an account for privacy, RLS ownership, and abuse-prevention.

### 3.2 Reusing existing middleware

The platform's `src/lib/supabase/middleware.ts` already:

- keeps a `PUBLIC_ROUTES` allow-list,
- redirects unauthenticated users to `/login?next=<path>`,
- fails open if Supabase env is missing.

**Change required (config only, documented — not written here):** add the public MiJustice routes to `PUBLIC_ROUTES`:

```
'/justice', '/justice/rights', '/justice/about'
```

Everything under `/justice/app/**` is *not* listed, so the existing gate automatically bounces signed-out users to `/login?next=/justice/app/...`. After sign-in they land exactly where they were headed. No new auth code — the current gate already does this.

### 3.3 Sign-in-only vs. sign-up-here

- **Sign in:** MiJustice's landing "Enter the War Room" button links to the existing `/login`. Existing MiLyfe users authenticate once and have access to both MiLyfe and MiJustice (same session, same cookie).
- **Sign up here:** the landing also offers "Create a free MiLyfe account," linking to the existing `/signup` with `?next=/justice/app/home`. The current signup flow (email + username + password → email confirmation → onboarding) is reused unchanged. After confirmation, the user is dropped into MiJustice.
- **One identity everywhere:** because MiJustice uses the same Supabase project and `auth.users`, a MiLyfe account *is* a MiJustice account. No separate accounts, no second password.

### 3.4 Privacy posture for case data

Case information is sensitive (charges, immigration status, incarceration). Design requirements:

- Every `justice_*` table with user data has **Row-Level Security**: a user can read/write only rows where `user_id = auth.uid()`.
- Attorney/partner access is via explicit, revocable **case shares** (`justice_case_shares`), never blanket access.
- No third-party analytics on `/justice/app/**`.
- Client-side encryption option for the most sensitive free-text (see §7.4).
- Follows the platform's existing `PRIVACY.md` / `SECURITY.md`.

---

## 4. Route architecture

```
src/app/
  (justice-public)/                 ← public, in PUBLIC_ROUTES
    justice/
      page.tsx                      ← LANDING (get.milyfe-style, branded)
      about/page.tsx
      rights/                       ← public Know-Your-Rights + Constitution decoded
        page.tsx
        [situation]/page.tsx        ← traffic stop, ICE at door, arrest, plea, bail...
        constitution/page.tsx       ← all 7 articles + 27 amendments, plain-English, multilingual
        jury-nullification/page.tsx

  (platform)/                       ← existing gated shell (Sidebar/BottomNav/TopBar)
    justice/
      app/
        home/page.tsx               ← MiJustice dashboard / launcher for the 24 modules
        defender/                   ← Module 1: AI Constitutional Defender (intake + scan + report)
        liberation/                 ← Module 2: Liberation Engine
        ice-shield/                 ← Module 3: ICE Defense Shield
        sovereignty/                ← Module 4: Native Sovereignty
        class-actions/              ← Module 5: Class Action War Room (+ the 20 lawsuits)
        knowledge/                  ← Module 6: People's Knowledge Base (gated tools; public mirror in /justice/rights)
        coalition/                  ← Module 8: Coalition Engine (partner directory + intake matching)
        pressure/                   ← Module 9: Political Pressure Engine (petitions, scorecards)
        asset-recovery/             ← Module 10
        youth/                      ← Module 11
        debt/                       ← Module 12
        solitary/                   ← Module 13
        surveillance/               ← Module 14
        juvenile/                   ← Module 15
        mental-health/              ← Module 16
        veterans/                   ← Module 17
        women-family/               ← Module 18
        lgbtq/                      ← Module 19
        medical-custody/            ← Module 20
        probation-parole/           ← Module 21
        grand-jury/                 ← Module 22
        whistleblower/              ← Module 23
        international/              ← Module 24
        case/[caseId]/page.tsx      ← a person's case workspace (violations, filings, status)
        tracker/page.tsx            ← public-facing live dashboards (read-only aggregates)
```

Module 7 (Open Source Architecture) is not a page — it's the repo/hosting strategy in §9.

---

## 5. The landing page (get.milyfe-style, MiJustice-branded)

The public `/justice` page is a direct sibling of `public_html/get-milyfe.html`: same CSS variable system (`--blue #1e4a8a`, `--teal`, `--gold #FFC107`, brand gradient), same Atkinson font, same section rhythm (attention bar → hero → benefit strip → what-it-is → "it actually works" → how-it-works → founder note → stats → guarantee → CTA band → P.S. → footer). It is implemented as a Next.js page (server component) so it can be part of the app and share the auth CTAs, but its markup/style mirrors the proven landing.

**Section-by-section spec:**

1. **Attention bar** — "For every neighbor who was ever counted out, locked up, or shaken down by a system built to profit off them."
2. **Hero** — circular white brandmark badge (MiJustice mark), kicker "The People's Constitutional War Room · Free Forever," H1 *"The System Isn't Broken. It Was BUILT This Way. Now We Fight Back."*, sub explaining MiJustice in one breath, dual CTA:
   - **Primary (gold):** "Enter the War Room" → `/login?next=/justice/app/home`
   - **Secondary (outline):** "Create a Free Account" → `/signup?next=/justice/app/home`
3. **Benefit strip (3)** — 100% Free Forever · 100% Open Source (AGPL-3.0) · Privacy-First & Multilingual.
4. **What is MiJustice** — plain-English: an AI-powered constitutional justice OS with 24 tools that fight back at every point the government abuses power; connects you to free attorneys and the right class action.
5. **"It actually works" stamp band** (charcoal) — "24 modules. 20 lawsuits. Every coalition. One login."
6. **The 24 modules grid** — icon cards, each links to its module (gated) or scrolls to explainer.
7. **The 20 lawsuits** — the full table (People vs. the United States) rendered as cards, each with "See if your case fits →" (→ intake, gated).
8. **How it works (3 steps)** — 1) Tell your story (intake) · 2) The AI scans it against every amendment · 3) Get your violation report, pre-drafted motions, and a matched free attorney.
9. **The proof / stats** — 750k incarcerated for victimless crimes · 5% of world population / 20% of prisoners · 8+ wrongful facial-recognition arrests · 180k+ veterans behind bars · qualified immunity was *invented*, not in the Constitution.
10. **Founder note** — lived-experience origin (30+ incarcerations), reusing the honest voice of the existing founder letter; links to `mijaxx.fun`.
11. **"Open Book" guarantee** — no founder keys, code is public, link to GitHub org.
12. **CTA band** — "Ready to Remember Who You Are?" → sign in / sign up.
13. **P.S.** — the skip-to-end summary.
14. **Footer** — same footer family as get.milyfe (links to platform, campaign, GitHub, contact; the non-authority disclaimer).

**Landing lead capture:** reuse the existing intake pattern (the get.milyfe form posts to the campaign intake API). For MiJustice, the "get on the list" form is optional; the primary conversion is account creation, not email capture, because operational value lives behind login.

---

*(Continued in the sections below: the 24 modules in detail, the 20 lawsuits, the legal weapons, the data model, i18n, and the GitHub/open-source plan.)*

---

## 6. The 24 Modules — full specification

Every module is a route under `/justice/app/`. Each spec lists **purpose**, **inputs**, **what it produces**, and **data/integrations**. All are 100% free, gated behind MiLyfe sign-in, RLS-protected, and available in every supported language.

### Module 1 — AI Constitutional Defender  ·  `/justice/app/defender`
*The machine that kills fake charges.*

- **Purpose:** scan any criminal charge against the Constitution and surface every violation.
- **Inputs (intake form):** charges filed, jurisdiction (state/county), circumstances of arrest, were rights read, was there a judicial warrant, was there a search, was counsel provided, was bail set and affordable, was a plea offered/pressured.
- **Constitutional scan:** checks each charge against 1st, 2nd, 4th, 5th, 6th, 7th, 8th, 9th, 10th, 13th, 14th Amendments (logic table in `justice_amendment_rules`).
- **Produces:** a violation report — every violation detected, the specific amendment(s), matching case law/precedent citations, pre-drafted motions (suppress, dismiss, in limine, discovery), a plain-English explanation, and next steps.
- **Auto-match to help:** connects to pro-bono attorneys nearby, nearest ACLU/NAACP LDF/EJI/CCR chapter, legal-aid clinics, public-defender support, and class-action intake if the case fits one of the 20 lawsuits.
- **Data/integrations:** `justice_cases`, `justice_violations`, `justice_motions`; LLM via the platform's existing `ai` SDK; citation library seeded in the open-source `mijustice-legal-content` repo.

### Module 2 — The Liberation Engine  ·  `/justice/app/liberation`
*Get our people out.*

- **Layer 1 — Constitutional audit:** scans active cases for victimless-crime convictions, excessive bail that forced pleas, Brady violations, illegal searches, coerced confessions, denied counsel, racial sentencing disparities, people held past release date, unconstitutional charges.
- **Layer 2 — Mass legal filings:** auto-generates habeas corpus petitions, post-conviction relief, appeals, compassionate release, sentence-reduction motions, Brady claims, ineffective-assistance (6th Am.) claims.
- **Layer 3 — Tracking dashboard (public read-only):** counts of people held unconstitutionally, most common violations, worst-offending states/counties, judges/prosecutors/departments with most violations, per-case status.
- **Layer 4 — Reentry support:** non-discriminating-housing DB, second-chance employers, automated expungement filing, mental-health/substance resources, benefits restoration, family reunification, state-by-state voting-rights restoration, financial-assistance navigation.
- **Data:** `justice_cases`, `justice_filings`, `justice_reentry_resources`.

### Module 3 — ICE Defense Shield  ·  `/justice/app/ice-shield`
*Nobody gets disappeared on our watch.*

- **Know Your Rights (every language):** what to say (nothing without a lawyer), what not to say/do, how to protect the household.
- **Warrant checker:** scans an uploaded/photographed document and tells the user instantly whether it's a real judicial warrant signed by a judge, or an administrative form (I-205) that creates *no* obligation to open the door.
- **Rapid response network:** one-button alert to immigration attorneys, community rapid-response teams, legal observers, media contacts, neighbors.
- **Detention tracker:** where a detainee is held, whether they've had a hearing, whether rights were violated, legality of detention, connection to free immigration attorneys for family.
- **Auto legal defense:** habeas petitions, bond-hearing requests, constitutional challenges, family-separation emergency motions.
- **Note:** the Know-Your-Rights content is mirrored on the **public** `/justice/rights/ice-at-your-door` and cached offline.

### Module 4 — Native Sovereignty  ·  `/justice/app/sovereignty`
*The only people with true birthright — and the only treaties that are supreme law.*

- Documents and litigates treaty violations (500+ broken treaties), frames tribal sovereignty as pre-constitutional and acknowledged by Article VI (Supremacy Clause).
- Partners with Native American Rights Fund (NARF) and tribal legal orgs; connects ICE-on-stolen-land argument to the sovereignty narrative; amplifies tribal voices; public education on the true history.
- **Data:** `justice_treaties`, `justice_partners` (NARF, tribal orgs).

### Module 5 — Class Action War Room  ·  `/justice/app/class-actions`
*Not one lawsuit. A machine that files them all.*

- As intake stories arrive, AI categorizes each person into the appropriate class action(s), identifies strong lead plaintiffs, generates evidence packages, tracks deadlines / statutes of limitations / administrative-claim requirements, feeds ready-to-file docs to legal teams, coordinates all 20 lawsuits, and learns from each outcome.
- **Rule 23 checklist per class:** numerosity, commonality, typicality, adequacy (see §8).
- **Data:** `justice_class_actions` (the 20), `justice_class_members`, `justice_evidence_packages`, `justice_deadlines`.

### Module 6 — People's Knowledge Base  ·  `/justice/app/knowledge` (+ public mirror `/justice/rights`)
*Reminding the people they are the power.*

- **Constitution decoded:** every article + all 27 amendments in plain English and every major language, with real-world violation examples and "what would this look like in YOUR life?" guides.
- **Know Your Rights by situation:** pulled over, arrested, ICE at your door, plea pressure, unaffordable bail, warrantless search, held without charges, prison mistreatment, post-release denial of housing/jobs/voting, kids targeted at school, solitary.
- **Jury nullification — the hidden right:** what it is, how it works, historical examples, how to exercise it, why it's hidden.
- **Violation database:** every documented overreach, searchable by state/county/type/outcome, visual patterns, feeds class-action evidence.
- **The people's history:** how the 13th loophole, mass incarceration, cash bail, qualified immunity, broken treaties, the school-to-prison pipeline, and civil forfeiture were built — and every time the people fought back and won.
- The educational content is public + offline; the violation database write/analytics are gated.

### Module 7 — Open Source Architecture  (not a page — see §9)
*Owned by nobody. Available to everybody. Forever.* All code public on GitHub under AGPL-3.0, decentralized hosting, E2E encryption for case data, zero for-profit data collection, community-governed, regular community security audits, integrations with LawDroid, Recidiviz, and Code for America's Clear My Record.

### Module 8 — Coalition Engine  ·  `/justice/app/coalition`
*United we are unstoppable.*

- Directory of allied orgs (ACLU, NAACP LDF, EJI, CCR, NARF, Ben Crump Law, National Immigration Project, Innocence Project, Brennan Center, Vera Institute, Public Justice, Code for America, Recidiviz, HIAS, tribal legal orgs, Disability Rights Advocates, Lambda Legal, National Veterans Legal Services Program).
- Routes each intake to the best-fit partner; MiJustice is the hub, partners are spokes.
- **Data:** `justice_partners`, `justice_referrals`.

### Module 9 — Political Pressure Engine  ·  `/justice/app/pressure`
*When the courts won't listen, the people make them listen.*

- Petition engine (target 1M signatures), voter-registration drive (esp. post-felony restoration), congressional scorecard on constitutional-rights support, ballot-initiative tracker, media engine (amplify every story/case/win), candidate endorsement system, legislative demand list.
- **The 18 legislative demands** (tracked as records in `justice_legislative_demands`): close the 13th loophole; end qualified immunity; end cash bail; regulate plea bargaining; ban collateral consequences; minimum wage for prison labor; fund public defenders equal to prosecutors; ban forfeiture without conviction; ban facial recognition in policing; counselors/nurses/social workers instead of police in schools; abolish solitary; abolish for-profit probation; require judicial warrants for all ICE actions; honor Native treaties; universal veterans' courts; abolish zero-tolerance school policies; end grand-jury secrecy; mandate jury-nullification disclosure.

### Module 10 — Asset Recovery Engine  ·  `/justice/app/asset-recovery`
Scans arrests/convictions for civil asset forfeiture, checks due process, auto-generates motions to recover seized property, tracks which departments profit most, files class actions (4th/5th/8th/14th), connects to property-recovery attorneys, public dashboard by department/jurisdiction.

### Module 11 — Youth Defense Shield  ·  `/justice/app/youth`
Monitors school disciplinary actions for constitutional violations, auto-generates parent advocacy letters, connects to education attorneys, tracks worst racial-disparity districts, files class action vs. zero-tolerance policies, kid-friendly Know-Your-Rights, advocates counselors over cops, challenges juvenile records following people to adulthood.

### Module 12 — Debt Defense Engine  ·  `/justice/app/debt`
Identifies people jailed for inability to pay, auto-generates motions to dismiss debt-based warrants, calculates 8th-Amendment Excessive-Fines violations, files indigency-hearing requests, tracks revenue-driven jurisdictions, exposes judicial conflicts of interest in fee collection, files class action vs. modern debtors' prisons.

### Module 13 — Solitary Confinement Abolition Engine  ·  `/justice/app/solitary`
Tracks everyone currently in solitary, flags court-barred placements (mental illness, juveniles, disabilities) and anyone past 15 days (UN torture threshold), auto-generates habeas + §1983 complaints, files international complaints with the UN Special Rapporteur on Torture, tracks duration/conditions/harm, files nationwide-ban class action.

### Module 14 — Surveillance Defense Shield  ·  `/justice/app/surveillance`
Identifies arrests based on facial recognition/predictive policing, challenges that evidence, tracks departments and error rates (racial disparities), files FOIA for algorithms/training data, demands transparency per search, files 4th-Amendment class actions, advocates a full facial-recognition ban, educates the public on the bias.

### Module 15 — Juvenile Defense Engine  ·  `/justice/app/juvenile`
Challenges charging juveniles as adults (8th/14th), challenges juvenile solitary, monitors record-sealing compliance, connects families to specialists, advocates brain-science-based sentencing, files class actions vs. trying children as adults for non-violent offenses.

### Module 16 — Mental Health Diversion Engine  ·  `/justice/app/mental-health`
Identifies crises and advocates diversion, challenges ADA violations in custody, tracks deaths of people with mental illness in custody, connects to diversion programs, advocates crisis-intervention teams over armed response, files class actions vs. punitive housing of the mentally ill.

### Module 17 — Veterans Defense Module  ·  `/justice/app/veterans`
Identifies incarcerated veterans, advocates universal veterans'-court access, connects to specialized defense, challenges PTSD-related incarceration, files service-based sentence reductions, partners with the National Veterans Legal Services Program.

### Module 18 — Women's & Family Defense Module  ·  `/justice/app/women-family`
Challenges shackling during childbirth (8th), fights incarceration-driven family separation, advocates adequate medical care, files complaints vs. guard sexual abuse, challenges conditions for pregnant people, tracks the fastest-growing/least-advocated population.

### Module 19 — LGBTQ+ Prisoner Rights Module  ·  `/justice/app/lgbtq`
Challenges wrong-gender facility placement, documents/fights disproportionate violence and sexual assault, challenges denial of medical care and hormone therapy, advocates federal protection standards, connects to Lambda Legal and the ACLU LGBT Rights Project.

### Module 20 — Medical Rights & Custody-Death Tracker  ·  `/justice/app/medical-custody`
Real-time tracker of every death in custody in the U.S., AI flags medical-neglect (8th) cases, auto-generates wrongful-death claims for families, tracks highest-death-rate facilities, files pattern class actions, partners with families for litigation, public dashboard making every custody death visible.

### Module 21 — Probation & Parole Defense Engine  ·  `/justice/app/probation-parole`
Identifies for-profit probation, challenges charging people for their own supervision, distinguishes inability-to-pay from willful refusal, files class actions vs. for-profit probation companies and authorizing states, tracks which companies profit and from which communities.

### Module 22 — Grand Jury Transparency Engine  ·  `/justice/app/grand-jury`
Educates on how grand juries work, advocates defense presence, tracks indictment rates by office and demographic, identifies prosecutorial-misconduct patterns, files reform advocacy, connects grand-jury targets to defense immediately.

### Module 23 — Whistleblower Protection Engine  ·  `/justice/app/whistleblower`
Connects whistleblowers to attorneys on contact, documents retaliation, files with oversight bodies, provides secure anonymous reporting channels, advocates expanded protection laws, tracks retaliation patterns by facility/jurisdiction.

### Module 24 — International Human Rights Engine  ·  `/justice/app/international`
Files complaints with the UN Human Rights Council; UN Special Rapporteurs on Torture, Contemporary Forms of Slavery, Rights of Indigenous Peoples, and Racism; the Inter-American Commission on Human Rights; the UN Committee Against Torture. Documents U.S. violations of the Mandela Rules, ICCPR, Convention Against Torture, modern-slavery commitments, and UNDRIP. Creates a two-front (domestic + international) pressure campaign.

---

## 7. Legal foundation content (Parts 1–3 of the vision)

Seeded as structured data in the open-source `mijustice-legal-content` repo and surfaced through Modules 1 and 6.

### 7.1 The Constitution (Part 1)
Preamble, 7 Articles (I–VII), and all 27 Amendments — stored as records with plain-English decoding + per-language translations. The Bill of Rights and Amendments 11–27 are each a row keyed for the Defender's scan logic.

### 7.2 The 23 manipulations (Part 2)
Each documented manipulation (13th-Amendment slavery loophole, qualified immunity, prosecutorial/judicial immunity, plea-bargain trap, cash bail, collateral consequences, civil asset forfeiture, debtors' prisons, surveillance state, school-to-prison pipeline, solitary as torture, prison-industrial complex, ICE enforcement, grand-jury manipulation, hidden jury nullification, veterans betrayal, women/pregnant people, LGBTQ+ incarceration, medical neglect/custody deaths, whistleblower retaliation, juvenile failures, mental-health crisis, international-law violations) is a record with the constitutional basis, the statistics, and the linked module + lawsuit.

### 7.3 Legal weapons (Part 3)
| # | Weapon | What it does |
|---|---|---|
| 1 | Federal Tort Claims Act (FTCA, 1946) | Sue the federal government; administrative claim required first |
| 2 | 42 U.S.C. § 1983 | Hold state/local officials accountable for constitutional violations; fees under §1988 |
| 3 | Bivens actions | Federal equivalent of §1983 against federal officials |
| 4 | Habeas corpus | Challenge unlawful detention |
| 5 | Brady violations | Prosecutors must disclose favorable evidence; can overturn convictions |
| 6 | Rule 23 class certification | Numerosity, commonality, typicality, adequacy |
| 7 | International human-rights complaints | UN HRC, IACHR, Special Rapporteurs |
| 8 | Sovereign-immunity waivers | The doors lawsuits pass through |

**Obstacles & counters** (stored in `justice_obstacles`): sovereign immunity → FTCA + §1983; qualified immunity → argue clearly-established right; prosecutorial/judicial immunity → target policy/systemic patterns + legislative reform; discretionary-function exception → argue constitutional violation; statutes of limitations → file admin claims immediately; standing → use the testimony database as evidence; mootness → class certification keeps cases alive.

### 7.4 Data model overview

All tables prefixed `justice_`, in the existing Supabase project, with RLS. Reference/content tables are public-read; user-case tables are owner-scoped.

**Reference / content (public read, admin write):**
`justice_constitution` · `justice_amendment_rules` · `justice_manipulations` · `justice_weapons` · `justice_obstacles` · `justice_class_actions` (the 20) · `justice_partners` · `justice_legislative_demands` · `justice_rights_guides` (know-your-rights by situation) · `justice_treaties`.

**User / case (RLS: `user_id = auth.uid()`):**
`justice_cases` (charge, jurisdiction, arrest circumstances, flags) · `justice_violations` (case_id → amendment, severity, precedent) · `justice_motions` / `justice_filings` (generated documents, status) · `justice_class_members` (case_id → class_action_id, lead-plaintiff score) · `justice_evidence_packages` · `justice_referrals` (case_id → partner) · `justice_case_shares` (case_id → attorney/partner, revocable) · `justice_detentions` (ICE + custody tracking) · `justice_deadlines`.

**Aggregate views (public read-only, no PII):** materialized views powering the live trackers in Modules 2, 10, 14, 20 — counts and patterns only, never individual identities.

**Encryption:** most-sensitive free-text (personal narrative, immigration status) supports client-side encryption before storage; only the owner (and explicitly shared attorneys) can decrypt.

### 7.5 Internationalization
Reuses/extends the platform's multilingual approach. Target languages from the vision: English, Spanish, Haitian Creole, Portuguese, French, Arabic, Chinese — extensible. All reference/content tables carry per-language fields; UI strings live in the shared i18n catalog. Atkinson Hyperlegible (already the default font) keeps everything accessible.

---

## 8. The 20 class-action lawsuits — The People vs. The United States

Stored in `justice_class_actions`; surfaced on the landing page and in Module 5. Each intake is auto-matched to any that fit.

| # | Lawsuit | Defendants | Constitutional basis |
|---|---|---|---|
| 1 | Victimless-Crime Mass Incarceration | Federal & State Governments | 8th, 9th, 14th |
| 2 | Coercive Plea Bargaining | DOJ, State Prosecutors | 5th, 6th, 14th |
| 3 | Cash Bail as Wealth Discrimination | Every State Using Cash Bail | 8th, 14th |
| 4 | Police Brutality & Wrongful Death | Officers + Departments | 4th, 14th, §1983 |
| 5 | Prison-Labor Exploitation (Slavery) | Bureau of Prisons, State DOCs | 13th |
| 6 | Collateral-Consequences Life Sentence | Federal & State Governments | 8th, 14th |
| 7 | ICE Warrantless Home Entries | DHS, ICE | 4th |
| 8 | ICE Deportation of U.S. Citizens | DHS, ICE | 5th, 14th |
| 9 | ICE Unconstitutional Fines | DHS, ICE | 5th, 7th, 8th |
| 10 | ICE Racial Profiling | DHS, ICE, CBP | 4th, 14th |
| 11 | Native Treaty Violations | Federal Government | Article VI (Supremacy Clause) |
| 12 | Wrongful Incarceration — Active Cases | All Jurisdictions | §1983, 4th, 5th, 6th, 14th |
| 13 | Civil Asset Forfeiture | Federal & State Governments | 4th, 5th, 8th, 14th |
| 14 | School-to-Prison Pipeline | School Districts, States | 14th, Title VI |
| 15 | Modern Debtors' Prisons | States + Municipalities | 8th, 14th |
| 16 | Solitary Confinement as Torture | Bureau of Prisons, State DOCs | 8th, §1983, Intl Law |
| 17 | AI Surveillance & Predictive Policing | Departments Using These Tools | 1st, 4th, 14th |
| 18 | Juvenile Justice Abuse | Juvenile Courts, States | 8th, 14th |
| 19 | Medical Neglect & Deaths in Custody | Prisons, Jails, ICE Facilities | 8th, §1983 |
| 20 | For-Profit Probation Companies | Private Probation Companies + States | 8th, 14th |

---

## 9. Module 7 in practice — the free & open-source GitHub plan

*Owned by nobody. Available to everybody. Forever.* MiJustice ships as free, open-source repositories under a dedicated GitHub org, consistent with the platform's existing AGPL-3.0 posture and the existing `RealMiLyfe` GitHub presence.

### 9.1 GitHub organization

**Org:** `MiJustice` (or a `mijustice-*` repo family under the existing `RealMiLyfe` org — recommended so it clearly ties to MiLyfe and reuses existing CI, CODEOWNERS, and Dependabot config).

### 9.2 Repositories (all public, AGPL-3.0-or-later)

| Repo | Contents |
|---|---|
| `mijustice-platform` | The Next.js route group, module UIs, and API routes (or a documented folder within the existing `milyfe-platform` repo if kept monorepo) |
| `mijustice-legal-content` | The Constitution decoded, amendment scan rules, 23 manipulations, 8 weapons + obstacles, know-your-rights guides, the 20 lawsuits — structured JSON/MDX, community-editable, multilingual |
| `mijustice-doc-templates` | Pre-drafted motion/petition templates (suppress, dismiss, habeas, §1983, Brady, compassionate release, bond hearing, FTCA admin claim, FOIA, international complaint) with mail-merge fields |
| `mijustice-defender` | The constitutional-scan engine logic (charge → amendments → violations → citations) with tests |
| `mijustice-i18n` | Translation catalogs for all supported languages |
| `mijustice-data-schema` | Supabase migrations for the `justice_*` tables, RLS policies, and public aggregate views |

### 9.3 Licensing & governance

- **License:** GNU AGPL-3.0-or-later (matches `milyfe-platform`) — any deployed fork must publish its source. Public code stays public.
- **No founder keys:** no private admin backdoor; governance changes go through transparent community process, mirroring the platform's stance.
- **Security:** reuse the existing `.github` CI, CODEOWNERS, Dependabot, and `SECURITY.md` reporting; regular community security audits; RLS + encryption reviewed before each release.
- **Contribution:** reuse the existing `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

### 9.4 Open-source integrations (from the vision)

- **Code for America — Clear My Record:** power the automated expungement filing in Module 2 (reentry).
- **Recidiviz:** criminal-justice data and reentry analytics feeding the trackers.
- **LawDroid:** open-source legal-AI patterns for the Defender and document generation.
- **Electronic Frontier Foundation** resources for the surveillance module.

### 9.5 Coalition & technology partners

**Legal partners:** ACLU · NAACP Legal Defense Fund · Equal Justice Initiative · Center for Constitutional Rights · Ben Crump Law · Innocence Project · Brennan Center for Justice · Native American Rights Fund · National Immigration Project · Lambda Legal · Disability Rights Advocates · National Veterans Legal Services Program · Public Justice · Vera Institute of Justice · HIAS · tribal legal organizations.

**Technology partners:** Code for America · Recidiviz · LawDroid · Electronic Frontier Foundation · the open-source community.

MiJustice is the hub; every partner is a spoke. They've fought in silos — this unites them under one login and one intake.

---

## 10. Phased rollout

> **Canonical build sequence = the 7-phase, Florida/Duval-first, guardrails-first plan in `MiJustice_OS_Expansion_v2.md` §8.** That is the authoritative order of work. The module groupings below are a *coverage map* (which modules land in roughly which stretch of the canonical plan), not a separate schedule.

**Module coverage map (maps onto the canonical 7 phases):**
- **Foundation (canonical Phase 1):** guardrails, consent, jurisdiction model (Duval `live`), advisory-board recruitment. Route groups, `PUBLIC_ROUTES` entries, `mijustice-*` repos, `justice_*` reference schema, landing page.
- **First value (canonical Phase 2):** Encounter Mode, public Know-Your-Rights + Constitution-decoded content (offline), FL statute/rule library, sidebar/launcher entry, auth wiring.
- **First template (canonical Phase 3):** expungement/sealing packet (attorney-reviewed).
- **Defender + matching (canonical Phase 4):** Module 1 (AI Constitutional Defender) → attorney/partner match; advisory-board review console.
- **Knowledge graph v1 (canonical Phase 5):** Module 6 (Knowledge Base / violation DB) + first aggregate tracker dashboard.
- **Network + media + pressure (canonical Phase 6):** Module 8 (Coalition), Module 9 (Political Pressure into MiLyfe Governance), media pipeline.
- **Expand (canonical Phase 7):** Modules 2, 3, 5, 10–24 on a rolling basis, then additional FL circuits, then other states — additively, each behind the accuracy gate.

At every phase: 100% free, 100% open source, privacy-first, multilingual, mobile-first, community-governed.

---

## 11. The message

> *"We The People were promised justice. We got a business."*

- **Not** anti-police — anti-abuse of power.
- **Not** about freeing dangerous people — about the millions who were never dangerous.
- **Not** partisan — it hits every race, state, and income level.
- **It is** about the Constitution they wrote and swore to uphold — and have been violating.
- **It is** about memory: reminding the people that *they* are the power.

**The proof:** 750,000 incarcerated for victimless crimes · 86% of federal prisoners there for victimless crimes · 5% of the world's population, 20% of its prisoners · 38,000 jailed yearly in Texas for unpaid court debt · 9,000 Ferguson warrants in one year for half the city · 1.7M students in schools with police but no counselors · Black students 4× more likely to be suspended · 8+ wrongful facial-recognition arrests · 180,000+ veterans behind bars · the 13th Amendment still permits slavery · qualified immunity was invented by the Supreme Court, not written into the Constitution.

---

## 12. The bottom line

The government built a machine to exploit the people. **MiJustice is the machine that sets them free** — 24 modules, 20 lawsuits, every coalition, every tool, every right, every language, every state, every court, every international body. 100% free. 100% open source. 100% for the people. One MiLyfe login opens the whole war room.

It lives inside the platform the people already own. It starts at **justice.milyfe.fun**.

> *"We The People are not asking. We are REMEMBERING who we are."* ✊
