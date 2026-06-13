# DASHBOARD — setup (op brabantdigital.nl/admin)

> Het dashboard draait op **https://brabantdigital.nl/admin**, met een eigen luxe inlogpagina
> (geen browser-popup). De auto-deploy synchroniseert de bestanden naar `/var/www/admin`.

## Caddyfile — /admin toevoegen aan je hoofdsite
Vervang je huidige `brabantdigital.nl { ... }`-blok door dit (gebruikt handle_path):
```
brabantdigital.nl {
    handle_path /admin* {
        root * /var/www/admin
        file_server
        encode gzip
    }
    handle {
        root * /var/www/brabantdigital
        file_server
        encode gzip
    }
}
```
Het oude losse `admin.demo.brabantdigital.nl { ... }`-blok mag je verwijderen (of laten staan).

## Publiceren + herladen
```bash
cd /root/klanten && git pull
rsync -a /root/klanten/dashboard/ /var/www/admin/ && chmod -R a+rX /var/www/admin
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl reload caddy
```

## Inloggen
Open **https://brabantdigital.nl/admin** → luxe inlogpagina → wachtwoord invullen.
Wachtwoord wijzigen? Geef het door aan Claude; die wisselt de hash in `dashboard/index.html`.

## Beveiliging (eerlijk)
De inlogpagina is een client-side slot: prima om meekijkers te weren, maar `clients.json` is
technisch op te vragen via de URL. Wil je het écht dichttimmeren, dan kan de data versleuteld
worden (alleen met het wachtwoord te ontsleutelen) of een server-side login erbij — vraag Claude.
