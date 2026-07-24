"""Designer render set (system python / matplotlib, non-acceptance).
Outputs: exterior, installed mating section, print-orientation, reference overlay."""
import numpy as np, trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

TOOL = trimesh.load("candidate_tool.stl", force="mesh", process=True)
LP = trimesh.load("candidate_coupon.stl", force="mesh", process=True)   # low-poly, same envelope
M = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 16.0], [0, 0, 0, 1]])

# bar F02 envelope (installed)
BAR = dict(x=(-31, 31), y=(-5.85, 5.85), z=(0, 24))


def poly3d(ax, mesh, facecolor="#8fa9c7", hl_mask=None, hl_color="#d1495b"):
    tris = mesh.triangles
    fc = np.array([matplotlib.colors.to_rgba(facecolor)] * len(tris))
    if hl_mask is not None:
        fc[hl_mask] = matplotlib.colors.to_rgba(hl_color)
    pc = Poly3DCollection(tris, facecolors=fc, edgecolor="#33445a", linewidths=0.2, alpha=1.0)
    ax.add_collection3d(pc)
    v = mesh.vertices
    for setlim, lo, hi in [(ax.set_xlim, v[:, 0].min(), v[:, 0].max()),
                           (ax.set_ylim, v[:, 1].min(), v[:, 1].max()),
                           (ax.set_zlim, v[:, 2].min(), v[:, 2].max())]:
        setlim(lo, hi)
    try:
        ax.set_box_aspect((v[:, 0].ptp(), v[:, 1].ptp(), v[:, 2].ptp()))
    except Exception:
        pass


# ---------- PNG 1: exterior (installed frame) ----------
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection="3d")
poly3d(ax, LP)
ax.set_title("Candidate tool - exterior (installed frame)\nhand grip + open bar-capture mouth (-Z)")
ax.set_xlabel("X = D1 (bar long)"); ax.set_ylabel("Y = D2"); ax.set_zlabel("Z = D3 (cap axis)")
ax.view_init(elev=22, azim=-58)
fig.tight_layout(); fig.savefig("render_exterior.png", dpi=130); plt.close(fig)


# ---------- PNG 2: installed mating section ----------
def section2d(mesh, origin, normal, ax_idx):
    s = mesh.section(plane_origin=origin, plane_normal=normal)
    out = []
    if s is not None:
        for poly in s.discrete:
            out.append(poly[:, ax_idx])
    return out

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4))
# X=0 : Y-Z plane (shows gable, cavity, open mouth, +-Y clearances)
for p in section2d(TOOL, [0, 0, 0], [1, 0, 0], (1, 2)):
    a1.plot(p[:, 0], p[:, 1], color="#33445a", lw=1.4)
a1.add_patch(plt.Rectangle((BAR["y"][0], BAR["z"][0]), 11.7, 24, color="#d1495b", alpha=.35, label="F02 bar 11.7x24"))
a1.axhline(0, color="#bf3b2b", ls="--", lw=.8); a1.axvline(0, color="#bf3b2b", ls="--", lw=.8)
a1.annotate("open mouth -> -Z", (0, 3.2), (0, -3), ha="center", color="#0e7490",
            arrowprops=dict(arrowstyle="->", color="#0e7490"))
a1.set_title("Section X=0 (Y-Z): gable roof self-supports;\ncavity open toward -Z; +-Y clearance 0.40 mm")
a1.set_xlabel("Y = D2 (mm)"); a1.set_ylabel("Z = D3 (mm)"); a1.set_aspect("equal"); a1.legend(fontsize=8)
# Y=0 : X-Z plane (shows 62 mm span, ceiling clearance, mouth)
for p in section2d(TOOL, [0, 0, 0], [0, 1, 0], (0, 2)):
    a2.plot(p[:, 0], p[:, 1], color="#33445a", lw=1.4)
a2.add_patch(plt.Rectangle((BAR["x"][0], BAR["z"][0]), 62, 24, color="#d1495b", alpha=.35, label="F02 bar 62x24"))
a2.axhline(0, color="#bf3b2b", ls="--", lw=.8); a2.axvline(0, color="#bf3b2b", ls="--", lw=.8)
a2.set_title("Section Y=0 (X-Z): full 62 mm engagement;\nend clearance 0.60 mm, top clearance 0.70 mm")
a2.set_xlabel("X = D1 (mm)"); a2.set_ylabel("Z = D3 (mm)"); a2.set_aspect("equal"); a2.legend(fontsize=8)
fig.suptitle("Installed-coordinate mating section (open architecture + clearances)")
fig.tight_layout(); fig.savefig("render_mating_section.png", dpi=130); plt.close(fig)


