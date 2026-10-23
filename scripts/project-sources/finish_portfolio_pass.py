from pathlib import Path
import re,json,html,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];P=R/'public';E=html.escape
DRAFTS=['global-services','inside-you','born2rage']
UTILITY='.portfolio-skip{position:fixed;left:16px;top:-100px;z-index:10000;padding:12px 18px;background:#ece9e3;color:#111;border:2px solid #111;text-decoration:none;font:14px/1.3 Arial,sans-serif}.portfolio-skip:focus{top:12px}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid #a6532a;outline-offset:4px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}'
utility_name='portfolio-finish-'+hashlib.sha256(UTILITY.encode()).hexdigest()[:12]+'.css';(P/'assets'/utility_name).write_text(UTILITY)
# Original project artwork, reused without changing the underlying files.
items=[('citta-di-castello','/assets/cdc-regular-alphabet.webp','CDC Regular','Type'),('no-font','/assets/no-font/01.webp','No Font','Specimen'),('rebuild-yourself','/assets/rebuild-v4/poster-front.webp','Rebuild Yourself','Poster'),('chaos-as-duality','/assets/piazzetta-chaos/chaos-poster-640.webp','Chaos as Duality','Event'),('bar-la-piazzetta','/assets/piazzetta-chaos/blp-poster-640.webp','Collasso BLP','Poster'),('collapse/collections/ss25-capsule-02','/assets/collapse/ss25-capsule-02/flowers-poster-640-e1c5c1e559ea.webp','Free Flowers','Campaign'),('collapse/collections/ss25-capsule-02','/assets/collapse/ss25-capsule-02/lovers-wordmark-640-f513395323af.webp','Lovers','Lettering'),('harmony','/assets/responsive/harmony-board-01-ec41702b4ee4-640.webp','Harmony','Editorial'),('first-things-first','/assets/first/poster-first-d1845711b8d8.webp','First Things First','Poster'),('axion-controllers','/assets/axion-case/campaign-640.webp','Axion Controllers','Identity')]
for it in [False,True]:
 pre='/it' if it else '';p=P/('it/index.html' if it else 'index.html');s=p.read_text()
 # Empty projects leave the public selection until their original work is supplied.
 for slug in DRAFTS:s=re.sub(r'<a class="archive-row"[^>]*href="'+pre+'/work/'+slug+r'/".*?</a>\s*','',s,flags=re.S)
 # Keep the compact project archive numbered in the order actually displayed.
 count=[7]
 def number(m):
  n=count[0];count[0]+=1;return re.sub(r'(<span class="n">)\d+(</span>)',rf'\g<1>{n:02d}\2',m.group())
 s=re.sub(r'<a class="archive-row".*?</a>',number,s,flags=re.S)
 cards=''
 for i,(slug,src,title,kind) in enumerate(items,1):
  cards+=f'<a class="graphic-item" href="{pre}/work/{slug}/" aria-label="{E(title)} — '+('apri il progetto' if it else 'open project')+f'"><div class="graphic-item-head"><span>{E(kind)}</span><span>{i:02d} ↗</span></div><div class="graphic-preview"><img src="{src}" alt="{E(title)} — {E(kind)}" loading="lazy" decoding="async" width="640" height="800"></div><div class="graphic-item-type">G—{i:03d} / {E(title)}</div></a>'
 pattern=r'(<div class="graphic-archive-track"[^>]*>).*?(</div>\s*</section>)'
 assert re.search(pattern,s,re.S);s=re.sub(pattern,lambda m:m.group(1)+cards+m.group(2),s,count=1,flags=re.S)
 rules='<style data-portfolio-finish>.graphic-item{display:block;text-decoration:none;color:inherit}.graphic-preview{padding:0!important;overflow:hidden}.graphic-preview img{width:100%;height:100%;object-fit:contain;display:block}.graphic-item:focus-visible{outline:2px solid #a6532a;outline-offset:5px}.graphic-item:hover .graphic-item-type{text-decoration:underline}.topbar nav a:focus-visible{outline:2px solid currentColor;outline-offset:5px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}</style>'
 
 if 'data-portfolio-finish' not in s:s=s.replace('</head>',rules+'</head>')
 micro=['Progetto identità visive, siti e materiali editoriali.','Con COLLAPSE lavoro tra moda, immagini ed eventi.','Porto avanti anche ricerca tipografica, installazioni e oggetti.'] if it else ['I design visual identities, websites and editorial materials.','Through COLLAPSE I work across fashion, imagery and events.','I also develop type research, installations and objects.']
 s=re.sub(r'<div class="micro-columns".*?</div>','<div class="micro-columns" aria-hidden="true">'+''.join('<p>'+x+'</p>' for x in micro)+'</div>',s,count=1,flags=re.S)
 intro='<div class="hero-intro"><strong>'+('SONO FILIPPO MANTINI.' if it else "I’M FILIPPO MANTINI.")+'</strong><span class="waiting">'+('GRAPHIC DESIGNER & ART DIRECTOR INDIPENDENTE.' if it else 'INDEPENDENT GRAPHIC DESIGNER & ART DIRECTOR.')+'</span><span class="mono">'+('Identità visive, siti e progetti culturali. Dal concept alle applicazioni.' if it else 'Visual identities, websites and cultural projects. From concept to applications.')+'</span></div>'
 s=re.sub(r'<div class="hero-intro".*?</div>',intro,s,count=1,flags=re.S);p.write_text(s)
