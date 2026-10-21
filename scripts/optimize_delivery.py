"""Build responsive delivery assets without changing any original image or video.

Run after optimize_photography.py. Generated paths include a content fingerprint,
so they can be cached for a year while HTML always revalidates. Re-running is safe.
"""
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from html import escape, unescape
from pathlib import Path
from PIL import Image, ImageOps
from optimize_video import build_video_delivery
from fontTools.ttLib import TTFont
from fontTools import subset
import hashlib
import io
import json
import re
import subprocess
import tempfile
from urllib.parse import urlsplit

PUBLIC = Path('public')
ASSETS = PUBLIC / 'assets'
RESPONSIVE = ASSETS / 'responsive'
STATIC = ASSETS / 'static'
FONTS = ASSETS / 'fonts'
RECIPE = 'delivery-v1-q93'
VIDEO_DELIVERY = {}
for directory in (RESPONSIVE, STATIC, FONTS):
    directory.mkdir(parents=True, exist_ok=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()[:12]


def public_url(path):
    return '/' + path.relative_to(PUBLIC).as_posix()


def local_path(url):
    return PUBLIC / urlsplit(unescape(url)).path.lstrip('/')


def attr(tag, name):
    match = re.search(r'(?<![\w-])' + re.escape(name) + r'\s*=\s*([\"\'])(.*?)\1', tag, re.S)
    return unescape(match[2]) if match else None


def set_attr(tag, name, value):
    pattern = r'(?<![\w-])' + re.escape(name) + r'\s*=\s*([\"\'])(.*?)\1'
    replacement = f'{name}="{escape(str(value), quote=True)}"'
    if re.search(pattern, tag, re.S):
        return re.sub(pattern, lambda _: replacement, tag, count=1, flags=re.S)
    return re.sub(r'\s*/?>$', lambda m: ' ' + replacement + m[0], tag)


@lru_cache(maxsize=None)
def variants(url):
    source = local_path(url)
    # Prefer original photographic pixels to a previously downsampled preview.
    original = Path(str(source).replace('/vib-preview/', '/').replace('/case-preview/', '/'))
    if original.exists():
        source = original
    raw = source.read_bytes()
    fingerprint = digest(raw + RECIPE.encode())
    with Image.open(io.BytesIO(raw)) as opened:
        image = ImageOps.exif_transpose(opened)
        width, height = image.size
        icc = opened.info.get('icc_profile')
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
        candidates = []
        for size in (320, 640, 1152, 1600):
            if size >= width:
                continue
            # 320px only helps the narrow Vibrazioni process strip.
            if size == 320 and not source.name.startswith('vib_'):
                continue
            dest = RESPONSIVE / f'{source.stem}-{fingerprint}-{size}.webp'
            if not dest.exists() or dest.stat().st_size == 0:
                thumb = image.copy()
                thumb.thumbnail((size, 100000), Image.Resampling.LANCZOS)
                encoded = io.BytesIO()
                thumb.save(encoded, 'WEBP', quality=93, method=6,
                           **({'icc_profile': icc} if icc else {}))
                # Publish a complete image, and recover interrupted empty cache files.
                temporary = dest.with_suffix('.tmp.webp')
                temporary.write_bytes(encoded.getvalue())
                temporary.replace(dest)
            if dest.stat().st_size < len(raw) * .9:
                candidates.append((size, public_url(dest)))
            else:
                dest.unlink(missing_ok=True)
        # Full-size pixels are the exact original bytes, never re-encoded.
        candidates.append((width, public_url(source)))
        return {'width': width, 'height': height, 'candidates': candidates,
                'source': public_url(source)}


def srcset(info):
    return ', '.join(f'{path} {width}w' for width, path in info['candidates'])


def responsive_img(tag, sizes, priority=None):
    url = attr(tag, 'src')
    if not url or not url.startswith('/assets/') or local_path(url).suffix.lower() not in ('.webp', '.jpg', '.jpeg', '.png'):
        return tag
    info = variants(urlsplit(url).path)
    tag = set_attr(tag, 'width', info['width'])
    tag = set_attr(tag, 'height', info['height'])
    tag = set_attr(tag, 'src', info['source'])
    tag = set_attr(tag, 'decoding', 'async')
    tag = set_attr(tag, 'srcset', srcset(info))
    tag = set_attr(tag, 'sizes', sizes)
    if priority:
        tag = set_attr(tag, 'loading', 'eager')
        tag = set_attr(tag, 'fetchpriority', 'high')
    elif not attr(tag, 'loading'):
        tag = set_attr(tag, 'loading', 'lazy')
    return tag


FONT_SOURCES = [
    ('IBM Plex Mono', 400, 'https://fonts.gstatic.com/s/ibmplexmono/v20/-F63fjptAgt5VM-kVkqdyU8n5ig.ttf'),
    ('IBM Plex Mono', 500, 'https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJ8lc.ttf'),
    ('Inter Tight', 400, 'https://fonts.gstatic.com/s/intertight/v9/NGSnv5HMAFg6IuGlBNMjxJEL2VmU3NS7Z2mjDw-qXA.ttf'),
    ('Inter Tight', 500, 'https://fonts.gstatic.com/s/intertight/v9/NGSnv5HMAFg6IuGlBNMjxJEL2VmU3NS7Z2mjPQ-qXA.ttf'),
    ('Inter Tight', 600, 'https://fonts.gstatic.com/s/intertight/v9/NGSnv5HMAFg6IuGlBNMjxJEL2VmU3NS7Z2mj0QiqXA.ttf'),
    ('Inter Tight', 700, 'https://fonts.gstatic.com/s/intertight/v9/NGSnv5HMAFg6IuGlBNMjxJEL2VmU3NS7Z2mj6AiqXA.ttf'),
]


def download(url, dest):
    subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                    '--retry', '2', '--max-time', '45', url, '-o', str(dest)], check=True)


