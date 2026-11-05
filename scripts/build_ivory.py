"""Build Ivory's scoped case study and web media from the uploaded originals."""
from pathlib import Path
from html import escape
import json
import re
import subprocess
import io
import shutil

import fitz
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'public/assets/ivory'
OUT = MEDIA / 'web'
OUT.mkdir(exist_ok=True)
BASE = '/assets/ivory/web/'
FFMPEG = shutil.which('ffmpeg')
if not FFMPEG:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
images = {}
report = []


def image(source, name, widths):
    im = ImageOps.exif_transpose(source).convert('RGB')
    variants = []
    for width in widths:
        width = min(width, im.width)
        if variants and variants[-1][0] == width:
            continue
        height = round(im.height * width / im.width)
        target = OUT / f'{name}-{width}.webp'
        buffer = io.BytesIO()
        im.resize((width, height), Image.Resampling.LANCZOS).save(buffer, 'WEBP', quality=86, method=6)
        target.write_bytes(buffer.getvalue())
        variants.append((width, target.name))
    images[name] = {'width': im.width, 'height': im.height, 'variants': variants}


sources = [
    ('post instagram.png', 'poster', (640, 1280, 1600)),
    ('prima storia instagram.webp', 'announcement', (540, 1080)),
    ('INFO_01.webp', 'tickets-story', (540, 1080)),
    ('INFO_02.webp', 'lineup-story', (540, 1080)),
    ('INFO_03.webp', 'access-story', (540, 1080)),
    ('close friends.webp', 'close-friends', (540, 1080)),
    ('ticket collapse comprende.webp', 'ticket-benefits', (540, 1080)),
    ('sold out 18€.webp', 'sold-out', (540, 1080)),
    ('INGRESSO IN CASSA NON GARANTITO.webp', 'final-tickets', (540, 1080)),
    ('info_01.jpg', 'tickets-post', (640, 1280)),
    ('info_02.jpg', 'lineup-post', (640, 1280)),
    ('info_03.jpg', 'access-post', (640, 1280)),
    ('IMG_9057.jpeg', 'banner-installation', (640, 1280, 1920)),
    ('IMG_9105.jpeg', 'banner-installed', (640, 1280, 1920)),
]
for filename, name, widths in sources:
    with Image.open(MEDIA / filename) as im:
        image(im, name, widths)

with fitz.open(MEDIA / 'banner.pdf') as doc:
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2400 / page.rect.width, 2400 / page.rect.width), alpha=False)
    image(Image.open(io.BytesIO(pix.tobytes('png'))), 'banner', (1200, 2400))

for source, name in [('VIDEO REEL FINITO.mp4', 'reel'), ('ivory recap.mp4', 'recap')]:
    target = OUT / f'{name}.mp4'
    subprocess.run([FFMPEG, '-y', '-v', 'error', '-i', str(MEDIA/source), '-map', '0:v:0', '-map', '0:a:0?',
                    '-vf', "scale='min(1080,iw)':-2,setsar=1", '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '22', '-pix_fmt', 'yuv420p', '-threads', '2', '-c:a', 'aac', '-b:a', '128k',
                    '-movflags', '+faststart', '-map_metadata', '-1', str(target)], check=True)
    frame = subprocess.check_output([FFMPEG, '-v', 'error', '-ss', '1', '-i', str(target), '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-threads', '1', '-'])
    cover = Image.open(io.BytesIO(frame))
    image(cover, name+'-cover', (540, 1080))
    report.append({'file': target.name, 'original_bytes': (MEDIA/source).stat().st_size, 'web_bytes': target.stat().st_size,
                   'width': cover.width, 'height': cover.height})


