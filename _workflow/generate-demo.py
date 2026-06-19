#!/usr/bin/env python3
"""Genereert per salon een kiesdemo op basis van het Scott-sjabloon, met:
- eigen merknaam/plaats/telefoon
- eigen foto's (bij 2+ echte foto's), anders AI
- 'Over ons + Tarieven'-sectie met echte content (in de kleuren van elk design)
- Cal-planner popup op de 'Afspraak maken'-knoppen
"""
import json, re, random
import urllib.parse as _ul
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "hondentrimsalonscott" / "03-designs"
FILES = ["index.html"] + [f"previews/design-{i:02d}.html" for i in range(1,11)]
salons = json.loads((ROOT/"_workflow"/"salons-batch1.json").read_text(encoding="utf-8"))
import sys as _sys
_sys.path.insert(0, str(ROOT/"_workflow"))
import gen_premium as _gp


_pp = ROOT/"_workflow"/"ai-pool.json"
POOL = json.loads(_pp.read_text(encoding="utf-8")) if _pp.exists() else {"clean":[],"dirty":[],"salon":[]}
POOL_OK = all(len(POOL.get(k,[]))>0 for k in ("clean","dirty","salon"))
AI_BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/"
AI_URLS=[AI_BASE+x for x in ["hf_20260613_085111_ed4bc4a1-2b25-4d9e-9d32-c845d82e43d5.png","hf_20260613_085111_f52a0629-6c32-41b2-b8dd-fef7eedcac53.png","hf_20260613_085113_6fec380b-3cdc-4be3-b70c-9d7c43c23dc1.png","hf_20260613_085115_b87c0cc0-c208-4c3b-8852-8bca6fcdcb98.png","hf_20260613_085116_7544c5ba-9d93-484b-bb04-5d7b6ab28cb3.png","hf_20260613_085118_a274f992-0d24-45ad-a2c6-c057fd5ec738.png","hf_20260613_085120_63fb879f-0316-4081-b785-cbc92515996b.png","hf_20260613_085121_b800ad99-b6c5-4d3b-acc0-2940c43fa059.png"]]
ROLES=["clean","clean","salon","dirty","clean","salon","clean","salon"]
def pick_pool(slug):
    rnd=random.Random("img-"+slug)
    sh={k:rnd.sample(POOL[k],len(POOL[k])) for k in ("clean","dirty","salon")}
    idx={"clean":0,"dirty":0,"salon":0}; out=[]
    for r in ROLES:
        l=sh[r]; out.append(l[idx[r]%len(l)]); idx[r]+=1
    return out

# ---- Niche: nagelstudio's (hergebruikt het trimsalon-template met nagel-copy + nagelbeelden) ----
# 8 nagelfoto's (Pexels, geverifieerd) in dezelfde index-vololgorde/rollen als AI_URLS:
# 0,1 clean (hero/finished)  2 salon-interieur  3 'before' (kale nagels, slider)  4 clean 'after'
# 5 salon (werk)  6 clean (lifestyle)  7 salon (werk)
_PX = "https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg?auto=compress&cs=tinysrgb&w=1280"
NAIL_IMG = [_PX%(i,i) for i in ["2268404","3557600","6135674","3997388","3997381","4677846","2600287","7446919"]]

# Decoratieve hond-emoji's -> nagel-emoji's (quiz design-09)
NAIL_EMOJI = [("\U0001F415‍\U0001F9BA","\U0001F485"),("\U0001F415","\U0001F485"),
    ("\U0001F9AE","\U0001F485"),("\U0001F429","✨"),("\U0001F43E","\U0001F485"),
    ("\U0001F9F9","\U0001F3A8"),("\U0001F98A","\U0001F48E")]

