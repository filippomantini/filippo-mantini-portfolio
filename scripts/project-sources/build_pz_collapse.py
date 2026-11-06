"""Build the PZ. COLLAPSE case study with original event media."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[2]

def build(lang):
    it = lang == 'it'
    def t(a, b): return a if it else b
    pre = '/it' if it else ''
    other = '' if it else '/it'
    url = f'https://filippomantini.com{pre}/work/pz-collapse/'
    description = t('PZ. COLLAPSE: identità visiva e produzione del Collapse Private Party del 26 aprile 2025 al Formula Discoteque di Città di Castello. Ospiti Dukwa e Bannyblanco.', 'PZ. COLLAPSE: visual identity and production for Collapse Private Party, 26 April 2025, Formula Discoteque, Città di Castello. Guests Dukwa and Bannyblanco.')
    fonts = ''.join(f'@font-face{{font-family:"{family}";font-style:normal;font-weight:{weight};font-display:swap;src:url("/assets/fonts/{file}") format("woff2")}}' for family, weight, file in [('IBM Plex Mono',400,'ibm-plex-mono-400-10dee56a771c.woff2'),('Inter Tight',400,'inter-tight-400-e79c2a2c294d.woff2'),('Inter Tight',500,'inter-tight-500-4f629505454e.woff2'),('Inter Tight',600,'inter-tight-600-5b78c99e7cda.woff2')])
    def heading(n, label, title):
        return f'<div class="pz-section-head"><p class="pz-mono">{n} / {label}</p><h2>{title}</h2></div>'
    media = json.loads((ROOT / 'scripts/project-sources/pz-collapse-assets.json').read_text())
    def image(name, caption):
        filename = name + '.webp'
        m = media[filename]
        return f'<figure class="pz-figure"><a href="/assets/pz-collapse/{filename}" target="_blank" rel="noopener"><img src="/assets/pz-collapse/{filename}" width="{m["width"]}" height="{m["height"]}" alt="{escape(caption, quote=True)}" loading="lazy" decoding="async"></a><figcaption class="pz-mono">{caption}</figcaption></figure>'
    def video(name, caption):
        m = media[name + '.mp4']
        return f'<figure class="pz-figure"><video controls playsinline preload="none" width="{m["width"]}" height="{m["height"]}" poster="/assets/pz-collapse/{name}-poster.webp" aria-label="{escape(caption, quote=True)}"><source src="/assets/pz-collapse/{name}.mp4" type="video/mp4"><a href="/assets/pz-collapse/{name}.mp4">{caption}</a></video><figcaption class="pz-mono">{caption}</figcaption></figure>'
    campaign = '<div class="pz-campaign">' + image('instagram-post',t('01 / Post Instagram — grafica originale','01 / Instagram post — original artwork')) + video('announcement',t('02 / Video annuncio della serata','02 / Event announcement film')) + image('instagram-story',t('03 / Story e copertina reel','03 / Story and reel cover')) + '</div>'
    tickets = '<div class="pz-tickets">' + image('presale-mockup',t('01 / Prevendita cartacea — mockup di presentazione','01 / Paper presale — presentation mockup')) + '<div>' + image('metro-pass-mockup',t('02 / Tessere NFC — mockup originale di Filippo Mantini','02 / NFC passes — original mockup by Filippo Mantini')) + '</div></div><div class="pz-scan"><div><p class="pz-mono">NFC / PZ. COLLAPSE</p><h3>' + t('La tessera<br>in funzione.','The card<br>in use.') + '</h3><p>' + t('Il video originale mostra la lettura NFC della tessera: il riferimento all’abbonamento della metropolitana entra nel sistema di accesso alla serata.','The original video shows the card being read via NFC: the reference to a metro pass becomes part of the event entry system.') + '</p></div>' + video('nfc-entry',t('03 / Funzionamento della tessera NFC','03 / NFC card demonstration')) + '</div>'
    signs = '<div class="pz-signs">' + ''.join(image('sign-0'+str(i),t('Insegna originale / ','Original sign / ')+str(i).zfill(2)) for i in range(1,4)) + '</div>'
    room_films = '<div class="pz-room-films">' + video('room-setup',t('Prima della serata / Allestimento della sala','Before the event / Room setup')) + '</div>'
    roles = [
      ('01',t('Organizzazione','Organisation'),t('Gestione dell’evento, PR e coordinamento dei DJ.','Event management, PR and DJ coordination.')),
      ('02',t('Identità e social','Identity & social'),t('Disegno dell’identità visiva e dei contenuti per post e stories.','Visual identity design and content for posts and stories.')),
      ('03',t('Produzione fisica','Physical production'),t('Disegno e ordine di gadget, prevendite e tessere d’ingresso.','Design and ordering of merchandise, paper presales and entry cards.')),
      ('04',t('Allestimento','Venue setup'),t('Costruzione e montaggio dell’identità nella sala, incluse le insegne.','Building and installing the identity inside the room, including signage.')),
    ]
    steps = [
      ('01',t('La prevendita.','The presale.'),t('La prevendita cartacea anticipava l’esperienza della serata: il primo elemento fisico dell’identità, prima di arrivare al locale.','The paper presale introduced the night’s experience: the first physical element of the identity, before arriving at the venue.')),
      ('02',t('La tessera.','The card.'),t('All’ingresso il cliente riceveva una tessera simile a un abbonamento della metropolitana. Il tema diventava un oggetto da utilizzare.','At the entrance, each customer received a card resembling a metro pass. The theme became an object to use.')),
      ('03',t('L’accesso in sala.','Entering the room.'),t('La tessera veniva scannerizzata all’ingresso della sala per entrare. Il passaggio completava il riferimento al viaggio in metropolitana.','The card was scanned at the entrance to the room to gain access. This final step completed the reference to travelling on the metro.')),
    ]
    role_html = ''.join(f'<article><span class="pz-mono">{n}</span><h3>{h}</h3><p>{p}</p></article>' for n,h,p in roles)
    step_html = ''.join(f'<article class="pz-step"><span class="pz-step-num">{n}</span><h3>{h}</h3><p>{p}</p></article>' for n,h,p in steps)
    nav = ''.join(f'<a href="#{id}"><span>{n} / {label}</span><span aria-hidden="true">↓</span></a>' for n,id,label in [('01','identity',t('Identità','Identity')),('02','direction',t('Direzione','Direction')),('03','access',t('Accesso','Access')),('04','room',t('La sala','The room'))])
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PZ. COLLAPSE — Metro Party / Filippo Mantini</title><meta name="description" content="{escape(description, quote=True)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="PZ. COLLAPSE — Metro Party / Filippo Mantini"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">
<link rel="alternate" hreflang="en" href="https://filippomantini.com/work/pz-collapse/"><link rel="alternate" hreflang="it" href="https://filippomantini.com/it/work/pz-collapse/"><link rel="alternate" hreflang="x-default" href="https://filippomantini.com/work/pz-collapse/">
<link rel="icon" href="/favicon.svg?v=7" type="image/svg+xml"><style>{fonts}</style>
<link rel="stylesheet" href="/assets/static/project-5497922a5cc4.css"><link rel="stylesheet" href="/assets/portfolio-finish-c620ab7df046.css"><link rel="stylesheet" href="/assets/portfolio-footer-9de7b03c7c85.css"><link rel="stylesheet" href="/assets/pz-collapse.css">
<style>.pz-opening{{position:relative;background:#140809}}.pz-opening video{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain}}.pz-opening-title{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}}</style>
<script defer src="/assets/static/project-cursor-10bb0092983c.js"></script></head>
<body><a class="portfolio-skip" href="#main">{t('Salta al contenuto','Skip to content')}</a><div class="site-cursor" id="siteCursor" aria-hidden="true"></div>
<header class="topbar"><a class="name" href="{pre}/">FILIPPO MANTINI</a><nav><a href="{pre}/#work">Work</a><a href="{pre}/#photo">Photo</a><a href="{pre}/work/filippo-mantini-studio/">Studio AI</a><a href="{pre}/about/">About</a><a href="{other}/work/pz-collapse/" lang="{t('en','it')}" hreflang="{t('en','it')}">{t('EN','IT')}</a></nav><a class="back" href="{pre}/work/collapse/">← COLLAPSE</a></header>
<main id="main" class="pz">
<section class="pz-opening" aria-label="PZ. COLLAPSE"><h1 class="pz-opening-title">PZ. COLLAPSE — PRIVATE PARTY</h1><video controls playsinline preload="metadata" width="1280" height="720" poster="/assets/pz-collapse/after-party-poster.webp" aria-label="{t('Video della serata','Event film')}"><source src="/assets/pz-collapse/after-party.mp4" type="video/mp4"></video></section>
<section class="pz-hero" aria-label="Collapse Private Party">
<div class="pz-hero-grid"><div class="pz-station"><p class="pz-mono"><span>COLLAPSE</span><small>26 / 04 / 25</small></p><h2>PRIVATE<br>PARTY.</h2></div><div class="pz-guests"><p class="pz-mono">{t('OSPITI','GUESTS')}</p><div><strong>DUKWA</strong><strong>BANNYBLANCO</strong></div><p class="pz-venue pz-mono">FORMULA DISCOTEQUE<br>CITTÀ DI CASTELLO / ITALIA</p></div></div></section>
<div class="pz-intro"><div><p class="pz-mono">{t('IL CONCEPT','THE CONCEPT')}</p><p class="pz-lead">{t('Una fermata della metro rossa di Milano.<br>Destinazione: COLLAPSE.','A stop on Milan’s red metro line.<br>Destination: COLLAPSE.')}</p><p class="pz-copy">{t('Il 26 aprile 2025, il Collapse Private Party al Formula Discoteque di Città di Castello prendeva la forma di una fermata immaginaria: PZ. COLLAPSE. Con Dukwa e Bannyblanco, il linguaggio della metropolitana univa comunicazione, oggetti d’ingresso e spazio della serata.','On 26 April 2025, Collapse Private Party at Formula Discoteque in Città di Castello took the form of an imaginary stop: PZ. COLLAPSE. With Dukwa and Bannyblanco, the language of the metro connected communication, entry objects and the venue.')}</p></div><div><p class="pz-mono">{t('IL MIO RUOLO','MY ROLE')}</p><p class="pz-lead">{t('Dall’idea<br>alla sala.','From the idea<br>to the room.')}</p><p class="pz-copy">{t('Ho seguito l’intero progetto: organizzazione, PR e DJ, identità visiva e post, disegno e ordine di gadget e ticket, fino alla costruzione e al montaggio dell’allestimento nella sala.','I managed the entire project: organisation, PR and DJs, visual identity and posts, the design and ordering of merchandise and tickets, through to building and installing the venue setup.')}</p></div></div>
<nav class="pz-nav pz-mono" aria-label="{t('Capitoli del progetto','Project chapters')}">{nav}</nav>
<section class="pz-section" id="identity">{heading('01',t('IDENTITÀ VISIVA','VISUAL IDENTITY'),t('Il linguaggio<br>della linea rossa.','The language<br>of the red line.'))}
<div class="pz-section-copy"><p>{t('Rosso e bianco, grandi scritte e griglie di composizione visibili: l’identità riprende il linguaggio della metropolitana e lo porta dentro il Collapse Private Party.','Red and white, oversized lettering and visible composition grids: the identity draws on the language of the metro and brings it into Collapse Private Party.')}</p><p>{t('La comunicazione si muove fra formati digitali e supporti fisici. Post e stories annunciano la serata; prevendite, tessere e insegne accompagnano il pubblico fino alla sala.','The communication moves between digital formats and physical objects. Posts and stories announce the night; presales, cards and signs accompany guests into the room.')}</p></div>
{campaign}
<div class="pz-identity" aria-label="{t('Composizione tipografica del progetto','Project typographic composition')}"><div><span class="pz-mono">PZ. COLLAPSE / 2025</span><p class="pz-word">PRIVATE<br>PARTY.</p><span class="pz-mono">FORMULA DISCOTEQUE</span></div><div class="pz-red-cell"><span class="pz-mono">{t('DATA','DATE')}</span><p class="pz-date">26<br>04</p><span class="pz-mono">2025</span></div><div><span class="pz-mono">{t('CODICE COLORE','COLOUR CODE')}</span><p class="pz-colors" aria-hidden="true"><i></i><i></i></p><span class="pz-mono">{t('ROSSO<br>BIANCO','RED<br>WHITE')}</span></div></div></section>
<section class="pz-section" id="direction">{heading('02',t('DIREZIONE & PRODUZIONE','DIRECTION & PRODUCTION'),t('Un progetto.<br>Ogni passaggio.','One project.<br>Every step.'))}
<div class="pz-section-copy"><p>{t('Ho gestito sia la parte organizzativa sia quella visiva: dal coordinamento delle persone alla realizzazione degli elementi che costruivano l’esperienza della serata.','I managed both the organisational and visual sides: from coordinating the people involved to producing the elements that shaped the experience of the night.')}</p><p>{t('L’identità non si fermava alla promozione. Proseguiva nei materiali stampati, nei gadget, nel sistema di accesso e nell’allestimento fisico del locale.','The identity extended beyond promotion into printed materials, merchandise, the entry system and the physical setup of the venue.')}</p></div><div class="pz-roles">{role_html}</div></section>
<div class="pz-divider" aria-hidden="true"><span>&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;</span></div>
<section class="pz-section" id="access">{heading('03',t('PREVENDITA & ACCESSO','PRESALE & ENTRY'),t('Il biglietto diventa<br>un abbonamento.','The ticket becomes<br>a metro pass.'))}
<div class="pz-section-copy"><p>{t('Due oggetti distinti, due momenti dell’esperienza: la prevendita cartacea prima della serata e la tessera consegnata all’ingresso.','Two distinct objects, two moments in the experience: the paper presale before the night and the card handed out at the entrance.')}</p><p>{t('La tessera, simile a un abbonamento della metropolitana, veniva scannerizzata per accedere alla sala. Il gesto dell’ingresso faceva parte del concept.','The card, resembling a metro pass, was scanned to access the room. The act of entering was part of the concept.')}</p></div><div class="pz-journey">{step_html}</div>
{tickets}

</section>
<section class="pz-section pz-room" id="room">{heading('04',t('ALLESTIMENTO & ORIENTAMENTO','SETUP & WAYFINDING'),t('La fermata<br>prende spazio.','The stop<br>takes shape.'))}
<div class="pz-section-copy"><p>{t('Ho costruito e montato gli elementi dell’identità all’interno della sala. Il riferimento alla fermata della metro diventava un ambiente da attraversare, oltre che un’immagine da vedere.','I built and installed the identity elements inside the room. The metro stop reference became an environment to move through, as well as an image to see.')}</p><p>{t('Ho disegnato tre insegne da stampare e appendere nel locale come guida per le persone. Comunicazione e orientamento condividevano lo stesso linguaggio.','I designed three signs to be printed and hung inside the venue to guide guests. Communication and wayfinding shared the same visual language.')}</p></div>
<div class="pz-room-grid"><div><strong>03</strong><span class="pz-mono">{t('INSEGNE / DISEGNO & STAMPA','SIGNS / DESIGN & PRINT')}</span></div><div><span class="pz-mono">PZ. COLLAPSE / FORMULA</span><h3>{t('Identità.<br>Spazio.<br>Persone.','Identity.<br>Space.<br>People.')}</h3><p>{t('Dai contenuti social agli elementi appesi nella sala: un unico progetto per raccontare la serata e accompagnare chi la viveva.','From social content to the elements hung inside the room: one project to communicate the night and guide the people experiencing it.')}</p></div></div>
{signs}{room_films}
</section>
<div class="pz-end pz-mono"><span>PZ. COLLAPSE / 26.04.2025</span><a href="{pre}/work/collapse/#archive">{t('TORNA A COLLAPSE','BACK TO COLLAPSE')} ↗</a></div>
<section class="pz-credits" aria-labelledby="pz-credits"><h2 id="pz-credits" class="pz-mono">{t('CREDITI / PROGETTO','PROJECT CREDITS')}</h2><p><b>Filippo Mantini</b><br>{t('Organizzazione · PR e coordinamento DJ · Identità visiva · Comunicazione social · Disegno e ordine di gadget e ticket · Costruzione e montaggio dell’allestimento','Organisation · PR and DJ coordination · Visual identity · Social communication · Merchandise and ticket design and ordering · Venue setup construction and installation')}<br><br><b>COLLAPSE PRIVATE PARTY</b><br>Dukwa · Bannyblanco / Formula Discoteque, Città di Castello / 26.04.2025</p></section>
</main><footer id="contact" class="portfolio-footer" data-portfolio-footer><h2>LET'S BUILD<br>SOMETHING<br><span>TOGETHER.</span></h2><div class="bottom"><span>Filippo Mantini © 2026</span><a href="mailto:info@filippomantini.com">info@filippomantini.com ↗</a><span class="footer-links"><a href="{pre}/privacy/">Privacy</a><span>Portfolio FM</span></span></div></footer></body></html>'''
    path = ROOT / f'public{pre}/work/pz-collapse/index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)

if __name__ == '__main__':
    for language in ('it', 'en'):
        build(language)
