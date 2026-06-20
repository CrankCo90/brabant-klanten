import json,sys,datetime
try:
    from zoneinfo import ZoneInfo; _NOW=datetime.datetime.now(ZoneInfo("Europe/Amsterdam"))
except Exception:
    _NOW=datetime.datetime.utcnow()+datetime.timedelta(hours=2)
SB='_workflow/salons-batch1.json'; CL='dashboard/clients.json'; PR='_workflow/outreach/prospects.json'
sb=json.load(open(SB)); cl=json.load(open(CL)); pr=json.load(open(PR))
quals=json.load(open('/tmp/new_quals.json'))
existing={s['slug'] for s in sb}
DEADLINE="vrijdag 26 juni 2026"; WERKDAG=_NOW.strftime("%Y-%m-%d"); AANGEMAAKT=_NOW.strftime("%Y-%m-%dT%H:%M:%S")
NL={"hond":"Hondentrimsalons","nagels":"Nagelstudio's","pedicure":"Pedicures","kapper":"Kappers","schilder":"Schilders & Stukadoors","donza":"DONZA TEST"}
WORD={"hond":"hondentrimsalons","nagels":"nagelstudio's","pedicure":"pedicures","kapper":"kapsalons","schilder":"schilders- en stukadoorsbedrijven","donza":"testbedrijven"}
TIP={
 "hond":"zorg dat je in Google goed vindbaar bent via een (gratis) Google-bedrijfsprofiel, met je openingstijden en een klikbaar telefoonnummer — daar zoeken baasjes als eerste naar een trimsalon.",
 "nagels":"zet een directe link naar je online agenda of WhatsApp bovenaan je Instagram-bio — zo boeken klanten met één tik, ook 's avonds.",
 "pedicure":"zorg dat je in Google goed vindbaar bent via een (gratis) Google-bedrijfsprofiel met je openingstijden en een klikbaar telefoonnummer — daar zoeken klanten als eerste naar een pedicure.",
 "kapper":"zet een directe link naar je online agenda of WhatsApp bovenaan je Instagram-bio en in je Google-profiel — zo boeken klanten met één tik, ook 's avonds.",
 "schilder":"zet duidelijke voor/na-foto's van je projecten online met je werkgebied erbij — zo zien nieuwe klanten meteen je vakmanschap en vinden ze je in Google.",
 "donza":"dit is een testprofiel om functionaliteiten te controleren."}
def benefits(niche,plaats):
    if niche=="hond":
        return ["Online een afspraak maken, 24/7 — geen telefoontjes meer tijdens het trimmen.",
         "Beter vindbaar in Google op 'hondentrimsalon %s'."%plaats,
         "Je behandelingen en reviews netjes op een rij, met voor/na-foto's.",
         "Klikbare WhatsApp- en belknop, en Nederlands/Engels met één knop.",
         "Snelle, moderne uitstraling op telefoon, tablet en computer."]
    if niche=="nagels":
        return ["Online een afspraak maken, 24/7 — minder appjes en gemiste boekingen.",
         "Beter vindbaar in Google op 'nagelstudio %s'."%plaats,
         "Je behandelingen en prijzen netjes op een rij, met foto's van je werk.",
         "Klikbare WhatsApp- en belknop, en Nederlands/Engels met één knop.",
         "Snelle, moderne uitstraling op telefoon, tablet en computer."]
    if niche=="kapper":
        return ["Online een afspraak maken, 24/7 — minder telefoon en gemiste boekingen.",
         "Beter vindbaar in Google op 'kapper %s'."%plaats,
         "Je behandelingen en prijzen netjes op een rij, met foto's van je werk.",
         "Klikbare WhatsApp- en belknop, en Nederlands/Engels met één knop.",
         "Snelle, moderne uitstraling op telefoon, tablet en computer."]
    if niche=="schilder":
        return ["Offertes 24/7 online aanvragen via een duidelijk formulier — minder telefoon, meer aanvragen.",
         "Beter vindbaar in Google op 'stukadoor %s' en 'schilder %s'."%(plaats,plaats),
         "Je projecten en reviews netjes op een rij, met voor/na-foto's die vakmanschap tonen.",
         "Klikbare WhatsApp- en belknop, en Nederlands/Engels met één knop.",
         "Snelle, moderne uitstraling op telefoon, tablet en computer."]
    if niche=="donza":
        return ["TEST: offerte-/contactformulier werkt 24/7.",
         "TEST: zes premium ontwerpen onder één subdomein.",
         "TEST: voor/na-slider in ontwerp 1 en 2.",
         "TEST: klikbare WhatsApp- en belknop (alleen bij mobiel nummer).",
         "TEST: responsive op telefoon, tablet en computer."]
    return ["Online een afspraak maken, 24/7 — geen telefoontjes meer tijdens een behandeling.",
     "Beter vindbaar in Google op 'pedicure %s'."%plaats,
     "Je behandelingen en tarieven netjes op een rij, met aandacht voor medische voetzorg.",
     "Klikbare WhatsApp- en belknop, en Nederlands/Engels met één knop.",
     "Snelle, moderne uitstraling op telefoon, tablet en computer."]
