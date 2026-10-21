from pathlib import Path
from PIL import Image, ImageOps
import hashlib, json, re, shutil

ROOT = Path("public/assets/photography")
OUT = ROOT / "optimized"
MANIFEST = ROOT / "manifest.json"
CATEGORIES = ("events", "street", "fashion", "personal")
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIDE = 2200
QUALITY = 80
STATIC_QUALITY = 82
STATIC_ASSETS = {
    Path("public/assets/about-desk.jpg"): Path("public/assets/about-desk.webp"),
    Path("public/assets/filippo-mantini-illustration.jpg"): Path("public/assets/filippo-mantini-illustration.webp"),
    Path("public/assets/citta-di-castello-hero.jpg"): Path("public/assets/citta-di-castello-hero.webp"),
}


# Display-sized, high-quality variants. Originals and existing gallery images
# remain untouched; only browsers at smaller viewports use these previews.
PREVIEW_WIDTH = 1152
PREVIEW_MAX_HEIGHT = 1600
PREVIEW_QUALITY = 93

def create_preview(src, dest, max_width=PREVIEW_WIDTH, max_height=PREVIEW_MAX_HEIGHT):
    with Image.open(src) as original:
        image = ImageOps.exif_transpose(original)
        full_width, full_height = image.size
        if full_width <= max_width and full_height <= max_height:
            return None
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        dest.parent.mkdir(parents=True, exist_ok=True)
        # WebP ICC preserves original color appearance.
        icc = original.info.get("icc_profile")
        image.save(dest, "WEBP", quality=PREVIEW_QUALITY, method=6,
                   **({"icc_profile": icc} if icc else {}))
        # Avoid a variant that saves no bandwidth.
        if dest.stat().st_size >= src.stat().st_size * 0.88:
            dest.unlink(missing_ok=True)
            return None
        return (image.width, image.height)

def natural_key(path):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", path.name)]

def file_hash(path):
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

try:
    old = json.loads(MANIFEST.read_text("utf-8")) if MANIFEST.exists() else {}
except Exception:
    old = {}

old_by_source = {}
for category, items in old.get("categories", {}).items():
    for item in items:
        old_by_source[(category, item.get("source", ""))] = item

manifest = {"version": 1, "categories": {}}
desired_outputs = set()

for category in CATEGORIES:
    src_dir = ROOT / category
    out_dir = OUT / category
    out_dir.mkdir(parents=True, exist_ok=True)

    items = []
    sources = sorted(
        [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED],
        key=natural_key
    ) if src_dir.exists() else []

    used_names = set()

    for index, src in enumerate(sources, start=1):
        stem = re.sub(r"[^A-Za-z0-9._-]+", "-", src.stem).strip("-") or f"photo-{index:02d}"
        out_name = f"{stem}.webp"
        counter = 2
        while out_name.lower() in used_names:
            out_name = f"{stem}-{counter}.webp"
            counter += 1
        used_names.add(out_name.lower())

        dest = out_dir / out_name
        digest = file_hash(src)
        previous = old_by_source.get((category, src.name))

        width = height = None
        try:
            if previous and previous.get("hash") == digest and dest.exists():
                width = previous.get("width")
                height = previous.get("height")
            else:
                with Image.open(src) as im:
                    im = ImageOps.exif_transpose(im)
                    width, height = im.size
                    # WebP files that are already within the portfolio size limit
                    # are kept byte-for-byte to avoid generation loss.
                    if src.suffix.lower() == ".webp" and max(width, height) <= MAX_SIDE:
                        shutil.copy2(src, dest)
                    else:
                        if im.mode not in ("RGB", "RGBA"):
                            im = im.convert("RGB")
                        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
                        width, height = im.size
                        if im.mode == "RGBA":
                            bg = Image.new("RGB", im.size, "white")
                            bg.paste(im, mask=im.getchannel("A"))
                            im = bg
                        else:
                            im = im.convert("RGB")
                        im.save(dest, "WEBP", quality=QUALITY, method=6)
        except (OSError, ValueError) as exc:
            print(f"Skipping invalid image {src}: {exc}")
            if dest.exists():
                dest.unlink()
            continue

        display_path = f"/assets/photography/optimized/{category}/{out_name}"
        preview = OUT / "preview" / category / out_name
        previous_preview = (previous or {}).get("previewPath")
        # Regenerate only when source changed; avoid re-encoding stable assets.
        if previous and previous.get("hash") == digest and previous_preview and preview.exists():
            preview_size = (previous.get("previewWidth"), previous.get("previewHeight"))
        else:
            preview_size = create_preview(src, preview)
        if preview_size:
            desired_outputs.add(preview.resolve())
            display_preview = f"/assets/photography/optimized/preview/{category}/{out_name}"
            preview_width, preview_height = preview_size
        else:
            display_preview = display_path
            preview_width, preview_height = width, height

        desired_outputs.add(dest.resolve())
        items.append({
            "source": src.name,
            "path": display_path,
            "previewPath": display_preview,
            "previewWidth": preview_width,
            "previewHeight": preview_height,
            "hash": digest,
            "width": width,
            "height": height
        })

    manifest["categories"][category] = items

# Remove optimized files whose source was deleted/renamed.
if OUT.exists():
    for p in OUT.rglob("*.webp"):
        if p.resolve() not in desired_outputs:
            p.unlink()

MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8")
print(json.dumps({k: len(v) for k, v in manifest["categories"].items()}))

# Optimize the large static images used by the portfolio itself.
for src, dest in STATIC_ASSETS.items():
    if not src.exists():
        continue
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.getchannel("A"))
            im = bg
        else:
            im = im.convert("RGB")
        im.save(dest, "WEBP", quality=STATIC_QUALITY, method=6)

# Static portfolio variants are generated by CI.


# Vibrazioni: 220px-wide horizontal gallery currently references several
# multi-megabyte originals. Preview assets are display-sized and optional.
# Keep every source image untouched for full quality access.
VIB_OUTPUT = Path("public/assets/vib-preview")
VIB_OUTPUT.mkdir(parents=True, exist_ok=True)
for source in sorted(Path("public/assets").glob("vib_*.webp"), key=natural_key):
    index = int(re.search(r"vib_(\d+)", source.stem).group(1))
    target = VIB_OUTPUT / source.name
    limits = (1440, 1800) if index == 1 else (1152, 1600)
    if not target.exists() or source.stat().st_mtime > target.stat().st_mtime:
        variant = create_preview(source, target, *limits)
        print(f"Vibrazioni {source.name}: " +
              (f"{variant[0]}x{variant[1]} preview" if variant else "original retained"))
