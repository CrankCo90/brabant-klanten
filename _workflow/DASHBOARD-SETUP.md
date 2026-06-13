# DASHBOARD — eenmalige setup (admin-login)

> Het dashboard draait op **https://admin.demo.brabantdigital.nl** (valt onder je bestaande
> `*.demo`-wildcard → geen nieuwe DNS nodig), achter een admin-login. De auto-deploy
> synchroniseert de bestanden naar `/var/www/admin`. De login regel je één keer hieronder.

## 1. Wachtwoord-hash maken (op de VPS)
```bash
caddy hash-password --plaintext 'KIES-EEN-WACHTWOORD'
```
Kopieer de hash (begint met `$2a$...`).

## 2. Caddy-blok toevoegen (`sudo nano /etc/caddy/Caddyfile`)
```
admin.demo.brabantdigital.nl {
    root * /var/www/admin
    file_server
    encode gzip
    basic_auth {
        leroy PLAK-HIER-DE-HASH
    }
}
```
> Geeft `caddy validate` een fout op `basic_auth`? Dan draai je een oudere Caddy: gebruik dan
> `basicauth` (zonder underscore).

## 3. Eerste publicatie + herladen
```bash
mkdir -p /var/www/admin
rsync -a /root/klanten/dashboard/ /var/www/admin/ && chmod -R a+rX /var/www/admin
sudo systemctl reload caddy
```

## 4. Inloggen
Open **https://admin.demo.brabantdigital.nl** → gebruikersnaam `leroy` + je wachtwoord.

Daarna houdt de 15-min auto-deploy het dashboard vanzelf up-to-date. De klantgegevens staan
in `dashboard/clients.json` (door Claude bijgehouden); nieuwe klanten meld je toe via het
formulier onderaan het dashboard.
