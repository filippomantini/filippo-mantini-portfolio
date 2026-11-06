(()=>{'use strict';
const cards=Array.from(document.querySelectorAll('#work .project-link')).filter(c=>c.querySelector('.project-visual img')).slice(0,6);
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let active=new Set(),frame=0,observer;
function render(){
 frame=0;
 if(reduced.matches||document.hidden)return;
 const vh=innerHeight,mobile=innerWidth<=900;
 active.forEach((card)=>{
 const rect=card.getBoundingClientRect();
 const progress=Math.max(-1,Math.min(1,(rect.top+rect.height/2-vh/2)/(vh/2+rect.height/2)));
 const direction=Number(card.dataset.motionDirection);
 card.style.setProperty('--pm-title',(progress*(mobile?9:32)*direction).toFixed(2)+'px');
 card.style.setProperty('--pm-image',(progress*(mobile?7:16)).toFixed(2)+'px');
 });
}
function schedule(){if(!frame)frame=requestAnimationFrame(render)}
function setup(){
 if(observer)observer.disconnect();active.clear();
 cards.forEach((card,i)=>{
 card.removeAttribute('data-project-motion');card.classList.remove('pm-wait','pm-in');
 card.style.removeProperty('--pm-title');card.style.removeProperty('--pm-image');
 });
 if(reduced.matches||!('IntersectionObserver'in window))return;
 observer=new IntersectionObserver(entries=>{
 entries.forEach(entry=>{
 const card=entry.target;
 if(entry.isIntersecting){active.add(card);card.classList.remove('pm-wait');card.classList.add('pm-in')}
 else active.delete(card);
 });schedule();
 },{rootMargin:'60px 0px',threshold:0});
 cards.forEach((card,i)=>{
 card.dataset.projectMotion='';card.dataset.motionDirection=i%2?'1':'-1';
 if(card.getBoundingClientRect().top>innerHeight)card.classList.add('pm-wait');
 observer.observe(card);
 });schedule();
}
addEventListener('scroll',schedule,{passive:true});
addEventListener('resize',schedule,{passive:true});
addEventListener('pageshow',schedule);
document.addEventListener('visibilitychange',schedule);
if(reduced.addEventListener)reduced.addEventListener('change',setup);
setup();
})();