/* Public, local-only presentation. No operational URLs, camera, network or storage. */
(()=>{'use strict';
 const root=document.querySelector('[data-event-demo]');if(!root)return;
 const code='CPV5-BCGR-WJLD',lang=document.documentElement.lang==='it'?'it':'en';
 const copy={it:{idle:['INVITO DI ESEMPIO','Filippo Mantini','Controlla il codice per esplorare il percorso.'],valid:['BIGLIETTO VALIDO','Filippo Mantini','VIP · '+code],used:['GIÀ UTILIZZATO','Filippo Mantini','Ingresso registrato nella demo.'],error:['CODICE NON RICONOSCIUTO','Usa l’invito di esempio','Questa presentazione riconosce solo il codice mostrato.']},en:{idle:['SAMPLE INVITATION','Filippo Mantini','Check the code to explore the admission flow.'],valid:['VALID TICKET','Filippo Mantini','VIP · '+code],used:['ALREADY USED','Filippo Mantini','Entry recorded in this demo.'],error:['CODE NOT RECOGNISED','Use the sample invitation','This presentation only recognises the displayed code.']}}[lang];
 const result=root.querySelector('[data-result]'),input=root.querySelector('input'),confirm=root.querySelector('[data-confirm]');let admitted=false;
 function show(state){result.dataset.state=state;const t=copy[state];result.querySelector('b').textContent=t[0];result.querySelector('strong').textContent=t[1];result.querySelector('span').textContent=t[2];confirm.hidden=state!=='valid';}
 root.querySelector('form').addEventListener('submit',e=>{e.preventDefault();show(input.value.trim().toUpperCase()===code?(admitted?'used':'valid'):'error');});
 confirm.addEventListener('click',()=>{if(admitted||result.dataset.state!=='valid')return;admitted=true;root.querySelector('[data-entered]').textContent='2';root.querySelector('[data-missing]').textContent='1';show('used');});
 root.querySelector('[data-reset]').addEventListener('click',()=>{admitted=false;input.value=code;root.querySelector('[data-entered]').textContent='1';root.querySelector('[data-missing]').textContent='2';show('idle');});
 const tabs=[...root.querySelectorAll('[role=tab]')];function select(tab){for(const t of tabs){const selected=t===tab;t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1;root.querySelector('#'+t.getAttribute('aria-controls')).hidden=!selected;}}
 for(const [index,tab]of tabs.entries()){tab.addEventListener('click',()=>select(tab));tab.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(index+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;select(tabs[next]);tabs[next].focus();});}
 for(const e of root.querySelectorAll('[data-demo-control]'))e.disabled=false;root.dataset.ready='true';
})();
