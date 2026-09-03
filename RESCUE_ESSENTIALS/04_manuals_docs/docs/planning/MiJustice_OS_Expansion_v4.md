# MiJustice — Expansion v4

## AI Legal Advisory Board · Recruitment Plan · UI/UX Design Spec

> Companion to the Master Design, v2, and v3. MiJustice is part of **MiLyfe — "We The People."** No code in this document.

---

## 1. The AI Legal Advisory Board (agents-assist-humans)

AI agents do the heavy lifting — research, drafting, citation verification, error-catching — but **licensed humans hold final sign-off on everything that reaches a real person.** The agents make the humans faster and more accurate; the humans keep the agents honest.

### 1.1 Agent roles & skills

Each agent is a specialized AI role with a defined skill scope, a toolset, and a handoff protocol.

| Agent role | Skill / focus | What it does | Tools it uses |
|---|---|---|---|
| **Constitutional Scanner** | Amendment analysis | Scans a case intake against all relevant amendments and FL statutes; produces a draft violation report with citations | `mijustice-legal-content`, FL statute library, amendment-rules table |
| **Citation Verifier** | Caselaw & statute accuracy | Checks every case, statute, and rule cited by any agent or user-facing content against authoritative sources; flags unverifiable or overruled citations | CourtListener API, official FL Statutes, FL Rules |
| **Template Drafter** | Motion/petition generation | Produces a draft legal filing from the template library, filling in case-specific fields, formatted for the correct court/division | `mijustice-doc-templates`, jurisdiction/division rules |
| **Precedent Researcher** | Case-law research | Finds relevant precedent for a violation type/jurisdiction, summarizes holdings, checks for overruling | CourtListener API, RECAP |
| **Pattern Analyst** | Knowledge-base patterns | Runs the disparity/anomaly analysis across the graph (judges, prosecutors, officers) and produces sourced briefs | `justice_kb_*`, Measures for Justice, Recidiviz data |
| **Intake Classifier** | Case routing | Categorizes each intake into the appropriate module(s) and class action(s), scores lead-plaintiff strength | Intake data, class-action rules, `justice_class_actions` |
| **Content Translator** | Multilingual draft | Produces draft translations of legal content, flagged as "machine draft — requires human review" | i18n catalogs, reference translations |
| **Compliance Monitor** | UPL / accuracy / safety | Scans all agent and user-facing output for UPL violations (phrasing that sounds like "legal advice"), hallucinated citations, crisis signals, and defamation risk | Guardrail rules from v2 §1 |

### 1.2 The human advisory board (what they actually do)

Humans are not reviewing every keystroke — agents handle volume. Humans intervene at **gates** where risk is highest:

| Gate | What the human does | Who qualifies |
|---|---|---|
| **Template sign-off** | Reviews a new filing-template type before it's enabled for users. Checks legal accuracy, formatting, and jurisdiction fit. Recorded in `justice_template_reviews` (bar number, date, status). | Licensed FL attorney in the template's practice area |
| **New-jurisdiction launch** | Reviews the statute/rule/contact library and the template set for a new jurisdiction before it goes `live`. | Licensed attorney in that state |
| **Escalation review** | Reviews flagged AI output (Compliance Monitor flags, user-reported issues, confidence < high). | Any board attorney |
| **Incident post-mortem** | Reviews corrections when wrong info reached a user (v3 §6.4 incident response). | Board + MiLyfe community transparency process |
| **Quarterly content audit** | Spot-checks a sample of live content, templates, and AI output for drift/staleness. | Board rotation |

### 1.3 Workflow (agent → human → user)

```
Intake arrives
  → Intake Classifier routes to module(s) + class action(s)
  → Constitutional Scanner produces draft violation report
  → Citation Verifier checks every citation
  → Compliance Monitor scans for UPL / hallucination / crisis
  → Precedent Researcher adds supporting caselaw
  ─── confidence ≥ high AND no flags ───→ user sees report
      (with "not legal advice" disclaimer, "DRAFT" banner)
  ─── confidence < high OR flagged ───→ queued for human review
      → human attorney reviews, corrects, approves or rejects
      → approved → user sees report
      → rejected → user gets a "we couldn't generate a reliable
        report — here's how to reach a free attorney directly"
        warm handoff (no dead end, per v3 §6.3)
```

