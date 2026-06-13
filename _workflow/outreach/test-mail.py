#!/usr/bin/env python3
"""Stuur EEN testmail om de SMTP-setup te controleren.
Gebruik op de VPS:
    OUTREACH_DATA=/root/outreach-data python3 _workflow/outreach/test-mail.py info@adres.nl
"""
import sys, os, ssl, smtplib
from email.message import EmailMessage
from pathlib import Path
if len(sys.argv) < 2:
    print("Gebruik: test-mail.py <ontvanger@adres>"); sys.exit(1)
to = sys.argv[1]
env_path = Path(os.environ.get("OUTREACH_DATA", "/root/outreach-data")) / ".smtp-env"
if not env_path.exists():
    print(f"Geen {env_path} — vul eerst je SMTP-gegevens in."); sys.exit(1)
env = {}
for ln in env_path.read_text().splitlines():
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1); env[k.strip()] = v.strip()
msg = EmailMessage()
msg["Subject"]  = "Testbericht — Brabant Digital"
msg["From"]     = f'{env["FROM_NAME"]} <{env["FROM_EMAIL"]}>'
msg["To"]       = to
msg["Reply-To"] = env["FROM_EMAIL"]
msg.set_content("Dit is een testbericht van Brabant Digital om te controleren of het e-mailversturen werkt.\n\nGroet,\nLeroy")
port = int(env["SMTP_PORT"])
if port == 465:
    srv = smtplib.SMTP_SSL(env["SMTP_HOST"], port, context=ssl.create_default_context())
else:
    srv = smtplib.SMTP(env["SMTP_HOST"], port); srv.starttls(context=ssl.create_default_context())
srv.login(env["SMTP_USER"], env["SMTP_PASS"]); srv.send_message(msg); srv.quit()
print("Testmail verzonden naar", to)
