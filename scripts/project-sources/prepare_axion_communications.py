"""Prepare original Axion communication assets and five-glyph display font."""
from pathlib import Path
import json,subprocess,zipfile,fitz,pathops,io
from PIL import Image
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib import TTFont
R=Path(__file__).resolve().parents[2]; U=R.parent/'upload';O=R/'public/assets/axion-communications';O.mkdir(parents=True,exist_ok=True)
manifest={}
inputs={'banner-red':U/'banner siito internet 01.jpg','banner-grey':U/'banner sito internet.jpg','twitch-poster':U/'banner twich 01.jpg','colours-story':U/'axion storia nuove colorsazioni.jpg','board-explained':U/'post-scheda_01.jpg','board-launch':U/'post-scheda.jpg','board-detail':U/'per-sito-marius-board.jpg'}
for arch in ['post IG AXION.zip','tmr axion.zip']:
 with zipfile.ZipFile(U/arch) as z:
  for i,n in enumerate(x for x in z.namelist() if not x.startswith('__MACOSX') and x.lower().endswith('.jpg')):
   folder=R/'revision'/Path(arch).stem;folder.mkdir(exist_ok=True);p=folder/Path(n).name;p.write_bytes(z.read(n))
   inputs[('social-' if arch.startswith('post') else 'tmr-')+str(i+1)]=p
for name,p in inputs.items():
 im=Image.open(p).convert('RGB');vs=[]
 for width in [480,960,1600]:
  w=min(width,im.width)
  if vs and w==vs[-1]['width']:continue
  h=round(im.height*w/im.width);dest=O/f'{name}-{w}.webp';encoded=io.BytesIO();im.resize((w,h),Image.Resampling.LANCZOS).save(encoded,format='WEBP',quality=87,method=6);dest.write_bytes(encoded.getvalue())
  vs.append({'src':'/assets/axion-communications/'+dest.name,'width':w,'height':h})
 manifest[name]=vs
v=U/'banner twich.mp4'; info=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(v)]));s=next(x for x in info['streams'] if x['codec_type']=='video');print('twitch',s['width'],s['height'],info['format']['duration'])
subprocess.run(['ffmpeg','-y','-v','error','-i',str(v),'-an','-vf','scale=960:-2','-c:v','libx264','-preset','slow','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'twitch-banner.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-ss','0.4','-i',str(v),'-frames:v','1','-vf','scale=960:-2',str(O/'twitch-banner-poster.webp')],check=True)
# Use the full original composition, never the cropped per-letter study pages.
subprocess.run(['python',str(R/'scripts/project-sources/build_axion_lettering.py')],check=True)
(R/'scripts/project-sources/axion-communications-assets.json').write_text(json.dumps(manifest,indent=2))
print('media bytes',sum(x.stat().st_size for x in O.iterdir()))
