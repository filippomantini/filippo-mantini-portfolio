// Exercise the actual gallery script against the real photo dimensions.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const manifest = JSON.parse(fs.readFileSync('public/assets/photography/manifest.json', 'utf8'));
const source = fs.readFileSync('public/assets/photography-gallery-v2.js', 'utf8');
const widths = [360, 390, 768, 800, 801, 900, 1100, 1280, 1440, 1920, 2560];
for (const items of Object.values(manifest.categories)) {
  const figures = items.map((item, index) => {
    const img = { loading: index < 2 ? 'eager' : 'lazy',
      getAttribute: key => ({ width: item.width, height: item.height })[key] };
    return { img, style: {}, querySelector: () => img };
  });
  let resize;
  const makeParent = () => ({ children: [], appendChild(node) { this.children.push(node); } });
  const gallery = { clientWidth: 0, classList: { add() {} }, querySelectorAll: () => figures,
    replaceChildren(fragment) { this.rows = fragment.children; } };
  const window = { innerWidth: 0 };
  const context = { window, document: { querySelector: () => gallery,
      createDocumentFragment: makeParent, createElement: makeParent },
    getComputedStyle: () => ({ paddingLeft: window.innerWidth <= 800 ? '14' : '22',
      paddingRight: window.innerWidth <= 800 ? '14' : '22' }),
    ResizeObserver: class { constructor(callback) { resize = callback; } observe() {} },
    setTimeout: callback => callback(), clearTimeout() {} };
  window.ResizeObserver = context.ResizeObserver;
  for (const [index, width] of widths.entries()) {
    window.innerWidth = width;
    gallery.clientWidth = width;
    if (index === 0) vm.runInNewContext(source, context); else resize();
    const available = width - (width <= 800 ? 28 : 44);
    assert.deepEqual(gallery.rows.flatMap(row => row.children), figures, 'Photos changed identity or order on resize');
    for (const row of gallery.rows) {
      const occupied = row.children.reduce((sum, figure) => sum + parseFloat(figure.style.width), 0)
        + (row.children.length - 1) * (width <= 1100 ? 10 : 14);
      assert.ok(occupied <= available + 1, `Horizontal overflow at ${width}px`);
      if (width <= 800) assert.equal(row.children.length, 1, 'Mobile gallery must keep one photo per row');
      for (const figure of row.children) {
        const requested = Number.parseInt(figure.img.sizes.replace('auto, ', ''), 10);
        assert.equal(requested, Math.ceil(parseFloat(figure.style.width)), 'Responsive request does not match display width');
      }
    }
  }
}
console.log('Gallery layout: four categories, 11 viewport widths, photo identity/order and responsive sizes passed.');
