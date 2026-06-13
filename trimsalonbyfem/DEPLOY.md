# DEPLOY — trimsalonbyfem demo's live zetten

## 1. Upload (vanaf je PC, in PowerShell/Git Bash, vanuit deze map)

```bash
rsync -av "04-websites/site-A/" root@93.190.187.213:/var/www/demos/trimsalonbyfem-a/
rsync -av "04-websites/site-B/" root@93.190.187.213:/var/www/demos/trimsalonbyfem-b/
rsync -av "04-websites/site-C/" root@93.190.187.213:/var/www/demos/trimsalonbyfem-c/
```

(Geen rsync? WinSCP: sleep de drie site-mappen naar `/var/www/demos/` en hernoem ze
naar trimsalonbyfem-a / -b / -c.)

## 1b. Leesrechten fixen (op de VPS, na élke upload vanaf Windows!)

```bash
sudo chmod -R a+rX /var/www/demos
```

Windows-scp zet mappen op privé (700) waardoor Caddy ze niet mag lezen → "404".

## 2. Caddyfile aanvullen (op de VPS: `sudo nano /etc/caddy/Caddyfile`)

```
trimsalonbyfem-a.demo.brabantdigital.nl {
    root * /var/www/demos/trimsalonbyfem-a
    file_server
}
trimsalonbyfem-b.demo.brabantdigital.nl {
    root * /var/www/demos/trimsalonbyfem-b
    file_server
}
trimsalonbyfem-c.demo.brabantdigital.nl {
    root * /var/www/demos/trimsalonbyfem-c
    file_server
}
```

Daarna: `sudo systemctl reload caddy`

## 3. Demo-links voor de pitch

- https://trimsalonbyfem-a.demo.brabantdigital.nl — Champagne & Charcoal (donker/goud)
- https://trimsalonbyfem-b.demo.brabantdigital.nl — Blush & Velvet (oudroze/elegant)
- https://trimsalonbyfem-c.demo.brabantdigital.nl — Editorial Wit (minimal/galerij)

## Bij verkoop nog activeren (5 min werk)

1. **Cal.com:** gratis account voor Femke aanmaken, agenda koppelen, embed-code plakken op de
   plek van de placeholder in `contact.html` (sectie `#boeken`).
2. **Web3Forms:** gratis access key aanmaken op web3forms.com en invullen in `contact.html`
   (regel met `DEMO-KEY-VERVANGEN-BIJ-OPLEVERING`).
3. **Foto's lokaal zetten:** nu hotlinken ze van het JouwWeb-CDN van de oude site — vóór de
   oude site opgezegd wordt de foto's downloaden naar /img/ en de URL's vervangen.
