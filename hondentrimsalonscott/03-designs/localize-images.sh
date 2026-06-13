#!/usr/bin/env bash
# Downloadt de 8 bron-foto's en zet ze om naar lokale WebP, en vervangt de CDN-links
# in de designs door lokale paden. Draai dit VANUIT de map 03-designs/ op je PC
# (Git Bash) of op de VPS — daar werkt internet wel.
#   chmod +x localize-images.sh && ./localize-images.sh
set -e
BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3EDLFqGUNpQE4EgXyTJzGEcupp2"
mkdir -p assets/img
# naam -> bron-PNG
declare -A SRC=(
 [hero-doodle]="hf_20260613_085111_ed4bc4a1-2b25-4d9e-9d32-c845d82e43d5.png"
 [hero-doodle2]="hf_20260613_085111_f52a0629-6c32-41b2-b8dd-fef7eedcac53.png"
 [salon]="hf_20260613_085113_6fec380b-3cdc-4be3-b70c-9d7c43c23dc1.png"
 [before]="hf_20260613_085115_b87c0cc0-c208-4c3b-8852-8bca6fcdcb98.png"
 [after]="hf_20260613_085116_7544c5ba-9d93-484b-bb04-5d7b6ab28cb3.png"
 [grooming]="hf_20260613_085118_a274f992-0d24-45ad-a2c6-c057fd5ec738.png"
 [pomeranian]="hf_20260613_085120_63fb879f-0316-4081-b785-cbc92515996b.png"
 [tools]="hf_20260613_085121_b800ad99-b6c5-4d3b-acc0-2940c43fa059.png"
)
# converter detecteren
if command -v cwebp >/dev/null; then CONV=cwebp
elif command -v magick >/dev/null; then CONV=magick
elif command -v convert >/dev/null; then CONV=convert
else echo "Geen webp-tool gevonden. Installeer 'cwebp' (webp) of ImageMagick."; echo "  Ubuntu/VPS: sudo apt install webp   |   Windows: choco install webp"; exit 1; fi
echo "Converter: $CONV"
for name in "${!SRC[@]}"; do
  url="$BASE/${SRC[$name]}"
  echo "↓ $name"
  curl -fsSL "$url" -o "assets/img/$name.png"
  case "$CONV" in
    cwebp)   cwebp -quiet -q 82 -resize 1600 0 "assets/img/$name.png" -o "assets/img/$name.webp" ;;
    magick)  magick "assets/img/$name.png" -resize "1600x1600>" -quality 82 "assets/img/$name.webp" ;;
    convert) convert "assets/img/$name.png" -resize "1600x1600>" -quality 82 "assets/img/$name.webp" ;;
  esac
  rm -f "assets/img/$name.png"
  # CDN-link -> lokaal pad (previews staan in previews/, dus ../assets/img/)
  sed -i.bak "s|$url|../assets/img/$name.webp|g" previews/*.html
done
rm -f previews/*.bak
echo "Klaar. Lokale WebP in assets/img/, links in de designs vervangen."
du -sh assets/img
