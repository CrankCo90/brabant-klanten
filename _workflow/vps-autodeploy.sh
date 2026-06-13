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
# admin-dashboard publiceren
if [ -f "$REPO_DIR/dashboard/index.html" ]; then
  mkdir -p /var/www/admin
  rsync -a --delete "$REPO_DIR/dashboard/" /var/www/admin/
  chmod -R a+rX /var/www/admin
  changed=1
  echo "$(date '+%F %T') dashboard gesynchroniseerd" >>"$LOG"
fi
# onboarding-formulier publiceren
if [ -f "$REPO_DIR/onboarding/index.html" ]; then
  mkdir -p /var/www/onboarding
  rsync -a --delete --exclude="*.txt" "$REPO_DIR/onboarding/" /var/www/onboarding/
  chmod -R a+rX /var/www/onboarding
  changed=1
  echo "$(date '+%F %T') onboarding gesynchroniseerd" >>"$LOG"
fi
if [ "$changed" = 1 ]; then systemctl reload caddy; echo "$(date '+%F %T') caddy herladen ($after)" >>"$LOG"; fi
exit 0
