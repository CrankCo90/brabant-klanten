#!/usr/bin/env bash
# Draait op de VPS via cron. Haalt de laatste versie op en publiceert elke klant
# met een kiesdemo (03-designs/index.html) naar /var/www/demos/<klant>.
# ROBUUST: een fout bij één klant mag de hele run (en de caddy-reload) niet blokkeren.
set -uo pipefail
# voorkom overlappende runs, maar laat een vastgelopen lock NIET de deploy eeuwig blokkeren:
# wacht max 50s op de lock i.p.v. meteen afbreken.
exec 9>/var/lock/bd-autodeploy.lock
flock -w 50 9 || { echo "$(date '+%F %T') lock bezet (>50s) — overgeslagen" >> /root/klanten/_workflow/logs/autodeploy.log; exit 0; }
REPO_DIR="/root/klanten"
WWW="/var/www/demos"
CADDY="/etc/caddy/Caddyfile"
SUFFIX="demo.brabantdigital.nl"
SKIP_FILE="$REPO_DIR/_workflow/niet-deployen.txt"   # 1 klant-slug per regel = nooit publiceren
LOG="$REPO_DIR/_workflow/logs/autodeploy.log"
mkdir -p "$(dirname "$LOG")"
cd "$REPO_DIR" || { echo "$(date '+%F %T') repo-dir ontbreekt" >>"$LOG"; exit 1; }

before=$(git rev-parse HEAD 2>/dev/null || echo none)
if ! git fetch --quiet origin main 2>>"$LOG"; then echo "$(date '+%F %T') fetch faalde" >>"$LOG"; exit 0; fi
git reset --hard --quiet origin/main
after=$(git rev-parse HEAD)

changed=0
for d in */ ; do
  klant="${d%/}"
  src="$REPO_DIR/$klant/03-designs"
  [ -f "$src/index.html" ] || continue          # alleen klanten met een kiesdemo
  # Afgewezen klanten: niet publiceren, en al-live exemplaar offline halen
  if [ -f "$SKIP_FILE" ] && grep -qxF "$klant" "$SKIP_FILE"; then
    if [ -d "$WWW/$klant" ]; then
      rm -rf "$WWW/$klant" && changed=1
      echo "$(date '+%F %T') afgewezen -> offline gehaald: $klant" >>"$LOG"
    fi
    continue
  fi
  dest="$WWW/$klant"
  mkdir -p "$dest"
  # fout bij één klant mag de rest niet stoppen
  if ! rsync -a --delete \
      --exclude='*.sh' --exclude='caddy-snippet.txt' --exclude='*.bak' \
      "$src/" "$dest/" 2>>"$LOG"; then
    echo "$(date '+%F %T') rsync faalde, overgeslagen: $klant" >>"$LOG"
    continue
  fi
  chmod -R a+rX "$dest" 2>>"$LOG" || true
  # Caddy-blok toevoegen als het nog niet bestaat (anker op regelbegin = geen substring-botsing)
  if ! grep -qE "^${klant}\.${SUFFIX} \{" "$CADDY"; then
    printf '\n%s.%s {\n    root * %s/%s\n    file_server\n    encode gzip\n}\n' \
      "$klant" "$SUFFIX" "$WWW" "$klant" >> "$CADDY"
    echo "$(date '+%F %T') Caddy-blok toegevoegd: $klant" >>"$LOG"
  fi
  changed=1
done
# admin-dashboard publiceren
if [ -f "$REPO_DIR/dashboard/index.html" ]; then
  mkdir -p /var/www/admin
  rsync -a --delete "$REPO_DIR/dashboard/" /var/www/admin/ 2>>"$LOG" && chmod -R a+rX /var/www/admin 2>>"$LOG" || true
  changed=1
fi
# onboarding-formulier publiceren
if [ -f "$REPO_DIR/onboarding/index.html" ]; then
  mkdir -p /var/www/onboarding
  rsync -a --delete --exclude="*.txt" "$REPO_DIR/onboarding/" /var/www/onboarding/ 2>>"$LOG" && chmod -R a+rX /var/www/onboarding 2>>"$LOG" || true
  changed=1
fi
# Caddy herladen — altijd proberen als er iets gewijzigd is; valideer eerst zodat
# één kapot blok de live-config niet platlegt.
if [ "$changed" = 1 ]; then
  if caddy validate --config "$CADDY" --adapter caddyfile >>"$LOG" 2>&1; then
    if systemctl reload caddy 2>>"$LOG"; then
      echo "$(date '+%F %T') caddy herladen ($after)" >>"$LOG"
    else
      echo "$(date '+%F %T') caddy reload FAALDE (zie systemctl status caddy)" >>"$LOG"
    fi
  else
    echo "$(date '+%F %T') Caddyfile ONGELDIG — reload overgeslagen, fix de config" >>"$LOG"
  fi
fi
exit 0
