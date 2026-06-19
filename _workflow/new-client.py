#!/usr/bin/env python3
"""Verwerkt een via het dashboard aangemelde klant: registreert, bouwt de demo, pusht en publiceert.
Aanroep: python3 _workflow/new-client.py '<json met bedrijf,niche,regio,link,notitie>'"""
import sys, os, json, re, subprocess, datetime
from pathlib import Path
ROOT=Path("/root/klanten")
def slug(n): 
    s=re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-'); return (s[:40] or "klant")
def run(c): return subprocess.run(c,cwd=str(ROOT),capture_output=True,text=True)
def _outreach(nk,plaats,bedrijf,taal):
    SEARCH={"hond":"hondentrimsalon","nagels":"nagelstudio","pedicure":"pedicure","kapper":"kapper","schilder":"stukadoor"}
    WORDNL={"hond":"hondentrimsalons","nagels":"nagelstudio's","pedicure":"pedicures","kapper":"kapsalons","schilder":"schilders- en stukadoorsbedrijven"}
    WORDEN={"hond":"dog grooming salons","nagels":"nail studios","pedicure":"pedicures","kapper":"hair salons","schilder":"painting and plastering companies"}
    pl=plaats or ("de buurt" if taal!="en" else "your area"); sw=SEARCH.get(nk,"")
    if taal=="en":
        w=WORDEN.get(nk,"local businesses")
        comp="I came across %s while looking for %s in %s \u2014 and noticed a modern website of your own is still missing or a bit dated."%(bedrijf,w,pl)
        tip="make sure you're easy to find on Google with a (free) Google Business profile, your opening hours and a clickable phone number."
        verb=["Book online, 24/7 \u2014 fewer calls and missed bookings.","Easier to find on Google for '%s %s'."%(sw,pl),"Your treatments and prices clearly listed, with photos.","Clickable WhatsApp & call button, Dutch/English with one tap.","Fast, modern look on phone, tablet and desktop."]
    else:
        w=WORDNL.get(nk,"lokale ondernemers")
        comp="Ik kwam %s tegen toen ik in %s naar %s zocht \u2014 en het viel me op dat een eigen, moderne website nog ontbreekt of wat verouderd is."%(bedrijf,pl,w)
        TIP={"kapper":"zet een directe link naar je online agenda of WhatsApp bovenaan je Instagram-bio en in je Google-profiel \u2014 zo boeken klanten met \u00e9\u00e9n tik, ook 's avonds.",
             "nagels":"zet een directe link naar je online agenda of WhatsApp bovenaan je Instagram-bio \u2014 zo boeken klanten met \u00e9\u00e9n tik, ook 's avonds.",
             "pedicure":"zorg dat je in Google goed vindbaar bent via een (gratis) Google-bedrijfsprofiel met je openingstijden en een klikbaar telefoonnummer.",
             "hond":"zorg dat je in Google goed vindbaar bent via een (gratis) Google-bedrijfsprofiel, met je openingstijden en een klikbaar telefoonnummer.",
             "schilder":"zet duidelijke voor/na-foto's van je projecten online met je werkgebied erbij — zo zien nieuwe klanten je vakmanschap en vinden ze je in Google."}
        tip=TIP.get(nk,"zorg dat je in Google goed vindbaar bent via een (gratis) Google-bedrijfsprofiel met je openingstijden en een klikbaar telefoonnummer.")
        verb=["Online een afspraak maken, 24/7 \u2014 minder telefoon en gemiste boekingen.","Beter vindbaar in Google op '%s %s'."%(sw or "jouw vak",pl),"Je behandelingen en prijzen netjes op een rij, met foto's.","Klikbare WhatsApp- en belknop, en Nederlands/Engels met \u00e9\u00e9n knop.","Snelle, moderne uitstraling op telefoon, tablet en computer."]
    return comp,tip,verb
