"""Refine the real FIRST portfolio object's sculpted geometry while preserving
the author-photograph texture atlas and separately modelled raised FIRST letters.

Important: interpretative, reference-driven geometry; not a 3D scan.
Source model and source reference photos are kept unchanged.
Run: python scripts/project-sources/refine_first_model.py
"""
from pathlib import Path
import json
import math
import struct
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "public/assets/first"
SOURCE = ASSETS / "first-sculpt-44d25053826e.glb"
DEST = ASSETS / "first-sculpt-handformed-v3.glb"
ANGULAR_SEGMENTS = 112
VERTICAL_SEGMENTS = 112

raw = SOURCE.read_bytes()
magic, version, length = struct.unpack_from("<III", raw, 0)
assert (magic, version, length) == (0x46546C67, 2, len(raw))
json_len, json_type = struct.unpack_from("<II", raw, 12)
assert json_type == 0x4E4F534A
data = json.loads(raw[20:20 + json_len])
bin_head = 20 + json_len
bin_len, bin_type = struct.unpack_from("<II", raw, bin_head)
assert bin_type == 0x004E4942
binary = bytearray(raw[bin_head + 8:bin_head + 8 + bin_len])
assert data.get("extras", {}).get("photoTexture") is True
assert "".join(data["extras"]["raisedLetters"]) == "FIRST"
letter_end = data["extras"]["letterVertexCount"]


def accessor(number):
    meta = data["accessors"][number]
    view = data["bufferViews"][meta["bufferView"]]
    offset = view.get("byteOffset", 0) + meta.get("byteOffset", 0)
    dtype = "<f4" if meta["componentType"] == 5126 else "<u2"
    channels = {"SCALAR": 1, "VEC2": 2, "VEC3": 3}[meta["type"]]
    return np.frombuffer(binary, dtype=dtype,
                         count=meta["count"] * channels, offset=offset
                         ).reshape(-1, channels)

pos = accessor(0)
norm = accessor(1)
faces = accessor(3).reshape(-1, 3)
body_start = letter_end
body_count = (ANGULAR_SEGMENTS + 1) * (VERTICAL_SEGMENTS + 1)
body_end = body_start + body_count
assert 0 < letter_end < len(pos) and body_end + 2 < len(pos)
assert np.isfinite(pos).all()
# Measurements and silhouette are based on the eight views of the physical
# object shown in the portfolio. Four fingertip cups form one continuous
# sculptural grip, along a broad curved side, not horizontal dents across
# the entire cylinder. Bottom to top center (normalized body height):
cups = [
    (0.125, 0.180, 0.112, 0.85),
    (0.358, 0.195, 0.118, 0.91),
    (0.592, 0.193, 0.122, 0.96),
    (0.824, 0.180, 0.119, 1.01),
]


def smoothstep(a, b, x):
    q = max(0.0, min(1.0, (x - a) / (b - a)))
    return q * q * (3.0 - 2.0 * q)


def angledelta(x):
    return math.atan2(math.sin(x), math.cos(x))