For **template generation** the gate is stricter:

```
Template Drafter fills case fields into a reviewed template
  → Citation Verifier re-checks all citations against current law
  → Compliance Monitor scans
  → user sees the draft with "DRAFT — attorney review recommended"
  → filing-type must have prior human sign-off (§1.2 gate)
      or the entire template type is blocked for that jurisdiction
```

### 1.4 Error reduction (why this is better than AI alone OR humans alone)

- Agents never hallucinate *citations* into the output because the Citation Verifier kills unverifiable ones before they reach anyone.
- Agents never phrase something as "legal advice" because the Compliance Monitor catches UPL language.
- Humans never have to read every single output — only the edge cases and new template types, so they can focus where their expertise matters most.
- Every agent action is logged and auditable; the harm-vs-help metric (v3 §6.5) runs continuously.

### 1.5 Implementation fit

- Agents run via the platform's existing `ai` SDK (Vercel AI SDK, already in `package.json`) with retrieval-augmented prompts grounded in the legal-content repo and the citation APIs.
- The human review queue is an internal admin UI under `/justice/app/admin/review` (gated to `role = board_attorney` in `justice_case_roles`).
- Agent logs are stored in `justice_agent_logs` (agent_role, action, input_hash, output_hash, citations_checked, flags, confidence, human_review_id).

---

## 2. Advisory-board recruitment plan

### 2.1 Who we need (minimum viable board)

| Seat | Practice area | Why | Count |
|---|---|---|---|
| FL Criminal Defense | felony, misdemeanor, expungement | reviews the Defender + expungement template (Phase 1) | 1–2 |
| FL Immigration | removal defense, ICE | reviews ICE Shield + warrant checker | 1 |
| FL Civil Rights / §1983 | police brutality, conditions of confinement | reviews class-action filings, pattern data | 1 |
| FL Family / Juvenile | juvenile defense, family court | reviews Youth + Juvenile + Women/Family modules | 1 |
| FL Appellate / Post-conviction | habeas, Rule 3.850 | reviews Liberation Engine filings | 1 |

**Total: 5–7 attorneys for Duval/FL launch.** Expandable as jurisdictions and modules grow.

### 2.2 Target sources (Duval / FL)

- **Jacksonville Area Legal Aid (JALA)** — natural first partner; pro-bono infrastructure already exists.
- **Public Defender 4th Circuit (pd4th.org)** — 156-person office, deep local expertise; partnership may be referral-only given their caseload.
- **ACLU of Florida** — active litigation in the exact areas; may contribute review capacity or co-counsel.
- **Florida law-school clinics** — UF Levin (criminal defense clinic), FSU College of Law (public interest), FIU (immigration clinic), Stetson (elder/disability). Clinical faculty can serve on the board; students can assist under supervision.
- **The Florida Bar's pro bono referral** — FL attorneys have a 20-hour/year pro bono aspirational goal; reviewing a template is a low-friction way to contribute.
- **National orgs with FL presence** — Innocence Project of Florida, Southern Poverty Law Center, Americans for Immigrant Justice.
- **Solo/small-firm criminal defense attorneys in Jacksonville** — found through the FL Bar member directory, Duval County Bar Association, and the FACDL (Florida Association of Criminal Defense Lawyers).

### 2.3 The pitch (what we offer vs. what we ask)

**What MiJustice offers:**
- Organized, AI-pre-screened intake referrals (saves their staff from triage).
- Sourced evidence packages for their existing cases/class actions.
- Pattern data for their advocacy and litigation.
- Public credit/attribution as an advisory-board member.
- AI agents that do the research grunt work so their review is focused and fast.

**What we ask:**
- Review and sign off on filing templates in their practice area (one-time per template type, occasional updates).
- Availability for flagged-escalation review (low volume, async, time-boxed).
- Quarterly spot-check participation (a few hours per quarter).

### 2.4 Outreach kit

A one-page brief + partner deck stored in the repo (consistent with v2 §4.3), customized per target:
- What MiJustice is (one paragraph).
- The guardrails (UPL posture, agent-assisted-human model, the sign-off gate).
- The value exchange (what they get, what we ask).
- A sample template for them to review as a "try before you commit."

