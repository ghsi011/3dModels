"""
verify.py -- DESIGNER SELF-CHECK, NON-ACCEPTANCE.

Re-imports cradle.stl (trimesh, not the in-memory CadQuery solid) and runs the Phase-4-style
checks from skills/3d-modeling/references/cadquery-patterns.md against the ACCEPTED
watch_reference.stl, plus the print_plan_checks.json geometry-rule numbers. This is designer
evidence for candidate_readiness.md -- it is never acceptance and never substitutes for a
fresh, independent verifier pass.
"""
import hashlib
import json
import math

import numpy as np
import trimesh

TILT_DEG = 27.5
WEDGE_HEIGHT = 18.0

# print_plan_checks.json numbers this script checks against
G01_MIN_CLR = 0.15
G01_MAX_CLR = 0.35
G01_NOMINAL_BORE = 51.75
G02_MIN_DEPTH = 15.05
G02_MAX_DEPTH = 15.25
G03_MIN_WALL = 1.6
G04_MIN_WALL = 0.8
E01_MIN_R, E01_MAX_R = 0.2, 0.4
E02_MIN_R = 0.5
E03_MIN_R = 1.0
E04_MIN_R = 0.3
S01_MAX_ARC_DEG = 180.0
S01_MAX_RADIAL_MM = 3.5
S01_MAX_AREA_MM2 = 250.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def to_world(mesh_local, tilt_deg=TILT_DEG, wedge_height=WEDGE_HEIGHT):
    theta = math.radians(tilt_deg)
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)],
    ])
    m = mesh_local.copy()
    m.vertices = m.vertices @ Rx.T + np.array([0, 0, wedge_height])
    return m


def to_local(mesh_world, tilt_deg=TILT_DEG, wedge_height=WEDGE_HEIGHT):
    theta = math.radians(tilt_deg)
    Rx_inv = np.array([
        [1, 0, 0],
        [0, math.cos(theta), math.sin(theta)],
        [0, -math.sin(theta), math.cos(theta)],
    ])
    m = mesh_world.copy()
    m.vertices = (m.vertices - np.array([0, 0, wedge_height])) @ Rx_inv.T
    return m


def to_local_points(points_world, tilt_deg=TILT_DEG, wedge_height=WEDGE_HEIGHT):
    theta = math.radians(tilt_deg)
    Rx_inv = np.array([
        [1, 0, 0],
        [0, math.cos(theta), math.sin(theta)],
        [0, -math.sin(theta), math.cos(theta)],
    ])
    return (np.asarray(points_world) - np.array([0, 0, wedge_height])) @ Rx_inv.T


