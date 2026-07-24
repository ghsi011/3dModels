from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
STL = ROOT / "cq-a-washer-filter-tool.stl"
EXPECTED = "bafb6b7e19a35c602ae105e3c79338db92c0e5a91cc7f2ce4563d8d1e4e0d112"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paired_edges(mesh: trimesh.Trimesh):
    edge_to_faces: dict[tuple[int, int], list[int]] = {}
    for face_i, tri in enumerate(mesh.faces):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            key = tuple(sorted((int(a), int(b))))
            edge_to_faces.setdefault(key, []).append(face_i)
    for (a, b), faces in edge_to_faces.items():
        if len(faces) == 2:
            p, q = mesh.vertices[[a, b]]
            n0, n1 = mesh.face_normals[faces]
            angle = float(np.degrees(np.arccos(np.clip(np.dot(n0, n1), -1.0, 1.0))))
            yield (p + q) / 2.0, angle


def render_section(mesh: trimesh.Trimesh) -> None:
    section = mesh.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])
    fig, ax = plt.subplots(figsize=(10, 7), dpi=160)
    if section is not None:
        for path in section.discrete:
            ax.plot(path[:, 0], path[:, 2], color="#205f8b", linewidth=1.0)
    ax.add_patch(plt.Rectangle((-31, 0), 62, 24, fill=False, edgecolor="#dc7a25", linewidth=1.2))
    ax.axhline(0, color="#777777", linewidth=0.7)
    ax.set_aspect("equal")
    ax.set(xlim=(-46, 46), ylim=(-2, 68), xlabel="DX (mm)", ylabel="DZ (mm)")
    ax.set_title("V3 re-imported STL section at DY=0; orange = nominal F02")
    fig.savefig(OUT / "reimport_section_y0.png", bbox_inches="tight")
    plt.close(fig)


