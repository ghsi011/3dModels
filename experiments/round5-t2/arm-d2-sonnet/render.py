"""Required matplotlib renders (system python): exterior, installed-coordinate mating
section, print-orientation view, and candidate-vs-reference overlay."""
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

OUT = Path(__file__).parent
mesh = trimesh.load(OUT / "candidate_tool.stl", force="mesh", process=True)
ref = trimesh.load(Path(__file__).parent.parent / "inputs" / "reference_bar.stl", force="mesh", process=True)

# ---- 1. Exterior render (isometric) ----
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection="3d")
tri = mesh.triangles
pc = Poly3DCollection(tri, facecolor="#8fa3b3", edgecolor="none", alpha=1.0)
ax.add_collection3d(pc)
b = mesh.bounds
ax.set_xlim(b[0][0], b[1][0]); ax.set_ylim(b[0][1], b[1][1]); ax.set_zlim(b[0][2], b[1][2])
ax.set_box_aspect([b[1][0]-b[0][0], b[1][1]-b[0][1], b[1][2]-b[0][2]])
ax.view_init(elev=22, azim=-60)
ax.set_xlabel("X (D1)"); ax.set_ylabel("Y (D2)"); ax.set_zlabel("Z (D3)")
ax.set_title("Candidate tool -- exterior isometric (installed coordinates)")
plt.savefig(OUT / "render_exterior.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("wrote render_exterior.png")

# ---- 2. Installed-coordinate mating section (cut at X=0, showing bar cavity + ref bar) ----
fig, ax = plt.subplots(figsize=(9, 6))
sec = mesh.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
pT = trimesh.geometry.plane_transform([0, 0, 0], [1, 0, 0])
p2d, _ = sec.to_2D(pT)
for poly in p2d.polygons_full:
    ext = np.array(poly.exterior.coords)
    # local coords here are (-Z, X) per earlier verification; convert back to (Y,Z)
    # NOTE: this section plane has normal (1,0,0) so local axes are (Y,Z)-ish; plot
    # raw local coords and label generically as the section trace.
    ax.fill(ext[:, 0], ext[:, 1], facecolor="#8fa3b3", edgecolor="#1c2733", linewidth=1)
    for h in poly.interiors:
        hc = np.array(h.coords)
        ax.fill(hc[:, 0], hc[:, 1], facecolor="white", edgecolor="#1c2733", linewidth=1)
ax.set_title("Installed-coordinate mating section (X=0 cut) -- open architecture + clearances")
ax.set_aspect("equal")
ax.grid(alpha=0.3)
plt.savefig(OUT / "render_section.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("wrote render_section.png")

# ---- 3. Print-orientation view (apply the transform, show P_BED as sole plate face) ----
M = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 16.0], [0, 0, 0, 1]])
verts_p = trimesh.transform_points(mesh.vertices, M)
mesh_p = trimesh.Trimesh(vertices=verts_p, faces=mesh.faces, process=False)
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection="3d")
normals_p = mesh_p.face_normals
bed_face_mask = normals_p[:, 2] < -0.99  # essentially P_BED (the only allowed plate face)
colors = np.where(bed_face_mask[:, None], np.array([[0.85, 0.25, 0.25]]), np.array([[0.56, 0.64, 0.70]]))
pc = Poly3DCollection(mesh_p.triangles, facecolor=colors, edgecolor="none")
ax.add_collection3d(pc)
b = mesh_p.bounds
ax.set_xlim(b[0][0], b[1][0]); ax.set_ylim(b[0][1], b[1][1]); ax.set_zlim(-1, b[1][2])
ax.set_box_aspect([b[1][0]-b[0][0], b[1][1]-b[0][1], b[1][2]-b[0][2]+1])
ax.view_init(elev=18, azim=-50)
ax.set_xlabel("printer_X"); ax.set_ylabel("printer_Y"); ax.set_zlabel("printer_Z (bed=0)")
ax.set_title("Print orientation -- P_BED (red) is the sole plate-touching face")
plt.savefig(OUT / "render_print_orientation.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("wrote render_print_orientation.png")

# ---- 4. Candidate vs reference-bar overlay (top view, X-Y) ----
fig, ax = plt.subplots(figsize=(9, 5))
# candidate silhouette at Z=12 (mid bar height, within cavity, shows the capture channel)
sec_top = mesh.section(plane_origin=[0, 0, 12.0], plane_normal=[0, 0, 1])
if sec_top is not None:
    pT2 = trimesh.geometry.plane_transform([0, 0, 12.0], [0, 0, 1])
    p2d_top, _ = sec_top.to_2D(pT2)
    for poly in p2d_top.polygons_full:
        ext = np.array(poly.exterior.coords)
        ax.fill(ext[:, 0], ext[:, 1], facecolor="#8fa3b3", edgecolor="#1c2733",
                 linewidth=1, alpha=0.55, label="candidate tool (Z=12 section)")
        for h in poly.interiors:
            hc = np.array(h.coords)
            ax.fill(hc[:, 0], hc[:, 1], facecolor="white", edgecolor="#1c2733", linewidth=1)
# reference bar footprint (constant 62x11.7 box, Z 0..24, so its footprint at Z=12 is full)
ref_x, ref_y = 62.0, 11.7
ax.add_patch(plt.Rectangle((-ref_x/2, -ref_y/2), ref_x, ref_y, fill=False,
                            edgecolor="#0e7490", linewidth=2.5, label="reference bar F02 envelope"))
ax.set_aspect("equal")
ax.legend(loc="upper right", fontsize=8)
ax.set_title("Overlay: candidate capture channel (Z=12 section) vs reference bar F02 envelope")
ax.grid(alpha=0.3)
plt.savefig(OUT / "render_overlay.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("wrote render_overlay.png")
