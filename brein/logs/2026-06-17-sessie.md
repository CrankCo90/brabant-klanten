# Sessie-overdracht — 17 juni 2026

> Korte, leesbare samenvatting van wat we deze sessie hebben besloten en gebouwd.
> Nieuwste afspraken staan ook in `CLAUDE.md` en `brein/beslissingen.md`.

## 1. Dashboard — Activiteit met datum + tijd
- Nieuwe clients krijgen een veld **`aangemaakt`** (ISO datum+tijd, Europe/Amsterdam) van `add-prospects.py`; `werkdag` is nu dynamisch (dag van toevoegen), niet meer hardcoded.
- Klant-detail → **Activiteit** toont nu exacte datum+tijd ("17 jun 2026 · 14:32 (vandaag)") bij "Toegevoegd door Claude" en "Demo-website gebouwd".
- "Laatste social-post" verschijnt in Bedrijfsgegevens als bekend.

## 2. Social-recency criterium
- Social telt alleen als bereikbaar contact als het profiel **laatste post in 2026 of later** heeft. Stale (bv. niets sinds 2022) → social-only valt af. Onbekend = voordeel van de twijfel (`laatste_post` leeg).
- Heeft prospect óók 06-mobiel of e-mail → social-recency maakt niet uit.
- Ingebouwd in `ingest-prospects.py` (`MIN_POST_YEAR=2026`), de n8n-extractieprompt en het dashboard.

## 3. Bronnen-landschap (advies)
- **Gratis/scrapebaar:** branchegidsen (hondentrimsalon-info.nl e.a.), cylex/telefoonboek/openingstijden/doggo, OpenStreetMap (Overpass), branche-ledenlijsten (ABHB/ProVoet/ANBOS).
- **Officiële API:** KvK Zoeken (gratis-zoek, ~€6,40/mnd key) — ruggengraat/dedupe, geen contactdata. Key nog aanmaken op developers.kvk.nl.
- **Betaald / niet nu:** Apify (Google Maps + Instagram-recency), Google Places API.
- **Nooit:** ingelogde IG/FB als scraper koppelen (tegen Meta-ToS, ban-risico).
- **Keuze gemaakt:** gratis/goedkoop bronnen + hybride opzet met één verifieer-agent.

## 4. n8n research-workflow
- **v1** (alleen branchegids) en **v2** (gids+OSM) → **gearchiveerd/vervangen**.
- **v3 = actueel:** "Prospect Research — Multi-bron (v3)", id `uY6wxWKFIWJOCkfT`.
  - URL: https://dutchdigital.app.n8n.cloud/workflow/uY6wxWKFIWJOCkfT
  - **Bronnen (parallel per stad):** branchegids + OpenStreetMap + DuckDuckGo + **Google** ("Webzoek ophalen2").
  - **Verifieer-agent (Claude)** kruist bronnen, dedupet, vult velden aan, past regels toe (06/e-mail/actieve social, recency 2026+, betrouwbaarheid).
  - → Bundel → POST naar `https://brabantdigital.nl/api/add-prospects` (VPS bouwt demo's, pusht, logt).
- **Eerlijk over Google zonder API:** kaal google.nl scrapen geeft vaak consent-/"unusual traffic"-pagina's; DuckDuckGo blijft de werkpaard. Google-node is toegevoegd zoals gevraagd.
- **Steden gekoppeld:** de "Steden uitvouwen"-node haalt `nl-provincies-steden.json` op via `https://brabantdigital.nl/admin/nl-provincies-steden.json` en vouwt die uit. Plaatsen beheer je dus op één plek.
- **Limiet/throughput:** max **50 plaatsen per run**; venster **schuift 1 op per uur**; planner staat op **elk uur** → heel NL (736 plaatsen, 15 vensters) is na ~15 uur rond, daarna opnieuw. Elke stad krijgt `_venster` (bv. 3/15) mee ter controle.

### Nog te doen op v3 (door Leroy, eenmalig)
1. Open v3 → koppel credentials: **"Claude"** → *Anthropic account*; **"Naar VPS"** → *BD control token*; ververs de editor.
2. Verwijder evt. de losse kladnode "Webzoek ophalen1".
3. **Start (handmatig)** draaien → bevestig dat "Naar VPS" een 200 geeft (`ingest: +N …`).
4. Daarna: v1 uitzetten zodat v3 de enige motor is.

## 5. nl-provincies-steden.json
- Uitgebreid van ~230 naar **736 plaatsen** over alle 12 provincies (incl. veel kleine plaatsen).
- Voedt nu ZOWEL de kaart in het dashboard ALS de n8n-workflow.

## 6. Feedback over toegevoegde prospects (3 plekken)
- **n8n** "Naar VPS"-respons: `ingest: +N toegevoegd -> namen … | totalen {…}`.
- **brein/logs/<datum>-ingest.md**: kopje "## Toegevoegd" met bullet per prospect.
- **Dashboard**: Dekkingskaart-tellers + "Alle klanten" (nieuwste boven, status `concept`).

## 7. Open vraag / volgende stap
Nog te kiezen door Leroy:
- (a) **Inbound-formulier → auto-demo**: website-formulier → webhook → niche-detectie → demo bouwen + publiceren (volledig auto voor bestaande niches hond/nagel/pedicure/kapper).
- (b) **Research multi-niche** maken (v3 sturen met een niche-config: zoekwoord/gids/OSM-tag/label per niche).
- (c) Beide.
- Bij gloednieuwe niche zonder content/beelden: keuze tussen "demo met fallback + melding" of "alleen melding".
- Beeldgeneratie voor een nieuwe niche loopt nu nog via Higgsfield (via Claude/deze app), niet headless in n8n.