def build_font(entry):
    family, weight, url = entry
    stem = family.lower().replace(' ', '-') + f'-{weight}-{digest(url.encode() + b"latin-v1")}'
    dest = FONTS / f'{stem}.woff2'
    if not dest.exists():
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory) / 'font.ttf'
            complete = FONTS / (family.lower().replace(' ', '-') + f'-{weight}-{digest(url.encode())}.woff2')
            if complete.exists():
                font = TTFont(complete)
            else:
                download(url, original)
                font = TTFont(original)
            # Same outlines and shaping; omit scripts unused by this IT/EN site.
            options = subset.Options()
            options.layout_features = ['*']
            subsetter = subset.Subsetter(options=options)
            ranges = [(0, 0x24f), (0x1e00, 0x1eff), (0x2000, 0x206f),
                      (0x20a0, 0x20cf), (0x2190, 0x22ff), (0xfeff, 0xfeff), (0xfffd, 0xfffd)]
            subsetter.populate(unicodes=[n for low, high in ranges for n in range(low, high + 1)])
            subsetter.subset(font)
            font.flavor = 'woff2'
            font.save(dest)
    return f'@font-face{{font-family:"{family}";font-style:normal;font-weight:{weight};font-display:swap;src:url("{public_url(dest)}") format("woff2")}}'


def build_fonts():
    with ThreadPoolExecutor(max_workers=4) as pool:
        faces = list(pool.map(build_font, FONT_SOURCES))
    for name, url in (
        ('inter-tight', 'https://raw.githubusercontent.com/google/fonts/main/ofl/intertight/OFL.txt'),
        ('ibm-plex-mono', 'https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt'),
    ):
        dest = FONTS / f'{name}-OFL.txt'
        if not dest.exists():
            download(url, dest)
    preloads = ''.join(f'<link rel="preload" as="font" href="{public_url(FONTS / (family.lower().replace(" ", "-") + "-400-" + digest(url.encode() + b"latin-v1") + ".woff2"))}" type="font/woff2" crossorigin>'
                       for family, weight, url in FONT_SOURCES if weight == 400)
    return preloads + '<style data-local-fonts>' + ''.join(faces) + '</style>'


@lru_cache(maxsize=None)
def video_info(url):
    source = local_path(url)
    data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'json', str(source)]))['streams'][0]
    return data['width'], data['height']


@lru_cache(maxsize=None)
def video_poster(url):
    source = local_path(url)
    key = digest(source.read_bytes() + b'poster-v1')
    dest = RESPONSIVE / f'{source.stem}-{key}-poster.webp'
    if not dest.exists():
        frame = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', '9' if 'vibrazioni' in source.name else '0',
            '-i', str(source), '-frames:v', '1', '-vf', 'scale=720:-1', '-f', 'image2pipe', '-vcodec', 'png', '-threads', '1', '-'])
        with Image.open(io.BytesIO(frame)) as im:
            im.save(dest, 'WEBP', quality=90, method=6)
    return public_url(dest)


