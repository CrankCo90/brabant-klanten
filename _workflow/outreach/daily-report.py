#!/usr/bin/env python3
"""Outreach-dagrapport per e-mail: hoeveel vandaag gemaild + welke reacties. Cron aan eind werkdag."""
import os,csv,json,datetime,ssl,smtplib
from email.message import EmailMessage
from email.utils import formatdate
DATA=os.environ.get("OUTREACH_DATA","/root/outreach-data")
TO=os.environ.get("REPORT_TO","leroyb@home.nl")
env={}
for ln in open(os.path.join(DATA,".smtp-env")).read().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln: k,v=ln.split("=",1); env[k.strip()]=v.strip()
today=datetime.date.today().isoformat()
mailed=[]
sl=os.path.join(DATA,"sent-log.csv")
if os.path.exists(sl):
    for r in csv.DictReader(open(sl)):
        if r["datum"].startswith(today): mailed.append(r.get("bedrijf") or r.get("email"))
reacties={"ja":[],"nee":[],"reactie":[]}
rp=os.path.join(DATA,"replies.json")
if os.path.exists(rp):
    for em,info in json.load(open(rp)).items():
        if (info.get("datum") or "")==today: reacties.get(info.get("status","reactie"),reacties["reactie"]).append(em)
tot=sum(len(v) for v in reacties.values())
L=["Outreach-dagrapport - %s"%today,"","Gemaild vandaag: %d"%len(mailed)]
L+=["  - "+str(b) for b in mailed]
L+=["","Reacties vandaag: %d (ja %d / nee %d / overig %d)"%(tot,len(reacties["ja"]),len(reacties["nee"]),len(reacties["reactie"]))]
if reacties["ja"]: L.append("  JA (opvolgen!): "+", ".join(reacties["ja"]))
if reacties["nee"]: L.append("  NEE (auto-afgewezen): "+", ".join(reacties["nee"]))
if reacties["reactie"]: L.append("  Overig: "+", ".join(reacties["reactie"]))
msg=EmailMessage(); msg["Subject"]="Outreach-dagrapport %s - %d gemaild, %d reacties"%(today,len(mailed),tot)
msg["From"]=f'{env["FROM_NAME"]} <{env["FROM_EMAIL"]}>'; msg["To"]=TO; msg["Date"]=formatdate(localtime=True)
msg.set_content("\n".join(L))
port=int(env["SMTP_PORT"])
s=smtplib.SMTP_SSL(env["SMTP_HOST"],port,context=ssl.create_default_context()) if port==465 else smtplib.SMTP(env["SMTP_HOST"],port)
if port!=465: s.starttls(context=ssl.create_default_context())
s.login(env["SMTP_USER"],env["SMTP_PASS"]); s.send_message(msg); s.quit()
print("dagrapport verzonden naar",TO)
