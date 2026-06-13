#!/usr/bin/env python3
"""Outreach-mailer. Draait op de VPS via cron.
- Leest prospects uit de repo (_workflow/outreach/prospects.json) — die beheert Claude.
- Wachtwoord + 'al-verzonden'-log staan BUITEN de repo (OUTREACH_DATA), zodat de
  15-min auto-pull ze nooit overschrijft.
- Vangrails: nooit hetzelfde adres twee keer, dagelijkse limiet, rustige spreiding,
  afmeldregel + duidelijke afzender in elke mail.
"""
import json, csv, os, sys, ssl, smtplib, datetime, time
from email.message import EmailMessage
from pathlib import Path

REPO_DIR  = Path(__file__).resolve().parent
DATA_DIR  = Path(os.environ.get("OUTREACH_DATA", "/root/outreach-data"))
PROSPECTS = REPO_DIR / "prospects.json"
TEMPLATE  = REPO_DIR / "template-nl.txt"
ENV_FILE  = DATA_DIR / ".smtp-env"
LOG       = DATA_DIR / "sent-log.csv"
CAP       = int(os.environ.get("OUTREACH_CAP", "20"))

def load_env(p):
    d = {}
    if p.exists():
        for ln in p.read_text().splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1); d[k.strip()] = v.strip()
    return d

def sent_set():
    s = set()
    if LOG.exists():
        with open(LOG, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f): s.add(r["email"].lower())
    return s

def sent_today():
    n, today = 0, datetime.date.today().isoformat()
    if LOG.exists():
        with open(LOG, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["datum"].startswith(today): n += 1
    return n

def log_send(email, bedrijf):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    new = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["datum", "email", "bedrijf"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), email, bedrijf])

def main():
    env = load_env(ENV_FILE)
    need = ["SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASS","FROM_NAME","FROM_EMAIL"]
    miss = [k for k in need if not env.get(k)]
    if miss:
        print(f"Ontbrekende SMTP-config {miss} in {ENV_FILE}"); sys.exit(1)
    if not PROSPECTS.exists():
        print("Geen prospects.json — niets te doen."); return
    prospects = json.loads(PROSPECTS.read_text(encoding="utf-8"))
    template  = TEMPLATE.read_text(encoding="utf-8")
    done = sent_set()
    left = CAP - sent_today()
    if left <= 0:
        print("Daglimiet bereikt."); return

    port = int(env["SMTP_PORT"])
    if port == 465:
        srv = smtplib.SMTP_SSL(env["SMTP_HOST"], port, context=ssl.create_default_context())
    else:
        srv = smtplib.SMTP(env["SMTP_HOST"], port); srv.starttls(context=ssl.create_default_context())
    srv.login(env["SMTP_USER"], env["SMTP_PASS"])

    sent = 0
    for p in prospects:
        if sent >= left: break
        if p.get("status") != "klaar": continue          # alleen prospects met klaarstaande demo
        email = (p.get("email") or "").strip()
        if "@" not in email or email.lower() in done: continue
        body = (template
                .replace("{{bedrijf}}",  p.get("bedrijf",""))
                .replace("{{plaats}}",   p.get("plaats",""))
                .replace("{{demo_url}}", p.get("demo_url",""))
                .replace("{{voornaam}}", p.get("voornaam") or "daar"))
        msg = EmailMessage()
        msg["Subject"]  = p.get("onderwerp") or f"Een websitevoorstel voor {p.get('bedrijf','uw bedrijf')}"
        msg["From"]     = f'{env["FROM_NAME"]} <{env["FROM_EMAIL"]}>'
        msg["To"]       = email
        msg["Reply-To"] = env["FROM_EMAIL"]
        msg.set_content(body)
        try:
            srv.send_message(msg)
            log_send(email, p.get("bedrijf",""))
            done.add(email.lower()); sent += 1
            print("verzonden:", email)
            time.sleep(8)                                  # rustige spreiding = betere reputatie
        except Exception as e:
            print("FOUT bij", email, ":", e)
    srv.quit()
    print(f"Klaar: {sent} verzonden (daglimiet {CAP}, al verzonden vandaag {sent_today()}).")

if __name__ == "__main__":
    main()
