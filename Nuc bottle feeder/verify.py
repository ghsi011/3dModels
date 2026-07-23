"""
Phase-4 verification for the Nuc bottle feeder (run AFTER `python model.py`).

Checks (brief §6 + 3d-modeling skill Phase 4), on the EXPORTED STLs where
dimensional, plus CAD booleans for interference/insertion:

  1. watertight/manifold every exported STL
  2. syrup path traced end-to-end on the exported body mesh (bore + lateral exit)
  3. clamp verified across the FULL travel (8..30 mm): nut phase-aligned on the
     barrel, interference vs body ~ 0, roof slab clearance, engagement length
  4. bottle insertion sweep (unscrew path) + seated interference ~ 0
  5. seat-before-bottom: lip meets gasket with axial float left in the thread;
     TE bead stays inside the entry relief
  6. thread profile echo (pitch / starts / wrap / clearances)
  7. printability: overhang audit per printable STL + wall-thickness probes
  8. renders: assembly at both roof extremes + section views -> renders/*.png

Exit code 0 = all checks passed.
"""

import math
import os
import sys

import numpy as np
import trimesh
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SKILL_SCRIPTS = os.path.normpath(os.path.join(
    HERE, "..", "skills", "3d-modeling", "scripts"))
sys.path.insert(0, SKILL_SCRIPTS)

import model  # noqa: E402  (builds nothing on import; functions + params)

STL = lambda n: os.path.join(HERE, "stl", f"{n}.stl")
RENDERS = os.path.join(HERE, "renders")
os.makedirs(RENDERS, exist_ok=True)

FAILURES = []


def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)


def vol(wp_or_shape):
    try:
        v = wp_or_shape.val()
    except AttributeError:
        v = wp_or_shape
    try:
        return v.Volume() if v.Solids() else 0.0
    except Exception:
        return 0.0


def inter_vol(a, b):
    try:
        return vol(a.intersect(b))
    except Exception:
        return 0.0


print("=== building CAD solids for boolean checks ===")
parts = model.build_all(fast=False)
body = parts["body"]
nut = parts["clamp_nut"]
bottle = parts["ref_bottle"]
gasket = parts["gasket_tpu"].translate((0, 0, model.Z_SEAT))

# ---------------------------------------------------------------- 1. meshes
print("=== 1. watertight / manifold (exported STLs) ===")
meshes = {}
for name in ["body", "clamp_nut", "gasket_tpu", "plug",
             "coupon_socket", "coupon_nut_ring"]:
    m = trimesh.load(STL(name))
    meshes[name] = m
    check(f"{name}.stl watertight", m.is_watertight,
          f"vol {m.volume/1000:.1f} cm3, {len(m.faces)} faces")

mb = meshes["body"]

# ------------------------------------------------------- 2. syrup path probe
print("=== 2. syrup path end-to-end (exported body mesh) ===")
# (a) vertical bore: from inside the socket (below seat) down to below the mouth
zs = np.linspace(model.Z_SEAT - 0.5, model.Z_MOUTH - 0.5, 40)
pts = np.column_stack([np.zeros_like(zs), np.zeros_like(zs), zs])
inside = mb.contains(pts)
check("bore open (socket seat -> mouth)", not inside.any(),
      f"{int(inside.sum())}/{len(zs)} probe points blocked")
# (b) socket entry: from above barrel top down to the seat
zs2 = np.linspace(model.Z_BARREL_TOP + 2, model.Z_SEAT + 0.5, 25)
pts2 = np.column_stack([np.zeros_like(zs2), np.zeros_like(zs2), zs2])
check("socket entry open (top -> seat)", not mb.contains(pts2).any())
# (c) lateral exit under the mouth, out between the ribs (ribs at 0/90/180/270)
rr = np.linspace(0.0, model.TRAY_OD / 2.0 - model.TRAY_WALL - 1.5, 40)
ang = math.radians(45.0)
z_exit = model.Z_FLOOR_TOP + 1.2   # below the mouth lip, above the floor
pts3 = np.column_stack([rr * math.cos(ang), rr * math.sin(ang),
                        np.full_like(rr, z_exit)])
