# DEPLOY — brabantdigital.nl live op de VPS

## 1. DNS aanpassen bij Vimexx (belangrijk: ook de AAAA-records!)

Nu wijzen `@` en `www` naar Vimexx-parking (185.104.28.238 + IPv6). Wijzig in Premium DNS:

| Record | Type | Nieuwe waarde |
|---|---|---|
| `@` | A | **93.190.187.213** |
| `www` | A | **93.190.187.213** |
| `@` | AAAA | **VERWIJDEREN** |
| `www` | AAAA | **VERWIJDEREN** |

> De AAAA-records (IPv6) MOETEN weg: browsers kiezen IPv6 eerst en komen anders nog
> steeds bij Vimexx-parking uit. `mail`, `ftp`, `*.demo` en de TXT-records laat je staan
> (mail blijft dan via Vimexx lopen).

## 2. Upload (op je PC, PowerShell)

```powershell
cd "C:\Users\Gebruiker\Desktop\Klanten werven voor nieuwe site\brabantdigital"
scp -r site root@93.190.187.213:/var/www/brabantdigital
```

## 3. Op de VPS: rechten + Caddy

```bash
sudo chmod -R a+rX /var/www/brabantdigital
sudo nano /etc/caddy/Caddyfile
```

Voeg toe:

```
brabantdigital.nl {
    root * /var/www/brabantdigital
    file_server
}
www.brabantdigital.nl {
    redir https://brabantdigital.nl{uri} permanent
}
```

Daarna: `sudo systemctl reload caddy`
(DNS-wijziging kan tot een uur duren; daarna haalt Caddy automatisch het certificaat.)

## 4. E-mail: aanbod@brabantdigital.nl laten werken

Het domein heeft Vimexx-mailrecords. Twee opties:

- **Vimexx-paneel** → check of er een (gratis) mailbox of doorstuur-optie bij je domein zit → maak `aanbod@` aan en stuur door naar leroyb@home.nl.
- Lukt dat niet: **ImprovMX.com** (gratis doorsturen) — vervang dan de MX-records volgens hun instructie.

> Let op bij het **versturen** vanaf aanbod@: de strenge SPF/DMARC-records (`p=reject`)
> kunnen verzending blokkeren. Versturen via Gmail "Send as" + Vimexx SMTP werkt het netst.

## 5. Nog activeren (placeholders in de site)

1. ~~Belafspraak-agenda~~ ✅ KLAAR — cal.eu inline embed ingebouwd (brabantdigital/intake-gesprek-brabant-digital-met-leroy, donker thema, goudkleur).
2. ~~Contactformulier~~ ✅ KLAAR — Web3Forms-key ingevuld; inzendingen komen binnen op aanbod@brabantdigital.nl.
3. **Portfolio-foto's** hotlinken nu van het JouwWeb-CDN — bij gelegenheid eigen screenshots van de demo's maken en lokaal zetten.
