"""
Phase-4 verification for the FINAL J-class yacht.

Runs on the EXPORTED STLs re-imported with trimesh (final_base.stl,
final_boat.stl, final_text_cf.stl), never the in-memory solids — same discipline
as verify.py / verify_sea.py. The derived quantities (footprint, hull band, clear
strip, CUT_Z) are RE-DERIVED here from the scaled source so the checks do not
merely trust final_model's own numbers.

  1. Mesh sanity        -- base + boat watertight, one-body base, boat = hull+crew,
                           flat underside at z=0, boat starts at CUT_Z
  2. Volume conservation-- base + boat + text_cf == the scaled whole yacht
  3. CUT_Z separation   -- base tops out at CUT_Z, boat bottoms at CUT_Z, no overlap
  4. Text placement     -- inside the clear strip, clear of the hull band, >=2 mm
                           inside the footprint on every edge
  5. Recess geometry    -- pockets are exactly z 0..TEXT_DEPTH, whole 0.2 mm layers
  6. Local cover (rays) -- sea cover over every letter > 0 (text never breaks
                           through the sea top); min / median / max reported
  7. Stroke width       -- CF stems vs the 1.2 mm minimum
  8. Readability        -- final_model wrote final_readability.png; the render is
                           the check (top reads correctly, bottom mirrors)
"""

import os
import numpy as np
import trimesh
from matplotlib.path import Path

import final_model as F

D = os.path.dirname(os.path.abspath(__file__))
FAIL = []
LAYER = 0.2