# Ordered replacements (combos eerst, dan hele zinnen, dan losse woorden). Toegepast als niche=="nagels".
NAIL_MAP = [
 # --- calculator (design-08) + quiz (design-09) opties/combo's: eerst, want ze bevatten substrings ---
 ('data-en="Small">Klein','data-en="Short">Kort'),
 ('data-en="Large">Groot','data-en="Long">Lang'),
 ('data-en="Short / smooth">Kort / glad','data-en="Gel polish">Gellak'),
 ('data-en="Long / doodle">Lang / doodle','data-en="BIAB">BIAB'),
 ('data-en="Wire-haired">Ruwharig','data-en="Acrylics">Acryl'),
 ('data-en="Double coat">Double coat','data-en="PolyGel">PolyGel'),
 ('data-en="Wash & blow-dry">Wassen &amp; föhnen','data-en="Gel polish">Gellak'),
 ('data-en="Full grooming">Volledige trimbeurt','data-en="Full set">Volledige set'),
 ('data-en="Tidy-up">Bijwerken','data-en="Refill">Bijwerken'),
 ('data-en="Short & smooth">Kort &amp; glad','data-en="Gel polish">Gellak'),
 ('data-rec="Wassen & föhnen|Wash & blow-dry"','data-rec="Gellak|Gel polish"'),
 ('data-rec="Volledige trimbeurt|Full grooming"','data-rec="Volledige set|Full set"'),
 ('data-rec="Plukbeurt (ruwharig)|Hand-stripping"','data-rec="BIAB-set|BIAB set"'),
 ('data-rec="Ontwol-behandeling|De-shed treatment"','data-rec="Acrylset|Acrylic set"'),
 ('recVal=[\'Volledige trimbeurt\',\'Full grooming\']','recVal=[\'Volledige set\',\'Full set\']'),
 # --- hele zinnen (EN) ---
 ('Certified dog groomer for all breeds — from doodle to Pomeranian. Book online and your dog is pampered in all peace and quiet.',
  'Certified nail stylist for every look — from a natural manicure to full acrylics. Book online and enjoy your nails in all peace and quiet.'),
 ('Certified dog grooming salon in Amsterdam Osdorp. All breeds, groomed with love and patience.',
  'Certified nail studio in Amsterdam Osdorp. Every style, done with love and precision.'),
 ('Certified groomer for all breeds. Book online — your dog is pampered in calm, professional hands.',
  'Certified nail stylist for every style. Book online — your nails in calm, professional hands.'),
 ('Certified groomer for all breeds. Combine the grooming with a walk around the Sloterplas — your dog comes back glowing.',
  'Certified nail stylist for every style. Combine your appointment with a coffee nearby — you leave glowing.'),
 ('Certified groomer for all breeds. Calm, careful and always with an eye for your dog.',
  'Certified nail stylist for every style. Calm, careful and always with an eye for you.'),
 ('A certified groomer who treats every coat as a craft. All breeds, with love and patience.',
  'A certified nail stylist who treats every set as a craft. Every style, with love and precision.'),
 ('Every dog gets time and attention. No rush, no stress — just patient, expert care from a certified groomer who keeps learning.',
  'Every client gets time and attention. No rush, no stress — just patient, expert care from a certified nail stylist who keeps learning.'),
 ('Diploma in hand and re-trained every year — most recently at the Purina Pro Plan symposium 2026. Your dog benefits from the latest insights in coat and skin care.',
  'Diploma in hand and re-trained every year — with the latest gel and nail techniques. You benefit from the newest insights in nail and skin care.'),
 ('A personal grooming salon. Love, patience and craftsmanship — for every coat, every breed.',
  'A personal nail studio. Love, patience and craftsmanship — for every set, every style.'),
 ('A gentle wash and careful drying, tailored to the coat.','A gentle prep and careful finish, tailored to your nails.'),
 ('Trimming, stripping or clipping — exactly what the breed needs.','Gel, BIAB or acrylics — exactly what your nails need.'),
 ('A relaxed first visit so grooming stays fun for life.','A relaxed first visit so your appointments stay something to look forward to.'),
 ('A spa day for your dog — drag the slider and watch a scruffy coat turn into a clean, fluffy result.',
  'A spa moment for your hands — drag the slider and watch worn nails turn into a fresh, flawless result.'),
 ('Hand-stripping that keeps the coat healthy and true to type.','Careful prep that keeps your natural nails healthy and strong.'),
 ('Gentle products, tailored to skin and coat.','Gentle products, tailored to skin and nails.'),
 ('Breed-true finish, neat and even.','Flawless finish, neat and even.'),
 ('Expert handling of demanding coats, with patience.','Expert handling of tricky nails, with patience.'),
 ("No more guessing. Pick your dog's size, coat and treatment and see a price indication right away.",
  'No more guessing. Pick your length, technique and treatment and see a price indication right away.'),
 ("* Indication only — the final price is set together after seeing your dog's coat.",
  '* Indication only — the final price is set together after seeing your nails.'),
 ('No more calling during grooming. Pick a treatment, a day and a time — done.',
  'No more calling during work. Pick a treatment, a day and a time — done.'),
 ('All breeds welcome, groomed with love and patience.','Every style welcome, done with love and precision.'),
 ('Book online or call directly. Your dog will thank you.','Book online or call directly. Your nails will thank you.'),
 ('Diploma plus yearly training. Specialised in doodles, wire-haired and double coats.',
  'Diploma plus yearly training. Specialised in gel polish, BIAB and acrylics.'),
 ('She trims our doodle with so much patience. He actually loves going now — and he comes back gorgeous.',
  'She does my nails with so much patience and care. I actually look forward to every visit — and they always look gorgeous.'),
 # --- hele zinnen (NL) ---
 ('Gediplomeerd hondentrimster voor alle rassen — van doodle tot pomeriaan. Boek online en uw hond wordt in alle rust verwend.',
  'Gediplomeerd nagelstyliste voor elke look — van een natuurlijke manicure tot complete acryl. Boek online en uw nagels worden in alle rust verwend.'),
 ('Gediplomeerde hondentrimsalon in Amsterdam Osdorp. Alle rassen, met liefde en geduld getrimd.',
  'Gediplomeerde nagelstudio in Amsterdam Osdorp. Elke stijl, met liefde en precisie gelakt.'),
 ('Gediplomeerd trimster voor alle rassen. Boek online — uw hond wordt in alle rust en met vakmanschap verwend.',
  'Gediplomeerd nagelstyliste voor elke stijl. Boek online — uw nagels worden in alle rust en met vakmanschap verwend.'),
 ('Gediplomeerd trimster voor alle rassen. Combineer de trimbeurt met een rondje Sloterplas — uw hond komt stralend terug.',
  'Gediplomeerd nagelstyliste voor elke stijl. Combineer uw afspraak met een koffie in de buurt — u gaat stralend naar huis.'),
 ('Gediplomeerd trimster voor alle rassen. Rustig, zorgvuldig en altijd met oog voor uw hond.',
  'Gediplomeerd nagelstyliste voor elke stijl. Rustig, zorgvuldig en altijd met oog voor u.'),
 ('Een gediplomeerd trimster die elke vacht als vakwerk behandelt. Alle rassen, met liefde en geduld.',
  'Een gediplomeerd nagelstyliste die elke set als vakwerk behandelt. Elke stijl, met liefde en geduld.'),
 ('Elke hond krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd trimster die blijft bijscholen.',
  'Elke klant krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd nagelstyliste die blijft bijscholen.'),
 ('Gediplomeerd én jaarlijks bijgeschoold — onlangs nog op het Purina Pro Plan-symposium 2026. Uw hond profiteert van de nieuwste inzichten in vacht- en huidverzorging.',
  'Gediplomeerd én jaarlijks bijgeschoold — met de nieuwste gel- en nageltechnieken. U profiteert van de nieuwste inzichten in nagel- en huidverzorging.'),
 ('Gediplomeerd plus jaarlijkse bijscholing. Gespecialiseerd in doodles, ruwharig en double coats.',
  'Gediplomeerd plus jaarlijkse bijscholing. Gespecialiseerd in gellak, BIAB en acryl.'),
 ('Een persoonlijke trimsalon. Liefde, geduld en vakmanschap — voor elke vacht, elk ras.',
  'Een persoonlijke nagelstudio. Liefde, geduld en vakmanschap — voor elke set, elke stijl.'),
 ('Een zachte wasbeurt en zorgvuldig drogen, afgestemd op de vacht.',
  'Een zachte voorbereiding en strakke afwerking, afgestemd op uw nagels.'),
 ('Knippen, plukken of scheren — precies wat het ras nodig heeft.',
  'Gellak, BIAB of acryl — precies wat uw nagels nodig hebben.'),
 ('Een ontspannen eerste keer zodat trimmen een leven lang leuk blijft.',
  'Een ontspannen eerste keer zodat uw afspraken iets blijven om naar uit te kijken.'),
 ('Met de hand plukken zodat de vacht gezond en raszuiver blijft.',
  'Zorgvuldige voorbereiding zodat uw natuurlijke nagel gezond en sterk blijft.'),
 ('Een spa-dag voor uw hond — sleep de slider en zie een verwaarloosde vacht veranderen in een schoon, donzig resultaat.',
  'Een spa-moment voor uw handen — sleep de slider en zie versleten nagels veranderen in een fris, perfect resultaat.'),
 ('Vakkundige aanpak van veeleisende vachten, met geduld.','Vakkundige aanpak van lastige nagels, met geduld.'),
 ('Zachte producten, afgestemd op huid en vacht.','Zachte producten, afgestemd op huid en nagels.'),
 ('Alle rassen welkom, met liefde en geduld getrimd.','Elke stijl welkom, met liefde en precisie gelakt.'),
 ('Geen giswerk meer. Kies grootte, vacht en behandeling van uw hond en zie direct een richtprijs.',
  'Geen giswerk meer. Kies lengte, techniek en behandeling en zie direct een richtprijs.'),
 ('Niet meer bellen tijdens het trimmen. Kies een behandeling, een dag en een tijd — klaar.',
  'Niet meer bellen tijdens het werk. Kies een behandeling, een dag en een tijd — klaar.'),
 ('Ze trimt onze doodle met zoveel geduld. Hij vindt het nu zelfs leuk — en hij komt er prachtig uit.',
  'Ze doet mijn nagels met zoveel geduld en aandacht. Ik kijk nu zelfs uit naar elke afspraak — en ze zien er altijd prachtig uit.'),
 # --- korte zinnen / labels (EN dan NL) ---
 ('Dog grooming · Amsterdam Osdorp','Nail studio · Amsterdam Osdorp'),
 ('Hondentrimsalon · Amsterdam Osdorp','Nagelstudio · Amsterdam Osdorp'),
 ('Groomed with love and patience','Styled with love and precision'),
 ('Met liefde en geduld getrimd','Met liefde en precisie gelakt'),
 ('Specialist in doodles, wire-haired and double coated.','Specialist in gel polish, BIAB and acrylics.'),
 ('Specialist in doodles, ruwharig en double coated.','Specialist in gellak, BIAB en acryl.'),
 ('Specialised in doodles, wire-haired & double coat','Specialised in gel, BIAB & acrylics'),
 ('Gespecialiseerd in doodles, ruwharig & double coat','Gespecialiseerd in gellak, BIAB & acryl'),
 ('A calm spa day for your dog','A calm spa moment for your hands'),
 ('Een rustige spa-dag voor uw hond','Een rustig spa-moment voor uw handen'),
 ('Honest coat advice, also for at home','Honest nail advice, also for at home'),
 ('Eerlijk vachtadvies, ook voor thuis','Eerlijk nageladvies, ook voor thuis'),
 ("Book your dog's spot online.",'Book your spot online.'),
 ('Boek online een plekje voor uw hond.','Boek online een plekje voor uzelf.'),
 ("Book your dog's session",'Book your session'),
 ('Boek de beurt van uw hond','Boek uw afspraak'),
 ("Book your dog's spot",'Book your spot'),
 ('Reserveer een plekje voor uw hond','Reserveer een plekje voor uzelf'),
 ('Expertly groomed, close to home','Expertly styled, close to home'),
 ('Vakkundig getrimd, vlak bij huis','Vakkundig gelakt, vlak bij huis'),
 ('Specialist care for every coat','Specialist care for every set'),
 ('Specialistische zorg voor elke vacht','Specialistische zorg voor elke set'),
 ('Wire-haired & stripping','BIAB & overlay'),
 ('Ruwharig &amp; plukken','BIAB &amp; overlay'),
 ('Doodles & double coat','Gel polish & acrylics'),
 ('Doodles &amp; double coat','Gellak &amp; acryl'),
 ('Plan a grooming session','Plan an appointment'),
 ('Plan een trimbeurt','Plan een afspraak'),
 ('Where your dog is <em>pampered</em>','Where your nails are <em>pampered</em>'),
 ('Waar uw hond wordt','Waar uw nagels worden'),
 ('Trimming, stripping or clipping','Gel, BIAB or acrylics'),
 ('Treat your dog','Treat yourself'),
 ('Verwen uw hond','Verwen uzelf'),
 ('Time and patience for every dog','Time and patience for every client'),
 ('Tijd en geduld voor elke hond','Tijd en geduld voor elke klant'),
 ('From doodle to Pomeranian','From natural to full set'),
 ('Van doodle tot pomeriaan','Van natuurlijk tot complete set'),
 ('The art of grooming','The art of nail styling'),
 ('De kunst van het trimmen','De kunst van het lakken'),
 ('Every coat, its own approach','Every set, its own approach'),
 ('Elke vacht, eigen aanpak','Elke set, eigen aanpak'),
 ('What does grooming cost?','What does a set cost?'),
 ('Wat kost een trimbeurt?','Wat kost een set?'),
 ('Which treatment suits your dog?','Which treatment suits you?'),
 ('Welke behandeling past bij uw hond?','Welke behandeling past bij u?'),
 ("What's your dog's size?",'What length do you want?'),
 ('Wat is de grootte van uw hond?','Welke lengte wilt u?'),
 ("What's the coat like?",'Which technique do you prefer?'),
 ('Wat voor vacht heeft uw hond?','Welke techniek heeft uw voorkeur?'),
 ('How often is your dog groomed?','How often do you get your nails done?'),
 ('Hoe vaak wordt uw hond getrimd?','Hoe vaak laat u uw nagels doen?'),
 ('Free trim advice','Free nail advice'),
 ('Gratis trimadvies','Gratis nageladvies'),
 ('Trim-quiz','Nagel-quiz'),
 ('Full grooming','Full set'),
 ('Volledige trimbeurt','Volledige set'),
 ('Wassen &amp; föhnen','Manicure &amp; gellak'),
 ('Wassen &amp; verzorgen','Manicure &amp; verzorging'),
 ('Knippen &amp; stylen','Vormen &amp; stylen'),
 ('Trim & style','Shape & style'),
 ('Plukbeurt ruwharig','BIAB-set'),
 ('1. Size of your dog','1. Nail length'),
 ('1. Grootte van uw hond','1. Nagellengte'),
 ('2. Coat type','2. Technique'),
 ('2. Vachttype','2. Techniek'),
 ('Long / doodle','Long'),
 ('Lang / doodle','Lang'),
 ('depending on coat condition','depending on nail condition'),
 ('afhankelijk van vachtconditie','afhankelijk van nagelconditie'),
 ('Certified groomer, all breeds','Certified stylist, every style'),
 ('Gediplomeerd, alle rassen','Gediplomeerd, elke stijl'),
 ('Wash, dry, nails & ears included','Manicure, file & topcoat included'),
 ('Wassen, drogen, nagels &amp; oren inbegrepen','Manicure, vijlen &amp; toplaag inbegrepen'),
 ('Wassen, drogen, nagels & oren inbegrepen','Manicure, vijlen & toplaag inbegrepen'),
 ('Honest advice for at home','Honest advice for at home'),
 ('Hand-stripping','Cuticle prep'),
 # --- batch 2: index-voorstelpagina, design-10 boekingen, gemiste NL/alt ---
 ('Wie zoekt op "hondentrimsalon Amsterdam Osdorp" vindt nu uw concurrenten. Met een eigen website verschijnt u in Google — elke dag nieuwe klanten die u nu misloopt.',
  'Wie zoekt op "nagelstudio Amsterdam Osdorp" vindt nu uw concurrenten. Met een eigen website verschijnt u in Google — elke dag nieuwe klanten die u nu misloopt.'),
 ("Mensen plannen zelf een afspraak, ook 's avonds. Die verschijnt direct in uw agenda — u wordt niet meer gestoord tijdens het trimmen.",
  "Mensen plannen zelf een afspraak, ook 's avonds. Die verschijnt direct in uw agenda — u wordt niet meer gestoord tijdens het werk."),
 ('Sleep de slider over de foto en zie een ongekamde vacht veranderen in een verzorgd resultaat. Uw vakwerk meteen zichtbaar.',
  'Sleep de slider over de foto en zie versleten nagels veranderen in een vers gelakt resultaat. Uw vakwerk meteen zichtbaar.'),
 ('grootte/vacht/dienst','lengte/techniek/dienst'),
 ('De bezoeker kiest grootte, vachttype en behandeling en ziet meteen een richtprijs — duidelijk, zonder dat u vastzit aan een vast bedrag.',
  'De bezoeker kiest lengte, techniek en behandeling en ziet meteen een richtprijs — duidelijk, zonder dat u vastzit aan een vast bedrag.'),
 ('Modern Mint — Trim-keuzehulp','Modern Mint — Nagel-keuzehulp'),
 ('Een korte, vriendelijke keuzehulp: "welke behandeling past bij mijn hond?" met persoonlijk advies en een directe boekingsknop.',
  'Een korte, vriendelijke keuzehulp: "welke behandeling past bij mij?" met persoonlijk advies en een directe boekingsknop.'),
 ('Trim-keuzehulp','Nagel-keuzehulp'),
 ('Wassen & föhnen|Wash & blow-dry|45','Gellak|Gel polish|45'),
 ('Volledige trimbeurt|Full grooming|65','Volledige set|Full set|65'),
 ('Plukbeurt ruwharig|Hand-stripping|70','BIAB-set|BIAB set|70'),
 ('Boek online of bel direct. Uw hond zal u dankbaar zijn.','Boek online of bel direct. Uw nagels zullen u dankbaar zijn.'),
 ('Vakwerk waar baasjes op rekenen','Vakwerk waar klanten op rekenen'),
 ('Careful de-shedding — never shaved, always respected.','Strong, natural-looking overlays — never bulky, always neat.'),
 ('Zorgvuldig ontwollen — nooit kaalscheren, altijd respecteren.','Sterke, natuurlijke overlay — nooit dik, altijd verzorgd.'),
 ('* Een richtprijs — de definitieve prijs bepalen we samen na het zien van de vacht.','* Een richtprijs — de definitieve prijs bepalen we samen na het zien van uw nagels.'),
 ('Vers getrimde hond','Vers gelakte nagels'),
 ('% alle rassen','% alle stijlen'),
 # --- losse woorden / restjes (langste eerst) ---
 ('All breeds','Every style'),('Alle rassen','Elke stijl'),('breeds welcome','styles welcome'),
 ('happy dogs','happy clients'),('blije honden','blije klanten'),
 ('Happy dog','Happy client'),('Blije hond','Blije klant'),
 ('Double coated','Acryl'),('Double coat','Acryl'),('double coat','acryl'),
 ('Wire-haired','BIAB'),('Ruwharig','BIAB'),('Doodles','Gellak'),('doodle','gellak'),
]
# ===== Pedicure (voetverzorging) — eigen content, zelfde keys als NAIL_MAP =====
PEDI_IMG = ["https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg?auto=compress&cs=tinysrgb&w=1280"%(i,i) for i in ["3997388","4677846","6135674","2600287","7446919","3557600","2268404","3997381"]]
PEDI_EMOJI = [("\U0001F415‍\U0001F9BA","\U0001F9B6"),("\U0001F415","\U0001F9B6"),
    ("\U0001F9AE","\U0001F9B6"),("\U0001F429","✨"),("\U0001F43E","\U0001FA77"),
    ("\U0001F9F9","\U0001F484"),("\U0001F98A","\U0001FA79")]
