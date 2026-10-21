/* Pause hidden decoders. Explicitly grouped silent motion studies may play together. */
(() => {
  const videos = [...document.querySelectorAll('video')];
  if (!videos.length) return;
  const separatePlayer = video => document.fullscreenElement === video ||
    document.pictureInPictureElement === video || video.webkitDisplayingFullscreen;
  const pause = video => { if (!video.paused) video.pause(); };
  videos.forEach(video => {
    video.addEventListener('play', () => videos.forEach(other => {
      const group=video.dataset?.playbackGroup;
      const sharedSilentGroup=group && group===other.dataset?.playbackGroup && video.muted && other.muted;
      if (other !== video && !sharedSilentGroup) pause(other);
    }));
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting && !separatePlayer(entry.target)) pause(entry.target);
    }), { threshold: 0 });
    videos.forEach(video => observer.observe(video));
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) videos.forEach(video => {
      if (document.pictureInPictureElement !== video) pause(video);
    });
  });
  window.addEventListener('pagehide', () => videos.forEach(pause));
})();
