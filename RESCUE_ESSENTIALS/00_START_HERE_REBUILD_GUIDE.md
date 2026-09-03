# MiLyfe — RESCUE ESSENTIALS (Read This First)

This folder holds the **irreplaceable** parts of the MiLyfe build — the stuff you
CANNOT re-download from GitHub. If the old PC is gone, everything you need to bring
the system back is in here, in rebuild order.

Captured: 2026-09-03 from `/home/milyfe/Documents/MiLyfe`

---

## What's here and why it matters

| Folder | What it is | Why it's irreplaceable |
|--------|-----------|------------------------|
| `01_git_history/` | Full git bundles of all 3 repos (ALL commits/branches) | **The root repo has NO GitHub remote** — its history exists only here. Also captures unpushed commits from platform. |
| `02_secrets_env/` | Live `.env` files, keys, and env templates | API keys, DB creds, service secrets. Never on GitHub. Without these nothing connects. |
| `03_databases_state/` | Live SQLite DBs + all 27 Supabase migrations + SQL scripts | The migrations rebuild all 145 tables. The `.db`/`.sqlite3` files hold real campaign + agent data. |
| `04_manuals_docs/` | Every manual, blueprint, roadmap, and project doc | The plans and decisions that got us here. The "how and why." |
| `05_agent_knowledge/` | htc agents, knowledge, data, brain, vault, workflows, config, content | The agent "brain" — research PDFs, memory (chromadb), n8n workflows, agent definitions, drafted-but-unpublished social/blog posts. |
| `06_custom_uncommitted/` | Custom scripts + live data not on any remote | `start-figranium.sh` and the 3D office live `events.json` — would be lost on a fresh clone. |

---

## The 5 git repos (download from GitHub where possible, else restore from bundle)

| Repo | GitHub remote | Notes |
|------|--------------|-------|
| root repo (+ hyperbolic-time-chamber, docs, public_html) | **NONE** | Restore from `01_git_history/root-repo-FULL.bundle`. Most of its working tree is UNTRACKED, so the real files live in the main copy + this rescue folder, NOT the bundle. |
| milyfe-platform | https://github.com/RealMiLyfe/MiLyfe-Universal-OS.git | Had unpushed dep-bump commits — full history in `milyfe-platform-FULL.bundle`. |
| fcc | https://github.com/Alishahryar1/free-claude-code.git | Python/uv project. |
| fcc/figranium | https://github.com/figranium/figranium.git | Custom `start-figranium.sh` is NOT on the remote — see `06_custom_uncommitted/`. |
| hyperbolic-time-chamber/dashboard-3d | https://github.com/0xMerl99/MyClaw3D.git | 3D office. Live `events.json` in `06_custom_uncommitted/`. |

> NOTE: `hyperbolic-time-chamber/dashboard/dist` and `dashboard-3d/dist` are gitignored build output — regenerable, not backed up on purpose.

> The actual source code lives on GitHub for the two above — you do NOT need to hoard it.
> What you need is in THIS folder: history that isn't pushed, secrets, DB schema+data, docs, agent state.

---

## REBUILD ORDER (do it top to bottom)

### Step 0 — New PC prerequisites
Install: `git`, `node` (v18+), `npm`/`pnpm`, `docker` + `docker-compose`, Python `uv`, Supabase CLI.

### Step 1 — Restore the code
```bash
# Projects that ARE on GitHub:
git clone https://github.com/RealMiLyfe/MiLyfe-Universal-OS.git milyfe-platform
git clone https://github.com/Alishahryar1/free-claude-code.git fcc

# The root repo / time-chamber that is NOT on GitHub — restore from bundle:
git clone "01_git_history/root-repo-FULL.bundle" MiLyfe
# (this gives you every commit incl. the unpushed infra/security work)
```
If the platform GitHub is behind, apply the unpushed commits too:
```bash
git clone "01_git_history/milyfe-platform-FULL.bundle" milyfe-platform-full
# then cherry-pick / merge anything newer than origin
```

### Step 2 — Restore secrets
Copy each file in `02_secrets_env/` back to the SAME relative path in the project.
The folder structure is preserved, e.g.:
- `02_secrets_env/milyfe-platform/.env.local` → `milyfe-platform/.env.local`
- `02_secrets_env/hyperbolic-time-chamber/.env` → `hyperbolic-time-chamber/.env`
- `02_secrets_env/hyperbolic-time-chamber/agents/.env` → `.../agents/.env`

### Step 3 — Rebuild the database
```bash
# From milyfe-platform, apply migrations in numeric order (001 → 027):
# Either supabase db push, or run supabase/APPLY_ALL.sql,
# migrations are in 03_databases_state/platform-supabase-migrations/migrations/
```
The live SQLite data (`campaign.db`, `chroma.sqlite3`) goes back to
`hyperbolic-time-chamber/data/` and `.../data/agents/chromadb/`.

### Step 4 — Reinstall dependencies (regenerates the junk I skipped)
```bash
cd milyfe-platform && npm install          # rebuilds node_modules
cd ../milyfe-app && npm install
cd ../fcc && uv sync                        # rebuilds .venv
# htc dashboards:
cd ../hyperbolic-time-chamber/dashboard && npm install
cd ../dashboard-3d && npm install
```

### Step 5 — Restore agent brain + bring up the stack
- Copy `05_agent_knowledge/` back into `hyperbolic-time-chamber/`.
- `cd hyperbolic-time-chamber && ./start.sh` (or `docker-compose up -d`)
- Import n8n workflows from `05_agent_knowledge/workflows/`.

### Step 6 — Read the plan and continue
- `04_manuals_docs/NEXT_SESSION_PROMPT.md` — exact next steps we were on.
- `04_manuals_docs/INDEX.md` — full map of the workspace.
- `04_manuals_docs/docs/planning/MiLyfe_Ultimate_Manual.md` — the complete manual.
- `04_manuals_docs/docs/status/MiLyfe_COMPLETE_STATUS.md` — where the build stood (96 routes, 145 tables, live).

---

## Verifying a git bundle (sanity check before you wipe the old PC)
```bash
git bundle verify 01_git_history/root-repo-FULL.bundle
```
Should say the bundle is OK and list refs.

## Note on this drive (exFAT)
This drive doesn't keep Linux permissions or symlinks. After restoring, you may need:
```bash
chmod +x hyperbolic-time-chamber/start.sh
```
