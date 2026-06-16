#!/usr/bin/env bash
# Draait op de VPS via cron. Haalt de laatste versie op en publiceert elke klant
# met een kiesdemo (03-designs/index.html) naar /var/www/demos/<klant>.
# Routing/HTTPS gaat via ÉÉN wildcard-blok in de Caddyfile (*.demo.brabantdigital.nl,
# wildcard-cert) — dit script hoeft dus GEEN Caddy-blokken meer toe te voegen of
# losse certs aan te vragen. Het synct alleen bestanden.
set -uo pipefail
exec 9>/var/lock/bd-autodeploy.lock
flock -w 50 9 || { echo "$(date '+%F %T') lock bezet (>50s) — overgeslagen" >> /root/klanten/_workflow/logs/autodeploy.log; exit 0; }
REPO_DIR="/root/klanten"; WWW="/var/www/demos"
SKIP_FILE="$REPO_DIR/_workflow/niet-deployen.txt"
LOG="$REPO_DIR/_workflow/logs/autodeploy.log"
mkdir -p "$(dirname "$LOG")" "$WWW"
cd "$REPO_DIR" || { echo "$(date '+%F %T') repo-dir ontbreekt" >>"$LOG"; exit 1; }

if ! git fetch --quiet origin main 2>>"$LOG"; then echo "$(date '+%F %T') fetch faalde" >>"$LOG"; exit 0; fi
git reset --hard --quiet origin/main
after=$(git rev-parse HEAD)

for d in */ ; do
  klant="${d%/}"
  src="$REPO_DIR/$klant/03-designs"
  [ -f "$src/index.html" ] || continue
  if [ -f "$SKIP_FILE" ] && grep -qxF "$klant" "$SKIP_FILE"; then
    [ -d "$WWW/$klant" ] && { rm -rf "$WWW/$klant"; echo "$(date '+%F %T') afgewezen -> offline: $klant" >>"$LOG"; }
    continue
  fi
  mkdir -p "$WWW/$klant"
  if rsync -a --delete --exclude='*.sh' --exclude='caddy-snippet.txt' --exclude='*.bak' "$src/" "$WWW/$klant/" 2>>"$LOG"; then
    chmod -R a+rX "$WWW/$klant" 2>>"$LOG" || true
  else
    echo "$(date '+%F %T') rsync faalde, overgeslagen: $klant" >>"$LOG"
  fi
done
# admin-dashboard + onboarding publiceren (eigen vhosts, bestaan al in Caddyfile)
[ -f "$REPO_DIR/dashboard/index.html" ] && { mkdir -p /var/www/admin; rsync -a --delete "$REPO_DIR/dashboard/" /var/www/admin/ 2>>"$LOG"; chmod -R a+rX /var/www/admin 2>>"$LOG" || true; }
[ -f "$REPO_DIR/brabantdigital/site/index.html" ] && { mkdir -p /var/www/brabantdigital; rsync -a --delete "$REPO_DIR/brabantdigital/site/" /var/www/brabantdigital/ 2>>"$LOG"; chmod -R a+rX /var/www/brabantdigital 2>>"$LOG" || true; }
[ -f "$REPO_DIR/onboarding/index.html" ] && { mkdir -p /var/www/onboarding; rsync -a --delete --exclude="*.txt" "$REPO_DIR/onboarding/" /var/www/onboarding/ 2>>"$LOG"; chmod -R a+rX /var/www/onboarding 2>>"$LOG" || true; }
echo "$(date '+%F %T') sync klaar ($after)" >>"$LOG"
exit 0
