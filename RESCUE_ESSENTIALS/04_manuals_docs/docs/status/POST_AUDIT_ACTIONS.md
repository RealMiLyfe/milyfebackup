# Post-Audit Action Items — 2026-08-30

Generated after the max-depth platform QC audit. These are the remaining items
that require YOUR action (things I couldn't do from inside the workspace).

## 1. Rotate exposed credentials (SECURITY — do soon)

These were pasted in plaintext during the chat session, so treat them as compromised.

| Credential | Value prefix | Action | Where |
|---|---|---|---|
| Token-minting API token "milyfe" | `cfat_W6Ep...` | **Delete** (unused, wrong type) | Cloudflare → My Profile → API Tokens |
| R2 API token (in use as CF_API_TOKEN) | `cfat_jgz2...` | **Roll** after domains stable, then update `hyperbolic-time-chamber/.env` + `systemctl --user restart milyfe-tunnel.service` | Cloudflare → My Profile → API Tokens |
| R2 Secret Access Key | `1acae0eb...` (Access Key ID `542af2a9...`) | **Rotate** (appears nowhere in workspace, safe to roll) | Cloudflare → R2 → Manage API Tokens |

NOT secret / no action: Account ID `76d84af6...` (identifier, not a secret).

## 2. Nameserver switch — DONE (mijaxx.fun LIVE, milyfe.fun activating)

Nameservers set to `athena`/`javon.ns.cloudflare.com` for both zones. Status as of 2026-08-30:

- **mijaxx.fun** — ✅ LIVE. Zone active, SSL cert active, https://mijaxx.fun + https://www.mijaxx.fun
  both serve the mayor campaign site over HTTPS through the tunnel.
- **milyfe.fun** — ⏳ Activating. Public NS already report Cloudflare (propagated), but Cloudflare's
  zone-status poller hasn't flipped it to `active` yet. No action needed — once it flips,
  Universal SSL provisions automatically and `get.milyfe.fun` goes live like mijaxx did.
  Verify later with: `curl -I https://get.milyfe.fun`

## 3. Test suite (DONE — extend over time)

Vitest is now set up in `milyfe-platform/`. Run with `npm test`.
First tests cover the XSS sanitization module (`src/lib/security/sanitize.test.ts`, 10 tests).
Recommended next targets: wallet/treasury transactions, governance voting rules, RLS policy checks.

## 4. Dependency vulnerabilities (from npm audit) — PARTIALLY DONE

Investigated all 13 advisories in `milyfe-platform`. Applied the safe fixes; the rest
need deliberate major-version upgrades (NOT auto-fixed to avoid breaking the app).

DONE (verified: tsc clean, 10 tests pass, production build succeeds):
- Next.js 14.2.15 → **14.2.35** (latest patch in the 14.2 line — security fixes, no breaking API changes).

TRIED + REVERTED (broke the build):
- `@supabase/supabase-js` 2.112.4 and `@supabase/ssr` 0.5.2 introduced cascading TS type
  errors (wallet RPC calls resolving to `never`, cookie handler types). Reverted to the
  working 2.45.4 / 0.5.1. These are LOW severity — not worth the refactor right now.

REQUIRES PLANNED MAJOR UPGRADE (do as a dedicated task, not a quick fix):
- Most remaining highs/criticals need **Next.js 16** (currently 14 → 2 major versions) and
  **vitest 4** (the 1 "critical" is in the dev-only test runner, NOT shipped to users).
- Recommended path: upgrade Next 14 → 15 → 16 incrementally with build+test verification at
  each step; bump vitest to 4 separately. Budget real time for this — it will have breaking changes.

Note: `next build` and the app run fine today; these advisories are mostly SSRF/DoS/cache
hardening in the framework, addressed by the vendor in later majors.

## Reference — what's already wired and working
- Tunnel `milyfe-campaign` (be3c2c88-...) running as user systemd service, enabled, lingering on.
- DNS: get.milyfe.fun, mijaxx.fun (apex), www.mijaxx.fun all CNAME → tunnel (proxied). Mail DNS (DKIM/autoconfig/www on milyfe.fun) set DNS-only.
- Live site served locally by htc-mayor-site on :8180 (host-routed by nginx).