for j in range(VERTICAL_SEGMENTS + 1):
    t = j / VERTICAL_SEGMENTS
    for i in range(ANGULAR_SEGMENTS + 1):
        a = i / ANGULAR_SEGMENTS * math.tau
        idx = body_start + j * (ANGULAR_SEGMENTS + 1) + i
        # Hand-formed, subtly tapered clay volume: wider near the base,
        # irregular shoulders and a gently asymmetric winding silhouette.
        r = (
            .435
            + .015 * math.sin(2.0 * a + t * 2.35)
            + .008 * math.cos(3.0 * a - t * 4.4)
            + .007 * math.cos(a + 3.0 * t)
            - .014 * t
        )
        # The real object has four separate broad cups whose rims form
        # curved edges; use a rounded superelliptic dish rather than a
        # Gaussian trough that looks like a smooth tube.
        for center, depth, height_span, arc in cups:
            # Finger recesses sweep slightly towards the right at the top.
            axis = 2.18 + 0.32 * (t - .45) + 0.09 * math.sin(center * 8)
            theta = abs(angledelta(a - axis))
            # Tilt the lower lip slightly for a natural, non-mechanical
            # transition between depressions.
            tt = t - center + .014 * math.sin(a - axis)
            elliptical = ((theta / arc) ** 2.4 +
                          (abs(tt) / height_span) ** 2.4) ** (1 / 2.4)
            cup = 1 - smoothstep(.25, 1.10, elliptical)
            r -= depth * cup
            # Subtle fuller clay lip at the lower and side edges.
            lip = math.exp(-((elliptical - 1.02) / .16) ** 2)
            r += .012 * lip
        # Smaller upper opposing finger mark, visible when rotated.
        thumb_angle = angledelta(a - 4.75)
        r -= .055 * math.exp(-((thumb_angle / .45) ** 4) -
                             (((t - .82) / .15) ** 4))
        # Irregular diagonal crease at the crown of the hand-made sculpture.
        crown_angle = 2.55 - .85 * (t - .90)
        crown_delta = angledelta(a - crown_angle)
        r += .014 * math.exp(-((crown_delta / .09) ** 2) -
                             (((t - .93) / .14) ** 2))
        # Tiny geometric relief; the existing author-photo texture retains
        # the fine tactile clay grain. No random/noisy mesh distortion.
        r += .0018 * math.sin(17 * a + 21 * t) * math.sin(11 * a - 13 * t)
        # Preserve the slightly rolled-in bottom/top closure.
        closure = max(.84, min(1, (t + .007) / .022,
                               (1 - t + .006) / .024))
        r = max(.16, r * closure)
        # Top edge is angled, dented, and uneven rather than a level cap.
        crown = (1.30 + .087 * math.sin(a + .45)
                 + .032 * math.sin(3.0 * a - .8)
                 - .055 * math.exp(-(angledelta(a - 2.68) / .34) ** 2))
        y = -1 + t * (crown + 1)
        pos[idx] = (r * math.cos(a), y, r * math.sin(a))

# Move the top cap's central vertex to the mean crown height.
cap_top_index = body_end + 1
if abs(float(pos[cap_top_index, 0])) < 1e-5 and abs(float(pos[cap_top_index, 2])) < 1e-5:
    pos[cap_top_index, 1] = float(np.mean(
        pos[body_end - ANGULAR_SEGMENTS - 1:body_end - 1, 1]))

# Recompute the body's normals in place; other components (raised black
# lettering, ring) preserve their normals/material/texture UVs exactly.
surface = np.zeros((len(pos), 3), dtype=np.float64)
for tri in faces:
    # Avoid changing the lettering and cylindrical base.
    if np.any(tri < body_start) or np.any(tri >= body_end + 2):
        continue
    p0, p1, p2 = pos[tri]
    n = np.cross(p1 - p0, p2 - p0)
    surface[tri] += n
for j in range(VERTICAL_SEGMENTS + 1):
    left = body_start + j * (ANGULAR_SEGMENTS + 1)
    right = left + ANGULAR_SEGMENTS
    joined = surface[left] + surface[right]
    surface[left] = joined
    surface[right] = joined
lengths = np.linalg.norm(surface[body_start:body_end + 2], axis=1)
valid = lengths > 1e-10
new_norm = surface[body_start:body_end + 2]
new_norm[valid] /= lengths[valid, None]
norm[body_start:body_end + 2] = new_norm.astype("<f4")

data["accessors"][0]["min"] = pos.min(axis=0).tolist()
data["accessors"][0]["max"] = pos.max(axis=0).tolist()
data["extras"]["classification"] = (
    "Interpretative 3D geometry reconstructed from the author's multi-angle "
    "photographs; not photogrammetry and not an exact 3D scan"
)
data["extras"]["geometryRefinement"] = "Hand-formed body; four deep curved grip cups; asymmetric crown"
data["extras"]["photographicTexturePreserved"] = True
data["asset"]["generator"] = "FIRST handformed silhouette refinement v3"

encoded = json.dumps(data, separators=(",", ":")).encode("utf-8")
encoded += b" " * (-len(encoded) % 4)
out = (struct.pack("<III", 0x46546C67, 2,
                   12 + 8 + len(encoded) + 8 + len(binary))
       + struct.pack("<II", len(encoded), 0x4E4F534A)
       + encoded
       + struct.pack("<II", len(binary), 0x004E4942)
       + bytes(binary))
DEST.write_bytes(out)
assert len(out) < 2_000_000
assert np.isfinite(pos).all() and np.isfinite(norm).all()
assert np.max(faces) < len(pos)
assert len(data["images"]) == 1 and data["images"][0]["mimeType"] == "image/jpeg"
print(f"FIRST v3: {len(pos)} vertices, {len(faces)} triangles; {len(out)} bytes")
print(f"Refined grip cup depth: up to {max(c[1] for c in cups):.3f}, source intact: {SOURCE.name}")
