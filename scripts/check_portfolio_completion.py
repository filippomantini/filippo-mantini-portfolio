from pathlib import Path
from html.parser import HTMLParser
import json,re,xml.etree.ElementTree as ET,subprocess
R=Path(__file__).resolve().parents[1];P=R/'public';DRAFTS=['global-services','inside-you','born2rage']
class H(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
active=0;pairs=0
for p in P.rglob('index.html'):
 s=p.read_text();h=H();h.feed(s)
 for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):json.loads(raw)
 if 'http-equiv="refresh"' in s:continue
 active+=1;assert sum(t=='h1' for t,a in h.tags)==1,p
 if 'hreflang="x-default"' in s:
  pairs+=1;assert len(re.findall(r'<link[^>]*rel="alternate"[^>]*hreflang=',s))==3,p
 assert 'Project material /' not in s and 'Original project material will replace' not in s,p
 for t,a in h.tags:
  if t=='img':assert 'alt' in a,p # Empty alt is valid for decorative images.
  if t=='a':assert not any('/work/'+d+'/' in a.get('href','') for d in DRAFTS),(p,a)
 if '<header class="topbar"' in s:
  header=re.search(r'<header class="topbar".*?</header>',s,re.S).group();assert 'Studio AI' in header,p
for p in [P/'index.html',P/'it/index.html']:
 s=p.read_text();archive=re.search(r'<section class="graphic-archive".*?</section>',s,re.S).group();assert archive.count('class="graphic-item"')==10 and 'class="ghost"' not in archive
for pre in ['', 'it/']:
 s=(P/f'{pre}work/axion-controllers/index.html').read_text();assert s.count('<video')==4 and s.count('preload="none"')==4;assert '02 / LOGO SYSTEM' in s and 'ui-review' in s;assert 'BreadcrumbList' in s
 for slug in DRAFTS:assert 'noindex,follow' in (P/f'{pre}work/{slug}/index.html').read_text()
ET.parse(P/'sitemap.xml')
for p in (P/'assets/axion-case').glob('*.svg'):ET.parse(p)
for p in (P/'assets/axion-case').glob('*.mp4'):subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
# SVG marks must bypass the raster pipeline, and authored column sizes must survive it.
import sys
sys.path.insert(0,str(R/'scripts'));import optimize_delivery as delivery
assert not delivery.is_raster_asset('/assets/axion-case/symbol.svg')
assert delivery.is_raster_asset('/assets/axion-case/front-640.webp?v=2')
svg='<img src="/assets/axion-case/symbol.svg" width="531" height="531" loading="lazy" decoding="async" alt="Axion">'
assert delivery.responsive_img(svg,'100vw')==svg
delivery.variants=lambda url:dict(width=640,height=360,candidates=[(640,url)],source=url)
assert 'sizes="48vw"' in delivery.responsive_img('<img src="/assets/axion-case/front-640.webp" sizes="48vw">','100vw')
print(f'{active} active pages, {pairs} pages with paired language metadata: structure, navigation, source artwork, draft exclusion, SVG/XML, JSON-LD and four video decodes passed.')
