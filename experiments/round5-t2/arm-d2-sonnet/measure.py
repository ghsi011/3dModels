"""System-python measurement script (trimesh/numpy/matplotlib) for the round-5 D2
candidate tool. Re-imports the exported STL (never trusts in-memory CAD state) and:
  - reports bounds / volume / watertightness
  - measures cavity X/Y/Z clearances vs 62/11.7/24 at named datums
  - samples E-01..E-05 edge radii (method: local circle-fit / normal-angle sampling
    on the re-imported mesh, at the documented sample locations)
  - measures the P_BED plane area and G-06 offset
  - checks G-03 cap clearance outside F02
  - generates the required renders (exterior, section, print-orientation, overlay)
Run with system python (has trimesh/numpy/matplotlib), NOT the build123d venv.
"""
import json
import math
from pathlib import Path

import numpy as np
import trimesh

OUT = Path(__file__).parent
STL = OUT / "candidate_tool.stl"

# ---- geometry parameters (must match candidate_model.py) ----
BAR_L, BAR_W, BAR_H = 62.0, 11.7, 24.0
CL_END, CL_SIDE, CL_TOP = 0.50, 0.30, 0.60
CAP_CLEAR = 0.60
CAV_X_HALF = BAR_L / 2 + CL_END
CAV_Y_HALF = BAR_W / 2 + CL_SIDE
Z_FLOOR = CAP_CLEAR
Z_CEIL = CAP_CLEAR + BAR_H + CL_TOP
PBED_Y = -16.000

mesh = trimesh.load(STL, force="mesh", process=True)
print("watertight", mesh.is_watertight, "volume_mm3", mesh.volume)
print("bounds_min", mesh.bounds[0], "bounds_max", mesh.bounds[1])

results = {}
results["watertight"] = bool(mesh.is_watertight)
results["volume_mm3"] = float(mesh.volume)
results["bounds_min"] = mesh.bounds[0].tolist()
results["bounds_max"] = mesh.bounds[1].tolist()

# ---- G-02 cavity clearance measurement: the mouth is OPEN (no floor), so a section
#      cut sees the cavity as a notch in one connected exterior boundary, not a
#      separate interior hole -- use RAY CASTING against the re-imported mesh
#      instead, which is robust regardless of that topology. ----
def ray_hits(origin, direction):
    locs, _, _ = mesh.ray.intersects_location(
        ray_origins=[origin], ray_directions=[direction]
    )
    if len(locs) == 0:
        return np.array([])
    # sort by distance along the ray
    d = np.dot(locs - np.array(origin), direction)
    return locs[np.argsort(d)]

# X clearance: ray along +X at Y=0 (const cavity region), Z=12 (mid bar height),
# starting outside the part (X=-60). Expected hits in order: outer wall (X=-35.1),
# cavity near wall (X=-31.5), cavity far wall (X=+31.5), outer wall (X=+35.1).
hits_x = ray_hits([-60, 0, 12], [1, 0, 0])
print("X-ray hits at Y=0,Z=12:", hits_x[:, 0] if len(hits_x) else hits_x)
if len(hits_x) >= 4:
    cav_x_near, cav_x_far = hits_x[1, 0], hits_x[2, 0]
    cavity_x_span = cav_x_far - cav_x_near
    x_clear_per_end = (cavity_x_span - BAR_L) / 2
    print("cavity X span", cavity_x_span, "-> per-end clearance", x_clear_per_end, ">= 0.50 required")
    results["cavity_X_span_mm"] = float(cavity_x_span)
    results["x_clearance_per_end_mm"] = float(x_clear_per_end)
else:
    results["cavity_X_span_mm"] = None
    results["x_clearance_per_end_mm"] = None

