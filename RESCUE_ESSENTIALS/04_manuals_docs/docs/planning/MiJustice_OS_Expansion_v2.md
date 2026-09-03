# MiJustice — Expansion v2

## Guardrails · Encounter Mode · Florida/Duval Localization · Resource Network · Pattern-Detection Knowledge Base

> Companion to `MiJustice_OS_Master_Design.md`. Standalone platform, consistent with MiLyfe, launching in **Florida — Duval County (Jacksonville) first**. No code in this document.

**How this reads with the master doc:** the master doc defines the product, the 24 modules, auth, branding, and the base data model. This v2 adds the safety/legal guardrails, the panic-flow, the real Florida/Duval infrastructure, the human network (attorneys, orgs, journalists, influencers), the law library and templates, and the pattern-detection engine — plus concrete places to inject MiJustice into MiLyfe.

**Source note:** the Florida/Duval and tooling references below were gathered from live public sources (court, clerk, sheriff, FDLE, and nonprofit sites) and summarized. Content was rephrased for compliance with licensing restrictions. All contacts/URLs must be re-verified at build time and kept fresh by the maintenance process in §6.6.

---

## 1. Legal & Ethical Guardrails (ship-blocking — nothing goes live without these)

MiJustice generates legal documents and tells people their rights may have been violated. That is powerful and, done carelessly, dangerous — both to users and to the project's survival. These guardrails are non-negotiable.

### 1.1 Unauthorized Practice of Law (UPL) posture
- MiJustice provides **legal information and self-help document assembly**, not legal advice, and does not form an attorney–client relationship until a licensed attorney explicitly takes a case.
- Persistent, plain-language disclaimer on every module and every generated document: *"This is legal information and a self-help tool, not legal advice. It was prepared with software, not by an attorney. Have a licensed attorney review anything before you file it."* Shown in the user's language.
- Every generated filing carries a visible "DRAFT — attorney review recommended" banner and a cover sheet explaining it was self-assembled.
- The "AI Constitutional Defender" frames output as *"possible issues to raise with a lawyer,"* never *"your case will win."*
- One-time onboarding acknowledgment (stored in `justice_consent`) that the user understands this is not legal advice.

### 1.2 AI accuracy & citation verification (anti-hallucination)
- **No unverified citations, ever.** Every case, statute, or rule the AI cites must be resolved against a real source (CourtListener/Free Law Project API for caselaw; official Florida Statutes for statutes) before it is shown. Unverifiable citations are dropped and flagged, not displayed.
- Confidence labels on AI output: *high / needs review / uncertain*. Anything below "high" is gated behind an explicit "show me anyway, I understand this is unverified" step.
- Retrieval-grounded generation: the model answers from the vetted `mijustice-legal-content` library and verified lookups, not from open-ended recall.
- Human-review queue: generated filing templates for a new charge type or jurisdiction are not enabled for users until a licensed attorney in that area signs off (see §1.6).
- Every AI answer logs its sources so a reviewer can audit it.

### 1.3 Mandatory-reporting & crisis handling
- Intake and free-text fields are scanned for crisis signals (self-harm, imminent danger, child safety). On detection: surface 988 / local emergency resources immediately, do **not** silently store the flagged content in plain text, do not auto-forward to third parties, and never make the user feel surveilled.
- Clear boundary: MiJustice is not a mandated reporter and not an emergency service; the UI says so and always points to real emergency help.

### 1.4 Data-breach threat model (this data is uniquely sensitive)
Case data can include immigration status, active charges, and whistleblower identities. Design so a breach or subpoena yields as little as possible:
- **Data minimization:** collect only what a module needs; default retention windows; auto-purge drafts after a case closes unless the user opts to keep them.
- **Client-side encryption by default** for the most sensitive free-text (personal narrative, immigration status, whistleblower reports) — MiJustice stores ciphertext it cannot read; only the user and explicitly shared attorneys hold keys.
- **Documented subpoena/warrant response policy:** what we hold, what we can and cannot produce, user notification where legally permitted, and a transparency report. If we can't read it, we can't be compelled to hand over readable copies.
- **RLS everywhere**, revocable `justice_case_shares`, no third-party analytics or ad trackers on `/justice/app/**`, and no selling of data — consistent with MiLyfe's `PRIVACY.md`/`SECURITY.md`.
- Anonymous/pseudonymous intake option for the highest-risk users (ICE, whistleblower).

