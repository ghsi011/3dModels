"""
measure_receipt.py -- re-import watch_reference.stl (trimesh; CadQuery has no
importSTL) and produce the measurement receipt for reference_manifest.md.
Run-once helper, not a primary deliverable itself.
"""
import numpy as np
import trimesh

m = trimesh.load("watch_reference.stl")
print("watertight:", m.is_watertight)
print("volume mm3: %.2f" % m.volume)
b = m.bounds
print("bounds x: [%.3f, %.3f]" % (b[0][0], b[1][0]))
print("bounds y: [%.3f, %.3f]" % (b[0][1], b[1][1]))
print("bounds z: [%.3f, %.3f]" % (b[0][2], b[1][2]))
print("extents (x,y,z):", np.round(m.extents, 3))

# ---- case diameter check: slice well clear of the button bosses/band stubs (Z=7.45, mid-height) ----
Z_SLICE = 7.45
sec = m.section(plane_origin=[0, 0, Z_SLICE], plane_normal=[0, 0, 1])
loops = sec.discrete
# at mid-height the button bosses ARE present (their Z-band spans 2.235-12.665), so the
# widest loop here is the case+button envelope, not the bare case -- report both by also
# slicing at a Z clear of the button pad band (Z=1.0, below BUTTON_PAD_Z_LO_FRAC*14.9=2.235)
print("\ncase-only diameter check (Z=1.0 slice, clear of button pads and band stubs):")
sec_bare = m.section(plane_origin=[0, 0, 1.0], plane_normal=[0, 0, 1])
loop_bare = max(sec_bare.discrete, key=len)
p_bare = loop_bare[:, :2]
dia_x = p_bare[:, 0].max() - p_bare[:, 0].min()
dia_y = p_bare[:, 1].max() - p_bare[:, 1].min()
print("  x-extent (button axis) %.3f mm (param CASE_DIA_BUTTON_AXIS=51.75)" % dia_x)
print("  y-extent (band axis)   %.3f mm (param CASE_DIA_BAND_AXIS=51.75)" % dia_y)

print("\nbutton-envelope diameter check (Z=%.2f slice, mid-height, through button pads):" % Z_SLICE)
loop_env = max(loops, key=len)
p_env = loop_env[:, :2]
dia_x_env = p_env[:, 0].max() - p_env[:, 0].min()
print("  x-extent (button axis, through pads) %.3f mm (param BUTTON_ENVELOPE_DIA=56.8)" % dia_x_env)

print("\ncase thickness check (overall Z extent): %.3f mm (param CASE_THICKNESS=14.9)" % m.extents[2])

# ---- band width check: slice through a band stub, well beyond the bare case radius ----
print("\nband-stub width check (Y=case_r+5=30.875 slice plane, normal +Y):")
sec_band = m.section(plane_origin=[0, 30.875, 0], plane_normal=[0, 1, 0])
if sec_band is not None:
    loop_band = max(sec_band.discrete, key=len)
    p_band = loop_band[:, [0, 2]]  # X, Z at this Y
    band_w = p_band[:, 0].max() - p_band[:, 0].min()
    print("  x-extent at the +Y band stub: %.3f mm (param BAND_WIDTH=26.0)" % band_w)
else:
    print("  no section (unexpected)")

print("\ncaseback flatness check: min Z over whole mesh should be exactly 0.000 (no charge-pad cuts/bumps):")
print("  min Z = %.6f mm" % m.bounds[0][2])
