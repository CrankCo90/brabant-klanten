import json
cl=json.load(open('dashboard/clients.json'))
sb=json.load(open('_workflow/salons-batch1.json'))
names={c['bedrijf'].strip().lower() for c in cl}
slugs={s['slug'] for s in sb}

quals=[
 {"bedrijf":"Melly's Trimsalon","kort":"Melly's Trimsalon","slug":"mellys-trimsalon-gorredijk","plaats":"Gorredijk","regio":"Friesland","niche":"hond","tel":"06-38362442","social":"","email":"","eigenaar":"",
  "verhaal":"Bij Melly's Trimsalon in Gorredijk kunt u terecht voor de volledige vachtverzorging van alle ras- en rasloze honden. Er is veel aandacht en zorg voor elke hond, en op verzoek wordt uw viervoeter zelfs aan huis getrimd.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimskuorre de Dôlle","kort":"Trimskuorre de Dôlle","slug":"trimskuorre-de-dolle-triemen","plaats":"Triemen","regio":"Friesland","niche":"hond","tel":"06-27521354","social":"","email":"","eigenaar":"",
  "verhaal":"Trimskuorre de Dôlle in Triemen verzorgt de vacht van honden, groot en klein, met vakkennis en geduld. De salon is gespecialiseerd in spaniëlvachten, ruwharige rassen en plukwerk.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon DOKS","kort":"Trimsalon DOKS","slug":"trimsalon-doks-dokkum","plaats":"Dokkum","regio":"Friesland","niche":"hond","tel":"06-47871226","social":"","email":"","eigenaar":"",
  "verhaal":"Trimsalon DOKS in Dokkum biedt een complete vachtverzorging voor uw hond, met indien gewenst een handige haal- en brengservice. Alles gebeurt op afspraak, ook 's avonds en in het weekend.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Benzel","kort":"Trimsalon Benzel","slug":"trimsalon-benzel-st-jacobiparochie","plaats":"St.-Jacobiparochie","regio":"Friesland","niche":"hond","tel":"06-13568643","social":"","email":"","eigenaar":"",
  "verhaal":"Bij Trimsalon Benzel in St.-Jacobiparochie is elke hond, ras of geen ras, van harte welkom. Bij het eerste bezoek volgt persoonlijk advies, zodat elke vacht precies de behandeling krijgt die past bij de hond en uw wensen.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Furry Buddy","kort":"Trimsalon Furry Buddy","slug":"trimsalon-furry-buddy-hoogezand","plaats":"Hoogezand","regio":"Groningen","niche":"hond","tel":"06-13924265","social":"","email":"","eigenaar":"Irina",
  "verhaal":"Trimsalon Furry Buddy in Hoogezand verzorgt honden op een rustige, vachtvriendelijke manier zonder dwangmiddelen of houdgrepen. Geduld, rust en vertrouwen staan voorop, zodat uw hond zich veilig en ontspannen voelt.",
  "spec":["Knippen & scheren","Wassen & föhnen","Effileren","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon JS","kort":"Trimsalon JS","slug":"trimsalon-js-kropswolde","plaats":"Kropswolde","regio":"Groningen","niche":"hond","tel":"06-83198017","social":"","email":"","eigenaar":"",
  "verhaal":"Trimsalon JS in Kropswolde is er voor het trimmen en verzorgen van de vacht van uw hond. Een kleinschalige salon waar elke hond rustig en met aandacht behandeld wordt, op afspraak en ook in het weekend.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
]
out=[]
for q in quals:
    if q['bedrijf'].strip().lower() in names: print("SKIP name dup:",q['bedrijf']); continue
    if q['slug'] in slugs: print("SKIP slug dup:",q['slug']); continue
    # safety: ensure 06 mobile or social
    t=q.get('tel','').replace('-','').replace(' ','')
    if not (t.startswith('06') or q.get('social') or q.get('email')):
        print("SKIP no-contact:",q['bedrijf']); continue
    out.append(q)
json.dump(out, open('new_quals.json','w'), ensure_ascii=False, indent=1)
print("qualified:",len(out))
