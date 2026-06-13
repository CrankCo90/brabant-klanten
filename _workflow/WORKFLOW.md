# MASTER WORKFLOW — Van klant-link naar live demo

> Dit is het draaiboek. Bij elke nieuwe klant: open Cowork in deze map, plak de prompt uit
> `NIEUWE-KLANT.md` met de website-link, en Claude voert dit document uit.

## Gouden regels

1. **Elke klant = eigen map.** Nooit bestanden, foto's of thema's delen tussen klanten.
2. **Alles statisch.** Eindresultaat is pure HTML/CSS/JS — geen database, geen updates, vrijwel onderhoudsvrij.
3. **Gratis/goedkoop eerst.** Geen betaalde software voor klant of voor ons, tenzij het echt niet anders kan (zie `TOOLS.md`).
4. **Klant afgewezen? Demo van VPS halen, map bewaren.** Klant kan later terugkomen.
5. **Na ELKE edit aan websitebestanden geeft Claude direct de upload-commando's** (rsync/scp vanaf PC + chmod op VPS) — Pro4Never hoeft er nooit om te vragen.
6. **De klant kiest zelf.** Niet wij pre-selecteren: we zetten ALLE 10 designs live onder één subdomein zodat de klant in z'n eigen tempo kan kiezen.

## Mapstructuur per klant

Bij een nieuwe klant (bijv. `https://www.trimsalonbyfem.nl/`) wordt dit aangemaakt:

```
trimsalonbyfem/
├── STATUS.md             ← fase, datums, beslissingen, demo-URL
├── DEPLOY.md             ← upload-/Caddy-commando's voor deze klant (Claude vult in)
├── 01-analyse/
│   ├── inhoud.md         ← alle teksten, diensten, prijzen, openingstijden, contactgegevens
│   ├── stijl.md          ← huidige kleuren, fonts, sfeer van de oude site
│   └── gemist.md         ← wat de huidige site MIST (= onze verkoopargumenten)
├── 02-media/
│   ├── origineel/        ← foto's gedownload van hun huidige site
│   └── ai/               ← AI-gegenereerde luxe extra's (passend bij hun stijl)
├── 03-designs/           ← de "kiesdemo": ALLE 10 designs onder 1 subdomein
│   ├── index.html        ← overzicht met de 10 designs (Fullscreen + Nieuw tabblad per stuk)
│   ├── previews/         ← design-01..10.html = 10 werkende mini-pagina's
│   ├── assets/img/       ← lokale WebP-foto's (na localize-images.sh)
│   ├── localize-images.sh← CDN-foto's → lokale WebP + links vervangen
│   └── caddy-snippet.txt ← kant-en-klaar Caddy-blokje
├── 04-websites/          ← pas NA de keuze: de gekozen designs volledig uitgebouwd
│   ├── site-A/           ← volledige website, gekozen design 1
│   ├── site-B/           ← volledige website, gekozen design 2
│   └── site-C/           ← volledige website, gekozen design 3
└── 05-offerte/
    └── pitch.md          ← verkooppraatje: wat ze missen + wat wij leveren
```

---

## FASE 1 — Analyse (Claude doet dit automatisch)

1. Maak de klantmap aan (naam = domeinnaam zonder www/.nl).
2. Bezoek de website en **alle** subpagina's (home, diensten, prijzen, over ons, contact, etc.).
   - Eerst via web fetch; als de site JavaScript-gerenderd is, via de Chrome-browser tools.
   - Heeft de klant GEEN website (alleen social media)? Analyseer dan het Instagram/Facebook-profiel — "geen website" is juist het sterkste verkoopargument.
3. Sla op in `01-analyse/`:
   - `inhoud.md`: alle teksten letterlijk + diensten + prijzen + adres + telefoon + e-mail + openingstijden + socials + KvK indien vermeld. Ontbrekende info = noteren als "navragen".
   - `stijl.md`: kleurenpalet (hex), fonts, beeldtaal, tone-of-voice.
