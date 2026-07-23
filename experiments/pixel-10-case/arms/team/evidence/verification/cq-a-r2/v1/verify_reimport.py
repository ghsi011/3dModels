from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw


RUN = Path(__file__).resolve().parent
TEAM = RUN.parents[3]
CANDIDATE = TEAM / "pixel10_case_cq_a.stl"
REFERENCE = TEAM / "evidence/reference/ref-2/pixel10_reference_ref2.stl"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def installed(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    out = mesh.copy()
    out.apply_translation([0.0, 0.0, -4.8])
    out.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    return out


def intersection_volume(a: trimesh.Trimesh, b: trimesh.Trimesh) -> float:
    result = trimesh.boolean.intersection([a, b], engine="manifold")
    return 0.0 if result is None else float(abs(result.volume))


def rings(mesh: trimesh.Trimesh, z: float) -> list[np.ndarray]:
    section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if section is None:
        return []
    planar, _ = section.to_2D(
        trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1])
    )
    result: list[np.ndarray] = []
    for polygon in planar.polygons_full:
        result.append(np.asarray(polygon.exterior.coords))
        result.extend(np.asarray(hole.coords) for hole in polygon.interiors)
    return result


def draw_plan(ref: trimesh.Trimesh, cand: trimesh.Trimesh, out: Path) -> None:
    width, height, pad = 960, 1760, 70
    im = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(im)
    draw.text((20, 18), "r2 re-imported same-datum plan sections: reference red / case blue", fill="black")
    all_bounds = np.vstack([ref.bounds, cand.bounds])
    xmin, ymin = all_bounds[:, 0].min() - 4, all_bounds[:, 1].min() - 4
    xmax, ymax = all_bounds[:, 0].max() + 4, all_bounds[:, 1].max() + 4
    scale = min((width - 2 * pad) / (xmax - xmin), (height - 2 * pad) / (ymax - ymin))
    def point(p: np.ndarray) -> tuple[float, float]:
        return (pad + (p[0] - xmin) * scale, height - pad - (p[1] - ymin) * scale)
    for mesh, color, label, z in ((ref, "#b22222", "reference at Z=0", 0.0), (cand, "#1556a8", "case at Z=0", 0.0), (cand, "#1556a8", "case camera-lip at Z=2", 2.0)):
        for ring in rings(mesh, z):
            if len(ring) > 2:
                draw.line([point(p) for p in ring], fill=color, width=3, joint="curve")
        draw.text((24, 48 + 22 * ((0 if label.startswith('reference') else 1) if z == 0 else 2)), label, fill=color)
    im.save(out)


def main() -> None:
    raw = trimesh.load_mesh(CANDIDATE, process=True)
    ref = trimesh.load_mesh(REFERENCE, process=True)
    case = installed(raw)
    sweep: list[dict[str, float]] = []
    for offset in range(-18, 1):
        moved = ref.copy()
        moved.apply_translation([0.0, 0.0, float(offset)])
        sweep.append({"screenward_offset_mm": float(offset), "intersection_mm3": intersection_volume(case, moved)})
    with (RUN / "check-2-insertion-sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["screenward_offset_mm", "intersection_mm3"])
        writer.writeheader(); writer.writerows(sweep)
    normals, centers = raw.face_normals, raw.triangles_center
    downward = (normals[:, 2] < -0.70710678) & (centers[:, 2] > 0.3)
    components = raw.split(only_watertight=False)
    result = {
        "candidate_sha256": sha256(CANDIDATE),
        "reference_sha256": sha256(REFERENCE),
        "candidate_raw_bounds_mm": raw.bounds.tolist(),
        "candidate_installed_bounds_mm": case.bounds.tolist(),
        "candidate_bbox_mm": (raw.bounds[1] - raw.bounds[0]).tolist(),
        "candidate_watertight": bool(raw.is_watertight),
        "candidate_winding_consistent": bool(raw.is_winding_consistent),
        "candidate_components": len(components),
        "candidate_triangles": int(len(raw.faces)),
        "candidate_volume_mm3": float(raw.volume),
        "reference_watertight": bool(ref.is_watertight),
        "seated_intersection_mm3": intersection_volume(case, ref),
        "sweep": sweep,
        "sweep_max_intersection_mm3": max(item["intersection_mm3"] for item in sweep),
        "unsupported_downward_area_mm2": float(raw.area_faces[downward].sum()),
        "downward_face_count": int(downward.sum()),
        "min_z_face_area_mm2": float(raw.area_faces[np.isclose(raw.triangles_center[:, 2], raw.bounds[0, 2], atol=0.02)].sum()),
        "section_ring_count_z0": len(rings(case, 0.0)),
        "section_ring_count_z2": len(rings(case, 2.0)),
    }
    draw_plan(ref, case, RUN / "check-3-4-same-datum-sections.png")
    (RUN / "reimport_metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
