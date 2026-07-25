"""
render_views.py -- matplotlib render of the re-imported stick_reference.stl
(Chromium PNG capture is unreliable in this environment; matplotlib is the
reliable path per the commission instructions).

Produces stick_reference_view.png: an isometric 3D view of the plain
cylinder plus a true-proportion 2D cross-section outline (mid-shaft,
Z=75) confirming the constant Ø30.0mm circular section.
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
    intensity = 0.6 + 0.4 * diffuse
    base = np.array(base_rgb, dtype=float)
    colors = base[None, :] * intensity[:, None]
    return np.clip(colors, 0, 1)


def plot_mesh(ax, mesh, base_rgb, max_edge=4.0):
    fine = mesh.subdivide_to_size(max_edge=max_edge, max_iter=12)
    verts = fine.vertices[fine.faces]
    colors = shaded_facecolors(fine, base_rgb)
    coll = Poly3DCollection(verts, facecolors=colors, edgecolors="none")
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
    mesh = trimesh.load("stick_reference.stl")
    assert mesh.is_watertight, "re-imported STL is not watertight"
    base_wood = (0.62, 0.46, 0.28)

    fig = plt.figure(figsize=(14, 7))

    # ---- Panel 1: isometric 3D view ----
    ax1 = fig.add_subplot(121, projection="3d")
    plot_mesh(ax1, mesh, base_wood)
    set_equal_aspect(ax1, mesh.bounds)
    ax1.view_init(elev=18, azim=-60)
    ax1.set_xlabel("X mm")
    ax1.set_ylabel("Y mm")
    ax1.set_zlabel("Z (shaft axis) mm")
    ax1.set_title("stick_reference.stl -- isometric view\n"
                  "plain right-circular cylinder, Ø30.0mm (M-001) x 150mm\n"
                  "(length parametrized, not measured -- F-003 not evidenced;\n"
                  "no dome/end-cap modeled -- F-002/F-003 deliberately omitted)")

    # ---- Panel 2: true-proportion mid-shaft cross-section outline ----
    section = mesh.section(plane_origin=[0, 0, 75.0], plane_normal=[0, 0, 1])
    ax2 = fig.add_subplot(122)
    if section is not None:
        for loop in section.discrete:
            xs, ys = loop[:, 0], loop[:, 1]
            ax2.fill(xs, ys, facecolor=(0.85, 0.78, 0.68), edgecolor="black", linewidth=1.2)
    ax2.set_xlabel("X mm")
    ax2.set_ylabel("Y mm")
    ax2.set_title("Mid-shaft (Z=75) cross-section outline\n"
                  "true circle, Ø30.0mm (F-004: true-circularity assumption)")
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig("stick_reference_view.png", dpi=160)
    plt.close(fig)
    print("wrote stick_reference_view.png")


if __name__ == "__main__":
    main()
