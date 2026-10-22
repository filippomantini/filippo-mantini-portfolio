"""Build the bilingual portfolio case study. The public interface is a presentation,
not a running copy of Studio; no application source, account or private data ships.
Reference: Studio V3.3.2 campus/studio-home/mailboxes/production + editorial.css.
"""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2]
A=R/'public/assets'
assets={}
for name in ['studio-project.css','studio-project.js']:
 p=A/name; h=hashlib.sha256(p.read_bytes()).hexdigest()[:12]; target=p.stem+'-'+h+p.suffix
 (A/target).write_bytes(p.read_bytes());assets[p.suffix]=target
T={
'it':{
 'title':'Filippo Mantini Studio — Interfaccia e progetto digitale',
 'description':'Il caso studio di Filippo Mantini Studio: un’app locale privata per posta, progetti e produzione video. Interfaccia, flussi e demo con dati di esempio.',
 'skip':'Vai al contenuto','portfolio':'Portfolio','project':'Il progetto','other':'EN','otherlabel':'Read this project in English',
 'eyebrow':'Progetto indipendente / Prodotto digitale','status':'Applicazione locale / In sviluppo',
 'lead':'Uno spazio personale per seguire la posta, organizzare i progetti e preparare i contenuti. Progettato a partire dal lavoro di ogni giorno.',
 'explore':'Esplora l’interfaccia','meta':['Ambito','Contributo','Stato'],
 'values':['Strumenti per il lavoro creativo','Direzione del progetto · UI · Flussi operativi','Progetto personale in evoluzione'],
 'showtitle':'L’interfaccia / Una vista del prodotto','shownote':'Seleziona una vista per esplorare la presentazione. I dati sono di esempio; nessun account è collegato.',
 'caption':'Ricostruzione dell’interfaccia dal codice Studio V3.3.2','caption2':'Dati dimostrativi / Nessuna operazione su account reali',
 'contextlabel':'01 / Il punto di partenza','contexttitle':'Organizzare anche ciò che sta intorno al progetto.',
 'contextp':'Un progetto creativo comprende anche richieste, file, scadenze e decisioni. Studio riunisce queste attività in un ambiente personale, per mantenere visibile il lavoro da seguire.',
 'contextp2':'Il progetto mette in relazione progettazione grafica e strumenti digitali: gerarchie tipografiche, navigazione e flussi vengono costruiti intorno alle attività quotidiane, dalla posta alla preparazione di un video.',
 'flowlabel':'02 / La logica del prodotto','flowtitle':'Prima capire.<br>Poi decidere.',
 'flowintro':'L’interfaccia distingue la lettura delle informazioni dalle azioni che le modificano. La revisione è un passaggio del flusso, con stati e conferme visibili.',
 'flows':[('Leggere','Riunire richieste, attività aperte e risultati nella vista Oggi. Le sezioni dedicate permettono poi di entrare nel dettaglio.'),('Organizzare','Suddividere la posta, associare incarichi ai progetti e preparare brief, script e schede per i contenuti.'),('Approvare','Verificare proposte e risultati prima delle azioni. Le modifiche alla posta seguono un percorso di conferma esplicito.')],
 'designlabel':'03 / Il linguaggio visivo','designtitle':'Un’interfaccia da leggere, prima che da guardare.',
 'designp':'Tipografia essenziale, indici e linee sottili organizzano le informazioni. La stessa struttura si ripete nelle diverse sezioni, così il cambio di attività non richiede di imparare ogni volta una nuova interfaccia.',
 'typecaption':'Tipografia dell’app / Helvetica, Arial','typetext':'Titoli, liste e stati. Una gerarchia editoriale applicata a uno strumento operativo.',
 'palette':'Carta / Inchiostro / Terracotta','palettep':'Fondi chiari e scuri, testo ad alto contrasto e un accento per gli elementi da verificare.',
 'system':'Una struttura, più sezioni','systemp':'Navigazione laterale, contenuti centrali e stati leggibili. Su mobile la struttura si ricompone in una colonna.',
 'statelabel':'04 / Stato del progetto','statetitle':'Uno strumento personale.<br>Un progetto aperto.',
 'stateintro':'Studio viene eseguito localmente sul computer. Questa pagina presenta il progetto e una ricostruzione dimostrativa dell’interfaccia; non permette di accedere all’app privata.',
 'states':[('Nell’app','Vista quotidiana, progetti e incarichi, gestione della posta e preparazione della produzione video.'),('Su consenso','Le connessioni ai servizi Google richiedono l’autorizzazione dell’utente. Le funzioni dipendono dai servizi e dai motori effettivamente configurati.'),('Da sviluppare','Verificare l’utilizzo quotidiano e semplificare i percorsi più frequenti, senza aggiungere complessità alla navigazione.')],
 'privacytitle':'Servizi Google e uso dei dati','privacyp':'Filippo Mantini Studio può connettersi a Gmail, previo consenso, per leggere, classificare e gestire la posta. Le operazioni che modificano i messaggi richiedono una conferma esplicita. Accesso ai dati e revoca delle autorizzazioni sono descritti nell’',
 'privacylink':'informativa privacy di Studio','credit':'Direzione del progetto e interfaccia: Filippo Mantini. Sviluppo assistito da strumenti AI.',
 'endlabel':'Filippo Mantini / Design e sistemi digitali','endtitle':'Dal progetto visivo<br>allo strumento di lavoro.',
 'contact':'Parliamone','footer':'Tutti i progetti','privacy':'Privacy Studio',
 'demo':{
 'operating':'STUDIO / OPERATING SYSTEM','space':'IL TUO SPAZIO','nav':['Oggi','Posta','Produzione video'],'local':'Presentazione / Dati di esempio','header':'STUDIO / DIREZIONE QUOTIDIANA','dark':'Tema scuro','light':'Tema chiaro','sample':'DATI DI ESEMPIO',
 'kicker':'FM—00 / Direzione quotidiana','headline':'Il lavoro,<br>in ordine.','intro':'La posta da seguire. Le idee da sviluppare.<br>Le decisioni che aspettano te.',
 'next':'IL PROSSIMO PASSO','nexttitle':'Controlla i risultati pronti.','nextp':'Leggi le bozze e gli output prima di approvare le azioni.',
 'metrics':['Posta da seguire','Da approvare','Incarichi in corso','Gmail collegate'],'digest':'La posta, in sintesi.','categories':['Richieste e preventivi','Documenti da verificare','Notifiche di sicurezza','Newsletter e promozioni'],
 'decisions':'Il controllo resta tuo.','decision1':'Risposte e azioni sulla posta','decision2':'Risultati degli agenti','footnote':'Esempio di organizzazione del lavoro. Contatori e contenuti sono dimostrativi.',
 'mailkicker':'FM—01 / Segreteria','mailtitle':'La posta,<br>da seguire.','mailintro':'Richieste, documenti e newsletter. Una vista per riconoscere le priorità prima di intervenire.',
 'mailrows':[('Studio esempio','Richiesta di preventivo','Da verificare'),('Archivio esempio','Documenti di progetto','Documento'),('Newsletter esempio','Novità della settimana','Newsletter')],
 'mailnotice':'Prima di modificare i messaggi: controlla la selezione e conferma l’operazione. Nella presentazione non viene letta o modificata alcuna email.',
 'videokicker':'FM—03 / Produzione video','videotitle':'Dal brief<br>alle scene.','videointro':'Un esempio di scheda di produzione: obiettivo, script e scene raccolti nello stesso progetto.',
 'steps':['Brief','Sceneggiatura','Scene','Revisione'],'scene':'01 / Scheda di esempio','scenetitle':'Presentare un oggetto.','scenep':'Un breve contenuto per raccontare forma e materia, dal dettaglio alla vista completa.',
 'checks':['Obiettivo e pubblico','Inquadrature e movimento','Audio e montaggio','Verifica dei materiali'],
 'videonotice':'La produzione è organizzata nello Studio. I media vengono generati o realizzati con strumenti esterni e importati per la verifica; nessuna pubblicazione automatica.'
 }},
'en':{
 'title':'Filippo Mantini Studio — Interface & Digital Product',
 'description':'The Filippo Mantini Studio case study: a private local app for email, projects and video production. Interface design, workflows and a sample-data demo.',
 'skip':'Skip to content','portfolio':'Portfolio','project':'The project','other':'IT','otherlabel':'Leggi il progetto in italiano',
 'eyebrow':'Independent project / Digital product','status':'Local application / In development',
 'lead':'A personal workspace for following up on email, organising projects and preparing content. Designed around the work of an ordinary day.',
 'explore':'Explore the interface','meta':['Field','Contribution','Status'],
 'values':['Tools for creative work','Project direction · UI · Operational workflows','Ongoing personal project'],
 'showtitle':'The interface / A product view','shownote':'Select a view to explore the presentation. All data is illustrative; no account is connected.',
 'caption':'Interface reconstructed from Studio V3.3.2 source code','caption2':'Sample data / No actions on real accounts',
 'contextlabel':'01 / Starting point','contexttitle':'Organising the work around the project.',
 'contextp':'Creative projects also involve requests, files, deadlines and decisions. Studio brings these activities into a personal environment, keeping the work that needs attention visible.',
 'contextp2':'The project connects graphic design with digital tools: typographic hierarchy, navigation and workflows are built around daily activities, from email to preparing a video.',
 'flowlabel':'02 / Product logic','flowtitle':'Understand first.<br>Then decide.',
 'flowintro':'The interface separates reading information from actions that change it. Review is a distinct step in the workflow, with visible states and confirmations.',
 'flows':[('Read','Bring requests, open tasks and results together in the Today view. Dedicated sections provide the details.'),('Organise','Sort email, assign tasks to projects and prepare briefs, scripts and content production sheets.'),('Approve','Check proposals and results before taking action. Changes to email follow an explicit confirmation process.')],
 'designlabel':'03 / Visual language','designtitle':'An interface designed to be read.',
 'designp':'Simple typography, indices and fine rules organise the information. The same structure runs through the different sections, so changing tasks does not require learning a new interface.',
 'typecaption':'Application typography / Helvetica, Arial','typetext':'Headings, lists and states. An editorial hierarchy applied to an operational tool.',
 'palette':'Paper / Ink / Terracotta','palettep':'Light and dark surfaces, high-contrast text and an accent for items that need review.',
 'system':'One structure, several sections','systemp':'Sidebar navigation, a central content area and readable states. On mobile, the structure becomes a single column.',
 'statelabel':'04 / Project status','statetitle':'A personal tool.<br>An ongoing project.',
 'stateintro':'Studio runs locally on a computer. This page presents the project and an illustrative reconstruction of its interface; it does not provide access to the private application.',
 'states':[('In the app','Daily overview, projects and tasks, email management and preparation for video production.'),('With consent','Google service connections require user authorisation. Available features depend on the services and engines actually configured.'),('Next steps','Evaluate everyday use and simplify the most frequent workflows without adding complexity to navigation.')],
 'privacytitle':'Google services and data use','privacyp':'With user consent, Filippo Mantini Studio can connect to Gmail to read, classify and manage email. Actions that modify messages require explicit confirmation. Data access and revoking authorisation are explained in the ',
 'privacylink':'Studio privacy policy','credit':'Project direction and interface: Filippo Mantini. Development assisted by AI tools.',
 'endlabel':'Filippo Mantini / Design and digital systems','endtitle':'From visual design<br>to a working tool.',
 'contact':'Get in touch','footer':'All projects','privacy':'Studio privacy',
 'demo':{
 'operating':'STUDIO / OPERATING SYSTEM','space':'YOUR WORKSPACE','nav':['Today','Email','Video production'],'local':'Presentation / Sample data','header':'STUDIO / DAILY OVERVIEW','dark':'Dark theme','light':'Light theme','sample':'SAMPLE DATA',
 'kicker':'FM—00 / Daily overview','headline':'Work,<br>in order.','intro':'Email to follow up on. Ideas to develop.<br>Decisions waiting for you.',
 'next':'THE NEXT STEP','nexttitle':'Review the results.','nextp':'Read drafts and outputs before approving actions.',
 'metrics':['Email to follow up','Awaiting approval','Tasks in progress','Connected Gmail accounts'],'digest':'Email, at a glance.','categories':['Requests and quotes','Documents to review','Security notifications','Newsletters and promotions'],
 'decisions':'You stay in control.','decision1':'Replies and email actions','decision2':'Agent outputs','footnote':'An example of how work is organised. Counts and content are illustrative.',
 'mailkicker':'FM—01 / Email desk','mailtitle':'Email,<br>to follow up.','mailintro':'Requests, documents and newsletters. A view for identifying priorities before taking action.',
 'mailrows':[('Example studio','Request for a quote','To review'),('Example archive','Project documents','Document'),('Example newsletter','This week’s updates','Newsletter')],
 'mailnotice':'Before modifying messages: review the selection and confirm the action. This presentation does not read or change any email.',
 'videokicker':'FM—03 / Video production','videotitle':'From brief<br>to scenes.','videointro':'A sample production sheet: objective, script and scenes in one project.',
 'steps':['Brief','Script','Scenes','Review'],'scene':'01 / Sample sheet','scenetitle':'Introducing an object.','scenep':'A short piece of content exploring form and material, from details to a complete view.',
 'checks':['Objective and audience','Framing and movement','Audio and editing','Material review'],
 'videonotice':'Production is organised in Studio. Media is created with external tools and imported for review; nothing is published automatically.'
 }}
}

