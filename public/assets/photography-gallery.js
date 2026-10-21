(() => {
  const gallery = document.querySelector('[data-gallery-category]');
  if (!gallery) return;

  const category = gallery.dataset.galleryCategory;
  const fallback = gallery.innerHTML;
  let items = [];
  let resizeTimer = 0;
  let lastLayoutWidth = window.innerWidth;
  const figureCache = new Map();

  const escapeText = value => String(value || '').replace(/[-_]+/g, ' ').replace(/\.[^.]+$/, '').trim();
  const ratioOf = item => {
    const width = Number(item.width) || 1;
    const height = Number(item.height) || 1;
    return Math.max(.25, Math.min(4, width / height));
  };

  const makeFigure = (item, index) => {
    // Reuse the original image elements between resizes; do not trigger a second decode.
    const cached = figureCache.get(item.path);
    if (cached) {
      cached.dataset.label = String(index + 1).padStart(2, '0');
      return cached;
    }
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
      figureCache.delete(item.path);
      items = items.filter(entry => entry !== item);
      render();
    }, { once: true });
    // Keep full-resolution originals for large displays, use high-quality
    // 1152px previews where the requested display size does not need them.
    const previewWidth = Number(item.previewWidth) || 0;
    const fullWidth = Number(item.width) || 0;
    if (item.previewPath && item.previewPath !== item.path &&
        previewWidth > 0 && fullWidth > previewWidth) {
      img.srcset = `${item.previewPath} ${previewWidth}w, ${item.path} ${fullWidth}w`;
      img.sizes = '(max-width: 800px) 100vw, (max-width: 1100px) 50vw, 30vw';
    }
    if (index === 0) img.fetchPriority = 'high';
    img.src = item.path;

    figure.appendChild(img);
    figureCache.set(item.path, figure);
    return figure;
  };

  const render = () => {
    if (!items.length) return;

    if (window.innerWidth <= 800) {
      const fragment = document.createDocumentFragment();
      items.forEach((item, index) => {
        const row = document.createElement('div');
        row.className = 'gallery-row';
        row.appendChild(makeFigure(item, index));
        fragment.appendChild(row);
      });
      gallery.replaceChildren(fragment);
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

    const fragment = document.createDocumentFragment();

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

      fragment.appendChild(row);
    });
    gallery.replaceChildren(fragment);
  };

  fetch('/assets/photography/manifest.json')
    .then(r => {
      if (!r.ok) throw new Error('manifest unavailable');
      return r.json();
    })
    .then(data => {
      items = data?.categories?.[category] || [];
      if (!items.length) return;
      // The HTML already has two visible photos; preserve these loaded DOM nodes.
      const initialFigures = [...gallery.querySelectorAll('[data-initial-gallery] .shot')];
      initialFigures.forEach((figure, index) => {
        const item = items[index];
        if (item && figure.querySelector('img')) {
          figureCache.set(item.path, figure);
        }
      });
      render();
      window.addEventListener('resize', () => {
        // Mobile address bars often change height without changing the layout width.
        const nextWidth = window.innerWidth;
        if (Math.abs(nextWidth - lastLayoutWidth) < 16) return;
        lastLayoutWidth = nextWidth;
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(render, 170);
      }, { passive: true });
    })
    .catch(() => {
      gallery.innerHTML = fallback;
    });
})();