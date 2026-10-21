const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
(async()=>{
 const input={value:'Citta di Castello',addEventListener(n,f){this[n]=f}},size={value:'96',addEventListener(n,f){this[n]=f}},preview={hidden:true,style:{setProperty(n,v){this[n]=v}}},status={};
 const section={querySelector:s=>s==='textarea'?input:s==='input[type=range]'?size:s==='[data-type-preview]'?preview:status};
 const document={documentElement:{lang:'it'},querySelectorAll:()=>[section],fonts:{load:()=>Promise.resolve([{}])}};
 vm.runInNewContext(fs.readFileSync('public/assets/type-specimen.js','utf8'),{document});await new Promise(r=>setImmediate(r));
 assert.equal(preview.textContent,'CITTA DI CASTELLO');assert.equal(preview.hidden,false);
 input.value='J 2026';input.input();assert.equal(preview.textContent,'□ □□□□');assert(status.textContent.includes('J'));
 size.value='150';size.input();assert.equal(preview.style['--type-size'],'150px');
 console.log('Type specimen: font readiness, uppercase, unsupported glyphs and size control passed.');
})();
