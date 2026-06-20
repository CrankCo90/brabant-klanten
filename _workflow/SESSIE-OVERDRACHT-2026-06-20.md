# Sessie-overdracht 2026-06-20 (DONZA TEST-niche + e-mail deliverability)

## 1) DONZA TEST-niche (testopzet — eigen e-mailadressen Pro4Never)
- Nieuwe niche `niche:"donza"` (label **"DONZA TEST"**) als TEST om functionaliteiten te checken — geen echte prospects.
- 9 demo's `donzatest1..9`, bedrijf **"DONZA Test 1".."9"**. Unieke namen zijn VERPLICHT: het dashboard koppelt e-mail via `prospectByName(bedrijf)` (exacte match) → identieke namen botsen.
- Inhoud = exacte kopie van **schilder-premium** (6 designs + cover). `generate-demo.py` schilder-tak draait nu ook voor `niche=="donza"`. In `add-prospects.py` donza-keys toegevoegd (NL-label "DONZA TEST", WORD, TIP, benefits).
- E-mails: secret17@live.nl, secret18@live.nl, admin@stayinfluence.eu, info@donley.eu, lbm1990@me.com, lbm1990@icloud.com, producten@donzahandel.com, yorelb@live.nl, _leroy@live.nl. Telefoons random: 06-46210627 / 06-18162519 / 0850608471.
- **`wa_number`-override** in `gen_premium.py`: expliciet wa_number geeft ook bij vast nummer (085) een WhatsApp-knop; leeg veld = oud gedrag (alleen 06/316).
- Clients score **9** → bovenaan outreach-wachtrij (dashboard sorteert op score).
- Incident: batch/handmatige verzending (NIET de autopilot — stond Ma-Vr en is uit) stuurde 20-06 21:58-21:59 alle 9 testmails uit. Allemaal eigen adressen → geen externe schade. 9 regels uit `/root/outreach-data/sent-log.csv` verwijderd (backup `sent-log.bak`) → weer in wachtrij voor handmatig testen.

## 2) E-mail deliverability (Hotmail/Outlook in spam) — AL UITGEZOCHT, niet herhalen
Geverifieerd 2026-06-20. Authenticatie is in orde:
- Verzending via **mail.zxcs.nl** (465 SSL, user aanbod@brabantdigital.nl), outbound via zxcs `filter-out.zxcs.nl`-pool — NIET direct vanaf VPS-IP. rDNS van de VPS is dus irrelevant voor mail.
- **SPF** pass (`a mx ip4:185.104.29.100 include:filter-out.zxcs.nl ~all`).
- **DKIM** AANWEZIG — zxcs-selector **`x`** (`x._domainkey.brabantdigital.nl`, RSA).
- **DMARC** `p=quarantine; sp=none` — aligned via SPF+DKIM → pass.
- **Conclusie:** spam bij Hotmail/Outlook ligt NIET aan DNS, maar aan (a) gedeelde zxcs-outbound-IP-reputatie bij Microsoft, (b) cold-outreach die SmartScreen filtert, (c) jong domein, (d) geen Microsoft SNDS/JMRP.
- **Volgende keer hierop focussen (niet DNS):** Microsoft SNDS + JMRP registreren + evt. delisting via Outlook sender support; warm-up + laag volume; minder links/spammy patterns; bij schaal dedicated cold-outreach-infra (apart verzenddomein + warmup) i.p.v. shared hosting.
