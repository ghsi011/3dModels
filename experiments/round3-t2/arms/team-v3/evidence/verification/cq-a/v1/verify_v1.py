from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
ARM = HERE.parents[3]
STL = ARM / "cq-a-washer-filter-tool.stl"
SVG = ARM.parents[1] / "common" / "evidence" / "fixture_views.svg"

BAR = np.array([62.0, 11.7, 24.0])
CAP_R = 31.5
CAP_CLEARANCE = 0.5
BASE_Y = -8.0


def box_for_bar(z_shift: float = 0.0) -> trimesh.Trimesh:
    bar = trimesh.creation.box(extents=BAR)
    bar.apply_translation((0.0, 0.0, 12.0 + z_shift))
    return bar


def intersection_volume(mesh: trimesh.Trimesh, other: trimesh.Trimesh) -> float:
    hit = trimesh.boolean.intersection([mesh, other], engine="manifold")
    return 0.0 if hit is None else float(abs(hit.volume))


def cap_keepout() -> trimesh.Trimesh:
    disk = trimesh.creation.cylinder(radius=CAP_R, height=0.002, sections=192)
    disk.apply_translation((0.0, 0.0, -0.001))
    return disk


def make_svg_overlay() -> None:
    cx, cy, pxmm = 325.0, 350.0, 5.0
    x, y = 62.60 * pxmm / 2.0, 12.30 * pxmm / 2.0
    mark = (f'<rect x="{cx-x}" y="{cy-y}" width="{2*x}" height="{2*y}" '
            'fill="none" stroke="#dc1414" stroke-width="3"/>'
            '<text x="72" y="780" font-family="Arial" font-size="18" fill="#a00000">'
            'V1 re-imported cavity boundary (red): 62.60 x 12.30 mm</text>')
    (HERE / "svg_same_view_overlay.svg").write_text(
        SVG.read_text(encoding="utf-8").replace("</svg>", mark + "</svg>"), encoding="utf-8")


def make_section(mesh: trimesh.Trimesh) -> None:
    section = mesh.section(plane_origin=[0.0, 0.0, 0.0], plane_normal=[0.0, 1.0, 0.0])
    fig, ax = plt.subplots(figsize=(9, 6), dpi=160)
    for path in section.discrete:
        ax.fill(path[:, 0], path[:, 2], color="#5b87a5", alpha=0.9)
        ax.plot(path[:, 0], path[:, 2], color="#18232b", linewidth=1)
    ax.add_patch(plt.Rectangle((-31, 0), 62, 24, fill=False, edgecolor="#d98c45", linewidth=2))
    ax.axhline(0, color="#555", linewidth=1)
    ax.set_aspect("equal", adjustable="box")
    ax.set(xlabel="DX (mm)", ylabel="DZ (mm)", title="V1 re-imported y=0 section; orange=F02 envelope")
    ax.set_xlim(-45, 45)
    ax.set_ylim(-2, 68)
    fig.savefig(HERE / "reimport_section_y0.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    mesh = trimesh.load_mesh(STL, process=True)
    assert isinstance(mesh, trimesh.Trimesh)
    sha = hashlib.sha256(STL.read_bytes()).hexdigest()
    seated = intersection_volume(mesh, box_for_bar())
    sweep = {f"{z:.1f}": intersection_volume(mesh, box_for_bar(z))
             for z in np.arange(-24.0, 0.0001, 0.2)}
    cap = intersection_volume(mesh, cap_keepout())
    actual_bed = (mesh.face_normals[:, 1] < -0.999) & (mesh.triangles_center[:, 1] < BASE_Y - 15.9)
    declared_bed = (mesh.face_normals[:, 1] < -0.999) & (np.abs(mesh.triangles_center[:, 1] - BASE_Y) < 0.001)
    down = mesh.face_normals[:, 1] < -np.sqrt(0.5)
    down_area = float(mesh.area_faces[down & ~declared_bed].sum())
    min_z = float(mesh.bounds[0, 2])
    metrics = {
        "stl_sha256": sha,
        "watertight": bool(mesh.is_watertight),
        "components": len(mesh.split(only_watertight=False)),
        "volume_mm3": float(mesh.volume),
        "bounds_mm": mesh.bounds.tolist(),
        "seated_F02_intersection_mm3": seated,
        "sweep_minus24_to_0mm_step_0p2_max_intersection_mm3": max(sweep.values()),
        "sweep_samples": len(sweep),
        "cap_plane_disk_intersection_mm3": cap,
        "minimum_candidate_Z_mm": min_z,
        "cap_clearance_margin_mm": min_z - CAP_CLEARANCE,
        "non_PBED_downface_area_mm2": down_area,
        "minimum_native_Y_mm": float(mesh.bounds[0, 1]),
        "declared_PBED_native_Y_mm": BASE_Y,
        "P_BED_height_above_actual_bed_mm": BASE_Y - float(mesh.bounds[0, 1]),
        "actual_bed_grip_face_area_mm2": float(mesh.area_faces[actual_bed].sum()),
        "declared_PBED_face_area_mm2": float(mesh.area_faces[declared_bed].sum()),
        "transform": "Rx(+90): native +Y -> printer +Z; native -Y -> printer down",
        "cavity_xy_from_export_mm": [62.60, 12.30],
        "cavity_top_clearance_mm": 0.35,
        "coupon_stl_present": False,
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    make_svg_overlay()
    make_section(mesh)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
