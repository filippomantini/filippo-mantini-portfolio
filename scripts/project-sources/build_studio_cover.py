"""Native typographic sharing card; no generated product photography."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1200,630),'#191918');d=ImageDraw.Draw(im)
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
f=lambda size:ImageFont.truetype(regular,size)
m=lambda size:ImageFont.truetype(mono,size)
paper='#ece9e3';muted='#b9afa1'
d.text((48,38),'FILIPPO MANTINI / DIGITAL PRODUCT',font=m(13),fill=muted)
for i,line in enumerate(['FILIPPO','MANTINI','STUDIO.']):d.text((42,130+i*93),line,font=f(88),fill=paper if i<2 else muted,stroke_width=0)
d.line((48,487,530,487),fill='#555148',width=1)
d.text((48,509),'INTERFACE / WORKFLOWS / DESIGN',font=m(12),fill=muted)
d.text((48,557),'filippomantini.com',font=f(17),fill=paper)
d.rectangle((610,98,1152,544),fill='#efeee8')
d.line((728,98,728,544),fill='#d3d0c7',width=1)
d.text((628,123),'FILIPPO',font=f(16),fill='#191918');d.text((628,143),'MANTINI',font=f(16),fill='#191918')
for i,x in enumerate(['Oggi','Posta','Progetti','Produzione']):
 if i==0:d.rectangle((622,210,717,241),fill='#191918')
 d.text((632,218+i*39),x,font=f(10),fill='#efeee8' if i==0 else '#716f68')
d.text((750,124),'STUDIO / OVERVIEW',font=m(8),fill='#716f68')
d.line((750,151,1126,151),fill='#d3d0c7',width=1)
d.text((748,187),'Il lavoro,',font=f(43),fill='#191918');d.text((748,237),'in ordine.',font=f(43),fill='#191918')
d.line((750,319,1126,319),fill='#191918',width=1)
for i,lab in enumerate(['POSTA','PROGETTI','REVISIONE']):
 x=750+i*128;d.text((x,338),lab,font=m(8),fill='#716f68');d.text((x,363),str([3,2,1][i]),font=f(39),fill='#191918')
for i,lab in enumerate(['Richieste e preventivi','Documenti di progetto','Newsletter e promozioni']):
 y=430+i*29;d.line((750,y+22,1126,y+22),fill='#d3d0c7');d.text((750,y),lab,font=f(10),fill='#716f68')
d.text((976,571),'STUDIO / CASE STUDY',font=m(10),fill=muted)
out=R/'public/assets/studio/studio-cover.png';out.parent.mkdir(parents=True,exist_ok=True);im.save(out,optimize=True)
print(out, out.stat().st_size)
