from pathlib import Path
from PIL import Image,ImageOps
import json,subprocess,xml.etree.ElementTree as E
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
R=Path(__file__).resolve().parents[2];U=R.parent/'upload';O=R/'public/assets/axion-case';O.mkdir(parents=True,exist_ok=True);m={}
def photo(k,f):
 im=ImageOps.exif_transpose(Image.open(f)).convert('RGB');v=[]
 for w in [640,min(1440,im.width)]:
  if v and v[-1]['width']==w:continue
  h=round(w*im.height/im.width);n=f'{k}-{w}.webp';im.resize((w,h),Image.Resampling.LANCZOS).save(O/n,quality=87,method=6);v.append(dict(src='/assets/axion-case/'+n,width=w,height=h))
 m[k]=v
for k,f in [('campaign','place holder axion controllers.webp'),('rear-detail','AXION__0000_DSC07010.jpg'),('grip-detail','AXION__0008_DSC07040.jpg'),('back','AXION__0013_DSC07051.jpg'),('top','AXION__0015_DSC07049.jpg'),('trigger-detail','AXION__0016_DSC07047.jpg'),('front','AXION__0019_Livello 0.jpg')]:photo(k,U/f)
for k,f in [('website-home','/workspace/scratch/axion-source-home.jpg')]:photo(k,Path(f))
# Bounded crops of the actual configurator panels, captured from the public website.
for key,name in [('ui-rear','axion-rear-viewport.jpg'),('ui-tmr','axion-tmr-viewport.jpg'),('ui-review','axion-review-viewport.jpg')]:
 im=Image.open(Path('/workspace/scratch')/name).convert('RGB').crop((680,250,1310,930));im.save(O/(key+'-630.webp'),quality=90,method=6);m[key]=[dict(src='/assets/axion-case/'+key+'-630.webp',width=630,height=680)]
# Preserve original transparent logo artwork; SVG groups contain wordmark and symbol.
root=E.fromstring((U/'axion-10 copia.svg').read_text());ns='{http://www.w3.org/2000/svg}'
for key,idx in [('wordmark',0),('symbol',1)]:
 g=root[idx];bounds=[]
 for el in g:
  pen=BoundsPen(None)
  if el.tag.endswith('path'):parse_path(el.attrib['d'],pen)
  elif el.tag.endswith('polygon'):
   points=list(map(float,el.attrib['points'].replace(',',' ').split()));pen.moveTo((points[0],points[1]));[pen.lineTo((points[i],points[i+1])) for i in range(2,len(points),2)];pen.closePath()
  if pen.bounds:bounds.append(pen.bounds)
 box=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds));x,y,x2,y2=box;w=x2-x;h=y2-y
 markup=E.tostring(g,encoding='unicode').replace('ns0:','').replace(':ns0','');svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">{markup}</svg>'
 (O/(key+'.svg')).write_text(svg);m[key]={'src':'/assets/axion-case/'+key+'.svg','box':box,'width':round(w),'height':round(h)}
 if key=='symbol':
  for part,children in [('diagonals',list(g)[:4]),('directions',list(g)[4:])]:
   content=''.join(E.tostring(el,encoding='unicode').replace('ns0:','').replace(':ns0','') for el in children);(O/(part+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">{content}</svg>')
for k,f in [('motion-back','close giro su back.mp4'),('motion-station','computer station.mp4'),('motion-material','sfera melted.mp4'),('motion-tmr','TMR tour.mp4')]:
 src=U/f;target=O/(k+'.mp4');subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-an','-vf','scale=960:-2','-c:v','libx264','-preset','slow','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True)
 poster=O/(k+'-poster.webp');subprocess.run(['ffmpeg','-y','-v','error','-ss','0.6','-i',str(target),'-frames:v','1',str(poster)],check=True)
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(target)]))['streams'][0];m[k]={'src':'/assets/axion-case/'+target.name,'poster':'/assets/axion-case/'+poster.name,**v}
(R/'scripts/project-sources/axion-case-assets.json').write_text(json.dumps(m,indent=2));print('assets MB',round(sum(f.stat().st_size for f in O.iterdir())/1e6,2));print('logo geometry',m['symbol'],m['wordmark'])
