#!/usr/bin/env python3
"""Scant de mailbox (IMAP) op antwoorden van prospects en schrijft replies.json:
{email: {"status":"nee|ja|reactie","datum":"...","laatste":"onderwerp/snippet"}}.
Leest IMAP-gegevens uit /root/outreach-data/.smtp-env (IMAP_HOST, IMAP_PORT, SMTP_USER, SMTP_PASS)."""
import imaplib, email, json, os, re, datetime
from email.header import decode_header
DATA=os.environ.get("OUTREACH_DATA","/root/outreach-data")
env={}
for ln in open(os.path.join(DATA,".smtp-env")).read().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln: k,v=ln.split("=",1); env[k.strip()]=v.strip()
host=env.get("IMAP_HOST"); port=int(env.get("IMAP_PORT","993"))
user=env.get("SMTP_USER"); pw=env.get("SMTP_PASS")
if not host: print("Geen IMAP_HOST in .smtp-env"); raise SystemExit
sent=set()
sl=os.path.join(DATA,"sent-log.csv")
if os.path.exists(sl):
    import csv
    for r in csv.DictReader(open(sl)): sent.add(r["email"].lower())
M=imaplib.IMAP4_SSL(host,port); M.login(user,pw); M.select("INBOX")
typ,data=M.search(None,'(SINCE "%s")'%(datetime.date.today()-datetime.timedelta(days=30)).strftime("%d-%b-%Y"))
out=json.load(open(os.path.join(DATA,"replies.json"))) if os.path.exists(os.path.join(DATA,"replies.json")) else {}
for num in data[0].split():
    t,d=M.fetch(num,"(RFC822)"); msg=email.message_from_bytes(d[0][1])
    frm=email.utils.parseaddr(msg.get("From"))[1].lower()
    if frm not in sent: continue
    subj=str(decode_header(msg.get("Subject",""))[0][0])
    body=""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type()=="text/plain":
                try: body=part.get_payload(decode=True).decode(errors="ignore"); break
                except: pass
    else:
        try: body=msg.get_payload(decode=True).decode(errors="ignore")
        except: body=""
    low=(subj+" "+body).lower()
    st="reactie"
    if re.search(r"\b(nee|geen interesse|afmeld|uitschrijf|niet ge.nteresseerd|stop)\b",low): st="nee"
    elif re.search(r"\b(ja|graag|interesse|akkoord|doen|bestellen|afspraak)\b",low): st="ja"
    out[frm]={"status":st,"datum":datetime.date.today().isoformat(),"laatste":subj[:120]}
json.dump(out,open(os.path.join(DATA,"replies.json"),"w"),ensure_ascii=False,indent=1)
print("replies bijgewerkt:",len(out))
