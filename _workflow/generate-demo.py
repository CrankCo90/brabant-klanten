#!/usr/bin/env python3
"""Genereert per salon een kiesdemo op basis van het Scott-sjabloon, met:
- eigen merknaam/plaats/telefoon
- eigen foto's (bij 2+ echte foto's), anders AI
- 'Over ons + Tarieven'-sectie met echte content (in de kleuren van elk design)
- Cal-planner popup op de 'Afspraak maken'-knoppen
"""
import json, re, random
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "hondentrimsalonscott" / "03-designs"
FILES = ["index.html"] + [f"previews/design-{i:02d}.html" for i in range(1,11)]
salons = json.loads((ROOT/"_workflow"/"salons-batch1.json").read_text(encoding="utf-8"))

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
# per design: (bg-var, text-var, accent-var) zodat de sectie de kleuren overneemt
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
    sel = NAIL_IMG if s.get("niche")=="nagels" else (pick_pool(s["slug"]) if POOL_OK else AI_URLS)
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
        _afg = "afgestemd op lengte en techniek" if s.get("niche")=="nagels" else "afgestemd op ras en vacht"
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

n=0
for s in salons:
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
    n+=1
print(f"{n} demo's gegenereerd (met content-sectie + Cal-popup).")
