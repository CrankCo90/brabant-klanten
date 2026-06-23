# Apple Shortcut — afwijzing op WhatsApp/SMS automatisch verwerken

> Doel: deel je een afwijzings-bericht naar deze Shortcut, dan zet de server de klant op
> **afgewezen**, haalt de **demo offline** en logt de reactie. Werkt op iPhone 6s (iOS 15).

## Wat het wel/niet doet
- **Wel:** één deel-actie + (kort) het afzendernummer → afwijzing volledig verwerkt.
- **Niet (kan niet op iPhone):** automatisch meelezen zonder dat jij iets deelt.
- Sneller en zonder typen: de rode **“Afwijzing ontvangen”-knop** in `/admin/wa.html` doet hetzelfde.

## Eénmalig: je controle-token ophalen
**VPS-terminal:**
```
cat /root/outreach-data/.control-token
```
Kopieer de uitvoer; die plak je straks in de Shortcut.

## De Shortcut bouwen (Opdrachten-app) — SIMPELE versie (4 acties)
> Tip: je hoeft de actie **“Tekst ophalen uit invoer” NIET** te gebruiken. Je verwijst gewoon
> rechtstreeks naar de variabele **“Opdrachtinvoer”** (Shortcut Input) — dat ís de gedeelde tekst.
> Elke actie vind je door onderaan in de **zoekbalk** de naam te typen.

1. Nieuwe opdracht → naam **Afwijzing verwerken**.
2. Tik op het **ⓘ (info)** onderaan → **“Weergeven in deelmenu”** AAN → invoertype alleen **Tekst**.
3. Acties toevoegen, in volgorde:
   - **Vraag om invoer** — Vraag: `Nummer van de klant (06… of +31…)`, type **Tekst**.
   - **Woordenlijst** (Dictionary), 3 sleutels:
     - `text`  → waarde: variabele **Opdrachtinvoer** (Shortcut Input)
     - `sender` → waarde: variabele **Opgegeven invoer** (uit “Vraag om invoer”)
     - `channel` → waarde: `whatsapp`
   - **Inhoud van URL ophalen** (Get Contents of URL):
     - URL: `https://brabantdigital.nl/api/incoming`
     - Methode: **POST**
     - Koppen: `Authorization` = `Bearer JOUW_TOKEN` · `Content-Type` = `application/json`
     - Aanvraagtekst: **JSON** → kies de **Woordenlijst** van hierboven.
   - **Toon resultaat** (Show Result) → inhoud = **Inhoud van URL ophalen**.
4. Bewaren.

### Een variabele invoegen (belangrijk)
Tik in een waardeveld (bv. bij `text`) → er verschijnt boven het toetsenbord een balk met
**variabelen**. Kies daar **Opdrachtinvoer** (Shortcut Input) of **Opgegeven invoer**.

## Gebruiken
1. Lees de afwijzing in WhatsApp of Berichten.
2. Selecteer/houd het bericht ingedrukt → **Deel** → kies **Afwijzing verwerken**.
3. Typ/plak het afzendernummer → klaar. De server:
   - “nee / geen interesse / stop / graag niet / …” → **afgewezen + demo offline + push**;
   - “ja / graag / afspraak / …” → gelogd als positieve reactie (geen statuswijziging);
   - twijfel → gelogd als “reactie”.

## Belangrijk
- Nummer hoeft niet exact: de server vergelijkt de **laatste 9 cijfers** (+31/06/spaties maakt niet uit).
- Werkt alleen voor klanten die met dat **mobiele nummer** in het systeem staan.
- Token is geheim — deel de Shortcut niet met het token erin.