### 2.5 Finding human translators (Spanish + Haitian Creole)

- FL law-school language-access programs.
- Local community interpreter networks in Jacksonville (large Haitian and Latin American communities).
- HIAS Florida chapter.
- National Association of Judiciary Interpreters and Translators (NAJIT) volunteer/pro-bono pipeline.
- Post on the MiLyfe platform itself — community members who are bilingual + legally literate.

---

## 3. UI/UX Design Spec — MiJustice, inside MiLyfe

Everything below uses the **existing MiLyfe design system exactly as built**: same components, same tokens, same patterns. Nothing new is invented; MiJustice pages look and feel like they were always part of the platform. The only visual distinction is a subtle justice accent (a `Scale` icon from `lucide-react` and a thin gold rule under section headers) that marks you're in the war room.

### 3.1 Design system rules (reuse, don't reinvent)

| Token/component | Source | MiJustice usage |
|---|---|---|
| Colors: `harbor-800` `teal-500` `mly-500` | `tailwind.config.ts` | Used exactly as-is; no new palette |
| Font: Atkinson Hyperlegible | `globals.css` / `tailwind fontFamily` | All type |
| `Button` variants | `ui/button.tsx` | `default` (teal) for primary actions, `harbor` for "Enter the War Room" / serious actions, `mly` for gold CTAs on the landing, `outline` for secondary, `ghost` for toolbar, `destructive` for danger |
| `Card` / `CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter` | `ui/card.tsx` | Module cards, case cards, violation cards, dashboard cards |
| `Badge` variants | `ui/badge.tsx` | `default` (teal) = protected right, `destructive` = violation detected, `success` = resolved/dismissed, `mly` = action needed, `live` (pulse) = active case/tracking, `harbor` = amendment number |
| `EmptyState` | `ui/empty-state.tsx` | No cases yet, no results, module empty |
| `Input`, `Textarea`, `FormField` | `ui/input.tsx` etc. | Intake forms |
| `Tabs` (pill-style) | Learn pattern `rounded-lg bg-muted p-1` | Module sub-tabs |
| `Skeleton` / `shimmer` | `ui/skeleton.tsx` / `globals.css` | Loading states |
| `.page-title` / `.page-subtitle` | `globals.css` | Every page header |
| `.section-header` (left `teal` border) | `globals.css` | Section dividers |
| `.stat-number` (tabular-nums) | `globals.css` | Dashboard counters |
| `.card-glass` / `.nav-glass` | `globals.css` | Glass overlays, Encounter Mode |
| `stagger-children` | `globals.css` | Card grid entrance |
| `lucide-react` icons | `package.json` | All icons |
| 44px min touch, safe-area-bottom, reduced-motion | `globals.css` | Accessibility baseline |

### 3.2 Information architecture (IA)

```
Public (no login):
  /justice                     Landing page (get.milyfe-style)
  /justice/rights              Know Your Rights hub
  /justice/rights/[situation]  Traffic stop, ICE at door, arrest, plea...
  /justice/rights/constitution Full Constitution decoded
  /justice/rights/jury-nullification
  /justice/about               About MiJustice

Gated (MiLyfe login):
  /justice/app/home            ★ Justice Home (launcher + dashboard)
  /justice/app/encounter       ★ Encounter Mode (panic flow)
  /justice/app/defender        Defender intake + report
  /justice/app/case/[id]       Case workspace
  /justice/app/liberation      Liberation Engine
  /justice/app/ice-shield      ICE Defense Shield
  /justice/app/class-actions   Class Action War Room
  /justice/app/knowledge       Knowledge Base (gated tools)
  /justice/app/[module-slug]   All other modules (11–24)
  /justice/app/tracker         Public-aggregate dashboards
  /justice/app/admin/review    Advisory-board review console (board only)
```

### 3.3 Key screens (composition, not code)

---

#### SCREEN 1: Landing page (`/justice`)
*Public, server component, mirrors get.milyfe.html section rhythm.*

**Layout:** full-width, no sidebar/nav (public visitor, not in the platform shell).

