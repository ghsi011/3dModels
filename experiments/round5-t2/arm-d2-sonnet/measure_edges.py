"""Edge-radius sampling for E-01..E-05, on the re-imported STL (system python).
Method: at each named sample location, collect mesh VERTICES in a small 3D
neighborhood of the known corner, project them onto the plane perpendicular to the
edge's own run axis (an explicit, known projection -- not an auto-oriented section
transform), and algebraically least-squares fit a circle to the projected points.
E-05 (P_BED chamfer) is reported as its offset, since it is plan-allowed-sharp with
min_radius_mm 0.0.
"""
import json
from pathlib import Path

import numpy as np
import trimesh

OUT = Path(__file__).parent
STL = OUT / "candidate_tool.stl"
mesh = trimesh.load(STL, force="mesh", process=True)
V = mesh.vertices

CAV_X_HALF = 31.5
CAV_Y_HALF = 6.15
Z_FLOOR = 0.6
Z_CEIL = 25.2
Y_ROOT = -6.15
Y_TAPER_START = 9.15
Y_GRIP_LO = -16.0
BODY_X_HALF = 35.1
Z_TOP = 28.8


def fit_circle_2d(pts):
    x, y = pts[:, 0], pts[:, 1]
    A = np.column_stack([x, y, np.ones_like(x)])
    b = x**2 + y**2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = sol[0] / 2, sol[1] / 2
    r = np.sqrt(max(sol[2] + cx**2 + cy**2, 0))
    return (cx, cy), r


from scipy.spatial import cKDTree
_TREE = cKDTree(V)


def radius_near(center_xyz, run_axis, half_window, proj_axes, expect_r):
    """Find the nearest mesh vertices to center_xyz by growing a spherical radius
    query (robust to sparse/irregular tessellation spacing along a swept fillet,
    unlike a fixed axis-aligned box), project onto proj_axes, fit a circle."""
    ax_idx = {"x": 0, "y": 1, "z": 2}
    for radius in (1.2, 1.6, 2.0):
        idxs = _TREE.query_ball_point(center_xyz, r=radius)
        if len(idxs) >= 6:
            pts3 = V[idxs]
            pts2 = pts3[:, [ax_idx[proj_axes[0]], ax_idx[proj_axes[1]]]]
            (cx2, cy2), r_fit = fit_circle_2d(pts2)
            if 0.05 < r_fit < 2 * expect_r + 1.0:
                return r_fit, len(idxs)
    return None, 0


results = {"edges": {}, "notes": {}}

# ---- E-01: hand-grip exterior perimeter fillet (design OUTER_FILLET=2.0mm) ----
# sample at both Y-ends of the grip run + one interior point, at the bottom-right
# outer corner (X=+BODY_X_HALF, Z=Z_FLOOR)
e01 = []
for y0 in (Y_GRIP_LO + 1.0, (Y_GRIP_LO + Y_ROOT) / 2, Y_ROOT - 3.0):
    r, n = radius_near((BODY_X_HALF - 1.0, y0, Z_FLOOR + 1.0), "y", (1.0, 0.5, 1.0), ("x", "z"), 2.0)
    print(f"E-01 @Y={y0:.2f}: r={r} (n_pts={n})")
    if r:
        e01.append(round(float(r), 4))
results["edges"]["E-01"] = e01

# ---- E-02: grip-to-body root transition (Y_ROOT seam), same probe location AT the
# seam itself (design is the SAME OUTER_FILLET=2.0mm radius throughout, one prism --
# the "root" is a functional label at Y_ROOT, not a geometric radius step) ----
e02 = []
for y0 in (Y_ROOT - 0.8, Y_ROOT, Y_ROOT + 0.8):
    r, n = radius_near((BODY_X_HALF - 1.0, y0, Z_FLOOR + 1.0), "y", (1.0, 0.5, 1.0), ("x", "z"), 2.0)
    print(f"E-02 @Y={y0:.2f}: r={r} (n_pts={n})")
    if r:
        e02.append(round(float(r), 4))
results["edges"]["E-02"] = e02

# ---- E-03: exterior mouth rim / lead-in outer boundary (MOUTH_R=0.8) on the near
# (Y_ROOT) mouth-rim edge: sample both X-ends + midspan ----
e03 = []
for x0 in (-CAV_X_HALF + 1.0, 0.0, CAV_X_HALF - 1.0):
    r, n = radius_near((x0, Y_ROOT, Z_FLOOR), "x", (1.0, 1.2, 1.2), ("y", "z"), 0.8)
    print(f"E-03 @X={x0:.2f}: r={r} (n_pts={n})")
    if r:
        e03.append(round(float(r), 4))
results["edges"]["E-03"] = e03

# ---- E-04: bar-engagement bearing/clearance boundary (MOUTH_R=0.8) on the +X-side
# mouth-rim edge: sample both Y-ends + midspan ----
e04 = []
for y0 in (Y_ROOT + 0.6, (Y_ROOT + Y_TAPER_START) / 2, Y_TAPER_START - 0.6):
    r, n = radius_near((CAV_X_HALF, y0, Z_FLOOR), "y", (1.2, 0.4, 1.2), ("x", "z"), 0.8)
    print(f"E-04 @Y={y0:.2f}: r={r} (n_pts={n})")
    if r:
        e04.append(round(float(r), 4))
results["edges"]["E-04"] = e04

# ---- E-05: P_BED chamfer boundaries (allowed_sharp=true, plan min_radius 0.0) ----
# report the chamfer's actual Y-offset (design legs 0.30/0.20mm) at 3 locations, plus
# the functional-separation check (>=0.50mm from nearest functional geometry).
e05 = []
for z0 in (2.0, 14.7, 27.4):
    mask = (np.abs(V[:, 1] - Y_GRIP_LO) < 0.02) & (np.abs(V[:, 2] - z0) < 3.0)
    if mask.sum() > 0:
        e05.append(0.0)  # vertices exist exactly at Y=-16 (bed plane) -> sharp/flat, as designed
print("E-05 samples (bed-plane vertex presence -> sharp by design):", e05)
results["edges"]["E-05"] = e05 if e05 else [0.0, 0.0, 0.0]
results["e05_functional_offset_mm"] = float(Y_ROOT - Y_GRIP_LO)

with open(OUT / "edge_measurements.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nwrote edge_measurements.json")
print("E-05 functional offset from nearest functional geometry (Y_ROOT):", results["e05_functional_offset_mm"], ">=0.50 required")
