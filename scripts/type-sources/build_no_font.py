"""Convert original Illustrator PDF outlines to a proof webfont; no glyphs redrawn.
Dependencies: pymupdf, skia-pathops, fonttools[woff], pillow.
Usage: python build_no_font.py /path/to/font-specimen.ai /path/to/output
"""
from pathlib import Path
import sys,json
import fitz,pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
drawings=fitz.open(source)[1].get_drawings()[:-1] # Final orange X is an editorial overlay.
rows=[('ABCDEFGHIJKLMN',[43,44,50,51,56,123,124,125,57,58,126,127,59,128],149.3),('OPQRSTUVWXYZÀ',[60,61,18,64,65,66,67,68,69,70,17,19,12],223.3),('ÅÉÎÕabcdefghijklmn',[7,6,5,4,73,74,75,24,79,129,80,25,87,26,27,92,93,130],301.3),('opqrstuvwxyzàåéî&1',[94,28,29,103,104,131,30,31,32,33,119,34,3,2,1,0,38,120],372.3),('234567890($£€.,!?)',[121,122,134,135,136,137,138,139,140,143,144,145,146,141,142,148,150,151],449.3)]
main={idx:(char,base) for text,indices,base in rows for char,idx in zip(text,indices,strict=True)}
groups={idx:[] for idx in main}
def distance(a,b):
 x,y=(a.x0+a.x1)/2,(a.y0+a.y1)/2
 return max(b.x0-x,0,x-b.x1)**2+max(b.y0-y,0,y-b.y1)**2
for i,d in enumerate(drawings):
 owner=i if i in main else min(main,key=lambda j:distance(d['rect'],drawings[j]['rect']))
 groups[owner].append(i)
def path(d):
 p=pathops.Path();last=None
 for item in d['items']:
  kind=item[0];assert kind in ('l','c'),kind
  st,end=item[1],item[-1]
  if last is None or abs(st.x-last.x)>.005 or abs(st.y-last.y)>.005:
   if last is not None:p.close()
   p.moveTo(st.x,st.y)
  if kind=='l':p.lineTo(end.x,end.y)
  else:p.cubicTo(*[v for pt in item[2:] for v in (pt.x,pt.y)])
  last=end
 if last is not None:p.close()
 p.fillType=pathops.FillType.EVEN_ODD if d['even_odd'] else pathops.FillType.WINDING
 p.simplify()
 return p
scale=700/39.4;order=['.notdef','space'];glyphs={};metrics={};cmap={32:'space'};manifest=[]
p=TTGlyphPen(None);p.moveTo((50,0));p.lineTo((450,0));p.lineTo((450,700));p.lineTo((50,700));p.closePath();p.moveTo((100,50));p.lineTo((100,650));p.lineTo((400,650));p.lineTo((400,50));p.closePath();glyphs['.notdef']=p.glyph();metrics['.notdef']=(500,50)
glyphs['space']=TTGlyphPen(None).glyph();metrics['space']=(300,0)
for idx,(char,baseline) in main.items():
 combined=pathops.Path()
 for i in groups[idx]:
  d=drawings[i];p=path(d);white=min(d['fill'])>.9
  combined=pathops.op(combined,p,pathops.PathOp.DIFFERENCE if white else pathops.PathOp.UNION)
 x0,y0,x1,y1=combined.bounds
 name='uni%04X'%ord(char);order.append(name);cmap[ord(char)]=name
 pen=TTGlyphPen(None);quadratic=Cu2QuPen(pen,max_err=.25,reverse_direction=False)
 combined.draw(TransformPen(quadratic,(scale,0,0,-scale,55-x0*scale,baseline*scale)))
 glyphs[name]=pen.glyph();metrics[name]=(round((x1-x0)*scale+110),55)
 manifest.append({'character':char,'unicode':ord(char),'page':2,'primary':idx,'components':groups[idx],'advance':metrics[name][0]})
fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=100)
fb.setupNameTable({'familyName':'No Font Prototype','styleName':'Regular','uniqueFontIdentifier':'FilippoMantini:NoFontPrototype:0.1','fullName':'No Font Prototype Regular','psName':'NoFontPrototype-Regular','version':'Version 0.100','copyright':'Original letterforms by Filippo Mantini. Prototype outline conversion 2026. Distribution terms to be defined by the author.','designer':'Filippo Mantini','description':'Prototype from original vector specimen, page 2. Initial sidebearings, no optical kerning. Only glyphs present in the source are included.'})
fb.setupOS2(sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=100,usWinAscent=1050,usWinDescent=300,sCapHeight=700,sxHeight=510,fsType=0);fb.setupPost();fb.setupMaxp();fb.save(out/'NoFontPrototype-Regular.ttf')
f=TTFont(out/'NoFontPrototype-Regular.ttf');f.flavor='woff2';f.save(out/'NoFontPrototype-Regular.woff2')
(out/'glyph-source-map.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for ext in ['ttf','woff2']:assert TTFont(out/('NoFontPrototype-Regular.'+ext)).getBestCmap()==cmap
im=Image.new('RGB',(1500,1100),'white');dr=ImageDraw.Draw(im);font=ImageFont.truetype(str(out/'NoFontPrototype-Regular.ttf'),65)
for i,r in enumerate(rows):dr.text((30,20+i*150),r[0],font=font,fill='black')
dr.text((30,800),'No Font / Filippo Mantini',font=font,fill='black');dr.text((30,940),'The right spacing is the most important thing.',font=ImageFont.truetype(str(out/'NoFontPrototype-Regular.ttf'),45),fill='black');im.save(out/'proof.png')
print('Verified',len(cmap),'Unicode characters. WOFF2', (out/'NoFontPrototype-Regular.woff2').stat().st_size,'bytes')
print(''.join(chr(c) for c in sorted(cmap)))