def main():
    raw=sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()
    d=json.loads(raw)
    bedrijf=(d.get("bedrijf") or "").strip()
    if not bedrijf: print("Geen bedrijfsnaam."); return 1
    niche=(d.get("niche") or "Onbekend").strip(); regio=(d.get("regio") or "").strip()
    _nlc=niche.lower()
    if "pedicure" in _nlc or "voet" in _nlc: nk2,nlabel="pedicure","Pedicures"
    elif "nagel" in _nlc or "nail" in _nlc: nk2,nlabel="nagels","Nagelstudio's"
    elif "stukadoor" in _nlc or "stucadoor" in _nlc or "stuc" in _nlc or "schilder" in _nlc or "pleister" in _nlc or "afbouw" in _nlc: nk2,nlabel="schilder","Schilders & Stukadoors"
    elif "kapper" in _nlc or "kapsalon" in _nlc or "barber" in _nlc or "haar" in _nlc: nk2,nlabel="kapper","Kappers"
    elif "hond" in _nlc or "trim" in _nlc or "dog" in _nlc: nk2,nlabel="hond","Hondentrimsalons"
    else: nk2,nlabel=None,niche
    link=(d.get("link") or "").strip(); notitie=(d.get("notitie") or "").strip(); telefoon=(d.get("telefoon") or "").strip()
    land=(d.get("land") or "NL").strip().upper(); taal=("nl" if land=="NL" else "en")
    sg=slug(bedrijf)
    sf=ROOT/"_workflow/salons-batch1.json"; S=json.loads(sf.read_text(encoding="utf-8"))
    if not any(x["slug"]==sg for x in S):
        kort=re.sub(r'^(hondentrimsalon|trimsalon|dogsalon|pedicuresalon|pedicurepraktijk|pedicure|nagelstudio|nagelsalon|stukadoorsbedrijf|stucadoorsbedrijf|stukadoor|stucadoor|schildersbedrijf|schilderbedrijf|schilder|salon)\s+','',bedrijf,flags=re.I).strip() or bedrijf
        _tel=re.sub(r'[^0-9]','',telefoon)
        if _tel.startswith("0"): _tel="+31"+_tel[1:]
        elif _tel and not _tel.startswith("31"): _tel="+31"+_tel
        td = telefoon if telefoon else ("Call or message us" if taal=="en" else "Bel of app ons")
        th = ("tel:"+_tel) if _tel else "#contact"
        ent={"bedrijf":bedrijf,"kort":kort,"slug":sg,"plaats":regio,"tel_display":td,"tel_href":th,"taal":taal}
        if nk2: ent["niche"]=nk2
        S.append(ent)
        sf.write_text(json.dumps(S,ensure_ascii=False,indent=1),encoding="utf-8")
    g=run(["python3","_workflow/generate-demo.py"])
    if g.returncode!=0: print("generate-demo fout:",g.stderr[-500:]); return 1
    url="https://%s.demo.brabantdigital.nl"%sg
    cf=ROOT/"dashboard/clients.json"; C=json.loads(cf.read_text(encoding="utf-8"))
    if not any(c["bedrijf"]==bedrijf for c in C):
        C.append({"bedrijf":bedrijf,"niche":nlabel,"regio":regio,"plaats":regio,"status":"demo","score":0,
                  "werkdag":datetime.date.today().isoformat(),"demo_url":url,
                  "waarom":"Via dashboard aangemeld. "+notitie,"fouten":[],"contact":link,
                  "bron":(link if link.lower().startswith("http") else None),"social":None,"telefoon":(telefoon or None),"land":land,"taal":taal})
        cf.write_text(json.dumps(C,ensure_ascii=False,indent=1),encoding="utf-8")
    pf=ROOT/"_workflow/outreach/prospects.json"; P=json.loads(pf.read_text(encoding="utf-8"))
    _comp,_tip,_verb=_outreach(nk2,regio,bedrijf,taal)
    if not any(p["bedrijf"]==bedrijf for p in P):
        P.append({"bedrijf":bedrijf,"aanhef":("Hi," if taal=="en" else "Hoi,"),"plaats":regio,"email":"","status":"concept","demo_url":url,"land":land,"taal":taal,
                  "deadline":"","onderwerp":(("I already built a website for %s (take a look)"%bedrijf) if taal=="en" else ("Ik heb alvast een website voor %s gemaakt (kijk even mee)"%bedrijf)),
                  "compliment":_comp,"gratis_tip":_tip,"verbeteringen":_verb})
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
