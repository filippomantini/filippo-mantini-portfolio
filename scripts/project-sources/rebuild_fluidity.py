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
 from fw24_ss24_story import build_story
 p=COLL/'fw24-25/index.html';doc=p.read_text();story=build_story(t,fig,group,intro,chapter)
 doc=re.sub(r'<!-- ARCHIVE_STORY_START -->[\s\S]*?<!-- ARCHIVE_STORY_END -->',lambda _:'<!-- ARCHIVE_STORY_START -->'+story+'<!-- ARCHIVE_STORY_END -->',doc)
 doc=re.sub(r'<link rel="stylesheet" href="/assets/(?:static/)?collapse-archive-editorial[^\"]*">','',doc);doc=doc.replace('</head>',f'<link rel="stylesheet" href="/assets/{cssname}"></head>')
 desc=t('COLLAPSE FW24/25 e SS24: Fluidity, collezione unisex, galleria dei look e identità grafica. Direzione creativa e comunicazione di Filippo Mantini.','COLLAPSE FW24/25 and SS24: Fluidity, unisex collection, lookbook gallery and graphic identity. Creative direction and communication by Filippo Mantini.')
 hero='https://filippomantini.com'+BASE+M['fw24ss24-fluidity-woman'][-1]['file']
 for tag,value in [('name="description"',desc),('property="og:description"',desc),('property="og:image"',hero)]:doc=re.sub(r'(<meta '+tag+r' content=")[^\"]*',lambda m:m[1]+html.escape(value,quote=True),doc)
 def update_schema(m):
  a=json.loads(m[1])
  if a.get('@type')=='CreativeWork':a.update(description=desc,image=hero)
  return '<script type="application/ld+json">'+json.dumps(a,ensure_ascii=False,separators=(',',':'))+'</script>'
 doc=re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>',update_schema,doc)
 p.write_text(doc)
print('Fluidity / IT + EN updated')
