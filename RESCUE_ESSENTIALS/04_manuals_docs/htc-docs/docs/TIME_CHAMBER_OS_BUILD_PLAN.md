# Time Chamber OS — Build Plan

**Version:** 1.0
**Date:** 29 August 2026
**Authority:** This plan governs the redesign and build of the Time Chamber operator OS.
It is subordinate to the MiLyfe UI/UX Blueprint (brand + interaction law) and the
Sovereign Infrastructure Design (the OS-2 Coordination protocols). Where this plan
conflicts with those on brand or rights, they win. Where it conflicts on Time-Chamber
operator behavior, this plan wins.

---

## 1. What the Time Chamber actually is

The Time Chamber is **not** a campaign dashboard. It is the **operator's cockpit for
running a sovereign civic OS and a campaign at the same time — built to the exact same
laws as the platform it serves.**

- **MiLyfe (the platform)** serves the people of Jacksonville: Pocket, Learn, Street,
  Voice, You, Mi. Calm neighborhood utility.
- **The mayoral site** is the public voice — it speaks, collects, recruits.
- **The Time Chamber** is the third thing: where the candidate and a tiny inner circle
  operate — think, decide, produce, and govern the machine that does the work.

### The governing idea

The operator's tool must embody the thing being sold. A campaign built on "machines
serve people, transparency is the default, no power is permanent" cannot run on a chaotic
neon war-room. **How you run the room is the first act of governance** — the most honest
signal of how you'll run the city. So the Time Chamber inherits MiLyfe's laws wholesale.

---

## 2. Inherited law (non-negotiable)

From the MiLyfe UI/UX Blueprint, applied to the operator:

1. **Useful before impressive.** No smart-city spectacle. (The old 26-agent glowing
   constellation is exactly the forbidden spectacle — it is removed.)
2. **Private by default, visible by choice.** Every object wears an audience label,
   always visible, set before it moves.
3. **Plain enough to read aloud.** No jargon. Past-tense plain sentences.
4. **Calm in normal life; unmistakable in danger.** Calm is the resting state; urgency
   is scarce and therefore meaningful.
5. **One home, not seventy products.** Five destinations, one helper (Mi).
6. **Accessibility blocks release.** WCAG 2.2 AA minimum.
7. **The visual brand never impersonates** a bank, court, government, police, or ID.

### Brand inheritance (from the Blueprint §3)

- **Palette:** Deep Harbor `#071E40`, Civic Blue `#0B668C`, Living Teal `#087F73`,
  Life Green `#078B5B`, Mist `#EEF6F5`, Paper `#FBFCFC`.
- **Semantic:** Action `#075E82`, Success `#087448`, Warning `#9A5B00`, Danger `#B4232D`,
  Stage `#6D4BB3`, Offline `#4E5968`, Focus `#135FD1`.
- **Color ratio:** 70% neutral, 20% navy/teal structure, 8% action, 2% warning/danger.
- **Type:** Atkinson Hyperlegible. Tabular numerals for money/dates/counts.
- **Status language:** Not shared / Saved / Still walking / Sent / Arrived / Ended.

---

## 3. The private/public resolution (the spine)

The campaign runs on radical transparency **and** is in a contested race. Both are held
by one rule:

> **Anything that is the public's business is transparent by default. Anything that is
> legitimate campaign craft — or that could endanger a person — is private by default.
> And the line between them is itself visible.**

### The audience model (mirrors the platform's audience chips)

Every object in the Time Chamber wears one of these, set before it moves:

| Level | Meaning |
|-------|---------|
| **Only me** | The candidate's raw thinking, unsent drafts, private notes |
| **Inner circle** | The tiny trusted team |
| **Campaign** | Staff/volunteers who need it to do their jobs |
| **Coalition** | Shared with pledge partners, not yet public |
| **Public** | Published, on the record, irreversible |

### The mapping