### 1.5 Defamation-aware public data
The trackers name judges, prosecutors, officers, and departments. To keep that lawful and credible:
- Publish **only** facts sourced from public records (court dockets, official disclosures, published opinions) with the source cited on every data point.
- Distinguish *documented outcomes* (a court found a Brady violation) from *allegations/patterns* (this office has N pending complaints). Never state opinion as fact about a named individual.
- A correction/dispute process and a takedown path for demonstrated inaccuracies.
- Aggregate/statistical framing wherever possible; individual call-outs require the strongest sourcing.

### 1.6 Legal advisory board sign-off gate
- Stand up a legal advisory board (target: Florida-barred attorneys + at least one from each priority module area). Recruitment is part of §5.
- **Hard dependency:** no auto-generated filing type is enabled for a jurisdiction until a licensed attorney in that jurisdiction has reviewed the template. Tracked in `justice_template_reviews` (template, reviewer, bar number, date, status).

### 1.7 Jurisdiction phasing (accuracy over reach)
- Launch **Florida / Duval County only**, done accurately, before claiming coverage elsewhere. The UI clearly states current coverage and marks other areas "coming soon / general information only."
- Everything jurisdiction-specific (statutes, rules, forms, contacts, deadlines) is keyed to a jurisdiction record so expansion is additive, never a rewrite (see §3.1).

---

## 2. Encounter Mode, Accessibility, Anti-Abuse, Metrics, Funding

### 2.1 Encounter Mode — the panic flow (first-class feature)
The tool people actually reach for mid-encounter. One tap from the home screen and the lock screen shortcut:
- **Your rights, right now:** the correct script for the situation (traffic stop / ICE at the door / arrest / search) in the user's language, big high-contrast text, readable one-handed, works fully **offline** (cached via the platform's existing service worker + IndexedDB).
- **Record:** one-tap audio/video capture with timestamp; optional automatic upload to encrypted storage so evidence survives even if the phone is taken.
- **Alert my people:** notifies pre-set rapid-response contacts (and, for ICE, the community rapid-response network) with location and a prewritten message.
- **What to say / not say:** the "remain silent, ask for a lawyer, do not consent to a search, am I free to go?" essentials.
- **Warrant checker shortcut:** jump straight to the ICE/search warrant scanner (Module 3).
- Designed to work with no signal, low battery, and a locked account (the rights scripts are public-tier content, so they load without login).

### 2.2 Accessibility
- Target **WCAG 2.2 AA**. Reuse Atkinson Hyperlegible (already the platform default), full keyboard nav, screen-reader labels, high-contrast/large-text modes, captions/transcripts for any video KYR content.
- Note: full WCAG conformance requires manual testing with assistive technologies and expert review, not just automated checks — that testing is part of the release checklist.
- Plain-language first (aim for a low reading level); every legal term has a tap-to-define plain-English tooltip.

### 2.3 Anti-abuse & moderation
- Reuse the platform's existing Upstash rate limiting on intake, alerts, and document generation.
- Rapid-response alerts require a verified account and are rate-limited to prevent false-alarm weaponization; repeat false alerts throttle/suspend.
- Human-in-the-loop before any user-submitted content becomes public in the violation database; naming individuals requires the §1.5 sourcing standard.
- Abuse-reporting and a moderation queue consistent with MiLyfe's community guidelines.

### 2.4 Success metrics (outcomes, not just activity)
Track impact, not vanity volume, in `justice_outcomes`:
- People released / detentions ended; cases dismissed or charges dropped; property recovered ($ and count); records sealed/expunged; class members successfully joined to certified actions; attorney matches that became representation; petitions delivered and legislative movement.
- Dashboards show both the funnel (intake → report → filing → outcome) and the human total ("N neighbors home").

### 2.5 Funding & sustainability ("free forever," credibly)
- "100% free to users" is the promise; sustainability comes from: individual donations, foundation/justice grants, court-awarded attorney's fees flowing to partner firms (not to MiJustice), and the platform's existing MiLyfe community model. No paywalls, no data sales, no premium tier — ever.
- Open-source + decentralized hosting keeps run costs low and prevents single-point shutdown, consistent with Module 7.

---

## 3. Florida + Duval County localization (launch jurisdiction)

