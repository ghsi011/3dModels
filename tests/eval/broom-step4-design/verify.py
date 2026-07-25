"""
verify.py -- DESIGNER SELF-CHECK, NON-ACCEPTANCE.

Re-imports clip.stl (trimesh, not the in-memory CadQuery solid) and runs the
Phase-4-style checks from cadquery-patterns.md against the accepted rod
(tests/eval/broom-step2-reference/stick_reference.stl geometry, reproduced
locally by radius/length -- see note below) plus this commission's own
print_plan_checks.json numbers. This is designer evidence for
candidate_readiness.md -- it is never acceptance and never substitutes for a
fresh, independent verifier pass.

Note on the reference rod: this script builds a plain Ø30.0mm cylinder locally
(matching stick_reference.py's own parametrization exactly: true circle,
constant diameter, ROD_R=15.0) rather than re-loading stick_reference.stl,
because the exported reference STL is 150mm long with its own axis origin and
this script needs the rod repositioned/swept along X and centered on the
clip's own local axis for the snap-through sweep -- same nominal geometry,
just re-expressed in the clip's coordinate frame for these checks.
"""
import hashlib
import json
import math

import numpy as np
import trimesh

# ==== constants mirrored from clip_model.py (kept in sync manually; both files
# cite the same commission parameters) ====
ROD_D = 30.0
ROD_R = ROD_D / 2.0
FIN_TIP_ID = 29.2
FIN_TIP_R = FIN_TIP_ID / 2.0
RING_OD_R = FIN_TIP_R + 2.4
CLIP_WIDTH = 24.0
WRAP_DEG = 210.0
MOUTH_HALF_DEG = (360.0 - WRAP_DEG) / 2.0
E01_MIN_R = 0.8  # plan floor ("Comfort radius >=0.8mm on exposed hand-contact edges")
E02_MIN_R, E02_MAX_R = 0.2, 0.4  # fdm-design.md elephant-foot band
G_MIN_WALL = 1.2  # plan floor ("wall >=1.2mm")
I1_MIN_DIAMETRAL, I1_MAX_DIAMETRAL = -1.0, -0.6  # accepted-plan interference band


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rod_cylinder(z_lo, z_hi, x=0.0, y=0.0, sections=128):
    rod = trimesh.creation.cylinder(radius=ROD_R, height=(z_hi - z_lo), sections=sections)
    # trimesh cylinder is centered at origin along Z by default; move to [z_lo, z_hi]
    rod.apply_translation((0, 0, (z_hi + z_lo) / 2.0))
    rod.apply_translation((x, y, 0))
    return rod


def circle_fit(points_2d):
    """Algebraic (Kasa) least-squares circle fit. Returns (cx, cy, r)."""
    x = points_2d[:, 0]
    y = points_2d[:, 1]
    A = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    b = x**2 + y**2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy, c = sol
    r = math.sqrt(c + cx**2 + cy**2)
    return cx, cy, r


def nearest_boundary_points(loop_xy, target_xy, n):
    """Return the n points of loop_xy (Mx2) nearest to target_xy."""
    d = np.linalg.norm(loop_xy - np.array(target_xy), axis=1)
    idx = np.argsort(d)[:n]
    return loop_xy[idx]


def section_loop_xy(mesh, z):
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    planar, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1]))
    loops = []
    for entity_points in planar.discrete:
        loops.append(np.asarray(entity_points))
    return loops


def largest_loop(loops):
    return max(loops, key=lambda p: p.shape[0])


def load_repaired(path):
    """Load + repair exactly like skills/3d-modeling/scripts/mesh_io.py's
    load_mesh(): drop OCC's zero-area tessellation-pole triangles FIRST, then
    merge coincident vertices. Order matters -- merge_vertices() alone does not
    fix the spurious extra "components" these degenerate slivers otherwise
    cause; confirmed directly (plain trimesh.load: watertight=False,
    components=5; same repair order as mesh_io.load_mesh: watertight=True,
    components=1). This is a known, documented tessellator artifact, not a
    real topology defect -- see mesh_io.py's own module docstring."""
    tm = trimesh.load(path, force="mesh")
    tm.update_faces(tm.nondegenerate_faces())
    tm.merge_vertices()
    return tm


