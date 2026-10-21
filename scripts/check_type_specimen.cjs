const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const script=fs.readFileSync('public/assets/type-specimen.js','utf8');
async function setup(family,value,load=()=>Promise.resolve([{}])){
 const input={value,addEventListener(n,f){this[n]=f}},size={value:'96',addEventListener(n,f){this[n]=f}},preview={hidden:true,style:{setProperty(n,v){this[n]=v}}},status={};
 const section={getAttribute:()=>family,querySelector:s=>s==='textarea'?input:s==='input[type=range]'?size:s==='[data-type-preview]'?preview:status};
 const document={documentElement:{lang:'it'},querySelectorAll:()=>[section],fonts:{load}};
 vm.runInNewContext(script,{document});await new Promise(r=>setImmediate(r));return {input,size,preview,status};
}
(async()=>{
 let c=await setup('CDCDisplay','Citta di Castello');
 assert.equal(c.preview.textContent,'CITTA DI CASTELLO');assert.equal(c.preview.hidden,false);
 c.input.value='J 2026';c.input.input();assert.equal(c.preview.textContent,'□ □□□□');assert(c.status.textContent.includes('J'));
 c.size.value='150';c.size.input();assert.equal(c.preview.style['--type-size'],'150px');
 let requested;
 let n=await setup('NoFontDisplay','No Font 2026! é €',family=>{requested=family;return Promise.resolve([{}]);});
 assert.equal(requested,'48px NoFontDisplay');assert.equal(n.preview.textContent,'No Font 2026! é €');assert.equal(n.preview.hidden,false);
 n.input.value='città è ó / 😀';n.input.input();assert.equal(n.preview.textContent,'città □ □ □ □');assert(n.status.textContent.includes('è'));
 let failed=await setup('NoFontDisplay','No Font',()=>Promise.reject(new Error('offline')));
 assert.equal(failed.preview.hidden,true);assert(failed.status.textContent.includes('non disponibile'));
 let empty=await setup('CDCDisplay','CDC',()=>Promise.resolve([]));assert.equal(empty.preview.hidden,true);
 console.log('Type specimen: both fonts, case preservation, unsupported glyphs, size and loading failures passed.');
})();
