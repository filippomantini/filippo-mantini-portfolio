/* Validate the authentic photogrammetry asset and its on-demand case-study integration. */
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const modelPath = '/assets/first/FIRST_THINGS_FIRST_SCANSIONE_LISCIA_V2.glb';
const viewerPath = '/assets/first-scan-viewer.js';

const js = fs.readFileSync('public' + viewerPath, 'utf8');
assert(js.includes('start.addEventListener("click"'), '3D loading must start on click');
assert(js.includes('await import('), '3D renderer must be loaded on demand');
assert(js.includes('model-viewer'), 'Real glTF renderer required');
assert(!js.includes('first-sculpt-handformed-v3.glb'), 'Do not restore the interpretative model');

for (const lang of ['it/', '']) {
  const html = fs.readFileSync('public/' + lang + 'work/first-things-first/index.html', 'utf8');
  assert(html.includes('data-model="' + modelPath + '"'), lang + ': authentic GLB is not linked');
  assert(/src="[^"]*first-scan-viewer[^\"]*"/.test(html), lang + ': lazy viewer missing');
  assert(html.includes('data-load-model'), lang + ': user activation missing');
  assert(html.includes('data-model-controls'), lang + ': accessible controls missing');
  assert(html.includes('reference-01-849a2faf4c07.webp'), lang + ': fallback poster missing');
  assert(!html.includes('data-model="/assets/first/first-sculpt-handformed-v3.glb"'), lang + ': outdated model');
}
const buf = fs.readFileSync('public' + modelPath);
assert.equal(buf.readUInt32LE(0), 0x46546c67, 'Invalid GLB magic');
assert.equal(buf.readUInt32LE(4), 2, 'GLB must be version 2');
assert.equal(buf.readUInt32LE(8), buf.length, 'Bad GLB length');
const jsonSize = buf.readUInt32LE(12);
const gltf = JSON.parse(buf.subarray(20,20+jsonSize).toString('utf8'));
assert(gltf.meshes.length>=2, 'Scan should contain original sculpture and complete underside');
assert(gltf.images.length>=2, 'Embedded photo textures must be preserved');
assert(!gltf.materials.some(m=>m.normalTexture), 'Old harsh normal map must be removed');
assert(gltf.meshes.some(m=>m.primitives.some(p => gltf.accessors[p.indices].componentType===5125)), '32-bit indices must remain intact');
assert(buf.length < 15000000, 'Use the web-optimized scan, not the 4K master');
console.log('FIRST scan verified: authentic GLB, materials, IT/EN, click-to-load, and photo fallback.');
