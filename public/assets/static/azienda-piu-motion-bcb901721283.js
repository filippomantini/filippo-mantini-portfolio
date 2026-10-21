/* Muted motion studies can play together; decode only while visible. */
(() => {
  const videos=[...document.querySelectorAll('.motion-video')];
  if(!videos.length)return;
  const visible=new WeakMap();
  function prepare(video){
    let changed=false;
    video.querySelectorAll('source[data-src]').forEach(source=>{
      source.src=source.dataset.src;
      source.removeAttribute('data-src');
      changed=true;
    });
    if(changed)video.load();
  }
  function playVisible(video){
    if(!visible.get(video)||document.hidden)return;
    video.muted=true;
    const attempt=video.play();
    if(attempt?.catch)attempt.catch(()=>{video.controls=true;});
  }
  videos.forEach(video=>{
    video.muted=true;
    video.defaultMuted=true;
    video.loop=true;
    video.playsInline=true;
    video.addEventListener('canplay',()=>playVisible(video));
  });
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      const video=entry.target,onScreen=entry.isIntersecting&&entry.intersectionRatio>=.1;
      visible.set(video,onScreen);
      if(onScreen){prepare(video);playVisible(video);}else video.pause();
    }),{rootMargin:'0px',threshold:[0,.1,.5]});
    videos.forEach(video=>observer.observe(video));
  }else{
    videos.forEach(video=>{visible.set(video,true);prepare(video);playVisible(video);});
  }
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden)videos.forEach(video=>video.pause());
    else videos.forEach(playVisible);
  });
  window.addEventListener('pagehide',()=>videos.forEach(video=>video.pause()));
  window.addEventListener('pageshow',()=>videos.forEach(playVisible));
})();