MiJustice launches in Florida's **Fourth Judicial Circuit → Duval County (Jacksonville)**. Everything jurisdiction-specific is keyed to a jurisdiction record so other counties/states are added as data, never as a rewrite.

### 3.1 Jurisdiction data model
`justice_jurisdictions` (hierarchical): `country → state → circuit → county → municipality`, each carrying the applicable statutes set, court rules set, forms/templates set, agencies, deadlines, and coverage status (`live` / `general-info-only` / `coming-soon`). Duval is the first `live` record; the UI banner reflects coverage per §1.7.

### 3.2 Duval County / 4th Circuit infrastructure directory (seed data — re-verify at build)
Stored in `justice_agencies` and `justice_contacts`. *(Public-record contacts; verify before publishing and refresh per §5.6.)*

| Entity | Role | Public source |
|---|---|---|
| Fourth Judicial Circuit Court | Trial court for Duval, Clay, Nassau (one of FL's largest circuits) | jud4.org — includes Duval judges' individual division procedures |
| Duval County Clerk of Courts | Case records, filings, certified dispositions; **CORE** online records ePortal | duvalclerk.com · core.duvalclerk.com · felony criminal court services; Downtown Courthouse, 501 W. Adams St., Jacksonville |
| State Attorney, 4th Circuit | Prosecution | sao4th.com |
| Public Defender, 4th Circuit | Indigent defense (Duval/Clay/Nassau) | pd4th.org · 904-255-HOPE |
| Jacksonville Sheriff's Office (JSO) | Policing, jail, inmate search | jaxsheriff.org · **transparency.jaxsheriff.org** (open-data portal: officer-involved shootings w/ export, inmate search, updated daily) · Public Records Unit 904-630-2209, 501 E. Bay St., Jacksonville 32202 |
| FDLE — Seal & Expunge Section | Certificate of Eligibility (required first step) | fdle.state.fl.us seal-and-expunge-process · SEinfo@fdle.state.fl.us |

The **judges directory** captures each Duval division's judge and posted division procedures (published on jud4.org), so a user's filing follows the *actual* division rules — a real differentiator most tools miss.

### 3.3 Florida law library
`justice_statutes` + `justice_rules`, sourced from official/free-access references and citation-verified per §1.2:
- **Florida Statutes** — official at the Legislature's site (updated annually, ~July/August); Chapter 900-series = Criminal Procedure. Mirrored/linked, never scraped in violation of terms.
- **Florida Rules of Criminal Procedure** — via the Florida Bar / Florida Courts official rules.
- **Priority seed statutes for Duval launch:** §943.0585 (expunction) and §943.059 (sealing) — one lifetime, FDLE Certificate of Eligibility required first, certified disposition needed from the Clerk; bail/pretrial-release provisions; speedy-trial rule (Fla. R. Crim. P. 3.191); the FL "25-foot" law near officers (relevant to KYR and recording rights); civil-forfeiture provisions; and the fees/costs provisions behind debt-based detention.
- Each record: citation, plain-English summary, per-language translation, linked module(s), linked template(s), and a "last verified" date.

### 3.4 Florida-specific templates & flows (attorney-reviewed before enabling — §1.6)
`mijustice-doc-templates`, keyed to Duval/4th Circuit formatting and the correct division:
- **Record sealing/expungement packet:** FDLE Certificate-of-Eligibility application walkthrough → certified-disposition request to the Duval Clerk → petition + proposed order in 4th Circuit format. (This is the highest-volume, highest-impact, lowest-risk first template — pairs with Code for America's Clear My Record.)
- Motion to suppress (4th Am.); motion to dismiss; discovery/Brady demand; indigency/ability-to-pay declaration (debtors'-prison defense); pretrial-release/bond motion; Rule 3.850 post-conviction motion; Rule 3.191 speedy-trial notice; small-claims/property-recovery for forfeiture; public-records requests to JSO and agencies.
- Every packet includes a plain-English "what this is, where to file it, what happens next, and the deadline" cover sheet.

### 3.5 Florida deadlines engine
`justice_deadlines` seeded with FL/4th-Circuit timelines (speedy trial, FTCA administrative-claim windows for federal matters, appeal windows, statute-of-limitations clocks). Feeds reminders and the Class Action War Room. Deadlines are advisory with a loud "confirm with an attorney" note (§1.1).

---

## 4. Resource & Partnership Network (people who add value)

The ask: more resources — attorneys, organizations, journalists, media, influencers, and anyone who can provide value. This becomes a first-class, structured, growing network inside MiJustice, not a static list.

### 4.1 Network data model
- `justice_partners` — orgs (legal, reentry, immigrant defense, disability, LGBTQ+, veterans, tribal, tech). Fields: name, type, coverage area, services, intake method, capacity/availability, verified status, contact.
- `justice_attorneys` — pro-bono/low-cost attorneys and firms: practice areas, bar number (verified against The Florida Bar), languages, jurisdictions, current capacity, referral method. **Verification required before a match is shown.**
- `justice_media` — journalists/outlets/influencers: beat, outlet, reach, contact, past coverage, preferred pitch format.
- `justice_referrals` — case → partner/attorney routing with status and outcome (feeds §2.4 metrics).
- CRM-style outreach pipeline (`justice_outreach`): prospect → contacted → onboarded → active, so coalition-building is tracked, not ad hoc.

### 4.2 Duval/Florida launch network (seed targets — outreach list)
*Contacts are public-record/organizational; verify and get consent before publishing or routing to them.*

**Legal & rights orgs:** ACLU of Florida (aclufl.org; statewide, immigrants'-rights KYR, active ICE-detention litigation) · Jacksonville Area Legal Aid (JALA — free civil legal aid for low-income Duval residents) · Public Defender 4th Circuit (pd4th.org) · Florida Justice Institute · Southern Poverty Law Center (FL presence) · Florida Rights Restoration Coalition (voting-rights restoration) · Americans for Immigrant Justice · local immigration clinics.

**Reentry & community:** RESTORE (transitional housing + wraparound for women returning from prison, Jacksonville) · Operation New Hope (Ready4Work/Ready4Release job & reentry) · local reentry councils and faith-based networks.

**National legal backbone (from the coalition list):** ACLU, NAACP LDF, EJI, CCR, NARF, Ben Crump Law, National Immigration Project, Innocence Project (+ Florida innocence orgs), Brennan Center, Vera Institute, Public Justice, Lambda Legal, Disability Rights Advocates, National Veterans Legal Services Program, HIAS.

**Media & journalists (accountability beat):** The Tributary (jaxtrib.org — nonprofit investigative, criminal-justice coverage) · Jacksonville Today (jaxtoday.org — nonprofit public-service/accountability journalism, INN member) · The Florida Times-Union (jacksonville.com) · WJCT public media · plus national justice desks (The Marshall Project, ProPublica, Bolts) for pattern stories.

**Academic/clinical:** Florida law-school clinics (e.g., UF, FSU, FIU, Stetson) for research capacity, template review, and student pro-bono; criminology departments for the pattern-detection work in §5.

**Influencers/messengers:** directly-impacted advocates, faith leaders, local organizers, and the founder's own lived-experience story (the honest voice already in the get.milyfe founder letter) — routed through the Political Pressure Engine (Module 9) and the media pipeline.

### 4.3 Outreach kit
A shareable one-pager + partner deck describing MiJustice, the guardrails, and the value exchange (free intake, organized evidence packages, referral traffic, pattern data for advocacy). Stored in the repo; used by the outreach pipeline. Every partnership is opt-in and consent-based.

---

## 5. MiLyfe integration — standalone platform, with direct injection points

MiJustice stands on its own (`justice.milyfe.fun`, its own repos, its own brand face) **and** shows up inside MiLyfe where it adds value, using the shared login and shell.

### 5.1 Direct injection points into MiLyfe
- **Sidebar / launcher:** a "Justice" entry in the existing `Sidebar`/`BottomNav` (same nav pattern as Home, Learn, Safety) → `/justice/app/home`.
- **Safety module (`/safety`):** surface Encounter Mode + Know-Your-Rights cards; the safety area is the natural home for the panic flow.
- **Learn (`/learn`):** publish the Constitution-decoded and jury-nullification content as MiLyfe learning tracks (public tier, offline-cached).
- **Governance / Voice (`/governance`):** wire the Political Pressure Engine's petitions, congressional scorecards, and the 18 legislative demands into the existing civic-voice surface.
- **Wallet / Rewards:** civic actions (completing KYR training, verified volunteer legal work, translation contributions) can earn the existing $MLY credits — ties MiJustice into MiLyfe's economy.
- **Mi (assistant) + CommandSearch:** the ambient `MiBubble` and Cmd+K search can answer "know your rights" and open the right module.
- **Transparency (`/transparency`):** the public outcome/violation dashboards render alongside the platform's existing transparency surface.
- **News (`/news`):** MiJustice wins/cases feed the platform news + the media pipeline.

### 5.2 Shared vs. separate
- **Shared:** one Supabase project, one auth, one design system, one PWA/offline layer, one Mi assistant.
- **Separate:** MiJustice's own public landing, its own repo family, its own `justice_*` tables with stricter RLS/encryption, and its own advisory-board governance for legal content.

---

## 6. Pattern-Detection Knowledge Base

The strategic core: turn many individual cases + public records into **patterns** — which judges, prosecutors, officers, courts, and agencies produce which outcomes — so MiJustice can spot systemic abuse, strengthen class actions, and arm journalists and advocates with evidence.

### 6.1 What we're detecting
- Sentencing/bail disparities by judge, controlling for charge and history.
- Prosecutor charging/plea patterns by office and demographic.
- Officers/units with repeated force complaints, suppressed-evidence rulings, or overturned cases.
- Courts/divisions with unusual conviction, dismissal, or continuance rates.
- Fee/fine-driven jailing concentrated in specific jurisdictions (debtors'-prison signal).
- Repeat Brady violations, denied-counsel patterns, speedy-trial breaches.
- Facial-recognition / predictive-policing arrests and their error rates.

### 6.2 The knowledge graph (data model)
A graph linking entities so patterns surface across cases, not just within one:
- **Nodes:** `person/case`, `charge/statute`, `judge`, `prosecutor`, `defense`, `officer`, `agency`, `court/division`, `jurisdiction`, `caselaw`, `violation-type`, `outcome`.
- **Edges:** presided-over, prosecuted-by, arrested-by, charged-under, resulted-in, cited, violated, filed-in.
- Stored as `justice_kb_nodes` + `justice_kb_edges` in Supabase (Postgres handles this well; a graph view/materialized paths layer powers queries). Optionally mirror to the platform's existing Meilisearch for fast search and to Neo4j if the campaign stack adds it (already flagged in the platform roadmap).

### 6.3 Sources feeding the graph
- **User cases** (consented, RLS-protected; only de-identified aggregates ever surface publicly per §1.5).
- **Public court records:** Duval Clerk CORE ePortal, 4th Circuit dockets.
- **Officer data:** JSO transparency portal (officer-involved shootings export, etc.).
- **Caselaw + federal dockets:** CourtListener / RECAP / Free Law Project API (also powers §1.2 citation verification).
- **Standardized county metrics:** Measures for Justice Commons; Recidiviz / Justice Counts; Vera data explorer.
- **Statutes/rules:** official Florida Statutes + Rules of Criminal Procedure.

### 6.4 Methods
- Entity resolution (match the same judge/officer/case across sources) with human confirmation for public claims.
- Rate/disparity analysis with appropriate controls; always show sample size and uncertainty.
- Anomaly detection to flag outliers for human review — never auto-publish an accusation.
- Every public pattern links back to its underlying public-record sources (defamation guardrail §1.5).
- Feeds: Class Action War Room (evidence + lead-plaintiff identification), Liberation Engine (who's held unconstitutionally), the public trackers, and the media pipeline.

### 6.5 Outputs
- **For users:** "cases like yours before this judge/court tend to…" context (framed as information, not prediction of their outcome).
- **For attorneys/partners:** exportable, sourced evidence packages.
- **For journalists:** sourced pattern briefs (Module 9 media engine).
- **For the public:** aggregate dashboards (no PII) on the Transparency surface.

### 6.6 Maintenance & freshness process
Legal data goes stale and wrong data harms people. Standing process:
- **Annual statute refresh** when Florida Statutes republish (~July/August); rules refresh on Florida Courts amendments.
- **Contact/agency re-verification** on a fixed cadence (e.g., quarterly) with "last verified" dates shown in-app.
- **Template re-review** by the advisory board whenever a rule or form changes (§1.6).
- **Citation health checks** run continuously against the caselaw API; broken/overruled citations are flagged.
- Community contributions to `mijustice-legal-content` go through maintainer + attorney review before merge.

---

## 7. Additional resources & tools discovered (what each adds)

Beyond the vision's original list, research surfaced concrete, real, mostly-free/open assets. Recommended adoptions:

**Legal data & citation integrity**
- **Free Law Project — CourtListener / RECAP** (courtlistener.com, REST API v4, open-source, even an MCP client for AI tools): millions of opinions, dockets, judges, and **citation verification**. → Powers §1.2 anti-hallucination *and* the caselaw layer of the knowledge graph. High priority.
- **Official Florida Statutes** (Legislature site) + **Florida Courts / Florida Bar rules**: authoritative statute/rule text for the library and verification.
- **FDLE Seal & Expunge** process + **Code for America Clear My Record**: back the highest-impact first template (expungement/sealing).

**Criminal-justice metrics & transparency (pattern detection)**
- **Measures for Justice — Commons**: standardized county-level prosecutor/court metrics (covers Florida) for like-for-like comparisons. → disparity baselines.
- **Recidiviz** (open-source `pulse-data`, Justice Counts, public dashboards): data-platform patterns and standardized agency metrics. → graph + trackers, and an integration/partnership target.
- **Vera Institute** Incarceration & Inequality data explorer: geographic incarceration/economic context.
- **JSO Transparency Portal** (transparency.jaxsheriff.org): local officer-involved-shooting and inmate data with exports — a rare, directly-usable local source.

**Local network already identified (Duval)**
- Courts/agencies: 4th Judicial Circuit (jud4.org, with per-judge division procedures), Duval Clerk CORE ePortal, State Attorney 4th (sao4th.com), Public Defender 4th (pd4th.org).
- Orgs: ACLU of Florida, Jacksonville Area Legal Aid, RESTORE, Operation New Hope, Florida Rights Restoration Coalition.
- Media: The Tributary, Jacksonville Today, Florida Times-Union, WJCT.
- Academic: Florida law-school clinics for template review + student pro-bono.

**Enhancement ideas worth adding (from adjacent tools)**
- **Docket alerts** (CourtListener-style): notify users/attorneys when something moves on a matching case.
- **Public-records-request automation** (JSO/agency FOIA generator) — feeds both defense and the pattern graph.
- **"Cases like yours" context** surfaced responsibly (information, not prediction).
- **MCP-based legal research** so the Mi assistant can pull grounded, cited answers instead of guessing.
- **Bulk-import pipelines** for the standardized datasets above to seed the graph before user volume exists.

**What to still investigate at build time**
- Terms/rate limits and licensing for each data source (some APIs are membership-based; scraping court sites may violate terms — prefer official APIs/bulk data).
- Florida Bar rules on lawyer-referral services and UPL as they apply to attorney matching (shape §1.1 / §4.1).
- Whether to add Neo4j to the existing Docker stack for the graph, vs. Postgres-only to start.

---

## 8. Canonical rollout — 7 phases (Florida/Duval-first, guardrails-first)

> **This is the single authoritative build sequence for MiJustice.** The Master Design §10 module list is a coverage map that defers to this plan. Total: **7 phases.**

1. **Foundation:** guardrails (§1) wired as platform primitives; consent + disclaimer flow; jurisdiction model with Duval as first `live` record; recruit legal advisory board.
2. **First real value:** Encounter Mode (offline KYR + record + alert) in the Safety surface; public Constitution-decoded + KYR content in Learn; Florida statute/rule library with citation verification.
3. **First template:** expungement/sealing packet (FDLE CoE → Duval Clerk disposition → 4th Circuit petition), attorney-reviewed, paired with Clear My Record.
4. **Defender + matching:** AI Constitutional Defender (retrieval-grounded, verified citations) → attorney/partner referral with verification.
5. **Knowledge graph v1:** seed from public records + standardized datasets (CourtListener, MFJ, Recidiviz, JSO), launch first aggregate transparency dashboard.
6. **Network + media:** run the outreach pipeline; onboard partners/attorneys/journalists; wire Political Pressure Engine into MiLyfe Governance.
7. **Expand:** additional templates and modules, then additional Florida circuits, then other states — additively, each behind the accuracy gate.

Throughout: 100% free, open source (AGPL-3.0), privacy-first, multilingual, mobile-first, offline-capable, community-governed — consistent with MiLyfe.
