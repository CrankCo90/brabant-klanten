
## Sessie (Cowork) — 15-06-2026, avond

**Dashboard fixes (live):**
- Mobiel-menu: sidebar sloot niet op telefoon. Toegevoegd: backdrop-overlay (klik = sluiten), sluitknop (✕), en sluit automatisch bij navigatie. (commit b90ebe2)
- Autopilot-instelling (aan/uit + dagcap) was per apparaat verschillend (PC 100/aan, telefoon 20/uit) doordat de UI uit localStorage/defaults las. Nu server-persistent: dashboard laadt aan/uit + cap + start/stop/dagen uit /api/status en slaat élke wijziging op. 3e schakelaar gewired; "Opslaan" wist 'on' niet meer (bug). Overal identiek. (commit 4b6664f)

**Prospects — batch Limburg (hond, 7 nieuw, demo's live):** (commit a6bd4b5)
- Roermond: Trimsalon Melis (FB), Trimsalon Rozely (FB) · Schinveld: Hondentrimsalon Graciël (FB, sinds 2007)
- Simpelveld: Trimsalon Kroes Control (06-17500027 + e-mail + oude site) · Tegelen: Hondenkapper Valuas (06-30706474, ABHB)
- Eygelshoven: Hondentrimsalon Pluto (06-30012720) · Venlo/Blerick: Trimsalon Bonito (06-45558685)
- Elk: 11-design demo + cal.eu-planner, geverifieerd contact (06 of social), zwakke/geen eigen site. Status concept → autopilot pakt ze op.
- Afgewezen na verificatie (contactregel/klantenstop): De Trimfabriek (klantenstop), Meg's Dog Barber (klantenstop), Duchess Heerlen (alleen vaste lijn), Diana Landgraaf (geen verifieerbaar contact).

**Openstaand:** richting 200/niche is meer-sessie-werk (echt 7-staps-onderzoek per prospect; ~tientallen/sessie). Limburg/Zeeland verder uitkammen voor hond, en nagel + pedicure nog starten.
