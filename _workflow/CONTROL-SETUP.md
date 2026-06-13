# DASHBOARD-BESTURING — eenmalige VPS-setup

> Hiermee kan het dashboard (brabantdigital.nl/admin) acties op de VPS starten:
> outreach versturen (prospects aanvinken + dagcap), demo's publiceren, autopilot aan/uit,
> en een vrije Claude-opdracht. Een kleine control-server draait lokaal (127.0.0.1:8787),
> Caddy proxyt `/api/*` ernaartoe, en alles is beveiligd met een geheim token + je admin-login.

## 1. Token aanmaken
```bash
openssl rand -hex 24 > /root/outreach-data/.control-token
chmod 600 /root/outreach-data/.control-token
cat /root/outreach-data/.control-token    # kopieer deze; plak 'm één keer in het dashboard
```

## 2. Control-server als service (systemd)
```bash
sudo tee /etc/systemd/system/bd-control.service >/dev/null <<'UNIT'
[Unit]
Description=Brabant Digital control-server
After=network.target
[Service]
ExecStart=/usr/bin/python3 /root/klanten/_workflow/control-server.py
WorkingDirectory=/root/klanten
Restart=always
User=root
[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload && sudo systemctl enable --now bd-control
sudo systemctl status bd-control --no-pager | head -5
```

## 3. Caddy: /api doorsturen (in het brabantdigital.nl-blok, BOVEN de andere handles)
```
brabantdigital.nl {
    handle /api/* {
        reverse_proxy 127.0.0.1:8787
    }
    handle_path /admin* { root * /var/www/admin
        file_server
        encode gzip
    }
    handle_path /welkom* { root * /var/www/onboarding
        file_server
        encode gzip
    }
    handle { root * /var/www/brabantdigital
        file_server
        encode gzip
    }
}
```
Daarna: `sudo systemctl reload caddy`

## 4. Autopilot-cron (respecteert de aan/uit-knop uit het dashboard)
```bash
( crontab -l 2>/dev/null | grep -v send-outreach.py; echo '0 10 * * * [ -f /root/outreach-data/.autopilot_on ] && OUTREACH_DATA=/root/outreach-data OUTREACH_CAP=20 /usr/bin/python3 /root/klanten/_workflow/outreach/send-outreach.py >> /root/outreach-data/send.log 2>&1' ) | crontab -
```
(Autopilot UIT = de cron doet niets; AAN = stuurt dagelijks tot de cap. Handmatig versturen via het dashboard werkt altijd.)

## 5. Automatische reactie-detectie (IMAP)
Voeg je IMAP-gegevens toe aan `/root/outreach-data/.smtp-env`:
```
IMAP_HOST=imap.jouwprovider.nl
IMAP_PORT=993
```
(gebruiker/wachtwoord = dezelfde SMTP_USER/SMTP_PASS). Dan elk uur scannen:
```bash
( crontab -l 2>/dev/null; echo '0 * * * * OUTREACH_DATA=/root/outreach-data /usr/bin/python3 /root/klanten/_workflow/outreach/scan-replies.py >> /root/outreach-data/replies.log 2>&1' ) | crontab -
```
Reacties (ja/nee/afmelden) verschijnen daarna automatisch bij de prospect in het dashboard.

## 6. Gebruik
Open brabantdigital.nl/admin → blok "Acties & autopilot" → plak je token → Verbinden.
Vink prospects aan → "Verstuur outreach" (met bevestiging) → live log verschijnt.

## Beveiliging
- Het eindpunt luistert alleen op 127.0.0.1 (niet direct vanaf internet); Caddy is de enige toegang.
- Elke aanroep vereist het Bearer-token. Token kwijt/gelekt? Genereer een nieuwe (stap 1) + herstart de service.
- De vrije Claude-opdracht draait met de guard-hook actief, dus systeem-vernietigende commando's blijven geblokkeerd.