| Section | Composition |
|---|---|
| Attention bar | Full-width `bg-harbor-950` strip, uppercase Atkinson, `text-xs tracking-widest` |
| Hero | `bg-gradient-to-r from-harbor-800 to-teal-600`, white circular badge (logo), kicker `Badge variant="harbor"`, H1 with `mly-500` span, two CTAs: `Button variant="mly" size="lg"` "Enter the War Room" + `Button variant="outline"` "Create Free Account" |
| Benefit strip | 3-col grid of icon + `CardTitle` + `CardDescription`, icons in `teal-50` circles |
| What is MiJustice | `.section-header` + prose + `Button variant="default"` CTA |
| "It actually works" | `bg-harbor-950` band, gold stamp `border-mly-500 text-mly-500 rotate-[-3deg]` |
| 24 modules grid | `grid cols-2 md:cols-3 lg:cols-4 gap-3`, each a `Card` with lucide icon + `CardTitle` + one-line `CardDescription` |
| 20 lawsuits | `Card` per lawsuit: `Badge variant="harbor"` for amendment, `CardTitle`, defendants, `Button variant="ghost"` "See if your case fits →" |
| How it works (3 steps) | `Card` with numbered circle (`bg-gradient harbor→teal` text-white), H3, description |
| Proof/stats | `bg-harbor-950`, `.stat-number` in `mly-500` + label |
| Founder note | `Card` with `.section-header`, pull-quote with `border-l-4 border-teal-500` |
| Guarantee | `Card` border-teal, circular seal `bg-gradient harbor→teal` |
| CTA band | `bg-gradient harbor→teal`, `Button variant="mly" size="lg"` |
| P.S. | `Card` |
| Footer | `bg-harbor-950`, same family as get.milyfe |

---

#### SCREEN 2: Justice Home / Launcher (`/justice/app/home`)
*Gated, inside platform shell (Sidebar + TopBar + BottomNav). The war-room dashboard.*

**Layout:** standard platform `space-y-6 p-6`, `max-w-3xl` (inherits from shell).

| Zone | Composition |
|---|---|
| Header | `.page-title` "MiJustice" + `.page-subtitle` "The People's Constitutional War Room" + `Badge variant="live"` "Duval County" |
| Quick-action bar | Row of 4 `Button variant="outline"` icon-buttons: `Shield` Encounter Mode, `Scale` Defend a Case, `FileText` Expungement, `Search` Find an Attorney |
| Active cases | `section-header` "Your Cases" + stacked `Card`s: `CardTitle` = charge summary, `Badge` = status (active/filed/resolved), `CardDescription` = jurisdiction + date, `CardFooter` = `Button variant="ghost"` "Open →" |
| If no cases | `EmptyState` icon=`Scale`, title="No cases yet", description="Start by defending a case or running an expungement check.", action=`Button variant="default"` "Start now" |
| Module launcher | `section-header` "Tools" + responsive `grid cols-2 md:cols-3 gap-3` of `Card` tiles: icon in `teal-50`/`harbor-50` circle + `CardTitle` + `CardDescription` one-liner. Grouped: Defense tools / Liberation / Pressure / Knowledge |
| Live numbers | `section-header` "Impact" + row of `.stat-number` cards: "N cases defended" / "N filings generated" / "N people matched to attorneys" (aggregates only) |

---

#### SCREEN 3: Encounter Mode (`/justice/app/encounter`)
*The panic flow. Designed for one-handed, low-light, offline, shared-device-safe use.*

**Layout:** full-viewport overlay (`card-glass` or opaque `bg-white`), no sidebar (exits shell to maximize screen). Big text, high contrast, zero clutter.

| Zone | Composition |
|---|---|
| Top bar | `Button variant="ghost" size="icon"` `X` close (returns to home) + language selector dropdown |
| Situation picker | 4 large tap targets (entire card is a button, `min-h-[80px]`), each a `Card` with a lucide icon and label: `Car` "Pulled Over", `Home` "ICE at My Door", `Handcuffs` "Being Arrested", `Search` "Being Searched" |
| Rights script | After tap: big text (`text-lg md:text-xl font-bold`) step-by-step: what to say, what not to say, what to do. Each step is a card. Cached offline. Green checkmark when user marks each step read. |
| Record button | Sticky bottom `Button variant="destructive" size="lg"` full-width: `Circle` icon "Record Audio/Video" — one tap to start, stores locally + optional encrypted upload |
| Alert button | `Button variant="mly" size="lg"` full-width: `Bell` icon "Alert My People" — sends prewritten alert with location to rapid-response contacts |
| Warrant checker | `Button variant="outline" size="lg"` "Scan a Warrant" — opens camera/upload for ICE warrant check |
| Duress exit | Triple-tap anywhere → instant exit to phone home screen (configurable) |

