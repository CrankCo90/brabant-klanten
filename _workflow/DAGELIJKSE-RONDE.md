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
- Bepaal LAND/TAAL van de regio: Noord-Brabant/NL → land "NL", taal "nl" (Nederlands). Een buitenlandse regio (bv. een Amerikaanse stad) → land "US" (of landcode), taal "en" (Engels). ALLE outreach-teksten EN de demo komen in de taal van de klant.

## 2. Vind ~20-30 bedrijven (WebSearch) in die niche+regio. Verzamel: naam, plaats, website/social, telefoon, e-mail.

## 3. Scan + rank (WebFetch per site)
- Per bedrijf: heeft het een (goede) website? mobiel? online boeken/contact? SEO? verouderd?
  concrete fouten/bugs? fulltime of bijbaan?
- Sla bedrijven met een al sterke, moderne, goed vindbare site over; ook duidelijke bijbanen.
- Kies de ~20 met de ZWAKSTE webaanwezigheid (geen/slechte site) én die serieus/fulltime lijken.

## 4. Bouw de demo's (gebruik de bestaande generator)
Per gekozen prospect:
- Voeg toe aan `_workflow/salons-batch1.json`: {"bedrijf","kort","slug","plaats","tel_display","tel_href","taal"}  (taal "nl" of "en"; tel_display in die taal)
  (slug = kleine letters + koppeltekens; tel_href "tel:+31..." of "#contact").
- Vul `"content"` als je het op hun site vond: {eigenaar, verhaal, specialisaties, certificering, tarieven, openingstijden, reviews}.
- Voeg toe aan `dashboard/clients.json`: {bedrijf, niche, regio, plaats, status:"demo", score (1-5),
  werkdag (vandaag YYYY-MM-DD), demo_url:"https://<slug>.demo.brabantdigital.nl", waarom, fouten:[gevonden punten], contact,
  telefoon (het mobiele/WhatsApp-nummer van het bedrijf, bv. "06-12345678" — zoek dit ACTIEF op, want het is cruciaal voor WhatsApp-benadering; null als echt niet te vinden),
  land ("NL" of bv. "US"), taal ("nl" of "en"), bron (de ORIGINELE website-URL, of null), social (link naar hun Facebook/Instagram, of null), wa_tekst (kort, persoonlijk WhatsApp-appje van 1-2 zinnen + de demo-link, vooral voor prospects mét telefoon zonder e-mail, of null)}.
  → bron/social zijn belangrijk: in het dashboard kan ik daarmee met één klik de bronpagina terugzien.
- Voeg toe aan `_workflow/outreach/prospects.json`: {bedrijf, aanhef, plaats, email (indien gevonden, anders ""),
  status: "klaar" als e-mail gevonden anders "concept", demo_url, deadline:"", onderwerp, compliment, gratis_tip, verbeteringen}.
  Schrijf ALLE teksten (aanhef, compliment, gratis_tip, verbeteringen, onderwerp, wa_tekst) in de TAAL VAN DE KLANT — Nederlands voor NL, Engels voor een Amerikaanse/buitenlandse klant. WARM, PERSOONLIJK en KORT — geen verkooppraat.
  • aanhef: NL "Hoi <voornaam>," / EN "Hi <firstname>," als je de eigenaar kent, anders "Hoi,"/"Hi,". Nooit "Geachte"/"Dear Sir".
  • onderwerp: rustig en concreet, bv. "Ik heb alvast een website voor <bedrijf> gemaakt (kijk even mee)". Geen "GRATIS", geen uitroeptekens, geen "aanbieding".
  • compliment: 2 zinnen die OPRECHT en SPECIFIEK over HÉN gaan — iets echt dat je zag (hun werk/foto's/reviews) + een zachte constatering dat ze een goede plek online verdienen. GEEN opsomming van wat er mis is, GEEN algemene verkoopzin.
  • gratis_tip: één ECHT bruikbare, concrete tip die ze zélf meteen kunnen toepassen (bv. Google-bedrijfsprofiel claimen, klikbaar nummer in de bio, één duidelijke 'Afspraak maken'-knop). Het is een cadeautje, NIET een herhaling van hun fout.
  • verbeteringen: 3 concrete voordelen, gelokaliseerd op plaats/niche (online boeken, vindbaar in Google op "<niche> <plaats>", foto's+reviews netjes op de telefoon). Hou het bij 3.
Demo-taal: zet `taal` in de salons-batch1-entry. NL → Nederlandse demo met NL/EN-knop. Buitenland → demo standaard in het Engels (de generator zet `<html lang>` en toont Engels); tweede taal-knop wordt later Spaans (de bilinguale teksten staan al klaar). Schrijf de content (verhaal/tarieven/reviews) in de taal van de klant.
Draai daarna: `python3 _workflow/generate-demo.py`

## 5. Vastleggen + publiceren (NIET mailen)
- Voeg 1 regel toe aan `_workflow/gedaan-niches.txt`: "<datum> · <niche> · <regio> · <aantal>".
- Commit + push: `bash _workflow/push.sh "Ochtendronde <niche> <regio>"`
- Publiceer live: `bash _workflow/vps-autodeploy.sh`
- Schrijf een korte samenvatting naar `_workflow/logs/DAGELIJKS-<datum>.md` (gekozen niche/regio + onderbouwing, aantal prospects, hoeveel met e-mail, opvallende vondsten).

## REGELS
- Verstuur GEEN e-mail. Mails blijven op "klaar"/"concept"; Pro4Never verstuurt via het dashboard.
- Maximaal ~20 prospects per ronde. Alleen B2B/lokale ondernemers. Geen al-goede sites benaderen.