def improve_video(match):
    block = match[0]
    opening = re.match(r'<video\b[^>]*>', block)[0]
    source = re.search(r'<source\b[^>]*>', block)
    url = (attr(source[0], 'src') or attr(source[0], 'data-src')) if source else attr(opening, 'src')
    if not url or not url.startswith('/assets/') or not local_path(url).exists():
        return block
    # Multiple media-query sources carry responsive encodes and original display ratio.
    # They already have a verified poster; do not rewrite dimensions from one rendition.
    if 'data-playback-group="azienda-motion"' in opening:
        return block
    url = urlsplit(url).path
    delivered = VIDEO_DELIVERY.get(url, url)
    if delivered != url:
        block = block.replace(url, delivered)
    url = delivered
    if 'vibrazioni-process' in url:
        if not re.search(r'\bmuted(?:\s|[=>])', opening):
            opening = opening[:-1] + ' muted>'
    width, height = video_info(url)
    opening = set_attr(set_attr(opening, 'width', width), 'height', height)
    opening = set_attr(opening, 'preload', 'none')
    if not attr(opening, 'poster'):
        opening = set_attr(opening, 'poster', video_poster(url))
    return re.sub(r'^<video\b[^>]*>', lambda _: opening, block)


def static_gallery(html, manifest):
    category = re.search(r'data-gallery-category="([a-z]+)"', html)[1]
    figures = []
    for index, item in enumerate(manifest['categories'][category]):
        info = variants(item['path'])
        label = f'{index + 1:02d}'
        alt = f'{category.upper()} photography by Filippo Mantini — {label}'
        loading = 'eager' if index < 2 else 'lazy'
        sizes = '(max-width:800px) calc(100vw - 28px), (max-width:1100px) calc(50vw - 27px), 30vw'
        if loading == 'lazy':
            sizes = 'auto, ' + sizes
        image = (f'<img src="{info["source"]}" srcset="{srcset(info)}" sizes="{sizes}" '
                 f'width="{info["width"]}" height="{info["height"]}" alt="{escape(alt, quote=True)}" '
                 f'loading="{loading}" decoding="async"' + (' fetchpriority="high"' if index == 0 else '') + '>')
        figures.append(f'<figure class="shot" data-label="{label}" style="--photo-ratio:{info["width"]}/{info["height"]}">{image}</figure>')
    section = f'<section class="gallery" data-gallery-category="{category}" data-gallery-static aria-label="{category.upper()} photography gallery">' + ''.join(figures) + '</section>'
    html = re.sub(r'<section\b[^>]*data-gallery-category[^>]*>[\s\S]*?</section>', lambda _: section, html)
    # Remove the legacy fetch/rebuild script, including a previously fingerprinted copy.
    html = re.sub(r'<script\b[^>]*src="/assets/(?:static/)?photography-gallery(?:-[a-f0-9]{12})?\.js[^\"]*"[^>]*></script>', '', html)
    if 'photography-gallery-v2' not in html:
        html = html.replace('</body>', '<script src="/assets/photography-gallery-v2.js" defer></script></body>')
    if 'photography-static' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/photography-static.css"></head>')
    return html


def image_sizes(page, url):
    path = urlsplit(url).path
    if '/collapse/eubodio/' in path:
        if any(name in path for name in ('/urban-', '/garment-')):
            return '(max-width:800px) calc((100vw - 38px)/2), calc((100vw - 80px)/3)'
        if '/campaign-01' not in path:
            return '(max-width:800px) calc(100vw - 28px), calc((100vw - 64px)/2)'
    if 'vib_' in path:
        index = int(re.search(r'vib_(\d+)', path)[1])
        if 2 <= index <= 8:
            return '(max-width:800px) 74vw, (min-width:1632px) calc((100vw - 92px)/7), 220px'
        if index in (9, 10, 12, 13):
            return '(max-width:800px) calc(100vw - 28px), calc(50vw - 26px)'
    if '/ss26/' in path:
        return '(max-width:800px) calc(100vw - 28px), calc(50vw - 36px)'
    if page in (PUBLIC / 'index.html', PUBLIC / 'it/index.html'):
        if 'about-home' in path:
            return '(max-width:900px) calc(100vw - 28px), calc(50vw - 46px)'
        return '(max-width:900px) calc(100vw - 28px), calc(100vw - 44px)'
    return '(max-width:800px) calc(100vw - 28px), calc(100vw - 44px)'


