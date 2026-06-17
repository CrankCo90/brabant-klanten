#!/usr/bin/env python3
"""Zet door n8n gevonden prospects (JSON-lijst) om naar demo's + brein-log.
Aanroep: python3 _workflow/ingest-prospects.py <pad-naar-json>
Record-velden (van n8n): bedrijf, plaats, provincie, telefoon, social, email, website_status, niche."""
import sys, json, re, datetime, subprocess
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parent.parent
ACC = str.maketrans("àáâäãåèéêëìíîïòóôöõùúûüçñ", "aaaaaaeeeeiiiiooooouuuucn")
def slugify(s):
    s = (s or "").lower().translate(ACC)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48]
NICHE = {
 "hond":     {"spec":["Alle rassen","Wassen & föhnen","Knippen & scheren","Nagels knippen"], "verhaal":"%s in %s verzorgt honden van alle rassen met aandacht en vakmanschap. Rustig en op afspraak."},
 "nagels":   {"spec":["Gellak","BIAB","Acryl","Manicure & nailart"], "verhaal":"%s in %s verzorgt verzorgde nagels — gellak, BIAB en nailart, met oog voor detail. Op afspraak."},
 "pedicure": {"spec":["Medische pedicure","Voetverzorging","Eeltbehandeling","Op afspraak"], "verhaal":"%s in %s biedt vakkundige voetverzorging met aandacht en zorg. Op afspraak."},
 "kapper":   {"spec":["Knippen","Kleuren","Highlights","Wassen & föhnen"], "verhaal":"%s in %s verzorgt knippen, kleuren en styling met zorg en vakmanschap. Op afspraak."},
}
PREFIX = re.compile(r'^(hondentrimsalon|trimsalon|hondenkapsalon|hondenkapper|dierenkapper|kapsalon|kapper|nagelstudio|nagelsalon|nailstudio|pedicuresalon|pedicurepraktijk|pedicure|haarsalon|salon)\s+', re.I)
def telhref(tel):
    d = re.sub(r"[^0-9]", "", tel or "")
    if d.startswith("0"): d = "+31" + d[1:]
    elif d and not d.startswith("31"): d = "+31" + d
    return ("tel:" + d) if d else "#contact"
def main():
    recs = json.load(open(sys.argv[1], encoding="utf-8"))
    sb = json.load(open(ROOT/"_workflow/salons-batch1.json", encoding="utf-8"))
    cl = json.load(open(ROOT/"dashboard/clients.json", encoding="utf-8"))
    slugs = {s.get("slug") for s in sb}
    names = {c.get("bedrijf","").lower().strip() for c in cl}
    quals, seen = [], set()
    for r in recs:
        bedrijf = (r.get("bedrijf") or "").strip()
        plaats = (r.get("plaats") or "").strip()
        if not bedrijf: continue
        nm = bedrijf.lower().strip()
        if nm in names or nm in seen: continue
        niche = (r.get("niche") or "hond").strip().lower()
        if niche not in NICHE: niche = "hond"
        tel = (r.get("telefoon") or "").strip(); dd = re.sub(r"[^0-9]", "", tel)
        is_mobile = dd.startswith("06") or dd.startswith("316")
        social = (r.get("social") or "").strip(); email = (r.get("email") or "").strip()
        if not (is_mobile or email or social): continue  # bereikbaarheidsregel
        slug = slugify(bedrijf)
        if slug in slugs: slug = slugify(bedrijf + "-" + plaats)
        if not slug or slug in slugs: continue
        seen.add(nm); slugs.add(slug)
        kort = (PREFIX.sub("", bedrijf).strip() or bedrijf)[:40]
        defv = NICHE[niche]
        waarom = "Geen eigen website (alleen Facebook)." if (social and not is_mobile and "facebook" in social.lower()) else ("Geen eigen website (alleen social)." if social and not is_mobile else "Geen eigen website (alleen vermelding/06).")
        quals.append({"bedrijf":bedrijf,"kort":kort,"slug":slug,"plaats":plaats,"regio":(r.get("provincie") or ""),
            "niche":niche,"tel":(tel if is_mobile else ""),"social":social,"email":email,"eigenaar":"",
            "verhaal": defv["verhaal"] % (bedrijf, plaats or "de regio"),
            "spec": defv["spec"], "cert": [], "waarom": waarom})
    json.dump(quals, open("/tmp/new_quals.json","w"), ensure_ascii=False)
    if quals:
        subprocess.run(["python3","_workflow/add-prospects.py"], cwd=str(ROOT))
        subprocess.run(["python3","_workflow/generate-demo.py"], cwd=str(ROOT))
    # brein-log
    cl2 = json.load(open(ROOT/"dashboard/clients.json", encoding="utf-8"))
    tot = Counter(c.get("niche") for c in cl2)
    by = Counter((q["regio"] or "?", q["niche"]) for q in quals)
    d = datetime.date.today().isoformat()
    log = ROOT/"brein"/"logs"/(d + "-ingest.md")
    log.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# %s — n8n ingest (+%d prospects)" % (d, len(quals)), ""]
    for (reg, nch), n in sorted(by.items()): lines.append("- %s / %s: +%d" % (reg, nch, n))
    lines += ["", "Totalen na ingest: " + ", ".join("%s: %d" % (k, v) for k, v in tot.items()), ""]
    with open(log, "a", encoding="utf-8") as f: f.write("\n".join(lines) + "\n")
    print("ingest: +%d toegevoegd; totalen %s" % (len(quals), dict(tot)))
main()