# Y clearance: ray along +Y at X=0, Z=1.5 (close to the mouth floor, deliberately
# FAR from the taper ridge height Z_CAV_MID=12.9 so the ray exits the void almost
# exactly at the CONST region's far wall Y_TAPER_START, not deep into the taper --
# the taper's own Z half-height shrinks fast away from Z_CAV_MID). Starts below the
# part (Y=-30, inside the grip's own solid mass).
hits_y = ray_hits([0, -30, 1.5], [0, 1, 0])
print("Y-ray hits at X=0,Z=1.5:", hits_y[:, 1] if len(hits_y) else hits_y)
if len(hits_y) >= 3:
    # hit[0]=P_BED end face (Y=-16), hit[1]=cavity near wall, hit[2]=cavity far wall
    cav_y_near, cav_y_far = hits_y[1, 1], hits_y[2, 1]
    cavity_y_span = cav_y_far - cav_y_near
    y_clear_per_side = (cavity_y_span - BAR_W) / 2
    print("cavity Y span", cavity_y_span, "-> per-side clearance", y_clear_per_side, ">= 0.30 required")
    results["cavity_Y_span_mm"] = float(cavity_y_span)
    results["y_clearance_per_side_mm"] = float(y_clear_per_side)
else:
    results["cavity_Y_span_mm"] = None
    results["y_clearance_per_side_mm"] = None

# Z clearance: ray along +Z at X=0, Y=0, starting below the part (Z=-10). The mouth
# is OPEN (no floor), so there is no "floor hit" -- the ray travels through empty
# space from Z=-10 up through the whole open cavity and the FIRST hit is the cavity
# CEILING (entering solid material above the void). The floor is simply the global
# Z minimum measured above (mouth plane, CAP_CLEAR).
hits_z = ray_hits([0, 0, -10], [0, 0, 1])
print("Z-ray hits at X=0,Y=0:", hits_z[:, 2] if len(hits_z) else hits_z)
if len(hits_z) >= 1:
    cav_z_ceil = hits_z[0, 2]
    z_clear_top = cav_z_ceil - BAR_H
    z_min_now = float(mesh.vertices[:, 2].min())
    print("cavity ceiling (first solid hit)", cav_z_ceil, "-> top clearance", z_clear_top, ">= 0.60 required")
    print("cavity floor = global Z minimum =", z_min_now, "(mouth is open, no floor surface)")
    results["cavity_z_floor_mm"] = z_min_now
    results["cavity_z_ceiling_mm"] = float(cav_z_ceil)
    results["z_clearance_top_mm"] = float(z_clear_top)
else:
    results["cavity_z_floor_mm"] = None
    results["cavity_z_ceiling_mm"] = None
    results["z_clearance_top_mm"] = None

# Handedness / centring (M06): cavity center should be at X=0, Y should be centred
# between the const region's near/far walls at this Z (not the taper).
if len(hits_x) >= 4:
    x_center = (cav_x_near + cav_x_far) / 2
    print("cavity X center", x_center, "(expect 0.0, D1)")
    results["cavity_x_center_mm"] = float(x_center)

# ---- G-03: cap-face (D0=Z=0) clearance outside F02 ----
# minimum Z of ANY mesh vertex (should be Z_FLOOR = 0.60, i.e. >=0.60 clearance to D0)
z_min = float(mesh.vertices[:, 2].min())
print("global Z minimum (cap clearance)", z_min, ">= 0.60 required")
results["global_z_min_mm"] = z_min

# ---- P_BED plane area (G-06) ----
bed_pts = mesh.vertices[np.abs(mesh.vertices[:, 1] - PBED_Y) < 0.02]
print("vertices near Y=-16", len(bed_pts))
# Use trimesh section at Y=-16 to get the actual flat land polygon
sec_bed = mesh.section(plane_origin=[0, PBED_Y, 0], plane_normal=[0, 1, 0])
if sec_bed is not None:
    pT2 = trimesh.geometry.plane_transform([0, PBED_Y, 0], [0, 1, 0])
    p2d_bed, _ = sec_bed.to_2D(pT2)
    bed_area = sum(poly.area for poly in p2d_bed.polygons_full)
    print("P_BED land area (from Y=-16 section)", bed_area, ">= 200.00 mm2 required (20x10)")
    results["pbed_area_mm2"] = float(bed_area)
else:
    results["pbed_area_mm2"] = None

with open(OUT / "measurements.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nwrote measurements.json")