PEDICURE_MAP = [
 ('data-en="Small">Klein','data-en="Basic">Basis'),
 ('data-en="Large">Groot','data-en="Extensive">Uitgebreid'),
 ('data-en="Short / smooth">Kort / glad','data-en="Basic pedicure">Basispedicure'),
 ('data-en="Long / doodle">Lang / doodle','data-en="Medical pedicure">Medische pedicure'),
 ('data-en="Wire-haired">Ruwharig','data-en="Problem foot">Probleemvoet'),
 ('data-en="Double coat">Double coat','data-en="Diabetic foot">Diabetische voet'),
 ('data-en="Wash & blow-dry">Wassen &amp; föhnen','data-en="Basic pedicure">Basispedicure'),
 ('data-en="Full grooming">Volledige trimbeurt','data-en="Complete treatment">Complete behandeling'),
 ('data-en="Tidy-up">Bijwerken','data-en="Touch-up">Bijwerken'),
 ('data-en="Short & smooth">Kort &amp; glad','data-en="Basic pedicure">Basispedicure'),
 ('data-rec="Wassen & föhnen|Wash & blow-dry"','data-rec="Basispedicure|Basic pedicure"'),
 ('data-rec="Volledige trimbeurt|Full grooming"','data-rec="Complete behandeling|Complete treatment"'),
 ('data-rec="Plukbeurt (ruwharig)|Hand-stripping"','data-rec="Medische pedicure|Medical pedicure"'),
 ('data-rec="Ontwol-behandeling|De-shed treatment"','data-rec="Eeltbehandeling|Callus treatment"'),
 ("recVal=['Volledige trimbeurt','Full grooming']","recVal=['Complete behandeling','Complete treatment']"),
 # hele zinnen (EN)
 ('Certified dog groomer for all breeds — from doodle to Pomeranian. Book online and your dog is pampered in all peace and quiet.',
  'Certified pedicurist for healthy, well-cared-for feet. Book online and your feet are in expert, caring hands.'),
 ('Certified dog grooming salon in Amsterdam Osdorp. All breeds, groomed with love and patience.',
  'Certified pedicure practice in Amsterdam Osdorp. Expert foot care, with attention and patience.'),
 ('Certified groomer for all breeds. Book online — your dog is pampered in calm, professional hands.',
  'Certified pedicurist. Book online — your feet in calm, professional hands.'),
 ('Certified groomer for all breeds. Combine the grooming with a walk around the Sloterplas — your dog comes back glowing.',
  'Certified pedicurist. Walk out comfortably again — feet cared for, problems solved.'),
 ('Certified groomer for all breeds. Calm, careful and always with an eye for your dog.',
  'Certified pedicurist. Calm, careful and always with an eye for you.'),
 ('A certified groomer who treats every coat as a craft. All breeds, with love and patience.',
  'A certified pedicurist who treats every foot with care. Expert foot care, with attention and patience.'),
 ('Every dog gets time and attention. No rush, no stress — just patient, expert care from a certified groomer who keeps learning.',
  'Every client gets time and attention. No rush, no stress — just patient, expert care from a certified pedicurist who keeps learning.'),
 ('Diploma in hand and re-trained every year — most recently at the Purina Pro Plan symposium 2026. Your dog benefits from the latest insights in coat and skin care.',
  'Diploma in hand and re-trained every year — including medical foot care. You benefit from the latest insights in foot and skin care.'),
 ('A personal grooming salon. Love, patience and craftsmanship — for every coat, every breed.',
  'A personal pedicure practice. Care, patience and craftsmanship — for every foot.'),
 ('A gentle wash and careful drying, tailored to the coat.','A gentle, thorough treatment tailored to your feet.'),
 ('Trimming, stripping or clipping — exactly what the breed needs.','Basic, medical or spa — exactly what your feet need.'),
 ('A relaxed first visit so grooming stays fun for life.','A relaxed first visit so foot care stays something easy.'),
 ('A spa day for your dog — drag the slider and watch a scruffy coat turn into a clean, fluffy result.',
  'A spa moment for your feet — drag the slider and watch tired feet turn into fresh, cared-for results.'),
 ('Hand-stripping that keeps the coat healthy and true to type.','Careful treatment that keeps your feet and nails healthy.'),
 ('Gentle products, tailored to skin and coat.','Gentle products, tailored to skin and nails.'),
 ('Breed-true finish, neat and even.','Neat, careful finish every time.'),
 ('Expert handling of demanding coats, with patience.','Expert care for problem feet, with patience.'),
 ("No more guessing. Pick your dog's size, coat and treatment and see a price indication right away.",
  'No more guessing. Pick your treatment, foot condition and extras and see a price indication right away.'),
 ("* Indication only — the final price is set together after seeing your dog's coat.",
  '* Indication only — the final price is set together after seeing your feet.'),
 ('No more calling during grooming. Pick a treatment, a day and a time — done.',
  'No more calling during work. Pick a treatment, a day and a time — done.'),
 ('All breeds welcome, groomed with love and patience.','Every foot welcome, cared for with attention and patience.'),
 ('Book online or call directly. Your dog will thank you.','Book online or call directly. Your feet will thank you.'),
 ('Diploma plus yearly training. Specialised in doodles, wire-haired and double coats.',
  'Diploma plus yearly training. Specialised in medical, diabetic and problem feet.'),
 ('She trims our doodle with so much patience. He actually loves going now — and he comes back gorgeous.',
  'She treats my feet with so much care and patience. I walk out comfortable every time — a real recommendation.'),
 # hele zinnen (NL)
 ('Gediplomeerd hondentrimster voor alle rassen — van doodle tot pomeriaan. Boek online en uw hond wordt in alle rust verwend.',
  'Gediplomeerd pedicure voor gezonde, verzorgde voeten. Boek online en uw voeten zijn in deskundige, zorgzame handen.'),
 ('Gediplomeerde hondentrimsalon in Amsterdam Osdorp. Alle rassen, met liefde en geduld getrimd.',
  'Gediplomeerde pedicurepraktijk in Amsterdam Osdorp. Vakkundige voetverzorging, met aandacht en geduld.'),
 ('Gediplomeerd trimster voor alle rassen. Boek online — uw hond wordt in alle rust en met vakmanschap verwend.',
  'Gediplomeerd pedicure. Boek online — uw voeten in alle rust en met vakmanschap verzorgd.'),
 ('Gediplomeerd trimster voor alle rassen. Combineer de trimbeurt met een rondje Sloterplas — uw hond komt stralend terug.',
  'Gediplomeerd pedicure. U loopt er weer soepel en verzorgd vandoor — klachten verholpen.'),
 ('Gediplomeerd trimster voor alle rassen. Rustig, zorgvuldig en altijd met oog voor uw hond.',
  'Gediplomeerd pedicure. Rustig, zorgvuldig en altijd met oog voor u.'),
 ('Een gediplomeerd trimster die elke vacht als vakwerk behandelt. Alle rassen, met liefde en geduld.',
  'Een gediplomeerd pedicure die elke voet met zorg behandelt. Vakkundige voetverzorging, met aandacht en geduld.'),
 ('Elke hond krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd trimster die blijft bijscholen.',
  'Elke klant krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd pedicure die blijft bijscholen.'),
 ('Gediplomeerd én jaarlijks bijgeschoold — onlangs nog op het Purina Pro Plan-symposium 2026. Uw hond profiteert van de nieuwste inzichten in vacht- en huidverzorging.',
  'Gediplomeerd én jaarlijks bijgeschoold — óók in medische voetzorg. U profiteert van de nieuwste inzichten in voet- en huidverzorging.'),
 ('Gediplomeerd plus jaarlijkse bijscholing. Gespecialiseerd in doodles, ruwharig en double coats.',
  'Gediplomeerd plus jaarlijkse bijscholing. Gespecialiseerd in medische, diabetische en probleemvoeten.'),
 ('Een persoonlijke trimsalon. Liefde, geduld en vakmanschap — voor elke vacht, elk ras.',
  'Een persoonlijke pedicurepraktijk. Zorg, geduld en vakmanschap — voor elke voet.'),
 ('Een zachte wasbeurt en zorgvuldig drogen, afgestemd op de vacht.',
  'Een zachte, grondige behandeling afgestemd op uw voeten.'),
 ('Knippen, plukken of scheren — precies wat het ras nodig heeft.',
  'Basis, medisch of spa — precies wat uw voeten nodig hebben.'),
 ('Een ontspannen eerste keer zodat trimmen een leven lang leuk blijft.',
  'Een ontspannen eerste keer zodat voetverzorging makkelijk blijft.'),
 ('Met de hand plukken zodat de vacht gezond en raszuiver blijft.',
  'Zorgvuldige behandeling zodat uw voeten en nagels gezond blijven.'),
 ('Een spa-dag voor uw hond — sleep de slider en zie een verwaarloosde vacht veranderen in een schoon, donzig resultaat.',
  'Een spa-moment voor uw voeten — sleep de slider en zie vermoeide voeten veranderen in een fris, verzorgd resultaat.'),
 ('Vakkundige aanpak van veeleisende vachten, met geduld.','Vakkundige aanpak van probleemvoeten, met geduld.'),
 ('Zachte producten, afgestemd op huid en vacht.','Zachte producten, afgestemd op huid en nagels.'),
 ('Alle rassen welkom, met liefde en geduld getrimd.','Elke voet welkom, met aandacht en geduld verzorgd.'),
 ('Geen giswerk meer. Kies grootte, vacht en behandeling van uw hond en zie direct een richtprijs.',
  'Geen giswerk meer. Kies behandeling, voetconditie en extra en zie direct een richtprijs.'),
 ('Niet meer bellen tijdens het trimmen. Kies een behandeling, een dag en een tijd — klaar.',
  'Niet meer bellen tijdens het werk. Kies een behandeling, een dag en een tijd — klaar.'),
 ('Ze trimt onze doodle met zoveel geduld. Hij vindt het nu zelfs leuk — en hij komt er prachtig uit.',
  'Ze behandelt mijn voeten met zoveel zorg en geduld. Ik loop er elke keer soepel vandoor — een echte aanrader.'),
 # korte zinnen / labels
 ('Dog grooming · Amsterdam Osdorp','Pedicure · Amsterdam Osdorp'),
 ('Hondentrimsalon · Amsterdam Osdorp','Pedicure · Amsterdam Osdorp'),
 ('Groomed with love and patience','Cared for with attention and patience'),
 ('Met liefde en geduld getrimd','Met aandacht en geduld verzorgd'),
 ('Specialist in doodles, wire-haired and double coated.','Specialist in medical, diabetic and problem feet.'),
 ('Specialist in doodles, ruwharig en double coated.','Specialist in medische, diabetische en probleemvoeten.'),
 ('Specialised in doodles, wire-haired & double coat','Specialised in medical & diabetic foot care'),
 ('Gespecialiseerd in doodles, ruwharig & double coat','Gespecialiseerd in medische & diabetische voetzorg'),
 ('A calm spa day for your dog','A calm spa moment for your feet'),
 ('Een rustige spa-dag voor uw hond','Een rustig spa-moment voor uw voeten'),
 ('Honest coat advice, also for at home','Honest foot advice, also for at home'),
 ('Eerlijk vachtadvies, ook voor thuis','Eerlijk voetadvies, ook voor thuis'),
 ("Book your dog's spot online.",'Book your spot online.'),
 ('Boek online een plekje voor uw hond.','Boek online een plekje voor uzelf.'),
 ("Book your dog's session",'Book your appointment'),
 ('Boek de beurt van uw hond','Boek uw afspraak'),
 ("Book your dog's spot",'Book your spot'),
 ('Reserveer een plekje voor uw hond','Reserveer een plekje voor uzelf'),
 ('Expertly groomed, close to home','Expertly cared for, close to home'),
 ('Vakkundig getrimd, vlak bij huis','Vakkundig verzorgd, vlak bij huis'),
 ('Specialist care for every coat','Specialist care for every foot'),
 ('Specialistische zorg voor elke vacht','Specialistische zorg voor elke voet'),
 ('Wire-haired & stripping','Medical foot care'),
 ('Ruwharig &amp; plukken','Medische voetzorg'),
 ('Doodles & double coat','Diabetic & problem feet'),
 ('Doodles &amp; double coat','Diabetische &amp; probleemvoeten'),
 ('Plan a grooming session','Plan an appointment'),
 ('Plan een trimbeurt','Plan een afspraak'),
 ('Where your dog is <em>pampered</em>','Where your feet are <em>cared for</em>'),
 ('Waar uw hond wordt','Waar uw voeten worden'),
 ('Trimming, stripping or clipping','Basic, medical or spa'),
 ('Treat your dog','Treat your feet'),
 ('Verwen uw hond','Verwen uw voeten'),
 ('Time and patience for every dog','Time and patience for every client'),
 ('Tijd en geduld voor elke hond','Tijd en geduld voor elke klant'),
 ('From doodle to Pomeranian','From basic to medical'),
 ('Van doodle tot pomeriaan','Van basis tot medisch'),
 ('The art of grooming','The art of foot care'),
 ('De kunst van het trimmen','De kunst van voetverzorging'),
 ('Every coat, its own approach','Every foot, its own approach'),
 ('Elke vacht, eigen aanpak','Elke voet, eigen aanpak'),
 ('What does grooming cost?','What does a treatment cost?'),
 ('Wat kost een trimbeurt?','Wat kost een behandeling?'),
 ('Which treatment suits your dog?','Which treatment suits you?'),
 ('Welke behandeling past bij uw hond?','Welke behandeling past bij u?'),
 ("What's your dog's size?",'Which treatment do you want?'),
 ('Wat is de grootte van uw hond?','Welke behandeling wilt u?'),
 ("What's the coat like?",'What is your foot like?'),
 ('Wat voor vacht heeft uw hond?','Wat voor voet heeft u?'),
 ('How often is your dog groomed?','How often do you get a pedicure?'),
 ('Hoe vaak wordt uw hond getrimd?','Hoe vaak laat u uw voeten doen?'),
 ('Free trim advice','Free foot advice'),
 ('Gratis trimadvies','Gratis voetadvies'),
 ('Trim-quiz','Voet-quiz'),
 ('Full grooming','Complete behandeling'),
 ('Volledige trimbeurt','Complete behandeling'),
 ('Wassen &amp; föhnen','Basispedicure'),
 ('Wassen &amp; verzorgen','Basispedicure'),
 ('Knippen &amp; stylen','Knippen &amp; verzorgen'),
 ('Trim & style','Care & finish'),
 ('Plukbeurt ruwharig','Medische pedicure'),
 ('1. Size of your dog','1. Treatment'),
 ('1. Grootte van uw hond','1. Behandeling'),
 ('2. Coat type','2. Foot condition'),
 ('2. Vachttype','2. Voetconditie'),
 ('Long / doodle','Medical'),
 ('Lang / doodle','Medisch'),
 ('depending on coat condition','depending on foot condition'),
 ('afhankelijk van vachtconditie','afhankelijk van voetconditie'),
 ('Certified groomer, all breeds','Certified pedicurist'),
 ('Gediplomeerd, alle rassen','Gediplomeerd pedicure'),
 ('Wash, dry, nails & ears included','Foot bath, nails & callus included'),
 ('Wassen, drogen, nagels &amp; oren inbegrepen','Voetbad, nagels &amp; eelt inbegrepen'),
 ('Wassen, drogen, nagels & oren inbegrepen','Voetbad, nagels & eelt inbegrepen'),
 ('Hand-stripping','Callus care'),
 ('Wie zoekt op "hondentrimsalon Amsterdam Osdorp" vindt nu uw concurrenten. Met een eigen website verschijnt u in Google — elke dag nieuwe klanten die u nu misloopt.',
  'Wie zoekt op "pedicure Amsterdam Osdorp" vindt nu uw concurrenten. Met een eigen website verschijnt u in Google — elke dag nieuwe klanten die u nu misloopt.'),
 ("Mensen plannen zelf een afspraak, ook 's avonds. Die verschijnt direct in uw agenda — u wordt niet meer gestoord tijdens het trimmen.",
  "Mensen plannen zelf een afspraak, ook 's avonds. Die verschijnt direct in uw agenda — u wordt niet meer gestoord tijdens het werk."),
 ('Sleep de slider over de foto en zie een ongekamde vacht veranderen in een verzorgd resultaat. Uw vakwerk meteen zichtbaar.',
  'Sleep de slider over de foto en zie vermoeide voeten veranderen in een verzorgd resultaat. Uw vakwerk meteen zichtbaar.'),
 ('grootte/vacht/dienst','behandeling/voetconditie/extra'),
 ('De bezoeker kiest grootte, vachttype en behandeling en ziet meteen een richtprijs — duidelijk, zonder dat u vastzit aan een vast bedrag.',
  'De bezoeker kiest behandeling, voetconditie en extra en ziet meteen een richtprijs — duidelijk, zonder dat u vastzit aan een vast bedrag.'),
 ('Modern Mint — Trim-keuzehulp','Modern Mint — Voet-keuzehulp'),
 ('Een korte, vriendelijke keuzehulp: "welke behandeling past bij mijn hond?" met persoonlijk advies en een directe boekingsknop.',
  'Een korte, vriendelijke keuzehulp: "welke behandeling past bij mij?" met persoonlijk advies en een directe boekingsknop.'),
 ('Trim-keuzehulp','Voet-keuzehulp'),
 ('Wassen & föhnen|Wash & blow-dry|45','Basispedicure|Basic pedicure|30'),
 ('Volledige trimbeurt|Full grooming|65','Complete behandeling|Complete treatment|45'),
 ('Plukbeurt ruwharig|Hand-stripping|70','Medische pedicure|Medical pedicure|40'),
 ('Boek online of bel direct. Uw hond zal u dankbaar zijn.','Boek online of bel direct. Uw voeten zullen u dankbaar zijn.'),
 ('Vakwerk waar baasjes op rekenen','Vakwerk waar klanten op rekenen'),
 ('Careful de-shedding — never shaved, always respected.','Careful callus care — never harsh, always gentle.'),
 ('Zorgvuldig ontwollen — nooit kaalscheren, altijd respecteren.','Zorgvuldige eeltverwijdering — nooit hard, altijd voorzichtig.'),
 ('* Een richtprijs — de definitieve prijs bepalen we samen na het zien van de vacht.','* Een richtprijs — de definitieve prijs bepalen we samen na het zien van uw voeten.'),
 ('Vers getrimde hond','Vers verzorgde voeten'),
 ('% alle rassen','% elke voet'),
 ('All breeds','Every foot'),('Alle rassen','Elke voet'),('breeds welcome','feet welcome'),
 ('happy dogs','happy clients'),('blije honden','blije klanten'),
 ('Happy dog','Happy client'),('Blije hond','Blije klant'),
 ('Double coated','Diabetische voet'),('Double coat','Diabetische voet'),('double coat','diabetische voet'),
 ('Wire-haired','Probleemvoet'),('Ruwharig','Probleemvoet'),('Doodles','Medisch'),('doodle','medisch'),
 ('Pomeranian','medische voet'),('Pomeriaan','Medische voet'),('pomeriaan','medische voet'),
]

