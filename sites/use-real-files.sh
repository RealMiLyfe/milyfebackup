#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# Swap the generic rebuilt sites for the REAL site files from the
# workspace zip in your phone's Downloads — then redeploy to Vercel.
#
# PREREQ (one tap): run  termux-setup-storage  and tap Allow.
#
# USAGE:
#   cd ~/milyfebackup/sites
#   bash use-real-files.sh
#
# WHAT IT DOES:
#   1. Finds the newest workspace-*.zip in Downloads, unzips it
#   2. Auto-detects the real site root (handles extra nesting)
#   3. Backs up the generic versions to ~/sites-generic-backup-*
#   4. Installs real files over sites/mijaxx (+ builds get-milyfe
#      from the real get-milyfe.html + shared css/js/images)
#   5. Commits + pushes the real files to GitHub (backup)
#   6. Redeploys both Vercel projects (domains + certs carry over)
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
echo "═══ 3. Detecting the real site root ═══"
ROOT="$HOME/realthing"
# Descend through single-folder nesting (workspace exports love wrappers)
while [ "$(find "$ROOT" -mindepth 1 -maxdepth 1 | wc -l)" -eq 1 ] \
  && [ -d "$(find "$ROOT" -mindepth 1 -maxdepth 1)" ] \
  && [ ! -f "$ROOT/index.html" ]; do
  ROOT="$(find "$ROOT" -mindepth 1 -maxdepth 1)"
done
echo "Site root: $ROOT"
echo "--- top of tree ---"
find "$ROOT" -maxdepth 2 | head -n 40
if [ ! -f "$ROOT/index.html" ]; then
  echo ""
  echo "ERROR: no index.html found — this zip doesn't look like the site."
  echo "Attach the zip in the Arena chat so it can be inspected by hand."
  exit 1
fi

echo ""
echo "═══ 4. Backing up generic versions ═══"
rm -rf ~/sites-generic-backup-mijaxx ~/sites-generic-backup-get-milyfe
cp -r "$SCRIPT_DIR/mijaxx" ~/sites-generic-backup-mijaxx
cp -r "$SCRIPT_DIR/get-milyfe" ~/sites-generic-backup-get-milyfe
echo "Backups: ~/sites-generic-backup-mijaxx + ~/sites-generic-backup-get-milyfe"

echo ""
echo "═══ 5. Installing REAL mijaxx files ═══"
cp -r "$ROOT/." "$SCRIPT_DIR/mijaxx/"
# Keep pretty URLs working on Vercel (invisible, doesn't change the look)
if [ ! -f "$SCRIPT_DIR/mijaxx/vercel.json" ]; then
  echo '{"cleanUrls":true,"trailingSlash":false}' > "$SCRIPT_DIR/mijaxx/vercel.json"
fi
echo "mijaxx now: $(find "$SCRIPT_DIR/mijaxx" -name '*.html' | wc -l) pages, $(find "$SCRIPT_DIR/mijaxx/images" -type f 2>/dev/null | wc -l) images"

echo ""
echo "═══ 6. Building get-milyfe from the real page ═══"
if [ -f "$ROOT/get-milyfe.html" ]; then
  rm -rf "$SCRIPT_DIR/get-milyfe"
  mkdir -p "$SCRIPT_DIR/get-milyfe"
  cp "$ROOT/get-milyfe.html" "$SCRIPT_DIR/get-milyfe/index.html"
  for d in css js images; do
    [ -d "$ROOT/$d" ] && cp -r "$ROOT/$d" "$SCRIPT_DIR/get-milyfe/"
  done
  echo '{"cleanUrls":true,"trailingSlash":false}' > "$SCRIPT_DIR/get-milyfe/vercel.json"
  echo "get-milyfe rebuilt from the real get-milyfe.html + shared assets."
else
  echo "(no get-milyfe.html in zip — keeping the rebuilt landing page)"
fi

echo ""
echo "═══ 7. Saving real files to GitHub (backup) ═══"
cd ~/milyfebackup
git add sites/ 2>/dev/null || true
git -c user.name="milyfe-phone" -c user.email="phone@milyfe.fun" \
  commit -qm "Replace generic rebuild with real site files from workspace zip" \
  || echo "(nothing new to commit)"
git push origin arena/01a07f01-milyfebackup \
  || echo "NOTE: push failed (run 'gh auth login' once). Continuing to deploy anyway."

echo ""
echo "═══ 8. Deploying REAL sites to Vercel ═══"
bash "$SCRIPT_DIR/deploy-vercel.sh"

echo ""
echo "═══ DONE — the real branding is live ═══"
