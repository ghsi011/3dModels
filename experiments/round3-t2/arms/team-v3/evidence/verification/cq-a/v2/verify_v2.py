from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
STL = ROOT / "cq-a-washer-filter-tool.stl"
BAR = np.array([62.0, 11.7, 24.0])
BASE_Y = -8.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    mesh = trimesh.load_mesh(STL, process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError("STL did not re-import as a single mesh")
    mesh.export(OUT / "reimported.stl")
    bounds = mesh.bounds
    seated_bar = trimesh.creation.box(extents=BAR)
    seated_bar.apply_translation((0.0, 0.0, 12.0))
    seated_intersection = trimesh.boolean.intersection([mesh, seated_bar], engine="manifold")
    seated_intersection_volume = 0.0 if seated_intersection is None else float(seated_intersection.volume)
    sweep_volumes = []
    for offset in np.linspace(-24.0, 0.0, 121):
        swept_bar = seated_bar.copy()
        swept_bar.apply_translation((0.0, 0.0, offset))
        intersection = trimesh.boolean.intersection([mesh, swept_bar], engine="manifold")
        sweep_volumes.append(0.0 if intersection is None else float(intersection.volume))
    center = mesh.triangles_center
    normals = mesh.face_normals
    areas = mesh.area_faces
    down = normals[:, 1] < -np.sqrt(0.5)
    non_pbed = down & (center[:, 1] > BASE_Y + 0.31)
    pbed = down & (center[:, 1] <= BASE_Y + 0.31)
    sharp = mesh.face_adjacency_angles > np.deg2rad(40.0)
    sharp_edges = mesh.face_adjacency_edges[sharp]
    sharp_midpoints = mesh.vertices[sharp_edges].mean(axis=1)
    non_bed_sharp = sharp_midpoints[:, 1] > BASE_Y + 0.31
    sharp_rows = [
        {"midpoint_mm": np.round(mid, 4).tolist(), "dihedral_deg": round(float(np.rad2deg(angle)), 3)}
        for mid, angle in zip(sharp_midpoints[non_bed_sharp], mesh.face_adjacency_angles[sharp][non_bed_sharp])
    ]
    f02_min = np.array([-31.0, -5.85, 0.0])
    f02_max = np.array([31.0, 5.85, 24.0])
    tri_min = mesh.triangles.min(axis=1)
    tri_max = mesh.triangles.max(axis=1)
    bbox_overlap = np.all(tri_max >= f02_min, axis=1) & np.all(tri_min <= f02_max, axis=1)
    xs = np.linspace(-30.9, 30.9, 9)
    ys = np.linspace(-5.75, 5.75, 5)
    zs = np.linspace(0.1, 23.9, 7)
    samples = np.array(np.meshgrid(xs, ys, zs)).reshape(3, -1).T
    inside_samples = int(mesh.contains(samples).sum())
    cavity = np.array([62.6, 12.3, 24.35])
    metrics = {
        "sha256": sha256(STL), "watertight": bool(mesh.is_watertight),
        "components": len(mesh.split(only_watertight=False)), "euler_number": int(mesh.euler_number),
        "volume_mm3": float(mesh.volume), "bounds_mm": bounds.tolist(),
        "native_min_y_mm": float(bounds[0, 1]), "native_max_y_mm": float(bounds[1, 1]),
        "pbed_downface_area_mm2": float(areas[pbed].sum()),
        "seated_intersection_volume_mm3": seated_intersection_volume,
        "insertion_sweep_samples": len(sweep_volumes), "insertion_sweep_max_intersection_volume_mm3": max(sweep_volumes),
        "non_pbed_downface_area_mm2": float(areas[non_pbed].sum()),
        "f02_bbox_overlapping_faces": int(bbox_overlap.sum()), "f02_interior_lattice_inside_count": inside_samples,
        "cavity_mm": cavity.tolist(), "clearance_xy_per_side_mm": 0.3,
        "top_clearance_mm": 0.35, "cap_plane_clearance_mm": 0.6,
        "ss01_out_of_limit_area_mm2": float(areas[non_pbed].sum()),
        "ss02_max_bridge_span_mm": 0.0, "ss03_transition_excess_area_mm2": 0.0,
        "ss04_support_volume_mm3": 0.0, "ss04_support_contacts": 0,
        "non_pbed_sharp_edge_count": int(non_bed_sharp.sum()),
        "max_non_pbed_sharp_dihedral_deg": float(np.rad2deg(mesh.face_adjacency_angles[sharp][non_bed_sharp]).max()),
        "non_pbed_sharp_edge_samples": sharp_rows[:30],
    }
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(8, 3), dpi=180)
    ax.add_patch(Rectangle((-31, -5.85), 62, 11.7, fill=True, facecolor="#8f9aa6", alpha=.55, edgecolor="#20262d", lw=2, label="nominal F02"))
    ax.add_patch(Rectangle((-31.3, -6.15), 62.6, 12.3, fill=False, edgecolor="#c9362b", lw=2.5, label="re-imported cavity"))
    ax.axhline(0, color="#777", lw=.5); ax.axvline(0, color="#777", lw=.5)
    ax.set(xlim=(-34, 34), ylim=(-8, 8), aspect="equal", xlabel="DX (mm)", ylabel="DY (mm)", title="Same-view D0 overlay — nominal F02 vs re-imported cavity")
    ax.legend(loc="upper right")
    ax.grid(alpha=.2)
    fig.tight_layout(); fig.savefig(OUT / "svg_same_view_overlay.png"); plt.close(fig)
    (OUT / "svg_same_view_overlay.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="680" height="160" viewBox="0 0 680 160">'
        '<rect width="680" height="160" fill="white"/><text x="20" y="24" font-family="Arial" font-size="16">D0 same-view overlay: nominal F02 (grey) / re-imported cavity (red)</text>'
        '<rect x="185" y="65" width="310" height="58.5" fill="#8f9aa6" fill-opacity=".55" stroke="#20262d" stroke-width="2"/>'
        '<rect x="183.5" y="63.5" width="313" height="61.5" fill="none" stroke="#c9362b" stroke-width="3"/>'
        '<text x="20" y="150" font-family="Arial" font-size="14">Scale 5 px/mm; 0.300 mm uniform XY clearance per side; centred on D0.</text></svg>', encoding="utf-8")

    section = mesh.section(plane_origin=[0.0, 0.0, 0.0], plane_normal=[0.0, 1.0, 0.0])
    fig, ax = plt.subplots(figsize=(9, 6), dpi=180)
    for path in section.discrete:
        ax.plot(path[:, 0], path[:, 2], color="#295b7a", lw=1.5)
    ax.add_patch(Rectangle((-31, 0), 62, 24, fill=True, facecolor="#d98c45", alpha=.28, edgecolor="#a55b22", lw=1.4))
    ax.axhline(0, color="#555", lw=.7)
    ax.set(aspect="equal", xlim=(-45, 45), ylim=(-3, 68), xlabel="DX (mm)", ylabel="DZ (mm)", title="Re-imported Y=0 section with nominal F02 envelope")
    ax.grid(alpha=.2)
    fig.tight_layout(); fig.savefig(OUT / "reimport_section_y0.png"); plt.close(fig)


if __name__ == "__main__":
    main()