# per design: (bg-var, text-var, accent-var) zodat de sectie de kleuren overneemt
# ===== Kapper (kapsalon) — eigen content, zelfde keys als NAIL_MAP =====
KAPPER_IMG = ["https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151809_65126f44-8710-49f6-84b8-47350cc8868d.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151811_2493dc60-0682-4320-9d05-8978c565aac6.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151807_81603210-c65e-4327-b49f-fb0f9281e955.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151807_5a723566-f3db-4b5b-8d19-8acb222a8565.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151810_e684e8f1-0375-4c83-9819-4fdff5d6f117.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151810_adbf5ded-a32e-4d1f-9cc5-0856b9974e6d.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151807_e9deb4fb-f709-4212-8689-2109fffe1e68.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_151807_73c5c071-d4f6-4f14-9e56-4fc686311843.png"]
KAPPER_EMOJI = [("\U0001F415\u200d\U0001F9BA","\u2702\uFE0F"),("\U0001F415","\u2702\uFE0F"),
    ("\U0001F9AE","\u2702\uFE0F"),("\U0001F429","\u2728"),("\U0001F43E","\u2702\uFE0F"),
    ("\U0001F9F9","\U0001F488"),("\U0001F98A","\U0001F488")]
KAPPER_MAP = [
 ('data-en="Small">Klein','data-en="Short">Kort'),
 ('data-en="Large">Groot','data-en="Long">Lang'),
 ('data-en="Short / smooth">Kort / glad','data-en="Wash & cut">Wassen &amp; knippen'),
 ('data-en="Long / doodle">Lang / doodle','data-en="Cut & blow-dry">Knippen &amp; föhnen'),
 ('data-en="Wire-haired">Ruwharig','data-en="Color">Kleuren'),
 ('data-en="Double coat">Double coat','data-en="Highlights">Highlights'),
 ('data-en="Wash & blow-dry">Wassen &amp; föhnen','data-en="Wash & blow-dry">Wassen &amp; föhnen'),
 ('data-en="Full grooming">Volledige trimbeurt','data-en="Cut & color">Knippen &amp; kleuren'),
 ('data-en="Tidy-up">Bijwerken','data-en="Fringe trim">Pony bijknippen'),
 ('data-en="Short & smooth">Kort &amp; glad','data-en="Wash & cut">Wassen &amp; knippen'),
 ('data-rec="Volledige trimbeurt|Full grooming"','data-rec="Knippen & kleuren|Cut & color"'),
 ('data-rec="Plukbeurt (ruwharig)|Hand-stripping"','data-rec="Highlights|Highlights"'),
 ('data-rec="Ontwol-behandeling|De-shed treatment"','data-rec="Balayage|Balayage"'),
 ("recVal=['Volledige trimbeurt','Full grooming']","recVal=['Knippen & kleuren','Cut & color']"),
 ('Certified dog groomer for all breeds — from doodle to Pomeranian. Book online and your dog is pampered in all peace and quiet.',
  'Certified hairstylist for every look — from a sharp cut to full colour. Book online and enjoy your new look in all peace and quiet.'),
 ('Certified dog grooming salon in Amsterdam Osdorp. All breeds, groomed with love and patience.',
  'Certified hair salon in Amsterdam Osdorp. Every style, cut with care and craftsmanship.'),
 ('Certified groomer for all breeds. Book online — your dog is pampered in calm, professional hands.',
  'Certified hairstylist for every style. Book online — your hair in calm, professional hands.'),
 ('Certified groomer for all breeds. Calm, careful and always with an eye for your dog.',
  'Certified hairstylist for every style. Calm, careful and always with an eye for you.'),
 ('A certified groomer who treats every coat as a craft. All breeds, with love and patience.',
  'A certified hairstylist who treats every cut as a craft. Every style, with care and craftsmanship.'),
 ('Every dog gets time and attention. No rush, no stress — just patient, expert care from a certified groomer who keeps learning.',
  'Every client gets time and attention. No rush, no stress — just patient, expert care from a certified hairstylist who keeps learning.'),
 ('A personal grooming salon. Love, patience and craftsmanship — for every coat, every breed.',
  'A personal hair salon. Care, attention and craftsmanship — for every cut, every style.'),
 ('A gentle wash and careful drying, tailored to the coat.','A gentle wash and careful blow-dry, tailored to your hair.'),
 ('Trimming, stripping or clipping — exactly what the breed needs.','Cut, colour or styling — exactly what your hair needs.'),
 ('Gentle products, tailored to skin and coat.','Gentle products, tailored to scalp and hair.'),
 ('No more calling during grooming. Pick a treatment, a day and a time — done.',
  'No more calling during work. Pick a treatment, a day and a time — done.'),
 ('All breeds welcome, groomed with love and patience.','Every style welcome, cut with care and craftsmanship.'),
 ('Book online or call directly. Your dog will thank you.','Book online or call directly. You will love the result.'),
 ('She trims our doodle with so much patience. He actually loves going now — and he comes back gorgeous.',
  'She does my hair with so much care and attention. I actually look forward to every visit — and it always looks gorgeous.'),
 ('Gediplomeerd hondentrimster voor alle rassen — van doodle tot pomeriaan. Boek online en uw hond wordt in alle rust verwend.',
  'Gediplomeerd kapper voor elke look — van een strakke coupe tot complete kleuring. Boek online en u wordt in alle rust verwend.'),
 ('Gediplomeerde hondentrimsalon in Amsterdam Osdorp. Alle rassen, met liefde en geduld getrimd.',
  'Gediplomeerde kapsalon in Amsterdam Osdorp. Elke stijl, met zorg en vakmanschap geknipt.'),
 ('Gediplomeerd trimster voor alle rassen. Boek online — uw hond wordt in alle rust en met vakmanschap verwend.',
  'Gediplomeerd kapper voor elke stijl. Boek online — u wordt in alle rust en met vakmanschap verwend.'),
 ('Gediplomeerd trimster voor alle rassen. Rustig, zorgvuldig en altijd met oog voor uw hond.',
  'Gediplomeerd kapper voor elke stijl. Rustig, zorgvuldig en altijd met oog voor u.'),
 ('Een gediplomeerd trimster die elke vacht als vakwerk behandelt. Alle rassen, met liefde en geduld.',
  'Een gediplomeerd kapper die elke coupe als vakwerk behandelt. Elke stijl, met zorg en vakmanschap.'),
 ('Elke hond krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd trimster die blijft bijscholen.',
  'Elke klant krijgt tijd en aandacht. Geen haast, geen stress — alleen geduldig vakwerk van een gediplomeerd kapper die blijft bijscholen.'),
 ('Een persoonlijke trimsalon. Liefde, geduld en vakmanschap — voor elke vacht, elk ras.',
  'Een persoonlijke kapsalon. Zorg, aandacht en vakmanschap — voor elke coupe, elke stijl.'),
 ('Een zachte wasbeurt en zorgvuldig drogen, afgestemd op de vacht.',
  'Een zachte wasbeurt en zorgvuldig föhnen, afgestemd op uw haar.'),
 ('Knippen, plukken of scheren — precies wat het ras nodig heeft.',
  'Knippen, kleuren of stylen — precies wat uw haar nodig heeft.'),
 ('Zachte producten, afgestemd op huid en vacht.','Zachte producten, afgestemd op hoofdhuid en haar.'),
 ('Niet meer bellen tijdens het trimmen. Kies een behandeling, een dag en een tijd — klaar.',
  'Niet meer bellen tijdens het werk. Kies een behandeling, een dag en een tijd — klaar.'),
 ('Alle rassen welkom, met liefde en geduld getrimd.','Elke stijl welkom, met zorg en vakmanschap geknipt.'),
 ('Ze trimt onze doodle met zoveel geduld. Hij vindt het nu zelfs leuk — en hij komt er prachtig uit.',
  'Ze doet mijn haar met zoveel zorg en aandacht. Ik kijk nu zelfs uit naar elke afspraak — en het ziet er altijd prachtig uit.'),
 ('Dog grooming · Amsterdam Osdorp','Hair salon · Amsterdam Osdorp'),
 ('Hondentrimsalon · Amsterdam Osdorp','Kapsalon · Amsterdam Osdorp'),
 ('Groomed with love and patience','Cut with care and craftsmanship'),
 ('Met liefde en geduld getrimd','Met zorg en vakmanschap geknipt'),
 ('Plan a grooming session','Plan an appointment'),
 ('Plan een trimbeurt','Plan een afspraak'),
 ('Treat your dog','Treat yourself'),
 ('Verwen uw hond','Verwen uzelf'),
 ('Time and patience for every dog','Time and attention for every client'),
 ('Tijd en geduld voor elke hond','Tijd en aandacht voor elke klant'),
 ('The art of grooming','The art of hairdressing'),
 ('De kunst van het trimmen','De kunst van het kappen'),
 ('What does grooming cost?','What does an appointment cost?'),
 ('Wat kost een trimbeurt?','Wat kost een behandeling?'),
 ('Which treatment suits your dog?','Which treatment suits you?'),
 ('Welke behandeling past bij uw hond?','Welke behandeling past bij u?'),
 ('Free trim advice','Free hair advice'),
 ('Gratis trimadvies','Gratis haaradvies'),
 ('Trim-quiz','Haar-quiz'),
 ('Volledige trimbeurt','Knippen &amp; kleuren'),
 ('Wassen &amp; verzorgen','Wassen &amp; föhnen'),
 ('Where your dog is <em>pampered</em>','Where you are <em>pampered</em>'),
 ('Waar uw hond wordt','Waar u wordt'),
 ("What's your dog's size?","How long is your hair?"),
 ('Wat is de grootte van uw hond?','Hoe lang is uw haar?'),
 ("What's the coat like?",'Which treatment do you want?'),
 ('Wat voor vacht heeft uw hond?','Welke behandeling wilt u?'),
 ('How often is your dog groomed?','How often do you visit a salon?'),
 ('Hoe vaak wordt uw hond getrimd?','Hoe vaak gaat u naar de kapper?'),
 ('Vers getrimde hond','Vers geknipt haar'),
 # --- woord-vangnet (langste eerst) ---
 ('Hondentrimsalon','Kapsalon'),('hondentrimsalon','kapsalon'),
 ('Hondenkapsalon','Kapsalon'),('hondenkapsalon','kapsalon'),
 ('Trimsalon','Kapsalon'),('trimsalon','kapsalon'),
 ('getrimd','geknipt'),('Getrimd','Geknipt'),
 ('trimbeurt','knipbeurt'),('Trimbeurt','Knipbeurt'),
 ('trimmen','knippen'),('Trimmen','Knippen'),
 ('trimster','kapper'),('trimmer','kapper'),('groomer','hairstylist'),
 ('vachtverzorging','haarverzorging'),('Vachtverzorging','Haarverzorging'),
 ('vacht','haar'),('Vacht','Haar'),
 ('baasjes','klanten'),('baasje','klant'),
 ('viervoeter','klant'),('Viervoeter','Klant'),
 ('honden','klanten'),('Honden','Klanten'),('hond','klant'),('Hond','Klant'),
 ('alle rassen','elke stijl'),('Alle rassen','Elke stijl'),('rassen','stijlen'),('Rassen','Stijlen'),
 ('all breeds','every style'),('All breeds','Every style'),('breeds','styles'),
 ('doodle','coupe'),('Doodle','Coupe'),('pomeriaan','model'),('Pomeriaan','Model'),('Pomeranian','model'),
 ('ruwharig','krullend haar'),('Ruwharig','Krullend haar'),
 ('double coat','dik haar'),('Double coat','Dik haar'),
 ('ontwollen','föhnen'),('Plukken','Föhnen'),('plukken','föhnen'),
]

