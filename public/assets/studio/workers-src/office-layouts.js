// Original V2.2 floor plans, tools and station assignments. Coordinates: 1200 × 720.
// Shared identities are read from SQLite; these assignments never create agents.
export const AGENT_PROFILES = {
 core:{color:'#1728FF',role:'Direzione e coordinamento',skills:'Pianificazione, delega, briefing e priorità'},
 scout:{color:'#5A8CB8',role:'Ricerca e fonti',skills:'Ricerca, raccolta fonti, ipotesi e incertezze'},
 flare:{color:'#735ED6',role:'Script e produzione video',skills:'Sceneggiature, storyboard, riprese e montaggio'},
 flux:{color:'#398C8A',role:'Distribuzione e crescita',skills:'SEO, metadata, calendario editoriale e analisi'},
 prism:{color:'#64738C',role:'Revisione e qualità',skills:'Revisione, controllo fonti, test e criteri di consegna'},
 pulse:{color:'#3488CF',role:'Sviluppo web',skills:'Codice, interfacce, automazioni e debug'},
 aura:{color:'#AD75A1',role:'Direzione artistica',skills:'Identità visiva, design, concept e linguaggio grafico'},
 ledger:{color:'#7F8D5E',role:'Finanza e report',skills:'Budget, rendicontazione, analisi del rischio e mercati'},
 'front-desk':{color:'#A38262',role:'Brief e clienti',skills:'Raccolta brief, richieste, organizzazione e bozze di risposta'}
};
const z=(id,name,x,y,w,h,tool,agents)=>({id,name,x,y,w,h,tool,agents});
export const OFFICE_LAYOUTS={
 secretary:{subtitle:'La posta diventa lavoro organizzato.',code:'SE / MAIL & OPERATIONS',detail:'Un banco di ingresso per le caselle Gmail, una sala briefing e postazioni per ordini, bozze e revisione. Ogni invio richiede la tua approvazione.',floor:'news',zones:[
  z('inbox','Caselle Gmail',32,80,400,260,'support',['front-desk']),
  z('brief','Briefing quotidiano',474,80,694,230,'meeting',['core']),
  z('orders','Ordini e richieste',32,382,400,258,'products',['flux']),
  z('drafts','Risposte e bozze',474,352,330,288,'books',[]),
  z('approval','Revisione invii',846,352,322,288,'review',['prism'])
 ],hall:[[454,80,0,560]]},
 'inside-matter':{
  subtitle:'Dalle domande alle immagini.',code:'IM / SCIENCE & MEDIA',detail:'Una biblioteca di ricerca, un set con camera e luci, una sala di montaggio. Il percorso segue la produzione di un contenuto.',
  floor:'lab',zones:[
   z('research','Research Lab',32,80,300,560,'science',['scout']),
   z('script','Script Room',364,80,362,235,'storyboard',['core']),
   z('video','Video Production',758,80,410,316,'camera',['flare']),
   z('editing','Editing Room',758,428,410,212,'timeline',['flux']),
   z('quality','Quality Review',364,347,362,293,'review',['prism'])
  ],hall:[[348,80,0,560],[742,80,0,560]]
 },
 shopify:{
  subtitle:'Un atelier per il commercio digitale.',code:'SH / DIGITAL COMMERCE',detail:'Atelier prodotto e laboratorio web affacciati sul corridoio commerciale; torre analytics e banco customer care.',floor:'store',zones:[
   z('product','Product Design',32,80,394,242,'products',['aura']),
   z('development','Web Development',458,80,346,242,'code',['pulse']),
   z('marketing','Marketing & SEO',32,364,394,276,'campaign',['flux']),
   z('care','Customer Care',458,364,346,276,'support',['front-desk','core']),
   z('analytics','Analytics',844,80,324,560,'analytics',['prism'])
  ],hall:[[32,342,792,0]]
 },
 gta6:{
  subtitle:'Una redazione, più punti di vista.',code:'GT / GAMING MEDIA',detail:'Newsroom aperta con tavolo notizie, postazioni console e due cabine di produzione. Rumor e verifiche rimangono distinti.',floor:'news',zones:[
   z('news','Gaming Newsroom',32,80,690,224,'news',['core']),
   z('research','Research & Reviews',764,80,404,224,'gaming',['scout']),
   z('production','Video Production',32,348,304,292,'camera',['flare']),
   z('editing','Editing',376,348,346,292,'timeline',['prism']),
   z('social','Social & Analytics',764,348,404,292,'campaign',['flux'])
  ],hall:[[32,326,1136,0]]
 },
 kids:{
  subtitle:'Storie, personaggi e cura.',code:'KD / ORIGINAL STORIES',detail:'Tavoli di scrittura e character design circondano un palco di animazione centrale. La Safety Review ha uno spazio separato.',floor:'play',zones:[
   z('story','Storytelling',32,80,306,272,'books',['core']),
   z('character','Character Design',32,386,306,254,'character',['aura']),
   z('animation','Animation Studio',378,80,416,560,'animation',['flare']),
   z('editing','Video Editing',834,80,334,272,'timeline',['flux']),
   z('safety','Safety Review',834,386,334,254,'safety',['prism','scout'])
  ],hall:[[358,80,0,560],[814,80,0,560]]
 },
 design:{
  subtitle:'Il pensiero prende forma.',code:'DB / VISUAL SYSTEMS',detail:'Galleria di art direction e banco identità, una lunga sala progetti clienti e cabine web e revisione.',floor:'gallery',zones:[
   z('direction','Art Direction',32,80,362,264,'art',['aura']),
   z('identity','Brand Identity',436,80,350,264,'identity',['flux']),
   z('web','Web Development',828,80,340,264,'code',['pulse']),
   z('clients','Client Projects',32,386,754,254,'meeting',['front-desk','core']),
   z('quality','Quality Review',828,386,340,254,'review',['prism'])
  ],hall:[[32,366,1136,0]]
 },
 finance:{
  subtitle:'Ricerca, metodo, prospettiva.',code:'FN / MARKET INTELLIGENCE',detail:'Un osservatorio mercati in alto, tavolo centrale di analisi e stanze distinte per rischio e reporting. Schermi senza quotazioni inventate.',floor:'finance',zones:[
   z('market','Market Intelligence',32,80,1136,172,'market',['scout']),
   z('research','Equity & ETF Research',32,294,302,346,'library',[]),
   z('portfolio','Portfolio Analysis',376,294,386,346,'portfolio',['ledger']),
   z('risk','Risk Management',804,294,364,150,'risk',['prism']),
   z('report','Financial Reporting',804,486,364,154,'report',['core'])
  ],hall:[[32,272,1136,0]]
 }
};
export function validateLayouts(){
 for(const [id,layout]of Object.entries(OFFICE_LAYOUTS)){
  if(layout.zones.length!==5)throw Error(`${id}: cinque aree richieste`);
  for(const a of layout.zones){if(a.x<0||a.y<0||a.x+a.w>1200||a.y+a.h>720)throw Error(`${id}: area fuori pianta`);
   for(const b of layout.zones){if(a===b)continue;if(a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y)throw Error(`${id}: aree sovrapposte`);}
  }
 }
 return true;
}
