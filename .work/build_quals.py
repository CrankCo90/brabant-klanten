import json
quals = [
 {"bedrijf":"Ina's Walk Out","kort":"Ina's Walk Out","slug":"inas-walk-out-westerlee","plaats":"Westerlee","regio":"Groningen","niche":"hond",
  "tel":"06-28027000","social":"FB","email":"","eigenaar":"Ina",
  "verhaal":"Ina's Walk Out in Westerlee is een trimsalon waar alle honden, van groot tot klein, welkom zijn. De salon beschikt over moderne apparatuur en er wordt bewust rust gecreeerd, want het welzijn van de hond staat altijd voorop.",
  "spec":["Wassen","Knippen","Ontwollen","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen Facebook)."},
 {"bedrijf":"Hondenkapsalon Poedelpret","kort":"Poedelpret","slug":"hondenkapsalon-poedelpret-zwolle","plaats":"Zwolle","regio":"Overijssel","niche":"hond",
  "tel":"06-26423022","social":"","email":"","eigenaar":"",
  "verhaal":"Hondenkapsalon Poedelpret in Zwolle is een kleine, gediplomeerde trimsalon met veel aandacht voor uw wensen en het welzijn van de hond. Er wordt een-op-een en huid- en vachtvriendelijk gewerkt, met een persoonlijk behandelplan voor elke hond.",
  "spec":["Wassen","Knippen","Effileren","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Knip & Soapy Trimsalon","kort":"Knip & Soapy","slug":"knip-en-soapy-apeldoorn","plaats":"Apeldoorn","regio":"Gelderland","niche":"hond",
  "tel":"06-15003043","social":"","email":"","eigenaar":"Charlotte",
  "verhaal":"Knip & Soapy is een mooie, moderne trimsalon in de Apeldoornse wijk Zevenhuizen, waar alle honden welkom zijn, ook de grotere rassen. Iedere hond verdient een goede trimbeurt en krijgt hier rustig de aandacht die hij verdient.",
  "spec":["Wassen","Knippen","Effileren","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon The Generation's","kort":"The Generation's","slug":"trimsalon-the-generations-voorthuizen","plaats":"Voorthuizen","regio":"Gelderland","niche":"hond",
  "tel":"06-43988336","social":"","email":"","eigenaar":"",
  "verhaal":"Trimsalon The Generation's in Voorthuizen biedt complete vachtverzorging en is gespecialiseerd in doodles, al zijn alle honden, groot of klein, van harte welkom. Er wordt rustig en alleen op afspraak gewerkt.",
  "spec":["Wassen","Knippen","Plukken","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Pluk","kort":"Trimsalon Pluk","slug":"trimsalon-pluk-apeldoorn","plaats":"Apeldoorn","regio":"Gelderland","niche":"hond",
  "tel":"06-30503994","social":"","email":"","eigenaar":"",
  "verhaal":"Trimsalon Pluk in Apeldoorn verzorgt met liefde voor de hond de complete vacht: van wassen en knippen tot plukken, scheren en nagels knippen. Elke hond krijgt een rustige, vakkundige behandeling.",
  "spec":["Wassen","Knippen","Plukken","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Happy Hound Hondentrimsalon","kort":"Happy Hound","slug":"happy-hound-apeldoorn","plaats":"Apeldoorn","regio":"Gelderland","niche":"hond",
  "tel":"06-17504124","social":"","email":"","eigenaar":"",
  "verhaal":"Happy Hound in Apeldoorn staat voor 'Happy Hounds, Happy People': een vrolijke trimsalon waar uw hond met aandacht en plezier wordt verzorgd. Alle rassen zijn welkom voor een complete vachtbehandeling.",
  "spec":["Wassen","Knippen","Plukken","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Manon's Trimsalon","kort":"Manon's Trimsalon","slug":"manons-trimsalon-biddinghuizen","plaats":"Biddinghuizen","regio":"Flevoland","niche":"hond",
  "tel":"06-17044417","social":"","email":"","eigenaar":"Manon",
  "verhaal":"Manon's Trimsalon in Biddinghuizen is een kleinschalige, gediplomeerde trimsalon met geduldige, een-op-een vachtverzorging voor honden. Er wordt rustig gewerkt met volop aandacht voor elke hond.",
  "spec":["Wassen","Knippen","Plukken","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Hondensalon Cell","kort":"Hondensalon Cell","slug":"hondensalon-cell-dronten","plaats":"Dronten","regio":"Flevoland","niche":"hond",
  "tel":"06-52363058","social":"","email":"","eigenaar":"",
  "verhaal":"Hondensalon Cell in Dronten verzorgt alle rassen en kruisingen met een complete trimbehandeling. Uw hond wordt rustig en vakkundig behandeld voor een mooi en verzorgd resultaat.",
  "spec":["Wassen","Knippen","Scheren","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
 {"bedrijf":"Trimsalon Van Chayoek","kort":"Van Chayoek","slug":"trimsalon-van-chayoek-arnhem","plaats":"Arnhem","regio":"Gelderland","niche":"hond",
  "tel":"06-81292344","social":"","email":"","eigenaar":"",
  "verhaal":"Trimsalon Van Chayoek in Arnhem is een honden- en kattentrimsalon voor de complete vachtverzorging van uw huisdier. Elke hond krijgt een vakkundige en rustige behandeling.",
  "spec":["Wassen","Knippen","Plukken","Nagels knippen"],"cert":[],"waarom":"Geen eigen website (alleen vermelding/06)."},
]
json.dump(quals, open('.work/new_quals.json','w'), ensure_ascii=False, indent=1)
sb=json.load(open('_workflow/salons-batch1.json')); existing={s['slug'] for s in sb}
print("count:", len(quals))
bad=[q['slug'] for q in quals if q['slug'] in existing]
print("slug collisions:", bad)
