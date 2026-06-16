#!/usr/bin/env bash
# Zet Caddy om naar ÉÉN wildcard-blok voor *.demo.brabantdigital.nl.
# Kopieert het LE-cert naar een door 'caddy' leesbare map (LE-map is root-only,
# anders start caddy niet) en laat de config daarnaar wijzen. Veilig: back-up +
# validatie + automatische terugval naar back-up als de start faalt.
set -uo pipefail
CADDY=/etc/caddy/Caddyfile
LEDIR=/etc/letsencrypt/live/demo.brabantdigital.nl
DST=/etc/caddy/certs
WWW=/var/www/demos
SUFFIX=demo.brabantdigital.nl
[ -f "$LEDIR/fullchain.pem" ] && [ -f "$LEDIR/privkey.pem" ] || { echo "FOUT: cert niet gevonden in $LEDIR"; exit 1; }
mkdir -p "$DST"
cp -L "$LEDIR/fullchain.pem" "$DST/demo.crt"
cp -L "$LEDIR/privkey.pem"  "$DST/demo.key"
chown caddy:caddy "$DST/demo.crt" "$DST/demo.key" 2>/dev/null || true
chmod 644 "$DST/demo.crt"; chmod 600 "$DST/demo.key"
BK="$CADDY.bak.$(date +%s)"; cp -a "$CADDY" "$BK" && echo "back-up: $BK"
python3 - "$CADDY" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
s=re.sub(r'(?ms)^[^\n{]*\.demo\.brabantdigital\.nl\s*\{.*?^\}[ \t]*$\n?','',s)
open(p,'w',encoding='utf-8').write(s)
PY
cat >> "$CADDY" <<EOF

*.$SUFFIX {
    tls $DST/demo.crt $DST/demo.key
    root * $WWW/{labels.3}
    file_server
    encode gzip
}
EOF
if caddy validate --config "$CADDY" --adapter caddyfile && systemctl restart caddy && sleep 1 && systemctl is-active --quiet caddy; then
  echo "OK — Caddy draait met wildcard-cert; alle demo's live."
else
  echo "FOUT bij start — back-up teruggezet."; cp -a "$BK" "$CADDY"; systemctl restart caddy; systemctl is-active caddy
fi