4. Download alle bruikbare afbeeldingen naar `02-media/origineel/` (logo, salonfoto's, werkfoto's).
   - Let op: Instagram-/CDN-foto-URL's verlopen vaak → niet hotlinken, downloaden of AI-beelden maken.
5. Schrijf `gemist.md` — controleer minimaal op:
   - [ ] Online boekingssysteem (live agenda)
   - [ ] Mobielvriendelijk (responsive)
   - [ ] HTTPS / SSL
   - [ ] SEO-basis: title/meta description per pagina, koppenstructuur
   - [ ] Google Business Profile koppeling + reviews zichtbaar
   - [ ] Schema.org LocalBusiness-markering (lokale vindbaarheid)
   - [ ] WhatsApp-knop (klik-om-te-chatten)
   - [ ] Duidelijke prijslijst
   - [ ] Snelheid (PageSpeed)
   - [ ] Engelse versie / taalknop
   - [ ] Foto's van werk (voor/na), team
   - [ ] Routekaart (Google Maps embed)

## FASE 2 — 10 verschillende designs (werkende mini-pagina's) + live kiesdemo

> Géén 10 kleurvarianten van één layout. **10 structureel verschillende** ontwerpen,
> elk een werkende mini-pagina met eigen kleur, NL/EN-toggle en duidelijke "Afspraak maken".

1. Bouw 10 designs in `03-designs/previews/design-01..10.html`. **Vast recept** (interactie
   aanpassen aan het type bedrijf):
   - **2× signature** — zelfde luxe opzet, 2 niveaus: `01` simpel/clean · `02` uitgebreid
     (foto-slideshow + Ken Burns, zwevende deeltjes, meetellende cijfers, scroll-reveals).
   - **4× luxe** — elk een andere wow-techniek + eigen kleur: `03` parallax + scroll-reveal ·
     `04` animated particles/pootjes · `05` fullscreen cinematic (scroll-snap/Ken Burns) ·
     `06` 3D-tilt op muisbeweging.
   - **4× interactie** — de bezoeker doet mee (kies wat bij het bedrijf past): `07` voor/na-slider ·
     `08` prijscalculator · `09` keuze-quiz ("welke behandeling/dienst past bij mij?") ·
     `10` mock-boekingsflow (kalender → tijd → bevestiging).
2. Elk design: eigen kleurpalet, **NL/EN-knop** (simpele JS-toggle, geen plugins), echte
   klantteksten, AI-beelden uit `02-media/ai/` of klantfoto's. Animatie-libraries mogen.
3. Maak `03-designs/index.html`: overzicht dat de 10 in iframes toont, in 3 categorieën,
   met per design een **Fullscreen**- en **Nieuw tabblad**-knop.
4. Genereer per klant `03-designs/localize-images.sh` (download de AI-foto's → WebP, vervang
   de CDN-links) en `03-designs/caddy-snippet.txt` (Caddy-blokje voor dit subdomein).
5. **Zet de kiesdemo live** (zie FASE 4a): alle 10 onder `klantnaam.demo.brabantdigital.nl`.
6. **STOP — de klant/Pro4Never kiest de top 3** in de live demo (Fullscreen werkt het best).

## FASE 3 — Bouw de top 3 volledig

Per gekozen design een complete site in `04-websites/site-A|B|C/`:

- **Pagina's:** Home, Diensten + prijzen, Over ons, Foto's, Contact (+ Boeken).
- **Taal:** Nederlands standaard, taalknop NL/EN rechtsboven (simpele JS-toggle, geen plugins).
- **Boeken:** Cal.com-widget ingebouwd (zie TOOLS.md → Boeken). In de demo een werkend
  voorbeeld; bij verkoop koppelt de klant in 5 min zijn eigen Google/Apple-agenda.
