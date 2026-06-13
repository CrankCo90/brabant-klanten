# publish.ps1 — publiceer (of update) een klant-demo naar de VPS.
# Gebruik in PowerShell, vanuit deze map:
#     .\publish.ps1 hondentrimsalonscott
# Zet de demo live op https://<klant>.demo.brabantdigital.nl en regelt Caddy de eerste keer zelf.
param([Parameter(Mandatory=$true)][string]$Klant)
$ErrorActionPreference = "Stop"
$base = "C:\Users\Gebruiker\Desktop\Klanten werven voor nieuwe site"
$src  = Join-Path $base "$Klant\03-designs"
$vps  = "root@93.190.187.213"

if (-not (Test-Path $src)) { Write-Host "Map niet gevonden: $src" -ForegroundColor Red; exit 1 }

Write-Host "1/3  Uploaden van $Klant ..." -ForegroundColor Cyan
ssh $vps "rm -rf /tmp/$Klant-deploy"
scp -r "$src" "${vps}:/tmp/$Klant-deploy"

Write-Host "2/3  Plaatsen + rechten + Caddy ..." -ForegroundColor Cyan
$remote = @"
set -e
mkdir -p /var/www/demos
rm -rf /var/www/demos/$Klant
mv /tmp/$Klant-deploy /var/www/demos/$Klant
chmod -R a+rX /var/www/demos/$Klant
if ! grep -q '$Klant.demo.brabantdigital.nl' /etc/caddy/Caddyfile; then
  printf '\n%s.demo.brabantdigital.nl {\n    root * /var/www/demos/%s\n    file_server\n    encode gzip\n}\n' '$Klant' '$Klant' >> /etc/caddy/Caddyfile
  echo 'Caddy-blok toegevoegd.'
fi
systemctl reload caddy
"@
ssh $vps $remote

Write-Host "3/3  Klaar!  ->  https://$Klant.demo.brabantdigital.nl" -ForegroundColor Green
