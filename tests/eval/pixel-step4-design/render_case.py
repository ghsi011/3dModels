"""
render_case.py - matplotlib renders of the re-imported case.stl (+ phone_reference.stl
for the installed view). Chromium PNG capture is unreliable in this environment per the
commission instructions; matplotlib is the reliable path (matches step2's render_views.py).

Produces:
  case_exterior_view.png      - 3/4 exterior view: rim, side walls, camera boss on back.
  case_installed_section.png  - half-section (X<=0 kept) with the phone SEATED inside,
                                 proving the snug wall fit + camera relief architecture.
  case_print_orientation.png  - the model after the print_plan's exact transform
                                 (180deg about model +X, R=diag(1,-1,-1)) with the bed
                                 plane drawn at printer Z=0.
"""
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def shaded_facecolors(mesh, base_rgb, light_dir=(0.4, -0.5, 0.75)):
    light = np.array(light_dir, dtype=float)
    light /= np.linalg.norm(light)
    normals = mesh.face_normals
    diffuse = np.clip(normals @ light, 0.0, 1.0)
    intensity = 0.45 + 0.55 * diffuse
    base = np.array(base_rgb, dtype=float)
    colors = base[None, :] * intensity[:, None]
    return np.clip(colors, 0, 1)


def plot_mesh(ax, mesh, base_rgb, alpha=1.0, max_edge=3.0):
    fine = mesh.subdivide_to_size(max_edge=max_edge, max_iter=12)
    verts = fine.vertices[fine.faces]
    colors = shaded_facecolors(fine, base_rgb)
    coll = Poly3DCollection(verts, facecolors=colors, edgecolors=(0, 0, 0, 0.04),
                             linewidths=0.1, alpha=alpha)
    ax.add_collection3d(coll)


def set_equal_aspect(ax, bounds):
    (xmin, ymin, zmin), (xmax, ymax, zmax) = bounds
    span = max(xmax - xmin, ymax - ymin, zmax - zmin) / 2
    cx, cy, cz = (xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2
    ax.set_xlim(cx - span, cx + span)
    ax.set_ylim(cy - span, cy + span)
    ax.set_zlim(cz - span, cz + span)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass


def main():
    case = trimesh.load("case.stl")
    phone = trimesh.load("../step2-reference-pixel7/phone_reference.stl")
    assert case.is_watertight, "re-imported case.stl is not watertight"

    case_teal = (0.30, 0.55, 0.50)
    phone_blue = (0.35, 0.55, 0.75)

    # ---- View 1: exterior, 3/4 back view (camera boss + button window side) ----
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, case, case_teal)
    set_equal_aspect(ax, case.bounds)
    ax.view_init(elev=-25, azim=-60)
    ax.set_xlabel("X (D5_LEFT -> D4_RIGHT) mm")
    ax.set_ylabel("Y (D3_BOT -> D2_TOP) mm")
    ax.set_zlabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax.set_title("case.stl - exterior: camera boss (back), button windows (D4_RIGHT),\n"
                  "USB-C + grilles (D3_BOT), top mic relief (D2_TOP), open rim (max Z)")
    plt.tight_layout()
    fig.savefig("case_exterior_view.png", dpi=160)
    plt.close(fig)

    # ---- View 2: installed half-section (X<=0 kept), phone SEATED inside ----
    case_half = case.slice_plane(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0], cap=True)
    phone_half = phone.slice_plane(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0], cap=True)
    assert case_half.is_watertight and phone_half.is_watertight

    fig = plt.figure(figsize=(15, 7.5))
    ax1 = fig.add_subplot(121, projection="3d")
    plot_mesh(ax1, case_half, case_teal, alpha=0.55)
    plot_mesh(ax1, phone_half, phone_blue, alpha=1.0)
    set_equal_aspect(ax1, case.bounds)
    ax1.view_init(elev=14, azim=-70)
    ax1.set_xlabel("X mm")
    ax1.set_ylabel("Y (D3_BOT -> D2_TOP) mm")
    ax1.set_zlabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax1.set_title("Installed half-section (X<=0 kept)\ncase (teal, translucent) wrapping the "
                  "seated phone (blue)")

    # 2D true-proportion outline at X=0: shows snug side-wall gap top-to-bottom,
    # camera relief pocket + boss standing proud below the flat back, and the raised
    # lip above the screen plane.
    case_section = case.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    phone_section = phone.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    ax2 = fig.add_subplot(122)
    if case_section is not None:
        for loop in case_section.discrete:
            ys, zs = loop[:, 1], loop[:, 2]
            ax2.fill(ys, zs, facecolor=(0.75, 0.9, 0.87), edgecolor=(0.1, 0.4, 0.35),
                      linewidth=1.2, alpha=0.85, zorder=1)
    if phone_section is not None:
        for loop in phone_section.discrete:
            ys, zs = loop[:, 1], loop[:, 2]
            ax2.fill(ys, zs, facecolor=(0.75, 0.85, 0.95), edgecolor=(0.15, 0.3, 0.55),
                      linewidth=1.2, alpha=0.95, zorder=2)
    ax2.axhline(0, color="gray", lw=0.5, ls="--")
    ax2.axhline(8.7, color="gray", lw=0.5, ls="--")
    ax2.text(-95, 1.3, "D0_BACK Z=0", fontsize=8, color="gray")
    ax2.text(-95, 9.9, "D6_SCREEN Z=8.7", fontsize=8, color="gray")
    ax2.set_xlabel("Y (D3_BOT -> D2_TOP) mm")
    ax2.set_ylabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax2.set_title("X=0 section outline: case (teal) vs phone (blue), true proportion\n"
                  "camera boss protects the bump; raised lip above the screen plane")
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig("case_installed_section.png", dpi=160)
    plt.close(fig)

    # ---- View 3: planned print orientation (rim-down) ----
    # print_plan.md: 180deg rotation about model +X axis, R = diag(1,-1,-1);
    # (x,y,z) -> (x,-y,-z); translation is Z-only so the open-rim plane lands at
    # printer Z=0. Z_TOP (model) = 9.9mm -> printer_z = -( -9.9) ... apply directly.
    R = np.diag([1.0, -1.0, -1.0])
    verts = case.vertices @ R.T
    z_top_model = case.bounds[1][2]           # 9.90mm, open rim (bed-contact landmark)
    verts[:, 2] = verts[:, 2] - (-z_top_model)  # shift so rim lands at printer Z=0
    printed = trimesh.Trimesh(vertices=verts, faces=case.faces, process=False)

    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, printed, case_teal)
    (xmin, ymin, zmin), (xmax, ymax, zmax) = printed.bounds
    pad = 3
    xx, yy = np.meshgrid([xmin - pad, xmax + pad], [ymin - pad, ymax + pad])
    ax.plot_surface(xx, yy, np.zeros_like(xx), color=(0.6, 0.6, 0.6), alpha=0.25)
    set_equal_aspect(ax, printed.bounds)
    ax.view_init(elev=14, azim=-60)
    ax.set_xlabel("printer X mm")
    ax.set_ylabel("printer Y mm")
    ax.set_zlabel("printer Z mm (bed = 0)")
    ax.set_title("Planned print orientation: open rim on the bed (Z=0, gray plane),\n"
                  "camera boss becomes the last-printed top feature (self-supporting)")
    plt.tight_layout()
    fig.savefig("case_print_orientation.png", dpi=160)
    plt.close(fig)

    print("wrote case_exterior_view.png, case_installed_section.png, case_print_orientation.png")
    print("printed-orientation bounds:", printed.bounds.tolist())


if __name__ == "__main__":
    main()
