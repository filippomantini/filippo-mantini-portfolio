/* FIRST Things First: load the real photographic GLB only after explicit interaction. */
(() => {
  "use strict";
  const stage = document.querySelector("[data-first-viewer]");
  if (!stage) return;
  const start = stage.querySelector("[data-load-model]");
  const poster = stage.querySelector("img");
  const oldCanvas = stage.querySelector("canvas");
  const controls = stage.querySelector("[data-model-controls]");
  const status = stage.querySelector('[role="status"]');
  const it = document.documentElement.lang === "it";
  const tr = (a,b) => it ? a : b;
  let viewer = null, busy = false;
  const initialOrbit = "35deg 78deg auto";
  const fail = error => {
    console.error("FIRST 3D:", error);
    if (viewer) viewer.remove();
    viewer = null;
    busy = false;
    poster.hidden = false;
    start.hidden = false;
    start.disabled = false;
    controls.hidden = true;
    status.textContent = tr("Impossibile caricare il modello 3D. Le fotografie restano disponibili.",
      "Unable to load the 3D model. The photographs remain available.");
  };
  start.addEventListener("click", async () => {
    if (busy || viewer) return;
    busy = true;
    start.disabled = true;
    status.textContent = tr("Preparazione del modello 3D…", "Preparing the 3D model…");
    try {
      await import("https://cdn.jsdelivr.net/npm/@google/model-viewer@4.3.1/dist/model-viewer.min.js");
      await customElements.whenDefined("model-viewer");
      viewer = document.createElement("model-viewer");
      viewer.setAttribute("aria-label", tr("Scansione tridimensionale dell'oggetto FIRST", "3D scan of the FIRST object"));
      viewer.setAttribute("camera-controls", "");
      viewer.setAttribute("camera-orbit", initialOrbit);
      viewer.setAttribute("interaction-prompt", "none");
      viewer.setAttribute("shadow-intensity", "0.45");
      viewer.setAttribute("exposure", "1.15");
      viewer.setAttribute("touch-action", "pan-y");
      viewer.setAttribute("poster", poster.currentSrc || poster.src);
      viewer.setAttribute("reveal", "auto");
      viewer.style.cssText = "display:block;width:100%;height:clamp(410px,54vw,760px);background:#eeebe5;--poster-color:#eeebe5;touch-action:pan-y;";
      viewer.addEventListener("load", () => {
        busy = false;
        controls.hidden = false;
        status.textContent = tr("Scansione caricata. Trascina per ruotare, usa due dita per ingrandire.",
          "Scan loaded. Drag to rotate, pinch to zoom.");
      }, {once:true});
      viewer.addEventListener("error", e => fail(e), {once:true});
      oldCanvas.before(viewer);
      viewer.src = stage.dataset.model;
      poster.hidden = true;
      start.hidden = true;
      status.textContent = tr("Caricamento della scansione 3D…", "Loading the 3D scan…");
    } catch (error) { fail(error); }
  });
  controls.addEventListener("click", event => {
    const button = event.target.closest("button[data-action]");
    if (!button || !viewer) return;
    const action = button.dataset.action;
    if (action === "reset") {
      viewer.cameraOrbit = initialOrbit;
      viewer.jumpCameraToGoal();
      return;
    }
    const orbit = viewer.getCameraOrbit();
    if (!orbit) return;
    let {theta, phi, radius} = orbit;
    if (action === "left") theta -= 0.25;
    if (action === "right") theta += 0.25;
    if (action === "up") phi = Math.max(0.1, phi-0.2);
    if (action === "down") phi = Math.min(Math.PI-0.1, phi+0.2);
    if (action === "in") radius *= 0.85;
    if (action === "out") radius *= 1.18;
    viewer.cameraOrbit = theta + "rad " + phi + "rad " + radius + "m";
  });
})();