---

#### SCREEN 4: AI Constitutional Defender — Intake (`/justice/app/defender`)
*Step-by-step intake form.*

**Layout:** standard platform shell, `space-y-6 p-6`.

| Zone | Composition |
|---|---|
| Header | `.page-title` "Defend Your Rights" + `.page-subtitle` "Answer a few questions. The AI scans every amendment." |
| Progress | `Progress` bar (step N of M) |
| Form steps | One step per card. `Card` with `CardHeader` (step title) + `CardContent` (form fields). Fields use `Input`, radio-pill groups (same pattern as get.milyfe voter-status), `Textarea` for narrative. Each step: "What are the charges?", "State / County", "Circumstances of arrest", "Were your rights read?", "Was there a warrant?", "Was there a search?", "Was counsel provided?", "Was bail set / affordable?", "Was a plea offered / pressured?" |
| Navigation | `CardFooter`: `Button variant="ghost"` "Back" + `Button variant="default"` "Next" / "Analyze My Case" on last step |
| Consent | Final step before submission: UPL acknowledgment checkbox + privacy consent (v2 §1.1 / v3 §2) |

---

#### SCREEN 5: AI Constitutional Defender — Report (`/justice/app/defender/report/[caseId]`)
*The violation report. The payoff.*

**Layout:** standard shell, `space-y-6 p-6`.

| Zone | Composition |
|---|---|
| Header | `.page-title` "Constitutional Analysis" + `Badge variant="live"` "DRAFT — Not Legal Advice" + `Badge variant="harbor"` jurisdiction |
| Summary card | `Card` with `text-gradient` stat: "N violations found across N amendments" + confidence level `Badge` (high/needs-review/uncertain) |
| Violations list | Stacked `Card`s, one per violation: `Badge variant="harbor"` "4th Amendment" + `CardTitle` "Illegal search without warrant" + `CardDescription` plain-English explanation + expandable `CardContent` with case-law citations (each linked, each verified with `Badge variant="success"` "Verified") + matching statutory basis |
| Pre-drafted motions | `section-header` "Your Next Moves" + `Card` per motion: icon (`FileText`), title ("Motion to Suppress"), status (`Badge variant="mly"` "Ready to download"), `Button variant="outline"` "Preview" + `Button variant="default"` "Download PDF". Each carries the "DRAFT — attorney review recommended" banner. |
| Attorney match | `section-header` "Free Legal Help Near You" + `Card` per matched attorney/org: name, practice area, intake method, `Button variant="default"` "Connect" |
| Class-action match | If applicable: `Card` with `Badge variant="mly"` "Your case may fit" + class-action name + `Button variant="ghost"` "Learn more →" |
| Actions bar | Sticky bottom on mobile: `Button variant="harbor"` "Save to My Cases" + `Button variant="outline"` "Share with Attorney" |

---

#### SCREEN 6: Case Workspace (`/justice/app/case/[caseId]`)
*A person's case HQ. Accessible by the case owner, proxy, or shared attorney.*

**Layout:** standard shell. `Tabs` at top for sub-views.

| Tab | Content |
|---|---|
| Overview | Case summary card, current status `Badge`, proxy/attorney list with roles, timeline of events |
| Violations | The violation report from the Defender (same cards as Screen 5) |
| Filings | All generated documents with status (`Badge`: draft / reviewed / filed / outcome), download/preview, "DRAFT" banner on un-filed |
| Deadlines | Advisory deadline list (with the "not authoritative — verify with attorney" caveat per v3 §3.1) |
| Share | Manage who has access: add attorney by email, revoke, view access log |
| Notes | Private encrypted notes (user + shared parties only) |

---

#### SCREEN 7: Advisory-board review console (`/justice/app/admin/review`)
*Internal, gated to `role = board_attorney`.*

