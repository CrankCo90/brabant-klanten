#!/usr/bin/env bash
# Draait op de VPS via cron. Haalt de laatste versie op en publiceert elke klant
# met een kiesdemo (03-designs/index.html) naar /var/www/demos/<klant>.
set -euo pipefail
REPO_DIR="/root/klanten"
WWW="/var/www/demos"
CADDY="/etc/caddy/Caddyfile"
SUFFIX="demo.brabantdigital.nl"
LOG="$REPO_DIR/_workflow/logs/autodeploy.log"
mkdir -p "$(dirname "$LOG")"
cd "$REPO_DIR"

before=$(git rev-parse HEAD 2>/dev/null || echo none)
if ! git fetch --quiet origin main 2>>"$LOG"; then echo "$(date '+%F %T') fetch faalde" >>"$LOG"; exit 0; fi
git reset --hard --quiet origin/main
after=$(git rev-parse HEAD)
[ "$before" = "$after" ] && exit 0   # niets nieuws

changed=0
for d in */ ; do
  klant="${d%/}"
  src="$REPO_DIR/$klant/03-designs"
  [ -f "$src/index.html" ] || continue          # alleen klanten met een kiesdemo
  dest="$WWW/$klant"
  mkdir -p "$dest"
  rsync -a --delete \
    --exclude='*.sh' --exclude='caddy-snippet.txt' --exclude='*.bak' \
    "$src/" "$dest/"
  chmod -R a+rX "$dest"
  if ! grep -q "$klant\.$SUFFIX" "$CADDY"; then
    printf '\n%s.%s {\n    root * %s/%s\n    file_server\n    encode gzip\n}\n' \
      "$klant" "$SUFFIX" "$WWW" "$klant" >> "$CADDY"
    echo "$(date '+%F %T') Caddy-blok toegevoegd: $klant" >>"$LOG"
  fi
  changed=1
  echo "$(date '+%F %T') gepubliceerd: $klant" >>"$LOG"
done
if [ "$changed" = 1 ]; then systemctl reload caddy; echo "$(date '+%F %T') caddy herladen ($after)" >>"$LOG"; fi
exit 0
