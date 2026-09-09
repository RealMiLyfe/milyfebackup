# mijaxx.fun + get.milyfe.fun — Recovered Files

Pulled live on **2026-09-09**. This workspace started empty, so these files were
re-downloaded from the live domains (workspaces don't share files across
conversations — there is no way to pull directly from "another workspace").

## What's here

### `mijaxx.fun/` — Mayor campaign site (static)
| File | Notes |
|---|---|
| `index.html` | Home — hero, countdown band, petition CTA |
| `about.html` | Journey |
| `platform.html` | Platform |
| `promise.html` | Our Promise |
| `get-involved.html` | Petition + volunteer forms |
| `blog.html` | News |
| `contact.html` | Contact |
| `illuminate.html` | Research |
| `css/style.css` | Main stylesheet (was `style.css?v=7`) |
| `js/main.js` | Nav toggle + scroll animations (was `main.js?v=7`) |
| `js/campaign.js` | Petition/volunteer/email/counter/countdown/Mastodon (was `campaign.js?v=2`) |
| `images/logo.svg`, `images/og-image.svg` | Brand + social card |
| `robots.txt` | Cloudflare-managed robots |

### `get.milyfe.fun/` — "Get MiLyfe" landing site (static, single page)
| File | Notes |
|---|---|
| `index.html` | One-pager: hero, what-changes, 3 steps, FAQ |
| `css/style.css` | Main stylesheet (was `style.css?v=1`) |
| `images/logo.svg`, `images/og-image.svg` | Brand + social card |
| `robots.txt` | Cloudflare-managed robots |

### Raw downloads (for reference)
`mijaxx_site/` and `getmilyfe_site/` are the untouched `wget` mirrors, including
`cdn-cgi/` Cloudflare email-decode scripts and `?v=` cache-buster filenames.
Use the clean `mijaxx.fun/` + `get.milyfe.fun/` folders for editing.

## Backend dependencies (NOT static files — these live elsewhere)

Found in `mijaxx.fun/js/campaign.js`:

- **Campaign API** `https://campaign-api.milyfe.fun`
  - `POST /petition/add`, `GET /petition/status`, `POST /intake/volunteer?...`
  - ⚠️ Currently DOWN (Cloudflare error 1033 as of 2026-09-09).
  - Code comment says: *"Sep 2026 rebuild — API server lost with old PC"*
  - Fallback in code: pre-filled `mailto:contact@milyfe.fun` links.
- **Listmonk** `https://list.milyfe.fun/subscription/form`
  - List UUID: `7d05bab2-85e3-45ab-acf2-b0de27709188`
  - ⚠️ Currently unreachable.
- **Mastodon** `@milyfe` on `mastodon.social` (feed on blog page).
- **Contact fallback**: `contact@milyfe.fun`

If your "other workspace" had the **Campaign API server code** (Python/Node?),
the **Listmonk config/export**, or **deployment configs** (wrangler.toml,
vercel.json, tunnel configs, DNS notes), those are **not recoverable from the
live sites** — only the static frontend is. You'll need to copy those from the
original workspace's file panel directly.

Also live but separate: `milyfe.fun` (Next.js on Vercel — the main platform,
not included here).

## How to move this to your other workspace

1. Download `mijaxx.fun.zip` and `get.milyfe.fun.zip` from this workspace's file panel.
2. In the other workspace conversation, upload / attach the zips and ask the agent to unzip them.
   (Or: open the other conversation and drag the files into it.)

## Preview locally

```bash
cd mijaxx.fun && python3 -m http.server 8000
# open http://localhost:8000

cd get.milyfe.fun && python3 -m http.server 8001
# open http://localhost:8001
```

Note: petition/volunteer/counter features need the Campaign API + Listmonk back
online; otherwise visitors get the email fallback.
