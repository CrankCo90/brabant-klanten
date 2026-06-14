# Brabant Digital — Overdracht & Status
_Laatst bijgewerkt aan het einde van de werksessie. Bewaar dit als startpunt voor een volgende sessie._

## 1. Wat is dit project
Pro4Never (merk: **Brabant Digital**) maakt statische demo-websites voor lokale ondernemers,
zet ze live op een VPS, en benadert ze met een persoonlijk voorstel. Doel: de ondernemer koopt
de website (eenmalig), met optioneel maandelijkse hosting/onderhoud. Het hele proces is grotendeels
geautomatiseerd: prospects vinden → demo bouwen → publiceren → benaderen, aangestuurd vanuit een
eigen beheer-dashboard en een dagelijkse autonome ronde.

## 2. Aanbod & strategie
- **Prijs:** €199 EENMALIG. Geen abonnement, geen verplichte maandkosten, klant zit nergens aan vast.
  Normaal €499 (lanceringskorting i.r.v. een eerlijke review). Eerste maand gratis kleine aanpassingen.
- **Hosting:** optioneel, losse service (~€19/mnd), 12 mnd vooruit = 25% korting. Niet verplicht.
- **Doelgroep:** lokale ondernemers/zzp'ers die een website hard nodig hebben maar er vaak geen
  (goede) hebben. Niches die goed werken: hondentrimsalons, nagelstudio's, klusbedrijven, hoveniers,
  stukadoors, pakketpunten aan huis, schoorsteenvegers, e.d.
- **Prospect-regel:** per niche+regio 20-30 bedrijven scannen, ranken (webaanwezigheid, foto's,
  social, vindbaarheid, fulltime vs bijbaan); alleen de ZWAKSTE benaderen. Al-goede sites NIET.
- **Regio's:** standaard Noord-Brabant. Buitenland (bv. VS) kan ook — zie §8 (meertalig).

## 3. Status nu
- **61 klanten** in het dashboard: 41 hondentrimsalons + 20 nagelstudio's. Allen land=NL.
- Statussen: 39 "demo" (demo klaar), 1 "benaderd", 21 "afgewezen" (niet benaderen / al goede site).
- **56/61 hebben een geverifieerd telefoonnummer** (voor WhatsApp). 5 niet (Instagram-only e.d.).
- 9 hebben een eigen bron-website; de rest geen/zwakke site (= de pitch).
- 46 demo-mappen live op de VPS (incl. originele Scott-template).
- Prospects-wachtrij: 45 entries, 11 met e-mail, 9 op status "klaar" (klaar om te mailen).
- **Er is nog GEEN enkele e-mail of WhatsApp echt verstuurd** (afgezien van testmails naar jezelf/mail-tester).

