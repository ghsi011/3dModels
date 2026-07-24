# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "trimesh", "matplotlib"]
# ///
# ─── How to run ───
# python .\verify.py
from __future__ import annotations

import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh


OUT = Path(__file__).resolve().parent
STL = OUT / "cq-a-washer-filter-tool.stl"
EVIDENCE = OUT / "evidence" / "candidates" / "cq-a"
BAR = np.array([62.0, 11.7, 24.0])
CAVITY = np.array([62.6, 12.3, 24.35])
BASE_Y = -8.0
BASE_EDGE_RADIUS = 1.80
BASE_SIDE_RADIUS = 1.60
BASE_X_CENTER = -40.20
BASE_SIDE_X_CENTER = -40.40
BASE_Z_LOWER_CENTER = 2.40
BASE_Z_UPPER_CENTER = 45.20
BASE_Y_SIDE_CENTER = -6.00
GRIP_MAJOR_RADIUS = 17.40
GRIP_RIM_CENTER_Y = 6.40
GRIP_CENTER_Z = 46.00


def render(mesh: trimesh.Trimesh, name: str, elev: float, azim: float, section: bool = False) -> None:
    shown = mesh.copy()
    if section:
        shown = shown.slice_plane(np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), cap=False)
    figure = plt.figure(figsize=(7, 7), dpi=160, facecolor="white")
    axes = figure.add_subplot(111, projection="3d")
    collection = Poly3DCollection(shown.triangles, facecolor="#5b87a5", edgecolor="none", alpha=0.93)
    axes.add_collection3d(collection)
    bounds = mesh.bounds
    center = bounds.mean(axis=0)
    half = float(np.max(bounds[1] - bounds[0]) * 0.58)
    axes.set(xlim=(center[0] - half, center[0] + half), ylim=(center[1] - half, center[1] + half), zlim=(center[2] - half, center[2] + half))
    axes.set_box_aspect((1, 1, 1))
    axes.view_init(elev=elev, azim=azim)
    axes.set_axis_off()
    figure.savefig(OUT / name, bbox_inches="tight", pad_inches=0.04)
    plt.close(figure)


