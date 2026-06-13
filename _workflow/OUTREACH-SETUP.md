# OUTREACH — automatisch prospects benaderen (e-mail)

> Funnel: Claude vindt prospects → bouwt per prospect een kiesdemo → pusht → de VPS
> publiceert (15-min cron) → de VPS mailt (dagcron) het voorstel, met daglimiet en logging.
> Reacties komen binnen op aanbod@brabantdigital.nl.

## Hoe de stukjes samenwerken
- **prospects.json** (in de repo, beheert Claude): de wachtrij. Een prospect met
  `"status": "klaar"` en een `demo_url` wordt gemaild.
- **send-outreach.py** (in de repo, draait op de VPS): verstuurt.
- **/root/outreach-data/** (op de VPS, BUITEN de repo): je wachtwoord (`.smtp-env`) en het
  `sent-log.csv`. Staat los van Git, dus de 15-min auto-pull overschrijft het nooit, en je
  wachtwoord komt nooit in Git of de chat.

## Vangrails (ingebouwd)
- **Nooit twee keer**: elk verzonden adres staat in `sent-log.csv`; dubbelen worden overgeslagen.
- **Daglimiet**: standaard 20/dag (instelbaar via `OUTREACH_CAP`). Rustige spreiding (8s) tussen mails.
- **Afmelden + afzender**: elke mail heeft een duidelijke afzender en een "antwoord nee"-afmeldregel.
- **Alleen na demo**: er gaat pas een mail uit als er een werkende demo-link klaarstaat.

## Eenmalige VPS-setup
```bash
mkdir -p /root/outreach-data
nano /root/outreach-data/.smtp-env      # vul in volgens _workflow/outreach/.smtp-env.example
chmod 600 /root/outreach-data/.smtp-env

# test (stuurt alleen als er een prospect 'klaar' staat; veilig met lege wachtrij):
OUTREACH_DATA=/root/outreach-data python3 /root/klanten/_workflow/outreach/send-outreach.py

# dagelijkse cron om 10:00 (max 20/dag):
( crontab -l 2>/dev/null; echo "0 10 * * * OUTREACH_DATA=/root/outreach-data OUTREACH_CAP=20 /usr/bin/python3 /root/klanten/_workflow/outreach/send-outreach.py >> /root/outreach-data/send.log 2>&1" ) | crontab -
```

## SMTP-gegevens vinden (Vimexx)
Webmail/instellingen → uitgaande server (SMTP). Meestal poort **587** (STARTTLS) of **465** (SSL),
host iets als `smtpauth.vimexx-mail.nl` of `mail.<jouwhost>`. Vul host/poort/wachtwoord in `.smtp-env`.

## Belangrijk (kort, eerlijk)
Koude B2B-mail mag in NL, mits herkenbaar, met afmeldoptie en zonder misleiding — dat zit ingebouwd.
Houd het volume laag en persoonlijk: dat is beter voor je domeinreputatie én voor de respons.
Reageert iemand met "nee", dan zet Claude dat adres op een blokkeerlijst (niet meer benaderen).
