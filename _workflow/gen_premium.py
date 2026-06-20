# -*- coding: utf-8 -*-
"""Premium-only generator voor niche schilder/stukadoor: 6 thema's op 1 responsive template + eigen coverpagina."""
import re, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TPL = (ROOT/"_workflow"/"templates"/"premium-schilder.html").read_text(encoding="utf-8")

def _initials(name):
    parts=[w for w in re.sub(r'[^A-Za-z0-9 ]',' ',name).split() if w]
    ig={'en','van','de','het','der','of','bv','vof'}
    letters=[p[0].upper() for p in parts if p.lower() not in ig][:2]
    return "".join(letters) or name[:2].upper()

def _ctx(s):
    merk=s["bedrijf"]; kort=(s.get("kort") or merk).strip(); plaats=s["plaats"]
    td=(s.get("tel_display") or s.get("tel") or "").strip()
    th=(s.get("tel_href") or "").strip()
    raw=(s.get("tel") or th or "").replace("tel:","")
    digits=re.sub(r'\D','',raw)
    email=(s.get("email") or "").strip()
    if th.startswith("tel:"): href=th
    elif digits: href="tel:+31"+digits[1:] if digits.startswith("0") else "tel:+"+digits
    elif email: href="mailto:"+email
    else: href="#offerte"
    phone = td or ("Mail ons" if email else "Bel ons")
    logo = merk.replace(kort,"<em>%s</em>"%html.escape(kort),1) if kort and kort in merk else html.escape(merk)
    wa=""
    if digits.startswith("06") or digits.startswith("316"):
        d2="31"+digits[1:] if digits.startswith("06") else digits
        wa=('<a class="wa-float" href="https://wa.me/%s" target="_blank" rel="noopener">'
            '<svg viewBox="0 0 32 32"><path d="M16 3C9 3 3.5 8.5 3.5 15.5c0 2.4.7 4.6 1.9 6.5L4 29l7.2-1.9c1.8 1 3.8 1.5 5.8 1.5 7 0 12.5-5.5 12.5-12.5S23 3 16 3z"/></svg> App ons</a>')%d2
    return dict(merk=merk,kort=kort,plaats=plaats,phone=phone,href=href,email=email,
                emailtxt=(email or "Op aanvraag"),logo=logo,initials=_initials(merk),wa=wa)

