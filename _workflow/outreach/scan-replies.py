#!/usr/bin/env python3
"""Scant de mailbox (IMAP) op antwoorden van prospects en schrijft replies.json:
{email: {"status":"nee|ja|reactie","datum":"...","laatste":"onderwerp/snippet"}}.
Leest IMAP-gegevens uit /root/outreach-data/.smtp-env (IMAP_HOST, IMAP_PORT, SMTP_USER, SMTP_PASS)."""
import imaplib, email, json, os, re, datetime, subprocess
from pathlib import Path
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

# --- "nee"-reacties automatisch verwerken: klant -> afgewezen, demo offline, nooit meer mailen ---
try:
    ROOT=Path(__file__).resolve().parents[2]
    P=json.load(open(ROOT/"_workflow/outreach/prospects.json"))
    email2bedr={(p.get("email") or "").lower():p.get("bedrijf") for p in P if p.get("email")}
    cf=ROOT/"dashboard/clients.json"; C=json.load(open(cf))
    nd=ROOT/"_workflow/niet-deployen.txt"
    nd_set=set(l.strip() for l in nd.read_text().splitlines() if l.strip() and not l.strip().startswith("#")) if nd.exists() else set()
    changed=False
    for em,info in out.items():
        if (info or {}).get("status")!="nee": continue
        bedr=email2bedr.get(em.lower())
        if not bedr: continue
        for c in C:
            if c.get("bedrijf")==bedr and c.get("status")!="afgewezen":
                c["status"]="afgewezen"; changed=True
                m=re.search(r"https://([^.]+)\.demo", c.get("demo_url") or "")
                if m: nd_set.add(m.group(1))
    if changed:
        json.dump(C,open(cf,"w"),ensure_ascii=False,indent=1)
        nd.write_text("# Klanten die NOOIT gepubliceerd mogen worden (1 map-slug per regel).\n# vps-autodeploy.sh slaat deze over en haalt een eventueel al-live exemplaar offline.\n# Regel weghalen = klant mag weer gedeployed worden. Regels met # worden genegeerd.\n"+"\n".join(sorted(nd_set))+"\n")
        subprocess.run(["bash","-lc","cd %s && git add -A && git -c user.email=vps@brabantdigital.nl -c user.name=BD-VPS commit -q -m 'auto: nee-reacties -> afgewezen'"%ROOT])
        if os.path.exists("/root/outreach-data/.git-token"):
            tok=open("/root/outreach-data/.git-token").read().strip()
            subprocess.run(["bash","-lc","cd %s && git push -q https://%s@github.com/CrankCo90/brabant-klanten.git HEAD:main"%(ROOT,tok)])
        print("nee-reacties -> afgewezen verwerkt")
except Exception as e:
    print("reply-verwerking fout:",e)