## 4. Infrastructuur
- **VPS:** `93.190.187.213`, webserver **Caddy** (automatische HTTPS).
- **Demo-URL per klant:** `https://<slug>.demo.brabantdigital.nl` (wildcard `*.demo` staat in DNS).
- **Dashboard:** `https://brabantdigital.nl/admin` (achter login), bestanden in `/var/www/admin`.
- **Onboarding-formulier:** `https://brabantdigital.nl/welkom` → `/var/www/onboarding`.
- **Git-pipeline:** GitHub repo **CrankCo90/brabant-klanten** (privé). De VPS staat in `/root/klanten`
  en pullt automatisch (cron, elke ~15 min: `git reset --hard origin/main`). Publiceren naar de
  webroot gaat via `bash _workflow/vps-autodeploy.sh` (rsync demo's + dashboard + onboarding, Caddy reload).
- **control-server** (`_workflow/control-server.py`): Python-API op `127.0.0.1:8787`, via Caddy
  als `/api/*` met Bearer-token. Hierdoor kan het dashboard echte acties op de VPS uitvoeren
  (outreach versturen, status wijzigen, Claude-opdracht, nieuwe klant, autopilot).
- **Mail:** domein `brabantdigital.nl` draait bij **ZXCS** (DirectAdmin, nameservers ns.zxcs.*).
  Uitgaande mail via `mail.zxcs.nl` (poort 465, SSL), afzender `aanbod@brabantdigital.nl`.
  SMTP-gegevens staan in `/root/outreach-data/.smtp-env` (buiten git).
- **Claude Code op de VPS** draait als root in `/root/klanten`. Onbewaakte runs gebruiken
  `--permission-mode acceptEdits` (NIET `--dangerously-skip-permissions`; dat wordt door Claude Code
  als root geweigerd). Een `.claude/hooks/guard.sh` blokkeert catastrofale commando's.

## 5. Het beheer-dashboard
Eén-pagina-app (SPA) met inlog (wachtwoord; sha256-hash in de pagina). Stijl: **puur zwart + metallic goud**,
met een kosmische **themawisselaar** rechtsboven (Obsidian = standaard puur zwart, Nebula = paars,
Aurora = smaragd, Royal = melkweg-goud); keuze wordt onthouden.
- **Overzicht:** 5 stat-cards + status-donut + balken per regio (live uit de data).
- **Klanten = actie-bord:** een "To-do"-balk bovenaan — **Te doen** (X versturen · Y bouwen) staat
  standaard aan; **Benaderd** apart; daarnaast **Klanten** (gekocht) en **Archief**. Per rij staan
  **twee kanaal-knoppen**: **Mailen** (verstuurt echt via de VPS, met bevestiging) en **WhatsApp**
  (opent je Business-app met de tekst klaar; jij verstuurt zelf). Zodra een kanaal gedaan is wordt
  de knop **✓ Gemaild** / **✓ Geappt**. Een klant blijft in **Te doen** tot ALLE beschikbare kanalen
  gedaan zijn en schuift dan door naar **Benaderd**; "geen e-mail"/"geen tel" telt niet mee. De
  WhatsApp-status wordt in de browser onthouden (localStorage). Prospects zonder demo tonen "Bouw demo".
  Niche-chips + sorteren werken. Klik op een rij = detailpagina.
- **Detailpagina:** live **snapshots** van de huidige site én de demo (WordPress mShots), analyse
  ("waarom"), pitch-tips ("fouten"), bron-links (site/zoek), bedrijfsgegevens, status wijzigen
  (slaat echt op via VPS), lead-score-opbouw, en knoppen Bel/Mail/WhatsApp.
- **Outreach → WhatsApp appjes:** wachtrij met telefoon-prospects (zonder e-mail bovenaan); per
  prospect een persoonlijk appje klaar (bewerkbaar) + "Open in WhatsApp" (wa.me, jij drukt zelf op
  verzenden — volgens de regels, geen ban-risico) + "Markeer als geappt".
- **Outreach → Acties/Campagne/Testkopie**, **Claude AI → Vrije opdracht/Autopilot**,
  **Nieuwe klant** (met land/taal-keuze NL/VS), **Instellingen** (control-token invoeren).
- **Belangrijk:** het dashboard moet eenmalig met het **control-token** verbonden worden
  (Instellingen → VPS control-token plakken). Zonder token: data toont wel, acties niet.

## 6. De demo's
- Per klant **10 structureel verschillende designs** + een overzichtspagina (afkomstig van het
  Hondentrimsalon-Scott-sjabloon). De generator `_workflow/generate-demo.py` zet de Scott-templates
  om naar elke klant (naam/plaats/telefoon, eigen foto's of AI-foto's, content-sectie met
  Over-ons/tarieven/reviews, Cal-popup voor "Afspraak maken").
- **Foto's:** eigen foto's van de prospect als er ≥2 bruikbare zijn, anders AI-beelden uit een pool;
  nooit dezelfde foto herhalen.
- **Branding/prijzen** zitten in de demo's: €199 (was €499, doorgestreept), Web3Forms-contactformulier
  (sleutel mailt naar aanbod@brabantdigital.nl), WhatsApp-knop, geen AI/interne verwijzingen.
- **Taal:** NL-demo's zijn tweetalig met een NL/EN-knop. Buitenlandse demo's bouwen standaard in
  het Engels (zie §8).

## 7. Outreach (mail + WhatsApp)
- **Toon:** warm, persoonlijk, kort — als een mede-ondernemer. Opbouw: oprecht compliment → één
  echt bruikbare gratis tip → de demo-link → 3 concrete voordelen → rustige prijsalinea → zachte CTA.
  Templates: `_workflow/outreach/template-nl.txt` (+ herinnering/kort) en `template-en.txt`.
- **Personalisatie:** aanhef met voornaam ("Hoi <naam>," / "Hi <name>,"); een vangnet in de
  verzendscripts leidt de voornaam af uit de bedrijfsnaam als die ontbreekt.
- **Vangrails:** nooit hetzelfde adres twee keer (`sent-log.csv`), daglimiet (cap, standaard 20),
  rustige spreiding, afmeldregel + duidelijke afzender. Alleen mailen als er een werkende demo klaarstaat.
- **WhatsApp:** koud automatisch appen mag NIET van WhatsApp (ban-risico voor je zakelijke nummer).
  Daarom **klik-om-te-sturen**: Claude schrijft het appje, jij verstuurt met één tik vanuit je eigen
  Business-app. Werkt voor telefoon-only prospects.
- **DELIVERABILITY — OPENSTAAND, BELANGRIJK:** een mail-tester gaf 6.8/10. SPF ✓, DMARC ✓, maar
  **DKIM faalt**: de gepubliceerde DKIM-sleutel (selector `x`) bij ZXCS hoort niet bij de sleutel
  waarmee uitgaande mail wordt ondertekend. Dit is een ZXCS-kwestie (het DirectAdmin-paneel toont een
  andere sleutel dan wat authoritatief gepubliceerd wordt). **Actie: supportticket bij ZXCS** om de
  ondertekening en de gepubliceerde sleutel weer gelijk te trekken. Tot die tijd komt mail wél aan
  (SPF/DMARC slagen), maar niet optimaal. Stuur na de fix opnieuw een test naar mail-tester.com (mik 9-10/10).

## 8. Meertalig (NL vs buitenland)
- Elke klant heeft `land` ("NL"/"US"/…) en `taal` ("nl"/"en"). Bestaande 61 = NL.
- Buitenlandse klanten worden **in hun taal** benaderd: Engelse mailtemplate, Engelse WhatsApp-tekst,
  "Hi <naam>,"-aanhef, Engelse afmeldregel. Het dashboard toont een 🇺🇸 EN-tag.
- **Demo's voor buitenland bouwen standaard in het Engels** (generator zet `<html lang="en">` en
  toont Engels; info-labels vertaald). De ochtendronde schrijft de content in de taal van de klant.
