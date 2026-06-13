#!/usr/bin/env bash
cd /root/klanten || exit 1
git add -A
git -c user.email=vps@brabantdigital.nl -c user.name=BD-VPS commit -q -m "${1:-update}" || exit 0
TOK=$(cat /root/outreach-data/.git-token 2>/dev/null)
[ -n "$TOK" ] && git push -q "https://$TOK@github.com/CrankCo90/brabant-klanten.git" HEAD:main && echo "gepusht"
