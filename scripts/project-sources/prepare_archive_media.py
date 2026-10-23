"""Export supplied COLLAPSE archives without cropping or generative changes.
Inputs remain outside the repository. Original metadata is removed from exports.
"""
from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'public/assets/collapse/archive';OUT.mkdir(parents=True,exist_ok=True)
inputs=json.loads((Path(__file__).parent/'collapse-archive-inputs.json').read_text());manifest={}
def export(im,key,widths):
 im=ImageOps.exif_transpose(im).convert('RGB');variants=[]
 for width in widths:
  width=min(width,im.width)
  if any(a['width']==width for a in variants):continue
  height=round(width*im.height/im.width);p=OUT/f'{key}-{width}.webp';im.resize((width,height),Image.Resampling.LANCZOS).save(p,'WEBP',quality=86,method=6);h=hashlib.sha256(p.read_bytes()).hexdigest()[:12];dest=p.with_name(f'{key}-{width}-{h}.webp');p.replace(dest);variants.append({'file':dest.name,'width':width,'height':height,'bytes':dest.stat().st_size})
 return variants
for group,items in inputs.items():
 for a in items:
  key=group+'-'+a['id'];src=ROOT/a['file']
  if 'width' in a:
   manifest[key]=export(Image.open(src),key,(640,1200));continue
  is_square=group=='fe26';scale='720:720' if is_square else '720:1280';temp=OUT/f'{key}.mp4'
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-map','0:v:0','-map','0:a:0?','-vf','fps=30,scale='+scale+',setsar=1','-c:v','libx264','-preset','slow','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-map_metadata','-1','-movflags','+faststart',str(temp)],check=True)
  digest=hashlib.sha256(temp.read_bytes()).hexdigest()[:12];dest=temp.with_name(f'{key}-{digest}.mp4');temp.replace(dest);manifest[key]={'file':dest.name,'width':720,'height':720 if is_square else 1280,'bytes':dest.stat().st_size,'duration':float(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',str(dest)]).strip())}
  poster=ROOT/f'{key}-preview.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss','6' if group=='capsule01' and a['id']=='12' else '3','-i',str(src),'-frames:v','1',str(poster)],check=True);manifest[key+'-poster']=export(Image.open(poster),key+'-poster',(640,))
  print(key,manifest[key]['bytes'],flush=True)
(ROOT/'scripts/project-sources/collapse-archive-assets.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'entries':len(manifest),'bytes':sum(sum(x['bytes'] for x in v) if isinstance(v,list) else v['bytes'] for v in manifest.values())}),flush=True)