def fingerprint_static(html):
    def replace(match):
        original = match[1]
        path = local_path(original)
        if path.parent == STATIC:
            # Resolve an earlier generated URL to the editable source asset.
            path = ASSETS / re.sub(r'-[a-f0-9]{12}(?=\.(?:css|js)$)', '', path.name)
        if not path.exists():
            raise FileNotFoundError(path)
        data = path.read_bytes()
        dest = STATIC / f'{path.stem}-{digest(data)}{path.suffix}'
        if not dest.exists():
            dest.write_bytes(data)
        return match[0].replace(original, public_url(dest))
    return re.sub(r'(?:src|href)="(/assets/[^\"]+\.(?:css|js)(?:\?[^\"]*)?)"', replace, html)


def main():
    manifest = json.loads((ASSETS / 'photography/manifest.json').read_text())
    font_html = build_fonts()
    VIDEO_DELIVERY.update(build_video_delivery())
    # Precompute once; language variants share the same media.
    image_urls = {item['path'] for items in manifest['categories'].values() for item in items}
    for page in PUBLIC.rglob('*.html'):
        for tag in re.findall(r'<img\b[^>]*>', page.read_text()):
            url = attr(tag, 'src')
            if url and url.startswith('/assets/'):
                image_urls.add(urlsplit(url).path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(variants, sorted(image_urls)))

    for page in sorted(PUBLIC.rglob('*.html')):
        html = page.read_text()
        # Replace the external Google stylesheet chain with the exact same fonts.
        html = re.sub(r'<link\b[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>', '', html)
        html = re.sub(r'<link[^>]*rel="preload"[^>]*as="font"[^>]*>', '', html)
        html = re.sub(r'<style data-local-fonts>[\s\S]*?</style>', '', html)
        html = html.replace('</head>', font_html + '</head>')

        if 'data-gallery-category=' in html:
            html = static_gallery(html, manifest)
        else:
            # Existing picture wrappers only select scaled copies of the same image.
            html = re.sub(r'<picture>\s*(?:<source\b[^>]*>\s*)+(<img\b[^>]*>)\s*</picture>', r'\1', html)
            def enhance(match):
                tag = match[0]
                url = attr(tag, 'src') or ''
                priority = attr(tag, 'fetchpriority') == 'high' or ('harmony-board-01' in url)
                return responsive_img(tag, image_sizes(page, url), priority)
            html = re.sub(r'<img\b[^>]*>', enhance, html)
        html = re.sub(r'<video\b[^>]*>[\s\S]*?</video>', improve_video, html)

        # A preload without matching srcset can download a second, full-size image.
        html = re.sub(r'<link\b[^>]*rel="preload"[^>]*as="image"[^>]*>', '', html)
        # The static poster replaces the old metadata seek to nine seconds.
        if page.parent.name == 'vibrazioni':
            html = re.sub(r"<script>\s*\(\(\) => \{\s*const video = document.getElementById\('vibrazioni-video'\);[\s\S]*?</script>", '', html)
        if '<video' in html and 'video-playback' not in html:
            html = html.replace('</body>', '<script src="/assets/video-playback.js" defer></script></body>')
        html = fingerprint_static(html)
        if html != page.read_text():
            page.write_text(html)

    (PUBLIC / '_headers').write_text(
        '# Only content-fingerprinted assets use immutable caching. HTML stays fresh.\n'
        '/assets/responsive/*\n  Cache-Control: public, max-age=31536000, immutable\n\n'
        '/assets/static/*\n  Cache-Control: public, max-age=31536000, immutable\n\n'
        '/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n\n'
        '/assets/video/*\n  Cache-Control: public, max-age=31536000, immutable\n\n'
        '/assets/type/*\n  Cache-Control: public, max-age=31536000, immutable\n')
    print(json.dumps({'gallery_photos': {k: len(v) for k, v in manifest['categories'].items()},
        'responsive_files': len(list(RESPONSIVE.glob('*'))), 'html_pages': len(list(PUBLIC.rglob('*.html')))}))


if __name__ == '__main__':
    main()
