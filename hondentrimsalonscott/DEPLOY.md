# DEPLOY — Hondentrimsalon Scott: alle 10 designs live

> Nieuwe aanpak: **1 subdomein per klant** dat het overzicht (`index.html`) toont met
> alle 10 designs erin. Scott kiest zelf via Fullscreen/Nieuw tabblad. Geen 10 losse
> subdomeinen nodig. Stack = **Caddy** (HTTPS automatisch), zoals in `_workflow/VPS-SETUP.md`.
>
> Demo-URL straks: **https://hondentrimsalonscott.demo.brabantdigital.nl**

## Wat er live gaat

De hele map `03-designs/` wordt één demo:
```
03-designs/
├── index.html          ← overzicht met de 10 designs (Caddy serveert dit als homepage)
├── previews/           ← design-01..10.html (de werkende mini-pagina's, in iframes)
├── assets/img/         ← lokale WebP-foto's (na stap 0)
└── localize-images.sh  ← maakt die WebP's + vervangt de CDN-links (eenmalig)
```

## Stap 0 (aanrader) — foto's lokaal + licht maken

Nu hotlinken de designs de AI-foto's vanaf een CDN. Voor een snelle, eigen demo zet je ze
lokaal als WebP. **Op je PC** (Git Bash), in de map `03-designs/`:

```bash
./localize-images.sh
```

Dit downloadt de 8 foto's, maakt er WebP van (~2-4 MB totaal) en vervangt de links in de
designs. Geen `cwebp`? → `sudo apt install webp` (VPS) of `choco install webp` (Windows),
of het script pakt automatisch ImageMagick als dat er is.

> Sla deze stap gerust over voor een supersnelle test: met de CDN-links werkt alles ook
> meteen, alleen niet volledig "eigen".

## Stap 1 — Uploaden (op je PC, vanuit de klantmap)

### PowerShell (geen rsync nodig) — aanrader op Windows
```powershell
scp -r "C:\Users\Gebruiker\Desktop\Klanten werven voor nieuwe site\hondentrimsalonscott\03-designs" root@93.190.187.213:/var/www/demos/
```
Daarna op de VPS even hernoemen naar de klantnaam:
```bash
mv /var/www/demos/03-designs /var/www/demos/hondentrimsalonscott
```
(Bestaat hondentrimsalonscott al van een eerdere poging? Eerst `sudo rm -rf /var/www/demos/hondentrimsalonscott`.)

### Git Bash (met rsync) — alternatief
```bash
rsync -av "03-designs/" root@93.190.187.213:/var/www/demos/hondentrimsalonscott/
```

(Geen van beide? WinSCP: sleep de **inhoud** van `03-designs/` naar
`/var/www/demos/hondentrimsalonscott/`.)


## Stap 2 — Leesrechten fixen (op de VPS, na élke upload vanaf Windows!)

```bash
sudo chmod -R a+rX /var/www/demos/hondentrimsalonscott
```

Windows-scp zet mappen op 700 → Caddy kan ze anders niet lezen ("404").

## Stap 3 — Caddyfile aanvullen (op de VPS: `sudo nano /etc/caddy/Caddyfile`)

Plak het blokje uit `03-designs/caddy-snippet.txt`:

```
hondentrimsalonscott.demo.brabantdigital.nl {
    root * /var/www/demos/hondentrimsalonscott
    file_server
    encode gzip
}
```

Daarna:

```bash
sudo systemctl reload caddy
```

(Eerste keer 1-2 min: Caddy haalt automatisch het HTTPS-certificaat op.)

## Stap 4 — Klaar

Open **https://hondentrimsalonscott.demo.brabantdigital.nl** — Scott ziet alle 10 designs
en kan elk fullscreen bekijken. Noteer de link in `STATUS.md` en stuur 'm naar Scott.

## Demo verwijderen (als Scott afwijst)

```bash
sudo rm -rf /var/www/demos/hondentrimsalonscott
# + het Caddy-blokje weghalen, daarna:
sudo systemctl reload caddy
```

De klantmap op je PC blijft bestaan.

## Capaciteit (waarom je CP2 ruim volstaat)

Statische site: code ~21 KB (gzip), foto's ~2-4 MB WebP per klant. Op 20 GB passen
honderden tot duizenden klanten. CPU/RAM zijn geen factor voor statische demo's —
upgraden (SP/CP) pas nodig bij zware dynamische dingen (databases, apps), niet hiervoor.
