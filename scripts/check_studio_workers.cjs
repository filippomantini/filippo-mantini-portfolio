const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const base=path.resolve(__dirname,'..');
(async()=>{
 const layouts=await import('data:text/javascript,'+encodeURIComponent(fs.readFileSync(base+'/public/assets/studio/workers-src/office-layouts.js','utf8')));
 assert.equal(layouts.validateLayouts(),true);
 for(const url of ['/studio/','/work/filippo-mantini-studio/']){
  const html=fs.readFileSync(base+'/public'+url+'index.html','utf8');
  const data=JSON.parse(html.match(/<script type="application\/json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(data.agents.length,9);assert.equal(new Set(data.agents.map(a=>a.id)).size,9);assert.equal(data.offices.length,7);
  assert.ok(html.includes('<header class="topbar">'));assert.ok(html.includes('class="portfolio-footer"'));assert.ok(html.includes('mailto:info@filippomantini.com'));
  assert.equal((html.match(/data-worker-agent=/g)||[]).length,9);assert.equal((html.match(/data-office=/g)||[]).length,7);
  assert.doesNotMatch(html,/data-phase="working"/);assert.ok(html.includes('id="workers"'));assert.ok(html.includes('class="immersive-svg"'));
  const b=(data,extra={})=>({dataset:data,attrs:{},disabled:true,events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.events[k]=v},...extra});
  const people=data.agents.map(a=>b({workerAgent:a.id})),offices=data.offices.map(o=>b({office:o.id}));
  const floor={},inspector={},title={},notice={};let enter,imports=0,latest,destroyed=0;
  const root={dataset:{scene:'/scene',layouts:'/layouts'},querySelector(s){return s==='script[type="application/json"]'?{textContent:JSON.stringify(data)}:s==='[data-workers-floor]'?floor:s==='[data-worker-inspector]'?inspector:s==='[data-office-title]'?title:notice},querySelectorAll(s){return s==='[data-office]'?offices:people}};
  const sceneModule={createOfficeScene(f,args){imports++;latest=args;return {assignments:new Map(args.agents.map(a=>[a.id,layouts.OFFICE_LAYOUTS[args.officeId].zones.find(z=>z.agents.includes(a.id))?.id||layouts.OFFICE_LAYOUTS[args.officeId].zones[0].id])),setSelected(id){f.selected=id},destroy(){destroyed++}}}};
  class IO{constructor(cb){enter=cb}observe(){}disconnect(){}}
  const source=fs.readFileSync(base+'/public/assets/studio-workers.js','utf8').replace('import(root.dataset.scene)','Promise.resolve(sceneModule)').replace('import(root.dataset.layouts)','Promise.resolve(layoutModule)');
  vm.runInNewContext(source,{document:{querySelector:()=>root},window:{IntersectionObserver:true},IntersectionObserver:IO,sceneModule,layoutModule:layouts});
  assert.equal(imports,0,'Office module must wait until the section approaches the viewport');
  enter([{isIntersecting:true}]);await new Promise(r=>setImmediate(r));
  assert.equal(root.dataset.ready,'true');assert.equal(latest.officeId,'design');assert.ok(people.every(x=>!x.disabled));assert.ok(offices.every(x=>!x.disabled));assert.equal(floor.selected,'aura');
  for(const office of offices){office.events.click();assert.equal(latest.officeId,office.dataset.office);assert.ok(latest.agents.every(a=>a.offices.includes(office.dataset.office)));assert.equal(office.attrs['aria-pressed'],'true');}
  for(const person of people){person.events.click();assert.equal(floor.selected,person.dataset.workerAgent);assert.equal(person.attrs['aria-pressed'],'true');assert.equal(people.filter(p=>p.attrs['aria-pressed']==='true').length,1);assert.ok(latest.agents.some(a=>a.id===person.dataset.workerAgent));}
  assert.ok(destroyed>=7,'Previous office listeners must be released');
  assert.doesNotMatch(source,/fetch\(|requestAnimationFrame|setInterval|localStorage/,'Presentation must not contact app services or run a render loop');
 }
 for(const [url,target] of [['/it/','/studio/'],['/','/work/filippo-mantini-studio/']]){const html=fs.readFileSync(base+'/public'+url+'index.html','utf8');const header=html.match(/<header[\s\S]*?<\/header>/)[0];assert.ok(header.includes('href="'+target+'">Studio AI</a>'),'Studio must be available in homepage navigation');}
 console.log('Studio workers: lazy initialization, 7 offices, 9 selectable agents, shared memberships, listener cleanup and homepage navigation passed.');
})().catch(e=>{console.error(e);process.exitCode=1});
