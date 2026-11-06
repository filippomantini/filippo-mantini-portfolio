(()=>{const section=document.querySelector('.collapse-home'),video=section?.querySelector('video'),button=section?.querySelector('.collapse-film-toggle');if(!video||!button)return;const motion=matchMedia('(prefers-reduced-motion: reduce)');let visible=false,paused=motion.matches;
function label(){button.textContent=paused?'Play film':'Pause film';button.setAttribute('aria-label',paused?'Play COLLAPSE campaign film':'Pause COLLAPSE campaign film')}
function update(){if(visible&&!paused&&!document.hidden){video.play().catch(()=>{paused=true;label()})}else video.pause();label()}
button.addEventListener('click',()=>{paused=!paused;update()});
if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;update()},{threshold:.15}).observe(section);else{visible=true;update()}
document.addEventListener('visibilitychange',update);motion.addEventListener('change',()=>{paused=motion.matches;update()});label()})();