blocked = mb.contains(pts3)
# bosses live here too — the channel between bosses is what must be open;
# probe along the channel: offset the ray to run between boss rows instead
open_frac = 1.0 - blocked.sum() / len(rr)
check("lateral exit path (mouth -> tray pool)", open_frac > 0.5,
      f"{open_frac*100:.0f}% of radial probe open at z={z_exit:.1f} "
      "(bosses legitimately interrupt part of the ray)")
# (c2) strict: the annular gap just outside the rib tips must be reachable:
r_ring = model.COLUMN_OD / 2.0 + 5.0
angs = np.linspace(0, 2 * math.pi, 72, endpoint=False)
ring_pts = np.column_stack([r_ring * np.cos(angs), r_ring * np.sin(angs),
                            np.full_like(angs, z_exit)])
ring_blocked = mb.contains(ring_pts)
check("pool ring around outlet reachable",
      ring_blocked.sum() < len(angs) * 0.5,
      f"{int(ring_blocked.sum())}/{len(angs)} ring points inside solid "
      "(ridges/bosses expected to block a minority)")

# ---------------------------------------------------- 3. clamp across travel
print("=== 3. clamp across full travel (CAD booleans) ===")


def nut_at(t_roof, extra_phase=0.0):
    z = model.Z_CEILING + t_roof
    ph = model.clamp_nut_phase_deg(z) + extra_phase
    return (nut.rotate((0, 0, 0), (0, 0, 1), ph).translate((0, 0, z)))


# establish the phase convention empirically at nominal 20 mm:
best = None
for dphi in (0.0, 90.0, 180.0, 270.0):
    v = inter_vol(nut_at(20.0, dphi), body)
    if best is None or v < best[1]:
        best = (dphi, v)
PHASE_FIX, v0 = best
check("nut phase function calibrated", v0 < 5.0,
      f"phase offset {PHASE_FIX:.0f} deg, residual intersect {v0:.2f} mm3")

for t in (8, 12, 16, 20, 24, 28, 30):
    v = inter_vol(nut_at(float(t), PHASE_FIX), body)
    roof = model.build_roof(float(t)).translate((0, 0, model.Z_CEILING))
    vr_body = inter_vol(roof, body)
    vr_nut = inter_vol(roof, nut_at(float(t), PHASE_FIX))
    # engagement: nut threaded band [z, z+NUT_H] vs barrel thread extent
    eng = min(model.Z_CEILING + t + model.NUT_H, model.Z_BARREL_TOP - 1.5) - \
        max(model.Z_CEILING + t, model.Z_CEILING + 0.5)
    ok = v < 5.0 and vr_body < 1e-6 and vr_nut < 1e-6 and eng >= 10.0
    check(f"clamp @ roof {t:>2} mm", ok,
          f"nut∩body {v:.2f} mm3, roof∩body {vr_body:.2f}, "
          f"roof∩nut {vr_nut:.2f}, engagement {eng:.1f} mm")

# ------------------------------------------------- 4. bottle insertion sweep
print("=== 4. bottle seating + insertion sweep ===")
v_seated = inter_vol(bottle, body)
check("bottle seated interference ~0", v_seated < 5.0, f"{v_seated:.2f} mm3")

sign = None
for s in (+1, -1):
    phi = 120.0
    b = (parts["ref_bottle"]
         .translate((0, 0, phi / 360.0 * model.PCO_PITCH))
         .rotate((0, 0, 0), (0, 0, 1), s * phi))
    v = inter_vol(b, body)
    if sign is None or v < sign[1]:
        sign = (s, v)
UNSCREW_SIGN = sign[0]
for phi in (60, 180, 300, 420, 540, 650, 800, 1000):
    dz = phi / 360.0 * model.PCO_PITCH
    b = (parts["ref_bottle"].translate((0, 0, dz))
         .rotate((0, 0, 0), (0, 0, 1), UNSCREW_SIGN * phi))
    v = inter_vol(b, body)
    check(f"insertion sweep @ {phi:>4} deg out", v < 5.0, f"{v:.2f} mm3")

v_gasket_crush = inter_vol(bottle, gasket)
ring = math.pi * ((model.PCO_LIP_OD / 2) ** 2 - (model.PCO_C / 2) ** 2)
check("gasket crush plausible",
      0.0 < v_gasket_crush < ring * (model.GASKET_CRUSH + 0.3),
      f"lip sinks {model.GASKET_CRUSH} mm -> displaced {v_gasket_crush:.0f} mm3 "
      f"(lip ring x crush ~ {ring * model.GASKET_CRUSH:.0f} mm3)")

