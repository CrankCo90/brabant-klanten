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
    sel = pick_pool(s["slug"]) if POOL_OK else AI_URLS
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
    chips=""
    if spec:
        chips='<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:18px">'
        for x in spec[:8]:
            chips+='<span style="border:1px solid var(%s);color:var(%s);border-radius:999px;padding:5px 12px;font-size:.78rem">%s</span>'%(acc,acc,x)
        chips+='</div>'
    cert_html=''
    if cert: cert_html='<p style="color:var(--mut);font-size:.85rem;margin-top:16px">\u2713 '+' \u00b7 '.join(cert)+'</p>'
    opening_html=''
    if opening: opening_html='<p style="color:var(--mut);margin-top:14px"><strong style="color:var(%s)">Openingstijden:</strong> %s</p>'%(text,opening)
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
        tar_html='<p style="color:var(--mut)">Prijs op aanvraag \u2014 afgestemd op ras en vacht. Vraag gerust een richtprijs.</p>'
    over=('<section id="over" style="background:var(%s);color:var(%s);padding:74px 0;border-top:1px solid rgba(128,128,128,.18)">'%(bg,text)
      +'<div style="max-width:1100px;margin:0 auto;padding:0 28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:46px">'
      +'<div><div style="color:var(%s);letter-spacing:.26em;text-transform:uppercase;font-size:.72rem;margin-bottom:14px">Over ons</div>'%acc
      +'<h2 style="font-family:var(--head);font-size:2rem;margin-bottom:16px">%s</h2>'%titel
      +'<p style="color:var(--mut);line-height:1.75">%s</p>%s%s%s</div>'%(verhaal,chips,cert_html,opening_html)
      +'<div><h3 style="font-family:var(--head);font-size:1.4rem;color:var(%s);margin-bottom:12px">Tarieven</h3>%s</div>'%(acc,tar_html)
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
              +'<div style="color:var(%s);letter-spacing:.26em;text-transform:uppercase;font-size:.72rem;margin-bottom:8px">Reviews</div>'%acc
              +'<h2 style="font-family:var(--head);font-size:2rem;margin-bottom:24px">Wat klanten zeggen</h2>'
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
        (dest/f).write_text(out,encoding="utf-8")
    n+=1
print(f"{n} demo's gegenereerd (met content-sectie + Cal-popup).")
