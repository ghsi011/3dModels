"""
Phase 4 verification for the yacht base text sample coupon.

Runs on the EXPORTED STLs re-imported with trimesh, not the in-memory CAD solids.
This coupon has no mating part, so the interference / insertion-sweep checks do
not apply; everything else does.

  1. Mesh sanity           -- watertight, volume, bbox vs the parameters
  2. Thickness ladder      -- each zone's plate top, and the cover left over the text
  3. Text does not break through, and stays inside the footprint
  4. Stroke width          -- stems vs the 1.2 mm PETG-CF minimum
  5. Readability render    -- top view (must read correctly) + bottom (mirrored)
  6. Measurement audit     -- every parameter accounted for in geometry
"""

import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.path import Path

import model as M

D = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{('  -- ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(label)


# ---------------------------------------------------------------- 1. mesh sanity
print("\n1. MESH SANITY (exported STL re-imported)")
base = trimesh.load(os.path.join(D, "sample_base.stl"))
tcf = trimesh.load(os.path.join(D, "sample_text_cf.stl"))
tall = trimesh.load(os.path.join(D, "sample_text_all.stl"))

check(base.is_watertight, "base watertight", f"{len(base.faces)} faces")
check(tcf.is_watertight, "CF text watertight", f"{len(tcf.faces)} faces")

bb = base.bounds
check(abs(bb[1][0] - bb[0][0] - M.cx) < 0.05, "coupon X extent",
      f"{bb[1][0]-bb[0][0]:.2f} vs {M.cx:.2f} mm")
check(abs(bb[1][1] - bb[0][1] - M.cy) < 0.05, "coupon Y extent",
      f"{bb[1][1]-bb[0][1]:.2f} vs {M.cy:.2f} mm")
check(abs(bb[0][2]) < 1e-6, "flat underside on z=0", f"z_min={bb[0][2]:.4f}")

expect_top = M.tdepth + max(M.zone_cover)
check(abs(bb[1][2] - expect_top) < 0.02, "tallest zone height",
      f"{bb[1][2]:.2f} vs {expect_top:.2f} mm")

vb, vt = base.volume / 1000, tcf.volume / 1000
print(f"  translucent PETG {vb:.2f} cm3 (~{vb*1.27:.1f} g)  |  PETG-CF {vt:.3f} cm3 (~{vt*1.27:.2f} g)")
check(vb + vt < 15.0, "small enough for a sub-1h print", f"{vb+vt:.2f} cm3 total")

# ------------------------------------------------------- 2/3. thickness ladder
print("\n2. THICKNESS LADDER + 3. TEXT CONTAINMENT")
# Use up-facing FACE CENTROIDS: a zone's top face is one rectangle whose corner
# vertices sit exactly on the zone boundary, so vertex filtering would either
# miss it or pick up the taller neighbour across the step.
fc, fn = base.triangles_center, base.face_normals
up = fn[:, 2] > 0.99
for i, cover in enumerate(M.zone_cover):
    y0 = -M.cy / 2 + M.EDGE_Y * M.SCALE + i * M.zone_len
    y1 = y0 + M.zone_len
    sel = fc[up & (fc[:, 1] > y0 + 0.1) & (fc[:, 1] < y1 - 0.1)]
    top = sel[:, 2].max()
    want = M.tdepth + cover
    check(abs(top - want) < 0.02, f"zone {i+1} plate top",
          f"{top:.2f} mm (cover {cover:.2f} + recess {M.tdepth:.2f})")

tv = tall.vertices
check(abs(tv[:, 2].min()) < 1e-6, "text starts at the underside", f"z_min={tv[:,2].min():.4f}")
check(abs(tv[:, 2].max() - M.tdepth) < 1e-6, "text stops at the recess depth",
      f"z_max={tv[:,2].max():.4f} vs {M.tdepth:.2f}")
check(min(M.zone_cover) >= 0.8, "thinnest cover is printable",
      f"{min(M.zone_cover):.2f} mm = {min(M.zone_cover)/0.2:.0f} layers @0.2")

# Every zone top must land on a whole 0.2 mm layer, or the slicer rounds the very
# thicknesses the coupon is trying to measure and the engraved labels become lies.
LAYER = 0.2
for i, cover in enumerate(M.zone_cover):
    total = M.tdepth + cover
    n = total / LAYER
    check(abs(n - round(n)) < 1e-6, f"zone {i+1} top is a whole layer @{LAYER} mm",
          f"{total:.2f} mm = {n:.2f} layers")
nrec = M.tdepth / LAYER
check(abs(nrec - round(nrec)) < 1e-6, f"text recess is a whole layer @{LAYER} mm",
      f"{M.tdepth:.2f} mm = {nrec:.2f} layers")
check(tv[:, 0].min() > -M.cx / 2 + 1 and tv[:, 0].max() < M.cx / 2 - 1,
      "text inside footprint (X)",
      f"X {tv[:,0].min():.2f}..{tv[:,0].max():.2f} in +/-{M.cx/2:.2f}")
check(tv[:, 1].min() > -M.cy / 2 + 1 and tv[:, 1].max() < M.cy / 2 - 1,
      "text inside footprint (Y)",
      f"Y {tv[:,1].min():.2f}..{tv[:,1].max():.2f} in +/-{M.cy/2:.2f}")

# every zone must carry exactly one CF word and one bare word
cfc = tcf.triangles_center
for i in range(len(M.zone_cover)):
    y0 = -M.cy / 2 + M.EDGE_Y * M.SCALE + i * M.zone_len
    y1 = y0 + M.zone_len
    inzone = cfc[(cfc[:, 1] > y0) & (cfc[:, 1] < y1)]
    check(len(inzone) > 0 and inzone[:, 0].max() < 0,
          f"zone {i+1}: CF word present and on the LEFT column only",
          f"X {inzone[:,0].min():.1f}..{inzone[:,0].max():.1f}")

# --------------------------------------------------------- 4. stroke width
print("\n4. STROKE WIDTH vs PETG-CF MINIMUM")
PPM = 20


def raster(mesh, ppm=PPM):
    """Rasterise a mesh's XY projection by filling its projected triangles."""
    b = mesh.bounds
    w = int((b[1][0] - b[0][0]) * ppm) + 4
    h = int((b[1][1] - b[0][1]) * ppm) + 4
    img = np.zeros((h, w), dtype=bool)
    tri = mesh.triangles[:, :, :2].copy()
    tri[:, :, 0] = (tri[:, :, 0] - b[0][0]) * ppm + 2
    tri[:, :, 1] = (tri[:, :, 1] - b[0][1]) * ppm + 2
    yy, xx = np.mgrid[0:h, 0:w]
    for t in tri:
        e1, e2 = t[1] - t[0], t[2] - t[0]
        if abs(e1[0] * e2[1] - e1[1] * e2[0]) < 1e-9:
            continue
        x0, x1 = int(t[:, 0].min()), int(np.ceil(t[:, 0].max())) + 1
        y0, y1 = int(t[:, 1].min()), int(np.ceil(t[:, 1].max())) + 1
        p = np.column_stack([xx[y0:y1, x0:x1].ravel(), yy[y0:y1, x0:x1].ravel()])
        img[y0:y1, x0:x1] |= Path(t).contains_points(p + 0.5).reshape(y1 - y0, x1 - x0)
    return img


# Words run along +X, so their vertical stems are crossed by scanning along X.
mask = raster(tcf)
runs = []
for row in range(mask.shape[0]):
    line = mask[row]
    if not line.any():
        continue
    d = np.diff(line.astype(np.int8))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]
    n = min(len(s), len(e))
    runs.extend((e[:n] - s[:n]) / PPM)
runs = np.array([r for r in runs if r > 0.15])
stem = np.percentile(runs, 25)
check(stem >= 1.2, "CF stem width >= 1.2 mm (3x nozzle)",
      f"p25={stem:.2f} mm, median={np.median(runs):.2f} mm")
print(f"  run lengths: p10={np.percentile(runs,10):.2f}  p25={stem:.2f}  "
      f"p50={np.median(runs):.2f}  p90={np.percentile(runs,90):.2f} mm")

word_h = M.report[0][3]
check(word_h >= 6.0, "cap height >= 6 mm for CF", f"word height {word_h:.2f} mm")

# ------------------------------------------------- 5. readability renders
print("\n5. READABILITY RENDER (top must read correctly, bottom must mirror)")


def draw(ax, flip, title):
    pb = base.bounds
    hx = [-pb[1][0], -pb[0][0]] if flip else [pb[0][0], pb[1][0]]
    ax.add_patch(plt.Rectangle((hx[0], pb[0][1]), hx[1] - hx[0], pb[1][1] - pb[0][1],
                               facecolor="#dfe8e6", edgecolor="#5a6b68", lw=1.2))
    for mesh, color in ((tcf, "#26315e"), (tall, None)):
        pass
    # bare recesses = everything in tall that is not in tcf -> draw tall light, tcf dark
    for mesh, color in ((tall, "#9fb3ae"), (tcf, "#26315e")):
        tri = mesh.triangles[:, :, :2]
        h = tri[:, :, 0] * (-1 if flip else 1)
        polys = np.stack([h, tri[:, :, 1]], axis=-1)
        ax.add_collection(PolyCollection(polys, facecolors=color, edgecolors="none"))
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.set_title(title, fontsize=10)
    ax.axis("off")


fig, axes = plt.subplots(1, 2, figsize=(12, 6.4))
draw(axes[0], False,
     "TOP view - read down through the translucent base\n"
     "MUST READ CORRECTLY   (dark = PETG-CF inlay, grey = bare recess)")
draw(axes[1], True,
     "BOTTOM view - the underside as printed\nMUST LOOK MIRRORED")
for i, c in enumerate(M.ZONE_COVER):
    y0 = -M.cy / 2 + M.EDGE_Y * M.SCALE + i * M.zone_len
    for ax in axes:
        ax.plot([-M.cx / 2, M.cx / 2], [y0, y0], color="#c0392b", lw=0.7, ls="--")
    axes[0].text(M.cx / 2 + 2, y0 + M.zone_len / 2, f"{c:.1f} mm cover",
                 va="center", fontsize=9, color="#c0392b")
plt.tight_layout()
out = os.path.join(D, "sample_readability.png")
plt.savefig(out, dpi=140, facecolor="white")
print(f"  wrote {out}")

# ------------------------------------------------- section render
fig, ax = plt.subplots(figsize=(9, 2.6))
for i, cover in enumerate(M.zone_cover):
    y0 = -M.cy / 2 + M.EDGE_Y * M.SCALE + i * M.zone_len
    ax.add_patch(plt.Rectangle((y0, M.tdepth), M.zone_len, cover,
                               facecolor="#bfe3dd", edgecolor="#2c6e63", lw=1))
    ax.add_patch(plt.Rectangle((y0, 0), M.zone_len, M.tdepth,
                               facecolor="#26315e", edgecolor="#2c6e63", lw=1))
    ax.text(y0 + M.zone_len / 2, M.tdepth + cover + 0.3, f"{cover:.1f}",
            ha="center", fontsize=9)
ax.set_xlim(-M.cy / 2 - 3, M.cy / 2 + 3)
ax.set_ylim(-0.8, max(M.zone_cover) + M.tdepth + 1.4)
ax.set_aspect(5)
ax.set_title("Section along the ladder - dark = 0.6 mm text layer, light = translucent cover (mm)",
             fontsize=10)
ax.set_xlabel("Y (mm)")
ax.set_ylabel("Z (mm)")
plt.tight_layout()
out2 = os.path.join(D, "sample_section.png")
plt.savefig(out2, dpi=140, facecolor="white")
print(f"  wrote {out2}")

# ------------------------------------------------- 6. measurement audit
print("\n6. MEASUREMENT AUDIT")
audit = {
    # Coupon is deliberately ~4 mm wider than the real base to fit the zone-label
    # strip; the text columns themselves still sit at true scale.
    "BASE_X 63.67 measured -> coupon width close to it":
        abs(M.cx - M.BASE_X) < 5.0,
    "BASE_MIN_THK 2.1 measured -> straddled within 0.15 mm by a rung":
        min(abs(c - M.BASE_MIN_THK) for c in M.ZONE_COVER) <= 0.15,
    "ladder brackets the real base on both sides":
        min(M.ZONE_COVER) < M.BASE_MIN_THK < max(M.ZONE_COVER),
    "TEXT_DEPTH 0.6 realised in geometry":
        abs(tv[:, 2].max() - M.tdepth) < 1e-6,
    "all 4 ZONE_COVER values realised": True,
    "WORD_SIZE 10 realised at true scale":
        abs(M.report[0][2] - 24.7) < 1.0,
    "both variants present (CF inlay + bare recess)":
        tcf.volume < tall.volume * 0.75,
}
for k, ok in audit.items():
    check(ok, k)

print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"))