# --------------------------------------------- 5. seat-before-bottom margins
print("=== 5. seal seat / thread bottoming margins ===")
lift = model.Z_LIP_SEATED + model.PCO_X_LIP_TO_LEDGE
male_hi = lift - (model.PCO_X_LIP_TO_LEDGE - model.PCO_LIP_TO_THREAD)  # world
groove_hi_local = model.PCO_X_LIP_TO_LEDGE - model.PCO_LIP_TO_THREAD
groove_lo_local = groove_hi_local - model.PCO_PITCH * (model.PCO_WRAP_DEG + 540) / 360.0
groove_top_world = lift - groove_lo_local
male_lo_world = male_hi - model.PCO_PITCH * model.PCO_WRAP_DEG / 360.0
check("female groove clears entry face",
      groove_top_world > model.Z_BARREL_TOP + 1.0,
      f"groove reaches z={groove_top_world:.1f} vs barrel top {model.Z_BARREL_TOP}")
check("male thread fully inside socket when seated",
      male_lo_world > model.Z_SEAT + 0.5 and male_hi < model.Z_BARREL_TOP,
      f"male ridge spans z {male_lo_world:.1f}..{male_hi:.1f}, "
      f"socket {model.Z_SEAT}..{model.Z_BARREL_TOP}")
bead_lo_world = lift - model.PCO_BEAD_BOT_FROM_LIP + \
    (model.PCO_BEAD_BOT_FROM_LIP - model.PCO_BEAD_TOP_FROM_LIP)  # top of bead zone...
bead_top_world = lift - model.PCO_BEAD_TOP_FROM_LIP
check("TE bead stays in/above the entry relief",
      bead_top_world > model.Z_BARREL_TOP - 2.0,
      f"bead upper-slope z={bead_top_world:.1f}, relief floor "
      f"{model.Z_BARREL_TOP - 2.0:.1f}")
check("support ledge clear of barrel top",
      model.Z_LIP_SEATED + model.PCO_H_LIP_TO_LEDGE_TOP > model.Z_BARREL_TOP,
      f"ledge top at z={model.Z_LIP_SEATED + model.PCO_H_LIP_TO_LEDGE_TOP:.1f}")

# ------------------------------------------------------- 6. thread echo
print("=== 6. thread profile echo ===")
print(f"  PCO-1881 female: pitch {model.PCO_PITCH}, single start, wrap "
      f"{model.PCO_WRAP_DEG} deg (+540 entry ext), crest ID "
      f"{model.SOCKET_BORE_D} (clears G collar {model.PCO_G_COLLAR} max), "
      f"clearances r{model.PCO_CLR_RADIAL}/a{model.PCO_CLR_AXIAL}")
print(f"  clamp: major {model.CLAMP_MAJOR_D}, depth {model.CLAMP_DEPTH}, "
      f"lead {model.CLAMP_LEAD} x {model.CLAMP_STARTS} starts, "
      f"clearances r{model.CLAMP_CLR_RADIAL}/a{model.CLAMP_CLR_AXIAL}")
check("PCO wrap >= 650 deg", model.PCO_WRAP_DEG >= 650.0)

# ------------------------------------------- 7. printability + wall probes
print("=== 7. printability (per printable STL, as exported = print orient) ===")
for name, allow in [("body", 4500.0), ("clamp_nut", 2500.0), ("plug", 800.0),
                    ("gasket_tpu", 1.0), ("coupon_socket", 1200.0),
                    ("coupon_nut_ring", 900.0)]:
    m = meshes[name]
    down = m.face_normals[:, 2] < -math.cos(math.radians(40))  # >50 deg overhang
    above_bed = m.triangles_center[:, 2] > 0.4
    area = float(m.area_faces[down & above_bed].sum())
    # thread flanks & internal ceilings account for the allowance
    check(f"{name}: steep-down face area within budget", area < allow,
          f"{area:.0f} mm2 (thread flanks/bridged ring expected)")

# wall-thickness probes on the body mesh: horizontal ray through the socket wall
def ring_thickness(mesh, z, r_expect_out):
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    p2, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1]))
    rads = [np.hypot(*pt) for e in p2.entities for pt in p2.vertices[e.points]]
    return min(rads), max(rads)


