# CLAUDE.md — projectgeheugen (autonoom werken)

> Claude Code laadt dit bestand automatisch bij elke sessie in deze map.
> Het master-draaiboek staat in `_workflow/WORKFLOW.md` — lees dat als leidraad.

## Wat dit project is
Pro4Never (Brabant Digital) maakt statische demo-websites voor lokale ondernemers,
zet ze live op een VPS, en pitcht ze. Doel: klant koopt website + maandelijkse hosting/onderhoud.

## Stack & vaste feiten
- **Hosting:** VPS `93.190.187.213`, webserver **Caddy** (HTTPS automatisch).
- **Demo-URL per klant:** `KLANT.demo.brabantdigital.nl` (wildcard `*.demo` staat al in DNS).
- **Mapstructuur per klant:** zie `_workflow/WORKFLOW.md`. Demo = de map `03-designs/` (alle 10 designs onder 1 subdomein).
- **Contact/merk:** Brabant Digital · aanbod@brabantdigital.nl · WhatsApp wa.me/31850608471.
- **Formulieren:** Web3Forms-sleutel `ef050157-d2a3-43ce-89c2-6088aa1b8bf2` (mailt naar aanbod@brabantdigital.nl). Herbruikbaar in elke demo.

## Deploy (Caddy) — standaard stappen
```bash
rsync -av "KLANT/03-designs/" root@93.190.187.213:/var/www/demos/KLANT/
sudo chmod -R a+rX /var/www/demos/KLANT          # na élke upload
# Caddy-blokje toevoegen (zie KLANT/03-designs/caddy-snippet.txt) en:
sudo systemctl reload caddy
```
Demo weghalen: `rm -rf /var/www/demos/KLANT` + Caddy-blok weg + reload.

## Autonomie-afspraken (door Pro4Never vastgesteld)
- **Mag automatisch, zonder te vragen:** demo's bouwen/bewerken, live zetten, Caddy beheren, demo's verwijderen.
- **Klantbenadering:** autonoom versturen toegestaan. Regels: log élke verzonden mail/bericht, benader nooit dezelfde prospect twee keer, en houd het netjes/persoonlijk. (Verzendkanaal wordt later ingericht.)
- **Geblokkeerd (altijd):** systeem-vernietigende commando's — afgevangen door `.claude/hooks/guard.sh`.
- **Vangnet:** maak/laat een **VPS-snapshot** maken vóór grote of verwijderende acties.

## Terugkoppeling
Schrijf aan het eind van elke werkdag een korte samenvatting naar
`_workflow/logs/DAGELIJKS-JJJJ-MM-DD.md`: wat gedaan, welke demo-links, wat openstaat, eventuele fouten.

## Stijlregels voor de sites
Statische HTML/CSS/JS, responsive, snel, NL met NL/EN-knop, SEO ingebakken, geen AI-/interne
verwijzingen op klantpagina's (zie het schoonmaak-resultaat van hondentrimsalonscott als voorbeeld).
