"""Public, static office presentation derived from the app's original scene modules."""
from pathlib import Path
from html import escape as e
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
EN={
'core':('Direction and coordination','Planning, delegation, briefings and priorities'),
'scout':('Research and sources','Research, sources, hypotheses and uncertainties'),
'flare':('Scripts and video production','Scripts, storyboards, filming and editing'),
'flux':('Distribution and growth','SEO, metadata, editorial planning and analysis'),
'prism':('Review and quality','Review, source checking, tests and delivery criteria'),
'pulse':('Web development','Code, interfaces, automation and debugging'),
'aura':('Art direction','Visual identity, design, concepts and visual language'),
'ledger':('Finance and reports','Budgets, reporting, risk analysis and market research'),
'front-desk':('Briefs and clients','Briefs, requests, organisation and draft replies')}

def build_workers(lang):
 it=lang=='it';source=ROOT/'scripts/project-sources'
 agents=json.loads((source/'studio-workers.json').read_text());profiles=json.loads((source/'studio-worker-profiles.json').read_text())
 if not it:
  for id,(role,skills) in EN.items():profiles[id].update(role=role,skills=skills)
 offices=[{'id':id,'name':name} for id,name in [('design','Design & Brand'),('inside-matter','Inside Matter'),('shopify','Shopify Studio'),('gta6','GTA 6 Studio'),('kids','Kids Studio'),('finance','Finance & Markets'),('secretary','Segreteria' if it else 'Email desk')]]
 copy={'profile':'Agente AI / Ruolo' if it else 'AI agent / Role','idle':'Demo / Inattivo' if it else 'Demo / Idle','note':'Nessun incarico in esecuzione e nessun motore AI collegato alla pagina.' if it else 'No task is running and no AI engine is connected to this page.','area':'Area dello Studio' if it else 'Studio area','empty':'Area di lavoro senza un agente assegnato in questa vista.' if it else 'An area without an assigned agent in this view.','fallback':'È disponibile la pianta statica. Ricarica la pagina per riprovare i controlli interattivi.' if it else 'The static floor plan is available. Reload the page to retry the interactive controls.'}
 src=ROOT/'public/assets/studio/workers-src';names=['immersive-office.js','office-layouts.js','agent-state.js']
 version=hashlib.sha256(b''.join((src/n).read_bytes() for n in names)).hexdigest()[:12]
 target=ROOT/('public/assets/studio/office-'+version);target.mkdir(parents=True,exist_ok=True)
 for n in names:(target/n).write_bytes((src/n).read_bytes())
 loader=ROOT/'public/assets/studio-workers.js';h=hashlib.sha256(loader.read_bytes()).hexdigest()[:12];js='studio-workers-'+h+'.js';(loader.parent/js).write_bytes(loader.read_bytes())
 svg=(source/'studio-office-default.svg').read_text().replace('role="group"','role="img"').replace('tabindex="0"','').replace('role="button"','')
 office_buttons=''.join(f'<button type="button" data-office="{o["id"]}" aria-pressed="{str(o["id"]=="design").lower()}" disabled>{e(o["name"])}</button>' for o in offices)
 cards=''.join(f'<button type="button" class="worker-card" data-worker-agent="{a["id"]}" aria-pressed="{str(a["id"]=="aura").lower()}" disabled><span class="worker-orb" style="--orb:{profiles[a["id"]]["color"]}" aria-hidden="true"></span><strong>{e(a["name"])}</strong><small>{e(profiles[a["id"]]["role"])}</small></button>' for a in agents)
 p=profiles['aura'];data=json.dumps({'agents':agents,'profiles':profiles,'offices':offices,'copy':copy},ensure_ascii=False).replace('</','<\\/')
 markup=f'''<section class="workers-section" id="workers" data-studio-workers data-scene="/assets/studio/office-{version}/immersive-office.js" data-layouts="/assets/studio/office-{version}/office-layouts.js" aria-labelledby="workers-title"><span class="label">{'Studio / Uffici e agenti AI' if it else 'Studio / Offices and AI agents'}</span><div class="workers-heading"><h2 id="workers-title">{'Dentro lo Studio.<br>Chi fa cosa.' if it else 'Inside the Studio.<br>Who does what.'}</h2><p>{'I lavoratori dello Studio sono agenti software con ruoli distinti. Le postazioni rendono visibili le competenze e gli ambiti di lavoro; la stessa identità può partecipare a più uffici.' if it else 'The Studio’s workers are software agents with distinct roles. Workstations make their skills and areas visible; the same identity can participate in several offices.'}</p></div><div class="workers-offices" role="group" aria-label="{'Scegli un ufficio' if it else 'Choose an office'}">{office_buttons}</div><div class="workers-office-title"><h3 data-office-title>Design &amp; Brand</h3><span class="label">{'7 uffici / 9 agenti / Dati dimostrativi' if it else '7 offices / 9 agents / Sample data'}</span></div><p class="workers-scroll-hint">{'Scorri la pianta in orizzontale per esplorare le postazioni. Puoi selezionare gli agenti anche nelle schede sotto.' if it else 'Scroll the floor plan horizontally to explore the workstations. You can also select agents in the cards below.'}</p><div class="workers-layout"><div class="workers-floor" data-workers-floor lang="it">{svg}</div><div class="worker-inspector" data-worker-inspector aria-live="polite" aria-atomic="true"><span class="label">{copy['profile']}</span><h3>Aura</h3><p class="worker-role">{e(p['role'])}</p><p>{e(p['skills'])}</p><div class="worker-state"><i aria-hidden="true"></i>{copy['idle']}</div><p class="worker-note">{copy['note']}</p></div></div><p class="workers-notice" data-workers-notice>{'Pianta originale dell’app / Seleziona un ufficio, una postazione o un agente. Gli stati sono dimostrativi e non rappresentano attività in tempo reale.' if it else 'Original app floor plan / Select an office, workstation or agent. The states are illustrative and do not represent live activity.'}</p><div class="workers-roster" role="group" aria-label="{'Agenti dello Studio' if it else 'Studio agents'}">{cards}</div><script type="application/json">{data}</script></section>'''
 return markup,js
