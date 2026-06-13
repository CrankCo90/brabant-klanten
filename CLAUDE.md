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
- **Klantbenadering (e-mail, autonoom):** zie `_workflow/OUTREACH-SETUP.md`. Funnel: prospect vinden → demo bouwen → pushen → VPS mailt via `outreach/send-outreach.py`. Regels: nooit dezelfde prospect twee keer (sent-log.csv), daglimiet (OUTREACH_CAP, standaard 20), afmeldregel + duidelijke afzender in elke mail, alleen mailen als er een werkende demo-link klaarstaat, en B2B/lokale ondernemers. 'Nee'-reacties → blokkeerlijst. WhatsApp NIET automatisch (alleen wa.me-knop/handmatig).
- **Geblokkeerd (altijd):** systeem-vernietigende commando's — afgevangen door `.claude/hooks/guard.sh`.
- **Vangnet:** maak/laat een **VPS-snapshot** maken vóór grote of verwijderende acties.

## Aanbod, hosting & strategie (zie `_workflow/STRATEGIE.md`)
- **Prijs:** €199 EENMALIG, geen maandelijkse/verplichte kosten, klant zit nergens aan vast. 1 maand gratis kleine aanpassingen na oplevering. Normaal €499 (lanceringskorting voor review).
- **Hosting:** optioneel, losse service (~€19/mnd), 12 mnd vooruit = 25% korting, niet verplicht.
- **Infra:** alles op één VPS, git-gedreven (demo's + productie /var/www/sites/<klant>, eigen domein via DNS). Geen VPS-per-klant.
- **Dashboard:** admin.brabantdigital.nl (basicauth), leest clients.json; per niche + werkdag, met stats.
- **Prospect-proces:** per niche+regio 20-30 bedrijven scannen, ranken (web/foto/social/vindbaarheid/fulltime), alleen de zwakste benaderen; al-goede sites NIET.
- **Onboarding 'ja':** welkomstmail + onboardingformulier; standaard hosten op onze VPS (alleen DNS). Logins veilig buiten git.

## Terugkoppeling
Schrijf aan het eind van elke werkdag een korte samenvatting naar
`_workflow/logs/DAGELIJKS-JJJJ-MM-DD.md`: wat gedaan, welke demo-links, wat openstaat, eventuele fouten.

## Stijlregels voor de sites
Statische HTML/CSS/JS, responsive, snel, NL met NL/EN-knop, SEO ingebakken, geen AI-/interne
verwijzingen op klantpagina's (zie het schoonmaak-resultaat van hondentrimsalonscott als voorbeeld).
