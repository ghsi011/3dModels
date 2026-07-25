"""
render_clip.py -- matplotlib renders of the re-imported clip.stl (Chromium PNG
capture is unreliable in this environment; matplotlib is the reliable path,
per this commission's instructions -- same approach as
tests/eval/broom-step2-reference/render_views.py).

Produces three files:
  clip_exterior_view.png       -- isometric + front + top exterior views
  clip_section_fin_grip.png    -- mid-height 2D cross-section with the Ø30 rod
                                   overlaid (to scale) showing the fin-tip
                                   interference, plus a 3D half-section with
                                   the rod seated
  clip_print_orientation.png   -- annotated print-orientation view (bed plane,
                                   ring axis, "C-opening lateral")
"""
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches

ROD_D = 30.0
ROD_R = ROD_D / 2.0
CLIP_WIDTH = 24.0


def load_repaired(path):
    tm = trimesh.load(path, force="mesh")
    tm.update_faces(tm.nondegenerate_faces())
    tm.merge_vertices()
    return tm


def shaded_facecolors(mesh, base_rgb, light_dir=(0.4, -0.5, 0.75)):
    light = np.array(light_dir, dtype=float)
    light /= np.linalg.norm(light)
    normals = mesh.face_normals
    diffuse = np.clip(normals @ light, 0.0, 1.0)
    intensity = 0.55 + 0.45 * diffuse
    base = np.array(base_rgb, dtype=float)
    colors = base[None, :] * intensity[:, None]
    return np.clip(colors, 0, 1)


def plot_mesh(ax, mesh, base_rgb, max_edge=1.5, alpha=1.0):
    fine = mesh.subdivide_to_size(max_edge=max_edge, max_iter=12)
    verts = fine.vertices[fine.faces]
    colors = shaded_facecolors(fine, base_rgb)
    if alpha < 1.0:
        colors = np.column_stack([colors, np.full(len(colors), alpha)])
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


def rod_mesh(z_lo, z_hi, sections=96):
    rod = trimesh.creation.cylinder(radius=ROD_R, height=(z_hi - z_lo), sections=sections)
    rod.apply_translation((0, 0, (z_hi + z_lo) / 2.0))
    return rod


def render_exterior(clip):
    fig = plt.figure(figsize=(15, 5.5))
    views = [
        ("Isometric (front)", 22, -50),
        ("Isometric (back)", 22, 130),
        ("Top (+Z, print-up view)", 89, -90),
    ]
    base_rgb = (0.55, 0.62, 0.72)  # PETG-ish grey-blue
    for i, (title, elev, azim) in enumerate(views):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        plot_mesh(ax, clip, base_rgb)
        set_equal_aspect(ax, clip.bounds)
        ax.view_init(elev=elev, azim=azim)
        ax.set_xlabel("X mm")
        ax.set_ylabel("Y mm")
        ax.set_zlabel("Z mm")
        ax.set_title(title)
    fig.suptitle(
        "clip.stl -- broom-holder clip candidate (PETG, I-1 compliant-retention grip)\n"
        "partial-wrap C-clip (210deg wrap, 150deg mouth), fin-tip ID 29.2mm vs Ø30.0mm rod "
        "(-0.8mm diametral interference); flat mounting flange with 2x Ø4.8mm clearance holes",
        fontsize=10,
    )
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig("clip_exterior_view.png", dpi=160)
    plt.close(fig)
    print("wrote clip_exterior_view.png")