- **NOG TE DOEN (pas bij start VS-outreach):** Spaanse 2e-taalknop op de Engelse demo's
  (i.p.v. NL). Vergt Spaanse vertalingen; de ochtendronde kan die per demo meeschrijven.

## 9. Dagelijkse autonome ronde
- Cron op de VPS draait elke ochtend (09:00) `_workflow/DAGELIJKSE-RONDE.md` via Claude Code.
- Stappen: marktonderzoek → niche+regio kiezen (NL of buitenland; land/taal bepalen) → ~20-30
  bedrijven vinden → scannen/ranken → ~20 zwakste kiezen → demo's bouwen → registreren in
  clients.json/prospects.json → publiceren → samenvatting loggen. **STOPT vóór het mailen.**
- Niches/regio's die al gedaan zijn staan in `_workflow/gedaan-niches.txt` (worden niet herhaald).
- Mailen/appen doe JIJ daarna via het dashboard (of zet autopilot aan).

## 10. Belangrijke bestanden
- `dashboard/index.html` — het volledige dashboard (SPA). `dashboard/clients.json` — alle klantdata.
- `_workflow/generate-demo.py` — demo-generator. `_workflow/salons-batch1.json` — bron per klant.
- `_workflow/new-client.py` — verwerkt een nieuwe klant (bouwt demo + registreert + pusht).
- `_workflow/outreach/` — `prospects.json` (wachtrij), `template-nl.txt` / `template-en.txt`,
  `send-outreach.py` (cron-mailer), `send-one.py` (testkopie), `scan-replies.py` (IMAP-reacties).