**Layout:** standard shell.

| Zone | Composition |
|---|---|
| Queue | Stacked `Card`s of items needing review, sorted by urgency. Each shows: agent role that flagged it, confidence, flag reason, `Badge` for type (template / escalation / audit). |
| Review view | Expand card → side-by-side: AI output on left, source citations on right (each linked to CourtListener / statute). Controls: `Button variant="default"` "Approve" / `Button variant="destructive"` "Reject + Note" / `Button variant="outline"` "Edit & Approve". |
| Audit log | Table of past reviews with reviewer, date, action, notes. |

---

#### SCREEN 8: Public tracker / transparency dashboard (`/justice/app/tracker`)
*Read-only aggregate data. No PII. Accessible even as public link shared from the platform.*

**Layout:** standard shell, wider content area.

| Zone | Composition |
|---|---|
| Header | `.page-title` "Justice Tracker" + `.page-subtitle` "Live data from MiJustice — no personal information" |
| Stat row | `.stat-number` cards: total cases defended, violations found, filings generated, people matched, outcomes (released/dismissed/recovered) |
| Charts | `recharts` (already in `package.json`): violations by amendment (bar), outcomes over time (line), geographic heat map (`maplibre-gl`, already in deps) by county |
| Worst-offender tables | Aggregate only, sourced from public records (per v2 §1.5): "Top 10 jurisdictions by X" — cards with `CardTitle` + `.stat-number` + source link |

---

### 3.4 Navigation injection into MiLyfe

**Sidebar (`src/components/shell/sidebar.tsx`):** add one entry to `NAV_ITEMS`:
```
{ href: '/justice/app/home', label: 'Justice', icon: Scale }
```
Placed after `Safety`, before `Treasury` — groups naturally with civic/safety tools.

**BottomNav (`src/components/shell/bottom-nav.tsx`):** the 5-slot mobile nav is tight; Justice is accessible via the sidebar (on desktop) and through the existing Safety or Apps surfaces on mobile, or by replacing one slot per user preference. Alternatively: a persistent floating action button (FAB) for Encounter Mode on the Safety page.

### 3.5 MiJustice accent (subtle brand layer)

- The `Scale` icon from `lucide-react` is the MiJustice mark; it appears in the sidebar, the launcher, and the landing hero badge.
- A thin `border-b-2 border-mly-500` gold rule under `section-header`s on Justice pages — the only visual flourish that distinguishes Justice from other platform areas.
- "Scales of justice" SVG in the landing hero badge (white circle, same treatment as the get.milyfe brandmark badge).
- Everything else is stock MiLyfe: same white backgrounds, same harbor text, same teal actions, same rounded-xl cards, same Atkinson type.

### 3.6 Mobile-first and offline

- Every screen is designed for `< 375px` first (the platform's existing `pt-14 pb-20 md:ml-56` shell handles this).
- Encounter Mode is the highest-priority offline surface: rights scripts + the warrant-checker logic are cached via the existing service worker + IndexedDB (`dexie`, already in deps).
- KYR public content (`/justice/rights/*`) is marked for offline caching.
- Operational pages degrade gracefully to read-only cached state when offline (show last-synced data, disable write actions, show `OfflineIndicator`).

### 3.7 Accessibility
- Inherits all platform baselines: 44px touch targets, `prefers-reduced-motion`, `aria-current`, `aria-label` on nav, screen-reader-friendly `EmptyState`.
- Encounter Mode: extra-large text, high-contrast (meets AAA for the rights script), no animation by default, voice-over friendly step flow.
- All images/icons have alt/aria-hidden labels. All form fields have visible labels and error messages.

---

## 4. What this means for the build

With v4 complete, the design covers:
- The product (24 modules, 20 lawsuits, FL/Duval localization).
- The guardrails (UPL, citation, safety, governance).
- The human network (advisory board + partners + media).
- The AI system (8 agent roles, human-in-loop gates, error reduction).
- The UI/UX (every key screen, composed from the real MiLyfe component library).

The build plan from v2 §8 (revised) is the concrete next step: Phase 1 = Encounter Mode + public KYR + FL statute library + the data model + sidebar injection → Phase 2 = Defender intake/report + expungement template + advisory-board review console.