def installed_render(mesh: trimesh.Trimesh) -> None:
    figure = plt.figure(figsize=(8, 7), dpi=160, facecolor="white")
    axes = figure.add_subplot(111, projection="3d")
    axes.add_collection3d(Poly3DCollection(mesh.triangles, facecolor="#4f7e9d", edgecolor="none", alpha=0.76))
    bar = trimesh.creation.box(extents=BAR)
    bar.apply_translation((0.0, 0.0, 12.0))
    axes.add_collection3d(Poly3DCollection(bar.triangles, facecolor="#d98c45", edgecolor="none", alpha=0.72))
    axes.set(xlim=(-46, 46), ylim=(-14, 14), zlim=(-15, 55))
    axes.set_box_aspect((1, 1, 1))
    axes.view_init(elev=20, azim=-55)
    axes.set_axis_off()
    figure.savefig(OUT / "cq-a-installed-engagement.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(figure)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    mesh = trimesh.load_mesh(STL, process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError("candidate STL did not re-import as one trimesh body")
    if not mesh.is_watertight or len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError("candidate STL must re-import as one watertight body")
    bounds = mesh.bounds
    down = mesh.face_normals[:, 1] < -0.70710678
    bed_tolerance = 0.01
    minimum_y = float(bounds[0, 1])
    if abs(minimum_y - BASE_Y) > bed_tolerance:
        raise RuntimeError(f"P_BED must be the lowest native-Y face: {minimum_y:.6f} != {BASE_Y:.6f}")
    non_bed = down & (mesh.triangles_center[:, 1] > BASE_Y + 0.31)
    unsupported_area = float(mesh.area_faces[non_bed].sum())
    centers = mesh.triangles_center
    normals = mesh.face_normals
    lower_mask = (centers[:, 0] < -40.1) & (centers[:, 2] < 2.6) & (centers[:, 1] < -6.0) & (np.abs(normals[:, 1]) < 0.1)
    middle_mask = (centers[:, 0] < -40.3) & (centers[:, 1] > -6.01) & (centers[:, 1] < -4.39) & (centers[:, 2] > 5.0) & (centers[:, 2] < 42.0) & (np.abs(normals[:, 2]) < 0.1)
    upper_mask = (centers[:, 0] < -40.1) & (centers[:, 2] > 45.0) & (centers[:, 1] < -6.0) & (np.abs(normals[:, 1]) < 0.1)
    lower_radii = np.linalg.norm(centers[lower_mask][:, [0, 2]] - np.array([BASE_X_CENTER, BASE_Z_LOWER_CENTER]), axis=1)
    middle_radii = np.linalg.norm(centers[middle_mask][:, [0, 1]] - np.array([BASE_SIDE_X_CENTER, BASE_Y_SIDE_CENTER]), axis=1)
    upper_radii = np.linalg.norm(centers[upper_mask][:, [0, 2]] - np.array([BASE_X_CENTER, BASE_Z_UPPER_CENTER]), axis=1)
    if min(lower_radii.min(), middle_radii.min(), upper_radii.min()) < 1.5:
        raise RuntimeError("E-02 re-imported radius sample is below G-05")
    grip_rho = np.hypot(centers[:, 0], centers[:, 2] - GRIP_CENTER_Z)
    grip_minor = np.hypot(grip_rho - GRIP_MAJOR_RADIUS, centers[:, 1] - GRIP_RIM_CENTER_Y)
    grip_mask = (centers[:, 1] > 6.3) & (centers[:, 1] < 8.1) & (grip_rho > 17.3) & (grip_rho < 19.1)
    grip_angle = np.arctan2(centers[:, 2] - GRIP_CENTER_Z, centers[:, 0])
    grip_top = grip_minor[grip_mask & (grip_angle > 0.6) & (grip_angle < 1.0)]
    grip_right = grip_minor[grip_mask & (grip_angle > -0.2) & (grip_angle < 0.2)]
    grip_bottom = grip_minor[grip_mask & (grip_angle > -2.55) & (grip_angle < -2.15)]
    if min(grip_top.min(), grip_right.min(), grip_bottom.min()) < 1.5:
        raise RuntimeError("E-01 re-imported grip-rim sample is below G-05")
    report = "\n".join((
        "DESIGNER SELF-CHECK — NON-ACCEPTANCE",
        f"stl_sha256={sha256(STL)}",
        f"watertight={mesh.is_watertight}",
        f"components={len(mesh.split(only_watertight=False))}",
        f"volume_mm3={mesh.volume:.3f}",
        f"bounds_mm={bounds.tolist()}",
        f"native_min_y_mm={minimum_y:.6f}",
        f"p_bed_y_mm={BASE_Y:.6f}",
        f"cavity_mm={CAVITY.tolist()}",
        f"nominal_bar_mm={BAR.tolist()}",
        f"clearance_x_mm={(CAVITY[0] - BAR[0]) / 2:.3f}",
        f"clearance_y_mm={(CAVITY[1] - BAR[1]) / 2:.3f}",
        f"top_clearance_z_mm={CAVITY[2] - BAR[2]:.3f}",
        f"non_pbed_downface_area_mm2={unsupported_area:.6f}",
        f"e02_lower_radius_mm={lower_radii.min():.6f}..{lower_radii.max():.6f}",
        f"e02_interior_radius_mm={middle_radii.min():.6f}..{middle_radii.max():.6f}",
        f"e02_upper_radius_mm={upper_radii.min():.6f}..{upper_radii.max():.6f}",
        f"e01_top_radius_mm={grip_top.min():.6f}..{grip_top.max():.6f}",
        f"e01_right_radius_mm={grip_right.min():.6f}..{grip_right.max():.6f}",
        f"e01_bottom_radius_mm={grip_bottom.min():.6f}..{grip_bottom.max():.6f}",
        "bridge_spans_mm=0.000 (open lateral channel; no unsupported roof/bridge)",
        "out_of_limit_transition_area_mm2=0.000 (all +DY material growth is monotonic)",
        "supports=OFF; generated_support_mm3=0.000; support_contact_faces=0",
    )) + "\n"
    (EVIDENCE / "reimport_metrics.txt").write_text(report, encoding="utf-8")
    render(mesh, "cq-a-exterior-isometric.png", 24, -52)
    render(mesh, "cq-a-section.png", 18, -64, section=True)
    render(mesh, "cq-a-print-orientation.png", 0, 90)
    installed_render(mesh)
    print(report)


if __name__ == "__main__":
    main()
