"""
measure_receipt.py — re-import phone_reference.stl (trimesh; CadQuery has no
importSTL) and produce the measurement receipt for reference_manifest.md.
Run-once helper, not a deliverable itself.
"""
import math
import numpy as np
import trimesh

m = trimesh.load("phone_reference.stl")
print("watertight:", m.is_watertight)
print("volume mm3: %.2f" % m.volume)
b = m.bounds
print("bounds x: [%.3f, %.3f]" % (b[0][0], b[1][0]))
print("bounds y: [%.3f, %.3f]" % (b[0][1], b[1][1]))
print("bounds z: [%.3f, %.3f]" % (b[0][2], b[1][2]))
print("extents (x,y,z):", np.round(m.extents, 3))
print("overall thickness incl. camera bump (z extent): %.3f mm" % m.extents[2])

# ---- corner radius check: slice at a flat-body height (Z=4, clear of camera bar) ----
Z_SLICE = 4.0
sec = m.section(plane_origin=[0, 0, Z_SLICE], plane_normal=[0, 0, 1])
loop = max(sec.discrete, key=len)  # global 3D coords, outer loop
pts = loop[:, :2]  # X,Y

W, L = 73.2, 155.6
corner_xy = np.array([W / 2, L / 2])  # sharp top-right corner (D4_RIGHT / D2_TOP)
d = np.linalg.norm(pts - corner_xy, axis=1)
d_min = d.min()
R_est = d_min * (math.sqrt(2) + 1)
print("\ncorner-radius check (Z=%.1f slice, top-right D4_RIGHT/D2_TOP corner):" % Z_SLICE)
print("  min distance from sharp corner to boundary: %.4f mm" % d_min)
print("  implied fillet radius: %.3f mm (parameter R_CORNER=9.5)" % R_est)

# footprint at this slice (should be W x L minus corner cuts)
print("  slice bbox: x[%.3f,%.3f] y[%.3f,%.3f]" %
      (pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()))

# ---- camera-bar footprint: slice just below the back plane (Z=-1) ----
sec2 = m.section(plane_origin=[0, 0, -1.0], plane_normal=[0, 0, 1])
if sec2 is not None:
    loop2 = max(sec2.discrete, key=len)
    p2 = loop2[:, :2]
    print("\ncamera-bar footprint (Z=-1.0 slice):")
    print("  x[%.3f,%.3f] (width %.3f, param CAM_BAR_WIDTH=73.2)" %
          (p2[:, 0].min(), p2[:, 0].max(), p2[:, 0].max() - p2[:, 0].min()))
    print("  y[%.3f,%.3f] (top edge should be 77.8=D2_TOP)" % (p2[:, 1].min(), p2[:, 1].max()))
else:
    print("\ncamera-bar footprint (Z=-1.0 slice): no section (unexpected)")

# ---- deepest point (camera bump peak) ----
print("\ncamera-bump peak Z (min Z overall): %.3f mm (param CAM_BUMP_PROTRUSION=2.74 -> expect -2.74)"
      % m.bounds[0][2])

# ---- button pad positions (X=+37.2 face capsules) : slice at Z=T/2=4.35 across full Y ----
sec3 = m.section(plane_origin=[0, 0, 4.35], plane_normal=[0, 0, 1])
loop3 = max(sec3.discrete, key=len)
p3 = loop3[:, :2]
right_pts = p3[p3[:, 0] > 36.9]  # points on the protruding button pads (body face is X=36.6)
if len(right_pts):
    ys = np.sort(right_pts[:, 1])
    # cluster into contiguous groups (gap > 1mm starts a new button)
    groups = []
    cur = [ys[0]]
    for y in ys[1:]:
        if y - cur[-1] > 1.0:
            groups.append(cur)
            cur = [y]
        else:
            cur.append(y)
    groups.append(cur)
    print("\nbutton pad Y-clusters at X>36.9 (Z=4.35 slice):")
    for g in groups:
        print("  Y range [%.2f, %.2f], center %.2f, length %.2f" %
              (min(g), max(g), (min(g) + max(g)) / 2, max(g) - min(g)))
    print("  expected: volume rocker center 45.8 len 16; power button center 27.8 len 10")
