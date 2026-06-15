# CLAUDE.md — projectgeheugen (autonoom werken)

> Claude Code laadt dit bestand automatisch bij elke sessie in deze map.
> Het master-draaiboek staat in `_workflow/WORKFLOW.md` — lees dat als leidraad.
>
> **BIJ OPSTART (eerste actie van elke nieuwe sessie):** lees éérst dit CLAUDE.md ÉN de meest recente
> `_workflow/SESSIE-OVERDRACHT-*.md` (sessie-overdrachten) volledig door, vóór je aan een opdracht begint.
> Zo heb je alle afspraken, de huidige staat en openstaande punten paraat.

## Wat dit project is
Pro4Never (Brabant Digital) maakt statische demo-websites voor lokale ondernemers,
zet ze live op een VPS, en pitcht ze. Doel: klant koopt website + maandelijkse hosting/onderhoud.

## Werkwijze & communicatie met Pro4Never (VASTE AFSPRAAK — altijd volgen)
- **Commando's ALTIJD één-voor-één aanleveren**, elk in een EIGEN codeblok. Nooit meerdere
  commando's in één blok of als één groot overzicht — Pro4Never plakt een blok in z'n geheel
  en zou anders alles als één commando uitvoeren.
- **Leg bij ELK commando uit wat het doet** (één korte zin vóór het codeblok). Geen kale
  commando's zonder uitleg.
- Eén logische actie = één codeblok (een `for`-lus die in één keer hoort te draaien mag samen).
  Combineer geen losse stappen met `&&` als ze ook apart kunnen.
- Waar de uitkomst van een stap de volgende beïnvloedt: geef de stap, laat Pro4Never 'm draaien
  en de output terugkoppelen, geef dan pas de volgende.
- **Benoem bij ELK commando expliciet in WELKE terminal het moet draaien:** ofwel
  "**PC-terminal**" (PowerShell op de pc van Pro4Never) ofwel "**VPS-terminal**" (SSH/bash op de
  VPS, `root@...:~/klanten`). Nooit een commando geven zonder de terminal te benoemen.
- Pro4Never draait commando's vaak in de **VPS bash-shell**, niet in PowerShell op de pc.
  Geef bash-commando's voor de VPS, tenzij expliciet anders gevraagd.
- Feedback van Pro4Never over werkwijze → hier vastleggen zodat het tussen sessies bewaard blijft.

## Werkwijze deploy (VASTE AFSPRAAK — door Pro4Never bevestigd)
- **Claude doet ALLES en pusht naar GitHub.** Bij nieuwe klanten: demo's bouwen, en
  `dashboard/clients.json`, `_workflow/outreach/prospects.json` én `_workflow/salons-batch1.json`
  bijwerken, daarna committen + pushen naar `github.com/CrankCo90/brabant-klanten` (branch main).
- **De VPS trekt elke minuut vanuit GitHub** (cron `* * * * *` → `vps-autodeploy.sh`, met `flock`-lock
  tegen overlap, doet `git reset --hard origin/main`) en publiceert. Dus na een push staat alles binnen
  ~1 min live — Pro4Never hoeft niets te draaien.
- **Hoe Claude uploadt (operationeel):** Claude pusht NIET vanuit de Cowork-map (git werkt daar niet).
  In plaats daarvan: in de sandbox een verse clone (`git clone https://x-access-token:<token>@github.com/
  CrankCo90/brabant-klanten.git`), de token uit `_workflow/.deploy-token`, daar de wijzigingen aanbrengen
  (`git pull` vooraf), committen en `git push HEAD:main`. De VPS-autodeploy pakt het op.
- **Valkuil bouwomgeving (belangrijk):** bestanden die via de Edit/Write-tool in de Cowork-map staan,
  worden bij lezen in de bash-sandbox afgekapt rond ~307 regels. Grote HTML (templates >~300 regels) dus
  NIET via de mount kopiëren — bouw/bewerk ze in de sandbox-clone zelf (anders krijg je afgekapte demo's).
- **Altijd éérst `git pull` (clone verversen) vóór je clients.json/prospects.json bewerkt**, zodat je
  geen recente entries overschrijft. Houd de JSON altijd geldig (valideren vóór push).
- Het **dashboard** is vooral een viewer/bewerker; gebruik de "Nieuwe klant"-knop niet tegelijk met
  een Cowork-push voor dezelfde klant (anders twee schrijvers tegelijk).
- Demo's bouw je via de pijplijn: zet de klant in `salons-batch1.json` (met `niche`) en draai
  `_workflow/generate-demo.py` (pedicure/nagels/hond hebben elk eigen content + design-11).

## Stack & vaste feiten
- **Hosting:** VPS `93.190.187.213`, webserver **Caddy** (HTTPS automatisch).
- **Demo-URL per klant:** `KLANT.demo.brabantdigital.nl` (wildcard `*.demo` staat al in DNS).
- **Mapstructuur per klant:** zie `_workflow/WORKFLOW.md`. Demo = de map `03-designs/` (alle 10 designs onder 1 subdomein).
- **Contact/merk:** Brabant Digital · aanbod@brabantdigital.nl · telefoon **085-0608491** · WhatsApp **wa.me/31850608491** (én appbaar). Oud nummer 0608471 is overal vervangen (mails, demo-coverpagina'