VARMAP = {
 "previews/design-01.html":("--bg","--text","--gold"),
 "previews/design-02.html":("--bg","--text","--gold"),
 "previews/design-03.html":("--bg","--text","--gold"),
 "previews/design-04.html":("--bg","--text","--plum"),
 "previews/design-06.html":("--bg","--ink","--terra"),
 "previews/design-07.html":("--bg","--ink","--teal"),
 "previews/design-08.html":("--bg","--ink","--honey"),
 "previews/design-09.html":("--bg","--ink","--mint"),
 "previews/design-10.html":("--bg","--text","--wood"),
}
# design-05 (cinematic, geen footer) krijgt geen infosectie

CAL = '''<script type="text/javascript">
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if(typeof namespace === "string"){cal.ns[namespace] = cal.ns[namespace] || api;p(cal.ns[namespace], ar);p(cal, ["initNamespace", namespace]);} else p(cal, ar); return;} p(cal, ar); }; })(window, "https://cal.eu/embed/embed.js", "init");
Cal("init", "demo-planner", {origin:"https://cal.eu"});
Cal.ns["demo-planner"]("ui", {"hideEventTypeDetails":false,"layout":"month_view"});
document.querySelectorAll("a").forEach(function(el){var t=(el.textContent||"").toLowerCase();if(/afspraak|online boeken|boek online|plan een afspraak|boek deze|deze afspraak|online afspraak/.test(t)||/^\\s*boek/.test(t)){el.setAttribute("data-cal-namespace","demo-planner");el.setAttribute("data-cal-link","brabantdigital/demo-planner");el.setAttribute("data-cal-config",'{"layout":"month_view"}');el.removeAttribute("href");el.style.cursor="pointer";}});
</script>'''


