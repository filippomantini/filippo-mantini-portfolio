"""Regression check: one same-garment comparison and an ordered separate gallery."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
ROOT=Path(__file__).resolve().parents[1]
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
for locale in ['en','it']:
 p=ROOT/('public/it' if locale=='it' else 'public')/'work/collapse/collections/fw24-25/index.html';s=p.read_text();a=s.split('id="fw24-25"',1)[1];fluidity,gallery=a.split('id="ss24"',1);gallery=gallery.split('id="graphic-system"',1)[0]
 f=Images();f.feed(fluidity);g=Images();g.feed(gallery)
 assert len(f.images)==2,'Fluidity must only show the two same-garment images'
 assert 'fluidity-woman' in f.images[0]['src'] and 'fluidity-man' in f.images[1]['src']
 assert all(float(a['height'])/float(a['width'])>1.49 for a in f.images)
 assert len(g.images)==16 and len({a['src'] for a in g.images})==16
 assert 'OFF THE GRID' not in gallery and 'FOOTBALL TEAM' not in gallery
 assert 'unisex' in fluidity.lower()
 for a in f.images:assert (ROOT/'public'/a['src'].lstrip('/')).exists()
 assert s.count('<h1>')==1 and s.count('ARCHIVE_STORY_START')==1
 assert 'fw24ss24-08-' not in s,'Unrelated portrait removed from garment gallery'
 for a in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',s):json.loads(a)
 print(locale+': unisex pair, gallery separation, unique photographs and metadata passed')
