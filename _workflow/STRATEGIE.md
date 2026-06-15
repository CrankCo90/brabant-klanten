# STRATEGIE & AFSPRAKEN — Brabant Digital (werkdocument)
> Centrale plek voor alle gemaakte afspraken + mijn voorstellen. Laatst bijgewerkt: 2026-06-13.

## 1. Aanbod & prijs (VAST)
- **€199 EENMALIG.** Daarna géén maandelijkse of verplichte kosten — de klant zit nergens aan vast.
- Inbegrepen: gekozen ontwerp volledig afgemaakt, alle gewenste functies (voor/na-slider,
  prijsindicatie, keuzehulp, online boeken), NL/EN, SEO, eigen foto's verwerkt, live zetten.
- **Conversie-conditie (lage inzet):** 1 maand gratis KLEINE aanpassingen na oplevering
  (tekst/foto's). Bewust "klein" gehouden om onze tijd te beperken; verlaagt de drempel sterk.
- Normaal €499; €199 = lanceringskorting in ruil voor een eerlijke review.

## 2. Hosting (OPTIONEEL — losse service)
- Hosting is 100% optioneel en NIET verplicht bij de €199.
- Pakket: hosting + onderhoud + updates + aanspreekpunt (richtprijs €19/mnd).
- **12 maanden vooruit = 25% korting.**
- Geen hosting? Wij leveren de bestanden; klant host zelf (of wij helpen eenmalig uploaden).

## 3. Infrastructuur — AANBEVELING: alles op één VPS, git-gedreven
- **Demo's:** /var/www/demos/<klant> → <klant>.demo.brabantdigital.nl (al live, auto-deploy).
- **Productie (betalende klanten):** /var/www/sites/<klant> → eigen domein van de klant.
  Klant wijzigt 1 DNS A-record naar onze VPS-IP; Caddy regelt HTTPS automatisch.
- **Bron = GitHub-repo**; Cowork/Claude Code bewerkt + pusht; VPS pullt (cron) en publiceert.
  Navigeren tussen klanten = mappen in één repo. Eén Caddyfile, één /var/www-boom.
- Statische sites wegen niets → één kleine VPS host honderden klanten. Pas opschalen
  (grotere of 2e VPS achter dezelfde git-workflow) als het echt nodig is.
- **Afgeraden: VPS per klant** — duur en onbeheersbaar, geen voordeel bij statische sites.
- **Alternatief/overloop:** Cloudflare Pages (gratis, wereldwijde CDN) per klant — handig als
  back-up of als de VPS ooit vol/traag raakt. Zelfde git-workflow.

## 4. Dashboard (PLAN)
- **admin.brabantdigital.nl**, achter admin-login (Caddy basicauth) — klanten kunnen er niet bij.
- Toont elke klant/demo + status, gegroepeerd per **niche** en per **werkdag**, met visuele
  statistieken (Chart.js): benaderd / gekocht (ja) / afgewezen (nee) / conversie per niche.
- Databron: `clients.json` in de repo (door Claude bijgehouden). Statisch + git-gedreven.
- **Zelf klanten toevoegen:** een formulier (Web3Forms) meldt een nieuwe klant/website aan →
  komt binnen → Claude verwerkt het in clients.json en gaat ermee aan de slag.
- **Ja/nee bijhouden:** in clients.json. (Semi-)automatisch later mogelijk: inkomende mail
  (IMAP) scannen op "ja"/"nee"/betaling en de status automatisch updaten — fase 2.

## 5. Prospect-proces (per werkdag/niche)
1. Kies 1 niche + 1 regio (bv. hondentrimsalons in Noord-Brabant).
2. Zoek 20-30 bedrijven.
3. Scan elk: website (bestaat/kwaliteit/mobiel/snelheid), foto's, social media,
   Google-vindbaarheid + reviews, en **fulltime-signaal** (openingsdagen/uren — 1-2 dagen/week
   = waarschijnlijk bijbaan → lagere koopkans).
4. **Rank** met onderstaande rubric.
5. Benader alleen de prospects met een ZWAKKE webaanwezigheid én voldoende fulltime-signaal.
   Bedrijven met al een goede, goed vindbare site → NIET benaderen.
6. Bouw per gekozen prospect een demo + persoonlijke mail (compliment + gratis tip +
   verbeteringen) en zet status op "klaar".
7. VPS publiceert (15 min) + mailt (dagcap).

### Rank-rubric (1 = slecht … 5 = top)
| Factor | 1 | 5 |
|---|---|---|
| Website aanwezig & kwaliteit | geen site | strakke, moderne site |
| Mobiel & snelheid | slecht | snel/responsive |
| Foto-kwaliteit | geen/slecht | professioneel |
| Social media | inactief | actief & sterk |
| Google-vindbaarheid + reviews | onvindbaar | top + veel reviews |
| Fulltime-signaal | 1-2 dagen/week | volle week open |
**Beslisregel:** lage score op web/vindbaarheid + hoog fulltime-signaal = beste prospect.
Hoge webscore = niet benaderen.

## 6. Onboarding na "JA" (PLAN)
- Direct: betaalbevestiging/welkomstmail + link naar **onboardingformulier** op de site.
- Onboardingformulier (Web3Forms): domeinnaam · "wil je dat wij hosten?" (ja/nee) · gewenst
  ontwerp · logo/foto's · openingstijden · prijzen · agenda-mail (voor boekingen) · bijzonderheden.
- **Hostingkeuze (lost de "100 providers"-vraag op):**
  - *Wij hosten (aanbevolen):* klant wijzigt alleen 1 DNS-record (of geeft tijdelijk DNS-toegang).
    Geen 100 hostingpanelen nodig — alles op onze VPS.
  - *Eigen hosting:* dan hebben we hun hosting-/FTP-login nodig → via het formulier verzamelen.
- **Logins/secrets:** altijd VEILIG bewaren (wachtwoordmanager), NOOIT in git of de chat.

## 7. Vaste feiten (samenvatting)
- Stack: statische HTML/CSS/JS, Caddy, VPS 93.190.187.213, demo's onder *.demo.brabantdigital.nl.
- Auto-deploy: GitHub-repo CrankCo90/brabant-klanten → VPS-cron elke 15 min.
- Outreach: e-mail via aanbod@brabantdigital.nl (SMTP), autonoom met dagcap + dedupe + afmeldregel,
  alleen na demo. Warme, persoonlijke mail (outreach/template-nl.txt). WhatsApp niet automatisch.
- Merk/contact: Brabant Digital · aanbod@brabantdigital.nl · 085-0608491.

## Openstaande beslissingen
- [ ] Infrastructuur bevestigen (1 VPS, git-gedreven = aanbeveling).
- [ ] Dashboard nu bouwen, of na de eerste prospect-ronde.
- [ ] Onboarding-hostingdefault (wij hosten vs eigen hosting vs beide aanbieden).