def demo(d):
 nav=''.join(f'<a href="#{id}" data-screen="{id}"><small>{n}</small>{label}</a>' for id,n,label in zip(['studio-today','studio-mail','studio-video'],['00','01','03'],d['nav']))
 metrics=''.join(f'<div><span class="demo-kicker">0{i+1} / {label}</span><strong>{value}</strong></div>' for i,(label,value) in enumerate(zip(d['metrics'],[3,2,0,0])))
 digest=''.join(f'<div class="demo-row"><span>{label}</span><b>{value}</b></div>' for label,value in zip(d['categories'],[2,1,0,8]))
 mail=''.join(f'<div class="demo-mail-row"><span class="mail-no">0{i+1}</span><b>{sender}</b><span>{subject}</span><span>{state}</span></div>' for i,(sender,subject,state) in enumerate(d['mailrows']))
 steps=''.join(f'<span class="{"active" if i==1 else ""}"><b>0{i+1}</b>{x}</span>' for i,x in enumerate(d['steps']))
 checks=''.join(f'<li>{x}</li>' for x in d['checks'])
 return f'''<div class="demo-shell" data-studio-demo><aside class="demo-side"><div class="demo-brand">FILIPPO<br> MANTINI<small>{d['operating']}</small></div><span>{d['space']}</span><nav class="demo-nav" aria-label="{d['local']}">{nav}</nav><div class="demo-signature">{d['local']}<br>STUDIO / V3.3</div></aside><div class="demo-main"><div class="demo-top"><span>{d['sample']}</span><button type="button" data-demo-theme data-dark="{d['dark']}" data-light="{d['light']}" aria-pressed="false" hidden>{d['dark']}</button></div>
 <section class="demo-view" id="studio-today" aria-labelledby="today-heading"><div class="demo-intro"><div><span class="demo-kicker">{d['kicker']}</span><h3 id="today-heading">{d['headline']}</h3><p>{d['intro']}</p></div><div class="demo-note"><span class="demo-kicker">{d['next']}</span><h4>{d['nexttitle']}</h4><p>{d['nextp']}</p></div></div><div class="demo-metrics">{metrics}</div><div class="demo-columns"><div><h4>{d['digest']}</h4>{digest}</div><div><h4>{d['decisions']}</h4><div class="demo-row"><span class="demo-count">1</span><span>{d['decision1']}</span></div><div class="demo-row"><span class="demo-count">1</span><span>{d['decision2']}</span></div></div></div><p class="demo-status">{d['footnote']}</p></section>
 <section class="demo-view" id="studio-mail" aria-labelledby="mail-heading"><span class="demo-kicker">{d['mailkicker']}</span><div class="demo-mail-head"><div><h3 id="mail-heading">{d['mailtitle']}</h3><p>{d['mailintro']}</p></div><span class="demo-kicker">{d['sample']}</span></div><div class="demo-mail-list">{mail}</div><div class="demo-callout">{d['mailnotice']}</div><p class="demo-status">{d['footnote']}</p></section>
 <section class="demo-view" id="studio-video" aria-labelledby="video-heading"><span class="demo-kicker">{d['videokicker']}</span><h3 id="video-heading">{d['videotitle']}</h3><p>{d['videointro']}</p><div class="demo-video-steps">{steps}</div><div class="demo-script"><div class="scene"><span class="demo-kicker">{d['scene']}</span><h4>{d['scenetitle']}</h4><p>{d['scenep']}</p></div><div class="scene"><span class="demo-kicker">{d['steps'][3]}</span><ul>{checks}</ul></div></div><div class="demo-callout">{d['videonotice']}</div></section></div></div>'''

