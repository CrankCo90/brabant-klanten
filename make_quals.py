import json
cl=json.load(open('dashboard/clients.json'))
sb=json.load(open('_workflow/salons-batch1.json'))
names={c['bedrijf'].strip().lower() for c in cl}
slugs={s['slug'] for s in sb}

quals=[
 {"bedrijf":"Manon's Trimsalon","kort":"Manon's Trimsalon","slug":"manons-trimsalon-biddinghuizen","plaats":"Biddinghuizen","regio":"Flevoland","niche":"hond","tel":"06-17044417","social":"","email":"","eigenaar":"Manon",
  "verhaal":"Bij Manon's Trimsalon in Biddinghuizen wordt elke hond rustig en met geduld verzorgd, één-op-één en met persoonlijke aandacht. Een gediplomeerd trimster zorgt voor een mooi en verzorgd resultaat.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Hondensalon Cell","kort":"Hondensalon Cell","slug":"hondensalon-cell-dronten","plaats":"Dronten","regio":"Flevoland","niche":"hond","tel":"06-52363058","social":"","email":"","eigenaar":"",
  "verhaal":"Hondensalon Cell in Dronten trimt alle rassen en kruisingen met zorg en aandacht. Iedere hond krijgt een complete en vakkundige vachtverzorging op afspraak.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Honden trimsalon De Stijlvolle 4-voeter","kort":"De Stijlvolle 4-voeter","slug":"trimsalon-de-stijlvolle-4voeter-almere","plaats":"Almere","regio":"Flevoland","niche":"hond","tel":"06-24656907","social":"","email":"","eigenaar":"",
  "verhaal":"Honden trimsalon De Stijlvolle 4-voeter in Almere neemt alle tijd voor uw hond, zonder lopendebandwerk. Elke hond wordt individueel en in een rustige sfeer verzorgd, met aandacht voor puppy's.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Hondentrimsalon Almere Buiten","kort":"Hondentrimsalon Almere Buiten","slug":"hondentrimsalon-almere-buiten","plaats":"Almere","regio":"Flevoland","niche":"hond","tel":"06-29281184","social":"","email":"","eigenaar":"",
  "verhaal":"Bij Hondentrimsalon Almere Buiten zijn alle hondenrassen en rasloze honden welkom. De vacht van uw hond wordt vakkundig en met aandacht verzorgd, ook 's avonds en in het weekend.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimmerman","kort":"Trimmerman","slug":"trimmerman-zuidhorn","plaats":"Zuidhorn","regio":"Groningen","niche":"hond","tel":"06-45422888","social":"FB","email":"","eigenaar":"Violetta",
  "verhaal":"Trimmerman in Zuidhorn verzorgt honden op een rustige, stressvrije manier met professionele, anti-allergische producten. Snel en zorgvuldig ontharen en een complete vachtverzorging horen tot de mogelijkheden.",
  "spec":["Knippen & scheren","Wassen & föhnen","Ontharen/deshedding","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen Facebook)."},
 {"bedrijf":"Trimsalon Mon Ami","kort":"Trimsalon Mon Ami","slug":"trimsalon-mon-ami-norg","plaats":"Norg","regio":"Drenthe","niche":"hond","tel":"06-50830692","social":"FB","email":"","eigenaar":"",
  "verhaal":"Trimsalon Mon Ami in Norg is een vertrouwde salon met een gediplomeerd trimster die ook kennis heeft van hondengedrag. De hond moet zich veilig voelen, daar wordt rustig en geduldig aan gewerkt.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen Facebook)."},
 {"bedrijf":"Trimsalon Josiena","kort":"Trimsalon Josiena","slug":"trimsalon-josiena-winsum","plaats":"Winsum","regio":"Groningen","niche":"hond","tel":"06-22724974","social":"","email":"","eigenaar":"Josiena",
  "verhaal":"Bij Trimsalon Josiena in Winsum kunt u terecht met hond, kat, konijn en cavia. Elk dier wordt met alle liefde en geduld behandeld; u bent als eigenaar van harte welkom om erbij te blijven.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Annet's Trimsalon","kort":"Annet's Trimsalon","slug":"annets-trimsalon-de-punt","plaats":"De Punt","regio":"Drenthe","niche":"hond","tel":"06-42748108","social":"","email":"","eigenaar":"Annet",
  "verhaal":"Annet's Trimsalon in De Punt is een gezellige, professionele salon waar alle honden, groot en klein, welkom zijn. Er wordt rustig de tijd genomen, alles op afspraak en met persoonlijke aandacht.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Karin Solle","kort":"Trimsalon Karin Solle","slug":"karin-solle-tolbert","plaats":"Tolbert","regio":"Groningen","niche":"hond","tel":"06-39545132","social":"","email":"","eigenaar":"Karin",
  "verhaal":"Bij Trimsalon Karin Solle in Tolbert kunt u terecht voor een volledige vachtverzorging, maar ook voor alleen wassen of nagels knippen. Er is zelfs een gratis puppy-uurtje zodat jonge honden rustig kunnen wennen.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Doggy's Delight","kort":"Trimsalon Doggy's Delight","slug":"trimsalon-doggys-delight-smilde","plaats":"Smilde","regio":"Drenthe","niche":"hond","tel":"06-19830556","social":"FB","email":"","eigenaar":"",
  "verhaal":"Trimsalon Doggy's Delight in Smilde wordt gerund door een gediplomeerd trimster met jarenlange ervaring, gespecialiseerd in onder meer terriërs, poedels en doodles. Er is een gratis ophaal- en terugbrengservice in de omgeving.",
  "spec":["Knippen & scheren","Wassen & föhnen","Plukken/trimmen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen Facebook)."},
]

out=[]
for q in quals:
    if q['bedrijf'].strip().lower() in names:
        print("SKIP name dup:", q['bedrijf']); continue
    if q['slug'] in slugs:
        print("SKIP slug dup:", q['slug']); continue
    out.append(q)
json.dump(out, open('/tmp/bk_1781650429/new_quals.json','w'), ensure_ascii=False, indent=1)
# also place at /tmp/new_quals.json expected by add-prospects.py
import shutil
print("qualified:", len(out))
