# DAGELIJKSE PROSPECT-RONDE (autonoom — STOPT vóór het mailen)
Je bent Claude Code op de VPS, in /root/klanten. Voer NU de dagelijkse prospect-ronde uit.
Verstuur GEEN enkele e-mail. Wees feitelijk; verzin geen reviews of gegevens.

## 1. Kies de niche via marktonderzoek (Noord-Brabant)
- Lees `_workflow/gedaan-niches.txt` — niches/regio's die er al in staan NIET opnieuw doen.
- Doe kort marktonderzoek (WebSearch) naar lokale ondernemers/zzp'ers in Noord-Brabant die
  (a) een website hard nodig hebben én (b) er statistisch vaak GÉÉN hebben. Denk aan:
  klusbedrijven/handyman, hondentrimsalons, pakket-/afhaalpunten aan huis, hoveniers,
  stukadoors, nagelstudio's/schoonheidsspecialisten aan huis, schoorsteenvegers, etc.
- Kies ÉÉN niche + ÉÉN NB-regio of -stad die nog niet gedaan is en de hoogste website-behoefte heeft.
  Noteer 1-2 zinnen onderbouwing.

## 2. Vind ~20-30 bedrijven (WebSearch) in die niche+regio. Verzamel: naam, plaats, website/social, telefoon, e-mail.

## 3. Scan + rank (WebFetch per site)
- Per bedrijf: heeft het een (goede) website? mobiel? online boeken/contact? SEO? verouderd?
  concrete fouten/bugs? fulltime of bijbaan?
- Sla bedrijven met een al sterke, moderne, goed vindbare site over; ook duidelijke bijbanen.
- Kies de ~20 met de ZWAKSTE webaanwezigheid (geen/slechte site) én die serieus/fulltime lijken.

## 4. Bouw de demo's (gebruik de bestaande generator)
Per gekozen prospect:
- Voeg toe aan `_workflow/salons-batch1.json`: {"bedrijf","kort","slug","plaats","tel_display","tel_href"}
  (slug = kleine letters + koppeltekens; tel_href "tel:+31..." of "#contact").
- Vul `"content"` als je het op hun site vond: {eigenaar, verhaal, specialisaties, certificering, tarieven, openingstijden, reviews}.
- Voeg toe aan `dashboard/clients.json`: {bedrijf, niche, regio, plaats, status:"demo", score (1-5),
  werkdag (vandaag YYYY-MM-DD), demo_url:"https://<slug>.demo.brabantdigital.nl", waarom, fouten:[gevonden punten], contact}.
- Voeg toe aan `_workflow/outreach/prospects.json`: {bedrijf, aanhef:"Hoi <voornaam of leeg>,", plaats,
  email (indien gevonden, anders ""), status: "klaar" als e-mail gevonden anders "concept",
  demo_url, deadline:"", onderwerp, compliment, gratis_tip (de sterkste gevonden fout, natuurlijke zin),
  verbeteringen:[5 punten, gelokaliseerd op plaats/niche]}.
Draai daarna: `python3 _workflow/generate-demo.py`

## 5. Vastleggen + publiceren (NIET mailen)
- Voeg 1 regel toe aan `_workflow/gedaan-niches.txt`: "<datum> · <niche> · <regio> · <aantal>".
- Commit + push: `bash _workflow/push.sh "Ochtendronde <niche> <regio>"`
- Publiceer live: `bash _workflow/vps-autodeploy.sh`
- Schrijf een korte samenvatting naar `_workflow/logs/DAGELIJKS-<datum>.md` (gekozen niche/regio + onderbouwing, aantal prospects, hoeveel met e-mail, opvallende vondsten).

## REGELS
- Verstuur GEEN e-mail. Mails blijven op "klaar"/"concept"; Pro4Never verstuurt via het dashboard.
- Maximaal ~20 prospects per ronde. Alleen B2B/lokale ondernemers. Geen al-goede sites benaderen.