LOGO_FILES = ("previews/design-06.html","previews/design-07.html")
def apply_stats(html, stats):
    divs=""
    for item in stats:
        n=item[0]; lbl=item[1]; dec=item[2] if len(item)>2 else 0
        divs+='<div><b data-count="%s"%s>0</b><span>%s</span></div>'%(n,(' data-dec="%d"'%dec if dec else ''),lbl)
    return re.sub(r'<section class="stats">.*?</section>', '<section class="stats">'+divs+'</section>', html, flags=re.S)
def apply_logo(html, logo, naam):
    img='<img src="%s" alt="%s" style="height:36px;width:auto;display:block">'%(logo,naam)
    return re.sub(r'(<span class="logo"[^>]*>).*?(</span>)', r'\1'+img+r'\2', html, count=1, flags=re.S)

def transform(text, s):
    merk=s["bedrijf"]; kort=s["kort"]; plaats=s["plaats"]; td=s["tel_display"]; th=s["tel_href"]
    if s.get("niche")=="nagels":
        for a,b in NAIL_MAP: text=text.replace(a,b)
        for a,b in NAIL_EMOJI: text=text.replace(a,b)
    elif s.get("niche")=="pedicure":
        for a,b in PEDICURE_MAP: text=text.replace(a,b)
        for a,b in PEDI_EMOJI: text=text.replace(a,b)
    elif s.get("niche")=="kapper":
        for a,b in KAPPER_MAP: text=text.replace(a,b)
        for a,b in KAPPER_EMOJI: text=text.replace(a,b)
    text = re.sub(r'Trimsalon (<em[^>]*>)Scott</em>', r'\1'+kort+'</em>', text)
    for a,b in [("Scott's","uw"),("Hondentrimsalon Scott",merk),("Trimsalon Scott",merk),
        ("Sloterpark Groen","Parkgroen"),("Verwijst naar de Sloterplas om de hoek.","Rustig, natuurlijk en gevestigd."),
        ("een rondje Sloterplas","een wandeling in de buurt"),(" · bij de Sloterplas",""),("bij de Sloterplas","in de buurt"),
        ("Sloterplas","het park"),("Jan van Zutphenstraat 141, 1069 RR Amsterdam · 06 25 54 84 20",plaats+" · "+td),
        ("Jan van Zutphenstraat 141<br>1069 RR Amsterdam",plaats),("Jan van Zutphenstraat 141",plaats),
        ("1069 RR Amsterdam",plaats),("1069 RR",""),("Amsterdam Osdorp",plaats),
        ("tel:+31625548420",th),("31625548420",th.replace("tel:+","").replace("#contact","")),
        ("06 25 54 84 20",td),("Amsterdam",plaats),(">Scott<",">"+kort+"<"),("Scott",kort)]:
        text=text.replace(a,b)
    fotos=s.get("fotos") or []
    own = fotos if len(fotos)>=2 else []
    sel = NAIL_IMG if s.get("niche")=="nagels" else (PEDI_IMG if s.get("niche")=="pedicure" else (KAPPER_IMG if s.get("niche")=="kapper" else (pick_pool(s["slug"]) if POOL_OK else AI_URLS)))
    for i,u in enumerate(AI_URLS):
        repl = own[i] if i < len(own) else sel[i]
        if repl != u: text=text.replace(u, repl)
    return text

