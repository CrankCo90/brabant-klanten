# Sessie-overdracht — 16 juni 2026

Lees bij opstart éérst `CLAUDE.md` + de nieuwste `SESSIE-OVERDRACHT-*.md`. Vaste afspraken staan in CLAUDE.md.

## 1. Dashboard-fixes (live)
- **Mobiel-menu**: sidebar sloot niet op telefoon → backdrop-overlay (klik=sluiten) + ✕-knop + sluit bij navigatie.
- **Autopilot aan/uit + dagcap**: was per apparaat verschillend (PC 100/aan, telefoon 20/uit). Nu **server-persistent**: dashboard laadt stand uit `/api/status` en slaat élke wijziging op (3 schakelaars gesynct, "Opslaan" wist `on` niet meer). Overal identiek.
- **Replies in "Activiteit"**: reply van een prospect (bv. "geen interesse") verschijnt nu bij de klant in de Activiteit-tijdlijn met onderwerp + datum. (`scan-replies.py` zet "nee" al om naar afgewezen + demo offline; dat werkte — Beauty Point Helmond stond correct op afgewezen + in niet-deployen.)

## 2. Demo-publicatie was kapot → opgelost
- **Oorzaak 1**: `vps-autodeploy.sh` brak af op `set -e` → Caddy nooit herladen. Nu robuust (geen abort bij 1 klant-fout, `flock -w 50`).
- **Oorzaak 2 (de echte)**: **Let's Encrypt rate-limit** (50 certs/week/domein) — elke demo kreeg een los cert. Opgelost met **één wildcard-cert** `*.demo.brabantdigital.nl` (LE DNS-challenge via Vimexx-TXT). Caddy serveert demo's nu via één wildcard-blok (`root * /var/www/demos/{labels.3}`), cert gekopieerd naar `/etc/caddy/certs` (LE-map is root-only → caddy kon anders niet starten) via `_workflow/caddy-wildcard.sh`. **Cert verloopt 14-09-2026 — handmatig verlengen** (herinnering in CLAUDE.md + geplande app-taak 5 sep).
- `niet-deployen.txt` was door `scan-replies.py` (`.split()`) verhaspeld → hersteld; script leest nu regel-voor-regel.
- Autodeploy synct nu ook de **hoofdsite** `brabantdigital/site` → `/var/www/brabantdigital` (hoofdsite stond op oud telefoonnummer; nu in sync).
- **Mail-authenticatie**: outreach gaat via `mail.zxcs.nl` (provider-SMTP) → SPF+DKIM kloppen al; VPS NIET aan SPF toevoegen.

## 3. Prospects — Limburg (deze sessie, live)
- **39 nieuw**: 24 hond, 14 nagel(? 16), 3 pedicure — Roermond/Maastricht/Heerlen/Kerkrade/Sittard/Geleen/Weert/Venlo/Venray e.o. Treatwell/Salonized/IG-only/06. Pedicure laag-renderend (veel eigen sites) → via `pedicure.nl` (regio/postcode) verder minen.

## 4. Nieuwe niches — kappers afgerond (eerste van 9)
- **Kapper-engine** in `generate-demo.py` (eigen content + Higgsfield-beelden in `niche-images.json`), **15 NB-kappers** (Tilburg/Breda/Helmond/Oss/Veghel) gebouwd, label "Kappers".
- **Twee eigen premium-designs**: design-11 (donker, video-hero, à la haaratelier Mari) + design-12 (licht/warm, à la kapsalon-asya). Beide met cal.eu + contactformulier + WhatsApp + NL/EN + Maps. Staan eerste op de cover. Zie CLAUDE.md "Kappers-niche + premium-designs".
- **new-client.py gefixt**: herkent kapper/barber/haar → `kapper`/"Kappers" (viel eerder terug op hondendemo + losse categorie). Outreach-velden nu net (geen lege compliment / notitie-in-tip meer). Bestaande upload `kapsalonasya` hersteld (kapper-demo + correcte mailtekst).

## Openstaand / volgende stappen
- Resterende 8 niches: barbershops (hergebruikt kapper-engine), lash/brow, schoonheidssalons, massage, visagie, autopoets (hero-beelden bestaan al in Higgsfield-historie), hoveniers, schilders — elk: eigen content/beelden + 15 prospects + demo's.
- Richting 100/niche voor hond/nagel/pedicure (Limburg verder, dan Zeeland); pedicure via pedicure.nl.
- Mailrelay/deliverability blijft aandachtspunt (warm-up, inhoud).

## Alles op GitHub (CrankCo90/brabant-klanten, main); VPS pullt elke minuut.
