"""Exact five-letter display font from the full, uncropped original PDF artwork."""
from pathlib import Path
import fitz,pathops,json,hashlib
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
R=Path(__file__).resolve().parents[2];O=R/'public/assets/axion-communications';U=R.parent/'upload'
page=fitz.open(next(U.glob('font axion*')))[0];letters={c:pathops.Path() for c in 'AXION'}
for drawing in page.get_drawings():
 if drawing['fill']!=(1.,1.,1.):continue
 cx=(drawing['rect'].x0+drawing['rect'].x1)/2
 letter=next(c for c,end in zip('AXION',[1130,2140,2630,3760,5000]) if cx<end)
 outline=pathops.Path();pen=outline.getPen();current=None
 for item in drawing['items']:
  start=item[1]
  if current is None or abs(current.x-start.x)>.01 or abs(current.y-start.y)>.01:
   if current is not None:pen.closePath()
   pen.moveTo(tuple(round(v,4) for v in start))
  if item[0]=='l':pen.lineTo(tuple(round(v,4) for v in item[2]));current=item[2]
  elif item[0]=='c':pen.curveTo(*[tuple(round(v,4) for v in x) for x in item[2:]]);current=item[-1]
  else:raise ValueError(item[0])
 if current is not None:pen.closePath()
 letters[letter]=pathops.op(letters[letter],outline,pathops.PathOp.UNION)
scale=800/page.rect.height
bounds={c:p.bounds for c,p in letters.items()}
fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(['.notdef','space']+list('AXION'));glyphs={'.notdef':TTGlyphPen(None).glyph(),'space':TTGlyphPen(None).glyph()};metrics={'.notdef':(650,0),'space':(300,0)}
for index,(c,outline) in enumerate(letters.items()):
 xmin,ymin,xmax,ymax=bounds[c];pen=TTGlyphPen(None);curves=Cu2QuPen(pen,.2,reverse_direction=False);outline.draw(TransformPen(curves,(scale,0,0,-scale,-xmin*scale,800)))
 glyphs[c]=pen.glyph()
 # Preserve the original AXION sequence, including its unequal letter widths and spacing.
 advance=((bounds['AXION'[index+1]][0]-xmin) if index<4 else xmax-xmin+90)*scale
 metrics[c]=(round(advance),0)
fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=850,descent=-150);fb.setupCharacterMap({ord(c):c.upper() for c in 'AXIONaxion'}|{32:'space'})
fb.setupNameTable({'familyName':'Axion Button Display','styleName':'Regular','uniqueFontIdentifier':'AxionButtonDisplay-Master-2026-v2','fullName':'Axion Button Display Regular','psName':'AxionButtonDisplay-Regular','version':'Version 0.2; original master outlines; A X I O N','copyright':'Original lettering supplied by Filippo Mantini. Digital font adaptation 2026.'})
fb.setupOS2(sTypoAscender=850,sTypoDescender=-150,usWinAscent=850,usWinDescent=150);fb.setupPost();fb.setupMaxp()
from io import BytesIO
buf=BytesIO();fb.font.save(buf);raw=buf.getvalue();ttf='axion-button-display-'+hashlib.sha256(raw).hexdigest()[:12]+'.ttf';(O/ttf).write_bytes(raw)
font=TTFont(BytesIO(raw));font.flavor='woff2';buf=BytesIO();font.save(buf);raw=buf.getvalue();woff='axion-button-display-'+hashlib.sha256(raw).hexdigest()[:12]+'.woff2';(O/woff).write_bytes(raw)
manifest={'ttf':'/assets/axion-communications/'+ttf,'woff2':'/assets/axion-communications/'+woff,'source':'PDF page 1: full original AXION composition','characters':'AXIONaxion ','bounds':bounds,'scale':scale}
(R/'scripts/project-sources/axion-lettering-font.json').write_text(json.dumps(manifest,indent=2));print(ttf,woff)
