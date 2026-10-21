/* SS26 assets are activated only after the full user-approved media bundle is deployed. */
(() => {
  const story = document.querySelector("[data-ss26-story]");
  const fallback = document.querySelector(".cc-gallery");
  if (!story || !fallback) return;
  const url = "/assets/collapse/ss26/ready.json";
  fetch(url, { cache: "no-store" })
    .then(response => response.ok ? response.json() : null)
    .then(data => {
      if (data?.collection !== "COLLAPSE_SS26" || data?.version !== 1 || data?.media !== 19) return;
      story.hidden = false;
      fallback.hidden = true;
      const duplicate = document.querySelector(".cc-directions");
      if (duplicate) duplicate.hidden = true;
    })
    .catch(() => { /* Original Instagram gallery remains available. */ });
})();
