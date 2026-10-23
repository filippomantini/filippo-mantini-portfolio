"""Export approved public presentation assets, never raw attendee data or video."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps
import qrcode

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/assets/collapse-event-system'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = {
 'hero': (ROOT.parent / 'generated_images/exec-66254ce7-228f-4de1-9934-4b13242897ea.png', (800,1440)),
 'ticket': (ROOT / 'inputs/input-08.png', (400,720)),
 'scanner': (ROOT / 'inputs/input-09.png', (900,1600)),
 'validation': (ROOT / 'inputs/input-02.png', (900,1600)),
}
manifest = {}
for name, (source, widths) in SOURCES.items():
 im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
 variants = []
 for width in widths:
  height = round(im.height * width / im.width)
  resized = im.resize((width,height),Image.Resampling.LANCZOS)
  temp = OUT / f'{name}-{width}.webp'
  resized.save(temp,'WEBP',quality=86,method=6)
  digest = hashlib.sha256(temp.read_bytes()).hexdigest()[:12]
  final = temp.with_name(f'{name}-{width}-{digest}.webp')
  temp.replace(final)
  variants.append({'file':final.name,'width':width,'height':height,'bytes':final.stat().st_size})
 manifest[name] = variants

(ROOT/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Approved original ticket exported')
