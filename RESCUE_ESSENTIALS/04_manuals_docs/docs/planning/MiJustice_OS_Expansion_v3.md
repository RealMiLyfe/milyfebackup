# MiJustice — Expansion v3 (Gap-Fill)

## Incarcerated Access · Family/Proxy · User Safety · Provenance · Last-Mile Filing · Governance & Operations

> Companion to `MiJustice_OS_Master_Design.md` and `MiJustice_OS_Expansion_v2.md`. Fills the load-bearing gaps needed before build. Florida/Duval-first, consistent with MiLyfe. No code in this document.

---

## 1. Reaching people who are incarcerated (the delivery-channel gap)

The Liberation Engine only matters if help actually reaches someone inside. People in jail/prison have no open internet. Design for the real channels:

- **Family/proxy as the primary user** (see §2): most action is taken by a loved one on the outside.
- **Physical mail path:** generate print-ready, correctly-formatted packets (with envelope + facility mailing rules + "legal mail" labeling where applicable) so a proxy can print and mail them. This is the most universal channel and works today.
- **Facility tablet / kiosk systems** (Securus/ViaPath/JPay-type): document the reality that these are paid, restricted, and vendor-controlled. MiJustice does not integrate with them at launch; instead it produces content the incarcerated person can request via the facility law library or receive by mail. Track as a later integration only if a facility permits it.
- **Jail law-library handoff:** provide a plain-English "how to ask the law library for this statute/rule/form" guide keyed to Florida.
- **Release-triggered reentry:** the moment someone is released (self- or proxy-reported), Encounter of reentry support (housing, expungement, benefits, voting restoration) activates.
- **Data model:** `justice_delivery` (case_id, channel = mail/proxy/library/tablet, status, tracking notes). No assumption of internet access for the affected person.

---

## 2. Family / proxy / representative accounts

Most real users act on behalf of someone else. This is a first-class model, not an afterthought.

- **Roles per case** (`justice_case_roles`): `self`, `family/proxy`, `attorney`, `advocate`, `translator`. Each role has scoped permissions.
- **Consent & authorization:** a proxy must record the relationship and (where required) authorization; the affected person can revoke access at any time through any channel available to them (including by mail request). Consent state stored in `justice_consent` with timestamps.
- **Minimal exposure:** a proxy sees only what their role needs; sensitive fields (immigration status, whistleblower content) require explicit per-field sharing.
- **Multiple helpers:** a case can have several proxies/advocates; all access is logged and revocable.
- **Account ≠ subject:** the MiLyfe account holder and the person the case is about are distinct records linked by consent.

---

## 3. User-safety & liability hardening

### 3.1 Deadline stance (liability)
- MiJustice **does not track, guarantee, or remind on legal deadlines as authoritative.** Deadlines are shown only as *general educational information* with a loud, persistent "this may be wrong for your case — confirm the exact deadline with a licensed attorney or the Clerk" warning.
- No authoritative-looking countdown timers. The `justice_deadlines` engine from v2 is reframed as advisory-only, and any reminder is explicitly labeled "not legal advice, verify independently."

### 3.2 Retaliation / physical-safety model
For users reporting on ICE, guards, or named officers:
- **Duress/quick-hide:** a one-tap panic-exit that instantly leaves the app for a neutral screen; optional "disguise" mode.
- **Silent notifications:** MiJustice never sends a push/notification that reveals justice activity on a shared or monitored device; default to no lock-screen previews.
- **Pseudonymous/anonymous intake** for highest-risk users (already in v2 §1.4) extended here to the whole safety flow.
- **No metadata leakage:** avoid storing anything (location, contacts) beyond what a chosen action requires; encrypt sensitive reports client-side.

### 3.3 Minors
- Youth/juvenile modules mean under-18 users are foreseeable. Stance: **guardian-mediated by default** — a minor's case is managed through a guardian/advocate proxy account.
- Age screening at intake; age-appropriate, plain-language KYR content for the public tier; **COPPA-aware** data handling (no collection from under-13 without verifiable parental consent).
- No direct minor account creation for operational modules at launch; educational KYR content remains openly readable.

---

## 4. Content provenance, versioning & translation QA

### 4.1 Provenance & "as-of" dating
- Every statute, rule, right, and template shows **"as of [date] · source: [official source]"** and carries version history (`justice_content_versions`).
- A user (or a court) can see exactly what the guidance said on the day they used it — critical for trust and for defending the tool's accuracy.