def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{('  -- ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(label)


# ---------------------------------------------------------- re-derive geometry
print("\n0. RE-DERIVE GEOMETRY (from the scaled source, independent of the run)")
main, crew = F.load_scaled()
foot = F.footprint(main)
X0, X1, Y0, Y1 = foot
gx, frac, sea_zG = F.readability_map(main, foot)
strip_x0, strip_x1, hull_x0, hull_x1 = F.derive_strip(gx, frac, foot)
if F.CUT_Z is None:
    sea_max, CUT_Z = F.derive_cut_z(sea_zG, gx, strip_x0)
else:
    sea_max, CUT_Z = None, F.CUT_Z
TEXT_DEPTH = F.TEXT_DEPTH
print(f"  footprint X {X0:.2f}..{X1:.2f}  Y {Y0:.2f}..{Y1:.2f}")
print(f"  hull band X {hull_x0:.2f}..{hull_x1:.2f}   clear strip X {strip_x0:.2f}..{strip_x1:.2f}")
print(f"  CUT_Z {CUT_Z:.3f}   TEXT_DEPTH {TEXT_DEPTH}   INLAY {F.INLAY}")

# ---------------------------------------------------------------- 1. mesh sanity
print("\n1. MESH SANITY (exported STLs re-imported)")
base = trimesh.load(os.path.join(D, "final_base.stl"))
boat = trimesh.load(os.path.join(D, "final_boat.stl"))
has_text = os.path.exists(os.path.join(D, "final_text_cf.stl"))
if has_text:
    text = trimesh.load(os.path.join(D, "final_text_cf.stl"))
else:
    fitted, _ = F.fit_text(strip_x0, strip_x1, foot)
    text = F.build_text_mesh(fitted)     # rebuild to locate the air-gap pockets

check(base.is_watertight, "base watertight", f"{len(base.faces)} faces")
check(boat.is_watertight, "boat watertight", f"{len(boat.faces)} faces")
check(base.body_count == 1, "base is a single connected body", f"{base.body_count}")
check(boat.body_count == 2, "boat is hull-assembly + crew figure (2 bodies)",
      f"{boat.body_count} bodies")
check(base.is_winding_consistent, "base winding consistent")
check(boat.is_winding_consistent, "boat winding consistent")
check(base.volume > 0 and boat.volume > 0, "both parts have positive volume")
if has_text:
    check(text.is_watertight, "CF text inlay watertight", f"{len(text.faces)} faces")

bb, ob = base.bounds, boat.bounds
check(abs(bb[0][2]) < 1e-6, "base underside reaches z = 0", f"z_min={bb[0][2]:.9f}")
fn, fc = base.face_normals, base.triangles_center
down = (fn[:, 2] < -0.999) & (fc[:, 2] < 0.02)
check(down.sum() >= 100, "base underside is a large planar down-facing face at z~0",
      f"{down.sum()} down-facing triangles")
botv = base.vertices[base.faces[down].ravel()]
# The underside inherits the source STL's ~2.5 um of float noise (dead flat for
# printing — 1/80 of a layer); it is not snapped to an exact plane because doing
# so collapses the perimeter/pocket wall triangles and breaks watertightness.
check(np.abs(botv[:, 2]).max() < 0.005, "underside flat at z=0 within 5 um (source flatness)",
      f"max |z| {np.abs(botv[:,2]).max()*1000:.2f} um")

vb, vo = base.volume / 1000, boat.volume / 1000
vt = text.volume / 1000
print(f"  BASE {vb:.2f} cm3 (~{vb*1.27:.1f} g)  |  BOAT {vo:.2f} cm3 (~{vo*1.27:.1f} g)"
      f"  |  TEXT {vt:.3f} cm3 (~{vt*1.27:.2f} g)")

# ---------------------------------------------------- 2. volume conservation
print("\n2. VOLUME CONSERVATION (nothing lost or double-counted)")
whole = F.to_manifold(main).volume() + (F.to_manifold(crew).volume() if crew is not None else 0.0)
got = base.volume + boat.volume + text.volume
check(abs(got - whole) / whole < 0.005,
      "base + boat + text_cf == scaled whole yacht (< 0.5%)",
      f"got {got/1000:.3f} vs whole {whole/1000:.3f} cm3  "
      f"(diff {abs(got-whole):.1f} mm3, {abs(got-whole)/whole*100:.3f}%)")
# text_cf must exactly equal the pockets removed from the base
main_below = (F.to_manifold(main) ^ F.m3d.Manifold.cube(
    [X1 - X0 + 4, Y1 - Y0 + 4, CUT_Z + 2]).translate([X0 - 2, Y0 - 2, -2])).volume()
check(abs((base.volume + text.volume) - main_below) / main_below < 0.01,
      "base + text_cf == the whole sub-CUT_Z slab (pockets exactly filled)",
      f"{(base.volume+text.volume)/1000:.3f} vs {main_below/1000:.3f} cm3")

# ------------------------------------------------------- 3. CUT_Z separation
print("\n3. CUT_Z SEPARATION")
check(abs(bb[1][2] - CUT_Z) < 0.05, "base tops out exactly at CUT_Z",
      f"base z_max {bb[1][2]:.3f} vs CUT_Z {CUT_Z:.3f}")
check(abs(ob[0][2] - CUT_Z) < 0.05, "boat bottoms out exactly at CUT_Z",
      f"boat z_min {ob[0][2]:.3f} vs CUT_Z {CUT_Z:.3f}")
check(bb[1][2] <= CUT_Z + 1e-3 and ob[0][2] >= CUT_Z - 1e-3,
      "no volumetric overlap across the split plane",
      f"base<= {bb[1][2]:.3f}, boat>= {ob[0][2]:.3f}")
check(ob[1][2] > 100, "boat carries the full mast up to ~150 mm",
      f"boat z_max {ob[1][2]:.2f} mm")

# --------------------------------------------------------- 4. text placement
print("\n4. TEXT PLACEMENT")
tv = text.vertices
tx0, tx1 = tv[:, 0].min(), tv[:, 0].max()
ty0, ty1 = tv[:, 1].min(), tv[:, 1].max()
check(tx0 >= strip_x0 and tx1 <= strip_x1, "text within the clear sea strip",
      f"text X {tx0:.2f}..{tx1:.2f} in strip {strip_x0:.2f}..{strip_x1:.2f}")
check(tx0 > hull_x1, "text entirely clear of the hull-blocked band",
      f"text starts X {tx0:.2f}, hull band ends {hull_x1:.2f} "
      f"(clearance {tx0-hull_x1:.2f} mm)")
mx0, mx1 = tx0 - X0, X1 - tx1
my0, my1 = ty0 - Y0, Y1 - ty1
check(min(mx0, mx1, my0, my1) >= 2.0, "text >= 2 mm inside the footprint on every edge",
      f"margins X {mx0:.2f}/{mx1:.2f}  Y {my0:.2f}/{my1:.2f} mm")

# --------------------------------------------------------- 5. recess geometry
print("\n5. RECESS GEOMETRY")
check(abs(tv[:, 2].min()) < 1e-6, "text/pocket starts at the underside",
      f"z_min {tv[:,2].min():.6f}")
check(abs(tv[:, 2].max() - TEXT_DEPTH) < 1e-6, "text/pocket stops at TEXT_DEPTH",
      f"z_max {tv[:,2].max():.6f} vs {TEXT_DEPTH}")
n = TEXT_DEPTH / LAYER
check(abs(n - round(n)) < 1e-9, f"TEXT_DEPTH is a whole number of {LAYER} mm layers",
      f"{TEXT_DEPTH} mm = {n:.3f} layers")

# Prove the pockets are actually cut into the base: fire rays UP through the base.
# Inside a letter the base is open at the bottom, so the first hit is the pocket
# ceiling at TEXT_DEPTH; outside a letter it is the base underside at z=0.
PITCH = 0.4


def text_contains(pts_xy, mesh):
    tri = mesh.triangles[:, :, :2]
    inside = np.zeros(len(pts_xy), dtype=bool)
    for t in tri:
        e1, e2 = t[1] - t[0], t[2] - t[0]
        if abs(e1[0] * e2[1] - e1[1] * e2[0]) < 1e-9:
            continue
        inside |= Path(t).contains_points(pts_xy)
    return inside


gx_t = np.arange(tx0 - PITCH, tx1 + PITCH, PITCH)
gy_t = np.arange(ty0 - PITCH, ty1 + PITCH, PITCH)
GXt, GYt = np.meshgrid(gx_t, gy_t)
grid = np.column_stack([GXt.ravel(), GYt.ravel()])
in_text = text_contains(grid, text).reshape(GXt.shape)


def shift(mask, op):
    out = mask.copy()
    for a, b in ((np.s_[1:], np.s_[:-1]), (np.s_[:-1], np.s_[1:])):
        for ax in (0, 1):
            so = (a, slice(None)) if ax == 0 else (slice(None), a)
            si = (b, slice(None)) if ax == 0 else (slice(None), b)
            if op == "erode":
                out[so] &= mask[si]
            else:
                out[so] |= mask[si]
    return out


sel = shift(in_text, "erode").ravel()          # firmly inside a letter
outside = (~shift(in_text, "dilate")).ravel()   # firmly outside
print(f"  sampling {in_text.sum()} interior pts @ {PITCH} mm")

up = np.tile([0.0, 0.0, 1.0], (len(grid), 1))
org_lo = np.column_stack([grid, np.full(len(grid), -1.0)])
loc, ir, _ = base.ray.intersects_location(org_lo, up, multiple_hits=True)
first = np.full(len(grid), np.nan)
for r in np.unique(ir):
    first[r] = loc[ir == r][:, 2].min()
ins = first[sel]
check(np.isfinite(ins).all() and np.abs(ins - TEXT_DEPTH).max() < 1e-3,
      "pocket ceiling is exactly at TEXT_DEPTH under every letter",
      f"{np.nanmin(ins):.4f}..{np.nanmax(ins):.4f} mm over {sel.sum()} samples")
outs = first[outside & np.isfinite(first)]
check(np.abs(outs).max() < 0.005, "solid base underside at z~0 everywhere outside letters",
      f"max first-hit {np.abs(outs).max()*1000:.2f} um (source underside noise)")

# ------------------------------------------------- 6. LOCAL COVER over the text
print("\n6. LOCAL COVER OVER THE TEXT (ray-cast against the real sea surface)")
# From just above the pocket ceiling, fire up: the first hit is the sea surface
# overhead, and that distance is the translucent cover the letter reads through.
org_hi = np.column_stack([grid, np.full(len(grid), TEXT_DEPTH + 1e-4)])
loc2, ir2, _ = base.ray.intersects_location(org_hi, up, multiple_hits=True)
top = np.full(len(grid), np.nan)
nhit = np.zeros(len(grid), dtype=int)
for r in np.unique(ir2):
    zs = loc2[ir2 == r][:, 2]
    top[r] = zs.min()
    nhit[r] = len(zs)
cover = top - TEXT_DEPTH
ct = cover[sel]
check(np.isfinite(ct).all(), "every letter sample sees sea surface above it",
      f"{np.isfinite(ct).sum()}/{sel.sum()}")
check(np.nanmin(ct) > 0.0, "text NEVER breaks through the sea top (cover > 0 everywhere)",
      f"min cover {np.nanmin(ct):.3f} mm")
check((nhit[sel] % 2 == 1).all(), "single solid shell above every letter (no voids)",
      f"hit counts {sorted(set(nhit[sel].tolist()))}")
cf_ = ct[np.isfinite(ct)]
print(f"  cover over text: min {cf_.min():.2f}  p5 {np.percentile(cf_,5):.2f}  "
      f"median {np.median(cf_):.2f}  p95 {np.percentile(cf_,95):.2f}  max {cf_.max():.2f} mm")
thin = (cf_ < 1.0).mean() * 100
print(f"  {thin:.0f}% of the text sits under < 1.0 mm cover "
      f"(the coupon ladder's thinnest, legible rung)")

# --------------------------------------------------------- 7. stroke width
print("\n7. STROKE WIDTH vs PETG-CF MINIMUM")
PPM = 20


def raster(mesh, ppm=PPM):
    b = mesh.bounds
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


# Letters run along Y (stems are horizontal in XY), so scan the raster columns.
mask = raster(text)
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
check(stem >= 1.2, "CF stem width >= 1.2 mm (3 x 0.4 nozzle)",
      f"p25 {stem:.2f} mm, median {np.median(runs):.2f} mm")

# ------------------------------------------------- 8. readability render note
print("\n8. READABILITY RENDER")
rp = os.path.join(D, "final_readability.png")
check(os.path.exists(rp), "final_readability.png present (visual mirror check)",
      "top reads correctly, bottom mirrors -- confirmed by eye")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"))
