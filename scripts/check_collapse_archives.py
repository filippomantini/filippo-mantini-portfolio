"""Verify archive consolidation, bilingual metadata and media dimensions."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];M=json.loads((ROOT/'scripts/project-sources/collapse-archive-assets.json').read_text())
class Page(HTMLParser):
 def __init__(self):super().__init__();self.img=[];self.video=[];self.link=[];self.a=[];self.ids=[];self.h1=0;self.iframe=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='img':self.img.append(a)
  if tag=='video':self.video.append(a)
  if tag=='link':self.link.append(a)
  if tag=='a':self.a.append(a)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='iframe':self.iframe+=1
for lang in ['en','it']:
 prefix='/it' if lang=='it' else '';base=ROOT/('public/it' if lang=='it' else 'public')/'work/collapse'
 for slug,photos,videos in [('ss25-capsule-01',12,2),('fw24-25',25,0),('fw23-24',13,4)]:
  s=(base/'collections'/slug/'index.html').read_text();d=Page();d.feed(s)
  assert d.h1==1 and d.iframe==0 and len(d.img)==photos and len(d.video)==videos,(slug,len(d.img),len(d.video))
  assert len(d.ids)==len(set(d.ids)),'Duplicate section IDs'
  assert len([a for a in d.img if a.get('fetchpriority')=='high'])==1
  for a in d.img:
   assert a.get('alt') and a.get('width') and a.get('height') and a.get('srcset')
   if a['src'].startswith('/assets/collapse/archive/'):assert (ROOT/'public'/a['src'].lstrip('/')).exists(),a['src']
  for a in d.video:
   assert a['preload']=='none' and 'controls' in a and 'playsinline' in a and 'autoplay' not in a
   assert (int(a['width'])==int(a['height']))==(slug=='fw23-24')
  assert not any('/collections/ss24/' in a.get('href','') for a in d.a)
  canonical=next(a['href'] for a in d.link if a.get('rel')=='canonical');assert canonical=='https://filippomantini.com'+prefix+'/work/collapse/collections/'+slug+'/'
  assert {a.get('hreflang') for a in d.link if a.get('rel')=='alternate'}>={'en','it','x-default'}
  for a in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',s):json.loads(a)
  if slug=='fw24-25':
   assert {'fw24-25','ss24','graphic-system'}.issubset(d.ids)
   assert 'instagram-ss24-' in s and 'instagram-fw24-25-' in s
   nav=re.search(r'<nav class="cc-paginate"[\s\S]*?</nav>',s)[0];assert '/collections/fw24-25/' not in nav,'Merged page cannot paginate to itself'
  if slug=='fw23-24':assert '<h2>Fe26</h2>' in s and '<title>Fe26' in s and 'not been supplied' not in s and 'non è ancora' not in s
  print(lang,slug,': editorial media, SEO, IDs and links passed')
 home=(base/'index.html').read_text();assert home.count('class="cp-collection"')==6
 assert 'href="'+prefix+'/work/collapse/collections/ss24/' not in home
 assert '<strong>Fe26</strong>' in home and '<strong>FW24/25 + SS24</strong>' in home
rules=(ROOT/'public/_redirects').read_text()
for prefix in ['', '/it']:
 for ending in ['', '/', '/index.html']:assert prefix+'/work/collapse/collections/ss24'+ending+' '+prefix+'/work/collapse/collections/fw24-25/ 301' in rules
sitemap=(ROOT/'public/sitemap.xml').read_text();ET.fromstring(sitemap);assert '/collections/ss24/' not in sitemap
for key,v in M.items():
 if not isinstance(v,dict):continue
 p=ROOT/'public/assets/collapse/archive'/v['file'];info=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','stream=codec_type,width,height','-of','json',str(p)]));video=next(x for x in info['streams'] if x['codec_type']=='video');assert (video['width'],video['height'])==(v['width'],v['height'])
print('Redirect variants, parent cards, sitemap and all 6 video dimensions passed')
