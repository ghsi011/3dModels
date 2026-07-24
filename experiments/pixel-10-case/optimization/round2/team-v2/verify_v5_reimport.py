from __future__ import annotations

import hashlib
import math
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parent
STL = ROOT / "pixel10_case.stl"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rounded_reference() -> trimesh.Trimesh:
    cx, cy, radius = 36.0, 76.4, 12.0
    base = cq.Workplane("XY").box(48.0, 152.8, 8.6, centered=(True, True, False)).translate((cx, cy, 0))
    base = base.union(cq.Workplane("XY").box(72.0, 128.8, 8.6, centered=(True, True, False)).translate((cx, cy, 0)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            base = base.union(cq.Workplane("XY").circle(radius).extrude(8.6).translate((cx + sx * 24.0, cy + sy * 64.4, 0)))
    temp = ROOT / "_v5_reference_only.stl"
    cq.exporters.export(base, str(temp), tolerance=0.025, angularTolerance=0.15)
    mesh = trimesh.load_mesh(temp, process=True)
    temp.unlink(missing_ok=True)
    return mesh


def intersection_volume(a: trimesh.Trimesh, b: trimesh.Trimesh) -> float:
    hit = trimesh.boolean.intersection([a, b], engine="manifold")
    return 0.0 if hit is None else abs(float(hit.volume))


def main() -> None:
    case = trimesh.load_mesh(STL, process=True)
    ref = rounded_reference()
    print("V5 FRESH REIMPORT — verifier-owned, non-acceptance until report verdict")
    print("candidate_sha256", digest(STL))
    print("step_sha256", digest(ROOT / "pixel10_case.step"))
    print("watertight", case.is_watertight, "components", len(case.split(only_watertight=False)), "winding", case.is_winding_consistent)
    print("bounds_mm", np.array2string(case.bounds, precision=6), "volume_mm3", f"{case.volume:.6f}")
    print("seated_interference_mm3", f"{intersection_volume(case, ref):.9f}")
    sweep = []
    for z in range(17):
        trial = ref.copy()
        trial.apply_translation((0, 0, float(z)))
        sweep.append(intersection_volume(case, trial))
    print("insertion_z_0_to_16_max_mm3", f"{max(sweep):.9f}", "samples", len(sweep))
    section = case.section(plane_origin=[36.0, 76.4, 0.0], plane_normal=[0, 1, 0])
    lines = [] if section is None else section.discrete
    vertices = 0 if section is None else sum(len(x) for x in lines)
    print("mid_y_section_loops", len(lines), "vertices", vertices)
    rim_section = case.section(plane_origin=[36.0, 120.0, 0.0], plane_normal=[0, 1, 0])
    rim_points = np.concatenate(rim_section.discrete)
    rim_points = rim_points[(rim_points[:, 0] >= 1.59) & (rim_points[:, 0] <= 2.01) & (rim_points[:, 2] >= -1.31) & (rim_points[:, 2] <= -0.89)]
    matrix = np.column_stack((2 * rim_points[:, 0], 2 * rim_points[:, 2], np.ones(len(rim_points))))
    rhs = rim_points[:, 0] ** 2 + rim_points[:, 2] ** 2
    center_x, center_z, offset = np.linalg.lstsq(matrix, rhs, rcond=None)[0]
    rim_radius = math.sqrt(offset + center_x**2 + center_z**2)
    print("g04_f23_rim_section_y120_radius_mm", f"{rim_radius:.6f}", "points", len(rim_points))
    zones = {
        "F14_center": ([36.0, 128.5, 0.0], [60.0, 35.0, 1.0]),
        "F21_center": ([36.0, -1.0, 4.0], [55.0, 5.0, 12.0]),
        "F05_F06_top_slot": ([36.0, 153.0, 4.0], [15.8, 5.0, 12.0]),
        "F07_F08_control_front": ([75.0, 87.5, 5.0], [5.0, 84.8, 7.0]),
    }
    for name, (center, extents) in zones.items():
        zone = trimesh.creation.box(extents=extents, transform=trimesh.transformations.translation_matrix(center))
        print(name + "_forbidden_material_mm3", f"{intersection_volume(case, zone):.9f}")
    land = np.array([-1.7464466094067206, 76.4, -0.9464466094067263])
    rotation = np.array([[math.sqrt(.5), 0, -math.sqrt(.5)], [0, 1, 0], [math.sqrt(.5), 0, math.sqrt(.5)]])
    qz = ((case.vertices - land) @ rotation.T)[:, 2]
    print("printer_z_range_mm", f"{qz.min():.9f}", f"{qz.max():.9f}", "bed_vertices_0p05", int(np.count_nonzero(np.abs(qz) <= .05)))
    print("known_g05_part_only_out_of_limit_area_mm2", "4.408623")
    print("known_g05_f23_transition_offsets_mm", "0.405512..43.587353")
    print("g05_v_scope", "exterior_nonfunctional_underside_only; P2 contact/toolpath evidence downstream")
    print("g04_radius_limit_mm", "0.380000..0.420000")
    print("forbidden_support_contacts", "cavity,capture_lip,F05_D09,F07_F08_D06,F14_opening,F21_opening,visible_exterior_opposite_L,exposed_G04_radius")


if __name__ == "__main__":
    main()
