# Dagverslag — 13 juni 2026

## Batch 1: hondentrimsalons Noord-Brabant (Den Bosch · Eindhoven · Tilburg · Breda e.o.)

**Gevonden & gescand:** ~40 salons. **Live in browser gecontroleerd** (de JS-sites).

**Resultaat:** 19 echte prospects (status `demo`) + Scott; 20 afgewezen (met reden in dashboard).

**Demo's:** 24 kiesdemo's gegenereerd via `_workflow/generate-demo.py` en live op
`<slug>.demo.brabantdigital.nl` (auto-deploy). Geverifieerd: o.a. peter-rijswijk & spadogs laden correct.
- **Eigen foto's** verwerkt voor 9 salons (bemellow, bonita, peter-rijswijk, wilma, knappe-snuitje,
  dogsalon-mila, van-kop-tot-staart, just4dogs, jokes). Rest: AI-placeholders (geen bruikbare eigen foto's).

**Live-check correcties (afvallers):** Trimsalon Elite, Lynn's, Mooie Hondjes (sites offline),
Hondentrimsalon Oss (klantenstop), Doggroomer Eindhoven (al moderne site met online boeken).

**Persoonlijke mails:** voor alle prospects als **concept** klaargezet (gevonden fouten = gratis tip).
9 hebben een e-mailadres → direct mailbaar na akkoord. Rest: geen e-mail gevonden → telefoon/WhatsApp/FB.

**Nieuw in handelingskader:** gebruik eigen foto's van de prospect in de demo (CLAUDE.md + STRATEGIE.md + generator).

## Batch 2: nagelstudio's Helmond e.o. (Helmond · Geldrop · Mierlo · Gemert)

**Niche-keuze (onderbouwing):** marktonderzoek wees uit dat nagelstudio's/nagelstylisten in Helmond
e.o. een hoge website-behoefte hebben: van de ~25 gecontroleerde studio's had de meerderheid een
zwakke of ontbrekende webaanwezigheid — een grote groep heeft alleen Facebook/Instagram of een
gidsvermelding, anderen draaien op verouderde bouwer-templates of kapotte sites. Online boeken
ontbrak vrijwel overal, terwijl klanten dat in deze branche steeds vaker verwachten. Nagelstudio's
passen bovendien qua structuur (afspraak/behandelingen/tarieven/reviews) goed op ons template.

**Gevonden & gescand:** ~25 studio's (via Treatwell, nagelstudio-info.nl, nagelstudios.nl, Goudengids,
Google + WebFetch per site). **20 prospects** geselecteerd (de zwakste/serieuze); sterke moderne sites
(o.a. La Petite Belge, LaLina, Lika Nail Center) en een avond-only bijbaan (B's BeautySpot) bewust overgeslagen.

**Concrete gevonden gebreken (echt waargenomen):** La Chica Nails draait op een self-signed
SSL-certificaat (beveiligingswaarschuwing); Beauty Point Helmond toont enkel een lege DirectAdmin-placeholder;
Schoonheidssalon Esthetika was bij controle onbereikbaar; Espaço Mão Bella heeft dode 404-links voor
prijs/contact; JAËL gebruikt slechts een kale Google business.site; veel anderen hebben géén eigen site.

**Demo's:** 20 kiesdemo's gegenereerd. De generator is **niche-bewust** gemaakt: per-entry veld
`"niche":"nagels"` past een NL/EN-copymap toe op alle 10 designs (incl. calculator/quiz/before-after-slider)
en gebruikt een **nagelbeeldpool** (geverifieerde Pexels-foto's, rolverdeling clean/salon/before) i.p.v.
de hondenfoto's. De bestaande trimsalon-demo's blijven ongewijzigd (geen niche-veld). Verificatie:
geen trim-/honden-tekst meer in de nagel-demo's (alleen een interne JS-variabele heet nog `coat`).

**E-mail:** 1 prospect heeft een e-mailadres (Nagelstudio Mariëlle, Geldrop) → status `klaar`;
de overige 19 → `concept` (geen e-mail gevonden, wel vaak telefoon/social). **Niets verstuurd.**

**Reviews:** géén reviews overgenomen — de enige gevonden "reviews" waren parafrases zonder echt
citaat (verzin geen reviews), dus leeg gelaten.

## STATUS: gestopt vóór verzenden — niets verstuurd. Wacht op controle door Pro4Never.

### Openstaand (na review)
- Demo's en mails nakijken in het dashboard (brabantdigital.nl/admin).
- Akkoord → de 9 mails met e-mailadres op `klaar` zetten zodat de VPS ze verstuurt (dagcap).
- Prospects zonder e-mail: benaderen via telefoon/WhatsApp/Facebook.
- Eventueel de demo-content per gekozen salon verder personaliseren.
