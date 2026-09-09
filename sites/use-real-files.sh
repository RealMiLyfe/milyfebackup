#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# Swap the generic rebuilt sites for the REAL site files from the
# workspace zip in your phone's Downloads — then redeploy to Vercel.
#
# Handles TWO zip layouts:
#   A) Mirror zip:  mijaxx.fun/ + get.milyfe.fun/ folders (what we have)
#   B) Single-site zip: index.html at root (old public_html style)
#
# PREREQ (one tap): run  termux-setup-storage  and tap Allow.
#
# USAGE:
#   cd ~/milyfebackup/sites
#   bash use-real-files.sh
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "═══ 1. Finding the workspace zip ═══"
if [ ! -d ~/storage/downloads ]; then
  echo "ERROR: phone storage not visible to Termux."
  echo "Run: termux-setup-storage   (then tap Allow on the popup)"
  echo "Then run this script again."
  exit 1
fi
ZIP="$(ls -t ~/storage/downloads/workspace-*.zip 2>/dev/null | head -n 1 || true)"
if [ -z "$ZIP" ]; then
  echo "ERROR: no workspace-*.zip found in Downloads."
  ls ~/storage/downloads/ | head -n 20 || true
  exit 1
fi
echo "Using: $ZIP ($(du -h "$ZIP" | cut -f1))"

echo ""
echo "═══ 2. Unzipping ═══"
rm -rf ~/realthing && mkdir -p ~/realthing
unzip -o -q "$ZIP" -d ~/realthing

echo ""
echo "═══ 3. Detecting the real site files ═══"
ROOT="$HOME/realthing"
# Descend through single-folder nesting (exports love wrapper folders),
# but stop if we already see a site layout.
while [ "$(find "$ROOT" -mindepth 1 -maxdepth 1 | wc -l)" -eq 1 ] \
  && [ -d "$(find "$ROOT" -mindepth 1 -maxdepth 1)" ] \
  && [ ! -f "$ROOT/index.html" ] \
  && [ ! -d "$ROOT/mijaxx.fun" ] && [ ! -d "$ROOT/get.milyfe.fun" ]; do
  ROOT="$(find "$ROOT" -mindepth 1 -maxdepth 1)"
done
echo "Root: $ROOT"
find "$ROOT" -maxdepth 1 | head -n 30

MIJAXX_SRC=""
GETM_SRC=""
GETM_FROM_PAGE=""   # layout B: build get-milyfe from get-milyfe.html

if [ -f "$ROOT/index.html" ]; then
  echo "Layout: single site (B)"
  MIJAXX_SRC="$ROOT"
  [ -f "$ROOT/get-milyfe.html" ] && GETM_FROM_PAGE=1
else
  echo "Layout: mirror with per-domain folders (A)"
  # Prefer clean folders over wget-mirror copies (*_site has cdn-cgi junk)
  if [ -d "$ROOT/mijaxx.fun" ]; then MIJAXX_SRC="$ROOT/mijaxx.fun"
  elif [ -d "$ROOT/mijaxx_site" ]; then MIJAXX_SRC="$ROOT/mijaxx_site"; fi
  if [ -d "$ROOT/get.milyfe.fun" ]; then GETM_SRC="$ROOT/get.milyfe.fun"
  elif [ -d "$ROOT/getmilyfe_site" ]; then GETM_SRC="$ROOT/getmilyfe_site"; fi
fi

if [ -z "$MIJAXX_SRC" ] && [ -z "$GETM_SRC" ]; then
  echo ""
  echo "ERROR: couldn't find the site files in this zip."
  echo "Attach the zip in the Arena chat so it can be inspected by hand."
  exit 1
fi
[ -n "$MIJAXX_SRC" ] && echo "mijaxx source: $MIJAXX_SRC"
[ -n "$GETM_SRC" ] && echo "get-milyfe source: $GETM_SRC"
[ -n "$GETM_FROM_PAGE" ] && echo "get-milyfe source: $ROOT/get-milyfe.html"