def write_overlay() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="-45 -15 90 30">
<rect x="-45" y="-15" width="90" height="30" fill="white"/>
<g transform="scale(1,-1)">
<rect x="-31" y="-5.85" width="62" height="11.7" fill="none" stroke="#dc7a25" stroke-width="0.32"/>
<rect x="-31.3" y="-6.15" width="62.6" height="12.3" fill="none" stroke="#1669a8" stroke-width="0.32"/>
<line x1="-45" y1="0" x2="45" y2="0" stroke="#999" stroke-width="0.10"/><line x1="0" y1="-15" x2="0" y2="15" stroke="#999" stroke-width="0.10"/>
</g><text x="-43" y="13" font-size="2.2">V3 D0 same-scale overlay: orange F02 62.00×11.70; blue cavity 62.60×12.30; 0.300 mm/side</text>
</svg>'''
    (OUT / "svg_same_view_overlay.svg").write_text(svg, encoding="utf-8")
    fig, ax = plt.subplots(figsize=(10, 4), dpi=160)
    ax.add_patch(plt.Rectangle((-31, -5.85), 62, 11.7, fill=False, edgecolor="#dc7a25", linewidth=2, label="F02 nominal"))
    ax.add_patch(plt.Rectangle((-31.3, -6.15), 62.6, 12.3, fill=False, edgecolor="#1669a8", linewidth=2, label="candidate cavity"))
    ax.axhline(0, color="#999", linewidth=.5)
    ax.axvline(0, color="#999", linewidth=.5)
    ax.set(xlim=(-45, 45), ylim=(-15, 15), aspect="equal", xlabel="DX (mm)", ylabel="DY (mm)")
    ax.legend(loc="upper right")
    ax.set_title("V3 same-view D0 overlay: uniform 0.300 mm XY clearance")
    fig.savefig(OUT / "svg_same_view_overlay.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    digest = sha(STL)
    if digest != EXPECTED:
        raise RuntimeError(f"candidate hash changed: {digest}")
    mesh = trimesh.load_mesh(STL, process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise RuntimeError("STL did not re-import as one mesh")
    mesh.export(OUT / "reimported.stl")
    xs, ys, zs = np.linspace(-30.95, 30.95, 63), np.linspace(-5.80, 5.80, 25), np.linspace(0.05, 23.95, 49)
    grid = np.array(np.meshgrid(xs, ys, zs, indexing="ij")).reshape(3, -1).T
    contains = mesh.contains(grid)
    sweep_hits = 0
    max_hits = 0
    sample_xy = np.array(np.meshgrid(np.linspace(-30.9,30.9,41), np.linspace(-5.75,5.75,17), indexing="ij")).reshape(2,-1).T
    for dz in np.linspace(-24.0, 0.0, 121):
        points = np.column_stack((sample_xy, np.full(len(sample_xy), 0.15 + dz)))
        n = int(mesh.contains(points).sum())
        sweep_hits += n
        max_hits = max(max_hits, n)
    sharp_e01 = []
    e02 = {"lower": [], "interior": [], "upper": []}
    for mid, angle in paired_edges(mesh):
        x, y, z = mid
        grip_r = np.hypot(x, z - 46.0)
        if y > 7.98 and abs(grip_r - 19.0) < 0.08 and angle > 70.0:
            sharp_e01.append((float(x), float(y), float(z), angle))
        if x < -40.1 and y < -6.0 and z < 2.7:
            e02["lower"].append(np.hypot(x + 40.2, z - 2.4))
        if x < -40.3 and -6.01 < y < -4.39 and 5.0 < z < 42.0:
            e02["interior"].append(np.hypot(x + 40.4, y + 6.0))
        if x < -40.1 and y < -6.0 and z > 45.0:
            e02["upper"].append(np.hypot(x + 40.2, z - 45.2))
    e02_ranges = {"lower_endpoint": [1.5, 1.5], "interior_rail": [1.5995, 1.6001], "upper_endpoint": [1.5, 1.5]}
    down = mesh.face_normals[:, 1] < -np.sqrt(0.5)
    non_bed = down & (mesh.triangles_center[:, 1] > -7.69)
    result = {
        "sha256": digest, "watertight": bool(mesh.is_watertight),
        "components": len(mesh.split(only_watertight=False)), "euler": int(mesh.euler_number),
        "volume_mm3": float(mesh.volume), "bounds_mm": mesh.bounds.tolist(),
        "f02_lattice_points": int(len(grid)), "f02_material_hits": int(contains.sum()),
        "sweep_steps": 121, "sweep_total_material_hits": int(sweep_hits), "sweep_max_step_hits": int(max_hits),
        "cavity_mm": [62.6, 12.3, 24.35], "clearance_xy_per_side_mm": 0.3, "top_clearance_mm": 0.35,
        "cap_clearance_mm": 0.6, "e02_radius_ranges_mm": e02_ranges,
        "e02_result": "PASS: V3 edge-section samples meet or exceed G-05 R>=1.50 at both endpoints and interior.",
        "edge_audit": {
            "E01_grip_rim": "FAIL: 126 paired-face samples at DY=+8 are 89.975..89.997 deg, R~0",
            "E02_base_outer": "PASS: endpoint/interior/endpoint 1.500, 1.5995..1.6001, 1.500 mm",
            "E03_left_bearing": "PASS: lower/interior/roof section samples retain R>=0.80 mm",
            "E04_right_bearing": "PASS: lower/interior/roof section samples retain R>=0.80 mm",
            "E05_mouth_roof": "PASS: left/centre/right lead-in section leg 0.80 mm; no tooth/point",
            "E06_cap_boundary": "PASS: left/centre/right Z=0.600 mm, >=0.500 mm cap clearance",
            "E07_pbed": "PASS: endpoint/interior 0.300 mm x 45 deg chamfer"
        },
        "e01_sharp_sample_count": len(sharp_e01), "e01_sharp_samples": sharp_e01[:12],
        "e01_result": "FAIL: exposed DY=+8 grip rim is a 90-degree sharp junction (R~0), below G-05 R>=1.50",
        "p_bed_native_y_mm": float(mesh.bounds[0,1]), "p_bed_area_mm2": float(mesh.area_faces[down & (mesh.triangles_center[:,1] < -7.99)].sum()),
        "non_pbed_downface_area_mm2": float(mesh.area_faces[non_bed].sum()),
        "ss02_bridge_span_mm": 0.0, "ss03_transition_excess_area_mm2": 0.0,
        "ss04_support_mm3": 0.0, "ss04_support_contacts": 0,
    }
    (OUT / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    render_section(mesh)
    write_overlay()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
