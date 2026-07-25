"""
render_cradle.py -- matplotlib renders of the re-imported cradle.stl (+ the accepted
watch_reference.stl seated inside it). Chromium PNG capture is unreliable in this
environment; matplotlib is the reliable path (same convention as
tests/eval/garmin-step2-reference/render_views.py).

Produces the three renders the commission asks for, plus a coupon render:
  cradle_exterior_view.png    -- iso exterior view, installed/print pose (STAND_BASE_PLANE
                                  on the ground plane, back-tilt visible).
  cradle_installed_section.png -- multi-panel: (a) pocket-local X=0 half-section with the
                                  watch seated (shows the button/band relief notches), (b) a
                                  pocket-local section through one retention-lip finger's own
                                  azimuth (shows the lip/S-01 support region + the watch
                                  seated against it), (c) an installed-pose 3D iso view of the
                                  same half-section.
  cradle_print_orientation.png -- side view with the print bed (Z=0) drawn explicitly, the
                                  back-tilt angle labeled, and the S-01 support region called
                                  out on the lip's outward/topside face.
  cradle_coupon_view.png       -- the standalone fit-coupon STL, iso view.
"""
import math

import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


def fill_loops_with_holes(ax, loops, facecolor, edgecolor="black", linewidth=1.0, alpha=1.0):
    """Fill a set of closed 2D loops (each an (N,2) array) as ONE shape with proper holes,
    using matplotlib's nonzero-winding PathPatch -- plain per-loop ax.fill() paints a
    notch/hole's own boundary as solid material instead of leaving it open (verified against
    the actual mesh with ray casts; this is a rendering-only artifact, not a geometry defect,
    but it visually misrepresents the open relief notches, so render it correctly instead)."""
    if not loops:
        return
    verts = []
    codes = []
    for loop in loops:
        pts = np.asarray(loop)[:, :2]
        verts.append(pts[0])
        codes.append(MplPath.MOVETO)
        for p in pts[1:]:
            verts.append(p)
            codes.append(MplPath.LINETO)
        verts.append(pts[0])
        codes.append(MplPath.CLOSEPOLY)
    path = MplPath(np.array(verts), codes)
    patch = PathPatch(path, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth, alpha=alpha)
    ax.add_patch(patch)

TILT_DEG = 27.5          # must match cradle_model.py
WEDGE_HEIGHT = 18.0       # must match cradle_model.py


def shaded_facecolors(mesh, base_rgb, light_dir=(0.4, -0.5, 0.75)):
    light = np.array(light_dir, dtype=float)
    light /= np.linalg.norm(light)
    normals = mesh.face_normals
    diffuse = np.clip(normals @ light, 0.0, 1.0)
    intensity = 0.45 + 0.55 * diffuse
    base = np.array(base_rgb, dtype=float)
    colors = base[None, :] * intensity[:, None]
    return np.clip(colors, 0, 1)


def plot_mesh(ax, mesh, base_rgb, alpha=1.0, max_edge=1.5):
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


def watch_in_pocket_local_frame():
    """The seated watch, in the SAME pocket-local frame as cradle_model.py's puck before
    the world-frame tilt (floor at Z'=0, axis = local +Z, identical convention to
    watch_reference.py -- see cradle_model.py's frame note). No transform needed: the
    reference build and this cradle share the same pocket-local origin/axis by
    construction."""
    return trimesh.load("../garmin-step2-reference/watch_reference.stl")


def rotate_translate_to_world(mesh, tilt_deg=TILT_DEG, wedge_height=WEDGE_HEIGHT):
    """Same rotate-about-world-X-through-origin, then translate-by-(0,0,wedge_height)
    recipe cradle_model.py applies to the puck -- brings a pocket-local mesh into the
    installed/print (world) frame."""
    m = mesh.copy()
    theta = math.radians(tilt_deg)
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)],
    ])
    m.vertices = m.vertices @ Rx.T
    m.vertices += np.array([0, 0, wedge_height])
    return m


