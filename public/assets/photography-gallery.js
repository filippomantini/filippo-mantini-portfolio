(() => {
  const gallery = document.querySelector('[data-gallery-category]');
  if (!gallery) return;

  const category = gallery.dataset.galleryCategory;
  const fallback = gallery.innerHTML;
  let items = [];
  let resizeTimer = 0;

  const escapeText = value => String(value || '').replace(/[-_]+/g, ' ').replace(/\.[^.]+$/, '').trim();
  const ratioOf = item => {
    const width = Number(item.width) || 1;
    const height = Number(item.height) || 1;
    return Math.max(.25, Math.min(4, width / height));
  };

  const makeFigure = (item, index) => {
    const figure = document.createElement('figure');
    figure.className = 'shot';
    figure.dataset.label = String(index + 1).padStart(2, '0');

    const img = document.createElement('img');
    img.alt = escapeText(item.source) || category + ' photography by Filippo Mantini';
    img.loading = index < 2 ? 'eager' : 'lazy';
    img.decoding = 'async';
    if (item.width) img.width = item.width;
    if (item.height) img.height = item.height;
    img.addEventListener('error', () => {
      items = items.filter(entry => entry !== item);
      render();
    }, { once: true });
    img.src = item.path;

    figure.appendChild(img);
    return figure;
  };

  const render = () => {
    if (!items.length) return;

    if (window.innerWidth <= 800) {
      gallery.innerHTML = '';
      items.forEach((item, index) => {
        const row = document.createElement('div');
        row.className = 'gallery-row';
        row.appendChild(makeFigure(item, index));
        gallery.appendChild(row);
      });
      return;
    }

    const gap = window.innerWidth <= 1100 ? 10 : 14;
    const targetHeight = window.innerWidth <= 1100 ? 260 : 330;
    const styles = getComputedStyle(gallery);
    const available = gallery.clientWidth - parseFloat(styles.paddingLeft || 0) - parseFloat(styles.paddingRight || 0);
    const rows = [];
    let current = [];
    let ratioSum = 0;

    items.forEach((item, index) => {
      const ratio = ratioOf(item);
      current.push({ item, index, ratio });
      ratioSum += ratio;

      const projectedWidth = ratioSum * targetHeight + gap * (current.length - 1);
      if (projectedWidth >= available && current.length > 1) {
        rows.push({ entries: current, ratioSum, last: false });
        current = [];
        ratioSum = 0;
      }
    });

    if (current.length) rows.push({ entries: current, ratioSum, last: true });

    gallery.innerHTML = '';

    rows.forEach(rowData => {
      const row = document.createElement('div');
      row.className = 'gallery-row';

      const gapsWidth = gap * (rowData.entries.length - 1);
      const justifiedHeight = Math.max(150, (available - gapsWidth) / rowData.ratioSum);
      const rowHeight = rowData.last && justifiedHeight > targetHeight * 1.28
        ? targetHeight
        : justifiedHeight;

      rowData.entries.forEach(({ item, index, ratio }) => {
        const figure = makeFigure(item, index);
        figure.style.width = Math.max(1, ratio * rowHeight) + 'px';
        figure.style.height = Math.max(1, rowHeight) + 'px';
        row.appendChild(figure);
      });

      gallery.appendChild(row);
    });
  };

  fetch('/assets/photography/manifest.json', { cache: 'no-cache' })
    .then(r => {
      if (!r.ok) throw new Error('manifest unavailable');
      return r.json();
    })
    .then(data => {
      items = data?.categories?.[category] || [];
      if (!items.length) return;
      render();
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(render, 120);
      }, { passive: true });
    })
    .catch(() => {
      gallery.innerHTML = fallback;
    });
})();