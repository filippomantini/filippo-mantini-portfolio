"""Check deployed page/media contracts after generating delivery assets."""
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from urllib.parse import urlsplit
import hashlib
import json
import re

PUBLIC = Path('public')
manifest = json.loads((PUBLIC / 'assets/photography/manifest.json').read_text())
dimensions = {}


def exists(url):
    if url.startswith('/') and not url.startswith('//'):
        path = PUBLIC / urlsplit(url).path.lstrip('/')
        assert path.exists(), f'Missing local resource: {url}'
        return path


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.gallery = None
        self.scripts = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        for name in ('src', 'poster', 'data-src'):
            if attrs.get(name):
                exists(attrs[name])
        if tag == 'link' and attrs.get('rel') in ('stylesheet', 'preload', 'icon'):
            exists(attrs.get('href', ''))
        if 'data-gallery-category' in attrs:
            self.gallery = attrs['data-gallery-category']
            assert 'data-gallery-static' in attrs, 'Gallery still waits for JavaScript/manifest'
        if tag == 'img':
            self.images.append(attrs)
            assert attrs.get('width') and attrs.get('height'), 'Missing intrinsic image dimensions'
            assert attrs.get('loading') in ('eager', 'lazy')
            assert attrs.get('decoding') == 'async'
            for candidate in attrs.get('srcset', '').split(','):
                if not candidate.strip():
                    continue
                url, descriptor = candidate.strip().split()
                path = exists(url)
                if path not in dimensions:
                    with Image.open(path) as image:
                        dimensions[path] = image.width
                assert descriptor == f'{dimensions[path]}w', f'Incorrect responsive width: {url}'
        if tag == 'video':
            assert attrs.get('preload') == 'none', 'Video eagerly requests data'
            assert attrs.get('poster'), 'Video has no static preview'
            assert attrs.get('width') and attrs.get('height'), 'Video has no reserved aspect ratio'
        if tag == 'script' and 'src' in attrs:
            self.scripts.append(attrs['src'])


pages = list(PUBLIC.rglob('*.html'))
galleries = 0
for path in pages:
    html = path.read_text()
    assert 'fonts.googleapis.com' not in html and 'fonts.gstatic.com' not in html, f'External font dependency: {path}'
    page = Page()
    page.feed(html)
    if page.gallery:
        expected = manifest['categories'][page.gallery]
        assert len(page.images) == len(expected), f'Incomplete gallery: {path}'
        assert [image['src'] for image in page.images] == [item['path'] for item in expected], f'Changed photo order: {path}'
        assert sum(image['loading'] == 'eager' for image in page.images) == 2
        assert page.images[0]['fetchpriority'] == 'high'
        assert any('photography-gallery-v2-' in script for script in page.scripts)
        assert not any(re.search(r'photography-gallery-[a-f0-9]{12}\.js', script) for script in page.scripts)
        galleries += 1
    for url in re.findall(r'url\([\"\']?(/assets/[^\)\"\']+)', html):
        exists(url)

for path in (PUBLIC / 'assets/static').glob('*'):
    match = re.search(r'-([a-f0-9]{12})\.(?:css|js)$', path.name)
    assert match and hashlib.sha256(path.read_bytes()).hexdigest()[:12] == match[1], f'Stale fingerprint: {path}'
    if path.suffix == '.js' and path.name.startswith('photography-gallery-v2-'):
        assert 'fetch(' not in path.read_text(), 'Manifest request reintroduced'

assert galleries == 8, f'Expected eight IT/EN galleries; found {galleries}'
for family in ('inter-tight', 'ibm-plex-mono'):
    assert (PUBLIC / f'assets/fonts/{family}-OFL.txt').exists()
    for path in (PUBLIC / 'assets/fonts').glob(f'{family}-*.woff2'):
        cmap = TTFont(path).getBestCmap()
        assert all(ord(char) in cmap for char in 'àèéìòùÀÈÉÌÒÙ'), f'Missing Italian glyph: {path}'

print(json.dumps({'pages_checked': len(pages), 'complete_galleries': galleries,
                  'responsive_images_verified': len(dimensions)}))
