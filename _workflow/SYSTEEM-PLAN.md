# Systeemplan — "Jarvis" + geautomatiseerde prospect-workflow

> Doel: het werk dat we nu handmatig/half-automatisch doen (prospects vinden → kwalificeren → demo bouwen → publiceren → benaderen → opvolgen) opdelen in losse, automatiseerbare stappen die elk door een eigen agent gedaan kunnen worden, aangestuurd door één "brein" (Jarvis) met geheugen en interfaces (dashboard, spraak, Telegram). Onderaan staat een gefaseerd stappenplan dat van makkelijk naar uitgebreid loopt.

## 1. De ruggengraat: wat gebruiken we waarvoor
- **n8n (al gekoppeld) = de workflow-/orkestratiemotor.** Visuele workflows, triggers (schedule, webhook, Telegram), HTTP-, Code- en AI-Agent-nodes, en het kan MCP-tools en Claude aanroepen. Hierin zetten we elke stap als node/sub-workflow.
- **Claude (Agent SDK / Cowork-agents) = het redeneren.** De "denkende" stappen (zoekwoorden bedenken, kwalificeren, content schrijven) draaien als Claude-agents, aangeroepen vanuit n8n of als Cowork-subagents.
- **VPS + Git-pipeline = de uitvoer.** Demo's bouwen (`generate-demo.py`), publiceren (autodeploy + wildcard-cert), outreach (autopilot), reply-scan. Blijft zoals het is.
- **Higgsfield-MCP (gekoppeld) = beeld/video** per niche.
- **Telegram = jouw afstandsbediening** via de n8n Telegram-node (geen aparte MCP nodig): je stuurt commando's ("voeg 50 trimsalons in Gelderland toe", "status?", "rapport") en krijgt antwoord/PDF/links terug.
- **Geheugen**: kort = n8n Data Tables; lang/structuur = Postgres op de VPS (evt. met pgvector voor semantisch geheugen) of Notion-MCP als kennisbank; projectgeheugen = `CLAUDE.md` + overdrachten (bestaat al).
- **Kaart**: in het bestaande admin-dashboard, gevoed door onze eigen data (`nl-provincies-steden.json` + coverage-status per stad/niche). Geen externe MCP nodig (Felt Maps-MCP is optioneel).

## 2. De prospect-workflow, minutieus (de "gouden lijn")
Elke stap is los uitvoerbaar en wordt straks een agent/sub-workflow:

1. **Zoekwoorden bepalen** — per niche meerdere termen (zie `_workflow/niche-zoekwoorden.json`). Agent kan de lijst uitbreiden met nieuwe synoniemen.
2. **Plaats kiezen** — volgende stad uit `dashboard/nl-provincies-steden.json` (per provincie, rond grote steden én kleine plaatsen). Houd bij welke stad×niche al "gedaan" is (coverage-status).
3. **Zoeken** — per stad × zoekwoord via: Google web, Google Maps, branchegidsen (hondentrimsalon-info.nl / nagelstudio-info.nl / pedicure.nl), Treatwell/Salonized/Fresha, Instagram/Facebook, telefoonboek/goudengids/cylex/doggo, KvK. Verzamel kandidaten (naam, plaats, telefoon, social, website).
4. **Kwalificeren** — regels: bereikbaar contact = 06-mobiel ÓF e-mail ÓF social (vaste lijn alléén telt niet); zwakke/geen/alleen-social site = prospect, goede eigen site valt af. NOOIT iets verzinnen.
5. **Dedupe** — tegen `dashboard/clients.json` (bedrijf) + `_workflow/salons-batch1.json` (slug).
6. **Content + beeld** — per niche eigen teksten/diensten + beelden (Higgsfield, `niche-images.json`). Voor nieuwe niches: vertaalmap + premium-designs (zoals kapper).
7. **Bouwen** — `add-prospects.py` (JSON's bijwerken) + `generate-demo.py` (11 designs + cal.eu).
8. **Publiceren** — commit + push; VPS autodeploy zet live (wildcard-cert).
9. **Outreach** — autopilot mailt/appt e-mailbare, niet-benaderde prospects binnen kantooruren tot dagcap.
10. **Opvolgen** — `scan-replies.py`: "nee" → afgewezen + demo offline + blocklist; "ja" → in rapport; reply in dashboard-Activiteit.
11. **Coverage bijwerken** — per stad×niche status (gevonden / gebouwd / benaderd / reacties) → voedt de kaart.
12. **Rapporteren** — dagrapport + Telegram-statusantwoorden.

## 3. Opdeling in agents (multi-agent)
- **Jarvis-router** — ontvangt jouw intentie (dashboard/Telegram/spraak) en start de juiste workflow met parameters.
- **Keyword-agent** — beheert/uitbreidt zoekwoorden per niche.
- **Research-agent** — stap 3-4 per stad×zoekwoord (kan parallel over meerdere steden tegelijk → grotere batches!).
- **Qualify/Dedupe-agent** — stap 4-5.
- **Content-agent** — stap 6 (nieuwe niche-content + beelden).
- **Builder/Publisher-agent** — stap 7-8.
- **Outreach-agent** + **Reply-agent** — stap 9-10 (bestaat grotendeels al).
- **Coverage/Report-agent** — stap 11-12 (voedt kaart + rapporten).

> **Grotere batches** komen niet van "meer per agent-run" (de research is het bottleneck) maar van **parallelle research-agents**: n8n splitst een lijst steden en draait N branches tegelijk, of we starten meerdere Cowork-subagents in één keer. Dat is dé manier om van 10-15 → 50-100+ per ronde te gaan.

## 4. De kaart-view (dashboard)
- Klikbare kaart van NL → provincies → steden (data uit `nl-provincies-steden.json`).
- **Inkleuring naar voortgang** per stad: # prospects gevonden / gebouwd / benaderd / reacties → kleurintensiteit ("heatmap van dekking").
- **Per-niche filter** (trimsalons, nagelstudio's, pedicures, kappers): is de kaart "vol" voor één niche, dan schakel je naar de volgende.
- Technisch: een NL-provincie/gemeente SVG of GeoJSON + onze coverage-JSON; rendert in het bestaande admin-dashboard. Geen externe dienst nodig.

## 5. Gefaseerd stappenplan (makkelijk → uitgebreid)
- **Fase 0 — Fundament (deze sessie):** provincie/stad-lijst ✓, niche-zoekwoorden ✓, dit plan ✓, en de zelf-opruimende prospect-taak ✓.
- **Fase 1 — Kaart-view in dashboard:** coverage per stad×niche tonen + inkleuren. Snel zichtbaar resultaat; geeft jou overzicht en stuurt de zoekvolgorde.
- **Fase 2 — Research als n8n-workflow met parallelle batches:** stad-lijst → parallelle research-branches → qualify → dedupe → build → push. Hiermee grote batches en betrouwbaar (logging, retries) i.p.v. één Cowork-taak.
- **Fase 3 — Telegram-Jarvis:** n8n Telegram-bot. Commando's: status, "voeg N <niche> in <provincie> toe", dagrapport, pauzeer/hervat. Jij stuurt het hele systeem vanaf je telefoon.
- **Fase 4 — Geheugen + brein:** Data Tables/Postgres voor coverage, prospect-historie en "wat is al geprobeerd". Jarvis-router die intenties naar workflows vertaalt.
- **Fase 5 — Nieuwe niches + Jarvis-chat/spraak:** content-agent per niche (kapper-aanpak hergebruiken) en een chat-/spraakpaneel in het dashboard.

## 6. Aandachtspunten / lessen
- **Schijfopruiming:** autonome taken die clonen MOETEN hun clone opruimen (anders loopt de sandbox-schijf vol — dat is gebeurd; de taak ruimt nu eerst op). In n8n geldt hetzelfde: werk in tijdelijke mappen en ruim op.
- **Integriteit:** nooit bedrijven/contacten verzinnen — de autopilot mailt echte mensen. Elke prospect = echt, geverifieerd, met reden.
- **Kosten:** Higgsfield-credits (beeld/video) en eventuele API-kosten in de gaten houden; per niche beelden hergebruiken.
- **Kwaliteit > snelheid:** liever 20 kloppende prospects dan 100 met fouten.

## 7. Wat nu klaar staat & de eerstvolgende stap
- Klaar: `dashboard/nl-provincies-steden.json`, `_workflow/niche-zoekwoorden.json`, dit plan, en de gerepareerde auto-taak.
- Aanbevolen eerste bouwstap: **Fase 1 (kaart-view)** — direct visueel en stuurt de rest. Daarna Fase 2 (parallelle n8n-research) voor de grote batches.