for lang,t in T.items():
 prefix='/it' if lang=='it' else ''
 path=prefix+'/work/filippo-mantini-studio/'
 alternate=('/work/filippo-mantini-studio/' if lang=='it' else '/it/work/filippo-mantini-studio/')
 url='https://filippomantini.com'+path
 schema={'@context':'https://schema.org','@type':'CreativeWork','@id':url+'#project','name':'Filippo Mantini Studio','url':url,'description':t['description'],'inLanguage':lang,'creator':{'@type':'Person','name':'Filippo Mantini','url':'https://filippomantini.com/'},'genre':['Interface design','Digital product design'],'image':'https://filippomantini.com/assets/studio/studio-cover.png','isAccessibleForFree':True}
 archive=f'''<aside class="related-work" aria-labelledby="visual-title"><div class="related-head"><div><span class="label">{'Dal portfolio / Grafica originale' if lang=='it' else 'From the portfolio / Original artwork'}</span><h2 id="visual-title">COLLAPSE EXHIBITION<br>{'Bracciale cartaceo.' if lang=='it' else 'Paper wristband.'}</h2></div><a class="text-link" href="{prefix}/work/rebuild-yourself/">{'Scopri il progetto completo' if lang=='it' else 'View the full project'} <span aria-hidden="true">↗</span></a></div><figure><div class="related-artwork"><img src="/assets/rebuild-v5/wristband.webp" alt="{'Grafica originale del bracciale cartaceo COLLAPSE EXHIBITION + PRIVATE PARTY: tipografia nera, segno viola e data 30.08.2025' if lang=='it' else 'Original COLLAPSE EXHIBITION + PRIVATE PARTY paper wristband artwork: black typography, purple mark and date 30.08.2025'}" width="2000" height="194" loading="lazy" decoding="async"></div><figcaption>{'Grafica originale / Access design / COLLAPSE EXHIBITION' if lang=='it' else 'Original artwork / Access design / COLLAPSE EXHIBITION'}</figcaption></figure></aside>'''
 meta=''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label,value in zip(t['meta'],t['values']))
 flows=''.join(f'<li><span>0{i+1}</span><h3>{title}</h3><p>{body}</p></li>' for i,(title,body) in enumerate(t['flows']))
 states=''.join(f'<li><b>{label}</b><span>{body}</span></li>' for label,body in t['states'])
 html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t['title']} | Filippo Mantini</title><meta name="description" content="{t['description']}"><meta name="theme-color" content="#191918"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="it" href="https://filippomantini.com/it/work/filippo-mantini-studio/"><link rel="alternate" hreflang="en" href="https://filippomantini.com/work/filippo-mantini-studio/"><link rel="alternate" hreflang="x-default" href="https://filippomantini.com/work/filippo-mantini-studio/"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="preload" href="/assets/fonts/inter-tight-400-e79c2a2c294d.woff2" as="font" type="font/woff2" crossorigin><meta property="og:type" content="article"><meta property="og:site_name" content="Filippo Mantini"><meta property="og:title" content="{t['title']}"><meta property="og:description" content="{t['description']}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{'it_IT' if lang=='it' else 'en_GB'}"><meta property="og:image" content="https://filippomantini.com/assets/studio/studio-cover.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Filippo Mantini Studio — Interface design"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t['title']}"><meta name="twitter:description" content="{t['description']}"><meta name="twitter:image" content="https://filippomantini.com/assets/studio/studio-cover.png"><link rel="stylesheet" href="/assets/{assets['.css']}"><script src="/assets/{assets['.js']}" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{t['skip']}</a><header class="site-header"><a class="site-brand" href="{prefix}/" aria-label="Filippo Mantini — {t['portfolio']}">FILIPPO<br>MANTINI</a><nav aria-label="{t['portfolio']}"><a href="{prefix}/">{t['portfolio']}</a><a href="#project">{t['project']}</a><a class="language" href="{alternate}" lang="{'en' if lang=='it' else 'it'}" hreflang="{'en' if lang=='it' else 'it'}" aria-label="{t['otherlabel']}">{t['other']}</a></nav></header>
