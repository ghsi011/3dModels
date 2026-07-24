"""Re-imported-STL measurement for candidate readiness (system python / trimesh).
Writes measure.json. Non-acceptance designer self-check."""
import json
import numpy as np, trimesh

m = trimesh.load("candidate_tool.stl", force="mesh", process=True)
n = m.face_normals
cen = m.triangles.mean(axis=1)
# geometry constants (kept in sync with candidate_model.py)
CX, CY, CZ_TOP, Z_MOUTH = 31.6, 6.25, 24.7, 3.0
X_OUT = float(m.bounds[1][0]); Y_TOP = float(m.bounds[1][1]); Z1 = float(m.bounds[1][2])
out = {"watertight": bool(m.is_watertight), "n_faces": int(len(m.faces)),
       "volume_mm3": round(float(m.volume), 3),
       "bounds_min": [round(float(x), 3) for x in m.bounds[0]],
       "bounds_max": [round(float(x), 3) for x in m.bounds[1]],
       "extents": [round(float(x), 3) for x in m.extents]}

def wall_pos(nx, ny, nz, xr=None, yr=None, zr=None, reducer="mean"):
    sel = (n[:, 0] * nx + n[:, 1] * ny + n[:, 2] * nz) > 0.985
    c = cen[sel]
    if xr: c = c[(c[:, 0] > xr[0]) & (c[:, 0] < xr[1])]
    if yr: c = c[(c[:, 1] > yr[0]) & (c[:, 1] < yr[1])]
    if zr: c = c[(c[:, 2] > zr[0]) & (c[:, 2] < zr[1])]
    if len(c) == 0: return None
    axis = 0 if abs(nx) > 0.5 else (1 if abs(ny) > 0.5 else 2)
    v = c[:, axis]
    return round(float({"mean": np.median(v), "min": v.min(), "max": v.max()}[reducer]), 3)

# cavity walls (inner faces), restricted to the bar footprint
xw_p = wall_pos(-1, 0, 0, yr=(-5.5, 5.0), zr=(6, 22))    # +X inner wall ~ +CX
xw_m = wall_pos(1, 0, 0, yr=(-5.5, 5.0), zr=(6, 22))     # -X inner wall ~ -CX
yw_m = wall_pos(0, 1, 0, yr=(-7, -3), zr=(6, 22), xr=(-30, 30))  # -Y inner floor ~ -CY
ceil = wall_pos(0, 0, -1, yr=(-5.0, 5.0), xr=(-30, 30), zr=(23, 26))  # ceiling ~CZ_TOP
out["wall_plusX"] = xw_p
out["wall_minusX"] = xw_m
out["wall_minusY"] = yw_m
out["ceiling_Z"] = ceil

# +Y closest approach (gable eave) within cavity: lowest-Y gable-band vertex
vg = m.vertices
vg = vg[(vg[:, 1] > CY - 0.5) & (vg[:, 1] < CY + 3.0) & (np.abs(vg[:, 0]) < CX + 0.3) &
        (vg[:, 2] > Z_MOUTH - 0.1) & (vg[:, 2] < CZ_TOP + 0.1)]
out["plusY_eave_minY"] = round(float(vg[:, 1].min()), 3) if len(vg) else None

# clearances vs bar (X +-31, Y +-5.85, Z 0..24)
if xw_p and xw_m:
    out["clear_X_per_end"] = round(min(xw_p - 31.0, -xw_m - 31.0), 3)
if yw_m:
    out["clear_Y_minusSide"] = round(-yw_m - 5.85, 3)
if out.get("plusY_eave_minY"):
    out["clear_Y_plusSide"] = round(out["plusY_eave_minY"] - 5.85, 3)
if ceil:
    out["clear_Z_top"] = round(ceil - 24.0, 3)
out["cap_face_clear_outsideF02"] = round(float(m.bounds[0][2]) - 0.0, 3)  # min Z above D0

# P_BED plane area (installed Y=-16, normal -Y)
ybed = float(m.bounds[0][1])
mask = (np.abs(cen[:, 1] - ybed) < 0.02) & (n[:, 1] < -0.99)
out["pbed_Y"] = round(ybed, 3)
out["pbed_area_mm2"] = round(float(m.area_faces[mask].sum()), 2)

# min wall via inward ray cast; exclude the P_BED skirt/chamfer band (Y<-14)
# and grazing hits, so the result reflects real structural walls only.
struct = cen[:, 1] > -14.0
origins = (cen - n * 1e-3)[struct]
nn = n[struct]
locs, ir, it = m.ray.intersects_location(origins, -nn, multiple_hits=False)
th = np.linalg.norm(locs - origins[ir], axis=1)
dot = np.abs(np.sum((-nn)[ir] * n[it], axis=1))
good = (th > 0.02) & (dot > 0.6)
tw = th[good]
# raw min is a tessellation sliver at the gable-eave/mouth/X-end triple junction;
# structural wall = robust low percentile (matches the 2.0 mm cap/top design walls).
out["min_wall_struct_mm"] = round(float(np.percentile(tw, 0.5)), 3)
out["min_wall_raw_mm"] = round(float(tw.min()), 3)
out["wall_p1_mm"] = round(float(np.percentile(tw, 1)), 3)

# edge radii via circle fit on 3D section vertices (drop the constant axis)
def fit_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    c, *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
    return float(np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2))

def radius(o, nrm, drop, apex2, Rexp, lo=0.25, hi=1.5):
    s = m.section(plane_origin=o, plane_normal=nrm)
    if s is None: return None
    ax = [a for a in range(3) if a != drop]
    P = s.vertices[:, ax]
    d = np.linalg.norm(P - np.array(apex2), axis=1)
    arc = P[(d > lo * Rexp) & (d < hi * Rexp)]
    if len(arc) < 5: return None
    for _ in range(2):  # robust: drop worst residuals, refit
        r = fit_circle(arc)
        # recompute center for residuals
        x, y = arc[:, 0], arc[:, 1]
        A = np.c_[2 * x, 2 * y, np.ones(len(x))]
        c, *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
        res = np.abs(np.sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2) - r)
        arc = arc[res < np.percentile(res, 80) + 1e-9]
        if len(arc) < 5: break
    return round(fit_circle(arc), 3)

def radius3(origins, nrm, drop, apex2, Rexp):
    vals = []
    for o in origins:
        r = radius(o, nrm, drop, apex2, Rexp)
        if r is not None:
            vals.append(r)
    return vals

# 3 samples along each filleted edge (both endpoints + interior)
out["E01_grip_R"] = radius3([[0, y, 0] for y in (-6, 4, 12)], [0, 1, 0], 1, (X_OUT, Z1), 2.0)
out["E02_top_R"] = radius3([[x, 0, 0] for x in (-22, 0, 22)], [1, 0, 0], 0, (Y_TOP, Z1), 1.0)
out["E03_mouth_R"] = radius3([[x, 0, 0] for x in (-25, 0, 25)], [1, 0, 0], 0, (-CY, Z_MOUTH), 0.9)
out["E04_bear_R"] = radius3([[0, 0, z] for z in (8, 14, 22)], [0, 0, 1], 2, (CX, -CY), 0.9)

print(json.dumps(out, indent=2))
json.dump(out, open("measure.json", "w"), indent=2)