def info_section(fname, s):
    c=s.get("content") or {}
    verhaal=c.get("verhaal",""); tar=c.get("tarieven") or []; opening=c.get("openingstijden","")
    eig=c.get("eigenaar",""); spec=c.get("specialisaties") or []; cert=c.get("certificering") or []; revs=c.get("reviews") or []
    if not (verhaal or tar or opening or spec or revs): return ""
    bg,text,acc=VARMAP[fname]
    titel=("Over "+eig) if eig else "Over ons"
    titel_en=("About "+eig) if eig else "About us"
    chips=""
    if spec:
        chips='<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:18px">'
        for x in spec[:8]:
            chips+='<span style="border:1px solid var(%s);color:var(%s);border-radius:999px;padding:5px 12px;font-size:.78rem">%s</span>'%(acc,acc,x)
        chips+='</div>'
    cert_html=''
    if cert: cert_html='<p style="color:var(--mut);font-size:.85rem;margin-top:16px">\u2713 '+' \u00b7 '.join(cert)+'</p>'
    opening_html=''
    if opening: opening_html='<p style="color:var(--mut);margin-top:14px"><strong style="color:var(%s)" data-en="Opening hours:">Openingstijden:</strong> %s</p>'%(text,opening)
    if tar:
        lis=''
        for t in tar[:26]:
            if "\u2014" in t or "—" in t:
                naam,prijs=t.replace("\u2014","—").rsplit("—",1)
                lis+='<li style="padding:7px 0;border-bottom:1px solid rgba(128,128,128,.14);display:flex;justify-content:space-between;gap:14px;break-inside:avoid"><span>%s</span><span style="color:var(%s);white-space:nowrap">%s</span></li>'%(naam.strip(),acc,prijs.strip())
            else:
                lis+='<li style="padding:7px 0;border-bottom:1px solid rgba(128,128,128,.14);break-inside:avoid">%s</li>'%t
        cols='column-count:2;column-gap:34px;' if len(tar)>6 else ''
        tar_html='<ul style="list-style:none;font-size:.9rem;%s">%s</ul>'%(cols,lis)
    else:
        _afg = "afgestemd op lengte en techniek" if s.get("niche")=="nagels" else ("afgestemd op uw voeten en wensen" if s.get("niche")=="pedicure" else ("afgestemd op uw haar en wensen" if s.get("niche")=="kapper" else "afgestemd op ras en vacht"))
        tar_html='<p style="color:var(--mut)" data-en="Price on request — tailored to your needs. Feel free to ask for a quote.">Prijs op aanvraag \u2014 %s. Vraag gerust een richtprijs.</p>'%_afg
    over=('<section id="over" style="background:var(%s);color:var(%s);padding:74px 0;border-top:1px solid rgba(128,128,128,.18)">'%(bg,text)
      +'<div style="max-width:1100px;margin:0 auto;padding:0 28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:46px">'
      +'<div><div style="color:var(%s);letter-spacing:.26em;text-transform:uppercase;font-size:.72rem;margin-bottom:14px" data-en="About us">Over ons</div>'%acc
      +'<h2 style="font-family:var(--head);font-size:2rem;margin-bottom:16px" data-en="%s">%s</h2>'%(titel_en,titel)
      +'<p style="color:var(--mut);line-height:1.75">%s</p>%s%s%s</div>'%(verhaal,chips,cert_html,opening_html)
      +'<div><h3 style="font-family:var(--head);font-size:1.4rem;color:var(%s);margin-bottom:12px" data-en="Pricing">Tarieven</h3>%s</div>'%(acc,tar_html)
      +'</div></section>')
    rev=''
    if revs:
        cards=''
        for r in revs[:6]:
            tk=(r.get("tekst") or "").strip(); nm=(r.get("naam") or "").strip()
            if not tk: continue
            cards+='<div style="background:rgba(128,128,128,.08);border:1px solid rgba(128,128,128,.18);border-radius:14px;padding:20px"><p style="font-style:italic;line-height:1.6;margin-bottom:10px">\u201c%s\u201d</p><p style="color:var(%s);font-size:.85rem">\u2014 %s</p></div>'%(tk,acc,nm)
        if cards:
            rev=('<section style="background:var(%s);color:var(%s);padding:64px 0;border-top:1px solid rgba(128,128,128,.18)">'%(bg,text)
              +'<div style="max-width:1100px;margin:0 auto;padding:0 28px">'
              +'<div style="color:var(%s);letter-spacing:.26em;text-transform:uppercase;font-size:.72rem;margin-bottom:8px" data-en="Reviews">Reviews</div>'%acc
              +'<h2 style="font-family:var(--head);font-size:2rem;margin-bottom:24px" data-en="What our clients say">Wat klanten zeggen</h2>'
              +'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px">%s</div></div></section>'%cards)
    return over+rev

# ---- design-11 (premium pedicure) generator ----
_D11P = (ROOT/"_workflow"/"templates"/"design11-pedicure.html")
PEDI_D11_TPL = _D11P.read_text(encoding="utf-8") if _D11P.exists() else ""
def _rev_cards(revs):
    cards=""
    for r in (revs or [])[:3]:
        nm=(r.get("naam") or "Klant").strip(); tk=(r.get("tekst") or "").strip()
        if not tk: continue
        cards+='<div class="rev"><div class="stars">★★★★★</div><p>“%s”</p><div class="who"><div class="av">%s</div><div><b>%s</b><span data-en="Pedicure">Pedicure</span></div></div></div>'%(tk,nm[0],nm)
    if not cards:
        fb=[("Vakkundig en met veel zorg geholpen. Ik loop er weer soepel vandoor.","Marit"),
            ("Rustig, hygiënisch en deskundig. Een echte aanrader.","Tom"),
            ("Eindelijk een pedicure die de tijd neemt. Top!","Sanne")]
        for tk,nm in fb:
            cards+='<div class="rev"><div class="stars">★★★★★</div><p>“%s”</p><div class="who"><div class="av">%s</div><div><b>%s</b><span data-en="Pedicure">Pedicure</span></div></div></div>'%(tk,nm[0],nm)
    return cards
def render_d11_pedicure(s):
    if not PEDI_D11_TPL: return ""
    merk=s["bedrijf"]; kort=s.get("kort") or merk; plaats=s["plaats"]
    th=s.get("tel_href",""); td=s.get("tel_display","")
    tel = th[4:] if th.startswith("tel:") else (th or "#contact")
    logo = merk.replace(kort,"<em>%s</em>"%kort,1) if kort and kort in merk else "<em>%s</em>"%merk
    c=s.get("content") or {}
    out=PEDI_D11_TPL
    for a,b in {
        "⟦TITLE⟧":"%s — Pedicure %s"%(merk,plaats),"⟦LOGO⟧":logo,"⟦NAME⟧":merk,"⟦PLAATS⟧":plaats,
        "⟦TEL⟧":tel,"⟦PHONE⟧":td or "Bel of app ons","⟦ADRES⟧":plaats,
        "⟦IMG_HERO⟧":PEDI_IMG[0],"⟦IMG_ABOUT⟧":PEDI_IMG[1],"⟦IMG_G1⟧":PEDI_IMG[2],"⟦IMG_G2⟧":PEDI_IMG[3],"⟦IMG_G3⟧":PEDI_IMG[4],
        "⟦REVIEWS⟧":_rev_cards(c.get("reviews")),
    }.items():
        out=out.replace(a,b)
    return out

# ---- design-11 (premium nagel & hond) generators ----
def _d11_common(s):
    merk=s["bedrijf"]; kort=s.get("kort") or merk; plaats=s["plaats"]
    th=s.get("tel_href",""); td=s.get("tel_display","")
    tel = th[4:] if th.startswith("tel:") else (th or "#contact")
    logo = merk.replace(kort,"<em>%s</em>"%kort,1) if kort and kort in merk else "<em>%s</em>"%merk
    hours='<div class="row"><span data-en="Mon – Sat">Ma – Za</span><span data-en="By appointment">Op afspraak</span></div>'
    return dict(merk=merk,plaats=plaats,tel=tel,td=td or "Bel of app ons",logo=logo,hours=hours)
def _fill_d11(tpl,s,title_prefix,img):
    if not tpl: return ""
    d=_d11_common(s); out=tpl
    for a,b in {"⟦TITLE⟧":"%s — %s %s"%(d["merk"],title_prefix,d["plaats"]),
        "⟦LOGO⟧":d["logo"],"⟦NAME⟧":d["merk"],"⟦PLAATS⟧":d["plaats"],
        "⟦PHONE⟧":d["td"],"⟦TEL⟧":d["tel"],
        "⟦IMG_HERO⟧":img[0],"⟦IMG_ABOUT⟧":img[1],"⟦IMG_G1⟧":img[2],
        "⟦IMG_G2⟧":img[3],"⟦IMG_G3⟧":img[4],"⟦HOURS_ROWS⟧":d["hours"]}.items():
        out=out.replace(a,b)
    return out
_D11N=(ROOT/"_workflow"/"templates"/"design11-nagel.html")
NAGEL_D11_TPL=_D11N.read_text(encoding="utf-8") if _D11N.exists() else ""
_D11H=(ROOT/"_workflow"/"templates"/"design11-hond.html")
HOND_D11_TPL=_D11H.read_text(encoding="utf-8") if _D11H.exists() else ""
def render_d11_nagel(s): return _fill_d11(NAGEL_D11_TPL,s,"Nagelstudio",NAIL_IMG)
def render_d11_hond(s):  return _fill_d11(HOND_D11_TPL,s,"Hondentrimsalon",(pick_pool(s["slug"]) if POOL_OK else AI_URLS))
_D11K=(ROOT/"_workflow"/"templates"/"design11-kapper.html")
KAPPER_D11_TPL=_D11K.read_text(encoding="utf-8") if _D11K.exists() else ""
KAPPER_VIDEO="https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/hf_20260616_181032_b972a3a9-1980-4adc-b865-ce27e40bb1d7.mp4"
KAPPER_PRICE_EX=[("Knippen dames","€ 39"),("Knippen heren","€ 27"),("Wassen, knippen & föhnen","€ 49"),("Kinderen (t/m 12 jr)","€ 22"),("Kleuren (uitgroei)","vanaf € 55"),("Highlights / folies","vanaf € 75"),("Balayage","vanaf € 95"),("Föhnen / opsteken","vanaf € 30")]
KAPPER_REV_EX=[("Altijd top geholpen — ze luisteren echt en denken mee. Mijn vaste kapper!","Sanne"),("Strakke coupe en een fijne sfeer. Online boeken is zo makkelijk.","Mark"),("Eindelijk een kleuring waar ik blij van word. Echt vakwerk.","Lisa")]
def render_d11_kapper(s):
    if not KAPPER_D11_TPL: return _fill_d11(HOND_D11_TPL,s,"Kapsalon",KAPPER_IMG)
    merk=s["bedrijf"]; kort=s.get("kort") or merk; plaats=s["plaats"]
    th=s.get("tel_href","") or ""; td=s.get("tel_display","") or ""
    logo = merk.replace(kort,"<em>%s</em>"%kort,1) if kort and kort in merk else "<em>%s</em>"%merk
    c=s.get("content") or {}; eig=(c.get("eigenaar") or "").strip(); email=(s.get("email") or "").strip()
    verhaal=c.get("verhaal") or ("%s is een kapsalon in %s voor knippen, kleuren en styling — met zorg, vakmanschap en persoonlijke aandacht voor dames, heren en kinderen."%(merk,plaats))
    about_title=("Over %s"%eig) if eig else ("Welkom bij %s"%merk)
    tar=c.get("tarieven") or []; rows=[]; note=""
    if tar:
        for t in tar[:12]:
            t=t.replace("\u2014","—")
            if "—" in t: n,pr=t.rsplit("—",1)
            else: n,pr=t,""
            rows.append((n.strip(),pr.strip()))
    else:
        rows=KAPPER_PRICE_EX; note="* Voorbeeld-richtprijzen ter illustratie — definitieve tarieven stemmen we samen af."
    prices_html="".join('<div class="price-row"><span class="pn">%s</span><span class="pp">%s</span></div>'%(n,pr) for n,pr in rows)
    revs=[((r.get("tekst") or "").strip(),(r.get("naam") or "Klant").strip()) for r in (c.get("reviews") or []) if (r.get("tekst") or "").strip()][:3]
    if not revs: revs=KAPPER_REV_EX
    rev_html="".join('<div class="rev"><div class="st">★★★★★</div><p>“%s”</p><div class="who">— %s</div></div>'%(tk,nm) for tk,nm in revs)
    hours="Di–Vr 09:00–18:00 · Za 09:00–17:00 · overig op afspraak"
    digits=th.replace("tel:","").replace("+","").replace(" ","").replace("-","")
    wa_btn=""; wa_float=""
    if digits.startswith("316") and len(digits)>=11:
        wlink="https://wa.me/%s"%digits
        wa_btn='<a class="btn btn-ghost" href="%s" target="_blank" rel="noopener" data-en="WhatsApp">WhatsApp</a>'%wlink
        wa_float='<a class="wa-float" href="%s" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 3C9 3 3.5 8.5 3.5 15.5c0 2.4.7 4.6 1.9 6.5L4 29l7.2-1.9c1.8 1 3.8 1.5 5.8 1.5 7 0 12.5-5.5 12.5-12.5S23 3 16 3z"/></svg> App ons</a>'%wlink
    maps_q=_ul.quote(plaats+", Nederland")
    repl={"⟦TITLE⟧":"%s — Kapsalon %s"%(merk,plaats),"⟦NAME⟧":merk,"⟦LOGO⟧":logo,"⟦PLAATS⟧":plaats,
      "⟦VIDEO⟧":KAPPER_VIDEO,"⟦POSTER⟧":KAPPER_IMG[2],"⟦IMG_ABOUT⟧":KAPPER_IMG[6],
      "⟦IMG_G1⟧":KAPPER_IMG[0],"⟦IMG_G2⟧":KAPPER_IMG[1],"⟦IMG_G3⟧":KAPPER_IMG[5],
      "⟦ABOUT_TITLE⟧":about_title,"⟦ABOUT⟧":verhaal,"⟦PRICES⟧":prices_html,"⟦PRICE_NOTE⟧":note,
      "⟦REVIEWS⟧":rev_html,"⟦HOURS⟧":hours,"⟦PHONE⟧":(td or "Bel of app ons"),
      "⟦EMAILTXT⟧":(email or "Op aanvraag"),"⟦EMAILRAW⟧":email,"⟦MAPS_Q⟧":maps_q,
      "⟦WA_BTN⟧":wa_btn,"⟦WA_FLOAT⟧":wa_float}
    out=KAPPER_D11_TPL
    for a,b in repl.items(): out=out.replace(a,b)
    return out