def telhref(tel):
    if not tel: return "#contact"
    dd=tel.replace("-","").replace(" ","")
    if dd.startswith("06"): dd="+31"+dd[1:]
    return "tel:"+dd
added=0
for p in quals:
    slug=p["slug"]
    if slug in existing: continue
    existing.add(slug); added+=1
    plaats=p["plaats"]; tel=p.get("tel",""); niche=p["niche"]
    td = tel if tel else "Bel of app ons"; th=telhref(tel)
    aanhef = ("Hoi %s,"%p["eigenaar"]) if p.get("eigenaar") else "Hoi,"
    demo="https://%s.demo.brabantdigital.nl"%slug
    sb.append({"bedrijf":p["bedrijf"],"kort":p["kort"],"slug":slug,"plaats":plaats,
      "tel_display":td,"tel_href":th,"niche":niche,
      "content":{"eigenaar":p.get("eigenaar",""),"verhaal":p["verhaal"],"specialisaties":p["spec"],
        "certificering":p.get("cert",[]),"tarieven":[],"openingstijden":"Op afspraak","reviews":[]},
      "email":p.get("email",""),"social":p.get("social",""),"taal":"nl"})
    cl.append({"bedrijf":p["bedrijf"],"niche":NL[niche],"regio":p.get("regio","Limburg"),"plaats":plaats,
      "status":"demo","score":4,"werkdag":WERKDAG,"aangemaakt":AANGEMAAKT,"laatste_post":p.get("laatste_post",""),"demo_url":demo,
      "waarom":p["waarom"],"fouten":[p["waarom"].rstrip('.')],"contact":(tel or (p.get("social") and "Alleen "+p["social"]) or "(contact nog nodig)"),
      "bron":None,"social":p.get("social",""),"telefoon":tel,"land":"NL","taal":"nl"})
    pr.append({"bedrijf":p["bedrijf"],"aanhef":aanhef,"plaats":plaats,"email":p.get("email",""),
      "status":"concept","demo_url":demo,"deadline":DEADLINE,
      "onderwerp":"Ik heb alvast een website voor %s gemaakt (kijk even mee)"%p["bedrijf"],
      "compliment":"Ik kwam %s tegen toen ik in %s naar %s zocht — en het viel me op dat een eigen, moderne website nog ontbreekt of wat verouderd is."%(p["bedrijf"],plaats,WORD[niche]),
      "gratis_tip":TIP[niche],"verbeteringen":benefits(niche,plaats),"land":"NL","taal":"nl"})
json.dump(sb,open(SB,'w'),ensure_ascii=False,indent=1)
json.dump(cl,open(CL,'w'),ensure_ascii=False,indent=1)
json.dump(pr,open(PR,'w'),ensure_ascii=False,indent=1)
for f in (SB,CL,PR): json.load(open(f))
print("added",added,"| salons",len(sb),"clients",len(cl),"prospects",len(pr))