# ---------- PNG 3: print orientation (P_BED sole plate face) ----------
LPp = LP.copy(); LPp.apply_transform(M)   # to printer frame
TOOLp = TOOL.copy(); TOOLp.apply_transform(M)
cz = LPp.triangles[:, :, 2]
hl = np.max(np.abs(cz - 0.0), axis=1) <= 0.05   # faces on bed plane (P_BED)
fig = plt.figure(figsize=(13, 5.6))
ax = fig.add_subplot(121, projection="3d")
poly3d(ax, LPp, facecolor="#9bb8a0", hl_mask=hl, hl_color="#d1495b")
ax.set_title("Printer frame (3D)\nprinter_Z = Y+16 up; supports OFF")
ax.set_xlabel("printer_X"); ax.set_ylabel("printer_Y"); ax.set_zlabel("printer_Z")
ax.view_init(elev=18, azim=-62)
# side section printer_X=0 : printer_Y vs printer_Z, shows P_BED on the bed line
a2 = fig.add_subplot(122)
s = TOOLp.section(plane_origin=[0, 0, 0], plane_normal=[1, 0, 0])
bedmin, bedmax = 1e9, -1e9
if s is not None:
    for poly in s.discrete:
        a2.plot(poly[:, 1], poly[:, 2], color="#33445a", lw=1.4)
        onbed = poly[poly[:, 2] < 0.1]
        if len(onbed):
            bedmin = min(bedmin, onbed[:, 1].min()); bedmax = max(bedmax, onbed[:, 1].max())
a2.axhline(0, color="#8a5a00", lw=2.5, alpha=.6)
if bedmax > bedmin:
    a2.plot([bedmin, bedmax], [0, 0], color="#d1495b", lw=7, solid_capstyle="butt",
            label="P_BED land (printer_Z=0)")
a2.annotate("bed (printer_Z=0)", (a2.get_xlim()[0], 1.0), color="#8a5a00", fontsize=9)
a2.annotate("mouth opens -> +printer_Y", (-3, 16), (-20, 30), fontsize=9, color="#0e7490",
            arrowprops=dict(arrowstyle="->", color="#0e7490"))
a2.set_title("Side section printer_X=0: P_BED is the sole face at\nprinter_Z=0; all functional geometry >=0.5 mm above bed")
a2.set_xlabel("printer_Y (mm)"); a2.set_ylabel("printer_Z build (mm)"); a2.set_aspect("equal")
a2.legend(fontsize=8, loc="upper left")
fig.suptitle("Print orientation - P_BED (installed Y=-16) is the sole bed-contact face")
fig.tight_layout(); fig.savefig("render_print_orientation.png", dpi=130); plt.close(fig)


# ---------- PNG 4: overlay vs reference bar ----------
fig, (b1, b2) = plt.subplots(1, 2, figsize=(12, 5.4))
for p in section2d(TOOL, [0, 0, 12.0], [0, 0, 1], (0, 1)):   # Z=12 top view X-Y
    b1.plot(p[:, 0], p[:, 1], color="#33445a", lw=1.3)
b1.add_patch(plt.Rectangle((BAR["x"][0], BAR["y"][0]), 62, 11.7, color="#155e75", alpha=.4, label="reference bar 62x11.7"))
b1.axhline(0, color="#bf3b2b", ls="--", lw=.8); b1.axvline(0, color="#bf3b2b", ls="--", lw=.8)
b1.set_title("Top overlay Z=12 (X-Y): candidate cavity vs reference F02\ncentred on D1/D2"); b1.set_aspect("equal")
b1.set_xlabel("X = D1 (mm)"); b1.set_ylabel("Y = D2 (mm)"); b1.legend(fontsize=8)
for p in section2d(TOOL, [0, 0, 0], [0, 1, 0], (0, 2)):     # Y=0 side X-Z
    b2.plot(p[:, 0], p[:, 1], color="#33445a", lw=1.3)
b2.add_patch(plt.Rectangle((BAR["x"][0], BAR["z"][0]), 62, 24, color="#155e75", alpha=.4, label="reference bar 62x24"))
b2.axhline(0, color="#bf3b2b", ls="--", lw=.8); b2.axvline(0, color="#bf3b2b", ls="--", lw=.8)
b2.set_title("Side overlay Y=0 (X-Z): channel encloses bar\nwith clearances; open mouth below"); b2.set_aspect("equal")
b2.set_xlabel("X = D1 (mm)"); b2.set_ylabel("Z = D3 (mm)"); b2.legend(fontsize=8)
fig.suptitle("Candidate overlay vs accepted reference F02 envelope (62 x 11.7 x 24)")
fig.tight_layout(); fig.savefig("render_overlay.png", dpi=130); plt.close(fig)

print("renders written")
