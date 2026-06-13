# VPS-SETUP — brabantdigital.nl

> Status: domein gekocht (Vimexx), DNS staat goed, Caddy geïnstalleerd.
> VPS-IP: **93.190.187.213** · Demo's: `klantnaam.demo.brabantdigital.nl`

## ✅ Al gedaan

- [x] Domein: brabantdigital.nl (Vimexx)
- [x] DNS: `*.demo` A-record → 93.190.187.213 (TTL 24h)
- [x] Caddy geïnstalleerd

## Stap A — Inloggen op de VPS (vanaf je eigen PC)

```
ssh root@93.190.187.213
```

(of jouw gebruikersnaam i.p.v. root — alle commando's hieronder voer je IN die SSH-sessie uit)

## Stap B — Demomap fixen (er staat nu per ongeluk "demos0")

```bash
sudo rm -rf /var/www/demos0
sudo mkdir -p /var/www/demos
```

## Stap C — Caddyfile instellen (= "Stap 2")

```bash
sudo nano /etc/caddy/Caddyfile
```

Verwijder alles wat erin staat en plak dit (testsite om de setup te bewijzen):

```
test.demo.brabantdigital.nl {
    root * /var/www/demos/test
    file_server
}
```

Opslaan: `Ctrl+O`, Enter, `Ctrl+X`.

> Per nieuwe klantdemo komt er straks zo'n blokje van 3 regels bij (Claude levert die
> kant-en-klaar aan bij fase 4 van de workflow). Geen wildcard-certificaat nodig —
> Caddy regelt per subdomein automatisch gratis HTTPS.

## Stap D — Testpagina + herladen

```bash
sudo mkdir -p /var/www/demos/test
echo '<h1>Brabant Digital werkt!</h1>' | sudo tee /var/www/demos/test/index.html
sudo systemctl reload caddy
```

Open nu in je browser: **https://test.demo.brabantdigital.nl**
(Eerste keer kan 1–2 min duren: Caddy haalt het HTTPS-certificaat op. Net DNS aangepast?
Dan kan het tot een uur duren voor het record overal bekend is.)

## Demo publiceren (per klant, vanaf je eigen PC)

```bash
rsync -av "04-websites/site-A/" root@93.190.187.213:/var/www/demos/trimsalonbyfem-a/
```

Plus het 3-regel blokje in de Caddyfile + `sudo systemctl reload caddy`.
→ Live op `https://trimsalonbyfem-a.demo.brabantdigital.nl`
(Windows zonder rsync: WinSCP-slepen naar /var/www/demos/ werkt ook.)

## Demo verwijderen (klant wijst af)

```bash
sudo rm -rf /var/www/demos/trimsalonbyfem-a
# + blokje uit /etc/caddy/Caddyfile halen, daarna:
sudo systemctl reload caddy
```

Klantmap op je PC blijft bestaan.

## Problemen?

```bash
sudo systemctl status caddy      # draait Caddy?
sudo journalctl -u caddy -n 50   # laatste logregels (certificaat-fouten zie je hier)
```

## Later (optioneel) — Cal.com self-hosten

Pas bij meerdere betalende klanten: Docker + ~2 GB RAM → `boeken.brabantdigital.nl`,
eigen merk-boekingssysteem, gratis. Tot die tijd: gratis hosted cal.com-accounts.