**Transparent by default (the public's business):** positions/platform once decided;
money in and out; commitments made and whether kept; the decision *record* for public
choices; citizen input and how it was used.

**Private by default (craft or protected people):** strategy/sequencing/timing;
opposition research *in progress*; debate prep, message testing, internal disagreement;
any real person's PII; coalition negotiations before partners agree to go public;
security-sensitive operational detail.

**The subtle middle — opposition research.** The Watch surface structurally separates
*holding public records accountable* (votes, filings, public statements — legitimate,
often can become public because it is already public record) from *surveilling a private
person* (movements, private life, profiling — the tool has no affordance for it, the same
way the platform's IoT layer cannot render an individual's location).

### Two guardrails

1. **Publishing is a Level-3 decision.** Moving anything to `Public` is the weightiest
   act in the system: re-confirmed, consequence stated plainly, human-gated, produces a
   receipt. The autonomous system may draft toward public; a person always makes the
   crossing.
2. **Every private thing is honestly labeled and auditable.** The system can always show
   the *shape* of what is private (category, never contents) so integrity is proven by
   being honest about what is protected — not by fake total openness.

---

## 4. The five destinations

Chosen by operator need, in priority order — not by what data exists.

1. **Today** — the priority stack applied to governing: crisis first, time-sensitive
   deadlines (petition, qualifying, filings) second, decisions waiting on you third, then
   what the machine did, then opportunities. Card anatomy from the Blueprint §5.2.
2. **Decide** — the heart. Everything the autonomous system wants to do that only a human
   should approve, as a decision with a plain consequence and an appeal-able trail.
   Includes the weightiest decision type: **Make public.**
3. **Produce** — content, research, speeches, positions move through the platform's own
   pipeline: **Idea → Talk → Try → Decide → What happened.** The campaign's content
   lifecycle IS the platform's proposal lifecycle.
4. **Watch** — intelligence, opponent activity, sentiment, field — bound to public records
   and aggregates. Structurally cannot surveil private individuals.
5. **Machine** — the engine room: agents, jobs, health, self-repair over the kernel.
   Demoted to one of five. Most days you don't open it.

**Mi** is the operator's helper here — labeled, sourced, unable to send/spend/publish/
commit alone (OS-5 rails).

---

## 5. Missing tools (what this build adds)

The current build is heavy on *thinking* (agents) and light on the *operational
instruments* a governing-in-public campaign runs on. The gaps, by priority:

### Tier 1 — the transparency + voice + coalition tools (build first)

1. **Public Ledger + Decision Receipts** — a live, plain-language record of money in/out
   and commitments made vs. kept, plus every public decision recorded the MiReceipt way
   (what, why, who's affected, reversible or not). This IS the transparency promise made
   real. Currently absent.
2. **Citizen Voice loop** — structured citizen input intake and the published
   **"you said → we did"** loop, mirroring Idea→…→What happened. The Coalition Proposal's
   "report back" made operational. Currently absent.
3. **Coalition workspace** — a shared space for cross-party pledge partners at the
   `Coalition` audience level, with the signable Transparency & Participation Pledge and a
   signer roster. This is literally the document being drafted (Coalition_Proposal.md).

### Tier 2 — the accountability + honesty registers

4. **What's open / What's held register** — the honest map of what is public and the
   *categories* (never contents) of what is private, with a reason for each. The artifact
   that defends integrity under attack.

### Tier 3 — field, compliance, coalition ops (sequenced later, not in this build unless time permits)

- Volunteer operations with role-scoping; petition→ballot legal-sufficiency pipeline;
  canvassing on public voter-file/aggregates only; event operations.
- Filing calendar + evidence vault; contribution compliance at intake.
- Unified calendar; secure document vault with audience enforcement.

---

## 6. Technical approach

- **Backend:** extend `services/campaign-api` (FastAPI + SQLite) with new routers for the
  audience-labeled records. GET public; writes behind existing auth. Never touches the
  sovereign platform DB. Kernel proxy (`/kernel/*` → agents :8067) already exists for the
  Machine surface.
- **Frontend:** the existing SvelteKit adapter-static SPA served same-origin by
  campaign-api. Replace the generic OS tokens with the real MiLyfe palette + Atkinson
  Hyperlegible. Reuse the kernel client/humanizer/store from prior work where they fit
  the Machine surface; everything else is new.
- **Data model note:** audience is a first-class column on every record. Records also
  carry a plain-language `summary`, a `reason`, and (where relevant) a
  `reversible`/`consequence` for the receipt pattern.

---

## 7. Build phases (execution order, commit at each boundary)

- **A.** Backend foundation: audience model + records (decisions, ledger, pledge/signers,
  voice items, register).
- **B.** Design tokens (real MiLyfe brand) + shell for the five destinations + the
  audience-chip and consequence/receipt components.
- **C.** Today (priority stack) + Decide (decision queue incl. Make-public Level-3 gate).
- **D.** Transparency tools: Public Ledger, Decision Receipts feed, What's-open/What's-held.
- **E.** Citizen Voice loop (input intake + you-said/we-did).
- **F.** Coalition workspace + pledge tracker (audience = Coalition).
- **G.** Watch (public-record-only) + Machine (engine room over kernel).
- **H.** Integrate, refresh static, verify build (svelte-check + build), final commit.

---

## 8. Non-negotiable laws for this build

1. Five destinations. No product explosion.
2. Every object shows its audience before it moves.
3. "Make public" is the weightiest, most deliberate act; it produces a receipt.
4. The system can always show the *shape* of what it keeps private.
5. Watch has no affordance to surveil a private individual.
6. Calm by default; urgency is scarce.
7. Plain language, read-aloud clean; tabular numerals for money/dates.
8. Accessibility (WCAG 2.2 AA) blocks release.
9. The Time Chamber never touches the sovereign platform's data.
10. The brand never impersonates a bank, court, government, or ID.

---

## 9. One-sentence principle

**The Time Chamber is the campaign governing itself by the exact rules it promises to
govern the city by — calm, transparent, human-gated, and tireless — making the public's
business open by default and the campaign's craft private by default, so the way the
candidate runs the machine is itself the proof of the promise.**
