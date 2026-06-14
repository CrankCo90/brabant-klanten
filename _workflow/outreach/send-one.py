#!/usr/bin/env python3
"""Stuurt EEN kopie van de outreach-mail van een prospect naar een opgegeven adres (voor tests).
Gebruik:  python3 send-one.py "<bedrijf>" <naar-adres>
Onderwerp krijgt [TEST] ervoor; wordt NIET in de sent-log gezet (telt niet als 'benaderd')."""
import sys, os, json, ssl, smtplib
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path
import re as _re
def _aanhef(p):
    a=(p.get("aanhef") or "").strip()
    if a and a.lower() not in ("hoi,","hoi"): return a
    b=p.get("bedrijf") or ""
    for pat in (r"^([A-Za-zÀ-ÿ]+)'s\b", r"\bby ([A-Za-zÀ-ÿ]+)", r"(?:nagelstudio|nagelsalon|hondentrimsalon|trimsalon|dogsalon|salon)\s+([A-Za-zÀ-ÿ]+)$"):
        m=_re.search(pat,b,_re.I)
        if m:
            n=m.group(1)
            if not _re.match(r"^(nails?|beauty|design|nagel|hair|studio|hondjes|dog)$",n,_re.I):
                return "Hoi %s,"%((n[:1].upper()+n[1:]) if len(n)>1 else b)
    return "Hoi,"

ROOT=Path("/root/klanten"); DATA=Path(os.environ.get("OUTREACH_DATA","/root/outreach-data"))
if len(sys.argv)<3: print('Gebruik: send-one.py "<bedrijf>" <naar-adres>'); sys.exit(1)
bedrijf=sys.argv[1]; to=sys.argv[2]
env={}
for ln in (DATA/".smtp-env").read_text().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln: k,v=ln.split("=",1); env[k.strip()]=v.strip()
P=json.loads((ROOT/"_workflow/outreach/prospects.json").read_text())
p=next((x for x in P if x.get("bedrijf")==bedrijf), None)
if not p: print("Prospect niet gevonden:",bedrijf); sys.exit(1)
tpl=(ROOT/"_workflow/outreach/template-nl.txt").read_text()
verb="\n".join("- "+v for v in (p.get("verbeteringen") or []))
afm='Je krijgt dit bericht eenmalig omdat ik lokale ondernemers in de buurt help. Geen interesse? Eén woordje "nee" terug en je hoort nooit meer iets van me.'
body=(tpl.replace("{{aanhef}}",_aanhef(p)).replace("{{compliment}}",p.get("compliment",""))
        .replace("{{gratis_tip}}",p.get("gratis_tip","")).replace("{{bedrijf}}",bedrijf)
        .replace("{{demo_url}}",p.get("demo_url","")).replace("{{verbeteringen}}",verb)
        .replace("{{deadline}}",p.get("deadline","")).replace("{{afmelder}}",afm))
msg=EmailMessage()
msg["Subject"]="[TEST] "+(p.get("onderwerp") or ("Websitevoorstel voor "+bedrijf))
msg["From"]=f'{env["FROM_NAME"]} <{env["FROM_EMAIL"]}>'; msg["To"]=to; msg["Reply-To"]=env["FROM_EMAIL"]
msg["Date"]=formatdate(localtime=True)
msg["Message-ID"]=make_msgid(domain=(env["FROM_EMAIL"].split("@")[-1]))
_intro=os.environ.get("OUTREACH_INTRO","").strip()
if _intro: body=_intro+"\n\n"+body
msg.set_content(body)
port=int(env["SMTP_PORT"])
s=smtplib.SMTP_SSL(env["SMTP_HOST"],port,context=ssl.create_default_context()) if port==465 else smtplib.SMTP(env["SMTP_HOST"],port)
if port!=465: s.starttls(context=ssl.create_default_context())
s.login(env["SMTP_USER"],env["SMTP_PASS"]); s.send_message(msg); s.quit()
print("Testkopie van de '%s'-mail verzonden naar %s"%(bedrijf,to))