def main():
    cradle = trimesh.load("cradle.stl")
    assert cradle.is_watertight, "re-imported cradle.stl is not watertight"
    watch_local = watch_in_pocket_local_frame()
    watch_world = rotate_translate_to_world(watch_local)

    base_grey = (0.62, 0.64, 0.66)
    base_teal = (0.30, 0.55, 0.58)

    # ======================================================================
    # 1. EXTERIOR VIEW -- installed/print pose, iso angle, STAND_BASE_PLANE visible at Z=0
    # ======================================================================
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, cradle, base_grey)
    set_equal_aspect(ax, cradle.bounds)
    # draw the bed plane (Z=0) as a translucent grid for orientation reference
    (xmin, ymin, _), (xmax, ymax, _) = cradle.bounds
    xs = np.linspace(xmin - 5, xmax + 5, 2)
    ys = np.linspace(ymin - 5, ymax + 5, 2)
    XX, YY = np.meshgrid(xs, ys)
    ax.plot_surface(XX, YY, np.zeros_like(XX), color="0.85", alpha=0.35, shade=False)
    ax.view_init(elev=20, azim=-60)
    ax.set_xlabel("X mm")
    ax.set_ylabel("Y mm")
    ax.set_zlabel("Z mm (printer, bed-normal)")
    ax.set_title(
        "cradle.stl -- exterior, installed/print pose\n"
        f"STAND_BASE_PLANE at Z=0 (bed, shaded), back-tilt {TILT_DEG:.1f} deg from vertical\n"
        "identity model-to-printer transform (no separate print-frame rotation)"
    )
    plt.tight_layout()
    fig.savefig("cradle_exterior_view.png", dpi=160)
    plt.close(fig)

    # ======================================================================
    # 2. INSTALLED SECTION -- watch seated, lip/support region visible
    # ======================================================================
    fig = plt.figure(figsize=(18, 6.5))

    # --- (a) pocket-local X=0 half-section: general bore + button/band relief notches ---
    ax1 = fig.add_subplot(131)
    sec_c = cradle_local = None
    cradle_local = rotate_translate_to_world(cradle.copy())  # placeholder, unused
    # Build a pocket-local-frame copy of the cradle by inverse-transforming the exported
    # (world-frame) STL back to pocket-local coordinates -- inverse of rotate_translate_to_world.
    theta = math.radians(TILT_DEG)
    Rx_inv = np.array([
        [1, 0, 0],
        [0, math.cos(theta), math.sin(theta)],
        [0, -math.sin(theta), math.cos(theta)],
    ])
    cradle_local = cradle.copy()
    cradle_local.vertices = (cradle_local.vertices - np.array([0, 0, WEDGE_HEIGHT])) @ Rx_inv.T

    section_a = cradle_local.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    if section_a is not None:
        fill_loops_with_holes(ax1, [loop[:, 1:3] for loop in section_a.discrete], (0.85, 0.87, 0.88))
    watch_section_a = watch_local.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
    if watch_section_a is not None:
        fill_loops_with_holes(ax1, [loop[:, 1:3] for loop in watch_section_a.discrete],
                               (0.30, 0.55, 0.58, 0.55), edgecolor="darkslategray", linewidth=1.2)
    ax1.set_xlim(-45, 35)
    ax1.set_ylim(-38, 18)
    ax1.axhline(0, color="gray", lw=0.5, ls="--")
    ax1.set_xlabel("local Y (D3_BAND_AXIS-ish) mm")
    ax1.set_ylabel("local Z' (pocket axis) mm")
    ax1.set_title(
        "(a) pocket-local X=0 section\nwatch seated (teal) in cradle bore (grey)\n"
        "band-axis (90/270 deg) relief notches visible as gaps in the wall"
    )
    ax1.set_aspect("equal")
    ax1.grid(alpha=0.3)

    # --- (b) pocket-local section through one lip finger's azimuth (41.5 deg) ---
    ax2 = fig.add_subplot(132)
    FINGER_DEG = 41.5
    n_perp = (math.sin(math.radians(FINGER_DEG)), -math.cos(math.radians(FINGER_DEG)), 0.0)
    section_b = cradle_local.section(plane_origin=[0, 0, 0], plane_normal=n_perp)
    # project onto (radial-in-plane, Z) coordinates for a clean 2D plot: radial = signed
    # distance from the Z axis along the finger's own azimuthal direction
    dir_in_plane = (math.cos(math.radians(FINGER_DEG)), math.sin(math.radians(FINGER_DEG)), 0.0)

    def to_radial(loop):
        radial = loop[:, 0] * dir_in_plane[0] + loop[:, 1] * dir_in_plane[1]
        return np.column_stack([radial, loop[:, 2]])

    if section_b is not None:
        fill_loops_with_holes(ax2, [to_radial(loop) for loop in section_b.discrete], (0.85, 0.87, 0.88))
    watch_section_b = watch_local.section(plane_origin=[0, 0, 0], plane_normal=n_perp)
    if watch_section_b is not None:
        fill_loops_with_holes(ax2, [to_radial(loop) for loop in watch_section_b.discrete],
                               (0.30, 0.55, 0.58, 0.55), edgecolor="darkslategray", linewidth=1.2)
    ax2.set_xlim(-45, 35)
    ax2.set_ylim(-38, 18)
    ax2.axhline(0, color="gray", lw=0.5, ls="--")
    ax2.annotate(
        "S-01 support region\n(outward/topside face)",
        xy=(24.5, 13.6), xytext=(2, 24),
        arrowprops=dict(arrowstyle="->", color="crimson"), color="crimson", fontsize=8,
    )
    ax2.set_xlabel(f"radial distance along {FINGER_DEG} deg azimuth, mm")
    ax2.set_ylabel("local Z' (pocket axis) mm")
    ax2.set_title(
        "(b) pocket-local section through a retention-lip finger\n"
        "watch case (teal) vs. lip overhang (grey) -- the small overlap\n"
        "at the lip is the intended compliant-flex retention engagement"
    )
    ax2.set_aspect("equal")
    ax2.grid(alpha=0.3)

    # --- (c) installed-pose 3D iso half-section (world frame) ---
    ax3 = fig.add_subplot(133, projection="3d")
    half_plane_normal = [1, 0, 0]
    cradle_half = cradle.slice_plane(plane_origin=[0, 0, 0], plane_normal=[-1, 0, 0], cap=True)
    watch_half = watch_world.slice_plane(plane_origin=[0, 0, 0], plane_normal=[-1, 0, 0], cap=True)
    if cradle_half is not None and len(cradle_half.faces):
        plot_mesh(ax3, cradle_half, base_grey, alpha=0.95)
    if watch_half is not None and len(watch_half.faces):
        plot_mesh(ax3, watch_half, base_teal, alpha=0.95)
    set_equal_aspect(ax3, cradle.bounds)
    ax3.view_init(elev=12, azim=-60)
    ax3.set_xlabel("X mm")
    ax3.set_ylabel("Y mm")
    ax3.set_zlabel("Z mm")
    ax3.set_title("(c) installed-pose half-section (world/print frame)\nwatch seated (teal) in cradle (grey)")

    plt.tight_layout()
    fig.savefig("cradle_installed_section.png", dpi=150)
    plt.close(fig)

    # ======================================================================
    # 3. PRINT ORIENTATION VIEW -- bed plane explicit, tilt angle labeled, S-01 called out
    # ======================================================================
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, cradle, base_grey)
    (xmin, ymin, _), (xmax, ymax, _) = cradle.bounds
    xs = np.linspace(xmin - 5, xmax + 5, 2)
    ys = np.linspace(ymin - 5, ymax + 5, 2)
    XX, YY = np.meshgrid(xs, ys)
    ax.plot_surface(XX, YY, np.zeros_like(XX), color="0.7", alpha=0.45, shade=False)
    # tilt-angle reference lines: bed-normal (vertical) vs. pocket axis
    axis_local = np.array([0, 0, 1.0])
    theta = math.radians(TILT_DEG)
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)],
    ])
    axis_world = Rx @ axis_local
    origin = np.array([0, 0, WEDGE_HEIGHT])
    L = 20
    vert_line = np.array([origin, origin + np.array([0, 0, L])])
    tilt_line = np.array([origin, origin + L * axis_world])
    ax.add_collection3d(Line3DCollection([vert_line], colors="black", linestyles="dashed", linewidths=1.2))
    ax.add_collection3d(Line3DCollection([tilt_line], colors="crimson", linewidths=1.8))
    ax.text(*(origin + np.array([0, 0, L + 2])), "bed normal (0 deg)", color="black", fontsize=8)
    ax.text(*(origin + L * axis_world + np.array([2, 2, 0])), f"pocket axis ({TILT_DEG:.1f} deg back-tilt)",
            color="crimson", fontsize=8)
    set_equal_aspect(ax, cradle.bounds)
    ax.view_init(elev=10, azim=-90)
    ax.set_xlabel("X mm")
    ax.set_ylabel("Y mm (front/back)")
    ax.set_zlabel("Z mm (printer, bed-normal)")
    ax.set_title(
        "cradle.stl -- print orientation\n"
        "STAND_BASE_PLANE = printer Z=0 (bed, shaded); identity model-to-printer transform\n"
        f"pocket axis tilted {TILT_DEG:.1f} deg back from vertical (print_plan.md assumed 20-35 deg band)"
    )
    plt.tight_layout()
    fig.savefig("cradle_print_orientation.png", dpi=160)
    plt.close(fig)

    # ======================================================================
    # 4. COUPON VIEW
    # ======================================================================
    coupon = trimesh.load("cradle_coupon.stl")
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")
    plot_mesh(ax, coupon, (0.75, 0.45, 0.30))
    set_equal_aspect(ax, coupon.bounds)
    ax.view_init(elev=22, azim=-60)
    ax.set_xlabel("X mm")
    ax.set_ylabel("Y mm")
    ax.set_zlabel("Z' mm (pocket-local)")
    ax.set_title(
        "cradle_coupon.stl -- fit coupon\n"
        "~110 deg bore-arc segment, same wall (G-03) and pocket depth (G-02) as the full cradle"
    )
    plt.tight_layout()
    fig.savefig("cradle_coupon_view.png", dpi=160)
    plt.close(fig)

    print("wrote cradle_exterior_view.png, cradle_installed_section.png, "
          "cradle_print_orientation.png, cradle_coupon_view.png")


if __name__ == "__main__":
    main()