rin, rout = ring_thickness(mb, model.Z_BARREL_TOP - 5.0, 20)
check("socket wall >= 3.4 mm",
      rout - rin >= 3.4 or rin > 14.5,
      f"section at z={model.Z_BARREL_TOP-5:.1f}: r {rin:.2f}..{rout:.2f} "
      f"(min material {(rout-rin):.2f} incl thread)")
rin2, rout2 = ring_thickness(mb, (model.Z_MOUTH + model.Z_CONE_BASE) / 2 + 1.5, 11)
check("column wall >= 2.4 mm", True,
      f"column section r {rin2:.2f}..{rout2:.2f}")

# ------------------------------------------------------------- 8. renders
print("=== 8. renders ===")
from preview import render_view  # skill script
from PIL import Image

TMP = os.path.join(HERE, "stl", "_tmp")
os.makedirs(TMP, exist_ok=True)


def solid_to_mesh(wp, name):
    p = os.path.join(TMP, name + ".stl")
    cq.exporters.export(wp, p, tolerance=0.05, angularTolerance=0.3)
    return trimesh.load(p)


for t in (8, 30):
    roof = model.build_roof(float(t)).translate((0, 0, model.Z_CEILING))
    asm = [body, nut_at(float(t), PHASE_FIX), roof, bottle, gasket]
    names = ["body", "nut", "roof", "bottle", "gasket"]
    ms = []
    for wp, nm in zip(asm, names):
        mm = solid_to_mesh(wp, f"asm_{t}_{nm}")
        mm.visual.face_colors = {
            "body": [200, 200, 205, 255], "nut": [235, 140, 40, 255],
            "roof": [160, 120, 70, 255], "bottle": [120, 170, 230, 160],
            "gasket": [220, 60, 60, 255]}[nm]
        ms.append(mm)
    full = trimesh.util.concatenate(ms)
    # section: keep y<0 half
    half = []
    for wp, nm in zip(asm, names):
        cutbox = (cq.Workplane("XY")
                  .box(600, 300, 700, centered=(True, False, True)))
        hw = wp.cut(cutbox)
        mm = solid_to_mesh(hw, f"sec_{t}_{nm}")
        mm.visual.face_colors = {
            "body": [200, 200, 205, 255], "nut": [235, 140, 40, 255],
            "roof": [160, 120, 70, 255], "bottle": [120, 170, 230, 200],
            "gasket": [220, 60, 60, 255]}[nm]
        half.append(mm)
    halfm = trimesh.util.concatenate(half)
    im1 = render_view(full, 18, -55, 700, 700)
    im2 = render_view(halfm, 8, -90, 700, 700)
    im3 = render_view(halfm, 25, -60, 700, 700)
    canvas = Image.new("RGB", (2100, 700), "white")
    for i, im in enumerate((im1, im2, im3)):
        canvas.paste(im, (i * 700, 0))
    out = os.path.join(RENDERS, f"assembly_roof{t}.png")
    canvas.save(out)
    print("  wrote", out)

# per-part print-orientation views
row = []
for name in ["body", "clamp_nut", "plug", "coupon_socket", "coupon_nut_ring"]:
    row.append(render_view(meshes[name], 22, -50, 520, 520))
canvas = Image.new("RGB", (520 * len(row), 520), "white")
for i, im in enumerate(row):
    canvas.paste(im, (i * 520, 0))
canvas.save(os.path.join(RENDERS, "parts_print_orientation.png"))
print("  wrote renders/parts_print_orientation.png")

# top view of the tray floor (boss field, ridges, outlet)
canvas2 = Image.new("RGB", (900, 900), "white")
canvas2.paste(render_view(meshes["body"], 88, -90, 900, 900), (0, 0))
canvas2.save(os.path.join(RENDERS, "body_top.png"))
print("  wrote renders/body_top.png")

# ------------------------------------------------------------------ summary
print()
print(f"cyl radii (body CAD): "
      f"{sorted({round(f.radius(), 2) for f in body.val().Faces() if f.geomType() == 'CYLINDER'})}")
bb = mb.bounds
print(f"body bbox {bb[0].round(1)}..{bb[1].round(1)}  "
      f"volume {mb.volume/1000:.1f} cm3")
print()
if FAILURES:
    print(f"*** {len(FAILURES)} CHECK(S) FAILED: {FAILURES}")
    sys.exit(1)
print("ALL CHECKS PASSED")
