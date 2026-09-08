#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# MiLyfe site recovery — deploy mijaxx.fun + get.milyfe.fun
# to VERCEL from your phone via Termux. Free. ~15 minutes.
#
# PREREQS (one time, in Termux):
#   pkg update && pkg install -y nodejs git
#   (this script installs the Vercel CLI itself on first run)
#
# USAGE:
#   cd ~/milyfebackup/sites
#   bash deploy-vercel.sh
#
# WHAT IT DOES:
#   1. Logs you into Vercel (email link — no passwords/tokens)
#   2. Uploads each rebuilt site as its own Vercel project
#   3. Attaches mijaxx.fun, www.mijaxx.fun, get.milyfe.fun
#
# AFTER THIS: update 3 DNS records in the Cloudflare dashboard
# (phone browser) — the script prints exactly what to set.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "═══ Checking tools ═══"
command -v node >/dev/null || { echo "ERROR: node not found. Run: pkg install -y nodejs"; exit 1; }
command -v npm >/dev/null || { echo "ERROR: npm not found. Run: pkg install -y nodejs"; exit 1; }

if ! command -v vercel >/dev/null 2>&1; then
  echo "Installing Vercel CLI (one time, ~1 min) ..."
  npm i -g vercel
fi

# Optional: export VERCEL_TOKEN=xxx to skip interactive login entirely.
# (Create one in phone browser: vercel.com → Account Settings → Tokens.)
TOKEN_ARGS=()
if [ -n "${VERCEL_TOKEN:-}" ]; then
  TOKEN_ARGS=(--token="$VERCEL_TOKEN")
fi

echo ""
echo "═══ Vercel login ═══"
if [ -n "${VERCEL_TOKEN:-}" ]; then
  echo "Using VERCEL_TOKEN from environment."
  vercel "${TOKEN_ARGS[@]}" whoami
elif ! vercel whoami >/dev/null 2>&1; then
  echo "A login is needed. Enter the EMAIL on your Vercel account"
  echo "(the one tied to your GitHub) at the prompt, then tap the"
  echo "verification link Vercel emails you."
  vercel login
  echo "Logged in as: $(vercel whoami)"
else
  echo "Already logged in as: $(vercel whoami)"
fi

deploy_site() {
  local SRC_DIR="$1"   # local folder, e.g. mijaxx
  local PROJ="$2"      # vercel project name, e.g. mijaxx-site
  shift 2
  local DOMAINS=("$@")

  echo ""
  echo "═══ $PROJ ═══"
  cd "$SCRIPT_DIR/$SRC_DIR"
  echo "Uploading + deploying to production ..."
  vercel "${TOKEN_ARGS[@]}" --prod --yes --name "$PROJ"

  for d in "${DOMAINS[@]}"; do
    echo "Attaching domain $d ..."
    # Subdomains (www.x, get.x) must be added WITH a project, else the
    # CLI errors: "Only apex domains can be added without a project."
    if [ "$(awk -F. '{print NF}' <<<"$d")" -gt 2 ]; then
      vercel "${TOKEN_ARGS[@]}" domains add "$d" "$PROJ" 2>&1 | tail -n 3 || true
    else
      vercel "${TOKEN_ARGS[@]}" domains add "$d" 2>&1 | tail -n 3 || true
    fi
  done
}

deploy_site "mijaxx"     "mijaxx-site"     "mijaxx.fun" "www.mijaxx.fun"
deploy_site "get-milyfe" "get-milyfe-site" "get.milyfe.fun"

echo ""
echo "═══ DONE — now the DNS step (dash.cloudflare.com, phone browser) ═══"
echo ""
echo "Zone milyfe.fun → DNS → edit record 'get':"
echo "  CNAME | get | cname.vercel-dns.com | Proxied (orange cloud ON)"
echo ""
echo "Zone mijaxx.fun → DNS → edit records '@' and 'www':"
echo "  CNAME | mijaxx.fun | cname.vercel-dns.com | Proxied"
echo "  CNAME | www        | cname.vercel-dns.com | Proxied"
echo ""
echo "Keep SSL/TLS mode on Full (strict). Vercel issues certificates"
echo "automatically once DNS points over (~2-15 min)."
echo ""
echo "Check status anytime: vercel domains inspect mijaxx.fun"
