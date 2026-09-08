# Recovery Playbook — get.milyfe.fun + mijaxx.fun back online (from your phone)

**Status when this was written (Sep 8, 2026):**
- `milyfe.fun` — UP (hosted on Vercel, unaffected). ✅
- `get.milyfe.fun` — DOWN (Cloudflare error). ❌
- `mijaxx.fun` — DOWN (Cloudflare error). ❌

## Why they're down

Both dead sites were served from your old PC:

1. The site files lived in `public_html/` on that PC (never committed to git).
2. A program called `cloudflared` on that PC held a **Cloudflare Tunnel**
   (`milyfe-campaign`, id `be3c2c88-…`) open to Cloudflare's network.
3. Cloudflare DNS points both domains at that tunnel.

PC dead → tunnel dead → Cloudflare has nowhere to send visitors → error page.

Checks done from the backup: `milyfe.fun` resolves to Vercel (good),
both dead domains still resolve to Cloudflare proxy IPs pointing at the
dead tunnel (expected). No Wayback Machine or Common Crawl copies of the
lost pages exist — the sites were too new to be archived.

## What was rebuilt (in this repo, `sites/`)

| Folder | Domain | Contents |
|--------|--------|----------|
| `sites/mijaxx/` | `mijaxx.fun` (+ `www`) | Full 7-page campaign site: Home, Journey, Platform, Promise, Get Involved, News, Contact + Illuminate research page. Original `campaign.js` + original News page restored from git; everything else faithfully rebuilt from the campaign knowledge base. New SVG logo/art (old PNG/JPGs were on the dead PC). |
| `sites/get-milyfe/` | `get.milyfe.fun` | New "Get MiLyfe" landing page → funnels visitors to `milyfe.fun`. |
| `sites/deploy-termux.sh` | — | One-shot deploy script for Termux (below). |

The new hosting is **GitHub Pages** (free, no server to babysit, editable
from your phone). The old tunnel setup is gone with the PC and is *not*
needed anymore for these two sites.

---

## PATH A — Full fix with GitHub Pages (~30 min, recommended)

### Step 1 — Termux setup (one time, ~5 min)

In Termux:

```bash
pkg update && pkg install -y gh git
gh auth login
```

For `gh auth login`, pick: **GitHub.com → HTTPS → Login with a web browser**
(it gives you a code — open `github.com/login/device` in your phone
browser, enter the code, authorize). This avoids typing passwords/tokens
on the phone.

Then get this backup repo onto the phone:

```bash
cd ~
gh repo clone RealMiLyfe/milyfebackup
cd milyfebackup/sites
```

> If the clone asks for credentials, you skipped `gh auth login` — go back.

### Step 2 — Deploy both sites (one command, ~5 min)

```bash
bash deploy-termux.sh
```

This creates two public repos (`mijaxx-site`, `get-milyfe-site`), pushes
the rebuilt sites, enables Pages, and sets the custom domains. It prints
two **staging URLs** like `https://RealMiLyfe.github.io/mijaxx-site/` —
open them in your browser to confirm the sites look right *before*
touching DNS.

### Step 3 — Point DNS at GitHub Pages (phone browser, ~5 min)

Open `dash.cloudflare.com` in your phone browser (desktop-site mode helps).

**Zone `milyfe.fun` → DNS → Records:**
Find the record named `get` (it points to `be3c2c88-….cfargotunnel.com`).
**Edit** it to:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `get` | `RealMiLyfe.github.io` (use YOUR GitHub username) | Proxied (orange cloud ON) |

**Zone `mijaxx.fun` → DNS → Records:**
1. Record `@` / `mijaxx.fun` → **Edit** to `CNAME | mijaxx.fun | RealMiLyfe.github.io | Proxied`
   (Cloudflare auto-flattens apex CNAMEs — this is fine.)
2. Record `www` → **Edit** to `CNAME | www | RealMiLyfe.github.io | Proxied`

