const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const player=fs.readFileSync('public/assets/azienda-piu-motion.js','utf8');
const coordinator=fs.readFileSync('public/assets/video-playback.js','utf8');
function video(group='azienda-motion'){
 return {dataset:group?{playbackGroup:group}:{},paused:true,muted:true,listeners:{},sources:[{dataset:{src:'/mobile.mp4'},removeAttribute(){delete this.dataset.src;}},{dataset:{src:'/desktop.mp4'},removeAttribute(){delete this.dataset.src;}}],loads:0,
 addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);},querySelectorAll(){return this.sources.filter(s=>s.dataset.src);},load(){this.loads++;},pause(){this.paused=true;},play(){this.paused=false;for(const f of this.listeners.play??[])f();return Promise.resolve();}};
}
const motion=[video(),video(),video()],hero=video(null),all=[hero,...motion],docEvents={},winEvents={},observers=[];
const document={hidden:false,querySelectorAll:s=>s==='.motion-video'?motion:all,addEventListener:(n,f)=>(docEvents[n]??=[]).push(f)};
const window={IntersectionObserver:true,addEventListener:(n,f)=>(winEvents[n]??=[]).push(f)};
class IntersectionObserver{constructor(fn,options){this.fn=fn;this.options=options;observers.push(this);}observe(){}}
const env={document,window,IntersectionObserver,WeakMap};
// This is the production order, including the script automatically re-added by CI.
vm.runInNewContext(player,env);vm.runInNewContext(coordinator,env);
assert(all.every(v=>v.paused));assert(motion.every(v=>!v.loads),'No movie downloads before visibility');
observers[0].fn(motion.map(target=>({target,isIntersecting:true,intersectionRatio:.5})));
assert(motion.every(v=>!v.paused),'All three visible motion studies must play simultaneously');assert(motion.every(v=>v.loop&&v.muted&&v.playsInline));assert(motion.every(v=>v.loads===1&&v.sources.every(s=>s.src)));
observers[0].fn([{target:motion[0],isIntersecting:false,intersectionRatio:0}]);assert(motion[0].paused);assert(!motion[1].paused&&!motion[2].paused);
document.hidden=true;for(const f of docEvents.visibilitychange)f();assert(all.every(v=>v.paused));document.hidden=false;for(const f of docEvents.visibilitychange)f();assert(motion[0].paused);assert(!motion[1].paused&&!motion[2].paused);
hero.play();assert(motion.every(v=>v.paused),'Unrelated videos keep exclusive playback');
for(const f of winEvents.pagehide)f();assert(all.every(v=>v.paused));
for(const lang of['it/','']){
 const html=fs.readFileSync(`public/${lang}work/azienda-piu/index.html`,'utf8');const clips=[...html.matchAll(/<video\b[^>]*class="motion-video"[^>]*>[\s\S]*?<\/video>/g)].map(m=>m[0]);assert.equal(clips.length,3);
 for(const c of clips){assert(c.includes('data-playback-group="azienda-motion"'));assert(c.includes('muted loop playsinline controls preload="none"'));assert(!c.includes(' autoplay'));assert(!c.includes('data-src'));assert(c.includes('media="(max-width:800px)"'));assert.equal((c.match(/<source /g)||[]).length,2);}
 const schema=JSON.parse(html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s)[1]);assert.equal(schema.hasPart.length,3);for(const v of schema.hasPart){assert.equal(v['@type'],'VideoObject');assert(v.thumbnailUrl&&v.contentUrl&&v.uploadDate&&v.duration);}
 assert.equal((html.match(/<h1\b/g)||[]).length,1);assert(html.includes(`rel="canonical" href="https://filippomantini.com/${lang}work/azienda-piu/"`));
}
console.log('Azienda Più: 3 simultaneous visible loops, responsive sources, offscreen/background pause, exclusive hero and SEO metadata passed.');
