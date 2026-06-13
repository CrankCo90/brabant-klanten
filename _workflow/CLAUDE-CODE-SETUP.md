# CLAUDE CODE — autonoom commando's laten uitvoeren

> Cowork (waar je dit nu leest) draait in een afgeschermde sandbox die je VPS niet kan
> bereiken. Voor échte commando's (rsync/ssh/caddy) gebruik je **Claude Code**: dezelfde
> Claude, als programma in een Terminal. Hieronder de aanbevolen, veilige opzet.

## Aanbevolen: Claude Code op de VPS
Altijd aan, Linux (rsync/ssh/caddy native), past bij je VPS-snapshots als vangnet.
Je PC + Cowork blijf je gebruiken voor het creatieve/ontwerpwerk; de VPS doet het draaien/deployen.

### Stap 1 — Project naar de VPS (eenmalig)
Vanaf je PC (PowerShell), upload de hele werkmap inclusief de `.claude/`-config en `CLAUDE.md`:
```powershell
scp -r "C:\Users\Gebruiker\Desktop\Klanten werven voor nieuwe site" root@93.190.187.213:/root/klanten
```

### Stap 2 — Aparte deploy-SSH-sleutel (jouw keuze, veiligst)
Op de VPS:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/brabant_deploy -N ""
cat ~/.ssh/brabant_deploy.pub >> ~/.ssh/authorized_keys   # voor deploy naar zichzelf/andere servers
```
Deze sleutel is los van je persoonlijke sleutel en kun je later in één regel intrekken.

### Stap 3 — Claude Code installeren op de VPS
```bash
curl -fsSL https://claude.ai/install.sh | bash      # of: npm i -g @anthropic-ai/claude-code
```
Inloggen: voer `claude` uit en volg de login (of zet een API-key: `export ANTHROPIC_API_KEY=...` in `~/.bashrc`).

### Stap 4 — Starten in de projectmap
```bash
cd /root/klanten
claude
```
De `.claude/settings.json` en `CLAUDE.md` worden automatisch geladen. Je kunt nu gewoon
opdrachten typen ("Zet de demo van Scott live", "Maak een nieuwe klant aan: <link>").

### Altijd-aan / op de achtergrond (optioneel)
```bash
tmux new -s claude
cd /root/klanten && claude
# loskoppelen: Ctrl-b daarna d   ·   terug: tmux attach -t claude
```
Of een losse opdracht zonder UI: `claude -p "Zet de demo van Scott live" --permission-mode acceptEdits`

## Hoe "volledig autonoom" hier werkt (veilig ingericht)
- Stand `acceptEdits` + een ruime **allow-lijst** (rsync, scp, ssh, chmod, caddy reload, git,
  beeldconversie, je deploy-script) → voor het dagelijkse werk vraagt Claude **niets**.
- Een korte **deny-lijst** + de **guard-hook** (`.claude/hooks/guard.sh`) blokkeren
  systeem-vernietigende commando's (rm op /, /var/www, /etc, mkfs, dd, reboot…). Die floor blijft
  altijd staan — ook als een opdracht verkeerd wordt begrepen.
- Wil je écht nul tussenvragen (ook voor nieuwe, onbekende commando's)? Dan kan
  `claude --dangerously-skip-permissions`, maar dat raad ik op een live server af; de huidige
  opzet voelt voor het normale werk al volledig autonoom.

## Vangnet & terugkoppeling
- **VPS-snapshot** vóór grote/verwijderende acties (jouw VPS-paneel → Snapshots).
- **Dagelijkse samenvatting** schrijft Claude naar `_workflow/logs/DAGELIJKS-<datum>.md`.

## Klantbenadering (autonoom — let op)
Je koos voor autonoom versturen. Eén eerlijke kanttekening: een verkeerd bericht is meteen
weg en kan je reputatie raken. In `CLAUDE.md` staat daarom de afspraak: élke verzending loggen,
nooit dezelfde prospect twee keer, netjes/persoonlijk houden. Het verzendkanaal (mail/WhatsApp)
richten we als aparte stap in — zeg het wanneer je daaraan toe bent.

## Alternatief: op je PC in VS Code
Kan ook, maar op Windows heeft Claude Code Git Bash of WSL nodig voor rsync/ssh. Minder soepel
dan de VPS; daarom is de VPS de aanrader.