# 6 thema's (kleuren/fonts/hero) — content komt uit de gedeelde template
IMG="https://assets.ls-assets.com/provider/istock/%s.jpg?w=1600"
THEMES=[
 # 1 Charcoal & Oranje
 dict(css="", bodyclass="t1", heroclass="",
   kicker='<span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <b>9.6</b> uit 50+ reviews',
   title='Strak stucwerk en <span class="ac">schilderwerk</span> met oog voor detail',
   sub='Vakmanschap, eerlijke prijzen en een nette afwerking - altijd. Afspraak = afspraak.',
   trust='&#10003; Gratis &amp; vrijblijvend - binnen 24 uur een eerlijke offerte',
   rating='<span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <b>9.6</b> uit 50+ reviews', promo='', topbar=''),
 # 2 Zwart & Goud
 dict(css=":root{--bg:#0e0d0b;--band:#15130f;--surface:#181510;--ink:#fff;--text:#cdc5b4;--muted:#9a9race;--accent:#c8a24a;--accent2:#c8a24a22;--ct:#1a1609;--line:#2b271f;--hbg:#0a0908;--hfg:#fff;--ov:linear-gradient(rgba(8,7,6,.74),rgba(8,7,6,.86));--himg:url('%s');--whyimg:url('%s');--revbg:#181510;--revtx:#cdc5b4;--rad:6px;--fh:'Playfair Display',serif}"%(IMG%"2223733287",IMG%"2250749192"),
   bodyclass="t2", heroclass="center",
   kicker='&#10022; Premium vakmanschap',
   title='Schilder- &amp; <span class="ac">Stucadoorsbedrijf</span> {{NAME}}',
   sub='Perfecte afwerking, duurzame kwaliteit en een zorgeloze ervaring. Hoogwaardig schilder- en stucadoorswerk.',
   trust='&#9733; 4.9/5 klantbeoordeling &nbsp;&bull;&nbsp; Garantie op al het werk',
   rating='<span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <b>4.9 / 5</b> - 200+ tevreden klanten', promo='', topbar=''),
 # 3 Licht editorial & Goud (serif italic)
 dict(css=":root{--bg:#fbf8f2;--band:#f3ebdd;--surface:#fff;--ink:#23201a;--text:#4b463d;--muted:#867d6f;--accent:#b0883a;--accent2:#b0883a1c;--ct:#fff;--line:#e8dccb;--hbg:#23201a;--hfg:#fff;--ov:linear-gradient(rgba(28,24,18,.42),rgba(28,24,18,.6));--himg:url('%s');--whyimg:url('%s');--fh:'Cormorant Garamond',Georgia,serif;--rad:4px}.hero h1{font-size:clamp(2.6rem,6vw,4.4rem)}.hero h1 .ac,.sec-head h2 .ac,.offer h2 .ac{font-style:italic}#lang{background:#ffffff22}"%(IMG%"2206957489",IMG%"2223733287"),
   bodyclass="t3", heroclass="",
   kicker='&mdash; Vakmanschap sinds jaar en dag',
   title='Strak schilder- en stucwerk <span class="ac">met een luxe uitstraling</span>',
   sub='Voor perfect afgewerkt schilder- en stucwerk dat jarenlang indruk maakt. Vakmanschap en heldere afspraken.',
   trust='Vrijblijvende offerte &nbsp;&bull;&nbsp; Persoonlijk advies &nbsp;&bull;&nbsp; Snelle reactie',
   rating='<b>Vertrouwd</b> door tevreden klanten', promo='', topbar=''),
 # 4 Licht & Goud, donkere hero links
 dict(css=":root{--bg:#fcfaf6;--band:#f4efe6;--surface:#fff;--ink:#1f1c17;--text:#48433b;--muted:#837b6d;--accent:#b8924e;--accent2:#b8924e1c;--ct:#fff;--line:#e9e0d2;--hbg:#1c1915;--hfg:#fff;--ov:linear-gradient(rgba(18,16,12,.6),rgba(18,16,12,.74));--himg:url('%s');--whyimg:url('%s');--fh:'Playfair Display',serif;--rad:6px}"%(IMG%"1368933301",IMG%"2206957489"),
   bodyclass="t4", heroclass="",
   kicker='Schilder &amp; Stukadoorsbedrijf',
   title='Vakwerk dat je ziet, <span class="ac">voelt en jarenlang vertrouwt</span>',
   sub='Vakmanschap, nette afwerking en heldere communicatie. Voor particulieren en bedrijven die houden van perfectie.',
   trust='&#10003; Gratis en vrijblijvend &nbsp;&bull;&nbsp; Reactie binnen 24 uur &nbsp;&bull;&nbsp; Heldere prijsopgave',
   rating='<b>Klanten die houden van perfectie</b>', promo='', topbar=''),
 # 5 Corporate blauw (WordPress-stijl)
 dict(css=":root{--bg:#fff;--band:#f3f6fb;--surface:#fff;--ink:#12294b;--text:#3a4254;--muted:#6b7384;--accent:#1a5fb4;--accent2:#1a5fb414;--ct:#fff;--line:#e2e8f1;--hbg:#fff;--hfg:#12294b;--ov:linear-gradient(rgba(12,30,60,.5),rgba(12,30,60,.62));--himg:url('%s');--whyimg:url('%s');--fh:'Poppins',sans-serif;--fb:'Inter',sans-serif;--rad:6px}#lang{background:#12294b12;color:var(--hfg);border-color:#12294b22}.menu a{opacity:.95}"%(IMG%"2217702678",IMG%"2223733287"),
   bodyclass="t5", heroclass="",
   kicker='Stukadoors- &amp; afbouwbedrijf',
   title='Stukadoors- en afbouwwerk met <span class="ac">vakmanschap &amp; netheid</span>',
   sub='Een betrouwbaar familiebedrijf voor pleisterwerk, spuitwerk, betonlook, schilderwerk en gevelisolatie.',
   trust='Vakmanschap &bull; Betrouwbaar &bull; Afspraak is afspraak',
   rating='<b>UITSTEKEND</b> - gebaseerd op tientallen recensies',
   promo='', topbar='<div class="topbar"><div class="wrap"><span>&#9742; {{PHONE}} &nbsp; &#9993; {{EMAILTXT}}</span><span>Vakwerk in {{PLAATS}} en omgeving</span></div></div>'),
 # 6 Modern blauw + oranje, nieuwbouw
 dict(css=":root{--bg:#fff;--band:#f2f7fb;--surface:#fff;--ink:#0f2b46;--text:#3a4658;--muted:#6e7888;--accent:#1f9bd6;--accent2:#1f9bd614;--ct:#fff;--line:#e3eaf2;--hbg:#0f1d2e;--hfg:#fff;--ov:linear-gradient(rgba(10,20,34,.76),rgba(10,20,34,.84));--himg:url('%s');--whyimg:url('%s');--fh:'Poppins',sans-serif;--fb:'Inter',sans-serif;--rad:10px}.btn-pri{background:#ef7d22;color:#fff}"%(IMG%"2250749192",IMG%"2235698324"),
   bodyclass="t6", heroclass="",
   kicker='&#9733;&#9733;&#9733;&#9733;&#9733; Top beoordeeld - 300+ reviews',
   title='Specialist in strak <span class="ac">stuc- en spuitwerk</span>',
   sub='Van nieuwbouw tot renovatie: dunpleister, spuitwerk, vloeren en meer. Vaste prijzen per m2, snel geregeld.',
   trust='&#10003; Binnen 1 werkdag een offerte in uw mail',
   rating='<span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> <b>Top beoordeeld</b> - 300+ reviews',
   promo='<div class="promo"><h3>Vaste prijzen per m&sup2;</h3><p>Binnen 1 werkdag een heldere offerte in uw mail - geen verrassingen.</p></div>', topbar=''),
]


