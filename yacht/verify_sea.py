"""
Phase 4 verification for coupon B — the real-sea reality-check coupon.

Runs on the EXPORTED STLs re-imported with trimesh, not the in-memory solids,
exactly like verify.py does for coupon A.

Coupon A's ladder is a controlled experiment: flat cover, one number per zone.
Coupon B has no such luxury -- the cover over every letter is whatever the real
sea sculpt happens to leave there. So on top of the usual mesh/geometry gates
this script MEASURES that cover by ray-casting, per word, and renders a heightmap
so you can see which letters sit under a crest and which under a trough. Without
that number coupon B is just "a lumpy thing" and cannot be compared to coupon A.

  1. Mesh sanity            -- watertight, volume, chunk extents, flat underside
  2. Recess geometry        -- exactly z = 0 .. 0.6, whole layers, nothing else
  3. Text containment       -- 1.5 mm clear of every edge
  4. CF split               -- present, LEFT column only, strict subset
  5. Stroke width           -- stems vs the 1.2 mm PETG-CF minimum
  6. LOCAL COVER            -- ray-cast cover over each of the 4 words
  7. Readability render     -- top reads correctly, bottom mirrored
  8. Coverage heightmap     -- cover in mm, text outlines overlaid
"""

import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.path import Path

import sea_model as S

D = os.path.dirname(os.path.abspath(__file__))
FAIL = []

CHUNK_X = S.CUT_X1 - S.CUT_X0          # 34.0 mm
CHUNK_Y = S.CUT_Y1 - S.CUT_Y0          # 62.0 mm
LAYER = 0.2
EDGE_MARGIN = 1.5                      # mm of chunk left clear round the text


