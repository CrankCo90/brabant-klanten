#!/usr/bin/env bash
# Eenmalig: zet Caddy om naar ÉÉN wildcard-blok voor *.demo.brabantdigital.nl
# (gebruikt het wildcard-cert) i.p.v. honderden losse blokken met elk een eigen cert.
# Veilig: maakt back-up, valideert, en herstart alleen bij geldige config.
set -uo pipefail
CADDY=/etc/caddy/Caddyfile
CERTDIR=/etc/letsencrypt/live/demo.brabantdigital.nl
CERT="$CERTDIR/fullchain.pem"
KEY="$CERTDIR/privkey.pem"
WWW=/var/www/demos
SUFFIX=demo.brabantdigital.nl
if [ ! -f "$CERT" ] || [ ! -f "$KEY" ]; then
  echo "FOUT: wildcard-cert niet gevonden in $CERTDIR — vraag eerst het cert aan."; exit 1
fi
cp -a "$CADDY" "$CADDY.bak.$(date +%s)" && echo "back-up gemaakt"
# Verwijder ALLE bestaande blokken die op .demo.brabantdigital.nl eindigen (losse slugs én een eerdere wildcard).
python3 - "$CADDY" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
pat=re.compile(r'(?ms)^[^\n{]*\.demo\.brabantdigital\.nl\s*\{.*?^\}[ \t]*$\n?')
s2=pat.sub('', s)
open(p,'w',encoding='utf-8').write(s2)
print("losse demo-blokken verwijderd")
PY
# Voeg één wildcard-blok toe (routeert op subdomein-label naar de juiste map).
cat >> "$CADDY" <<EOF

*.$SUFFIX {
    tls $CERT $KEY
    root * $WWW/{labels.3}
    file_server
    encode gzip
}
EOF
echo "wildcard-blok toegevoegd"
if caddy validate --config "$CADDY" --adapter caddyfile; then
  systemctl restart caddy && echo "OK — Caddy draait met wildcard-cert; alle demo's live."
else
  echo "FOUT: Caddyfile ongeldig. Back-up staat naast het bestand (.bak.*). Niets herstart."
  exit 1
fi
