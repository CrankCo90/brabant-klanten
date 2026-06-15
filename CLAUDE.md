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
## Telefoon & WhatsApp (VASTE FEITEN — 15-06-2026)
- **Nieuw nummer:** `085-0608491`. WhatsApp-link: `https://wa.me/31850608491` (0 weg, 31 ervoor).
- Staat in: outreach-mails (template-nl/kort/herinnering), de demo-**coverpagina** (index.html) en BD-site/onboarding.
- **Meelopende 'App ons'-knop** op elke demo-coverpagina: vaste WhatsApp-pil rechtsonder, `id="bd-wa-float"`,
  groene (#25D366) pil + officieel WhatsApp-logo → opent `wa.me/31850608491`. Zit ook in de brontemplate
  (`hondentrimsalonscott/03-designs/index.html`), dus nieuwe demo's krijgen 'm automatisch.
- BD-contact (WhatsApp/tel) hoort ALLEEN op de coverpagina (de pitch), NIET in de 11 ontwerpen zelf.
- **Vaste WhatsApp-tekst (dashboard `waText`):** "Hoi {voornaam}! 👋 Ik ben Leroy van Brabant Digital……voor {bedrijf} … 30 seconden: 👉 {demo_url} … En zo niet, dan hoor ik dat ook graag eerlijk 😊 — Groetjes van Leroy". Bij `mailDone` aangepaste opening ("Ik had je net een mailtje gestuurd…"). Voornaam via `waName`; EN-variant aanwezig.

## Prospect-contactregel (VASTE AFSPRAAK — aangescherpt 15-06-2026)
Een prospect mag in de lijst/gebouwd worden als hij MINSTENS ÉÉN van deze heeft:
**e-mail OF social (IG/FB/TikTok) OF een 06-MOBIEL nummer.**
- Een **vaste lijn** (040/030/073/013/0162/0492 enz.) telt NIET als bereikbaar contact.
- Geen van de drie → verwijderen + vervangen door een prospect die wél voldoet.

## Outreach-mail (opbouw & regels — VASTE AFSPRAAK)
- Template: `_workflow/outreach/template-nl.txt`. Placeholders uit `prospects.json`: `compliment`,
  `gratis_tip`, `verbeteringen` (+ aanhef/bedrijf/demo_url). NOOIT website-status of fouten in die velden.
- `compliment` = nette opener (niche+plaats), `gratis_tip` = echte tip, `verbeteringen` = VOORDELEN.
- **List-Unsubscribe (mailto) header** in send-one.py + send-outreach.py. Status `concept` wordt niet gemaild.
- Afleverbaarheid: mail-tester 10/10 ≠ inbox; grootste hefboom = mailrelay (Postmark/Brevo) i.p.v. VPS-IP.

## Design-11 voor ALLE niches (generator — 15-06-2026)
- `generate-demo.py` bouwt design-11 voor pedicure, nagels én hond (`render_d11_pedicure/nagel/hond` +
  templates `_workflow/templates/design11-{pedicure,nagel,hond}.html`). Cal.eu-blok 1-op-1 uit de generator-`CAL`.

## Dashboard — Acties & autopilot (VASTE AFSPRAAK — 15-06-2026)
- Outreach-wachtrij toont ALLEEN klanten die per e-mail bereikbaar zijn én nog niet gemaild/benaderd
  (`c.em && c.es!=='verzonden' && niet benaderd/gekocht/afgewezen`). Gemailde vallen automatisch weg (sent-log.csv).
- "Publiceer demo's"-knop is verwijderd (autodeploy publiceert elke minuut). Niet terugzetten.

## Autopilot & outreach-engine (VASTE WERKING — 15-06-2026)
- Autopilot mailt ALLE e-mailbare, niet-benaderde klanten: `OUTREACH_ALL=1` + `OUTREACH_BATCH=1` +
  `OUTREACH_CAP`=daglimiet. Cron elke 2 min, alleen binnen kantooruren/werkdagen → 1 mail/2 min tot daglimiet.
- "nee"-reacties → `scan-replies.py` zet klant op afgewezen + demo offline + blocklist + commit/push.
- `daily-report.py` mailt elke werkdag 17:35 naar leroyb@home.nl (# gemaild + reacties).
- Statuswijzigingen worden gecommit+gepusht (token in `/root/outreach-data/.git-token`).
- Na control-server.py-wijziging: `sudo systemctl restart bd-control`.

## Outreach — VPS-commando's (cron-installers + test)
```bash
sudo systemctl restart bd-control
( crontab -l 2>/dev/null | grep -v autopilot-run.sh; echo '*/2 * * * * bash /root/klanten/_workflow/autopilot-run.sh' ) | crontab -
( crontab -l 2>/dev/null | grep -v scan-replies.py; echo '*/15 * * * * cd /root/klanten && OUTREACH_DATA=/root/outreach-data /usr/bin/python3 _workflow/outreach/scan-replies.py >> /root/outreach-data/replies.log 2>&1' ) | crontab -
( crontab -l 2>/dev/null | grep -v daily-report.py; echo '35 17 * * 1-5 cd /root/klanten && OUTREACH_DATA=/root/outreach-data /usr/bin/python3 _workflow/outreach/daily-report.py >> /root/outreach-data/report.log 2>&1' ) | crontab -
```
- Dagrapport handmatig testen: `cd /root/klanten && git pull -q && OUTREACH_DATA=/root/outreach-data python3 _workflow/outreach/daily-report.py`.
- Testmodus NIET gewenst. Reply-scan + rapport vereisen IMAP_HOST/IMAP_PORT in `.smtp-env`.

## "Afspraak maken" → ALTIJD de cal.eu demo-planner (VASTE AFSPRAAK — mag NOOIT fout)
- Elke "Afspraak maken"-knop in ELKE demo (10 designs ÉN design-11) MOET de cal.eu demo-planner openen:
  `data-cal-link="brabantdigital/demo-planner"`, namespace `demo-planner`, origin `https://cal.eu`.
  NOOIT uitkomen op `#contact`/`#book`. Cal-blok 1-op-1 uit een werkende demo of de generator-`CAL`.
- Check na elke build: knop heeft ná laden GÉÉN `href` meer maar wél `data-cal-link`, 0 JS-fouten.

## Nieuwe niche = nieuwe content (VASTE AFSPRAAK)
Eigen teksten/diensten/iconen/beelden per vak + eigen content-mapping in `generate-demo.py` + eigen design-11.
Nooit content van een andere niche hergebruiken.

## Prospect-onderzoek (VASTE WERKWIJZE)
Volg ALTIJD `05-marktonderzoek/prospect-onderzoek-werkwijze.md` (7 stappen, keten doorvolgen, max 10 bronnen).

## Beeldgebruik in demo's
Werkende site/openbare social met 2+ foto's → eigen foto's; anders AI. Eén losse afbeelding = meestal logo, niet gebruiken.

## Stijlregels voor de sites
Statische HTML/CSS/JS, responsive, snel, NL met NL/EN-knop, SEO ingebakken, geen AI-/interne verwijzingen op klantpagina's.

## Afgewezen klanten NOOIT deployen
Map-slug in `_workflow/niet-deployen.txt`; `vps-autodeploy.sh` slaat die over én haalt een live exemplaar offline.
