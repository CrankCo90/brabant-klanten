# Apple Shortcut — afwijzing op WhatsApp/SMS automatisch verwerken

> Doel: als een prospect via WhatsApp of SMS afwijst, deel je dat bericht naar een Shortcut.
> De server herkent automatisch of het een "nee" is, zet de klant op **afgewezen**, haalt de
> **demo offline** en logt de reactie. Werkt op je iPhone (ook iOS 15 / iPhone 6s).

## Wat het wel/niet doet
- **Wel:** met één deel-actie + (kort) het afzendernummer wordt de afwijzing volledig verwerkt.
- **Niet (kan technisch niet op iPhone):** automatisch meelezen zónder dat jij iets deelt. iOS geeft
  een app/Shortcut geen toegang tot binnenkomende berichten of de afzender. Daarom: jij deelt het bericht.
- De rode **"Afwijzing ontvangen"-knop** in de WhatsApp-lijst (`/admin/wa.html`) doet exact hetzelfde
  zónder typen — gebruik die als je toch al in de lijst zit.

## Eénmalig: je controle-token ophalen
Het token is geheim en zit op de VPS. Print het en kopieer het (je plakt het straks in de Shortcut):

**VPS-terminal:**
```
cat /root/outreach-data/.control-token
```

## De Shortcut bouwen (Opdrachten-app)
1. Open **Opdrachten** → **+** (nieuwe opdracht) → naam: *Afwijzing verwerken*.
2. Tik op het **info-icoon (ⓘ)** onderaan → zet **"Weergeven in deelmenu"** AAN → bij "Soort deelmenu-invoer" alleen **Tekst** aanvinken.
3. Voeg deze acties toe, in deze volgorde:
   - **"Tekst ophalen uit invoer"** (Get text from Input) → invoer = *Opdrachtinvoer (deelmenu)*. Hiermee komt de berichttekst binnen.
   - **"Vraag om invoer"** (Ask for Input) → Vraag: `Nummer van afzender (06… of +31…)`, type **Getal/Tekst**. (Tip: kopieer het nummer eerst uit de chat, dan kun je plakken.)
   - **"Woordenlijst"** (Dictionary) met drie sleutels:
     - `text`  → waarde: *Tekst ophalen uit invoer* (de berichttekst)
     - `sender` → waarde: *Opgegeven invoer* (het nummer uit de vorige stap)
     - `channel` → waarde: `whatsapp`  (of `sms`)
   - **"Inhoud van URL ophalen"** (Get Contents of URL):
     - URL: `https://brabantdigital.nl/api/incoming`
     - Methode: **POST**
     - Koppen (Headers):
       - `Authorization` = `Bearer JOUW_TOKEN_HIER`  ← plak hier het token uit de VPS-stap
       - `Content-Type` = `application/json`
     - Aanvraagtekst (Request Body): **JSON** → kies *Woordenlijst* (de Dictionary van hierboven).
   - **"Toon meldingstekst"** (Show Notification) of **"Snel kijken"** (Quick Look) → inhoud = *Inhoud van URL ophalen* (dan zie je wat er is gebeurd, bv. "… op 'afgewezen' gezet en demo offline gehaald").
4. Klaar. Bewaren.

## Gebruiken
1. Lees de afwijzing in WhatsApp of Berichten.
2. Houd het bericht ingedrukt → **Deel** (of selecteer de tekst → Deel) → kies **Afwijzing verwerken**.
3. Plak/typ het afzendernummer → klaar. De server:
   - herkent "nee / geen interesse / stop / graag niet / …" → **afgewezen + demo offline + commit/push**;
   - herkent "ja / graag / afspraak / …" → logt het als positieve reactie (geen status­wijziging);
   - twijfel → logt het als "reactie" zodat je het terugziet.
4. Geen match op het nummer? Dan meldt de Shortcut dat, en verandert er niets (controleer het nummer).

## Belangrijk
- Het nummer hoeft niet exact te matchen op +31/06/spaties — de server vergelijkt de laatste 9 cijfers.
- Werkt alleen voor klanten die met dat **mobiele nummer** in het systeem staan.
- Het token is geheim: deel de Shortcut niet met het token erin.
