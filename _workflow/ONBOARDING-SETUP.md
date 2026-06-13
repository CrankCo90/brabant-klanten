# ONBOARDING — formulier op brabantdigital.nl/welkom

> Na een "ja"/betaling stuur je de welkomstmail (`onboarding/welkomstmail.txt`) met de link
> naar het onboardingformulier. De klant vult daar alles in → komt binnen op
> aanbod@brabantdigital.nl → Claude gaat bouwen. Geen wachtwoorden via het formulier
> (bij eigen hosting nemen we daarna persoonlijk + veilig contact op).

## Caddyfile — /welkom toevoegen
Je `brabantdigital.nl`-blok krijgt er één `handle_path` bij (naast /admin):
```
brabantdigital.nl {
    handle_path /admin* {
        root * /var/www/admin
        file_server
        encode gzip
    }
    handle_path /welkom* {
        root * /var/www/onboarding
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

## Publiceren + herladen
```bash
cd /root/klanten && git pull
rsync -a /root/klanten/onboarding/ /var/www/onboarding/ --exclude '*.txt' && chmod -R a+rX /var/www/onboarding
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl reload caddy
```
Daarna live op **https://brabantdigital.nl/welkom**. (De cron houdt het hierna vanzelf bij.)

## Logins van klanten (eigen hosting)
Verzamel NOOIT wachtwoorden via het formulier. Bij "eigen hosting" neem je persoonlijk contact
op en deel je gegevens via een wachtwoordmanager of versleuteld — nooit in git of de chat.
