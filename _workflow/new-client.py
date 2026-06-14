#!/usr/bin/env python3
"""Verwerkt een via het dashboard aangemelde klant: registreert, bouwt de demo, pusht en publiceert.
Aanroep: python3 _workflow/new-client.py '<json met bedrijf,niche,regio,link,notitie>'"""
import sys, os, json, re, subprocess, datetime
from pathlib import Path
ROOT=Path("/root/klanten")
def slug(n): 
    s=re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-'); return (s[:40] or "klant")
def run(c): return subprocess.run(c,cwd=str(ROOT),capture_output=True,text=True)
def main():
    raw=sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()
    d=json.loads(raw)
    bedrijf=(d.get("bedrijf") or "").strip()
    if not bedrijf: print("Geen bedrijfsnaam."); return 1
    niche=(d.get("niche") or "Onbekend").strip(); regio=(d.get("regio") or "").strip()
    link=(d.get("link") or "").strip(); notitie=(d.get("notitie") or "").strip(); telefoon=(d.get("telefoon") or "").strip()
    sg=slug(bedrijf)
    sf=ROOT/"_workflow/salons-batch1.json"; S=json.loads(sf.read_text(encoding="utf-8"))
    if not any(x["slug"]==sg for x in S):
        kort=re.sub(r'^(hondentrimsalon|trimsalon|dogsalon|salon)\s+','',bedrijf,flags=re.I).strip() or bedrijf
        S.append({"bedrijf":bedrijf,"kort":kort,"slug":sg,"plaats":regio,"tel_display":"Bel of app ons","tel_href":"#contact"})
        sf.write_text(json.dumps(S,ensure_ascii=False,indent=1),encoding="utf-8")
    g=run(["python3","_workflow/generate-demo.py"])
    if g.returncode!=0: print("generate-demo fout:",g.stderr[-500:]); return 1
    url="https://%s.demo.brabantdigital.nl"%sg
    cf=ROOT/"dashboard/clients.json"; C=json.loads(cf.read_text(encoding="utf-8"))
    if not any(c["bedrijf"]==bedrijf for c in C):
        C.append({"bedrijf":bedrijf,"niche":niche,"regio":regio,"plaats":regio,"status":"demo","score":0,
                  "werkdag":datetime.date.today().isoformat(),"demo_url":url,
                  "waarom":"Via dashboard aangemeld. "+notitie,"fouten":[],"contact":link,
                  "bron":(link if link.lower().startswith("http") else None),"social":None,"telefoon":(telefoon or None)})
        cf.write_text(json.dumps(C,ensure_ascii=False,indent=1),encoding="utf-8")
    pf=ROOT/"_workflow/outreach/prospects.json"; P=json.loads(pf.read_text(encoding="utf-8"))
    if not any(p["bedrijf"]==bedrijf for p in P):
        P.append({"bedrijf":bedrijf,"aanhef":"Hoi,","plaats":regio,"email":"","status":"concept","demo_url":url,
                  "deadline":"","onderwerp":"Ik heb alvast een website voor %s gemaakt (kijk even mee)"%bedrijf,
                  "compliment":"","gratis_tip":notitie,"verbeteringen":[]})
        pf.write_text(json.dumps(P,ensure_ascii=False,indent=1),encoding="utf-8")
    run(["git","add","-A"]); run(["git","-c","user.email=vps@brabantdigital.nl","-c","user.name=BD-VPS","commit","-q","-m","Nieuwe klant via dashboard: "+bedrijf])
    tokf=Path("/root/outreach-data/.git-token")
    pushed=False
    if tokf.exists():
        tok=tokf.read_text().strip()
        r=run(["git","push","-q","https://%s@github.com/CrankCo90/brabant-klanten.git"%tok,"HEAD:main"]); pushed=(r.returncode==0)
    if pushed:
        run(["bash","_workflow/vps-autodeploy.sh"])
        print("✅ %s verwerkt + gepusht + gepubliceerd → %s"%(bedrijf,url))
    else:
        # geen push mogelijk: lokaal publiceren (let op: niet permanent tot pushen lukt)
        run(["bash","-lc","mkdir -p /var/www/demos/%s && rsync -a %s/%s/03-designs/ /var/www/demos/%s/ && chmod -R a+rX /var/www/demos/%s"%(sg,ROOT,sg,sg,sg)])
        run(["bash","-lc","rsync -a %s/dashboard/ /var/www/admin/ && chmod -R a+rX /var/www/admin"%ROOT])
        print("⚠️ %s lokaal gebouwd + gepubliceerd → %s (geen .git-token → nog niet naar GitHub gepusht; zie CONTROL-SETUP)"%(bedrijf,url))
    return 0
sys.exit(main())
