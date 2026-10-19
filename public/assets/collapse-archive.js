/**
 * COLLAPSE project archive: filter cards by category and reveal the full list.
 * Card navigation is native; unsourced entries use <details> for accessibility.
 */
(() => {
  const archive = document.querySelector(".cp-archive");
  if (!archive) return;

  const cards = [...archive.querySelectorAll(".cp-archive-item")];
  const filters = [...archive.querySelectorAll("[data-filter]")];
  const toggle = archive.querySelector(".cp-more");

  let category = "all";
  let expanded = false;

  function render() {
    const matching = cards.filter(card =>
      category === "all" || card.dataset.category === category
    );

    for (const card of cards) {
      const index = matching.indexOf(card);
      card.hidden = index < 0 || (!expanded && index >= 8);
    }

    for (const button of filters) {
      const active = button.dataset.filter === category;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }

    toggle.hidden = matching.length <= 8;
    toggle.textContent =
      (expanded ? toggle.dataset.expanded : toggle.dataset.collapsed) +
      (expanded ? " ↑" : " ↓");
    toggle.setAttribute("aria-expanded", String(expanded));
  }

  for (const button of filters) {
    button.addEventListener("click", () => {
      category = button.dataset.filter;
      expanded = false;
      render();
    });
  }

  toggle.addEventListener("click", () => {
    expanded = !expanded;
    render();
  });

  render();
})();
