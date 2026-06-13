#!/usr/bin/env python3
"""Genereert per salon een kiesdemo op basis van het Scott-sjabloon, met:
- eigen merknaam/plaats/telefoon
- eigen foto's (bij 2+ echte foto's), anders AI
- 'Over ons + Tarieven'-sectie met echte content (in de kleuren van elk design)
- Cal-planner popup op de 'Afspraak maken'-knoppen
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "hondentrimsalonscott" / "03-designs"
FILES = ["index.html"] + [f"previews/design-{i:02d}.html" for i in range(1,11)]
salons = json.loads((ROOT/"_workflow"/"salons-batch1.json").read_text(encoding="utf-8"))

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
    if len(fotos)>=2:
        BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/"
        AI=[BASE+x for x in ["hf_20260613_085111_ed4bc4a1-2b25-4d9e-9d32-c845d82e43d5.png","hf_20260613_085111_f52a0629-6c32-41b2-b8dd-fef7eedcac53.png","hf_20260613_085113_6fec380b-3cdc-4be3-b70c-9d7c43c23dc1.png","hf_20260613_085115_b87c0cc0-c208-4c3b-8852-8bca6fcdcb98.png","hf_20260613_085116_7544c5ba-9d93-484b-bb04-5d7b6ab28cb3.png","hf_20260613_085118_a274f992-0d24-45ad-a2c6-c057fd5ec738.png","hf_20260613_085120_63fb879f-0316-4081-b785-cbc92515996b.png","hf_20260613_085121_b800ad99-b6c5-4d3b-acc0-2940c43fa059.png"]]
        for i,u in enumerate(AI):
            if i < len(fotos): text=text.replace(u,fotos[i])
    return text

def info_section(fname, s):
    c=s.get("content") or {}
    verhaal=c.get("verhaal",""); tar=c.get("tarieven") or []; opening=c.get("openingstijden",""); eig=c.get("eigenaar","")
    if not (verhaal or tar or opening): return ""
    bg,text,acc=VARMAP[fname]
    titel=("Over "+eig) if eig else "Over ons"
    opening_html=f'<p style="color:var(--mut);margin-top:14px"><strong style="color:var({text})">Openingstijden:</strong> {opening}</p>' if opening else ""
    if tar:
        lis=""
        for t in tar[:8]:
            if "—" in t:
                naam,prijs=t.rsplit("—",1)
                lis+=f'<li style="display:flex;justify-content:space-between;gap:18px;padding:8px 0;border-bottom:1px solid rgba(128,128,128,.16)"><span>{naam.strip()}</span><span style="color:var({acc});white-space:nowrap">{prijs.strip()}</span></li>'
            else:
                lis+=f'<li style="padding:8px 0;border-bottom:1px solid rgba(128,128,128,.16)">{t}</li>'
        if len(tar)>8: lis+='<li style="padding:8px 0;color:var(--mut)">… en meer — vraag de volledige prijslijst</li>'
        tar_html=f'<ul style="list-style:none;font-size:.92rem">{lis}</ul>'
    else:
        tar_html='<p style="color:var(--mut)">Prijs op aanvraag — afgestemd op ras en vacht. Vraag gerust een richtprijs.</p>'
    return (f'<section id="over" style="background:var({bg});color:var({text});padding:74px 0;border-top:1px solid rgba(128,128,128,.18)">'
      f'<div style="max-width:1100px;margin:0 auto;padding:0 28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:44px">'
      f'<div><div style="color:var({acc});letter-spacing:.26em;text-transform:uppercase;font-size:.72rem;margin-bottom:14px">Over ons</div>'
      f'<h2 style="font-family:var(--head);font-size:2rem;margin-bottom:16px">{titel}</h2>'
      f'<p style="color:var(--mut);line-height:1.75">{verhaal}</p>{opening_html}</div>'
      f'<div><h3 style="font-family:var(--head);font-size:1.4rem;color:var({acc});margin-bottom:12px">Tarieven</h3>{tar_html}</div>'
      f'</div></section>')

n=0
for s in salons:
    dest=ROOT/s["slug"]/"03-designs"; (dest/"previews").mkdir(parents=True,exist_ok=True)
    for f in FILES:
        out=transform((SRC/f).read_text(encoding="utf-8"), s)
        if f!="index.html":
            if f in VARMAP and "<footer" in out:
                sec=info_section(f,s)
                if sec: out=out.replace("<footer",sec+"<footer",1)
            out=out.replace("</body>", CAL+"\n</body>",1)
        (dest/f).write_text(out,encoding="utf-8")
    n+=1
print(f"{n} demo's gegenereerd (met content-sectie + Cal-popup).")
