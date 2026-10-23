from pathlib import Path
from PIL import Image,ImageOps
import json,subprocess
R=Path(__file__).resolve().parents[2];U=R.parent/'upload';O=R/'public/assets/piazzetta-chaos';O.mkdir(parents=True,exist_ok=True);p=R/'scripts/project-sources/piazzetta-chaos-assets.json';m=json.loads(p.read_text())
for key,name in [('chaos-crowd-portrait','e5f3c292-0d16-4355-8cf0-24615d99e08e.JPG'),('chaos-dj-booth','IMG_6471.jpg'),('chaos-room','IMG_6472.jpg'),('chaos-crowd-wide','IMG_6497 2.jpg'),('chaos-wristbands-original','IMG_6182.jpg')]:
 im=ImageOps.exif_transpose(Image.open(U/name)).convert('RGB');vs=[]
 for w in [640,min(1400,im.width)]:
  if vs and vs[-1]['width']==w:continue
  h=round(im.height*w/im.width);n=f'{key}-{w}.webp';im.resize((w,h),Image.Resampling.LANCZOS).save(O/n,quality=87,method=6);vs.append(dict(src='/assets/piazzetta-chaos/'+n,width=w,height=h))
 m[key]=vs
src=U/'9c4935993f33490a886fee55fec11862.MOV';out=O/'chaos-original-night.mp4';subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-c:v','libx264','-preset','slow','-crf','26','-maxrate','1200k','-bufsize','2400k','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',str(out)],check=True)
poster=O/'chaos-original-night-poster.webp';subprocess.run(['ffmpeg','-v','error','-y','-ss','1','-i',str(out),'-frames:v','1',str(poster)],check=True)
m['chaos-night-film']=dict(src='/assets/piazzetta-chaos/'+out.name,poster='/assets/piazzetta-chaos/'+poster.name,width=538,height=960);p.write_text(json.dumps(m,indent=2));print('new assets',len(list(O.iterdir())),'bytes',sum(x.stat().st_size for x in O.iterdir()))
