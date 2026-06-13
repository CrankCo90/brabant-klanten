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
    # eigen foto's van de prospect gebruiken (anders blijven de AI-beelden staan)
    fotos = s.get("fotos") or []
    # 1 eigen afbeelding = bijna altijd een logo/banner -> dan liever nette AI-foto's
    if len(fotos) >= 2:
        BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2/"
        AI=[BASE+x for x in [
            "hf_20260613_085111_ed4bc4a1-2b25-4d9e-9d32-c845d82e43d5.png",
            "hf_20260613_085111_f52a0629-6c32-41b2-b8dd-fef7eedcac53.png",
            "hf_20260613_085113_6fec380b-3cdc-4be3-b70c-9d7c43c23dc1.png",
            "hf_20260613_085115_b87c0cc0-c208-4c3b-8852-8bca6fcdcb98.png",
            "hf_20260613_085116_7544c5ba-9d93-484b-bb04-5d7b6ab28cb3.png",
            "hf_20260613_085118_a274f992-0d24-45ad-a2c6-c057fd5ec738.png",
            "hf_20260613_085120_63fb879f-0316-4081-b785-cbc92515996b.png",
            "hf_20260613_085121_b800ad99-b6c5-4d3b-acc0-2940c43fa059.png"]]
        # eigen foto's vullen de eerste beeldplekken (incl. hero); rest blijft AI -> mix, geen herhaling
        for i,u in enumerate(AI):
            if i < len(fotos):
                text = text.replace(u, fotos[i])
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
