/* Exercise public presentation navigation/theme without requiring the private app. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const rootPath=require('node:path').resolve(__dirname,'..');
for(const prefix of ['/it','']){
 const html=fs.readFileSync(rootPath+'/public'+prefix+'/work/filippo-mantini-studio/index.html','utf8');
 assert.equal((html.match(/<h1[ >]/g)||[]).length,1);
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size);
 for(const m of html.matchAll(/href="#([^"]+)"/g))assert.ok(ids.includes(m[1]),'Missing anchor '+m[1]);
 assert.ok(html.includes('href="https://filippomantini.com'+prefix+'/work/filippo-mantini-studio/"'));
 assert.match(html,/<div class="swatches" role="img" aria-label=/,'Named palette must expose an accessible role');
 assert.ok(html.includes('/studio/privacy/'));assert.ok(html.includes('hreflang="en"'));assert.ok(html.includes('hreflang="it"'));
 for(const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g))assert.equal(JSON.parse(m[1])['@type'],'CreativeWork');
 assert.doesNotMatch(html,/<iframe|<video|<canvas|onload=|onclick=/i);
 const css=html.match(/href="(\/assets\/(?:static\/)?studio-project-[^"]+\.css)"/)[1];const js=html.match(/src="(\/assets\/(?:static\/)?studio-project-[^"]+\.js)"/)[1];assert.ok(fs.existsSync(rootPath+'/public'+css));assert.ok(fs.existsSync(rootPath+'/public'+js));
 const create=id=>({id,hidden:false,dataset:{screen:id},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},addEventListener(k,v){this.events[k]=v}});
 const panels=['studio-today','studio-mail','studio-video'].map(create);const links=panels.map(p=>create(p.id));
 const theme=create('theme');theme.hidden=true;theme.dataset={dark:'Dark',light:'Light'};
 const root={dataset:{},querySelector:s=>s==='.demo-nav'?{querySelectorAll:()=>links}:theme,querySelectorAll:()=>panels};
 const ctx={document:{querySelector:()=>root}};vm.runInNewContext(fs.readFileSync(rootPath+'/public'+js,'utf8'),ctx);
 assert.deepEqual(panels.map(p=>p.hidden),[false,true,true]);assert.equal(links[0].attrs['aria-current'],'true');assert.equal(theme.hidden,false);
 links[1].events.click({preventDefault(){}});assert.deepEqual(panels.map(p=>p.hidden),[true,false,true]);assert.equal(links[1].attrs['aria-current'],'true');assert.equal(links[0].attrs['aria-current'],undefined);
 links[2].events.click({preventDefault(){}});assert.deepEqual(panels.map(p=>p.hidden),[true,true,false]);
 theme.events.click();assert.equal(root.dataset.theme,'dark');assert.equal(theme.attrs['aria-pressed'],'true');assert.equal(theme.textContent,'Light');
 theme.events.click();assert.equal(root.dataset.theme,'light');assert.equal(theme.attrs['aria-pressed'],'false');
 links[0].events.click({preventDefault(){}});assert.deepEqual(panels.map(p=>p.hidden),[false,true,true]);
 // No JavaScript: all three anchored views remain available in the original document.
 assert.doesNotMatch(html,/<section class="demo-view"[^>]*\bhidden\b/);
 assert.ok(fs.statSync(rootPath+'/public'+js).size<2500,'Presentation JS budget');
}
console.log('Studio: IT/EN metadata, anchors, no-JS content, three-view navigation and theme passed.');
