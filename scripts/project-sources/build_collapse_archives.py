"""Build three bilingual collection essays and consolidate the SS24 route.
Run on the existing repository pages, preserving their social source material.
"""
from pathlib import Path
import re,json,html,hashlib
ROOT=Path(__file__).resolve().parents[2];M=json.loads((Path(__file__).parent/'collapse-archive-assets.json').read_text());BASE='/assets/collapse/archive/'
css=ROOT/'public/assets/collapse-archive-editorial.css';cssname='collapse-archive-editorial-'+hashlib.sha256(css.read_bytes()).hexdigest()[:12]+'.css';css.with_name(cssname).write_bytes(css.read_bytes())
for lang in ['it','en']:
 t=lambda it,en:it if lang=='it' else en
 prefix='/it' if lang=='it' else '';COLL=ROOT/('public/it' if lang=='it' else 'public')/'work/collapse/collections'
 def image(key,alt,eager=False,sizes='(max-width:550px) calc(50vw - 19px), calc(50vw - 29px)'):
  v=M[key];a=v[-1];return f'<img src="{BASE+a["file"]}" srcset="'+', '.join(BASE+x['file']+' '+str(x['width'])+'w' for x in v)+f'" sizes="{sizes}" width="{a["width"]}" height="{a["height"]}" alt="{html.escape(alt)}" loading="'+('eager' if eager else 'lazy')+'" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
 def fig(key,it,en,label,eager=False,sizes=None,cls=''):
  return '<figure'+(f' class="{cls}"' if cls else '')+'>'+image(key,t(it,en),eager,**({'sizes':sizes} if sizes else {}))+f'<figcaption><span>{label}</span><span>COLLAPSE</span></figcaption></figure>'
 def group(items,cls='pair'):
  return f'<div class="{cls}">'+''.join(fig(*item) for item in items)+'</div>'
 def intro(label,title,copy):return f'<section class="ca"><div class="intro"><div><span class="label">{label}</span><h2>{title}</h2></div><p>{copy}</p></div>'
 def chapter(label,title,copy,content,dark=False,id=''):
  return '<div class="chapter'+(' dark' if dark else '')+(' ca-anchor' if id else '')+'"'+(f' id="{id}"' if id else '')+f'><div class="heading"><span class="label">{label}</span><h3>{title}</h3><p>{copy}</p></div>'+content+'</div>'
 def film(key,title):
  a=M[key];poster=M[key+'-poster'][-1]['file'];return f'<figure><video controls playsinline preload="none" width="{a["width"]}" height="{a["height"]}" poster="{BASE+poster}" aria-label="{title}"><source src="{BASE+a["file"]}" type="video/mp4"></video><figcaption><span>{title}</span><span>COLLAPSE / FILM</span></figcaption></figure>'
 # SS25 Capsule 01: eleven supplied photographs/artworks and two original films.
 s=intro('01 / CAMPAIGN / SS25',t('AN ITALIAN<br>ROAD TRIP.','AN ITALIAN<br>ROAD TRIP.'),t('Una spider rossa, un muro arancione, denim e luce diretta. La campagna costruisce un racconto di viaggio attraverso fotografie, dettagli dei capi e comunicazione grafica.','A red roadster, an orange wall, denim and direct sunlight. The campaign builds a road-trip story through photographs, garment details and graphic communication.'))
 s+='<div class="pair">'+fig('capsule01-01','Modello con denim COLLAPSE davanti a un muro arancione, accanto a uno stereo','Model in COLLAPSE denim against an orange wall beside a stereo','CAMPAIGN / ORANGE WALL',True)+fig('capsule01-06','Due modelli nella spider rossa della campagna COLLAPSE','Two models inside the red roadster from the COLLAPSE campaign','CAMPAIGN / ROAD TRIP')+'</div>'
 road=group([('capsule01-08','Spider rossa con cofano aperto durante la campagna','Red roadster with its bonnet open during the campaign','ROAD TRIP / 01'),('capsule01-09','Dettaglio di styling e mani nell’abitacolo della spider','Styling and hands inside the roadster','ROAD TRIP / DETAIL'),('capsule01-07','Dettaglio COLLAPSE Made in Italy sulla portiera rossa','COLLAPSE Made in Italy detail on the red car door','COLLAPSE / MADE IN ITALY')],'trio')
 road+=fig('capsule01-10','Fotografia dall’alto della spider rossa con i modelli della campagna','Overhead photograph of the red roadster and campaign models','CAMPAIGN / OVERHEAD',sizes='(max-width:850px) calc(100vw - 28px), 1050px',cls='ca-trip-wide')
 s+=chapter('02 / PHOTO STORY',t('SULLA STRADA.','ON THE ROAD.'),t('L’auto è parte del set: cromie, inquadrature ravvicinate e punti di vista dall’alto collegano il prodotto all’immaginario del viaggio.','The car becomes part of the set: colour, close framing and overhead views connect the product with the visual world of the road trip.'),road)
 s+=chapter('03 / DENIM & STYLING',t('IL CAPO,<br>DA VICINO.','THE GARMENT,<br>UP CLOSE.'),t('Il denim torna al centro delle immagini: silhouette, costruzione, cuciture e dettagli di styling emergono sul fondo arancione.','Denim takes centre stage: silhouette, construction, stitching and styling details stand out against the orange backdrop.'),group([('capsule01-02','Look completo con denim COLLAPSE davanti al muro arancione','Full COLLAPSE denim look against the orange wall','DENIM / FULL LOOK'),('capsule01-04','Ritratto del modello con occhiali e guanto, campagna COLLAPSE','Portrait of the model wearing sunglasses and a glove','CAMPAIGN / PORTRAIT'),('capsule01-03','Dettaglio del denim, della cintura e delle cuciture','Close-up of denim, waistband and stitching','DENIM / DETAIL')],'trio'))
 s+=chapter('04 / GRAPHIC COMMUNICATION','TOUR<br>COLLAPSE.',t('Le composizioni originali trasformano le fotografie in copertine e materiali promozionali. Sono presentate come documentazione del lancio, insieme al poster Summer Sale d’archivio.','The original compositions turn photographs into cover art and promotional material. They document the launch alongside the archival Summer Sale poster.'),group([('capsule01-05','Copertina grafica originale Tour Collapse con fotografia dall’alto della spider','Original Tour Collapse cover with overhead roadster photography','TOUR COLLAPSE / ORIGINAL COVER'),('capsule01-11','Poster originale Summer Sale COLLAPSE 24, materiale promozionale d’archivio','Original COLLAPSE 24 Summer Sale poster, archival promotional material','SUMMER SALE / ARCHIVE POSTER')]),True)
 s+=chapter('05 / MOTION',t('IL VIAGGIO<br>CONTINUA.','THE JOURNEY<br>CONTINUES.'),t('Il film An Italian Road Trip e il contenuto promozionale Summer Sale completano il racconto della campagna. I materiali di vendita sono conservati come archivio della comunicazione.','The An Italian Road Trip film and the Summer Sale promotional piece complete the campaign story. Sales material is preserved as a communication archive.'),'<div class="film-grid ca-film-two">'+film('capsule01-12','AN ITALIAN ROAD TRIP')+film('capsule01-13','SUMMER SALE / ARCHIVE FILM')+'</div>')+'</section>'
 capsule_story=s
 # FW24/25 + SS24: unisex comparison and ordered lookbook.
 from fw24_ss24_story import build_story as build_seasonal_story
 unified_story=build_seasonal_story(t,fig,group,intro,chapter)
 # Fe26: the supplied graphics explicitly identify SS23 / Fe26. Keep the legacy URL.
 s=intro('01 / Fe26 / COLLECTION ARCHIVE',t('IL DENIM<br>COME SUPERFICIE.','DENIM<br>AS A SURFACE.'),t('Fe26 mette in relazione denim, segni di lavorazione e riferimenti industriali. Il progetto si legge nei capi, nelle personalizzazioni manuali e nelle immagini realizzate per raccontarli.','Fe26 connects denim, surface treatments and industrial references. The project takes shape through garments, manual customisation and the imagery created to present them.'))
 s+='<div class="pair">'+fig('fe26-15','Immagine originale Fe26 con modello seduto nel cassone di un pick-up e cielo azzurro','Original Fe26 image with a model seated in a pickup bed against a blue sky','Fe26 / CAMPAIGN',True)+fig('fe26-17','Composizione originale con capi Fe26 disposti su fondo in cemento','Original composition of Fe26 garments on a concrete surface','Fe26 / GARMENT COMPOSITION')+'</div>'
 s+=chapter('02 / MATERIAL & TREATMENT',t('SEGNI.<br>SUPERFICI.<br>LAVORAZIONI.','MARKS.<br>SURFACES.<br>TREATMENTS.'),t('La documentazione accosta fronte, retro e dettagli: campiture calde sul denim scuro, motivi chiari e applicazioni rosse sui tessuti a righe. Le immagini mostrano le differenze tra i capi della collezione.','The documentation brings together fronts, backs and details: warm marks on dark denim, light motifs and red applications on striped fabric. The images show the differences between the collection’s garments.'),group([('fe26-03','Vista frontale dei jeans Fe26 con lavorazioni color ruggine','Front view of Fe26 jeans with rust-coloured treatments','Fe26 / FRONT'),('fe26-02','Vista posteriore dei jeans Fe26 con lavorazioni color ruggine','Back view of Fe26 jeans with rust-coloured treatments','Fe26 / BACK'),('fe26-07','Pantaloni a righe con applicazioni rosse Fe26','Striped trousers with red Fe26 applications','Fe26 / SURFACE'),('fe26-12','Pantalone a zampa Fe26 con motivi chiari','Fe26 flared trousers with light motifs','Fe26 / FLARED DENIM')],'four'))
 looks=group([('fe26-09','Look Fe26 con maglia lavorata e gonna denim, vista posteriore','Fe26 look with a treated top and denim skirt, back view','Fe26 / LOOK'),('fe26-14','Completo Fe26 presentato sospeso nell’ambiente di lavoro','Fe26 matching set displayed hanging in the workspace','Fe26 / GARMENT DISPLAY')])
 looks+='<div style="margin-top:45px">'+group([('fe26-06','Borsa denim Fe26 con catena e gonna coordinata','Fe26 denim bag with chain and matching skirt','Fe26 / DENIM BAG'),('fe26-16','Vista frontale dei pantaloni Fe26 con segni e volume a zampa','Front view of Fe26 trousers with graphic marks and a flared silhouette','Fe26 / VOLUME')])+'</div>'
 s+=chapter('03 / GARMENTS & ACCESSORIES',t('IL LAVORO<br>DIVENTA CAPO.','THE PROCESS<br>BECOMES A GARMENT.'),t('Silhouette, dettagli e accessori completano la ricerca sulla superficie. I capi sono mostrati indossati e fuori dal corpo, con attenzione a volumi, orli, catene e costruzione.','Silhouettes, details and accessories extend the surface research. Garments are shown on and off the body, with attention to volume, hems, chains and construction.'),looks)
 s+=chapter('04 / ORIGINAL COMMUNICATION',t('L’IMMAGINARIO<br>DI Fe26.','THE VISUAL<br>WORLD OF Fe26.'),t('Le immagini originali collegano il prodotto a superfici industriali, cielo e mezzi di lavoro. I materiali d’archivio riportano il nome Fe26 e il riferimento SS23.','The original imagery connects the product with industrial surfaces, sky and working vehicles. The archival material carries the Fe26 name and the SS23 reference.'),group([('fe26-01','Composizione originale COLLAPSE SS23 Fe26 con canotta bianca e pick-up','Original COLLAPSE SS23 Fe26 composition with a white tank top and pickup','Fe26 / ORIGINAL ARTWORK 01'),('fe26-11','Composizione originale COLLAPSE SS23 Fe26 con denim su pick-up','Original COLLAPSE SS23 Fe26 composition with denim on a pickup','Fe26 / ORIGINAL ARTWORK 02'),('fe26-05','Dettaglio della giacca a righe Fe26 con marchio COLLAPSE','Detail of the Fe26 striped jacket with COLLAPSE label','Fe26 / ORIGINAL DETAIL')],'trio'),True)
 s+=chapter('05 / MOTION STUDIES',t('IL CONTESTO<br>IN MOVIMENTO.','THE CONTEXT<br>IN MOTION.'),t('Quattro brevi composizioni video sviluppano i riferimenti visivi del progetto: mezzi di lavoro, strutture, superfici metalliche e segni. Il formato quadrato originale è mantenuto.','Four short video compositions develop the project’s visual references: working vehicles, structures, metal surfaces and marks. Their original square format is preserved.'),'<div class="film-grid ca-film-four">'+''.join(film('fe26-'+n,'Fe26 / MOTION '+str(i).zfill(2)) for i,n in enumerate(['04','08','10','13'],1))+'</div>')+'</section>'
 fe26_story=s
 config={
 'ss25-capsule-01':{'title':'SS25 / CAPSULE 01','h2':'SS25<br>CAPSULE 01','story':capsule_story,'hero':'capsule01-01','copy':t('Una campagna on the road tra denim, una spider rossa e luce estiva. Fotografia, styling e comunicazione grafica costruiscono il racconto della capsule.','An on-the-road campaign with denim, a red roadster and summer light. Photography, styling and graphic communication build the capsule’s story.'),'desc':t('COLLAPSE SS25 Capsule 01: campagna An Italian Road Trip, denim, fotografia, copertine e film. Direzione creativa e contenuti di Filippo Mantini.','COLLAPSE SS25 Capsule 01: An Italian Road Trip campaign, denim, photography, cover art and films. Creative direction and content by Filippo Mantini.')},
 'fw24-25':{'title':'FW24/25 + SS24','h2':'FW24/25<br>SS24','story':unified_story,'hero':'fw24ss24-fluidity-woman','copy':t('FW24/25 e SS24 in un unico archivio: FLUIDITY, denim, camiceria grafica e riferimenti sportivi. Due capitoli stagionali collegati da set, styling e direzione visiva.','FW24/25 and SS24 in one archive: FLUIDITY, denim, graphic shirts and sports references. Two seasonal chapters connected by set, styling and visual direction.'),'desc':t('COLLAPSE FW24/25 e SS24: FLUIDITY, Denim Industry, Off the Grid e Football Team. Archivio unificato di capi, art direction e comunicazione di Filippo Mantini.','COLLAPSE FW24/25 and SS24: FLUIDITY, Denim Industry, Off the Grid and Football Team. A unified archive of garments, art direction and communication by Filippo Mantini.')},
 'fw23-24':{'title':'Fe26','h2':'Fe26','story':fe26_story,'hero':'fe26-15','copy':t('Denim, lavorazioni manuali e riferimenti industriali. Fe26 è una ricerca sui capi e sulle superfici, raccontata attraverso prodotto, fotografia e motion.','Denim, manual treatments and industrial references. Fe26 explores garments and surfaces through product, photography and motion.'),'desc':t('Fe26 di COLLAPSE: denim, personalizzazioni manuali, borsa, fotografia e motion studies. Progetto e direzione creativa di Filippo Mantini.','Fe26 by COLLAPSE: denim, manual customisation, bag, photography and motion studies. Project and creative direction by Filippo Mantini.')}}
 for slug,c in config.items():
  p=COLL/slug/'index.html';doc=p.read_text();wrapped='<!-- ARCHIVE_STORY_START -->'+c['story']+'<!-- ARCHIVE_STORY_END -->'
  if '<!-- ARCHIVE_STORY_START -->' in doc:doc=re.sub(r'<!-- ARCHIVE_STORY_START -->[\s\S]*?<!-- ARCHIVE_STORY_END -->',lambda _:wrapped,doc)
  else:doc=re.sub(r'<section class="cc-gallery"[\s\S]*?</section>',lambda _:wrapped,doc,count=1)
  doc=re.sub(r'(<div class="cc-hero-below"><div><span class="cc-overline">[^<]*</span>)<h2>[\s\S]*?</h2></div><p>[\s\S]*?</p></div>',lambda m:m[1]+'<h2>'+c['h2']+'</h2></div><p>'+c['copy']+'</p></div>',doc,count=1)
  title=c['title']+' — COLLAPSE | Filippo Mantini';doc=re.sub(r'<title>[^<]*</title>','<title>'+title+'</title>',doc)
  for tag,value in [('name="description"',c['desc']),('property="og:description"',c['desc']),('property="og:title"',title),('property="og:image"','https://filippomantini.com'+BASE+M[c['hero']][-1]['file'])]:doc=re.sub(r'(<meta '+tag+r' content=")[^"]*',lambda m:m[1]+html.escape(value,quote=True),doc)
  def schema(m):
   a=json.loads(m[1])
   if a.get('@type')=='CreativeWork':a.update(name=c['title']+' / COLLAPSE',description=c['desc'],image='https://filippomantini.com'+BASE+M[c['hero']][-1]['file'])
   if a.get('@type')=='BreadcrumbList':a['itemListElement'][-1]['name']=c['title']
   return '<script type="application/ld+json">'+json.dumps(a,ensure_ascii=False,separators=(',',':'))+'</script>'
  doc=re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>',schema,doc)
  doc=re.sub(r'<link rel="stylesheet" href="/assets/(?:static/)?collapse-archive-editorial[^\"]*">','',doc);doc=doc.replace('</head>',f'<link rel="stylesheet" href="/assets/{cssname}"></head>')
  if 'Studio AI</a>' not in doc:doc=doc.replace(f'<a href="{prefix}/about/">About</a>',f'<a href="{("/studio/" if lang=="it" else "/work/filippo-mantini-studio/")}">Studio AI</a><a href="{prefix}/about/">About</a>')
  if slug!='fw24-25' and 'video-playback-' not in doc:doc=doc.replace('</body>','<script defer src="/assets/static/video-playback-f1c3d61df99e.js"></script></body>')
  if slug=='fw23-24':doc=doc.replace('2023—24','2023').replace('FW 23/24','Fe26');num='06'
  elif slug=='ss25-capsule-01':num='07';doc=doc.replace('<span>SOCIAL MEDIA / SS25 / CAPSULE 01</span>','<span>06 / SOCIAL MEDIA / SS25 / CAPSULE 01</span>')
  else:num='06'
  doc=doc.replace('02 / IL MIO CONTRIBUTO',num+' / IL MIO CONTRIBUTO').replace('02 / MY CONTRIBUTION',num+' / MY CONTRIBUTION')
  if slug=='fw24-25':
   # Retain both genuine Instagram mockups within one publishing section.
   old=COLL/'ss24/index.html';oldtext=old.read_text() if old.exists() else ''
   sm=re.search(r'<section class="collection-social"[\s\S]*?</section>',oldtext)
   current=re.search(r'<section class="collection-social"[\s\S]*?</section>',doc)
   if sm and current:
    extra=re.search(r'<figure class="social-device">[\s\S]*?</figure>',sm[0])[0]
    content=current[0];own=re.search(r'<figure class="social-device">[\s\S]*?</figure>',content)[0]
    content=content.replace('class="collection-social"','class="collection-social archive-social"').replace(own,'<div class="archive-social-screens">'+own+extra+'</div>')
    content=content.replace('SOCIAL MEDIA / FW 24/25','05 / SOCIAL MEDIA / FW24/25 + SS24')
    content=content.replace('Il piano editoriale Instagram di FW 24/25:','Il piano editoriale Instagram di FW24/25 e SS24:').replace('The Instagram editorial plan for FW 24/25:','The Instagram editorial plan for FW24/25 and SS24:')
    doc=doc.replace(current[0],content)
   doc=doc.replace('<strong>FW 24/25</strong>','<strong>FW24/25 + SS24</strong>')
  p.write_text(doc)
 # Consolidate all collection navigation and the index; no duplicate SS24 tile.
 for p in list(COLL.glob('*/index.html'))+[ROOT/('public/it' if lang=='it' else 'public')/'work/collapse/index.html']:
  if p.parent.name=='ss24':continue
  text=p.read_text()
  if p.parent.name=='collapse':
   text=re.sub(r'<a class="cp-collection" href="'+prefix+r'/work/collapse/collections/ss24/">[\s\S]*?</a>','',text)
   text=text.replace('<strong>FW 24/25</strong>','<strong>FW24/25 + SS24</strong>').replace('<strong>FW 23/24</strong>','<strong>Fe26</strong>')
   text=re.sub(r'(href="'+prefix+r'/work/collapse/collections/fw23-24/"><span class="cp-collection-year">)2023—24',r'\g<1>2023',text)
  # A merged page must move to Fe26, never paginate to itself via SS24.
  if p.parent.name=='fw24-25':
   text=re.sub(r'(<a href=")'+prefix+r'/work/collapse/collections/ss24/("[\s\S]*?<strong>)[^<]*(</strong>)',lambda m:m[1]+prefix+'/work/collapse/collections/fw23-24/'+m[2]+'Fe26'+m[3],text)
  text=text.replace(prefix+'/work/collapse/collections/ss24/',prefix+'/work/collapse/collections/fw24-25/')
  text=text.replace('<strong>SS24</strong>','<strong>FW24/25 + SS24</strong>').replace('<strong>FW 24/25</strong>','<strong>FW24/25 + SS24</strong>').replace('<strong>FW 23/24</strong>','<strong>Fe26</strong>')
  p.write_text(text)
# Existing public SS24 URLs now permanently redirect to the merged seasonal archive.
p=ROOT/'public/_redirects';text=p.read_text();block='\n# SS24 is included in the unified FW24/25 + SS24 archive.\n'
for prefix in ['', '/it']:
 old=prefix+'/work/collapse/collections/ss24';dest=prefix+'/work/collapse/collections/fw24-25/'
 for ending in ['', '/', '/index.html']:block+=old+ending+' '+dest+' 301\n'
if '# SS24 is included' not in text:p.write_text(text.rstrip()+'\n'+block)
p=ROOT/'public/sitemap.xml';text=p.read_text();text=re.sub(r'\s*<url>\s*<loc>https://filippomantini.com/(?:it/)?work/collapse/collections/ss24/</loc>[\s\S]*?</url>','',text);p.write_text(text)
print('Built SS25 Capsule 01, unified FW24/25 + SS24, Fe26: EN + IT')