# Temporarily park incomplete legacy case studies. Keep their source in Git history.
redirects=(P/'_redirects').read_text()
if '# Case studies awaiting original' not in redirects:redirects+='\n# Case studies awaiting original project documentation. Temporary redirects.\n'
for pre in ['', '/it']:
 for slug in DRAFTS:
  route=f'{pre}/work/{slug}/';target=pre+'/#work';p=P/route.strip('/')/'index.html';lang='it' if pre else 'en';p.write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={target}"><title>Filippo Mantini — Portfolio</title></head><body><a href="{target}">Portfolio — Work</a></body></html>')
  for suffix in ['', '/', '/index.html']:
   rule=f'{pre}/work/{slug}{suffix} {target} 302\n'
   if rule not in redirects:redirects+=rule
(P/'_redirects').write_text(redirects)
# Update references to the temporarily parked pages rather than leaving dead ends.
for p in P.rglob('index.html'):
 s=p.read_text();it='<html lang="it"' in s;pre='/it' if it else ''
 if any('/work/'+slug+'/' in '/'+str(p.relative_to(P)) for slug in DRAFTS):continue
 for slug in DRAFTS:
  s=re.sub(r'<a\b[^>]*href="(?:/it)?/work/'+slug+r'/"[^>]*>.*?</a>',f'<a href="{pre}/#work">'+('Tutti i progetti ↗' if it else 'All projects ↗')+'</a>',s,flags=re.S)
 # Portfolio headers retain their layout and gain the same destination set.
 def nav(m):
  h=m.group()
  if '<nav' not in h or 'class="topbar"' not in h:return h
  studio='/studio/' if it else '/work/filippo-mantini-studio/'
  language='EN' if it else 'IT';other='en' if it else 'it'
  match=re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>\s*'+language+r'\s*</a>',h)
  if not match:return h
  links=f'<nav><a href="{pre}/#work">Work</a><a href="{pre}/#photo">Photo</a><a href="{studio}">Studio AI</a><a href="{pre}/about/">About</a><a href="{match.group(1)}" lang="{other}" hreflang="{other}">{language}</a></nav>'
  return re.sub(r'<nav\b.*?</nav>',links,h,flags=re.S)
 s=re.sub(r'<header\b.*?</header>',nav,s,flags=re.S)
 def foot(m):
  f=m.group()
  if 'class="footer"' not in f:return f
  if 'mailto:info@filippomantini.com' not in f:f=f.replace('</footer>','<a href="mailto:info@filippomantini.com">info@filippomantini.com</a></footer>')
  if 'href="'+pre+'/privacy/"' not in f and '>Privacy</a>' not in f and '>PRIVACY</a>' not in f:f=f.replace('</footer>',f'<a href="{pre}/privacy/">Privacy</a></footer>')
  return f
 s=re.sub(r'<footer\b.*?</footer>',foot,s,flags=re.S)
 if 'http-equiv="refresh"' not in s and '<main' in s:
  if 'data-portfolio-utility' not in s:s=s.replace('</head>',f'<link rel="stylesheet" data-portfolio-utility href="/assets/{utility_name}"></head>')
  if 'class="portfolio-skip"' not in s:
   main=re.search(r'<main\b[^>]*>',s);tag=main.group();found=re.search(r'\bid="([^"]+)"',tag)
   if found:main_id=found.group(1)
   else:main_id='portfolio-main';s=s[:main.start()]+tag[:-1]+' id="portfolio-main">'+s[main.end():]
   label='Salta al contenuto' if it else 'Skip to content';skip=f'<a class="portfolio-skip" href="#{main_id}">{label}</a>'
   s=re.sub(r'(<body\b[^>]*>)',lambda m:m.group(1)+skip,s,count=1)
 # Link paired language pages only where the matching public route exists.
 canonical=re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"',s)
 if canonical and 'http-equiv="refresh"' not in s:
  current=canonical.group(1).replace('https://filippomantini.com','');expected='/'+str(p.parent.relative_to(P)).replace('\\','/')+'/' if p.parent!=P else '/';expected=expected.replace('//','/')
  if current==expected:
   if current=='/studio/':en='/work/filippo-mantini-studio/';ita='/studio/'
   elif current=='/work/filippo-mantini-studio/':en=current;ita='/studio/'
   else:en=current[3:] if current.startswith('/it/') else current;ita='/it'+en
   enfile=P/en.strip('/')/'index.html';itfile=P/ita.strip('/')/'index.html'
   if enfile.exists() and itfile.exists():
    s=re.sub(r'<link\b(?=[^>]*\brel="alternate")(?=[^>]*\bhreflang=)[^>]*>','',s)
    tags=''.join(f'<link rel="alternate" hreflang="{l}" href="https://filippomantini.com{v}">' for l,v in [('en',en),('it',ita),('x-default',en)])
    s=s.replace('</head>',tags+'</head>')
 p.write_text(s)
# Exclude parked routes from the sitemap.
p=P/'sitemap.xml';s=p.read_text()
for slug in DRAFTS:s=re.sub(r'\s*<url>\s*<loc>https://filippomantini.com(?:/it)?/work/'+slug+r'/</loc>.*?</url>','',s,flags=re.S)
p.write_text(s)
print('Home archive: 10 original project previews. Parked drafts: 3 projects. Navigation, footer and language metadata normalised.')
