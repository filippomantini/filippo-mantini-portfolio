"""Responsive exports for the supplied SS25 Capsule 02 campaign photographs.
Originals are kept outside the repository. Two approved tonal-retouch derivatives
are used for the rail and denim close-up; other photographs are unchanged.
"""
from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];UPLOAD=ROOT.parent/'upload';OUT=ROOT/'public/assets/collapse/ss25-capsule-02';OUT.mkdir(parents=True,exist_ok=True)
SOURCES={
'campaign-group':'17.02 1.jpg','campaign-cars':'gaia panda 01.jpg','bedroom':'post 14.02.jpg','chess':'scacchi 03.jpg','raglan-look':'0001.jpg','wardrobe':'004.jpg','flowers-room':'Fiori Post 21_02 2.jpg','flowers-detail':'Fiori Post 21_02 3(1).jpg','flowers-poster':'Fiori Post 21_02 4.jpg','flowers-still':'Fiori Post 21_02 ok.jpg','campaign-duo':'17.02 2.jpg','campaign-stairs':'17.02 6.jpg','cars-detail':'gaia panda 04.jpg','set-documentation':'Screenshot 2025-02-13 alle 11.10.32\u202fAM.png','graphic-composition':'5830AB60-4DB2-45C7-AC6A-570D03698E9C.JPG','lovers-wordmark':'scritta lovers.PNG',
'product-rail':'../generated_images/exec-9bac37c9-b254-46b6-86e0-8cd607d54497.png','denim-study':'../generated_images/exec-edb43b12-c537-4e19-a5c6-386678ce60fd.png',
'campaign-film-poster':'../ss25-capsule-review/campaign-poster.jpg','bts-film-poster':'../ss25-capsule-review/film-02.jpg'}
manifest={}
for key,name in SOURCES.items():
 im=ImageOps.exif_transpose(Image.open(UPLOAD/name)).convert('RGB');variants=[]
 widths=(462,) if key=='campaign-film-poster' else (640,1200)
 for w in widths:
  w=min(w,im.width)
  if any(x['width']==w for x in variants):continue
  h=round(w*im.height/im.width);out=im.resize((w,h),Image.Resampling.LANCZOS);temp=OUT/f'{key}-{w}.webp';out.save(temp,'WEBP',quality=88 if key in ['flowers-poster','lovers-wordmark','graphic-composition'] else 84,method=6)
  digest=hashlib.sha256(temp.read_bytes()).hexdigest()[:12];dest=temp.with_name(f'{key}-{w}-{digest}.webp');temp.replace(dest);variants.append({'file':dest.name,'width':w,'height':h,'bytes':dest.stat().st_size})
 manifest[key]=variants
for key in ['campaign-film','behind-the-scenes']:
 p=OUT/f'{key}.mp4';digest=hashlib.sha256(p.read_bytes()).hexdigest()[:12];dest=p.with_name(f'{key}-{digest}.mp4');p.rename(dest);manifest[key]={'file':dest.name,'bytes':dest.stat().st_size,'width':462 if key=='campaign-film' else 720,'height':822 if key=='campaign-film' else 1280}
(ROOT/'scripts/project-sources/ss25-capsule-02-assets.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'image_bytes':sum(x['bytes'] for v in manifest.values() if isinstance(v,list) for x in v),'video_bytes':sum(v['bytes'] for v in manifest.values() if isinstance(v,dict))}))