def main():
    results = {}

    clip = load_repaired("clip.stl")

    # ---- 0. integrity ----
    results["clip_watertight"] = bool(clip.is_watertight)
    results["clip_volume_mm3"] = float(clip.volume)
    results["clip_bounds"] = clip.bounds.tolist()
    results["clip_components"] = len(clip.split(only_watertight=False))
    print("0. integrity:", json.dumps({k: results[k] for k in
          ("clip_watertight", "clip_volume_mm3", "clip_bounds", "clip_components")}, indent=2))

    # ---- 1. seated interference (rigid boolean, rod concentric with the ring axis --
    #          the INSTALLED state). This interface is an INTENDED interference/retention
    #          fit (I-1) -- a nonzero geometric overlap here is the fit working as designed,
    #          not a defect; 0-collision does not apply, per the accepted print plan. ----
    rod_seated = rod_cylinder(-18.0, 42.0)  # generously overlaps the clip's Z=[0,24] band
    inter = trimesh.boolean.intersection([clip, rod_seated], engine="manifold")
    seated_interference_mm3 = float(inter.volume) if len(inter.faces) else 0.0
    results["seated_interference_mm3"] = seated_interference_mm3
    print(f"1. seated interference (rod concentric, rigid boolean): "
          f"{seated_interference_mm3:.4f} mm3 -- INTENDED per I-1 (compliant retention), "
          f"not a defect")

    # ---- 2. snap-through sweep: rod approaches along -X (through the mouth) from clear
    #          of the part down to the seated (concentric) position. Adapts the classic
    #          axial "insertion/travel sweep" check to this interface's actual motion path
    #          (radial snap through the open mouth, per I-1's motion_path), rather than an
    #          axial slide -- there is no axial insertion for a C-clip. ----
    sweep = []
    for x in (60, 45, 30, 22, 18, 15, 12, 10, 8, 6, 4, 2, 0):
        rod_t = rod_cylinder(-18.0, 42.0, x=x)
        inter_t = trimesh.boolean.intersection([clip, rod_t], engine="manifold")
        v = float(inter_t.volume) if len(inter_t.faces) else 0.0
        sweep.append({"rod_center_x_mm": x, "interference_mm3": v})
        print(f"   x={x:+3d} mm  interference={v:.4f} mm3")
    results["snap_through_sweep"] = sweep

    # ---- 3/4. section + exterior renders produced separately (render_clip.py) ----
    print("3/4. section + exterior + print-orientation renders: see render_clip.py outputs")

    # ---- 5. fin-tip ID re-measurement (mid-height section, clear of top-rim/bed-chamfer
    #          fillet zones) ----
    z_mid = CLIP_WIDTH / 2.0
    loops = section_loop_xy(clip, z_mid)
    loop = largest_loop(loops)
    center = np.array([0.0, 0.0])
    radii = np.linalg.norm(loop - center, axis=1)
    angles = np.degrees(np.arctan2(loop[:, 1], loop[:, 0])) % 360.0
    # inner-wall band: angles well inside the wrap, away from both tip-fillet zones
    inner_band = (angles > (MOUTH_HALF_DEG + 12)) & (angles < (360 - MOUTH_HALF_DEG - 12))
    inner_radii = radii[inner_band & (radii < (FIN_TIP_R + 1.0))]
    results["fin_tip_radius_min_mm"] = float(inner_radii.min())
    results["fin_tip_radius_max_mm"] = float(inner_radii.max())
    results["fin_tip_radius_mean_mm"] = float(inner_radii.mean())
    results["fin_tip_id_mean_mm"] = float(inner_radii.mean() * 2)
    results["diametral_interference_vs_rod_mm"] = float(inner_radii.mean() * 2 - ROD_D)
    print(f"5. fin-tip ID @ z={z_mid}mm: mean={inner_radii.mean()*2:.4f}mm "
          f"(min {inner_radii.min()*2:.4f} / max {inner_radii.max()*2:.4f}); "
          f"diametral interference vs ROD_D={inner_radii.mean()*2 - ROD_D:.4f}mm "
          f"(accepted band [{I1_MIN_DIAMETRAL}, {I1_MAX_DIAMETRAL}]mm)")

    # mouth chord between the two fin tips at this same section: nearest actual
    # boundary point to each tip's theoretical (pre-fillet) ID corner.
    tip_a_theory = np.array([FIN_TIP_R * math.cos(math.radians(MOUTH_HALF_DEG)),
                              FIN_TIP_R * math.sin(math.radians(MOUTH_HALF_DEG))])
    tip_b_theory = np.array([FIN_TIP_R * math.cos(math.radians(360 - MOUTH_HALF_DEG)),
                              FIN_TIP_R * math.sin(math.radians(360 - MOUTH_HALF_DEG))])
    tip_a = loop[np.argmin(np.linalg.norm(loop - tip_a_theory, axis=1))]
    tip_b = loop[np.argmin(np.linalg.norm(loop - tip_b_theory, axis=1))]
    mouth_chord = float(np.linalg.norm(tip_a - tip_b))
    results["mouth_chord_mm"] = mouth_chord
    print(f"   mouth chord between fin tips (nearest-actual-point method): "
          f"{mouth_chord:.4f}mm (< {ROD_D}mm forces elastic entry)")

    # ---- 6. wall-thickness ray-cast (whole part) ----
    np.random.seed(0)
    samples, face_idx = trimesh.sample.sample_surface_even(clip, 4000)
    normals = clip.face_normals[face_idx]
    eps = 0.02
    origins = samples - normals * eps
    locations, ray_idx, _ = clip.ray.intersects_location(
        ray_origins=origins, ray_directions=-normals, multiple_hits=False
    )
    if len(locations):
        dists = np.linalg.norm(locations - samples[ray_idx], axis=1)
        valid = dists > 2 * eps
        min_wall = float(dists[valid].min()) if valid.any() else float("nan")
        min_wall_idx = np.argmin(np.where(valid, dists, np.inf))
    else:
        min_wall = float("nan")
    results["min_wall_thickness_mm"] = min_wall
    print(f"6. wall-thickness ray-cast (4000 samples): min={min_wall:.4f}mm "
          f"(plan floor {G_MIN_WALL}mm)")

    # ---- 7. E-01 comfort-fillet radius measurement: 4 tip corners (OD+ID x 2 tips),
    #          analytic fillet-arc-center method (cadquery-patterns.md / precedent style):
    #          for a convex corner between a radial flat face (at angle A) and a circular
    #          arc face (radius R, centered at the origin), the fillet-of-radius-r arc
    #          center sits at radius (R-r) [OD corner; (R+r) for an ID/concave corner] and
    #          angle A + asin(r/(R-r)) (offset INTO the material). Sample mesh boundary
    #          points near that theoretical corner and fit a circle; compare its radius to
    #          the E01_MIN_R floor. ----
    z_edge = CLIP_WIDTH / 2.0  # same clear mid-height section as the fin-tip measurement
    loop_e = largest_loop(section_loop_xy(clip, z_edge))
    ang_e = np.degrees(np.arctan2(loop_e[:, 1], loop_e[:, 0])) % 360.0
    rad_e = np.linalg.norm(loop_e, axis=1)

    def measure_tip_fillet(tip_angle_deg, side, r_guess):
        # side: "OD" (convex, R=RING_OD_R) or "ID" (convex from inside the wedge too --
        # the tip's ID corner is ALSO convex/exterior material corner in this design,
        # same sign convention as the OD corner)
        R = RING_OD_R if side == "OD" else FIN_TIP_R
        # offset direction into material: for the "start" tip (~75deg) material is at
        # angle > tip_angle_deg; for the "end" tip (~285deg) material is at angle <
        # tip_angle_deg (going the short way through 360/0 is NOT material -- the wrap
        # covers 75..285 the LONG way through 180).
        sign = +1 if abs(tip_angle_deg - MOUTH_HALF_DEG) < 1 else -1
        theta_c = tip_angle_deg + sign * math.degrees(math.asin(min(0.999, r_guess / R)))
        Rc = R - r_guess
        center_xy = np.array([Rc * math.cos(math.radians(theta_c)),
                               Rc * math.sin(math.radians(theta_c))])
        pts = nearest_boundary_points(loop_e, center_xy, 6)
        cx, cy, r_fit = circle_fit(pts)
        # also report the simple distance-from-theoretical-center spread as a cross-check
        dists = np.linalg.norm(pts - center_xy, axis=1)
        return r_fit, float(dists.min()), float(dists.max())

    e01_samples = []
    tip_start = MOUTH_HALF_DEG
    tip_end = 360 - MOUTH_HALF_DEG
    for tip_angle, tip_label in ((tip_start, "start"), (tip_end, "end")):
        for side in ("OD", "ID"):
            r_fit, dmin, dmax = measure_tip_fillet(tip_angle, side, E01_MIN_R + 0.1)
            e01_samples.append({
                "tip": tip_label, "side": side,
                "fitted_radius_mm": r_fit,
                "center_distance_range_mm": [dmin, dmax],
            })
            print(f"7. E-01 tip={tip_label} side={side}: fitted radius {r_fit:.4f}mm "
                  f"(center-distance range {dmin:.4f}-{dmax:.4f}mm)")
    results["e01_tip_fillet_samples"] = e01_samples

    # top-rim fillet (>Z region): single-height radius-offset, analytically inverted.
    # For a quarter-round fillet of radius r blending a flat top (Z=Z_top) into a
    # cylindrical OD (radius R_nom), the radius at height h below the top is
    # R_nom - r + sqrt(2rh - h^2), i.e. offset(h) = R_nom - radius(h) = r - sqrt(2rh -
    # h^2). Solving that quadratic for r given one measured (h, offset) pair:
    # r = (offset + h) +/- sqrt(2*offset*h) -- the physically valid root is the "+"
    # branch (r must exceed both h and offset here). This is simpler and was hand-
    # verified against this script's own dev-time numeric probe (h=0.05 -> offset
    # 0.605mm -> r=0.901mm, matching the CAD target E01_FILLET_TARGET=0.9mm almost
    # exactly) -- preferred over a circle fit on the sparse section polyline, which
    # gave noisy/inconsistent results between the two (should-be-symmetric) angles
    # tried during development. Sampled at angles 100/260deg (clear of both tip
    # fillets and the flange footprint, per the angle-vs-radius inspection above).
    def solve_fillet_radius(h, offset):
        disc = 2.0 * offset * h
        if disc < 0 or offset <= 0:
            return float("nan")
        return (offset + h) + math.sqrt(disc)

    top_rim_samples = []
    h_e01 = 0.05
    z_probe = CLIP_WIDTH - h_e01
    loop_probe = largest_loop(section_loop_xy(clip, z_probe))
    rad_probe = np.linalg.norm(loop_probe, axis=1)
    ang_probe = np.degrees(np.arctan2(loop_probe[:, 1], loop_probe[:, 0])) % 360.0
    for a in (100, 260):
        near = (np.abs(((ang_probe - a + 180) % 360) - 180) < 2)
        if not near.any():
            continue
        od_here = rad_probe[near].max()
        offset = float(RING_OD_R - od_here)
        r_fit = solve_fillet_radius(h_e01, offset)
        top_rim_samples.append({"angle_deg": a, "offset_at_h_mm": offset, "fitted_radius_mm": r_fit})
        print(f"   E-01 top-rim OD fillet @ angle={a}deg: offset(h={h_e01})={offset:.4f}mm "
              f"-> fitted radius {r_fit:.4f}mm")
    results["e01_top_rim_od_fillet_samples"] = top_rim_samples

    # flange outer vertical corners (90deg flat-flat corner, X face meets Y face):
    # same horizontal-section circle-fit method as the tip corners, at the same
    # mid-height z. Theoretical fillet center for a radius-r round of a 90deg convex
    # corner = (x_outer_nominal + r, sign*(MOUNT_W/2 - r)).
    MOUNT_W_LOCAL = 36.0  # mirrors clip_model.py MOUNT_W
    x_outer_nominal = -(RING_OD_R + 4.0)
    flange_corner_samples = []
    for sign, label in ((+1, "+Y"), (-1, "-Y")):
        r_guess = E01_MIN_R + 0.1
        center_guess = np.array([x_outer_nominal + r_guess, sign * (MOUNT_W_LOCAL / 2 - r_guess)])
        pts = nearest_boundary_points(loop_e, center_guess, 6)
        cx, cy, r_fit = circle_fit(pts)
        flange_corner_samples.append({"corner": label, "fitted_radius_mm": float(r_fit)})
        print(f"7. E-01 flange outer corner ({label}): fitted radius {r_fit:.4f}mm")
    results["e01_flange_corner_samples"] = flange_corner_samples

    # ---- 8. E-02 bed-contact chamfer measurement (0.2-0.4mm, 45deg) ----
    # Ring OD samples restricted to angles 90-120/240-270deg -- confirmed clear of the
    # mounting-flange's rectangular footprint (see top-rim note above); a naive
    # "RING_OD_R - measured_radius" formula is only valid where the boundary is genuinely
    # the ring's own circular arc.
    z_lo_e02 = 0.05
    loop_lo = largest_loop(section_loop_xy(clip, z_lo_e02))
    rad_lo = np.linalg.norm(loop_lo, axis=1)
    ang_lo = np.degrees(np.arctan2(loop_lo[:, 1], loop_lo[:, 0])) % 360.0
    e02_samples = []
    for a in (95, 105, 115, 245, 255, 265):
        near = (np.abs(((ang_lo - a + 180) % 360) - 180) < 3)
        if not near.any():
            continue
        od_here = rad_lo[near].max()
        run = float((RING_OD_R - od_here) + z_lo_e02)
        e02_samples.append({"region": "ring_od", "angle_deg": a, "chamfer_run_mm": run})
        print(f"8. E-02 bed chamfer (ring OD) @ angle={a}deg: run={run:.4f}mm "
              f"(band [{E02_MIN_R},{E02_MAX_R}]mm)")

    # Flange outer (wall-facing) flat face: same run measurement, along -X instead of
    # radius. The section polyline's vertex density is edge-crossing-driven (not a
    # uniform grid), so rather than requiring a point within a fixed Y-tolerance band
    # (which can legitimately find none), select among the CANDIDATE outer-face points
    # (x well past the flange's nominal, chamfered, outer-face position) the one nearest
    # each target Y.
    x_outer_nominal = -(RING_OD_R + 4.0)  # MOUNT_T=4.0, mirrors clip_model.py
    on_outer_face = loop_lo[loop_lo[:, 0] < (x_outer_nominal + 2.0)]
    for yy in (-8.0, 0.0, 8.0):
        if len(on_outer_face) == 0:
            continue
        pick = on_outer_face[np.argmin(np.abs(on_outer_face[:, 1] - yy))]
        run = float((pick[0] - x_outer_nominal) + z_lo_e02)
        e02_samples.append({"region": "flange_outer_face", "y_mm": yy,
                             "sample_y_actual_mm": float(pick[1]), "chamfer_run_mm": run})
        print(f"8. E-02 bed chamfer (flange outer face) @ y~={yy}mm (actual "
              f"{pick[1]:.2f}mm): run={run:.4f}mm (band [{E02_MIN_R},{E02_MAX_R}]mm)")
    results["e02_bed_chamfer_samples"] = e02_samples

    # ---- hashes ----
    results["clip_stl_sha256"] = sha256_file("clip.stl")
    results["clip_step_sha256"] = sha256_file("clip.step")
    print("hashes:", results["clip_stl_sha256"], results["clip_step_sha256"])

    with open("verify_output.json", "w") as f:
        json.dump(results, f, indent=2)
    print("wrote verify_output.json")


if __name__ == "__main__":
    main()