import shutil as _shutil
VN_DIR = ROOT/"_workflow"/"assets"/"voornaa"
VN_PAIRS=[("kamer7.jpg","kamer7a.jpg","Woonkamer - van ruwbouw naar strak afgewerkt"),
          ("kamer8.jpg","kamer8a.jpg","Slaapkamer - compleet gestukt en geschilderd")]
def _vn_have():
    return [(v,n,c) for (v,n,c) in VN_PAIRS if (VN_DIR/v).exists() and (VN_DIR/n).exists()]
def voorna_section():
    have=_vn_have()
    if not have: return ""
    cards=""
    for v,n,cap in have:
        cards+=('<div class="ba"><div class="ba-wrap">'
          '<img class="ba-after" src="../assets/voornaa/%s" alt="Na">'
          '<img class="ba-before" src="../assets/voornaa/%s" alt="Voor">'
          '<input type="range" min="0" max="100" value="50" class="ba-range" aria-label="Voor en na">'
          '<div class="ba-handle"><span>&#8596;</span></div>'
          '<span class="ba-lbl ba-l" data-en="Before">Voor</span><span class="ba-lbl ba-r" data-en="After">Na</span>'
          '</div><div class="ba-cap">%s</div></div>')%(n,v,cap)
    return ('<section id="voorna" class="band"><div class="wrap"><div class="sec-head">'
      '<span class="eyebrow" data-en="Before &amp; after">Voor &amp; na</span>'
      '<h2 data-en="See the transformation">Zie de <span class="ac">transformatie</span></h2>'
      '<p data-en="Drag the slider to see the result of our work.">Sleep de schuif om het resultaat van ons werk te zien.</p></div>'
      '<div class="ba-grid">%s</div></div></section>')%cards
def voorna_grid():
    have=_vn_have()
    if not have: return ""
    cards=""
    for v,n,cap in have:
        cards+=('<div class="ba"><div class="ba-wrap">'
          '<img class="ba-after" src="../assets/voornaa/%s" alt="Na">'
          '<img class="ba-before" src="../assets/voornaa/%s" alt="Voor">'
          '<input type="range" min="0" max="100" value="50" class="ba-range" aria-label="Voor en na">'
          '<div class="ba-handle"><span>&#8596;</span></div>'
          '<span class="ba-lbl ba-l" data-en="Before">Voor</span><span class="ba-lbl ba-r" data-en="After">Na</span>'
          '</div><div class="ba-cap">%s</div></div>')%(n,v,cap)
    return '<div class="ba-grid">'+cards+'</div>'
def copy_voorna(dest):
    if not VN_DIR.exists(): return
    out=dest/"assets"/"voornaa"
    if out.exists(): _shutil.rmtree(out)
    _shutil.copytree(VN_DIR, out)

