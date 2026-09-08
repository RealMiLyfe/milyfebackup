#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# MiLyfe site recovery — deploy mijaxx.fun + get.milyfe.fun
# from your PHONE via Termux + GitHub Pages. Free. ~15 minutes.
#
# PREREQS (one time, in Termux):
#   pkg update && pkg install -y gh git
#   gh auth login        (choose GitHub.com → HTTPS → paste a token,
#                         or login with browser code)
#
# USAGE:
#   cd ~/milyfebackup/sites
#   bash deploy-termux.sh
#
# WHAT IT DOES:
#   1. Creates RealMiLyfe/mijaxx-site + RealMiLyfe/get-milyfe-site
#      (public repos — required for free GitHub Pages)
#   2. Pushes each rebuilt site to its repo (main branch)
#   3. Enables GitHub Pages + sets the custom domain
#
# AFTER THIS: update 3 DNS records in the Cloudflare dashboard
# (phone browser) — see RECOVERY-PLAYBOOK.md Step 3.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "═══ Checking tools ═══"
command -v gh >/dev/null || { echo "ERROR: gh not found. Run: pkg install -y gh git"; exit 1; }
command -v git >/dev/null || { echo "ERROR: git not found. Run: pkg install -y git"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "ERROR: not logged in. Run: gh auth login"; exit 1; }

OWNER="$(gh api user -q .login)"
echo "GitHub user: $OWNER"

deploy_site() {
  local SRC_DIR="$1"   # local folder with the site
  local REPO="$2"      # repo name, e.g. mijaxx-site
  local DOMAIN="$3"    # custom domain, e.g. mijaxx.fun

  echo ""
  echo "═══ $REPO → $DOMAIN ═══"

  if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
    echo "Repo $OWNER/$REPO already exists — reusing it."
  else
    echo "Creating public repo $OWNER/$REPO ..."
    gh repo create "$OWNER/$REPO" --public \
      --description "Static site for $DOMAIN (rebuilt Sep 2026 after PC loss)" \
      --disable-wiki
  fi

  local WORK
  WORK="$(mktemp -d)"
  echo "Staging files in $WORK ..."
  cp -r "$SCRIPT_DIR/$SRC_DIR/." "$WORK/"
  echo "$DOMAIN" > "$WORK/CNAME"

  (
    cd "$WORK"
    git init -q -b main
    git add -A
    # Termux-friendly identity (local to this repo only)
    git -c user.name="milyfe-phone" -c user.email="phone@milyfe.fun" \
      commit -qm "Rebuilt $DOMAIN site (phone recovery, Sep 2026)"
    git remote add origin "https://github.com/$OWNER/$REPO.git" 2>/dev/null || \
      git remote set-url origin "https://github.com/$OWNER/$REPO.git"
    echo "Pushing to $OWNER/$REPO ..."
    git push -q -f origin main
  )
  rm -rf "$WORK"

  echo "Enabling GitHub Pages ..."
  gh api -X POST "repos/$OWNER/$REPO/pages" \
    -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/' \
    >/dev/null 2>&1 || echo "(Pages may already be enabled — continuing)"

  echo "Setting custom domain $DOMAIN ..."
  if gh api -X PUT "repos/$OWNER/$REPO/pages" -f cname="$DOMAIN" >/dev/null 2>&1; then
    echo "Domain set. GitHub will issue the HTTPS certificate once DNS points here (~5-30 min)."
  else
    echo "NOTE: could not set the domain via API. Set it manually:"
    echo "  repo → Settings → Pages → Custom domain → $DOMAIN → Save"
  fi

  echo "Live soon at: https://$DOMAIN  (after DNS step)"
  echo "Staging URL:  https://$OWNER.github.io/$REPO/"
}

deploy_site "mijaxx"    "mijaxx-site"    "mijaxx.fun"
deploy_site "get-milyfe" "get-milyfe-site" "get.milyfe.fun"

echo ""
echo "═══ DONE — now do the DNS step (Step 3 in RECOVERY-PLAYBOOK.md) ═══"
echo "Then, once each site loads, enforce HTTPS:"
echo "  repo → Settings → Pages → ☑ Enforce HTTPS"