Also confirm **SSL/TLS → Overview** is **Full (strict)** or **Full** —
*not* Flexible. (Flexible breaks GitHub Pages HTTPS.)

### Step 4 — Verify + enforce HTTPS (~10–30 min wait)

1. Wait a few minutes, then open `https://mijaxx.fun` and
   `https://get.milyfe.fun`. First load may show a certificate warning
   for a few minutes while GitHub issues the certificate — that's normal.
2. Once both load clean, enforce HTTPS (in a phone browser, or via Termux):
   - `github.com/RealMiLyfe/mijaxx-site` → **Settings → Pages** → ☑ **Enforce HTTPS**
   - same for `get-milyfe-site`.

Done. Both sites are back, on infrastructure that can't die with a PC.

### Step 5 — Later, from any computer (optional cleanup)

- Delete the dead tunnel so it stops confusing things:
  `cloudflared tunnel delete milyfe-campaign`
  (needs the old credentials — if they're lost, delete it in
  dash.cloudflare.com → Zero Trust → Networks → Tunnels.)
- The subdomains `campaign-api`, `analytics`, `blog`, `list` still point
  at the dead tunnel. They need a real server (see "Still down" below).
  Until then the rebuilt sites degrade gracefully (forms fall back to
  email, counters show "—").

---

## PATH B — 5-minute band-aid (optional, do this FIRST if you want the error gone NOW)

In `dash.cloudflare.com` → zone `milyfe.fun` → **Rules → Redirect Rules**
→ Create rule:

- Name: `get-to-platform`
- When: Hostname equals `get.milyfe.fun`
- Then: Redirect to `https://milyfe.fun`, status **302**, preserve path: off.

Same in zone `mijaxx.fun`: Hostname equals `mijaxx.fun` (add `www` too)
→ `https://milyfe.fun`, 302.

This kills the Cloudflare error pages immediately. **Delete these rules**
when Path A is done.

---

## Still down after this (needs a server, NOT phone-fixable today)

These all ran as containers on the dead PC behind the same tunnel:

| Host | Service | Needs |
|------|---------|-------|
| `campaign-api.milyfe.fun` | Petition/volunteer API + counters | VPS + `campaign.db` (lost unless in secrets archive) |
| `blog.milyfe.fun` | Ghost blog | VPS + Ghost data (lost unless in secrets archive) |
| `list.milyfe.fun` | Listmonk email | VPS + list data (same) |
| `analytics.milyfe.fun` | Umami stats | VPS, easily recreated |
| Time Chamber | Whole HTC stack | New PC/VPS + secrets + DBs |

**Confirmed Sep 8, 2026: the secrets/database archive is gone with the PC.**
There is no encrypted copy anywhere. Consequences:

- Petition signatures, volunteer list, email list, blog posts, analytics
  history: **lost**. Counters restart at 0.
- Until a new backend exists, all site forms use a **one-tap email
  fallback** (`contact@milyfe.fun`, pre-filled) — nothing from visitors
  gets lost going forward.
- Fresh-rebuild plan (needs a VPS or new PC, not phone-work):
  1. Tiny VPS ($4–6/mo) or new machine + Docker.
  2. Rebuild `campaign-api` from `milyfe-platform` + HTC sources in this
     backup; fresh SQLite/Postgres; new Listmonk + Umami + Ghost.
  3. New Cloudflare Tunnel (or plain Nginx + Cloudflare proxy) for
     `campaign-api / list / analytics / blog` subdomains.
  4. Point the rebuilt `campaign.js` API_BASE at the new backend, redeploy
     `mijaxx-site` via `deploy-termux.sh`.

Either way, the two public sites above come back regardless — that part
needs no secrets at all.

---

## Editing the sites from your phone later

```bash
cd ~/milyfebackup/sites
# edit files with nano (pkg install nano), then:
bash deploy-termux.sh     # re-pushes everything, ~1 min
```

No build step, no server restart — it's plain HTML/CSS/JS.