echo ""
echo "═══ 4. Backing up generic versions ═══"
rm -rf ~/sites-generic-backup-mijaxx ~/sites-generic-backup-get-milyfe
cp -r "$SCRIPT_DIR/mijaxx" ~/sites-generic-backup-mijaxx
cp -r "$SCRIPT_DIR/get-milyfe" ~/sites-generic-backup-get-milyfe
echo "Backups: ~/sites-generic-backup-mijaxx + ~/sites-generic-backup-get-milyfe"

# Keep any notes about where the mirror came from
[ -f "$ROOT/README.md" ] && cp "$ROOT/README.md" "$SCRIPT_DIR/REAL_FILES_README.md" || true

install_site() {
  local SRC="$1" DST="$2" NAME="$3"
  echo ""
  echo "═══ Installing REAL $NAME files ═══"
  rm -rf "$DST"
  mkdir -p "$DST"
  cp -r "$SRC/." "$DST/"
  # Vercel pretty-URL config (invisible, doesn't change the look)
  echo '{"cleanUrls":true,"trailingSlash":false}' > "$DST/vercel.json"
  echo "$NAME now: $(find "$DST" -name '*.html' | wc -l) pages, $(find "$DST" -type f | wc -l) files total"
}

[ -n "$MIJAXX_SRC" ] && install_site "$MIJAXX_SRC" "$SCRIPT_DIR/mijaxx" "mijaxx"

if [ -n "$GETM_SRC" ]; then
  install_site "$GETM_SRC" "$SCRIPT_DIR/get-milyfe" "get-milyfe"
elif [ -n "$GETM_FROM_PAGE" ]; then
  echo ""
  echo "═══ Building get-milyfe from the real page ═══"
  rm -rf "$SCRIPT_DIR/get-milyfe"
  mkdir -p "$SCRIPT_DIR/get-milyfe"
  cp "$ROOT/get-milyfe.html" "$SCRIPT_DIR/get-milyfe/index.html"
  for d in css js images; do
    [ -d "$ROOT/$d" ] && cp -r "$ROOT/$d" "$SCRIPT_DIR/get-milyfe/"
  done
  echo '{"cleanUrls":true,"trailingSlash":false}' > "$SCRIPT_DIR/get-milyfe/vercel.json"
  echo "get-milyfe rebuilt from the real get-milyfe.html + shared assets."
else
  echo ""
  echo "(no real get-milyfe found — keeping current landing page)"
fi

# If pages use Cloudflare email-protection, bring the decoder along so
# emails still display (copy from wget-mirror variants if present).
for pair in "mijaxx_site:mijaxx" "getmilyfe_site:get-milyfe"; do
  src="${pair%%:*}"; dst="${pair##*:}"
  if [ -d "$ROOT/$src/cdn-cgi" ] && [ ! -d "$SCRIPT_DIR/$dst/cdn-cgi" ]; then
    cp -r "$ROOT/$src/cdn-cgi" "$SCRIPT_DIR/$dst/"
    echo "(+ cdn-cgi email decoder for $dst)"
  fi
done

echo ""
echo "═══ Saving real files to GitHub (backup) ═══"
cd ~/milyfebackup
git add sites/ 2>/dev/null || true
git -c user.name="milyfe-phone" -c user.email="phone@milyfe.fun" \
  commit -qm "Replace generic rebuild with real site files from workspace zip" \
  || echo "(nothing new to commit)"
# GIT_TERMINAL_PROMPT=0: fail fast instead of hanging on a Username prompt.
# The GitHub backup is optional — the Vercel deploy below is what matters.
GIT_TERMINAL_PROMPT=0 git push origin arena/01a07f01-milyfebackup \
  || echo "NOTE: GitHub backup skipped (needs 'gh auth login'). Deploying anyway."

echo ""
echo "═══ Deploying REAL sites to Vercel ═══"
bash "$SCRIPT_DIR/deploy-vercel.sh"

echo ""
echo "═══ DONE — the real branding is live ═══"
