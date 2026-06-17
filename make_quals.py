import json,re
sb=json.load(open('_workflow/salons-batch1.json'))
existing_slugs={s['slug'] for s in sb}

def kebab(s):
    s=s.lower()
    s=s.replace("&","en").replace("'","").replace('"','')
    s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
    return s

def slugify(bedrijf,plaats):
    base=kebab(bedrijf)+'-'+kebab(plaats)
    return base

# bedrijf, plaats, regio, tel, social, eigenaar, verhaal, spec(list4)
SPEC_A=["Wassen, föhnen en borstelen","Knippen en scheren op maat","Plukken en effileren","Nagels knippen en oren verzorgen"]
SPEC_B=["Volledige vachtverzorging","Trimmen van alle hondenrassen","Wassen en ontwollen","Persoonlijke aandacht per hond"]
SPEC_C=["Trimmen van kleine en grote honden","Wassen, knippen en scheren","Plukvachten en rasspecifiek trimwerk","Nagels en oren verzorgen"]

data=[
 ("Trimsalon Rylana","Ter Apel","Groningen","06-22253276","","",
  "Trimsalon Rylana in Ter Apel verzorgt grote en kleine honden met zorg voor een mooie, gezonde vacht.",SPEC_C),
 ("Trimsalon Onyx","Westerlee","Groningen","06-22141467","","Ingrid Kruize",
  "Ingrid Kruize is een gepassioneerde hondentrimster in Westerlee met aandacht voor vachtverzorging en voedingsadvies.",SPEC_B),
 ("Trimsalon Furry Choice","Hoogeveen","Drenthe","06-38402069","","",
  "Bij Trimsalon Furry Choice in Hoogeveen zijn honden, katten en knaagdieren welkom voor een professionele trimbehandeling.",SPEC_A),
 ("Trimsalon Caja","Norg","Drenthe","06-46025443","","",
  "Trimsalon Caja in Norg bestaat al ruim achttien jaar en behandelt elk dier geduldig en vakkundig.",SPEC_C),
 ("Trimsalon Lilian Belga","Kiel-Windeweer","Groningen","06-13085953","","",
  "Trimsalon Lilian Belga verzorgt het plukken, wassen, knippen en scheren van alle honden, klein en groot.",SPEC_A),
 ("Hondentrimsalon Joan","Boksum","Friesland","06-12610137","","",
  "Hondentrimsalon Joan in Boksum trimt honden en katten op een dier- en vachtvriendelijke manier, met bijna 25 jaar ervaring.",SPEC_C),
 ("Honden en kattentrimsalon Chica Bella","Oosterstreek","Friesland","06-51669539","","",
  "Chica Bella in Oosterstreek werkt uitsluitend op afspraak en neemt ruim de tijd voor elke hond en kat.",SPEC_B),
 ("Trimsalon Knippe en Waskje","Oosterstreek","Friesland","06-27908291","","Patricia Siem",
  "Patricia Siem runt Trimsalon Knippe & Waskje in Oosterstreek, waar alle hondenrassen welkom zijn voor een verwenmoment.",SPEC_B),
 ("Trimsalon Kwiebus","Peize","Drenthe","06-46688680","","Jolinde Bos",
  "Jolinde Bos maakte van haar liefde voor honden haar beroep en verzorgt in Peize de vacht van alle rassen.",SPEC_B),
 ("Trimsalon Juffrouw Jansen","De Bult","Overijssel","06-57202095","","",
  "Bij Trimsalon Juffrouw Jansen in De Bult is uw hond in handen van een gediplomeerde trimster met persoonlijke aandacht.",SPEC_A),
 ("Trimsalon 't Vossie","Zandeweer","Groningen","06-12940839","","Tamara de Vos",
  "Tamara de Vos trimt sinds 1999 met passie honden, katten en konijnen in haar salon in Zandeweer.",SPEC_C),
 ("Trimsalon CreaDog","Epe","Gelderland","06-18439059","","",
  "Bij Trimsalon CreaDog in Epe wordt elke hond één op één verzorgd met veel geduld en aandacht.",SPEC_A),
 ("Hondensalon BiDo","Olst","Overijssel","06-28453484","","",
  "Hondensalon BiDo verzorgt honden met liefde en geduld en werkt ergonomisch in een rustige salon.",SPEC_B),
 ("Honden- en kattentrimsalon Vitalidad","Nijverdal","Overijssel","06-36149458","","",
  "Vitalidad in Nijverdal is een gediplomeerde honden- en kattentrimsalon waar het welzijn van het dier voorop staat.",SPEC_B),
 ("Trimsalon Trudy","Zwolle","Overijssel","06-30604486","","Trudy",
  "Bij Trimsalon Trudy in Zwolle wordt elke hond persoonlijk en met alle aandacht getrimd voor een mooi resultaat.",SPEC_A),
 ("DE trimsalon Meppel","Meppel","Drenthe","06-23038299","","",
  "DE trimsalon Meppel is de geknipte plek in het centrum van Meppel, met aparte, rustige trimruimtes.",SPEC_C),
 ("Honden en Katten Trimsalon de Aandacht","Dronten","Flevoland","06-40119182","","",
  "Trimsalon de Aandacht in Dronten heet elke hond, kat en konijn welkom in een modern ingerichte salon.",SPEC_B),
]

quals=[]
seen=set()
for bedrijf,plaats,regio,tel,social,eig,verhaal,spec in data:
    slug=slugify(bedrijf,plaats)
    # ensure unique
    s=slug; i=2
    while s in existing_slugs or s in seen:
        s=slug+'-'+str(i); i+=1
    seen.add(s)
    quals.append({
      "bedrijf":bedrijf,
      "kort":bedrijf,
      "slug":s,
      "plaats":plaats,
      "regio":regio,
      "niche":"hond",
      "tel":tel,
      "social":social,
      "email":"",
      "eigenaar":eig,
      "verhaal":verhaal,
      "spec":spec,
      "cert":[],
      "waarom":"Zelfstandige hondentrimsalon in %s; gebaat bij een moderne, goed vindbare website met online afspraken."%plaats
    })

json.dump(quals,open('/tmp/bkrun/new_quals.json','w'),ensure_ascii=False,indent=1)
print("quals:",len(quals))
for q in quals: print(q['slug'],'|',q['tel'],'|',q.get('social'))