- **SEO ingebakken:** unieke title + meta description per pagina, schema.org LocalBusiness
  (adres, openingstijden, reviews), sitemap.xml, robots.txt, alt-teksten, nette URL's.
- **Standaard-extra's:** WhatsApp-knop, Google Maps embed, klikbaar telefoonnummer,
  contactformulier (Web3Forms, gratis), responsive, snelle laadtijd (geoptimaliseerde foto's).
- **Techniek:** statische HTML/CSS/JS. Geen build-stap, geen database, geen abonnementen.

## FASE 4 — Live zetten op de VPS (Caddy)

Stack = **Caddy** (HTTPS automatisch), VPS-IP **93.190.187.213**, wildcard `*.demo` staat al.
Zie `VPS-SETUP.md`. Claude levert de commando's + Caddy-blokken altijd kant-en-klaar aan.
Vergeet na élke Windows-upload niet: `sudo chmod -R a+rX /var/www/demos`.

### FASE 4a — Kiesdemo live (alle 10 designs, 1 subdomein) — gebeurt al in fase 2

```bash
# (optioneel maar aanrader, op je PC in 03-designs/) foto's lokaal + WebP:
./localize-images.sh
# uploaden:
rsync -av "03-designs/" root@93.190.187.213:/var/www/demos/KLANT/
```
Op de VPS: `sudo chmod -R a+rX /var/www/demos/KLANT` + dit Caddy-blokje + `sudo systemctl reload caddy`:
```
KLANT.demo.brabantdigital.nl {
    root * /var/www/demos/KLANT
    file_server
    encode gzip
}
```
→ **https://KLANT.demo.brabantdigital.nl** toont alle 10 designs.

### FASE 4b — Top-3 volledige sites live (na keuze + fase 3)

```bash
rsync -av "04-websites/site-A/" root@93.190.187.213:/var/www/demos/KLANT-a/
rsync -av "04-websites/site-B/" root@93.190.187.213:/var/www/demos/KLANT-b/
rsync -av "04-websites/site-C/" root@93.190.187.213:/var/www/demos/KLANT-c/
```
+ `chmod -R a+rX`, 3 Caddy-blokjes (`KLANT-a/-b/-c.demo.brabantdigital.nl`), `reload caddy`.
Noteer alle URL's in `STATUS.md`.

## FASE 5 — Pitch

`05-offerte/pitch.md` bevat:

1. Wat hun huidige site mist (uit `gemist.md`, in klantentaal, geen techniek).
2. De demo-links: de kiesdemo (alle 10) en/of de 3 uitgebouwde sites.
3. Aanbod: eenmalige bouwprijs + **upsell**: hosting, onderhoud, 24/7 hulp (maandbedrag).
4. "Live boekingssysteem: klanten boeken zelf, verschijnt direct in uw telefoonagenda."

## FASE 6 — Uitkomst

- **Verkocht** → site live op klantdomein, boekingssysteem koppelen, upsell activeren.
- **Afgewezen** → demo's van VPS verwijderen:
  ```bash
  sudo rm -rf /var/www/demos/KLANT /var/www/demos/KLANT-*
  # + de Caddy-blokjes weghalen, daarna:
  sudo systemctl reload caddy
  ```
  **Klantmap blijft bestaan.** Zet status op "afgewezen + datum" in STATUS.md.

---

## Over de "YouTube multi-AI-tool workflows"

Die ketens (ChatGPT → Midjourney → Framer → Zapier → ...) bestaan omdat elk los tool maar één
ding kan. Hier is dat niet nodig: Claude in Cowork doet scrapen, analyseren, ontwerpen, bouwen
en (via jouw VPS) publiceren in één omgeving, en je hebt al een AI-beeldgenerator gekoppeld.
Minder tools = minder abonnementen, minder foutpunten, en alles blijft in de klantmap.
Het enige "externe" in de keten: jouw VPS (hosting) en Cal.com (agenda). Dat is de hele stack.