def render_section_fin_grip(clip):
    fig = plt.figure(figsize=(15, 6.5))

    # ---- Panel 1: mid-height 2D cross-section, clip profile + rod overlay ----
    z_mid = CLIP_WIDTH / 2.0
    ax1 = fig.add_subplot(131)
    sec = clip.section(plane_origin=[0, 0, z_mid], plane_normal=[0, 0, 1])
    if sec is not None:
        planar, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z_mid], [0, 0, 1]))
        for loop in planar.discrete:
            xs, ys = loop[:, 0], loop[:, 1]
            ax1.fill(xs, ys, facecolor=(0.75, 0.80, 0.86), edgecolor="black", linewidth=1.2, zorder=2)
    rod_circle = mpatches.Circle((0, 0), ROD_R, facecolor=(0.85, 0.55, 0.25, 0.55),
                                  edgecolor=(0.6, 0.3, 0.05), linewidth=1.5, zorder=3,
                                  label="Ø30.0mm rod (nominal, concentric)")
    ax1.add_patch(rod_circle)
    ax1.set_xlim(-24, 8)
    ax1.set_ylim(-20, 20)
    ax1.set_aspect("equal")
    ax1.grid(alpha=0.3)
    ax1.set_xlabel("X mm")
    ax1.set_ylabel("Y mm")
    ax1.set_title(f"Mid-height (Z={z_mid:.0f}mm) section\nclip profile vs Ø30.0mm rod overlay\n"
                   "(rod overlaps the fin-tip wall -- the INTENDED elastic interference)")
    ax1.legend(loc="lower left", fontsize=8)

    # ---- Panel 2: zoom on one fin tip / mouth region ----
    ax2 = fig.add_subplot(132)
    if sec is not None:
        for loop in planar.discrete:
            xs, ys = loop[:, 0], loop[:, 1]
            ax2.fill(xs, ys, facecolor=(0.75, 0.80, 0.86), edgecolor="black", linewidth=1.2, zorder=2)
    ax2.add_patch(mpatches.Circle((0, 0), ROD_R, facecolor=(0.85, 0.55, 0.25, 0.55),
                                   edgecolor=(0.6, 0.3, 0.05), linewidth=1.5, zorder=3))
    ax2.set_xlim(-2, 10)
    ax2.set_ylim(6, 18)
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)
    ax2.set_xlabel("X mm")
    ax2.set_ylabel("Y mm")
    ax2.set_title("Zoom: +Y fin tip / mouth\n(the pinch point the rod must\nelastically clear on snap-on)")

    # ---- Panel 3: 3D half-section with the rod seated ----
    ax3 = fig.add_subplot(133, projection="3d")
    half = clip.slice_plane(plane_origin=[0, 0, 0], plane_normal=[0, -1, 0], cap=True)
    if half is not None and len(half.faces):
        plot_mesh(ax3, half, (0.55, 0.62, 0.72))
    rod = rod_mesh(-4, 28)
    rod_half = rod.slice_plane(plane_origin=[0, 0, 0], plane_normal=[0, -1, 0], cap=True)
    if rod_half is not None and len(rod_half.faces):
        plot_mesh(ax3, rod_half, (0.85, 0.55, 0.25), alpha=0.75)
    set_equal_aspect(ax3, clip.bounds)
    ax3.view_init(elev=14, azim=-35)
    ax3.set_xlabel("X mm")
    ax3.set_ylabel("Y mm")
    ax3.set_zlabel("Z mm")
    ax3.set_title("3D half-section (Y<=0)\nrod seated concentric, showing\nfin grip engagement over the band")

    fig.suptitle("Interface I-1 -- fin grip on the Ø30.0mm rod (compliant retention)", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("clip_section_fin_grip.png", dpi=160)
    plt.close(fig)
    print("wrote clip_section_fin_grip.png")


def render_print_orientation(clip):
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, clip, (0.55, 0.62, 0.72))

    # bed plane patch at Z=0
    bx, by = clip.bounds[:, 0], clip.bounds[:, 1]
    pad = 4
    xs = [bx[0] - pad, bx[1] + pad, bx[1] + pad, bx[0] - pad]
    ys = [by[0] - pad, by[1] + pad, by[1] + pad, by[0] - pad]
    # simple bed outline using Line3DCollection via plot
    bed_x = [bx[0] - pad, bx[1] + pad, bx[1] + pad, bx[0] - pad, bx[0] - pad]
    bed_y = [by[0] - pad, by[0] - pad, by[1] + pad, by[1] + pad, by[0] - pad]
    bed_z = [0, 0, 0, 0, 0]
    ax.plot(bed_x, bed_y, bed_z, color="red", linewidth=1.5, label="print bed (Z=0)")

    set_equal_aspect(ax, clip.bounds)
    ax.view_init(elev=20, azim=-55)
    ax.set_xlabel("X mm")
    ax.set_ylabel("Y mm")
    ax.set_zlabel("Z mm (build/layer direction)")
    ax.set_title(
        "Print orientation -- IDENTITY model-to-printer transform\n"
        "ring axis vertical (=print Z): every layer is a complete horizontal\n"
        "C-slice -> support-free; mouth opens toward +X = LATERAL in-plane\n"
        "(per print_plan_checks.json S-01, matches the plan's \"C-opening lateral\" guidance)"
    )
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig("clip_print_orientation.png", dpi=160)
    plt.close(fig)
    print("wrote clip_print_orientation.png")


def main():
    clip = load_repaired("clip.stl")
    assert clip.is_watertight, "re-imported clip.stl is not watertight"
    render_exterior(clip)
    render_section_fin_grip(clip)
    render_print_orientation(clip)


if __name__ == "__main__":
    main()