<main id="main"><section class="hero" aria-labelledby="project-title"><div class="hero-index label"><span>{t['eyebrow']}</span><span>{t['status']}</span></div><div class="hero-heading"><h1 id="project-title">FILIPPO<br>MANTINI<span>STUDIO.</span></h1><div class="hero-intro"><p>{t['lead']}</p><a class="text-link" href="#interface">{t['explore']} <span aria-hidden="true">↓</span></a></div></div><dl class="project-meta">{meta}</dl><section class="showcase" id="interface" aria-labelledby="interface-title"><div class="showcase-head"><h2 class="label" id="interface-title">{t['showtitle']}</h2><p>{t['shownote']}</p></div>{demo(t['demo'])}<div class="demo-caption"><span>{t['caption']}</span><span>{t['caption2']}</span></div></section></section>
<div class="case-body"><section class="case-section" id="project" aria-labelledby="context-title"><span class="label">{t['contextlabel']}</span><div><h2 id="context-title">{t['contexttitle']}</h2><div class="case-copy"><p>{t['contextp']}</p><p class="case-detail">{t['contextp2']}</p></div></div></section>
<section class="case-section" aria-labelledby="flow-title"><span class="label">{t['flowlabel']}</span><div><h2 id="flow-title">{t['flowtitle']}</h2><div class="case-copy"><p>{t['flowintro']}</p></div><ol class="workflow">{flows}</ol></div></section>
<section class="case-section" aria-labelledby="design-title"><span class="label">{t['designlabel']}</span><div><h2 id="design-title">{t['designtitle']}</h2><div class="case-copy"><p>{t['designp']}</p></div><div class="design-board"><div class="design-type"><span class="label">{t['typecaption']}</span><strong>Aa 01</strong><p>{t['typetext']}</p></div><div class="design-rules"><div><div class="swatches" aria-label="{t['palette']}"><span style="--swatch:#efeee8"></span><span style="--swatch:#191918"></span><span style="--swatch:#a44629"></span></div><p>{t['palettep']}</p></div><div><span class="label">{t['system']}</span><p>{t['systemp']}</p></div></div></div></div></section>
<section class="case-section" aria-labelledby="status-title"><span class="label">{t['statelabel']}</span><div><h2 id="status-title">{t['statetitle']}</h2><div class="case-copy"><p>{t['stateintro']}</p></div><ul class="state-list">{states}</ul><details class="privacy"><summary>{t['privacytitle']}</summary><p>{t['privacyp']}<a href="/studio/privacy/">{t['privacylink']}</a>.</p><p><a href="mailto:filippomantini00@gmail.com">filippomantini00@gmail.com</a></p></details><p class="label case-detail" style="margin-top:30px">{t['credit']}</p></div></section></div>
{archive}<section class="project-end" aria-labelledby="end-title"><div><span class="label">{t['endlabel']}</span><h2 id="end-title">{t['endtitle']}</h2></div><a class="text-link" href="mailto:filippomantini00@gmail.com">{t['contact']} <span aria-hidden="true">↗</span></a></section></main><footer class="site-footer"><span>© Filippo Mantini / Studio</span><div><a href="{prefix}/">{t['footer']}</a><a href="/studio/privacy/">{t['privacy']}</a><a href="#main">↑ Top</a></div></footer></body></html>'''
 dest=R/('public'+path+'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html)
print(json.dumps({'assets':assets,'languages':list(T)},indent=2))