CSS = '''
.ivory-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:36px;align-items:start}
.ivory-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}.ivory-grid.stories{grid-template-columns:repeat(4,minmax(0,1fr));gap:24px 16px}
.ivory-figure{margin:0;min-width:0}.ivory-figure img{display:block;width:100%;height:auto;background:#11110f}
.ivory-figure a{display:block}.ivory-figure a:focus-visible{outline:3px solid var(--orange);outline-offset:5px}
.ivory-figure figcaption{padding-top:12px;font:10px/1.5 "IBM Plex Mono",monospace;text-transform:uppercase;color:var(--muted)}
.ivory-video{display:block;width:100%;height:auto;background:#11110f}.ivory-video.portrait{aspect-ratio:9/16;max-height:760px;object-fit:contain}
.ivory-campaign{display:grid;grid-template-columns:1.25fr 1fr;gap:7vw;align-items:center;margin-top:42px;padding:40px;background:#151513}
.ivory-campaign .ivory-figure{width:100%;max-width:660px;margin:auto}.ivory-campaign .ivory-figure:last-child{max-width:400px}
.ivory-campaign figcaption{color:#bfbab3}.ivory-grid .ivory-figure{height:100%}
.ivory-banner{margin-top:42px}.ivory-recap{margin:42px auto 0;max-width:1100px}
.ivory-recap video{aspect-ratio:5/4}.ivory-back{display:inline-block;margin-top:30px;font:12px "IBM Plex Mono",monospace}
.hero h1{padding-bottom:12px}.meta{grid-template-columns:1fr 1fr}.ivory-details{display:flex;flex-wrap:wrap;gap:12px 32px;margin:20px 0 0;font:10px/1.5 "IBM Plex Mono",monospace;text-transform:uppercase;color:var(--muted)}
@media(max-width:1000px){.ivory-grid.stories{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.ivory-grid,.ivory-grid.three{grid-template-columns:1fr}.ivory-grid.stories{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 12px}.meta{grid-template-columns:1fr}.hero-grid{gap:24px}.section h2{overflow-wrap:anywhere}.ivory-campaign{grid-template-columns:1fr;padding:16px;gap:32px}.ivory-campaign .ivory-figure:last-child{max-width:360px}.ivory-grid.stories figcaption{font-size:9px}}
'''


def picture(name, caption, alt, sizes='(max-width: 700px) calc(100vw - 28px), calc(50vw - 34px)', eager=False, linked=True):
    data = images[name]
    variants = data['variants']
    srcset = ', '.join(f'{BASE}{filename} {width}w' for width,filename in variants)
    src = BASE + variants[-1][1]
    tag = (f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{data["width"]}" height="{data["height"]}" '
           f'alt="{escape(alt, quote=True)}" loading="{"eager" if eager else "lazy"}" decoding="async"'
           + (' fetchpriority="high"' if eager else '') + '>')
    if linked:
        tag = f'<a href="{src}" target="_blank" rel="noopener">{tag}</a>'
    return f'<figure class="ivory-figure">{tag}<figcaption>{escape(caption)}</figcaption></figure>'


def video(name, caption, label, portrait=False):
    cover = BASE + images[name+'-cover']['variants'][-1][1]
    data = next(x for x in report if x['file']==name+'.mp4')
    return (f'<figure class="ivory-figure"><video class="ivory-video{" portrait" if portrait else ""}" controls playsinline preload="none" '
            f'width="{data["width"]}" height="{data["height"]}" poster="{cover}" aria-label="{escape(label, quote=True)}">'
            f'<source src="{BASE}{name}.mp4" type="video/mp4"><a href="{BASE}{name}.mp4">{escape(label)}</a></video>'
            f'<figcaption>{escape(caption)}</figcaption></figure>')


