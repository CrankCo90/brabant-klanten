# TOOLS — gratis/goedkoop, per categorie

> Regel: eerst de **aanrader**, daarna alternatieven. Alles hieronder is gratis of bijna gratis,
> en vereist géén programmeerkennis van de klant.

## 1. Boeken / live agenda (het belangrijkste verkoopargument)

| Tool | Prijs | Agenda-sync (Apple/Google) | Oordeel |
|---|---|---|---|
| **Cal.com** ⭐ | Gratis (individueel) | Ja, Google + Apple (iCloud) + Outlook, 2-richtingen | Aanrader. Embed in de site, klant koppelt eigen agenda in 5 min, krijgt pushmelding op telefoon bij boeking. Open source → later gratis self-host op jouw VPS onder eigen merk mogelijk. |
| Zoho Bookings | Gratis t/m 1 medewerker | Ja | Prima alternatief, iets zakelijker uitstraling. |
| Setmore | Gratis t/m 4 gebruikers | Google/Apple via app | Goed gratis plan. |
| SuperSaaS | ~€8/mnd | Beperkt | Nederlands, maar betaald → alleen op verzoek. |
| Google Agenda "afsprakenschema" | Gratis | Native Google | Gratis maar lelijk embedbaar, geen Apple-sync. Nood-optie. |
| Zelf bouwen | "gratis" | Zelf onderhouden | **Niet doen**: CalDAV/API-onderhoud, beveiliging, storingen = het tegenovergestelde van onderhoudsvrij. |

**Demo-aanpak:** maak één gratis Cal.com-account voor demo's. In elke demosite staat die widget
werkend. Bij verkoop maakt de klant z'n eigen gratis account (of jij doet dat als service).

## 2. Contactformulieren (geen server nodig)

- **Web3Forms** ⭐ — gratis, alleen e-mailadres nodig, formulier mailt direct naar klant. Geen account voor de klant.
- Formspree — gratis t/m 50 inzendingen/mnd.
- FormSubmit.co — gratis, geen registratie.

## 3. Afbeeldingen

- **Klantfoto's** van hun oude site = altijd basis (echt werk, echte salon).
- **AI-extra's:** je gekoppelde beeldgenerator in Cowork (hero's, achtergronden, sfeerbeelden in stijl van de klant).
- **Gratis stock:** Unsplash, Pexels, Pixabay (let op: échte dieren/salonfoto's verkopen beter dan stock).
- **Optimaliseren:** Squoosh.app (gratis, in browser) of automatisch door Claude (WebP, juiste formaten) — cruciaal voor snelheid/SEO.
- **Achtergrond verwijderen:** gratis via je gekoppelde generator of Photopea (gratis Photoshop in browser).

## 4. Vindbaarheid (SEO) — allemaal gratis

- **Google Business Profile** ⭐ — nr. 1 voor lokale bedrijven. Gratis. Reviews + kaart + openingstijden in Google. Elke klant hierop wijzen/instellen = enorme waarde, kost niets.
- **Google Search Console** — site aanmelden, sitemap indienen, zien waarop mensen zoeken.
- **Schema.org LocalBusiness** — bouwen we standaard in (Claude doet dit, klant merkt er niets van).
- **PageSpeed Insights** — gratis snelheidstest; ook leuk als bewijs in de pitch ("uw site scoort 34, onze demo 98").
- Bing Webmaster Tools — 2 min werk, gratis extra's.

## 5. Kaart, chat, reviews

- **Google Maps embed** — gratis routekaart op de contactpagina.
- **WhatsApp klik-om-te-chatten** (wa.me-link) — gratis, dé manier waarop NL-klanten contact willen.
- **Google reviews**: link "Bekijk onze reviews" + losse quotes als tekst op de site (gratis). Live review-widgets (Elfsight e.d.) zijn betaald → vermijden.

## 6. Hosting & domein

- **Demo's:** jouw VPS (zie `VPS-SETUP.md`). Eén wildcard-subdomein → onbeperkt demo's, €0 extra.
- **Domein voor jezelf:** Cloudflare Registrar (inkoopprijs, ~€9/jr) of Versio/TransIP (.nl vanaf ~€5/jr).
- **Klant live:** op jouw VPS (= jouw maandelijkse upsell) óf op hun bestaande hosting (statische bestanden uploaden — overal mogelijk).
- Gratis alternatief zonder VPS: Cloudflare Pages / Netlify (onbeperkt statische sites, gratis) — handig als back-up of als de VPS vol zit.

## 7. Statistieken (upsell-materiaal)

- **GoatCounter** — gratis, privacyvriendelijk, geen cookiebanner nodig. ⭐
- Cloudflare Web Analytics — gratis, geen cookies.
- GA4 — gratis maar vereist cookiemelding → liever niet voor kleine bedrijven.

## 8. Beheer & professionaliteit (voor jou)

- **UptimeRobot** — gratis monitoring; je krijgt bericht als een klantsite plat ligt = je "24/7 hulp"-belofte waarmaken.
- **rsync/scp** — demo's publiceren is één commando (staat in VPS-SETUP.md).
- E-mail op eigen domein: ImprovMX (gratis doorsturen, bijv. info@jouwdomein.nl → leroyb@home.nl).

## Kosten-samenvatting

| Post | Voor jou | Voor de klant |
|---|---|---|
| Website bouwen | €0 (Cowork) | eenmalige bouwprijs (jouw tarief) |
| Demo-hosting | VPS die je al hebt + ~€9/jr domein | €0 |
| Boekingssysteem | €0 | €0 (Cal.com gratis plan) |
| Formulieren, SEO, kaart, WhatsApp, statistieken | €0 | €0 |
| Live hosting | — | jouw maandelijkse upsell |
