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

## STATUS: gestopt vóór verzenden — niets verstuurd. Wacht op controle door Pro4Never.

### Openstaand (na review)
- Demo's en mails nakijken in het dashboard (brabantdigital.nl/admin).
- Akkoord → de 9 mails met e-mailadres op `klaar` zetten zodat de VPS ze verstuurt (dagcap).
- Prospects zonder e-mail: benaderen via telefoon/WhatsApp/Facebook.
- Eventueel de demo-content per gekozen salon verder personaliseren.
