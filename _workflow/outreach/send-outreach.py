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
from email.utils import formatdate, make_msgid
from pathlib import Path
import re as _re
def _aanhef(p):
    g="Hi" if p.get("taal")=="en" else "Hoi"
    a=(p.get("aanhef") or "").strip()
    if a and a.lower() not in ("hoi,","hoi","hi,","hi"): return a
    b=p.get("bedrijf") or ""
    for pat in (r"^([A-Za-zÀ-ÿ]+)'s\b", r"\bby ([A-Za-zÀ-ÿ]+)", r"(?:nagelstudio|nagelsalon|hondentrimsalon|trimsalon|dogsalon|salon)\s+([A-Za-zÀ-ÿ]+)$"):
        m=_re.search(pat,b,_re.I)
        if m:
            n=m.group(1)
            if not _re.match(r"^(nails?|beauty|design|nagel|hair|studio|hondjes|dog)$",n,_re.I):
                return g+" %s,"%((n[:1].upper()+n[1:]) if len(n)>1 else b)
    return g+","


REPO_DIR  = Path(__file__).resolve().parent
DATA_DIR  = Path(os.environ.get("OUTREACH_DATA", "/root/outreach-data"))
PROSPECTS = REPO_DIR / "prospects.json"
TEMPLATE  = Path(os.environ["OUTREACH_TEMPLATE"]) if os.environ.get("OUTREACH_TEMPLATE") else (REPO_DIR / "template-nl.txt")
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
    template_en = (REPO_DIR/"template-en.txt").read_text(encoding="utf-8") if (REPO_DIR/"template-en.txt").exists() else template
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
        _only=os.environ.get("OUTREACH_ONLY","").strip()
        _onlyset=set(x.strip() for x in _only.split("|") if x.strip()) if _only else None
        if _onlyset is not None:
            if p.get("bedrijf") not in _onlyset: continue     # expliciete selectie uit dashboard -> stuur ongeacht concept/klaar
        elif p.get("status") != "klaar":
            continue                                          # autopilot / bulk-alles -> alleen status 'klaar' 
        email = (p.get("email") or "").strip()
        if "@" not in email or email.lower() in done: continue
        verb = p.get("verbeteringen") or []
        verb_txt = "\n".join("- " + v for v in verb) if verb else "- Online afspraken, betere vindbaarheid in Google en een snelle, moderne uitstraling."
        afmelder = p.get("afmelder") or (("You received this message once because I help local businesses get online. Not interested? Just reply 'no' and you will never hear from me again.") if p.get("taal")=="en" else ("Je krijgt dit bericht eenmalig omdat ik lokale ondernemers in de buurt help. Geen interesse? Eén woordje \"nee\" terug en je hoort nooit meer iets van me."))
        _tpl = template_en if p.get("taal")=="en" else template
        body = (_tpl
                .replace("{{aanhef}}",       _aanhef(p))
                .replace("{{compliment}}",   p.get("compliment",""))
                .replace("{{gratis_tip}}",   p.get("gratis_tip",""))
                .replace("{{bedrijf}}",      p.get("bedrijf",""))
                .replace("{{plaats}}",       p.get("plaats",""))
                .replace("{{demo_url}}",     p.get("demo_url",""))
                .replace("{{verbeteringen}}",verb_txt)
                .replace("{{deadline}}",     p.get("deadline") or "twee weken vanaf vandaag")
                .replace("{{afmelder}}",     afmelder))
        msg = EmailMessage()
        msg["Subject"]  = p.get("onderwerp") or f"Een websitevoorstel voor {p.get('bedrijf','uw bedrijf')}"
        msg["From"]     = f'{env["FROM_NAME"]} <{env["FROM_EMAIL"]}>'
        msg["To"]       = email
        msg["Reply-To"] = env["FROM_EMAIL"]
        msg["Date"]       = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=(env["FROM_EMAIL"].split("@")[-1]))
        msg["List-Unsubscribe"]="<mailto:%s?subject=Uitschrijven>"%env["FROM_EMAIL"]
        _intro=os.environ.get("OUTREACH_INTRO","").strip()
        if _intro: body=_intro+"\n\n"+body
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
