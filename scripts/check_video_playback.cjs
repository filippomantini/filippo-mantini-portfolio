const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
function video() {
  return { paused:true, listeners:{}, addEventListener(name, fn){this.listeners[name]=fn},
    pause(){this.paused=true}, play(){this.paused=false;this.listeners.play()} };
}
const clips=[video(),video(),video()];
const docEvents={},winEvents={};let intersection;
const document={querySelectorAll:()=>clips,addEventListener:(n,f)=>docEvents[n]=f,hidden:false};
const window={addEventListener:(n,f)=>winEvents[n]=f,IntersectionObserver:true};
class IntersectionObserver { constructor(fn){intersection=fn} observe(){} }
vm.runInNewContext(fs.readFileSync('public/assets/video-playback.js','utf8'),{document,window,IntersectionObserver});
clips[0].play();clips[1].play();assert(clips[0].paused);assert(!clips[1].paused);
intersection([{target:clips[1],isIntersecting:false}]);assert(clips[1].paused);
clips[0].play();document.fullscreenElement=clips[0];intersection([{target:clips[0],isIntersecting:false}]);assert(!clips[0].paused);document.fullscreenElement=null;
document.hidden=true;docEvents.visibilitychange();assert(clips[0].paused);
clips[2].play();document.pictureInPictureElement=clips[2];docEvents.visibilitychange();assert(!clips[2].paused);
winEvents.pagehide();assert(clips.every(v=>v.paused));
console.log('Video playback: single active player, offscreen, fullscreen, background, PiP and navigation passed.');