_D12K=(ROOT/"_workflow"/"templates"/"design12-kapper.html")
KAPPER_D12_TPL=_D12K.read_text(encoding="utf-8") if _D12K.exists() else ""
KAPPER_REV5=[("Eindelijk een kapper die écht luistert. Ik ga elke keer met een topgevoel naar buiten.","Sanne"),
 ("Eerlijk advies en vakwerk — mijn haar zat nog nooit zo goed.","Lisa"),
 ("Heerlijke persoonlijke aandacht doordat het op afspraak is. Geen gehaast, geen wachtrij.","Marjolein"),
 ("Al jaren mijn vaste kapper. Aangeraden aan mijn hele vriendengroep.","Demi"),
 ("Mooie kleur, perfecte coupe en een fijne sfeer. Hier voel je je meteen op je gemak.","Fatima")]
def render_d12_kapper(s):
    if not KAPPER_D12_TPL: return render_d11_kapper(s)
    merk=s["bedrijf"]; kort=s.get("kort") or merk; plaats=s["plaats"]
    th=s.get("tel_href","") or ""; td=s.get("tel_display","") or ""
    logo = merk.replace(kort,"<em>%s</em>"%kort,1) if kort and kort in merk else "<em>%s</em>"%merk
    c=s.get("content") or {}; email=(s.get("email") or "").strip()
    about_title="Een salon waar je \u00e9cht gehoord wordt"
    about=c.get("verhaal") or ("Bij %s draait het niet om snel even knippen en wegwezen. Wij nemen de tijd, luisteren naar wat jij wilt en geven eerlijk, deskundig advies over wat bij jouw gezicht, stijl en haartype past."%merk)
    revs=[((r.get("tekst") or "").strip(),(r.get("naam") or "Klant").strip()) for r in (c.get("reviews") or []) if (r.get("tekst") or "").strip()][:5]
    if not revs: revs=KAPPER_REV5
    rev_html="".join('<div class="rev"><div class="st">\u2605\u2605\u2605\u2605\u2605</div><p>\u201c%s\u201d</p><div class="who">\u2014 %s</div></div>'%(tk,nm) for tk,nm in revs)
    digits=th.replace("tel:","").replace("+","").replace(" ","").replace("-","")
    if th.startswith("tel:") and digits:
        bel_btn='<a class="btn btn-out" href="%s" data-en="Call directly">Bel direct \u2014 %s</a>'%(th,td)
    else:
        bel_btn='<a class="btn btn-out" href="#contact" data-en="Call or message us">Bel of app ons</a>'
    wa_btn=""; wa_float=""
    if digits.startswith("316") and len(digits)>=11:
        wl="https://wa.me/%s"%digits
        wa_btn='<a class="btn btn-out" href="%s" target="_blank" rel="noopener" data-en="WhatsApp">WhatsApp</a>'%wl
        wa_float='<a class="wa-float" href="%s" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 3C9 3 3.5 8.5 3.5 15.5c0 2.4.7 4.6 1.9 6.5L4 29l7.2-1.9c1.8 1 3.8 1.5 5.8 1.5 7 0 12.5-5.5 12.5-12.5S23 3 16 3z"/></svg> App ons</a>'%wl
    import urllib.parse as _u
    repl={"\u27e6TITLE\u27e7":"%s \u2014 Kapsalon %s"%(merk,plaats),"\u27e6NAME\u27e7":merk,"\u27e6LOGO\u27e7":logo,"\u27e6PLAATS\u27e7":plaats,
      "\u27e6IMG_HERO\u27e7":KAPPER_IMG[1],"\u27e6IMG_ABOUT\u27e7":KAPPER_IMG[2],"\u27e6ABOUT_TITLE\u27e7":about_title,"\u27e6ABOUT\u27e7":about,
      "\u27e6REVIEWS\u27e7":rev_html,"\u27e6PHONE\u27e7":(td or "Bel of app ons"),"\u27e6EMAILTXT\u27e7":(email or "Op aanvraag"),"\u27e6EMAILRAW\u27e7":email,
      "\u27e6MAPS_Q\u27e7":_u.quote(plaats+", Nederland"),"\u27e6BEL_BTN\u27e7":bel_btn,"\u27e6WA_BTN\u27e7":wa_btn,"\u27e6WA_FLOAT\u27e7":wa_float}
    out=KAPPER_D12_TPL
    for a,b in repl.items(): out=out.replace(a,b)
    return out

n=0
for s in salons:
    if s.get("niche")=="schilder":
        dest=ROOT/s["slug"]/"03-designs"; (dest/"previews").mkdir(parents=True,exist_ok=True)
        (dest/"index.html").write_text(_gp.render_cover(s),encoding="utf-8")
        for _i in range(1,7):
            (dest/"previews"/("design-%d.html"%_i)).write_text(_gp.render_premium(s,_i),encoding="utf-8")
        n+=1; continue
    dest=ROOT/s["slug"]/"03-designs"; (dest/"previews").mkdir(parents=True,exist_ok=True)
    for f in FILES:
        out=transform((SRC/f).read_text(encoding="utf-8"), s)
        if s.get("stats") and 'class="stats"' in out: out=apply_stats(out, s["stats"])
        if s.get("logo") and f in LOGO_FILES: out=apply_logo(out, s["logo"], s["bedrijf"])
        if f!="index.html":
            if f in VARMAP and "<footer" in out:
                sec=info_section(f,s)
                if sec: out=out.replace("<footer",sec+"<footer",1)
            out=out.replace("</body>", CAL+"\n</body>",1)
        if s.get("taal")=="en":
            out=out.replace('<html lang="nl">','<html lang="en">')
            out=out.replace("</body>", '<script>addEventListener("load",function(){var b=document.getElementById("lang");if(b&&/EN/i.test(b.textContent))b.click();});</script>\n</body>',1)
        (dest/f).write_text(out,encoding="utf-8")
    _nb=s.get("niche")
    if _nb=="pedicure":
        (dest/"previews"/"design-11.html").write_text(render_d11_pedicure(s),encoding="utf-8")
    elif _nb=="nagels":
        (dest/"previews"/"design-11.html").write_text(render_d11_nagel(s),encoding="utf-8")
    elif _nb=="kapper":
        (dest/"previews"/"design-11.html").write_text(render_d11_kapper(s),encoding="utf-8")
        (dest/"previews"/"design-12.html").write_text(render_d12_kapper(s),encoding="utf-8")
        _idx=dest/"index.html"
        try:
            _h=_idx.read_text(encoding="utf-8"); _an='<div class="cat"><h2>Tijdloos'
            if "previews/design-12.html" not in _h and _an in _h:
                _card=('<div class="card" data-src="previews/design-12.html">\n'
                  '    <div class="head"><span class="num">\u2605</span><h3>Premium 2 \u2014 Warm &amp; Persoonlijk</h3>\n'
                  '      <div class="tags"><span class="tag">nieuw</span><span class="tag">persoonlijk</span><span class="tag">op afspraak</span></div></div>\n'
                  '    <p class="desc">Lichte, warme one-pager met de nadruk op persoonlijk advies en exclusief-op-afspraak: behandelingen, redenen om te kiezen, reviews en een direct boekings- en contactblok.</p>\n'
                  '  </div>\n\n')
                _h=_h.replace(_an,_card+_an,1); _idx.write_text(_h,encoding="utf-8")
        except Exception: pass
    else:
        (dest/"previews"/"design-11.html").write_text(render_d11_hond(s),encoding="utf-8")
    n+=1
print(f"{n} demo's gegenereerd (met content-sectie + Cal-popup).")