- `_workflow/control-server.py`, `vps-autodeploy.sh`, `push.sh`, `autopilot-run.sh`.
- `_workflow/DAGELIJKSE-RONDE.md` — het ochtendrecept. `_workflow/STRATEGIE.md`, `WORKFLOW.md` e.a.
- `CLAUDE.md` — projectgeheugen (regels/afspraken voor Claude).

## 11. Geheimen (waar ze staan — NIET in git/chat zetten)
- GitHub-token, dashboard-wachtwoord, control-token, SMTP-wachtwoord, git-token: bewaard buiten de repo
  (op de VPS in `/root/outreach-data/`, of lokaal). `.gitignore` houdt `.smtp-env`, `.control-token`,
  `.git-token`, `.deploy-token`, `sent-log.csv` uit git. Tip: wijzig het info@-mailwachtwoord dat
  eerder in de chat langskwam voor de zekerheid.

## 12. Openstaande punten / aandachtspunten
1. **DKIM bij ZXCS rechtzetten** (supportticket) — grootste deliverability-winst. Zie §7.
2. **Eerste echte outreach** nog niet verstuurd — wanneer jij klaar bent, via het dashboard
   (eerst eventueel 1 testronde, klein volume, opbouwen).
3. **Spaanse taalknop** op Engelse demo's: pas bouwen bij start VS-outreach.
4. 5 klanten zonder telefoonnummer (Instagram-only) — daar is WhatsApp niet mogelijk; eventueel via
   Instagram/Facebook-DM.
5. Controleer of **autopilot uit** staat als je nog niet automatisch wilt mailen.
6. Mail-/WhatsApp-historie van vóór de kanaal-vinkjes is niet geregistreerd; eerder benaderde klanten
   kunnen weer als "te doen" verschijnen. Vanaf nu wordt elk verstuurd kanaal bijgehouden
   (mail via de sent-log op de VPS, WhatsApp via de browser-localStorage).

## 13. Veelgebruikte commando's (op de VPS)
```bash
# Nieuwste versie + dashboard live zetten:
cd /root/klanten && git pull && rsync -a dashboard/ /var/www/admin/

# Alles publiceren (demo's + dashboard + onboarding):
cd /root/klanten && bash _workflow/vps-autodeploy.sh

# Ochtendronde handmatig draaien:
cd /root/klanten && claude -p "$(cat _workflow/DAGELIJKSE-RONDE.md)" --permission-mode acceptEdits

# Testkopie van een prospect-mail naar jezelf/mail-tester:
cd /root/klanten && OUTREACH_DATA=/root/outreach-data python3 _workflow/outreach/send-one.py "<bedrijf>" <adres>
```

## 14. Belangrijkste beslissingen deze sessie
- Dashboard volledig herbouwd in het nieuwe zwart/goud-design met actie-bord (To-do, Benaderd apart).
- Mails herschreven naar warm/persoonlijk; deliverability uitgezocht (DKIM-oorzaak gevonden bij ZXCS).
- WhatsApp-benadering toegevoegd als compliant "klik-om-te-sturen" wachtrij (geen auto-blast).
- Telefoonnummers verzameld en geverifieerd (56/61).
- Meertaligheid ingebouwd (NL/EN), demo's bouwen in de taal van de klant.
- Actie-bord gemaakt: Mailen + WhatsApp per rij met ✓-vinkje per kanaal; klant blijft in 'Te doen' tot beide kanalen gedaan zijn.
- Werkwijze: dashboardwijzigingen worden vóór publiceren in een nagebootste browser (jsdom) getest.
