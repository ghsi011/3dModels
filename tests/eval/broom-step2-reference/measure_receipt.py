"""
measure_receipt.py -- re-import stick_reference.stl (trimesh; CadQuery has
no importSTL) and produce the measurement receipt for reference_manifest.md.
Run-once helper, not a primary deliverable itself.
"""
import numpy as np
import trimesh

m = trimesh.load("stick_reference.stl")
print("watertight:", m.is_watertight)
print("volume mm3: %.2f" % m.volume)
b = m.bounds
print("bounds x: [%.3f, %.3f]" % (b[0][0], b[1][0]))
print("bounds y: [%.3f, %.3f]" % (b[0][1], b[1][1]))
print("bounds z: [%.3f, %.3f]" % (b[0][2], b[1][2]))
print("extents (x,y,z):", np.round(m.extents, 3))

# ---- diameter check: slice mid-shaft (clear of both end faces) ----
Z_SLICE = 75.0
sec = m.section(plane_origin=[0, 0, Z_SLICE], plane_normal=[0, 0, 1])
loop = max(sec.discrete, key=len)
p = loop[:, :2]
dia_x = p[:, 0].max() - p[:, 0].min()
dia_y = p[:, 1].max() - p[:, 1].min()
print("\nmid-shaft diameter check (Z=%.1f slice):" % Z_SLICE)
print("  x-extent %.4f mm (param STICK_DIAMETER=30.0, sheet M-001)" % dia_x)
print("  y-extent %.4f mm (param STICK_DIAMETER=30.0, sheet M-001)" % dia_y)

print("\nlength check (overall Z extent): %.4f mm (param STICK_LENGTH=150.0, ASSUMPTION)" % m.extents[2])

# ---- roundness spot-check: radial deviation of the mid-shaft loop from a perfect circle ----
center = p.mean(axis=0)
radii = np.linalg.norm(p - center, axis=1)
print("\nroundness check (mid-shaft loop radii): min=%.4f max=%.4f mean=%.4f mm (nominal R=15.0)"
      % (radii.min(), radii.max(), radii.mean()))
