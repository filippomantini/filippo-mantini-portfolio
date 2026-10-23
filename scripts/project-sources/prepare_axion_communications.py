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
# The supplied PDF contains only A, X, I, O, N. Preserve those outlines;
# do not invent the rest of an alphabet or present it as a complete typeface.
doc=fitz.open(next(U.glob('font axion*')))
fb=FontBuilder(1000,isTTF=True);order=['.notdef','space']+list('AXION');fb.setupGlyphOrder(order)
glyphs={};metrics={'.notdef':(650,0),'space':(330,0)}
pen=TTGlyphPen(None);pen.moveTo((60,0));pen.lineTo((60,800));pen.lineTo((560,800));pen.lineTo((560,0));pen.closePath();pen.moveTo((110,50));pen.lineTo((510,50));pen.lineTo((510,750));pen.lineTo((110,750));pen.closePath();glyphs['.notdef']=pen.glyph();glyphs['space']=TTGlyphPen(None).glyph()
for i,letter in enumerate('AXION',1):
 page=doc[i];W=page.rect.width;scale=800/W
 # White figure is negative space between the blue vector shapes.
 outline=pathops.Path();p=outline.getPen();p.moveTo((0,0));p.lineTo((W,0));p.lineTo((W,W));p.lineTo((0,W));p.closePath()
 for d in page.get_drawings():
  if not d['fill'] or d['fill'][2]<.8:continue
  blue=pathops.Path();bp=blue.getPen();current=None
  for item in d['items']:
   typ=item[0];start=item[1]
   if typ=='re':
    rr=item[1];bp.moveTo((rr.x0,rr.y0));bp.lineTo((rr.x1,rr.y0));bp.lineTo((rr.x1,rr.y1));bp.lineTo((rr.x0,rr.y1));bp.closePath();continue
   if current is None or abs(current.x-start.x)>.02 or abs(current.y-start.y)>.02:
    if current is not None:bp.closePath()
    bp.moveTo(tuple(round(v,3) for v in start))
   if typ=='l':bp.lineTo(tuple(round(v,3) for v in item[2]));current=item[2]
   elif typ=='c':bp.curveTo(*[tuple(round(v,3) for v in x) for x in item[2:]]);current=item[-1]
  if current is not None:bp.closePath()
  try:outline=pathops.op(outline,blue,pathops.PathOp.DIFFERENCE)
  except Exception:
   print('failed',letter,d['rect'],len(d['items']));raise
 clean=pathops.Path()
 for contour in outline.contours:
  if abs(contour.area)>1:clean.addPath(contour)
 outline=clean
 xmin,ymin,xmax,ymax=outline.bounds
 pen=TTGlyphPen(None);q=Cu2QuPen(pen,1.0,reverse_direction=False);trans=TransformPen(q,(scale,0,0,-scale,60-xmin*scale,800));outline.draw(trans)
 glyphs[letter]=pen.glyph();metrics[letter]=(round((xmax-xmin)*scale)+120,60)
fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=880,descent=-120);fb.setupCharacterMap({ord(c):c.upper() for c in 'AXIONaxion'}|{32:'space'})
fb.setupNameTable({'familyName':'Axion Button Display','styleName':'Regular','uniqueFontIdentifier':'AxionButtonDisplay-2026','fullName':'Axion Button Display Regular','psName':'AxionButtonDisplay-Regular','version':'Version 0.1; five original letters A X I O N','copyright':'Original lettering supplied by Filippo Mantini. Digital font adaptation 2026.'})
fb.setupOS2(sTypoAscender=880,sTypoDescender=-120,usWinAscent=880,usWinDescent=120);fb.setupPost();fb.setupMaxp();fb.save(O/'axion-button-display.ttf');font=TTFont(O/'axion-button-display.ttf');font.flavor='woff2';font.save(O/'axion-button-display.woff2')
# Exact artwork as a specimen: no font rasterisation or redesign.
pix=doc[0].get_pixmap(matrix=fitz.Matrix(.4,.4),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.save(O/'button-lettering.webp',quality=92)
(R/'scripts/project-sources/axion-communications-assets.json').write_text(json.dumps(manifest,indent=2))
print('media bytes',sum(x.stat().st_size for x in O.iterdir()))
