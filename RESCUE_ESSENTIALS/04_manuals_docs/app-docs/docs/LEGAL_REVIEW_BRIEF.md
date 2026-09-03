# MiLyfe Legal Review Brief

**For:** Counsel reviewing $MLY, privacy, and jurisdictional compliance  
**Jurisdiction:** Florida (US-FL) initial deployment; EU awareness required

---

## Key Legal Questions

### 1. $MLY Classification

**Current state:** Practice mode only. No real-world value. Cannot be transferred, sold, or exchanged.

**Live mode questions (for counsel):**
- Is $MLY a "virtual currency" under FL MSB laws (Ch. 560)?
- If peer-to-peer only (MiLyfe does not custody or exchange), is licensure required?
- Does UBI distribution require securities registration?
- Can shops accept $MLY without triggering money transmission?
- The "Bitcoin split": protocol vs user vs doorway — does this analysis hold?

**Design intent:** MiLyfe does NOT operate an exchange. Peer swap is between consenting individuals. A shop that cashes out the public is THEIR regulated booth, not MiLyfe's.

### 2. Children (COPPA/FL)

- Youth mode collects: name, guardian link, learning progress
- Does NOT collect: location, financial data, health, biometrics
- Guardian consent required for profile creation
- Children cannot: send money, vote, message unknown adults, share location
- Emergency access always available regardless of consent state

### 3. Privacy (FIPA / GDPR if EU users)

- All data stored on-device (local-first architecture)
- No server-side storage of messages (E2E encrypted via Matrix)
- Export always available (GDPR Article 20 portability)
- Deletion on request (GDPR Article 17, with exceptions for community records)
- Consent receipts maintained for all data processing
- No advertising, no profiling, no data sales
- No third-party analytics

### 4. Not-a-State Claim

- "Citizen of this commons" = member. Disclaimed every time it appears.
- Compact is association rules, not legislation. 
- Dispute resolution does not replace courts. Criminal process never waived.
- No fake court orders, passports, or government documents generated.

### 5. Liability

- Helper (Mi) is labeled. Not legal advice. Not medical advice.
- Rue says "not a lawyer or the police" every time.
- Court paper assistance: identify document type, show deadline, find legal aid. NEVER "you will win" or "ignore this."
- Resource directory: verified with dates, but not guaranteed. Source shown.

---

## Documents for Review

1. `MiLyfe_COMPLETE.md` — Book A §X (Pocket/$MLY legal nature)
2. `MiLyfe_Blueprint_Gap_and_New_Tech_Audit.md` — Section 3.4 (MiWalk offline money)
3. `src/services/pocket-ledger.ts` — Issuance and settlement logic
4. `src/services/mistage.ts` — Practice/Live boundary enforcement
5. `src/services/legal-resources.ts` — Resource directory with verification
6. `src/services/recovery-engine.ts` — 2-of-3 key recovery
7. `src/services/miappeal.ts` — Due process / appeal flow

---

## Recommended Engagement

- FL money transmission counsel for $MLY live-mode readiness
- Privacy counsel for FIPA compliance certification
- Child protection specialist for COPPA analysis
- IP counsel for OSI license purity (MiCompat gate)
- General liability review of helper disclaimers