### 4.2 Translation quality control
- Legal content is **not** published from machine translation alone. Standard: human review by a qualified bilingual reviewer before a legal translation goes live, priority Spanish and Haitian Creole for the Duval region.
- Machine translation may be used for *draft* UI strings, but anything legal carries a "human-reviewed" flag; un-reviewed translations show a caution and link to the English source.

### 4.3 Interpreter / ADA / language-access rights
- Add a KYR guide on the right to a court interpreter and ADA accommodations, and how to request them — a real friction point for the population served.

---

## 5. Last-mile filing reality (Florida/Duval)

Templates alone don't get a document filed. Document and guide the last mile:

- **Notarization:** Florida sealing/expungement requires a notarized application. Provide guidance on notary options (including remote online notarization where valid) and clearly mark which documents need notarization vs. a signature.
- **Certified copies:** step-by-step for ordering a certified disposition from the Duval Clerk (needed for FDLE Certificate of Eligibility).
- **Wet signature vs. e-file:** mark, per document, what can be filed by a self-represented person through the Clerk's e-portal vs. what must be mailed/hand-delivered/wet-signed.
- **Fees & fee-waiver:** show filing fees and the indigency/fee-waiver path so cost isn't a silent barrier.
- **"Where it goes" cover sheet** (from v2) extended with the exact division/address and filing method for Duval.

---

## 6. Governance, accountability & operations

### 6.1 Responsible entity & content authority
- **Entity (decided):** MiJustice is **not** a separate organization. It is part of **MiLyfe — "We The People."** The responsible entity is MiLyfe itself; MiJustice is another part of the same platform, same community, same governance, same "no founder keys" ethos. There is no separate nonprofit to stand up.
- **Content-approval authority:** the **AI Legal Advisory Board that assists a human legal advisory board** (see `MiJustice_OS_Expansion_v4.md` §1). AI agents draft, check, and cite-verify; licensed humans hold final sign-off on legal content and templates (preserves v2 §1.6).
- Decision process (transparent, auditable): proposal → AI agent review/cite-verify → human attorney sign-off → community visibility → publish, with a recorded version history (v3 §4.1).

### 6.2 Volunteer / pro-bono operations
- Workflow for the human network (`justice_volunteers`): apply → verify (Florida Bar status check for attorneys; skills check for translators/advocates) → onboard → assign → track → offboard.
- Capacity signals so matching never routes someone to a full or inactive volunteer.

### 6.3 No-match / warm handoff (no dead ends)
- Every path has a defined fallback: if a case doesn't fit a module, or no attorney has capacity, the user is routed to the next-best resource (legal aid, self-help guide, waitlist, or a general referral) with a clear explanation — never a blank "sorry."
- Track no-match events as a signal of where capacity/partnerships are needed.

### 6.4 Incident response for wrong legal information
- A playbook for when incorrect guidance reaches a user: identify affected users, correct the content (with a version bump per §4.1), notify affected users where possible, and log the incident. Ties to the citation-health checks in v2 §6.6.

### 6.5 Privacy-preserving analytics
- Product metrics without surveillance: aggregate, no third-party trackers on `/justice/app/**`, no per-user behavioral profiles, sensitive modules excluded from analytics entirely. Consistent with v2 §1.4 and MiLyfe's privacy posture.
- Track a **harm-vs-help safety metric**: sampled review of AI/template output for accuracy, and a running count of correction incidents.

### 6.6 Legal-correctness QA
- QA is not just code tests. A review harness for templates and AI output: golden-set legal questions with attorney-verified answers, regression checks when content or models change, and mandatory attorney sign-off before a template type is enabled (v2 §1.6).

---

## 7. Offline & shared-device details
- Define sync/conflict rules for data captured offline (last-write-wins is unsafe for legal drafts; use explicit merge or per-field versioning).
- Shared-device safety ties to §3.2: no previews, optional PIN/biometric lock on the Justice section independent of the MiLyfe session.

---

## 8. Where this leaves us
With v3, the design covers not just the *what* (24 modules, 20 lawsuits, Florida/Duval infrastructure) but the *how it reaches and protects real people*: incarcerated access, the proxy who actually does the work, deadline/retaliation/minor safety, provenance, the last mile to an actual filed document, and the governance/operations to run it responsibly. Remaining items are build-time decisions and human commitments (see the readiness note), not missing design.
