"""
render_views.py -- matplotlib renders of the re-imported watch_reference.stl
(Chromium PNG capture is unreliable in this environment; matplotlib is the
reliable path per the commission instructions).

Produces:
  watch_reference_top_view.png  -- top-down view (crystal side up), showing
                                    the round case/bezel, the button-envelope
                                    bosses on the D2_BUTTON_AXIS (+X/-X), and
                                    the band stubs on the D3_BAND_AXIS (+Y/-Y).
  watch_reference_side_view.png -- side/profile view plus a true-proportion
                                    2D cross-section outline (X=0 plane)
                                    showing the flat caseback (Z=0, no
                                    charge-pad geometry), case thickness, and
                                    band-stub exit height.
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


def plot_mesh(ax, mesh, base_rgb, alpha=1.0, max_edge=1.5):
    # Subdivide first: CadQuery's big flat/curved faces export as coarse triangles, which
    # starves mplot3d's per-polygon average-depth z-sort of resolution and lets a far
    # triangle bleed through a near one. Finer triangles give the sort enough granularity.
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
    z_exaggeration so a ~15mm thickness is legible next to a ~67mm footprint. Axis
    tick values stay real mm -- only the box_aspect ratio is exaggerated -- and the
    title must say so; this is a labeled illustrative distortion, not a measurement."""
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
    mesh = trimesh.load("watch_reference.stl")
    assert mesh.is_watertight, "re-imported STL is not watertight"
    base_teal = (0.30, 0.55, 0.58)

    # ---- View 1: top-down (crystal face up), looking down -Z ----
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, mesh, base_teal)
    set_equal_aspect(ax, mesh.bounds)
    ax.view_init(elev=89, azim=-90)   # near-top-down, +X (button axis) to the right
    ax.set_xlabel("X (D2_BUTTON_AXIS) mm")
    ax.set_ylabel("Y (D3_BAND_AXIS) mm")
    ax.set_zlabel("Z (D1_AXIS) mm")
    ax.set_title("watch_reference.stl -- top view: round case/bezel (F-001),\n"
                 "button-envelope bosses +/-X (F-002), band stubs +/-Y (F-004)")
    plt.tight_layout()
    fig.savefig("watch_reference_top_view.png", dpi=160)
    plt.close(fig)

    # ---- View 2: side/profile 3D view + true-proportion 2D cross-section outline (X=0) ----
    Z_EXAGGERATION = 3   # labeled distortion only, ticks stay in real mm
    fig = plt.figure(figsize=(14, 8))
    ax1 = fig.add_subplot(121, projection="3d")
    plot_mesh(ax1, mesh, (0.75, 0.45, 0.30))
    set_z_exaggerated_aspect(ax1, mesh.bounds, Z_EXAGGERATION)
    ax1.view_init(elev=8, azim=-90)   # near side-on, band axis (Y) horizontal
    ax1.set_xlabel("X mm")
    ax1.set_ylabel("Y (D3_BAND_AXIS) mm")
    ax1.set_zlabel("Z (D1_AXIS) mm")
    ax1.set_title(f"Side/profile view, Z exaggerated {Z_EXAGGERATION}x for legibility\n"
                  "NOTE: no side-profile evidence exists (OQ-05) -- case is a plain\n"
                  "right cylinder, not tapered/stepped; caseback (Z=0) is flat, no\n"
                  "charge-contact geometry modeled (F-003/OQ-01, blocking, unmodeled)")

    # 2D cross-section outline through the X=0 plane (case profile + band-stub exit).
    # Use the section's raw 3D vertices (section.discrete, global coords) and plot Y,Z
    # directly -- NOT section.to_2D()/.to_planar() without an explicit plane_transform,
    # which re-origins on a path-dependent frame that need not align with global Y/Z
    # (see cadquery-patterns.md item 5: "hole centers silently stop matching datums").
    section = mesh.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    ax2 = fig.add_subplot(122)
    if section is not None:
        for loop in section.discrete:
            ys, zs = loop[:, 1], loop[:, 2]
            ax2.fill(ys, zs, facecolor=(0.85, 0.9, 0.88), edgecolor="black", linewidth=1.2)
    ax2.axhline(0, color="gray", lw=0.5, ls="--")
    ax2.axhline(14.9, color="gray", lw=0.5, ls="--")
    ax2.text(-33, 0.6, "D0_CASEBACK Z=0 (flat -- no charge-pad cuts)", fontsize=8, color="gray")
    ax2.text(-33, 15.4, "crystal apex Z=14.9", fontsize=8, color="gray")
    ax2.set_xlabel("Y (D3_BAND_AXIS) mm")
    ax2.set_ylabel("Z (D1_AXIS) mm")
    ax2.set_title("X=0 section outline: plain right-cylinder case profile\n"
                 "(CASE_THICKNESS=14.9) + band stubs at +/-Y lugs")
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)

    plt.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig("watch_reference_side_view.png", dpi=160)
    plt.close(fig)

    print("wrote watch_reference_top_view.png and watch_reference_side_view.png")


if __name__ == "__main__":
    main()
