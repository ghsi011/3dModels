"""
render_views.py — matplotlib renders of the re-imported phone_reference.stl
(Chromium PNG capture is unreliable in this environment; matplotlib is the
reliable path per the commission instructions.)

Produces:
  phone_reference_back_view.png   — oblique view of the back, camera bar,
                                     lens-oval recess, buttons, SIM tray,
                                     mic hole, USB-C, bottom grilles.
  phone_reference_side_section.png — half-section (X<=0 kept) side view plus
                                      a 2D cross-section outline through the
                                      camera-bump/flat-body/screen-plane.
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
    intensity = 0.45 + 0.55 * diffuse   # ambient floor so back-facing tris aren't near-black
    base = np.array(base_rgb, dtype=float)
    colors = base[None, :] * intensity[:, None]
    return np.clip(colors, 0, 1)


def plot_mesh(ax, mesh, base_rgb, alpha=1.0, max_edge=3.0):
    # Subdivide first: CadQuery's big flat faces export as ~2 giant triangles, which
    # starves mplot3d's per-polygon average-depth z-sort of resolution and lets a
    # far triangle bleed through a near one (visible as a diagonal seam). Finer
    # triangles give the sort enough granularity to order correctly.
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


def set_z_exaggerated_aspect(ax, bounds, z_exaggeration):
    """Tight (true-proportion) limits on X/Y, but the rendered BOX stretches Z by
    z_exaggeration so a ~2.7mm step is visible next to a 155mm length. Axis tick
    values stay real mm — only the box_aspect ratio is exaggerated — and the
    title must say so; this is a labeled illustrative distortion, not a
    measurement."""
    (xmin, ymin, zmin), (xmax, ymax, zmax) = bounds
    xr, yr, zr = xmax - xmin, ymax - ymin, zmax - zmin
    pad = 0.1 * max(xr, yr)
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    zc = (zmin + zmax) / 2
    zpad = max(zr, 1.0) * 0.6
    ax.set_zlim(zc - zpad, zc + zpad)
    try:
        ax.set_box_aspect((xr + 2 * pad, yr + 2 * pad, (zr + 2 * zpad) * z_exaggeration))
    except Exception:
        pass


def main():
    mesh = trimesh.load("phone_reference.stl")
    assert mesh.is_watertight, "re-imported STL is not watertight"
    base_blue = (0.35, 0.55, 0.75)

    # ---- View 1: back with camera bar, near-orthogonal view from behind ----
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, mesh, base_blue)
    set_equal_aspect(ax, mesh.bounds)
    ax.view_init(elev=-25, azim=-60)   # 3/4 view of the back (-Z outward normal) + right edge
    ax.set_xlabel("X (D5_LEFT -> D4_RIGHT) mm")
    ax.set_ylabel("Y (D3_BOT -> D2_TOP) mm")
    ax.set_zlabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax.set_title("phone_reference.stl — back view: camera bar / lens-oval recess /\n"
                  "buttons (D4_RIGHT) / SIM tray (D5_LEFT) / USB-C + grilles (D3_BOT)")
    plt.tight_layout()
    fig.savefig("phone_reference_back_view.png", dpi=160)
    plt.close(fig)

    # ---- View 2: half-section (keep X<=0) + 2D cross-section outline ----
    half = mesh.slice_plane(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0], cap=True)
    assert half.is_watertight, "half-section mesh is not watertight"

    Z_EXAGGERATION = 6   # labeled distortion only, ticks stay in real mm (see set_z_exaggerated_aspect)
    fig = plt.figure(figsize=(14, 7))
    ax1 = fig.add_subplot(121, projection="3d")
    plot_mesh(ax1, half, (0.75, 0.35, 0.35))
    set_z_exaggerated_aspect(ax1, half.bounds, Z_EXAGGERATION)
    ax1.view_init(elev=18, azim=-70)
    ax1.set_xlabel("X mm")
    ax1.set_ylabel("Y (D3_BOT -> D2_TOP) mm")
    ax1.set_zlabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax1.set_title(f"Half-section (X<=0 kept), Z exaggerated {Z_EXAGGERATION}x for legibility\n"
                  "cut face shows camera-bump step vs flat body")

    # 2D cross-section outline through the X=0 plane (camera-bump / body / screen profile).
    # Use the section's raw 3D vertices (section.discrete, global coords) and plot Y,Z
    # directly -- NOT section.to_2D()/.to_planar() without an explicit plane_transform,
    # which re-origins on a path-dependent frame that need not align with global Y/Z
    # (see cadquery-patterns.md item 5: "hole centers silently stop matching datums").
    section = mesh.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    ax2 = fig.add_subplot(122)
    if section is not None:
        for loop in section.discrete:
            ys, zs = loop[:, 1], loop[:, 2]
            ax2.fill(ys, zs, facecolor=(0.85, 0.85, 0.9), edgecolor="black", linewidth=1.2)
    ax2.axhline(0, color="gray", lw=0.5, ls="--")
    ax2.axhline(8.7, color="gray", lw=0.5, ls="--")
    ax2.text(-75, 1.3, "D0_BACK Z=0", fontsize=8, color="gray")
    ax2.text(-75, 9.9, "D6_SCREEN Z=8.7", fontsize=8, color="gray")
    ax2.set_xlabel("Y (D3_BOT -> D2_TOP) mm")
    ax2.set_ylabel("Z (D0_BACK -> D6_SCREEN) mm")
    ax2.set_title("X=0 section outline: flat body (T=8.7) +\ncamera bump to Z=-2.74 near D2_TOP")
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig("phone_reference_side_section.png", dpi=160)
    plt.close(fig)

    print("wrote phone_reference_back_view.png and phone_reference_side_section.png")


if __name__ == "__main__":
    main()