def render_premium(s, i):
    t=THEMES[i-1]; c=_ctx(s)
    _bespoke=ROOT/"_workflow"/"templates"/("premium%d-schilder.html"%i)
    if _bespoke.exists():
        out=_bespoke.read_text(encoding="utf-8")
        for k,v in [("{{TITLE}}","%s - Schilder &amp; Stukadoor %s"%(html.escape(c["merk"]),html.escape(c["plaats"]))),
                    ("{{LOGO}}",c["logo"]),("{{NAME}}",html.escape(c["merk"])),("{{INITIALS}}",c["initials"]),
                    ("{{PHONE}}",html.escape(c["phone"])),("{{TEL_HREF}}",c["href"]),
                    ("{{EMAILTXT}}",html.escape(c["emailtxt"])),("{{EMAILRAW}}",c["email"]),
                    ("{{PLAATS}}",html.escape(c["plaats"])),("{{WA_FLOAT}}",c["wa"]),("{{VOORNA}}",voorna_grid()),
                    ("{{TOPMAIL}}",(' of mail naar <a href="mailto:%s">%s</a>'%(c["email"],html.escape(c["email"])) if c["email"] else ""))]:
            out=out.replace(k,v)
        return out
    out=TPL
    for k,v in [("{{THEME_CSS}}",t["css"]),("{{BODYCLASS}}",t["bodyclass"]),("{{HEROCLASS}}",t["heroclass"]),
                ("{{TOPBAR}}",t["topbar"]),("{{HERO_KICKER}}",t["kicker"]),("{{HERO_TITLE}}",t["title"]),
                ("{{HERO_SUB}}",t["sub"]),("{{TRUST}}",t["trust"]),("{{RATING}}",t["rating"]),("{{PROMO}}",t["promo"]),("{{VOORNA}}",voorna_section())]:
        out=out.replace(k,v)
    for k,v in [("{{TITLE}}","%s - Schilder &amp; Stukadoor %s"%(html.escape(c["merk"]),html.escape(c["plaats"]))),
                ("{{LOGO}}",c["logo"]),("{{NAME}}",html.escape(c["merk"])),("{{INITIALS}}",c["initials"]),
                ("{{PHONE}}",html.escape(c["phone"])),("{{TEL_HREF}}",c["href"]),
                ("{{EMAILTXT}}",html.escape(c["emailtxt"])),("{{EMAILRAW}}",c["email"]),
                ("{{PLAATS}}",html.escape(c["plaats"])),("{{WA_FLOAT}}",c["wa"])]:
        out=out.replace(k,v)
    return out

_CARDS=[("1","Charcoal &amp; Oranje","Krachtig en warm - donkere hero met oranje accent, serif-koppen en heldere dienstenkaarten."),
 ("2","Zwart &amp; Goud","Luxe en exclusief - zwart met goud, premium uitstraling voor wie zich wil onderscheiden."),
 ("3","Licht &amp; Editorial","Verfijnd en rustig - lichte, elegante look met goud-cursieve accenten."),
 ("4","Licht &amp; Goud","Strak en modern - lichte stijl met donkere fotohero en goud accent."),
 ("5","Corporate Blauw","Zakelijk en vertrouwd - blauw, clean en overzichtelijk, ideaal voor een gevestigd bedrijf."),
 ("6","Modern Blauw + Oranje","Fris en commercieel - nadruk op prijszekerheid en snelle offerte, sterk voor nieuwbouw.")]

def render_cover(s):
    c=_ctx(s); merk=html.escape(c["merk"]); plaats=html.escape(c["plaats"])
    cards=""
    for num,naam,desc in _CARDS:
        cards+=('<div class="card" data-src="previews/design-%s.html"><div class="head"><span class="num">%s</span>'
                '<h3>%s</h3></div><p class="desc">%s</p></div>\n')%(num,num,naam,desc)
    return COVER.replace("{{MERK}}",merk).replace("{{PLAATS}}",plaats).replace("{{INITIALS}}",c["initials"]).replace("{{CARDS}}",cards)