def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{('  -- ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(label)


# ---------------------------------------------------------------- 1. mesh sanity
print("\n1. MESH SANITY (exported STL re-imported)")
base = trimesh.load(os.path.join(D, "sea_base.stl"))
tcf = trimesh.load(os.path.join(D, "sea_text_cf.stl"))
tall = trimesh.load(os.path.join(D, "sea_text_all.stl"))

check(base.is_watertight, "sea base watertight", f"{len(base.faces)} faces")
check(base.body_count == 1, "sea base is one connected body", f"{base.body_count} bodies")
check(tcf.is_watertight, "CF text watertight", f"{len(tcf.faces)} faces")
check(tall.is_watertight, "full text watertight", f"{len(tall.faces)} faces")
check(base.is_winding_consistent, "sea base winding consistent")
check(base.volume > 0, "sea base has positive (outward) volume", f"{base.volume:.1f} mm3")

bb = base.bounds
check(abs(bb[1][0] - bb[0][0] - CHUNK_X) < 0.1, "chunk X extent",
      f"{bb[1][0]-bb[0][0]:.3f} vs CUT_X1-CUT_X0 = {CHUNK_X:.1f} mm")
check(abs(bb[1][1] - bb[0][1] - CHUNK_Y) < 0.1, "chunk Y extent",
      f"{bb[1][1]-bb[0][1]:.3f} vs CUT_Y1-CUT_Y0 = {CHUNK_Y:.1f} mm")

# Sane volume: it must sit between "solid box to the lowest sea point" and
# "solid box to the highest", minus the text that was cut out of it.
sea_lo, sea_hi = None, None
fn, fc = base.face_normals, base.triangles_center
upf = fn[:, 2] > 0.2
sea_lo = fc[upf][:, 2].min()
sea_hi = bb[1][2]
tvol = tall.volume
lo_bound = CHUNK_X * CHUNK_Y * sea_lo - tvol
hi_bound = CHUNK_X * CHUNK_Y * sea_hi
check(lo_bound < base.volume < hi_bound, "sea base volume is sane",
      f"{base.volume/1000:.3f} cm3 in ({lo_bound/1000:.2f} .. {hi_bound/1000:.2f}) cm3")

# --- flat underside: a REAL face at z = 0, not a stray vertex ---------------
down = fn[:, 2] < -0.999
bot = down & (fc[:, 2] < 1e-6)
bot_area = base.area_faces[bot].sum()
text_area = tall.volume / S.TEXT_DEPTH          # text is a prism, so this is exact
check(abs(bb[0][2]) < 1e-9, "underside sits at exactly z = 0", f"z_min={bb[0][2]:.9f}")
check(bot.sum() >= 2, "underside is a real face, not a stray vertex",
      f"{bot.sum()} down-facing triangles at z=0")
check(abs(bot_area + text_area - CHUNK_X * CHUNK_Y) < 0.5,
      "underside face area = footprint minus the text openings",
      f"{bot_area:.1f} + {text_area:.1f} = {bot_area+text_area:.1f} vs {CHUNK_X*CHUNK_Y:.1f} mm2")
# and every vertex of those faces really is on z=0
botv = base.vertices[base.faces[bot].ravel()]
check(np.abs(botv[:, 2]).max() < 1e-9, "every underside vertex on z = 0",
      f"max |z| = {np.abs(botv[:,2]).max():.2e}")

vb, vt = base.volume / 1000, tcf.volume / 1000
print(f"  translucent PETG {vb:.3f} cm3 (~{vb*1.27:.2f} g)  |  "
      f"PETG-CF {vt:.3f} cm3 (~{vt*1.27:.2f} g)")
print(f"  sea top spans z {sea_lo:.2f} .. {sea_hi:.2f} mm")

# ------------------------------------------------------------ 2. recess geometry
print("\n2. RECESS GEOMETRY")
tv = tall.vertices
check(abs(tv[:, 2].min()) < 1e-6, "text starts at the underside", f"z_min={tv[:,2].min():.6f}")
check(abs(tv[:, 2].max() - S.TEXT_DEPTH) < 1e-6, "text stops at the recess depth",
      f"z_max={tv[:,2].max():.6f} vs {S.TEXT_DEPTH:.2f}")
n = S.TEXT_DEPTH / LAYER
check(abs(n - round(n)) < 1e-9 and round(n) == 3,
      f"recess is exactly 3 layers @ {LAYER} mm", f"{S.TEXT_DEPTH:.2f} mm = {n:.3f} layers")

# The recess must open onto the plate and stop dead at z = TEXT_DEPTH: fire rays
# straight up from below the plate and look at where they first hit solid.
# Inside a letter that must be the recess ceiling at 0.6; outside it, the plate
# underside at 0.0. Anything in between means the cut went too deep or too shallow.
PPM = 20


def raster(mesh, bounds=None, ppm=PPM):
    """Rasterise a mesh's XY projection by filling its projected triangles."""
    b = mesh.bounds if bounds is None else bounds
    w = int(round((b[1][0] - b[0][0]) * ppm)) + 4
    h = int(round((b[1][1] - b[0][1]) * ppm)) + 4
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


def text_contains(pts_xy, mesh):
    """True where an XY point falls inside a text prism's footprint."""
    tri = mesh.triangles[:, :, :2]
    inside = np.zeros(len(pts_xy), dtype=bool)
    for t in tri:
        e1, e2 = t[1] - t[0], t[2] - t[0]
        if abs(e1[0] * e2[1] - e1[1] * e2[0]) < 1e-9:
            continue
        inside |= Path(t).contains_points(pts_xy)
    return inside


PITCH = 0.4
gx = np.arange(-CHUNK_X / 2 + PITCH / 2, CHUNK_X / 2, PITCH)
gy = np.arange(-CHUNK_Y / 2 + PITCH / 2, CHUNK_Y / 2, PITCH)
GX, GY = np.meshgrid(gx, gy)
grid_xy = np.column_stack([GX.ravel(), GY.ravel()])
in_text = text_contains(grid_xy, tall)
print(f"  sampling grid {len(gx)} x {len(gy)} @ {PITCH} mm, "
      f"{in_text.sum()} points fall inside a letter")

# Erode / dilate by one cell. A sample sitting exactly on a glyph outline is
# neither in nor out -- its ray grazes the recess wall -- so the "inside" tests
# use the eroded mask and the "outside" tests the complement of the dilated one.
tmask = in_text.reshape(GX.shape)


def shift_and(mask, op):
    out = mask.copy()
    for a, b in ((np.s_[1:], np.s_[:-1]), (np.s_[:-1], np.s_[1:])):
        for ax in (0, 1):
            sl_o = (a, slice(None)) if ax == 0 else (slice(None), a)
            sl_i = (b, slice(None)) if ax == 0 else (slice(None), b)
            if op == "erode":
                out[sl_o] &= mask[sl_i]
            else:
                out[sl_o] |= mask[sl_i]
    return out


sel = shift_and(tmask, "erode").ravel()
outside_sel = ~shift_and(tmask, "dilate").ravel()

up_from_below = np.column_stack([grid_xy, np.full(len(grid_xy), -1.0)])
dirs_up = np.tile([0.0, 0.0, 1.0], (len(grid_xy), 1))
loc, idx_ray, _ = base.ray.intersects_location(up_from_below, dirs_up, multiple_hits=True)

first_hit = np.full(len(grid_xy), np.nan)
for r in np.unique(idx_ray):
    first_hit[r] = loc[idx_ray == r][:, 2].min()

inside_first = first_hit[sel]
outside_first = first_hit[outside_sel & ~np.isnan(first_hit)]
check(np.isfinite(inside_first).all() and
      np.abs(inside_first - S.TEXT_DEPTH).max() < 1e-3,
      "recess ceiling is exactly at z = 0.6 under every letter",
      f"{np.nanmin(inside_first):.4f} .. {np.nanmax(inside_first):.4f} mm "
      f"over {sel.sum()} samples")
check(np.abs(outside_first).max() < 1e-3,
      "solid plate starts at z = 0 everywhere outside the letters",
      f"max first-hit {np.abs(outside_first).max():.2e} mm over {len(outside_first)} samples")

# Nothing deeper, nothing shallower: no base geometry anywhere strictly INSIDE a
# glyph between the plate underside and the recess ceiling. (The recess side
# walls are on the outline itself, so the mask is eroded 0.15 mm before testing.)
tb = np.array([[-CHUNK_X / 2, -CHUNK_Y / 2, 0], [CHUNK_X / 2, CHUNK_Y / 2, 0]])
tras = raster(tall, bounds=tb)
for _ in range(3):
    tras = shift_and(tras, "erode")
bv = base.vertices
near = bv[(bv[:, 2] > 1e-6) & (bv[:, 2] < S.TEXT_DEPTH - 1e-6)]
px = ((near[:, 0] + CHUNK_X / 2) * PPM + 2).astype(int)
py = ((near[:, 1] + CHUNK_Y / 2) * PPM + 2).astype(int)
ok = (px >= 0) & (py >= 0) & (px < tras.shape[1]) & (py < tras.shape[0])
in_near = np.zeros(len(near), dtype=bool)
in_near[ok] = tras[py[ok], px[ok]]
check(in_near.sum() == 0, "no base geometry strictly inside the recess volume",
      f"{int(in_near.sum())} stray vertices in 0 < z < {S.TEXT_DEPTH} "
      f"(of {len(near)} on the recess walls)")

# ---------------------------------------------------------- 3. text containment
print("\n3. TEXT CONTAINMENT")
mx = min(tv[:, 0].min() + CHUNK_X / 2, CHUNK_X / 2 - tv[:, 0].max())
my = min(tv[:, 1].min() + CHUNK_Y / 2, CHUNK_Y / 2 - tv[:, 1].max())
check(mx >= EDGE_MARGIN, f"text >= {EDGE_MARGIN} mm clear of the X edges",
      f"X {tv[:,0].min():.2f}..{tv[:,0].max():.2f} in +/-{CHUNK_X/2:.1f}, margin {mx:.2f} mm")
check(my >= EDGE_MARGIN, f"text >= {EDGE_MARGIN} mm clear of the Y edges",
      f"Y {tv[:,1].min():.2f}..{tv[:,1].max():.2f} in +/-{CHUNK_Y/2:.1f}, margin {my:.2f} mm")

# ------------------------------------------------------------------ 4. CF split
print("\n4. CF / BARE SPLIT")
cv = tcf.vertices
check(len(tcf.faces) > 0 and cv[:, 0].max() < 0,
      "CF text present and on the LEFT column only",
      f"X {cv[:,0].min():.2f}..{cv[:,0].max():.2f}")
cfc = tcf.triangles_center
for sign, name in ((-1, "bottom"), (+1, "top")):
    got = np.sign(cfc[:, 1]) == sign
    check(got.sum() > 0, f"CF word present in the {name} row", f"{int(got.sum())} triangles")

resid = trimesh.boolean.difference([tcf, tall])
rv = resid.volume if resid is not None and len(resid.faces) else 0.0
check(abs(rv) < 1e-3, "CF text is a strict subset of the full text volume",
      f"CF-minus-all residual volume {rv:.2e} mm3")
check(tcf.volume < tall.volume * 0.75, "both variants present (CF inlay + bare recess)",
      f"CF {tcf.volume:.1f} vs all {tall.volume:.1f} mm3")

# -------------------------------------------------------------- 5. stroke width
print("\n5. STROKE WIDTH vs PETG-CF MINIMUM")
# Coupon B's words are rotated 90 deg (they run along +Y to fit the narrow sea
# strip), so the stems are horizontal in the XY plane: scan the raster along X,
# which for a transposed mask means walking its columns.
mask = raster(tcf)
runs = []
for col in range(mask.shape[1]):
    line = mask[:, col]
    if not line.any():
        continue
    d = np.diff(line.astype(np.int8))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]
    k = min(len(s), len(e))
    runs.extend((e[:k] - s[:k]) / PPM)
runs = np.array([r for r in runs if r > 0.15])
stem = np.percentile(runs, 25)
check(stem >= 1.2, "CF stem width >= 1.2 mm (3x nozzle)",
      f"p25={stem:.2f} mm, median={np.median(runs):.2f} mm")
print(f"  run lengths: p10={np.percentile(runs,10):.2f}  p25={stem:.2f}  "
      f"p50={np.median(runs):.2f}  p90={np.percentile(runs,90):.2f} mm")

# ------------------------------------------------------- 6. LOCAL COVER (rays)
print("\n6. LOCAL COVER OVER THE TEXT (ray-cast against the real sea surface)")
# From just above the recess ceiling, fire straight up. The first hit is the sea
# surface directly overhead; that distance IS the translucent cover the word has
# to be read through, and it is the number that makes coupon B comparable to a
# rung of coupon A's ladder.
org = np.column_stack([grid_xy, np.full(len(grid_xy), S.TEXT_DEPTH + 1e-4)])
loc2, ray2, _ = base.ray.intersects_location(org, dirs_up, multiple_hits=True)
top_first = np.full(len(grid_xy), np.nan)
nhits = np.zeros(len(grid_xy), dtype=int)
for r in np.unique(ray2):
    zs = loc2[ray2 == r][:, 2]
    top_first[r] = zs.min()
    nhits[r] = len(zs)

cover = top_first - S.TEXT_DEPTH
ct = cover[sel]
check(np.isfinite(ct).all(), "every text sample sees sea surface above it",
      f"{np.isfinite(ct).sum()}/{sel.sum()} samples hit")
check(np.nanmin(ct) > 0.3, "text never breaks through / is never near-transparent",
      f"min cover {np.nanmin(ct):.2f} mm")
check((nhits[sel] % 2 == 1).all(), "single solid shell above every letter (no voids)",
      f"hit counts {sorted(set(nhits[sel].tolist()))}")


def stats(v):
    v = v[np.isfinite(v)]
    if not len(v):
        return None
    return (v.min(), np.percentile(v, 5), np.median(v), np.percentile(v, 95), v.max())


def line(name, v):
    s = stats(v)
    if s is None:
        print(f"  {name:<28} (no samples)")
        return
    print(f"  {name:<28} min {s[0]:5.2f}  p5 {s[1]:5.2f}  med {s[2]:5.2f}  "
          f"p95 {s[3]:5.2f}  max {s[4]:5.2f}   n={np.isfinite(v).sum()}")


print(f"  {'':<28} ---------------- cover in mm ----------------")
line("ALL TEXT", ct)
gx_sel = grid_xy[sel]
left = gx_sel[:, 0] < 0
bottom = gx_sel[:, 1] < 0
line("LEFT column (PETG-CF)", ct[left])
line("RIGHT column (bare)", ct[~left])
line("BOTTOM row (y<0)", ct[bottom])
line("TOP row (y>0)", ct[~bottom])
WORDS = [("word 1  LEFT/BOTTOM  CF", left & bottom),
         ("word 2  LEFT/TOP     CF", left & ~bottom),
         ("word 3  RIGHT/BOTTOM bare", ~left & bottom),
         ("word 4  RIGHT/TOP    bare", ~left & ~bottom)]
for nm, m in WORDS:
    line(nm, ct[m])

print("  coupon A ladder for reference: 1.0 / 1.6 / 2.2 / 3.0 mm flat cover")

# ------------------------------------------------- 7. readability renders
print("\n7. READABILITY RENDER (top must read correctly, bottom must mirror)")


def draw(ax, flip, title):
    pb = base.bounds
    hx = [-pb[1][0], -pb[0][0]] if flip else [pb[0][0], pb[1][0]]
    ax.add_patch(plt.Rectangle((hx[0], pb[0][1]), hx[1] - hx[0], pb[1][1] - pb[0][1],
                               facecolor="#dfe8e6", edgecolor="#5a6b68", lw=1.2))
    for mesh, color in ((tall, "#9fb3ae"), (tcf, "#26315e")):
        tri = mesh.triangles[:, :, :2]
        h = tri[:, :, 0] * (-1 if flip else 1)
        polys = np.stack([h, tri[:, :, 1]], axis=-1)
        ax.add_collection(PolyCollection(polys, facecolors=color, edgecolors="none"))
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.set_title(title, fontsize=10)
    ax.axis("off")


fig, axes = plt.subplots(1, 2, figsize=(10.5, 7.6))
draw(axes[0], False,
     "TOP view - read down through the real sea surface\n"
     "MUST READ CORRECTLY   (dark = PETG-CF inlay, grey = bare recess)")
draw(axes[1], True,
     "BOTTOM view - the underside as printed\nMUST LOOK MIRRORED")
plt.tight_layout()
out = os.path.join(D, "sea_readability.png")
plt.savefig(out, dpi=140, facecolor="white")
plt.close(fig)
print(f"  wrote {out}")

# ------------------------------------------------- 8. coverage heightmap
print("\n8. COVERAGE HEIGHTMAP")
cov_img = cover.reshape(GX.shape)
fig, ax = plt.subplots(figsize=(6.4, 9.2))
im = ax.imshow(cov_img, origin="lower", cmap="viridis",
               extent=[-CHUNK_X / 2, CHUNK_X / 2, -CHUNK_Y / 2, CHUNK_Y / 2],
               interpolation="nearest")
ax.contour(GX, GY, tmask.astype(float), levels=[0.5], colors="white", linewidths=1.0)
ax.contour(GX, GY, cov_img, levels=[1.0, 1.6, 2.2, 3.0],
           colors="#ffffff", linewidths=0.5, alpha=0.45, linestyles="--")
cb = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.03)
cb.set_label("translucent cover above the text (mm)")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_title("Coupon B - cover left by the real sea surface\n"
             "white outlines = letters, dashed = coupon A's 1.0/1.6/2.2/3.0 rungs",
             fontsize=10)
ax.set_aspect("equal")
plt.tight_layout()
out2 = os.path.join(D, "sea_coverage.png")
plt.savefig(out2, dpi=140, facecolor="white")
plt.close(fig)
print(f"  wrote {out2}")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"))