for lang in ['en', 'it']:
    it = lang == 'it'
    def t(en, ita): return ita if it else en
    prefix = '/it' if it else ''
    path = ROOT / ('public/it/work/ivory/index.html' if it else 'public/work/ivory/index.html')
    html = path.read_text()
    # Keep the shared header, fonts, navigation, credits styles and footer intact.
    html = re.sub(r'<style(?: data-ivory)?>\s*\.ivory-grid.*?</style>', '<style data-ivory>'+CSS+'</style>', html, flags=re.S)
    description = t('Visual communication, social campaign and event production for COLLAPSE PARTY VOL IV with IVORY, at Formula Disco on 19 December 2025.',
                    'Comunicazione visiva, campagna social e produzione di COLLAPSE PARTY VOL IV con IVORY, al Formula Disco il 19 dicembre 2025.')
    html = re.sub(r'<meta name="description"[^>]*>', '', html)
    html = html.replace('</title>', '</title><meta name="description" content="'+escape(description, quote=True)+'">', 1)
    if 'src="/assets/video-playback.js"' not in html:
        html = html.replace('</head>', '<script defer src="/assets/video-playback.js"></script></head>')
    role = t('Creative direction · Graphic design · Photography · Event organisation and production', 'Direzione creativa · Graphic design · Fotografia · Organizzazione e produzione')
    main = f'''<main id="main">
<section class="hero"><div class="kicker"><span>COLLAPSE / EVENT</span><span>VOL IV / 2025</span></div><h1>IVORY</h1>
<div class="hero-grid"><div><p>{t('One night, one visual language. The communication and production of COLLAPSE PARTY VOL IV, with IVORY at Formula Disco.', 'Una serata, un linguaggio visivo. La comunicazione e la produzione di COLLAPSE PARTY VOL IV, con IVORY al Formula Disco.')}</p>
<div class="ivory-details"><span>19.12.2025</span><span>Formula Disco / Jeko Room</span></div></div>
<div class="meta"><div><b>{t('Project', 'Progetto')}</b>COLLAPSE / IVORY</div><div><b>{t('My role', 'Il mio ruolo')}</b>{role}</div></div></div></section>
<section class="section"><div class="section-head"><span class="n">01 / CAMPAIGN</span><h2>{t('Identity and motion', 'Identità e movimento')}</h2></div>
<div class="copy"><p>{t('Black and white, photographic grain and a restrained typographic system connect the guest announcement, the promotional reel and the event information.', 'Bianco e nero, grana fotografica e un sistema tipografico essenziale collegano l’annuncio dell’ospite, il reel promozionale e le informazioni sull’evento.')}</p><p>{t('The portrait of IVORY becomes the centre of a visual language that moves from the Instagram feed to stories and the venue entrance.', 'Il ritratto di IVORY diventa il centro di un linguaggio visivo che passa dal feed Instagram alle stories, fino all’ingresso del locale.')}</p></div>
<div class="ivory-campaign">{picture('poster', t('01 / Instagram post', '01 / Post Instagram'), t('IVORY event poster for COLLAPSE Private Party, 19 December 2025', 'Post dell’evento IVORY per COLLAPSE Private Party, 19 dicembre 2025'), eager=True)}{video('reel', t('02 / Promotional reel', '02 / Reel promozionale'), t('Play the IVORY promotional reel', 'Riproduci il reel promozionale IVORY'), True)}</div></section>
<section class="section"><div class="section-head"><span class="n">02 / SOCIAL SYSTEM</span><h2>{t('Before the night', 'Prima della serata')}</h2></div>
<div class="copy"><p>{t('The same visual system structures practical information: ticket releases, set times and the reserved entrance route. A coordinated series accompanies the audience from the announcement to the final tickets.', 'Lo stesso sistema visivo organizza le informazioni pratiche: uscite dei biglietti, orari dei set e percorso di accesso riservato. Una serie coordinata accompagna il pubblico dall’annuncio agli ultimi ticket.')}</p></div>
<div class="ivory-grid three">'''
    for name,en,ita in [('tickets-post','Tickets / Feed format','Biglietti / Formato feed'),('lineup-post','Set times / Feed format','Orari / Formato feed'),('access-post','Reserved entrance / Feed format','Accesso riservato / Formato feed')]:
        main += picture(name,t(en,ita),t(en,ita)+' — IVORY / COLLAPSE', '(max-width: 700px) calc(100vw - 28px), calc(33vw - 30px)')
    main += '</div><div class="ivory-grid stories">'
    for name,en,ita in [('announcement','Guest announcement','Annuncio ospite'),('close-friends','Close friends / Presale','Close friends / Prevendite'),('tickets-story','Ticket releases','Uscite biglietti'),('lineup-story','Set times','Orari dei set'),('access-story','Entrance map','Mappa degli accessi'),('ticket-benefits','Ticket benefits','Il ticket comprende'),('sold-out','Release update','Aggiornamento disponibilità'),('final-tickets','Final tickets','Ultimi biglietti')]:
        main += picture(name,t(en,ita),t(en,ita)+' — Instagram story / IVORY', '(max-width: 700px) calc(50vw - 20px), (max-width: 1000px) 30vw, 23vw')
    main += f'''</div></section>
<section class="section"><div class="section-head"><span class="n">03 / IN THE SPACE</span><h2>{t('From screen to venue', 'Dallo schermo allo spazio')}</h2></div>
<div class="copy"><p>{t('The exterior banner extends the campaign into the physical space. The COLLAPSE mark, IVORY portrait and directional arrow identify the entrance to the private party.', 'Il banner esterno porta la campagna nello spazio fisico. Il marchio COLLAPSE, il ritratto di IVORY e la freccia direzionale identificano l’accesso al private party.')}</p></div>
<div class="ivory-banner">{picture('banner',t('Exterior banner / Print artwork','Banner esterno / Esecutivo di stampa'),t('Wide COLLAPSE Private Party banner with IVORY portrait and entrance arrow','Banner orizzontale COLLAPSE Private Party con ritratto di IVORY e freccia d’ingresso'), 'calc(100vw - 44px)')}</div>
<div class="ivory-grid">{picture('banner-installation',t('Installation / Formula Disco','Montaggio / Formula Disco'),t('Installing the COLLAPSE banner above the venue entrance','Montaggio del banner COLLAPSE sopra l’ingresso del locale'))}{picture('banner-installed',t('The installed banner','Il banner installato'),t('COLLAPSE and IVORY banner installed above the entrance at night','Banner COLLAPSE e IVORY installato sopra l’ingresso di notte'))}</div></section>
<section class="section"><div class="section-head"><span class="n">04 / THE NIGHT</span><h2>{t('Inside the event', 'Dentro l’evento')}</h2></div>
<div class="copy"><p>{t('The video recap brings the project back to the dance floor: the audience, the music and the atmosphere of the night.', 'Il video recap riporta il progetto in pista: il pubblico, la musica e l’atmosfera della serata.')}</p></div>
<div class="ivory-recap">{video('recap',t('IVORY / Event recap','IVORY / Recap della serata'),t('Play the IVORY event recap','Riproduci il recap della serata IVORY'))}</div></section>
<section class="section"><div class="section-head"><span class="n">CREDITS</span><h2>Filippo Mantini</h2></div><p>{role}</p><a class="ivory-back" href="{prefix}/work/collapse/#archive">← COLLAPSE / ARCHIVE</a></section></main>'''
    html = re.sub(r'<main id="main">.*?</main>', main, html, flags=re.S)
    if 'ivory-placeholder' in html or 'Placeholder' in html:
        raise RuntimeError('Unreplaced placeholder')
    for local in re.findall(r'(?:src|poster)="(/assets/ivory/[^\"]+)"',html):
        assert (ROOT/'public'/local.lstrip('/')).is_file(), local
    path.write_text(html)

for asset in OUT.iterdir():
    assert 0 < asset.stat().st_size < 25 * 1024 * 1024, asset
    if asset.suffix == '.webp':
        with Image.open(asset) as check:
            check.verify()

original_bytes = sum((MEDIA / filename).stat().st_size for filename,_,_ in sources) + (MEDIA/'banner.pdf').stat().st_size + sum(x['original_bytes'] for x in report)
web_bytes = sum(p.stat().st_size for p in OUT.iterdir() if p.suffix in {'.webp','.mp4'})
print(json.dumps({'original_bytes': original_bytes, 'web_bytes_all_resolutions': web_bytes, 'videos': report}, indent=2))