COVER=r"""<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{MERK}} - 6 premium ontwerpen | Brabant Digital</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:Inter,system-ui,sans-serif;background:#11161d;color:#e7ecf3;line-height:1.6}
.wrap{max-width:1100px;margin:0 auto;padding:0 22px}a{color:inherit}
.hero{padding:74px 0 40px;text-align:center}.hero .ey{color:#5fb0ff;font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:.8rem}
.hero h1{font-size:clamp(2rem,4.5vw,3rem);margin:14px 0;font-weight:800}.hero h1 span{color:#5fb0ff}
.hero p{color:#aeb8c6;max-width:60ch;margin:0 auto;font-size:1.06rem}
.benefits{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:30px 0 10px}
.benefit{background:#19202a;border:1px solid #243040;border-radius:14px;padding:20px}.benefit .ic{font-size:1.5rem}.benefit h3{font-size:1rem;margin:8px 0 4px}.benefit p{color:#9fabbb;font-size:.86rem}
.cat{padding:34px 0 6px}.cat h2{font-size:1.5rem}.cat .sub{color:#9fabbb}
.card{background:#19202a;border:1px solid #243040;border-radius:16px;padding:22px;margin:16px 0}
.head{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.num{width:34px;height:34px;border-radius:9px;background:#5fb0ff22;color:#5fb0ff;display:grid;place-items:center;font-weight:800}
.head h3{font-size:1.2rem}.desc{color:#9fabbb;margin:10px 0 0;font-size:.94rem}
.frame{position:relative;border-radius:14px;overflow:hidden;border:1px solid #243040;box-shadow:0 20px 50px rgba(0,0,0,.4);background:#000;margin-top:16px}
.frame iframe{width:100%;height:640px;border:0;display:block}
.frame .bar{display:flex;gap:10px;justify-content:flex-end;padding:8px;background:#0d1218}.frame .bar button{background:#5fb0ff;color:#06121f;border:0;border-radius:8px;padding:7px 13px;font-weight:700;cursor:pointer;font-family:inherit}
.contact{background:#19202a;border:1px solid #243040;border-radius:16px;padding:30px;margin:34px 0;text-align:center}
.contact h2{font-size:1.5rem}.contact p{color:#9fabbb}.contact .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.contact a{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:10px;font-weight:700;text-decoration:none}
.wa{background:#25D366;color:#fff}.mail{background:#5fb0ff;color:#06121f}
footer{text-align:center;color:#7e8a99;font-size:.84rem;padding:30px 0 90px}
#bd-wa-float{position:fixed;bottom:22px;right:22px;z-index:99999;display:flex;align-items:center;gap:9px;background:#25D366;color:#fff;text-decoration:none;padding:12px 18px;border-radius:999px;font-weight:700;font-size:.95rem;box-shadow:0 6px 20px rgba(0,0,0,.28)}
@media(max-width:820px){.benefits{grid-template-columns:1fr 1fr}.frame iframe{height:520px}}
@media(max-width:560px){.benefits{grid-template-columns:1fr}.frame iframe{height:460px}}
</style></head><body>
<div class="wrap">
<div class="hero"><div class="ey">Brabant Digital - voorstel voor {{MERK}}</div>
<h1>Zes <span>premium</span> ontwerpen voor {{MERK}}</h1>
<p>We hebben alvast zes complete website-ontwerpen voor {{MERK}} in {{PLAATS}} gebouwd. Bekijk ze hieronder, kies je favoriet - en wij zetten 'm live op je eigen domein.</p></div>
<div class="benefits">
<div class="benefit"><div class="ic">&#128270;</div><h3>Gevonden in Google</h3><p>Wie zoekt op "stukadoor {{PLAATS}}" vindt straks jou - elke dag nieuwe aanvragen.</p></div>
<div class="benefit"><div class="ic">&#128221;</div><h3>Offertes binnen</h3><p>Bezoekers vragen direct via het formulier een offerte aan, 24/7.</p></div>
<div class="benefit"><div class="ic">&#10024;</div><h3>Professionele uitstraling</h3><p>Een verzorgde eigen site met eigen domein en e-mail. Je oogt gevestigd en betrouwbaar.</p></div>
<div class="benefit"><div class="ic">&#11088;</div><h3>Vertrouwen op 1 plek</h3><p>Diensten, reviews en projecten overzichtelijk bij elkaar.</p></div>
</div>
<div class="cat"><h2>Kies je favoriete ontwerp</h2><p class="sub">Zes complete richtingen - klik op een ontwerp om de volledige website te bekijken.</p></div>
{{CARDS}}
<div class="contact"><h2>Welke spreekt je het meest aan?</h2><p>Laat het ons weten via WhatsApp of mail - we zetten je favoriet live op je eigen domein, inclusief hosting en onderhoud.</p>
<div class="btns"><a class="wa" href="https://wa.me/31850608491" target="_blank" rel="noopener">&#128172; WhatsApp 085-0608491</a><a class="mail" href="mailto:aanbod@brabantdigital.nl">&#9993; aanbod@brabantdigital.nl</a></div></div>
<footer>Gemaakt door Brabant Digital &bull; aanbod@brabantdigital.nl &bull; 085-0608491</footer>
</div>
<a id="bd-wa-float" href="https://wa.me/31850608491" target="_blank" rel="noopener" aria-label="App ons via WhatsApp"><svg width="22" height="22" viewBox="0 0 24 24" fill="#fff"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg><span>App ons</span></a>
<script>document.querySelectorAll('.card[data-src]').forEach(function(card){var src=card.getAttribute('data-src');var f=document.createElement('div');f.className='frame';f.innerHTML='<div class="bar"><button>Volledig scherm</button></div><iframe loading="lazy" src="'+src+'"></iframe>';card.appendChild(f);f.querySelector('button').onclick=function(){window.open(src,'_blank');};});</script>
</body></html>"""
