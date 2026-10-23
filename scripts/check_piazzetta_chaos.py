from pathlib import Path
from html.parser import HTMLParser
import json,re
R=Path(__file__).resolve().parents[1]
class Check(HTMLParser):
 def __init__(self):super().__init__();self.h=0;self.img=0;self.vid=0;self.alt=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h+=1
  if tag=='img':
   self.img+=1;assert a.get('alt');assert a.get('width') and a.get('height')
  if tag=='video':self.vid+=1;assert a.get('preload')=='none';assert 'controls' in a and 'playsinline' in a
  if tag in ['img','source'] and a.get('src'):assert (R/'public'/a['src'].lstrip('/')).exists(),a['src']
  if tag=='link' and a.get('hreflang'):self.alt+=1
for lang in ['', 'it/']:
 for slug in ['bar-la-piazzetta','chaos-as-duality']:
  p=R/f'public/{lang}work/{slug}/index.html';s=p.read_text();c=Check();c.feed(s);assert c.h==1 and c.alt==3
  assert 'Project material /' not in s and 'archive will be' not in s
  for v in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s):json.loads(v)
  print(lang+slug,c.img,'images',c.vid,'videos')
print('Structure, media paths, responsive dimensions, video loading and SEO passed')
