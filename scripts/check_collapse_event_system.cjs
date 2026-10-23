const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const rootDir=path.resolve(__dirname,'..');
class El{constructor(){this.textContent='';this.dataset={};this.attrs={};this.listeners={};this.hidden=false;}addEventListener(k,f){this.listeners[k]=f;}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k];}focus(){}fire(k,e={}){this.listeners[k]?.({preventDefault(){},...e});}}
for(const lang of ['it','en']){
 const els=Object.fromEntries(['input','form','[data-confirm]','[data-reset]','[data-entered]','[data-missing]','[data-result]','#scanner-panel','#guests-panel'].map(k=>[k,new El()]));
 els.input.value='CPV5-BCGR-WJLD';const texts=Object.fromEntries(['b','strong','span'].map(k=>[k,new El()]));els['[data-result]'].querySelector=k=>texts[k];els['[data-result]'].dataset.state='idle';els['[data-entered]'].textContent='1';
 const tabs=[new El(),new El()];tabs.forEach((t,i)=>t.attrs['aria-controls']=i?'guests-panel':'scanner-panel');
 const root={dataset:{},querySelector:k=>els[k],querySelectorAll:k=>k==='[role=tab]'?tabs:[]};
 vm.runInNewContext(fs.readFileSync(path.join(rootDir,'public/assets/collapse-event-system.js'),'utf8'),{document:{documentElement:{lang},querySelector:()=>root}});
 els['[data-confirm]'].fire('click');assert.equal(els['[data-entered]'].textContent,'1','Idle cannot admit');
 els.form.fire('submit');assert.equal(els['[data-result]'].dataset.state,'valid');
 els['[data-confirm]'].fire('click');assert.equal(els['[data-entered]'].textContent,'2');assert.equal(els['[data-missing]'].textContent,'1');
 els.form.fire('submit');assert.equal(els['[data-result]'].dataset.state,'used');els['[data-confirm]'].fire('click');assert.equal(els['[data-entered]'].textContent,'2','No duplicate admission');
 els.input.value='INVALID';els.form.fire('submit');assert.equal(els['[data-result]'].dataset.state,'error');
 els['[data-reset]'].fire('click');assert.equal(els['[data-entered]'].textContent,'1');assert.equal(els['[data-result]'].dataset.state,'idle');
 tabs[0].fire('keydown',{key:'ArrowRight'});assert.equal(tabs[1].attrs['aria-selected'],'true');assert.equal(els['#scanner-panel'].hidden,true);
 const doc=fs.readFileSync(path.join(rootDir,'public',lang==='it'?'it':'','work/collapse-event-system/index.html'),'utf8');assert.equal((doc.match(/<h1>/g)||[]).length,1);assert(doc.includes('29.08.2026'));assert(!/vercel\.app|Mario Rossi|CPV5-Q7H3/.test(doc));
}
console.log('EN/IT: state transitions, duplicate protection, invalid code, reset, keyboard tabs and public markup passed');
