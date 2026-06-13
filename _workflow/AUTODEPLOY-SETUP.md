# AUTOMATISCH PUBLICEREN — opzet (eenmalig)

> Doel: wij werken in Cowork → ik push de nieuwe versie naar een privé GitHub-repo →
> de VPS haalt elke 15 minuten op en zet automatisch live. Jij hoeft niets te draaien.
>
> De repo leeft op **GitHub + de VPS** (niet in je Desktop-map — die mount ondersteunt git niet).

## Onderdelen
- **Mijn kant (push):** ik gebruik een fijnmazig token om naar de repo te pushen.
- **VPS-kant (pull + publiceren):** een read-only deploy-sleutel + cron die elke 15 min
  `_workflow/vps-autodeploy.sh` draait.

---

## DEEL A — GitHub (jij, eenmalig, ~5 min)

1. **Repo aanmaken:** ga naar https://github.com/new
   - Naam: `brabant-klanten`
   - Zichtbaarheid: **Private**
   - Niets aanvinken (geen README), klik **Create repository**.

2. **Token aanmaken (voor mijn push):**
   - GitHub → rechtsboven je foto → **Settings** → onderaan **Developer settings**
     → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
   - Token name: `cowork-push` · Expiration: bv. 90 dagen (of langer).
   - **Repository access:** *Only select repositories* → kies `brabant-klanten`.
   - **Permissions:** klap *Repository permissions* open → **Contents** → **Read and write**.
   - Klik **Generate token** en **kopieer** de token (begint met `github_pat_...`).
     Je ziet 'm maar één keer.

3. **Plak in deze chat:**
   - de repo-URL (bv. `https://github.com/CrankCo90/brabant-klanten`)
   - de token (`github_pat_...`)

   Dan bewaar ik de token veilig (in `_workflow/.deploy-token`, staat in `.gitignore` →
   wordt nooit meegestuurd) en doe ik de eerste push.

---

## DEEL B — VPS (eenmalig, ik geef je het exacte blok zodra de repo bestaat)

Globaal gebeurt dit (read-only, los van mijn push-token):

```bash
# 1) read-only deploy-sleutel voor de VPS
ssh-keygen -t ed25519 -f ~/.ssh/gh_klanten -N ""
cat ~/.ssh/gh_klanten.pub
#   -> deze publieke sleutel plak je in GitHub: repo → Settings → Deploy keys
#      → Add deploy key (Allow write access UIT laten = alleen lezen)

# 2) git via die sleutel laten lopen
cat >> ~/.ssh/config <<'CFG'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/gh_klanten
CFG

# 3) oude kopie opzij, repo klonen naar /root/klanten
mv /root/klanten /root/klanten-oud-$(date +%s) 2>/dev/null || true
git clone git@github.com:CrankCo90/brabant-klanten.git /root/klanten

# 4) deploy-script één keer testen
bash /root/klanten/_workflow/vps-autodeploy.sh && echo "eerste publicatie gelukt"

# 5) cron elke 15 minuten
( crontab -l 2>/dev/null; echo "*/15 * * * * /root/klanten/_workflow/vps-autodeploy.sh >/dev/null 2>&1" ) | crontab -
crontab -l   # controle
```

Daarna is alles automatisch: elke 15 min haalt de VPS de laatste versie op en publiceert
elke klant met een kiesdemo (`03-designs/index.html`) naar
`https://<klant>.demo.brabantdigital.nl`. Een log staat in `_workflow/logs/autodeploy.log`.

## Wat het script doet (kort)
- `git fetch` + hard reset naar de laatste versie (de VPS is een schone spiegel).
- Voor elke klant met `03-designs/index.html`: bestanden synchroniseren naar
  `/var/www/demos/<klant>`, rechten zetten, Caddy-blok toevoegen (de 1e keer), Caddy herladen.
- Tooling (`*.sh`, `caddy-snippet.txt`, `*.bak`) wordt niet mee gepubliceerd.

---

## (Intern) Hoe Claude pusht in een nieuwe sessie
De mount ondersteunt geen `.git`, dus pushen gaat via een schone kopie in de sandbox:
```bash
TOK=$(tr -d '\n' < "_workflow/.deploy-token")
rm -rf /tmp/bk && git clone "https://${TOK}@github.com/CrankCo90/brabant-klanten.git" /tmp/bk
rsync -a --delete --exclude='.git' --exclude='_workflow/.deploy-token' --exclude='*.bak' \
      --exclude='**/assets/img/*.png' "./" /tmp/bk/
cd /tmp/bk && git add -A && git -c user.email=leroyb@home.nl -c user.name=Pro4Never \
      commit -q -m "update" && git push -q origin main
```
De VPS-cron (elke 15 min) doet de rest.
