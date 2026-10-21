const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync('public/assets/eubodio-gallery.js','utf8');
let callback,observed=0,removed=0;
const img={dataset:{src:'/image.webp',srcset:'/small.webp 400w'},removeAttribute(k){delete this.dataset[k.replace('data-','')];}};
const src={dataset:{srcset:'/small.avif 400w'},removeAttribute(){delete this.dataset.srcset;}};
const frame={querySelector:()=>img,querySelectorAll:()=>[src]};
class IO{constructor(fn,opts){callback=fn;assert.equal(opts.rootMargin,'260px 0px');}observe(){observed++;}unobserve(){removed++;}}
vm.runInNewContext(source,{window:{IntersectionObserver:IO},IntersectionObserver:IO,document:{querySelectorAll:()=>[frame]}});
assert.equal(observed,1);assert.equal(img.src,undefined,'Images must not fetch before entering the viewport');
callback([{target:frame,isIntersecting:false}]);assert.equal(img.src,undefined);
callback([{target:frame,isIntersecting:true}]);assert.equal(img.src,'/image.webp');assert.equal(src.srcset,'/small.avif 400w');assert.equal(removed,1);
for(const lang of['','it/']){const html=fs.readFileSync(`public/${lang}work/collapse/collections/eubodio/index.html`,'utf8');assert.equal((html.match(/data-eub-image/g)||[]).length,38);assert(html.includes('<picture data-delivery-picture><source type="image/avif"'));assert(html.includes('calc((100vw - 38px)/2)'));assert(html.includes('<noscript>'));}
console.log('Eubodio: viewport loading, AVIF sources, responsive grid sizing and no-JS fallback verified.');
