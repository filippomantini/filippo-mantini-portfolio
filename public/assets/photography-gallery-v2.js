(() => {
  const gallery = document.querySelector('[data-gallery-static]');
  if (!gallery) return;
  // Photos are in the HTML: no manifest request and no replacement image nodes.
  const figures = [...gallery.querySelectorAll('.shot')];
  if (!figures.length) return;
  let lastWidth = 0;
  let resizeTimer;

  const layout = () => {
    const styles = getComputedStyle(gallery);
    const available = gallery.clientWidth - parseFloat(styles.paddingLeft || 0) - parseFloat(styles.paddingRight || 0);
    if (!available || Math.abs(available - lastWidth) < 1) return;
    lastWidth = available;
    const mobile = window.innerWidth <= 800;
    const gap = window.innerWidth <= 1100 ? 10 : 14;
    const targetHeight = window.innerWidth <= 1100 ? 260 : 330;
    const rows = [];
    let entries = [], sum = 0;
    for (const figure of figures) {
      const img = figure.querySelector('img');
      const ratio = Math.max(.25, Math.min(4, Number(img.getAttribute('width')) / Number(img.getAttribute('height')) || 1));
      entries.push({ figure, ratio });
      sum += ratio;
      if (mobile || (sum * targetHeight + gap * (entries.length - 1) >= available && entries.length > 1)) {
        rows.push({ entries, sum, last: false });
        entries = []; sum = 0;
      }
    }
    if (entries.length) rows.push({ entries, sum, last: true });
    const fragment = document.createDocumentFragment();
    for (const rowData of rows) {
      const row = document.createElement('div');
      row.className = 'gallery-row';
      const justified = (available - gap * (rowData.entries.length - 1)) / rowData.sum;
      const height = rowData.last && justified > targetHeight * 1.28 ? targetHeight : justified;
      for (const { figure, ratio } of rowData.entries) {
        const width = mobile ? available : Math.max(1, ratio * height);
        figure.style.width = width + 'px';
        figure.style.height = mobile ? 'auto' : height + 'px';
        const img = figure.querySelector('img');
        // Match the real justified column width, including on Retina screens.
        img.sizes = (img.loading === 'lazy' ? 'auto, ' : '') + Math.ceil(width) + 'px';
        row.appendChild(figure);
      }
      fragment.appendChild(row);
    }
    gallery.classList.add('is-laid-out');
    gallery.replaceChildren(fragment);
  };
  layout();
  if ('ResizeObserver' in window) {
    new ResizeObserver(() => { clearTimeout(resizeTimer); resizeTimer = setTimeout(layout, 100); }).observe(gallery);
  } else {
    window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(layout, 100); }, { passive: true });
  }
})();
