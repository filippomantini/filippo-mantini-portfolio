"""Compress the two supplied original unisex look photographs, without edits."""
from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'public/assets/collapse/archive';OUT.mkdir(parents=True,exist_ok=True);P=Path(__file__).parent/'collapse-archive-assets.json';m=json.loads(P.read_text())
for key,name in [('fw24ss24-fluidity-man','3:4 FRONT FELPA.jpg'),('fw24ss24-fluidity-woman','_MG_9087.jpg')]:
 im=ImageOps.exif_transpose(Image.open(ROOT.parent/'upload'/name)).convert('RGB');variants=[]
 for width in [640,1200]:
  height=round(width*im.height/im.width);p=OUT/f'{key}-{width}.webp';im.resize((width,height),Image.Resampling.LANCZOS).save(p,'WEBP',quality=86,method=6);digest=hashlib.sha256(p.read_bytes()).hexdigest()[:12];dest=p.with_name(f'{key}-{width}-{digest}.webp');p.replace(dest);variants.append({'file':dest.name,'width':width,'height':height,'bytes':dest.stat().st_size})
 m[key]=variants
P.write_text(json.dumps(m,indent=2)+'\n')
