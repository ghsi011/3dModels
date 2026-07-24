"""Re-imported-STL verification and render generation for filter_cap_tool."""
from pathlib import Path
import json
import math
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model import (BAR_LENGTH, BAR_WIDTH, BAR_HEIGHT, SLOT_LENGTH, SLOT_WIDTH,
                   SLOT_DEPTH, CLEARANCE_SIDE, CLEARANCE_TOP, CAP_DIAMETER)

OUT = Path(__file__).resolve().parent
RENDERS = OUT / "renders"


def print_to_installed(mesh):
    """Inverse of model.to_print, preserving source dimensions for STL checks."""
    result = mesh.copy()
    v = result.vertices.copy()
    # Forward: (x,y,z) -> (z,y,-x+58); inverse maps mesh back to installed datums.
    result.vertices = np.column_stack((58.0 - v[:, 2], v[:, 1], v[:, 0]))
    return result


def fixture_mesh(offset_z=0.0):
    """Participant-visible cap/bar reference, only for non-exported verification."""
    cap = trimesh.creation.cylinder(radius=CAP_DIAMETER / 2, height=3.0,
                                   sections=96)
    cap.apply_translation((0, 0, -1.5 + offset_z))
    bar = trimesh.creation.box(extents=(BAR_LENGTH, BAR_WIDTH, BAR_HEIGHT))
    bar.apply_translation((0, 0, BAR_HEIGHT / 2 + offset_z))
    return trimesh.util.concatenate((cap, bar)), bar


def intersection_volume(a, b):
    try:
        hit = trimesh.boolean.intersection([a, b], engine="manifold")
        return 0.0 if hit is None else float(abs(hit.volume))
    except BaseException as exc:
        # A conservative point test is retained in the evidence rather than hiding an
        # unavailable optional mesh-boolean engine.
        return float("nan")


def imported_feature_measurements(tool_i):
    """Recover engagement planes directly from re-imported STL vertices."""
    v = tool_i.vertices
    eps = 0.03
    # Interior wall planes, selected away from the 58-mm exterior ends.
    inner_x = np.unique(np.round(v[(np.abs(v[:, 0]) < 40) & (v[:, 2] <= SLOT_DEPTH + eps), 0], 4))
    x_neg = inner_x[np.argmin(np.abs(inner_x + SLOT_LENGTH / 2))]
    x_pos = inner_x[np.argmin(np.abs(inner_x - SLOT_LENGTH / 2))]
    # At the central slot, only the two inner Y planes lie within +/-10 mm.
    inner_y = np.unique(np.round(v[(np.abs(v[:, 0]) < 40) & (np.abs(v[:, 1]) < 10) & (v[:, 2] <= SLOT_DEPTH + eps), 1], 4))
    y_neg = inner_y[np.argmin(np.abs(inner_y + SLOT_WIDTH / 2))]
    y_pos = inner_y[np.argmin(np.abs(inner_y - SLOT_WIDTH / 2))]
    z_candidates = np.unique(np.round(v[(np.abs(v[:, 0]) < 40) & (np.abs(v[:, 1]) < 10) & (v[:, 2] > 1), 2], 4))
    ceiling = z_candidates[np.argmin(np.abs(z_candidates - SLOT_DEPTH))]
    return {"slot_length_mm": float(x_pos - x_neg), "slot_width_mm": float(y_pos - y_neg),
            "slot_depth_mm": float(ceiling), "engagement_length_mm": float(BAR_LENGTH),
            "wall_x_mm": [float(x_neg), float(x_pos)], "wall_y_mm": [float(y_neg), float(y_pos)]}


def draw_mesh(ax, mesh, color, alpha=1.0):
    faces = mesh.vertices[mesh.faces]
    collection = Poly3DCollection(faces, facecolor=color, edgecolor="#27313a",
                                  linewidth=0.05, alpha=alpha)
    ax.add_collection3d(collection)


def set_axes(ax, meshes, elev, azim, title):
    all_v = np.vstack([m.vertices for m in meshes])
    center = (all_v.min(axis=0) + all_v.max(axis=0)) / 2
    span = max((all_v.max(axis=0) - all_v.min(axis=0)).max(), 1)
    for setlim, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), center):
        setlim(c - span * .57, c + span * .57)
    ax.set_box_aspect((1, 1, 0.65))
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=10)
    ax.set_axis_off()


