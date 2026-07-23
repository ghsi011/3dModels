"""Phase-4 verification for knob_v4 — all checks on the EXPORTED STL where dimensional."""
import sys
import numpy as np
import trimesh
import cadquery as cq
from model import (body, lever, plate_h, bore_d, bore_depth, chan_env, rail_ch_w,
                   rail_ch_depth, btn_ch_w, btn_ch_depth, btn_ch_env, knob_h)

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name, detail)
    ok = ok and bool(cond)

# ---- 1. seated interference (OCC, exact) ----
inter = body.intersect(lever(0.0))
v = inter.val().Volume() if inter.val().Solids() else 0.0
check("1 seated interference ~0", abs(v) < 1e-6, f"{v:.6f} mm3")

# ---- 2. insertion sweep: knob raised by t, no interference at any travel ----
worst = 0.0
for t in np.arange(2.0, 70.0, 4.0):
    s = body.intersect(lever(float(t)))
    vv = s.val().Volume() if s.val().Solids() else 0.0
    worst = max(worst, abs(vv))
check("2 insertion sweep 2..68 clear", worst < 1e-6, f"worst {worst:.6f} mm3")

# ---- 3. section render (half cut, with lever seated) ----
half = cq.Workplane("XY").box(200, 200, 400, centered=(True, False, True))
sec = body.cut(half)
lv_sec = lever(0.0).cut(half)
cq.exporters.export(sec, "_check_section.stl", tolerance=0.02, angularTolerance=0.2)
cq.exporters.export(lv_sec, "_check_section_lever.stl", tolerance=0.02, angularTolerance=0.2)
print("     section exported (render separately)")

# ---- 5. feature positions/sizes measured on the EXPORTED STL ----
m = trimesh.load("knob_v4.stl")
m.apply_translation(-m.bounds[0] * [1, 1, 0] * 0)  # already z0 at bottom
def slice_at(z):
    sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    p, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1]))
    return p

def hole_dims(z):
    p = slice_at(z)
    if p is None:
        return None
    for poly in p.polygons_full:
        for h in poly.interiors:
            c = np.array(h.coords)
            mn, mx = c.min(0), c.max(0)
            yield (mx[0] - mn[0], mx[1] - mn[1])

# bore + both channel sets at z=20 (rail channels ±X, button channels ±Y)
d20 = list(hole_dims(20.0)) or []
big = max(d20, key=lambda d: d[0] * d[1]) if d20 else (0, 0)
check("5a z20 X-extent = rail env", abs(big[0] - chan_env) < 0.15, f"{big[0]:.2f} vs {chan_env}")
check("5b z20 Y-extent = button env", abs(big[1] - btn_ch_env) < 0.15, f"{big[1]:.2f} vs {btn_ch_env}")
# between rail-channel end (41.8) and button-channel end (48): Y still open to btn env
d45 = list(hole_dims(45.0)) or [(0, 0)]
g = max(d45, key=lambda d: d[0] * d[1])
check("5c z45 button channel open, rails closed",
      abs(g[1] - btn_ch_env) < 0.15 and g[0] < chan_env - 2.0,
      f"{g[0]:.2f}x{g[1]:.2f} (btn env {btn_ch_env})")
# above button channels (z=55): bore only
d55 = list(hole_dims(55.0)) or [(0, 0)]
b55 = max(d55, key=lambda d: d[0] * d[1])
check("5d z55 bore only", abs(b55[0] - bore_d) < 0.15 and abs(b55[1] - bore_d) < 0.15,
      f"{b55[0]:.2f}x{b55[1]:.2f} vs {bore_d}")
# bore top: solid at z just above bore_depth
p71 = slice_at(bore_depth + 0.5)
holes71 = [h for poly in (p71.polygons_full if p71 else []) for h in poly.interiors]
check("5e bore ends at bore_depth", len(holes71) == 0, f"depth {bore_depth:.1f}")

# ---- 6. measurement audit (every caliper number -> geometry) ----
audit = [
    ("12.9 shaft",        f"bore Ø{bore_d} (=12.9+2x0.15)"),
    ("16.7 rail env",     f"channel env Ø{chan_env} (=16.7+2x0.45)"),
    ("5.5 rail width",    f"rail channels {rail_ch_w} wide, depth {rail_ch_depth}"),
    ("72.1 rod exposed",  f"bore depth {bore_depth:.1f} = (72.1-4 plate)+2 headroom"),
    ("42.8 rail top",     f"rail channel depth {rail_ch_depth} = 38.8+3"),
    ("6.5 tip / 10 taper","clears Ø13.2 bore + 2mm headroom"),
    ("8.2 button",        f"button channels {btn_ch_w} wide, env Ø{btn_ch_env}, depth {btn_ch_depth}"),
    ("47.5 button z",     f"channel depth {btn_ch_depth} covers seated 43.5 +4.5 margin (±2 est. absorbed)"),
    ("4 plate seat",      "z=0 seat plane = plate top; knob bottoms on plate"),
]
for a, b in audit:
    print(f"     AUDIT {a:<18} -> {b}")

# ---- 7. printability (upside-down) + face audit ----
mi = m.copy()
mi.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
mi.apply_translation(-mi.bounds[0])
down = mi.face_normals[:, 2] < -np.cos(np.radians(30))
above = mi.triangles_center[:, 2] > 2.5
frac = mi.area_faces[down & above].sum() / mi.area_faces.sum()
check("7 overhang frac (inverted print) < 6%", frac < 0.06, f"{frac:.3f}")
check("7 watertight", m.is_watertight, "")
bb = m.bounds[1] - m.bounds[0]
check("7 bbox sane 46x46x~95", abs(bb[0] - 46) < 1.5 and abs(bb[2] - 95) < 1.5,
      np.round(bb, 1))
print("\nALL PASS" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
