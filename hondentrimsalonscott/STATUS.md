# STATUS — hondentrimsalonscott

- **Bron:** https://www.instagram.com/hondentrimsalonscott/ (GEEN website — sterkste pitch tot nu toe)
- **13-06-2026:** Fase 1 afgerond (analyse via live Instagram).
- **13-06-2026 (v2):** Fase 2 OPNIEUW gedaan op verzoek Pro4Never. Oude designs.html (10 kleurvarianten van 1 layout) bewaard als `03-designs/designs-OUD-10-kleurvarianten.html`.
  Nieuw: **10 structureel verschillende designs** als losse werkende mini-pagina's in `03-designs/previews/design-01..10.html`, plus overzicht `03-designs/designs.html` (iframes + fullscreen-knop per design).
  - A: 01 Champagne&Charcoal simpel · 02 Champagne&Charcoal uitgebreid (slideshow/deeltjes/tellers/scroll)
  - B luxe: 03 parallax (groen) · 04 animated paws (blush) · 05 cinematic (navy) · 06 3D-tilt (wit/terracotta)
  - C interactie: 07 voor/na-slider (mint) · 08 prijscalculator (honing) · 09 trim-quiz (mint/coral) · 10 boekingsflow (hout)
  - Elk design: eigen kleur, NL/EN-toggle, duidelijke "Afspraak maken".
  - AI-beelden via Higgsfield (soul_2), nu gehotlinkt vanaf cloudfront-CDN. **Voor echte site: lokaal hosten / vervangen door Scott's eigen foto's.**
- **Wacht op:** keuze top 3 designs door Pro4Never → daarna kleurkeuze → fase 3 (uitbouwen tot demo-sites).
- **Nog navragen bij Scott:** naam eigenaresse, openingstijden, prijzen, e-mail, KvK (nu placeholders). Typefout bio-adres "Zupthenstraat" → Zutphenstraat.
- **Demo-URL's (straks):** hondentrimsalonscott-a/-b/-c.demo.brabantdigital.nl

## Deploy (alle 10 designs als 1 demo)
- Aanpak: 1 subdomein per klant → **hondentrimsalonscott.demo.brabantdigital.nl** toont `03-designs/index.html` met alle 10.
- Bestanden klaar: `03-designs/index.html`, `previews/`, `localize-images.sh`, `caddy-snippet.txt`, en `DEPLOY.md` (Caddy, stap voor stap).
- Foto's: nu CDN-hotlinks; `./localize-images.sh` zet ze om naar lokale WebP (~2-4 MB) en vervangt de links.
- Stack = Caddy (niet nginx). CP2-VPS ruim voldoende; geen upgrade nodig voor statische demo's.

## LIVE (13-06-2026)
- Kiesdemo live: **https://hondentrimsalonscott.demo.brabantdigital.nl** (HTTPS via Caddy, geverifieerd).
- Klantpagina: Brabant Digital-gebrand, alle AI-/interne verwijzingen verwijderd, prijs €499→€199, WhatsApp + werkend Web3Forms-formulier.
- Auto-deploy actief: VPS-cron elke 15 min (`_workflow/vps-autodeploy.sh`) pullt uit GitHub-repo CrankCo90/brabant-klanten en publiceert.
- Wacht op: Scott's reactie / keuze ontwerp(en).