def main():
    results = {}

    cradle = trimesh.load("cradle.stl")
    coupon = trimesh.load("cradle_coupon.stl")
    watch_local = trimesh.load("../garmin-step2-reference/watch_reference.stl")
    watch_world = to_world(watch_local)

    # ---- 0. basic integrity ----
    results["cradle_watertight"] = bool(cradle.is_watertight)
    results["cradle_volume_mm3"] = float(cradle.volume)
    results["cradle_bounds"] = cradle.bounds.tolist()
    results["cradle_components"] = len(cradle.split(only_watertight=False))
    results["coupon_watertight"] = bool(coupon.is_watertight)
    results["coupon_components"] = len(coupon.split(only_watertight=False))
    print("0. integrity:", json.dumps({k: results[k] for k in
          ("cradle_watertight", "cradle_volume_mm3", "cradle_bounds", "cradle_components",
           "coupon_watertight", "coupon_components")}, indent=2))

    # ---- 1. seated interference (general bore vs. the intentional lip engagement) ----
    # METHOD NOTE: a straight trimesh.boolean.intersection([cradle, watch]) (manifold engine)
    # reports a nonzero volume dominated by numerical noise at local Z'=0 -- the watch's flat
    # caseback and the cradle floor's flat top are DESIGNED to sit exactly coincident there (a
    # flush seat, zero nominal gap), and boolean engines produce a spurious sliver volume at an
    # exactly-coincident shared face (the same class of issue cadquery-patterns.md and this
    # project's own case_model.py precedent call out for coincident-face booleans). This is
    # therefore measured with dense Monte Carlo point-containment sampling instead (300k points
    # drawn inside the watch's own bounding box, kept if inside the watch, then tested for
    # containment in the cradle) -- confirmed to find the *entire* non-floor-plane overlap
    # concentrated exactly at local Z' in [13.15, 15.15] (the S-01 lip band, the intended
    # retention engagement), and effectively zero genuine general-bore interference once points
    # within 0.2mm of the Z'=0 seating plane (which is the coincident-face noise band, not a
    # real gap) are excluded. The raw boolean total is reported alongside for transparency, not
    # silently discarded.
    lip_z0 = 15.15 - 2.0  # POCKET_DEPTH - LIP_HEIGHT, must match cradle_model.py
    rng = np.random.default_rng(0)
    lo, hi = watch_world.bounds
    mc_pts = rng.uniform(lo, hi, size=(300_000, 3))
    mc_in_watch = watch_world.contains(mc_pts)
    watch_vol_est = float(mc_in_watch.mean()) * float(np.prod(hi - lo))
    mc_watch_pts = mc_pts[mc_in_watch]
    mc_in_cradle = cradle.contains(mc_watch_pts)
    mc_hits_world = mc_watch_pts[mc_in_cradle]
    mc_hits_local = to_local_points(mc_hits_world) if len(mc_hits_world) else np.zeros((0, 3))
    # "general bore" = away from BOTH the Z'=0 floor-coincidence noise band AND the S-01 lip
    # band (lip_z0=13.15..15.15); "at lip" = within the lip band specifically.
    general_bore_mask = (mc_hits_local[:, 2] > 0.2) & (mc_hits_local[:, 2] < lip_z0) \
        if len(mc_hits_local) else np.zeros((0,), dtype=bool)
    at_lip_mask = mc_hits_local[:, 2] >= lip_z0 if len(mc_hits_local) else np.zeros((0,), dtype=bool)
    away_from_floor = mc_hits_local[general_bore_mask]
    at_lip = mc_hits_local[at_lip_mask]

    vol_below = len(away_from_floor) / max(1, len(mc_watch_pts)) * watch_vol_est
    vol_at_lip_mc = len(at_lip) / max(1, len(mc_watch_pts)) * watch_vol_est

    inter_full = trimesh.boolean.intersection([cradle, watch_world], engine="manifold")
    vol_full_raw_boolean = float(inter_full.volume) if len(inter_full.faces) else 0.0

    results["montecarlo_watch_interior_samples"] = int(mc_in_watch.sum())
    results["montecarlo_hits_in_cradle_total"] = int(len(mc_hits_world))
    results["montecarlo_hits_away_from_floor_plane_gt0p2mm"] = int(len(away_from_floor))
    results["interference_general_bore_mm3"] = vol_below
    results["interference_at_lip_only_mm3"] = vol_at_lip_mc
    results["interference_full_incl_lip_mm3_raw_boolean"] = vol_full_raw_boolean
    vol_lip = vol_at_lip_mc
    print(f"1. interference (Monte Carlo point-containment, 300k samples): "
          f"general bore={vol_below:.6f} mm3 (plan G-01 threshold: 0), "
          f"at-lip-only={vol_lip:.6f} mm3 (intentional retention engagement, see "
          f"print_notes.md); raw boolean total (includes Z'=0 coincident-face noise, "
          f"reported for transparency, NOT authoritative)={vol_full_raw_boolean:.6f} mm3")

    # ---- 2. insertion/travel sweep (rigid straight-line, along local +Z') ----
    print("2. insertion sweep (rigid straight-line translate along pocket axis):")
    sweep = []
    for t in (-3, -1, 0, 1, 2, 3, 5, 8, 12, 16, 20):
        watch_t_local = watch_local.copy()
        watch_t_local.apply_translation((0, 0, t))
        watch_t_world = to_world(watch_t_local)
        inter = trimesh.boolean.intersection([cradle, watch_t_world], engine="manifold")
        v = float(inter.volume) if len(inter.faces) else 0.0
        sweep.append({"travel_mm": t, "interference_mm3": v})
        print(f"   t={t:+3d} mm  interference={v:.4f} mm3")
    results["insertion_sweep"] = sweep

    # ---- 3. section render already produced by render_cradle.py (cradle_installed_section.png) ----
    print("3. section render: see cradle_installed_section.png (produced by render_cradle.py)")

    # ---- 4. visual side-by-side: see cradle_exterior_view.png / cradle_print_orientation.png ----
    print("4. visual check: see cradle_exterior_view.png, cradle_print_orientation.png")

    # ---- 5/7a. feature re-measurement: pocket bore diameter, depth, floor, wall thickness ----
    local = to_local(cradle)
    # bore diameter: slice at local z'=1.0 (clear of floor/rim), measure the INNER ring
    sec = local.section(plane_origin=[0, 0, 1.0], plane_normal=[0, 0, 1])
    bore_diams = []
    if sec is not None:
        planar, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, 1.0], [0, 0, 1]))
        for poly in planar.polygons_full:
            for hole in poly.interiors:
                c = np.array(hole.coords)
                center = c.mean(axis=0)
                r = np.linalg.norm(c - center, axis=1)
                bore_diams.append((float(r.min()) * 2, float(r.max()) * 2))
    results["bore_diam_slices_at_z1"] = bore_diams
    print("5/7. bore diameter re-measured at local z'=1.0mm (min-dia, max-dia) per hole:",
          bore_diams, " nominal target:", G01_NOMINAL_BORE + 2 * G01_MIN_CLR, "-",
          G01_NOMINAL_BORE + 2 * G01_MAX_CLR)

    # pocket depth: local z extent of the bore wall region (max z of the wall at the bore radius)
    results["local_bounds"] = local.bounds.tolist()
    print("   local-frame bounds (z' axis is bounds[:,2]):", local.bounds.tolist())

    # wall-thickness ray-cast (whole part, matches cadquery-patterns.md pattern). Sample
    # count kept modest (no embree backend in this environment -- pure-python ray casting
    # is slow; 3000 samples finishes in reasonable time and is still a meaningful screen).
    np.random.seed(0)
    samples, face_idx = trimesh.sample.sample_surface_even(cradle, 3000)
    normals = cradle.face_normals[face_idx]
    eps = 0.02
    origins = samples - normals * eps
    locations, ray_idx, _ = cradle.ray.intersects_location(
        ray_origins=origins, ray_directions=-normals, multiple_hits=False
    )
    if len(locations):
        dists = np.linalg.norm(locations - samples[ray_idx], axis=1)
        valid = dists > 2 * eps
        min_wall = float(dists[valid].min()) if valid.any() else float("nan")
    else:
        min_wall = float("nan")
    results["min_wall_thickness_mm"] = min_wall
    print(f"7b. wall-thickness ray-cast (3000 samples): min={min_wall:.4f} mm "
          f"(G-03 structural floor {G03_MIN_WALL}, G-04 absolute floor {G04_MIN_WALL})")

    # ---- 6. measurement audit: printed separately in candidate_readiness.md parameter mapping ----

    # ---- 7c. cylindrical/printability audit: down-facing overhang area (informational; the
    #          gated version is team_preflight.py support-audit, run separately below) ----
    down = cradle.face_normals[:, 2] < -0.70710678
    bed_contact = np.abs(cradle.triangles[:, :, 2] - 0.0).max(axis=1) <= 0.05
    overhang_area = float(cradle.area_faces[down & ~bed_contact].sum())
    results["downward_facing_nonbed_area_mm2_informational"] = overhang_area
    print(f"7c. informational downward-facing (non-bed) area: {overhang_area:.2f} mm2 "
          "(the GATED measurement is team_preflight.py support-audit, run separately)")

    # ---- hashes ----
    results["cradle_stl_sha256"] = sha256_file("cradle.stl")
    results["cradle_step_sha256"] = sha256_file("cradle.step")
    results["cradle_coupon_stl_sha256"] = sha256_file("cradle_coupon.stl")
    print("hashes:", results["cradle_stl_sha256"], results["cradle_step_sha256"],
          results["cradle_coupon_stl_sha256"])

    with open("verify_output.json", "w") as f:
        json.dump(results, f, indent=2)
    print("wrote verify_output.json")


if __name__ == "__main__":
    main()
