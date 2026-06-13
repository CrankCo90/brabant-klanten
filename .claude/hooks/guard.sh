#!/usr/bin/env bash
# PreToolUse-vangnet: blokkeert systeem-vernietigende commando's. exit 2 = blokkeren.
# Toegestaan blijft: een specifieke demo verwijderen (bijv. /var/www/demos/scott).
cmd=$(python3 -c "import sys,json;d=json.load(sys.stdin);ti=d.get('tool_input') or {};print(ti.get('command') or d.get('command') or '')" 2>/dev/null)
block(){ echo "⛔ Geblokkeerd door guard.sh ($1): $cmd" >&2; exit 2; }

# A) rm op beschermde systeemmappen (ook subpaden hiervan)
echo "$cmd" | grep -Eq 'rm +.*(/etc|/usr|/bin|/sbin|/boot|/lib|/lib64|/var/log|/var/lib)(/|$| )' && block "rm op systeemmap"
# B) rm op een gevaarlijke HOOFDmap als laatste argument (root, home, demos-root, /var, /var/www)
echo "$cmd" | grep -Eq 'rm +(-[a-zA-Z]+ +)+(/|~|\*|/\*|/var|/var/www|/var/www/demos|/root|/home)(/? *\*?)? *$' && block "rm op hoofd-/webroot"
# C) schijf/systeem-ingrijpend
echo "$cmd" | grep -Eq '\b(mkfs|shutdown|reboot|halt)\b|\bdd +if=|\binit +0\b|:\(\)\s*\{' && block "systeem-ingrijpend"
# D) hele Caddyfile leeggooien (gebruik Edit i.p.v. >)
echo "$cmd" | grep -Eq '> */etc/caddy/Caddyfile *$' && block "Caddyfile overschrijven (gebruik Edit)"
exit 0
