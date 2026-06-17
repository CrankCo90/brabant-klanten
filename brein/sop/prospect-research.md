# SOP — Prospect research (stap voor stap)

> Verkorte, uitvoerbare versie. Volledige uitleg: [onderzoeks-werkwijze (7 stappen)](../../05-marktonderzoek/prospect-onderzoek-werkwijze.md).
> Dit is de "gouden lijn" die we per agent/workflow-stap automatiseren (zie [Systeemplan](../../_workflow/SYSTEM-PLAN.md)).

## Doel
Per stad × niche echte, **bereikbare** prospects vinden met een **zwakke/geen/alleen-social** website, en die omzetten in demo's.

## Stappen
1. **Zoekwoorden** — meerdere per niche (zie `_workflow/niche-zoekwoorden.json`). Niet vasthouden aan één term (hond: hondentrimsalon, trimsalon, dierenkapper, hondenkapper, hondensalon…).
2. **Plaats** — volgende stad uit `dashboard/nl-provincies-steden.json`. Rond grote steden én juist kleine plaatsen. Houd coverage bij (zie Dekkingskaart).
3. **Zoeken** — per stad × zoekwoord via: Google, Google Maps, branchegidsen (hondentrimsalon-info.nl / nagelstudio-info.nl / pedicure.nl), Treatwell/Salonized/Fresha, Instagram/Facebook, telefoonboek/goudengids/cylex/doggo, KvK.
4. **Kwalificeren** — bereikbaar contact = **06-mobiel óf e-mail óf social**; vaste-lijn-only telt NIET. Zwakke/geen/alleen-social site = prospect; goede eigen site valt af. **Nooit verzinnen.**
5. **Dedupe** — tegen `dashboard/clients.json` (bedrijf) + `_workflow/salons-batch1.json` (slug).
6. **Content + beeld** — per niche eigen teksten/diensten + Higgsfield-beelden (`niche-images.json`). Nieuwe niche = eigen vertaalmap + premium-designs.
7. **Bouwen** — `add-prospects.py` + `generate-demo.py` (11 designs + cal.eu).
8. **Publiceren** — commit + push; VPS autodeploy zet live (wildcard-cert).
9. **Outreach** — autopilot mailt/appt e-mailbare, niet-benaderde prospects binnen kantooruren tot dagcap.
10. **Opvolgen** — `scan-replies.py`: "nee" → afgewezen + offline + blocklist; reply in dashboard-Activiteit.

## Kwaliteitsregels
- Liever 20 kloppende prospects dan 100 met fouten.
- Geen AI-/interne verwijzingen of website-status in de outreach-teksten of demo's.
- Status nieuwe prospect = `concept` tot de autopilot 'm oppakt.
