(() => {
  const gallery = document.querySelector('[data-gallery-category]');
  if (!gallery) return;

  const category = gallery.dataset.galleryCategory;
  const fallback = gallery.innerHTML;

  const escapeText = value => String(value || '').replace(/[-_]+/g, ' ').replace(/\.[^.]+$/, '').trim();

  fetch('/assets/photography/manifest.json', { cache: 'no-cache' })
    .then(r => {
      if (!r.ok) throw new Error('manifest unavailable');
      return r.json();
    })
    .then(data => {
      const items = data?.categories?.[category] || [];
      if (!items.length) return;

      gallery.innerHTML = '';
      const relabel = () => {
        [...gallery.children].forEach((figure, index) => {
          figure.dataset.label = String(index + 1).padStart(2, '0');
        });
      };

      items.forEach((item, index) => {
        const figure = document.createElement('figure');
        figure.className = 'shot' + ((index === 2 || index === 7) ? ' tall' : '');
        figure.dataset.label = String(index + 1).padStart(2, '0');

        const img = document.createElement('img');
        img.alt = escapeText(item.source) || category + ' photography by Filippo Mantini';
        img.addEventListener('error', () => {
          figure.remove();
          relabel();
        }, { once: true });
        img.src = item.path;
        img.loading = index < 2 ? 'eager' : 'lazy';
        img.decoding = 'async';
        if (item.width) img.width = item.width;
        if (item.height) img.height = item.height;

        figure.appendChild(img);
        gallery.appendChild(figure);
      });
    })
    .catch(() => {
      gallery.innerHTML = fallback;
    });
})();
