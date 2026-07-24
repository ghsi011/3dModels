from pathlib import Path
import hashlib
import math
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent
STL = ROOT / "pixel10_case.stl"
REF = ROOT / "reference_phone.stl"
OUT = ROOT / "verification_evidence.txt"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def volume_intersection(a, b):
    hit = trimesh.boolean.intersection([a, b], engine="manifold")
    return 0.0 if hit is None else abs(float(hit.volume))


def zone(x0, x1, y0, y1, z0, z1):
    result = trimesh.creation.box(extents=(x1 - x0, y1 - y0, z1 - z0))
    result.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    return result


def main():
    case = trimesh.load_mesh(STL, process=True)
    phone = trimesh.load_mesh(REF, process=True)
    b = case.bounds
    seated = volume_intersection(case, phone)
    sweep = []
    for travel in np.linspace(0.0, 16.0, 17):
        p = phone.copy()
        p.apply_translation((0, 0, float(travel)))
        sweep.append((float(travel), volume_intersection(case, p)))

    land = np.array([-1.7464466, 76.4, -0.9464466])
    rel = case.vertices - land
    qz = math.sqrt(0.5) * (rel[:, 0] + rel[:, 2])
    n_qz = math.sqrt(0.5) * (case.face_normals[:, 0] + case.face_normals[:, 2])
    c_rel = case.triangles_center - land
    c_qz = math.sqrt(0.5) * (c_rel[:, 0] + c_rel[:, 2])
    downward = (n_qz < -math.sqrt(0.5)) & (c_qz > 0.30)

    sec = case.section(plane_origin=[36.0, 76.4, 0.0], plane_normal=[0, 1, 0])
    sec_v = np.empty((0, 3)) if sec is None else sec.vertices
    pairs = case.face_adjacency
    dots = (case.face_normals[pairs[:, 0]] * case.face_normals[pairs[:, 1]]).sum(axis=1)
    dihedral = np.degrees(np.arccos(np.clip(dots, -1.0, 1.0)))
    sharp_85 = int((dihedral >= 85.0).sum())
    sharp_45 = int((dihedral >= 45.0).sum())
    opening_checks = {
        "F14_rear_aperture_inner": zone(5.0, 67.0, 110.0, 147.0, -1.25, -0.05),
        "F21_bottom_opening_inner": zone(10.0, 62.0, -3.5, 1.5, -1.25, 9.65),
        "F05_F06_top_opening_inner": zone(30.0, 42.0, 152.0, 154.0, -1.25, 9.65),
        "F07_F08_right_sidewall": zone(72.0, 73.9, 46.0, 129.0, 2.0, 8.0),
    }
    opening_results = {key: volume_intersection(case, value) for key, value in opening_checks.items()}

    lines = [
        "V1 fresh exported-STL evidence (CadQuery/trimesh re-import; no candidate generation)",
        f"candidate_sha256={sha(STL)}",
        f"reference_sha256={sha(REF)}",
        f"step_sha256={sha(ROOT / 'pixel10_case.step')}",
        f"watertight={case.is_watertight} components={len(case.split(only_watertight=False))} euler={case.euler_number}",
        f"bounds_mm={np.round(b, 6).tolist()} volume_mm3={case.volume:.6f}",
        f"seated_intersection_mm3={seated:.9f}",
        "sweep_intersection_mm3=" + ", ".join(f"{t:.1f}:{v:.9f}" for t, v in sweep),
        f"mid_y_section_vertices={len(sec_v)} x_range_mm={([float(sec_v[:,0].min()), float(sec_v[:,0].max())] if len(sec_v) else None)} z_range_mm={([float(sec_v[:,2].min()), float(sec_v[:,2].max())] if len(sec_v) else None)}",
        f"required_transform_z_range_mm=[{qz.min():.9f},{qz.max():.9f}] contact_vertices_abs_lt_0p05={int((np.abs(qz) < .05).sum())}",
        f"unsupported_downward_area_mm2={case.area_faces[downward].sum():.9f} faces={int(downward.sum())}",
        f"exported_mesh_sharp_edges_dihedral_ge_85deg={sharp_85} ge_45deg={sharp_45} max_dihedral_deg={dihedral.max():.6f}",
        "opening_zone_intersection_mm3=" + ", ".join(f"{k}:{v:.9f}" for k, v in opening_results.items()),
        "visual_inspection=V1 viewed all four candidate renders and reference_rear_overlay.png; no candidate rear same-camera overlay/composite against S2 is supplied.",
        "interpretation=All numeric records above derive from re-imported pixel10_case.stl, except file hashes and visual-inspection statement.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
