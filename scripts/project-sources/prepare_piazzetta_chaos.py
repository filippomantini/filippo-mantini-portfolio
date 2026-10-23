from pathlib import Path
from PIL import Image
import fitz,json,subprocess
ROOT=Path(__file__).resolve().parents[2]; src=ROOT/'source';out=ROOT/'public/assets/piazzetta-chaos';out.mkdir(parents=True,exist_ok=True)
P=src/'PIAZZETTA/PIAZZETTA';C=src/'chaos as duality/chaos as duality';manifest={}
def image(key,path):
 im=Image.open(path).convert('RGB'); variants=[]
 for w in [640,1400]:
  w=min(w,im.width)
  if variants and variants[-1]['width']==w:continue
  h=round(im.height*w/im.width);name=f'{key if key != "wristband" else "wristband-folded-v2"}-{w}.webp';im.resize((w,h),Image.Resampling.LANCZOS).save(out/name,quality=86,method=6);variants.append(dict(src='/assets/piazzetta-chaos/'+name,width=w,height=h))
 manifest[key]=variants
for key,f in [('blp-poster',P/'poster 70x100.jpg'),('brochure',P/'BROCHURE 1.jpg'),('drink-menu',P/'04.jpg'),('dj-story',P/'111.jpg'),('gift-story',P/'112.jpg'),('drink-collasso',P/'drink1.jpg'),('drink-cookie',P/'cookie.jpg'),('drink-flash',P/'flash.jpg'),('drink-ivy',P/'ivy.jpg'),('chaos-preparty',C/'blp story1.jpg'),('invitation',C/'C6EFF07A-D422-4287-BF13-44E9D2750C29.JPG'),('lanyard',ROOT/'lanyard-source-0.jpeg'),('wristband',ROOT.parent/'generated_images/exec-8ef181c7-1b56-4435-9b0b-752b21569d19.png')]:image(key,f)
for key,f,pg in [('chaos-poster',C/'stampa poster.pdf',0),('chaos-drinks',C/'flyer.pdf',1),('wristband-artwork',C/'500pieces.pdf',0)]:
 d=fitz.open(f);page=d[pg];scale=1800/page.rect.width;temp=ROOT/(key+'.png');page.get_pixmap(matrix=fitz.Matrix(scale,scale)).save(temp);image(key,temp)
d=fitz.open(P/'CLPS X PIAZZETTA.pdf')
# Preserve the original presentation: these are concept proposals, not event photography.
for key,pg in [('venue-proposal',11),('console-proposal',26)]:
 page=d[pg];temp=ROOT/(key+'.png');page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(temp);image(key,temp)
for key,f,width in [('blp-film',P/'PIAZZETTA.MP4',960),('preparty-film',C/'storiaa piazzetta.mp4',540)]:
 target=out/(key+'.mp4');subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf',f'scale={width}:-2','-c:v','libx264','-preset','slow','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',str(target)],check=True)
 poster=out/(key+'-poster.webp');subprocess.run(['ffmpeg','-y','-v','error','-ss','1','-i',str(target),'-frames:v','1',str(poster)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(target)]))['streams'][0]
 manifest[key]={'src':'/assets/piazzetta-chaos/'+target.name,'poster':'/assets/piazzetta-chaos/'+poster.name,**probe}
(ROOT/'scripts/project-sources/piazzetta-chaos-assets.json').write_text(json.dumps(manifest,indent=2))
print('assets',len(list(out.iterdir())),'bytes',sum(f.stat().st_size for f in out.iterdir()))
