# Sessie-overdracht — 15 juni 2026

Samenvatting van wat we deze sessie hebben gedaan, afgesproken en gewijzigd. De vaste afspraken staan
ook in `CLAUDE.md` (laadt elke sessie automatisch). Lees bij opstart éérst `CLAUDE.md` + de nieuwste
`SESSIE-OVERDRACHT-*.md`.

## 1. Prospect-campagne afgerond (100 per niche → toen aangescherpt)
- Heel Noord-Brabant uitgekamd via parallel onderzoek (7-stappen-werkwijze). Bereikt: pedicure 107,
  nagelsalon 106, hondentrimsalon 99 in `05-marktonderzoek/master-prospects-NB.md`.

## 2. Demo's gebouwd voor alle bereikbare prospects
- Eerst **168 demo's** gebouwd (nagel 63, pedicure 55, hond 50), elk 11 designs + werkende cal.eu.
- Generator uitgebreid: **design-11 nu voor álle niches** (`render_d11_nagel` + `render_d11_hond` +
  templates `_workflow/templates/design11-nagel.html` / `design11-hond.html`). Cal-blok geïnjecteerd uit
  de geverifieerde generator-`CAL` (de oude `_mockups`-templates hadden nog de kapotte `#contact`-knop).

## 3. Contactregel aangescherpt (BELANGRIJK)
- Een prospect blijft alleen in de lijst met **e-mail OF social OF 06-mobiel**.
- **Vaste lijn (040/073/013/0162 enz.) telt NIET.** Geen van de drie → verwijderen + vervangen.
- Hierop: **25 vaste-lijn-only klanten verwijderd** (incl. demo's), **2 zonder enig contact** verwijderd,
  en **35 nieuwe prospects** met 06/mail/social toegevoegd (Valkenswaard, Best, Veghel, Uden, Boxtel,
  Oisterwijk, Dongen, Goirle, Drunen, Kaatsheuvel, Son, Waalwijk) — elk met volledige 11-design demo.
- Eindstand lijsten: **clients ~248 · prospects ~232 · salons-batch1 ~231**. 0 prospects zonder 06/mail/social.

## 4. Outreach-mails gerepareerd
- De oude entries hadden de website-status in `gratis_tip` en de fouten-lijst in `verbeteringen` →
  kapotte mail. Alle **232 prospects** opnieuw gevuld:
  - `compliment` = nette opener (niche + plaats) die op "Daarom schrijf ik je" doorloopt.
  - `gratis_tip` = echte tip (Google-bedrijfsprofiel / Instagram-bio-link).
  - `verbeteringen` = voordelen (online afspraken, vindbaarheid, WhatsApp/bel, NL/EN, mobiel).
- Tip-zin geherformuleerd: *"Een tip die ik je sowieso gratis wil meegeven, ook als je verder niets met deze mail doet:"*
- **List-Unsubscribe (mailto) header** toegevoegd aan `send-one.py` en `send-outreach.py` (mail-tester groen).
- Niets verzonden: alle prospects op `concept` (alleen `klaar` wordt gemaild).

## 5. Nieuw telefoonnummer + WhatsApp
- Nieuw: **085-0608491**, WhatsApp **wa.me/31850608491**.
- Vervangen in: outreach-mails, **alle 232 demo-coverpagina's**, BD-site, onboarding, CLAUDE.md, STRATEGIE.
- **Meelopende 'App ons'-WhatsApp-knop** toegevoegd aan elke demo-coverpagina (`id="bd-wa-float"`,
  vaste pil rechtsonder, opent wa.me) + in de brontemplate → automatisch in nieuwe demo's.

## 6. Afleverbaarheid / spam (advies, nog te doen door Pro4Never)
- mail-tester gaf 10/10 maar testmail belandde in Ziggo-spam. 10/10 ≠ inbox: ontvanger weegt
  afzender-/IP-reputatie. **Grootste hefboom: versturen via een mailrelay** (Postmark/Brevo/Mailgun) met
  DKIM op brabantdigital.nl i.p.v. het VPS-IP. Plus: "geen spam" markeren + warm-up (laag volume).
- `wa.me` kan als "verkorte URL" gezien worden; desnoods `api.whatsapp.com/send?phone=31850608491`.

## 7. Dashboard — Acties & autopilot opgeschoond
- Outreach-wachtrij toont nu alleen **e-mailbare, nog-niet-gemailde** klanten; gemailde vallen er
  automatisch uit (via `sent-log.csv`). Geen dubbele mails meer. Test-mail telt niet mee.
- **"Publiceer demo's"-knop verwijderd** (beide plekken + handler): autodeploy publiceert al elke minuut.

## 8. Outreach/autopilot gerepareerd + volledig geautomatiseerd
- **Bugs gefixt:** niets werd verstuurd (status-gate `klaar` terwijl alles `concept`); 13 e-mails ontbraken
  in prospects.json (gesynct vanuit clients.json); bulk-knop sprak verkeerde sleutel aan (`only` vs
  `prospects`); "Status verversen"-knop had geen handler; settings-ops
## 9. Outreach-engine extra fixes (laatste ronde)
- "Verstuur outreach naar geselecteerde" in de Acties-sectie werkte niet (`data-act="send-sel"` had geen
  handler) → gekoppeld. Vereist wel `sudo systemctl restart bd-control` voor de `only`-fix.
- Dagrapport-test: `daily-report.py` handmatig draaibaar (naar leroyb@home.nl). Testmodus niet gewenst.
