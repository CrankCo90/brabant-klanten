#!/usr/bin/env python3
"""Genereert per salon een kiesdemo (03-designs/) op basis van het Scott-sjabloon."""
import json, re, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "hondentrimsalonscott" / "03-designs"
FILES = ["index.html"] + [f"previews/design-{i:02d}.html" for i in range(1,11)]
salons = json.loads((ROOT/"_workflow"/"salons-batch1.json").read_text(encoding="utf-8"))

def transform(text, s):
    merk = s["bedrijf"]; kort = s["kort"]; plaats = s["plaats"]
    td = s["tel_display"]; th = s["tel_href"]
    # logo: "Trimsalon <em ...>Scott</em>" -> alleen de merknaam
    text = re.sub(r'Trimsalon (<em[^>]*>)Scott</em>', r'\1'+kort+'</em>', text)
    rep = [
        ("Scott's", "uw"),
        ("Hondentrimsalon Scott", merk),
        ("Trimsalon Scott", merk),
        ("Sloterpark Groen", "Parkgroen"),
        ("Verwijst naar de Sloterplas om de hoek.", "Rustig, natuurlijk en gevestigd."),
        ("een rondje Sloterplas", "een wandeling in de buurt"),
        (" · bij de Sloterplas", ""),
        ("bij de Sloterplas", "in de buurt"),
        ("Sloterplas", "het park"),
        ("Jan van Zutphenstraat 141, 1069 RR Amsterdam · 06 25 54 84 20", plaats+" · "+td),
        ("Jan van Zutphenstraat 141<br>1069 RR Amsterdam", plaats),
        ("Jan van Zutphenstraat 141", plaats),
        ("1069 RR Amsterdam", plaats),
        ("1069 RR", ""),
        ("Amsterdam Osdorp", plaats),
        ("tel:+31625548420", th),
        ("31625548420", th.replace("tel:+","").replace("#contact","")),
        ("06 25 54 84 20", td),
        ("Amsterdam", plaats),
        (">Scott<", ">"+kort+"<"),
        ("Scott", kort),
    ]
    for a,b in rep:
        text = text.replace(a,b)
    return text

count=0
for s in salons:
    dest = ROOT / s["slug"] / "03-designs"
    (dest/"previews").mkdir(parents=True, exist_ok=True)
    for f in FILES:
        out = transform((SRC/f).read_text(encoding="utf-8"), s)
        (dest/f).write_text(out, encoding="utf-8")
    count+=1
print(f"{count} demo's gegenereerd.")
