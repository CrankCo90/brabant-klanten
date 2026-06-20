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
## ⚠️ TLS-wildcardcert demo's (VASTE FEIT + HERINNERING — verloopt 14-09-2026)
- Alle demo-subdomeinen (`*.demo.brabantdigital.nl`) draaien op **ÉÉN wildcard-certificaat** (Let's Encrypt, DNS-challenge), niet meer per subdomein. Reden: losse per-subdomein-certs liepen tegen de LE-limiet (50/week per domein) → nieuwe demo's bleven offline.
- **Cert verloopt 14-09-2026 en moet HANDMATIG verlengd worden** (geen auto-renew bij `--manual`). Doe dit vóór die datum, anders vallen ALLE demo's offline. Stappen op de VPS-terminal:
  1. `sudo certbot certonly --manual --preferred-challenges dns --agree-tos -m aanbod@brabantdigital.nl --no-eff-email -d '*.demo.brabantdigital.nl'` → de NIEUWE TXT-waarde in Vimexx zetten op record `_acme-challenge.demo`, ~1-2 min wachten, dan Enter.
  2. `cd /root/klanten && git pull -q && sudo bash _workflow/caddy-wildcard.sh` (kopieert cert naar `/etc/caddy/certs`, herstart Caddy, met automatische terugval bij fout).
- Caddy serveert demo's via één wildcard-blok (`*.demo.brabantdigital.nl` → `root * /var/www/demos/{labels.3}`). **`vps-autodeploy.sh` voegt GEEN losse Caddy-blokken of -certs meer toe** (alleen bestanden syncen). Niet terugdraaien naar losse certs.
- Er staat ook een geplande herinnering (5 sep 2026) in de Cowork-app.

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

## Kappers-niche + premium-designs (VASTE FEIT — 16-06-2026)
- **Kapper is een volwaardige niche** in `generate-demo.py` (`niche:"kapper"`): eigen `KAPPER_MAP` (kapsalon-content, geen honden-/nagel-resten) + eigen Higgsfield-beelden (`_workflow/niche-images.json` → key `kapper`). Clients-label = **"Kappers"**.
- **Twee eigen premium-ontwerpen, beide bovenaan op de cover (vóór Champagne & Charcoal):**
  - **design-11** = donker/luxe à la haaratelier Mari (`_workflow/templates/design11-kapper.html`): **video-hero** (Higgsfield-clip `…b972a3a9….mp4`, met still als terugval), merkenregel, over-blok, voorbeeld-prijzen (alleen als prospect zelf geen prijzen heeft; label "* richtprijs"), 5★ voorbeeldreviews, openingstijden, Maps op plaats.
  - **design-12** = licht/warm à la kapsalon-asya.landingsite (`_workflow/templates/design12-kapper.html`): hero "op afspraak", 4 behandelingen, 4 redenen, 5 reviews, contactblok + openingstijden-week (voorbeeld).
  - Beide met **onze vaste eisen**: prominente **cal.eu**-boeking (`brabantdigital/demo-planner`), **contactformulier** (mailto bij bekend e-mailadres), **WhatsApp-knop + zwevende "App ons"-pil** (alleen als een **mobiel** nummer bekend is), **NL/EN-knop**, Maps op plaatsniveau, mobielvriendelijk.
- design-12 wordt als 12e kaart in de coverpagina geïnjecteerd door de generator (alleen voor niche kapper).
- **Per niche een eigen premium**: voor nieuwe niches (barber/lash/beauty…) maken we op dezelfde manier eigen demo-content + (waar nodig) eigen premium-designs. Beelden via **Higgsfield** (generate_image/generate_video), vastgelegd in `niche-images.json`.

## new-client.py — niche-herkenning + outreach-velden (VASTE AFSPRAAK — 16-06-2026)
- De "Nieuwe klant"-upload herkent de niche uit de ingetypte tekst en koppelt die aan zowel de **generator-niche** als het **canonieke categorie-label**:
  pedicure/voet→`pedicure`/"Pedicures" · nagel/nail→`nagels`/"Nagelstudio's" · **kapper/kapsalon/barber/haar→`kapper`/"Kappers"** · hond/trim/dog→`hond`/"Hondentrimsalons". Anders → hond-fallback (let op).
- **Outreach-velden worden nette, niche-gerichte teksten** (compliment opent op niche+plaats en loopt door op "Daarom schrijf ik je."; `gratis_tip` = echte niche-tip; `verbeteringen` = voordelen). **NOOIT** de notitie of website-status in `gratis_tip`/`compliment` zetten (anders krijg je "Hoi, Daarom schrijf ik je." + "verouderde website" in de tip).

## Dashboard & deploy — fixes (VASTE FEIT — 16-06-2026)
- **Mobiel-menu**: sidebar sluit nu (backdrop + ✕ + sluit bij navigatie).
- **Autopilot aan/uit + dagcap**: server-persistent (laadt uit `/api/status`, slaat alle wijzigingen op); overal identiek. 3e schakelaar gewired; "Opslaan" wist `on` niet meer.
- **Replies in "Activiteit"**: elke reply (uit `replies.json`) verschijnt bij de klant in de Activiteit-tijdlijn (onderwerp + datum). `replyOf()` object-fix.
- **scan-replies.py** corrumpeert `niet-deployen.txt` niet meer (leest regel-voor-regel, schrijft met header terug).
- **vps-autodeploy.sh** is robuust (geen abort bij 1 klant-fout, `flock -w 50`) en synct nu ook de **hoofdsite** (`brabantdigital/site` → `/var/www/brabantdigital`). Caddy serveert demo's via één **wildcard-cert** (zie cert-sectie); autodeploy vraagt géén losse certs meer aan.

## Niche Schilders & Stukadoors — PREMIUM-ONLY (VASTE FEIT — 20-06-2026)
- **Eén niche** `niche:"schilder"` voor schilders én stukadoors (slimme labeling per prospect). Clients-label = **"Schilders & Stukadoors"**. Zoektermen: "stukadoor", "schilder", "stukadoorsbedrijf", "schildersbedrijf", "stukadoor en schilderbedrijf" (+ synoniemen).
- **Alleen premium-demo's** (GEEN 10 standaarddesigns). De generator (`generate-demo.py`) heeft een schilder-tak die `gen_premium.py` aanroept: schrijft eigen coverpagina (`index.html`) + 6 previews (`previews/design-1..6.html`) per slug. Templates in `_workflow/templates/premium{1..6}-schilder.html`.
- **GEEN cal.eu in deze niche** — uitsluitend een **contactformulier** (mailto naar prospect-e-mail indien bekend, anders demo-bedankmelding). Prijscalculator mogelijk later.
- Voor/na-slider ALLEEN in design 1 ("Charcoal & Oranje") en design 2 ("Zwart & Goud"). Eigen foto's van Pro4Never in `assets/voornaa/`. Higgsfield-beelden per design (elk een eigen stijl, niet op elkaar lijkend).
- WhatsApp 'App ons'-pil alleen als een **mobiel** nummer bekend is. NL/EN-knop, Maps op plaatsniveau, mobielvriendelijk.
- Volledige bron-analyse + designspecs: `_workflow/premium-schilder-spec.md`.

## Werven — credit-zuinige engine + HANDMATIGE scheduled taken (VASTE AFSPRAAK — 20-06-2026)
- **Werving/verrijking draait HANDMATIG**, niet via cron. De scheduled taken zijn "ad-hoc" (alleen "Run now" in de Scheduled-balk) zodat er NOOIT automatisch credits verbranden. Er is geen API om een taak te triggeren — Pro4Never start ze zelf met **Run now** (draait in vers geheugen, doet ~25/run + creditrapport). Taken: `schilders-stukadoors-werven-nl`, `trimsalons-werven-nl`, `trimsalons-verrijken-100-handmatig`, `sandbox-opruimen` (allen handmatig) + `wildcard-cert-verlengen-demo` (one-time 05-09-2026).
- **Credit-zuinig (HARD):** per kandidaat eerst `firecrawl_search` (±2 cr — snippets bevatten vaak e-mail/telefoon), pas `firecrawl_scrape` markdown (1 cr) als de eigen site écht ingezien moet worden, `screenshot` (1 cr) alleen bij twijfel over site-kwaliteit. **NOOIT** json-scrape (5 cr) of `firecrawl_extract` tenzij echt nodig. Houd een creditteller bij, **STOP zodra een run > 1200 credits** gebruikt, **NOOIT upgraden** (Smart Upgrade staat uit / moet uit blijven), **waarschuw bij < 250 resterende credits**.
- **Gratis lokale pass eerst** (0 cr): bij verrijking e-mail/telefoon/social uit het bestaande `contact`-veld halen voordat je Firecrawl inzet.
- **Dubbel werk voorkomen bij verrijking:** `verrijkt`-datumvlag op elke klant; alleen klanten zónder vlag oppakken, en na verwerking de vlag zetten (ook als niets gevonden). Commit+push, anders is voortgang niet bewaard.

## Prospect-kwalificatie — 10-punts site-rubric (VASTE AFSPRAAK — 20-06-2026)
- Werkwijze-docs: `05-marktonderzoek/prospect-werkplan.md` (run-niveau) + `prospect-onderzoek-werkwijze.md` (per bedrijf, 7 stappen).
- **Bereikbaar contact VEREIST:** 06-mobiel OF e-mail OF social. Een **vaste lijn telt NIET**.
- **Prospect = zwakke/verouderde site**: geen HTTPS, oud copyright of `last-modified` (bv. WordPress 2018), geen offerteformulier, JouwWeb/Wix, fax-tijdperk, niet mobiel, alleen social, of geen site. Een goede moderne site valt af, tenzij Pro4Never 'm als redesign-kans aanwijst.
- **"Leeg ≠ afwezig"** + altijd Google Bedrijfsprofiel checken vóór een conclusie. Bij eigen site: meerdere pagina's crawlen (home + contact). **Nooit bedrijven of contactgegevens verzinnen** — altijd verifiëren met bron-URL.

## Bouwen + pushen — operationele valkuilen (VASTE FEIT — 20-06-2026)
- Git werkt NIET in de Cowork-map → altijd een **verse sandbox-clone** in /tmp (token uit `_workflow/.deploy-token`), eerst `git pull`.
- **`/tmp/new_quals.json` is van een andere uid → Permission denied.** Schrijf je quals-array naar een schrijfbaar pad in de clone en pas het pad in add-prospects.py aan met sed: `sed "s#/tmp/new_quals.json#mijnpad.json#" _workflow/add-prospects.py > _run_add.py && python3 _run_add.py`.
- **Quals-entry-schema** (per prospect): `slug, bedrijf, kort, plaats, regio, niche, eigenaar, tel, email, social, verhaal, spec[], cert[], waarom`. `add-prospects.py` vult hieruit `salons-batch1.json` + `dashboard/clients.json` + `outreach/prospects.json`; daarna `python3 _workflow/generate-demo.py`.
- **Pushen:** gebruik `git push -q origin HEAD:main` — NIET `git push HEAD:main` (git parst dan `HEAD` als remotenaam → "ssh: Could not resolve hostname head").
- **Check na build:** geen onvervulde `{{tokens}}` in de HTML (grep-treffers in binaire jpg's negeren), naam/telefoon/mailto correct gevuld, 6 designs aanwezig, schilder = géén cal.eu. Ruim scratch op vóór commit. VPS publiceert binnen ~1 min.
- **Mount-valkuil (NIEUW 20-06-2026):** de bash-sandbox kan een door de Edit/Write-tool bijgewerkt bestand in de Cowork-map verouderd/afgekapt teruglezen. Sync naar git daarom door de wijziging **direct in de clone** te schrijven, niet door uit de mount te kopiëren.
- **Recent toegevoegd (20-06-2026):** `antoonvandenbergstucadoors` (Breda — http/geen HTTPS, ©2015) en `mtstukadoors` (Oosterhout — WordPress, last-modified 2018, geen formulier).

## E-mail deliverability (VAST FEIT — uitgezocht 2026-06-20, NIET opnieuw doen)
- Verzending loopt via **mail.zxcs.nl** (465 SSL, user `aanbod@brabantdigital.nl`), outbound via zxcs `filter-out.zxcs.nl`-pool — NIET direct vanaf het VPS-IP. rDNS van de VPS is irrelevant voor e-mail.
- **SPF ✓, DKIM ✓ (zxcs-selector `x`), DMARC ✓** (`p=quarantine`, aligned). Authenticatie is dus in orde.
- **Spam bij Hotmail/Outlook ligt NIET aan DNS**, maar aan: gedeelde zxcs-IP-reputatie bij Microsoft, cold-outreach-filtering (SmartScreen), jong domein, geen Microsoft SNDS/JMRP. Hefbomen: SNDS+JMRP registreren/delisten, warm-up + laag volume, minder links, evt. dedicated cold-outreach-infra. Zie `_workflow/SESSIE-OVERDRACHT-2026-06-20.md`.
