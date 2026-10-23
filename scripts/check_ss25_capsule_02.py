"""Check both collection pages and their locally authored media contracts."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.images=[];self.videos=[];self.h1=0;self.sources=[];self.iframes=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='img':self.images.append(a)
  if tag=='video':self.videos.append(a)
  if tag=='source':self.sources.append(a)
  if tag=='iframe':self.iframes.append(a)
  if tag=='link':self.links.append(a)
for locale in ['it','en']:
 p=ROOT/('public/it' if locale=='it' else 'public')/'work/collapse/collections/ss25-capsule-02/index.html';s=p.read_text();d=Page();d.feed(s)
 assert d.h1==1 and len(d.videos)==2 and len(d.images)==19
 assert not d.iframes,'Campaign must not depend on an Instagram embed'
 assert s.count('SS25_STORY_START')==1 and s.count('SS25_STORY_END')==1
 assert len([i for i in d.images if i.get('fetchpriority')=='high'])==1
 for i in d.images:
  assert i.get('alt') and i.get('width') and i.get('height') and i.get('srcset')
 for v in d.videos:
  assert v.get('preload')=='none' and 'controls' in v and 'playsinline' in v
  assert 'autoplay' not in v and int(v['height'])/int(v['width'])>1.7
 for a in d.images+d.sources:
  for attr in ['src','poster']:
   v=a.get(attr,'')
   if v.startswith('/assets/collapse/ss25-capsule-02/'):assert (ROOT/'public'/v.lstrip('/')).is_file(),v
 for v in d.videos:assert (ROOT/'public'/v['poster'].lstrip('/')).is_file()
 canonical=next(x['href'] for x in d.links if x.get('rel')=='canonical');assert ('/it/' in canonical)==(locale=='it')
 assert {x.get('hreflang') for x in d.links if x.get('rel')=='alternate'}>={'en','it','x-default'}
 for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):json.loads(raw)
 print(locale+': media references, SEO structure, original aspect ratios and deferred video passed')
m=json.loads((ROOT/'scripts/project-sources/ss25-capsule-02-assets.json').read_text())
for key in ['campaign-film','behind-the-scenes']:
 v=m[key];path=ROOT/'public/assets/collapse/ss25-capsule-02'/v['file'];data=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','stream=codec_type,width,height','-of','json',str(path)]));stream=next(x for x in data['streams'] if x['codec_type']=='video');assert stream['width']==v['width'] and stream['height']==v['height'];assert path.stat().st_size<3_000_000
print('Both compressed videos: valid dimensions and under 3 MB each')
