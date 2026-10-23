"""Export approved editorial retouches to responsive WebP, preserving framing.

Usage: python export_exhibition_editorial.py input-map.json output-directory
Input map: {"11": "/path/to/approved-retouch.png", ...}.
"""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageOps

sources = json.loads(Path(sys.argv[1]).read_text())
output = Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
manifest = []
for number, source in sorted(sources.items(), key=lambda item: int(item[0])):
    original = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    variants = []
    for width in (640, 1120):
        width = min(width, original.width)
        height = round(original.height * width / original.width)
        image = original.resize((width, height), Image.Resampling.LANCZOS)
        temporary = output / f"exhibition-{number}-{width}.webp"
        image.save(temporary, "WEBP", quality=84, method=6)
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()[:12]
        final = temporary.with_name(f"exhibition-{number}-{width}-{digest}.webp")
        temporary.replace(final)
        variants.append({"file": final.name, "width": width, "height": height, "bytes": final.stat().st_size})
    manifest.append({"number": int(number), "variants": variants})
(output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"images": len(manifest), "bytes": sum(v["bytes"] for m in manifest for v in m["variants"])}))