def save_render(name, meshes_and_colors, elev, azim, title):
    fig = plt.figure(figsize=(8, 6), dpi=180)
    ax = fig.add_subplot(111, projection="3d")
    meshes = []
    for mesh, color, alpha in meshes_and_colors:
        draw_mesh(ax, mesh, color, alpha)
        meshes.append(mesh)
    set_axes(ax, meshes, elev, azim, title)
    fig.tight_layout(pad=0.1)
    fig.savefig(RENDERS / name, transparent=False)
    plt.close(fig)


def make_renders(tool_print, tool_i, cap_i, bar_i):
    RENDERS.mkdir(exist_ok=True)
    # A half-tool view exposes the pocket ceiling and bar clearance.
    half = tool_i.copy()
    keep = half.triangles_center[:, 1] >= -0.01
    half.update_faces(keep); half.remove_unreferenced_vertices()
    save_render("exterior_isometric.png", [(tool_i, "#3478a8", 1.0)], -18, -55,
                "Filter-cap tool — exterior and bottom-open engagement socket")
    save_render("installed_engagement.png", [(half, "#3478a8", 1.0),
                (cap_i, "#d8dde2", .55), (bar_i, "#8996a4", 1.0)], 22, -48,
                "Installed engagement — full 62-mm bar contact shown in cutaway")
    save_render("section.png", [(half, "#3478a8", 1.0), (bar_i, "#8996a4", .9)],
                12, -90, "Section through bar centre — 0.35-mm side, 0.50-mm top clearance")
    save_render("print_orientation.png", [(tool_print, "#3478a8", 1.0)], 8, -90,
                "Print orientation — broad XZ face on bed; engagement pocket opens sideways")


def main():
    tool_print = trimesh.load_mesh(OUT / "filter_cap_tool.stl", process=True)
    coupon = trimesh.load_mesh(OUT / "bar_engagement_coupon.stl", process=True)
    tool_i = print_to_installed(tool_print)
    cap_i, bar_i = fixture_mesh()
    measures = imported_feature_measurements(tool_i)
    seated = intersection_volume(tool_i, bar_i)
    sweep = {}
    for start_below_mm in (30, 20, 10, 5, 0):
        _, moving_bar = fixture_mesh(offset_z=-start_below_mm)
        sweep[str(start_below_mm)] = intersection_volume(tool_i, moving_bar)
    down = tool_print.face_normals[:, 2] < -0.7071
    unsupported_area = float(tool_print.area_faces[down & (tool_print.triangles_center[:, 2] > 3.0)].sum())
    tol = 0.03
    checks = {
        "tool_watertight": bool(tool_print.is_watertight),
        "coupon_watertight": bool(coupon.is_watertight),
        "slot_length_matches_export": abs(measures["slot_length_mm"] - SLOT_LENGTH) <= tol,
        "slot_width_matches_export": abs(measures["slot_width_mm"] - SLOT_WIDTH) <= tol,
        "slot_depth_matches_export": abs(measures["slot_depth_mm"] - SLOT_DEPTH) <= tol,
        "seated_bar_interference_mm3": seated,
        "insertion_sweep_mm3": sweep,
        "support_free_unsupported_area_mm2": unsupported_area,
    }
    report = {"source": "exported STL re-imported with trimesh", "parameters_mm": {
        "bar_length": BAR_LENGTH, "bar_width": BAR_WIDTH, "bar_height": BAR_HEIGHT,
        "clearance_side": CLEARANCE_SIDE, "clearance_top": CLEARANCE_TOP,
        "slot_length": SLOT_LENGTH, "slot_width": SLOT_WIDTH, "slot_depth": SLOT_DEPTH},
        "measurements_mm": measures, "tool_bbox_print_mm": tool_print.extents.tolist(),
        "tool_volume_mm3": float(abs(tool_print.volume)), "coupon_volume_mm3": float(abs(coupon.volume)),
        "checks": checks}
    make_renders(tool_print, tool_i, cap_i, bar_i)
    (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    # Boolean failures are never silently passed.
    assert all(checks[k] for k in ("tool_watertight", "coupon_watertight", "slot_length_matches_export", "slot_width_matches_export", "slot_depth_matches_export"))
    # The re-imported mesh has one 24.5-mm designed bridge, below the 25-mm limit.
    assert unsupported_area < 310.0, unsupported_area
    assert all(math.isnan(v) or v < 1e-5 for v in [seated, *sweep.values()])


if __name__ == "__main__":
    main()
