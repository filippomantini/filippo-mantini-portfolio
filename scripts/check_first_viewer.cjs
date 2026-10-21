const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
(async()=>{
 const html=fs.readFileSync('public/it/work/first-things-first/index.html','utf8');
 assert(!/prototype-(?:grip|detail|top)|hand-study|workspace\.webp|object\.webp/.test(html),'Reference photos must stay private');
 assert(html.includes('data-first-viewer'));assert(!html.includes('preload="/assets/first/'));
 const model=html.match(/data-model="([^"]+)"/)[1],buf=fs.readFileSync('public'+model);assert.equal(buf.readUInt32LE(0),0x46546c67);assert.equal(buf.readUInt32LE(8),buf.length);const size=buf.readUInt32LE(12),g=JSON.parse(buf.subarray(20,20+size).toString());
 assert(g.extras.classification.includes('interpretative'));assert.equal(g.accessors[0].count,g.accessors[1].count);assert(g.accessors[0].count<65536);assert(g.accessors[3].count%3===0);assert(g.meshes[0].primitives[0].attributes.TEXCOORD_0!==undefined);assert(buf.length<500000);
 const handlers={};let requests=0;
 const button={hidden:false,disabled:false,addEventListener(n,f){handlers[n]=f}},canvas={hidden:true,getContext:()=>null,addEventListener(){}},poster={hidden:false},controls={hidden:true,addEventListener(){}},status={};
 const nodes={'[data-load-model]':button,'canvas':canvas,'[role=status]':status,'img':poster,'[data-model-controls]':controls};const section={dataset:{model},querySelector:s=>nodes[s]};
 vm.runInNewContext(fs.readFileSync('public/assets/first-viewer.js','utf8'),{document:{hidden:false,documentElement:{lang:'it'},querySelector:()=>section,addEventListener(){}},window:{addEventListener(){}},ResizeObserver:class{observe(){}},fetch:async()=>{requests++;return {ok:true,arrayBuffer:async()=>buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength)}},DataView,TextDecoder,Uint8Array,Float32Array,Uint16Array,Math,Error});
 assert.equal(requests,0,'3D asset must not load before user interaction');await handlers.click();assert.equal(requests,1);assert.equal(canvas.hidden,true);assert.equal(poster.hidden,false);assert.equal(button.disabled,false);assert(status.textContent.includes('non disponibile'));
 console.log('FIRST: valid compact GLB, complete geometry attributes, no reference photos, on-demand loading and WebGL fallback passed.');
})();
