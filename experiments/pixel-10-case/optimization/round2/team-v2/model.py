from pathlib import Path
import math
import cadquery as cq
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent

PHONE_X, PHONE_Y, PHONE_Z = 72.0, 152.8, 8.6
CLEAR_XY, CLEAR_REAR = 0.30, 0.30
CAV_X, CAV_Y, CAV_Z = PHONE_X + 2 * CLEAR_XY, PHONE_Y + 2 * CLEAR_XY, PHONE_Z + CLEAR_REAR
PHONE_R, CAV_R = 12.0, 12.30
BACK, WALL, LIP_PROUD = 1.30, 1.80, 1.10
OUTER_X, OUTER_Y, OUTER_R = CAV_X + 2 * WALL, CAV_Y + 2 * WALL, 14.0
Z_REAR, Z_TOP = -BACK, PHONE_Z + LIP_PROUD
CX, CY = PHONE_X / 2, PHONE_Y / 2

CAM_X0, CAM_X1, CAM_Y0, CAM_Y1, CAM_R = 2.0, 70.0, 107.0, 150.0, 3.0
BOTTOM_X0, BOTTOM_X1 = 8.0, 64.0
TOP_X0, TOP_X1 = 28.0, 44.0
RIGHT_Y0, RIGHT_Y1 = 45.0, 130.0

LAND_HALF_AXIS = 1.0 / (2 * math.sqrt(2))
XMIN, ZMIN = CX - OUTER_X / 2, Z_REAR
LAND_SUM = XMIN + ZMIN + 2 * LAND_HALF_AXIS
LAND_MID = (XMIN + LAND_HALF_AXIS, CY, ZMIN + LAND_HALF_AXIS)


def rounded_box(cx, cy, width, height, radius, z0, depth):
    part = cq.Workplane("XY").box(width - 2 * radius, height, depth, centered=(True, True, False)).translate((cx, cy, z0))
    part = part.union(cq.Workplane("XY").box(width, height - 2 * radius, depth, centered=(True, True, False)).translate((cx, cy, z0)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            part = part.union(cq.Workplane("XY").circle(radius).extrude(depth).translate((cx + sx * (width / 2 - radius), cy + sy * (height / 2 - radius), z0)))
    return part


def make_case():
    outer = rounded_box(CX, CY, OUTER_X, OUTER_Y, OUTER_R, Z_REAR, Z_TOP - Z_REAR)
    profile = (cq.Workplane("XZ").polyline([
        (XMIN, ZMIN + 2 * LAND_HALF_AXIS), (XMIN, Z_TOP + 2),
        (CX + OUTER_X / 2 + 2, Z_TOP + 2), (CX + OUTER_X / 2 + 2, ZMIN),
        (XMIN + 2 * LAND_HALF_AXIS, ZMIN)
    ]).close().extrude(220, both=True))
    body = outer.intersect(profile)
    cavity = rounded_box(CX, CY, CAV_X, CAV_Y, CAV_R, 0.0, Z_TOP + 3)
    body = body.cut(cavity)
    body = body.cut(rounded_box((CAM_X0 + CAM_X1) / 2, (CAM_Y0 + CAM_Y1) / 2,
                               CAM_X1 - CAM_X0, CAM_Y1 - CAM_Y0, CAM_R, Z_REAR - 1, BACK + 2))
    body = body.cut(cq.Workplane("XY").box(BOTTOM_X1 - BOTTOM_X0, 10, Z_TOP - Z_REAR + 3,
                                             centered=(True, True, False)).translate(((BOTTOM_X0 + BOTTOM_X1) / 2, 1.0, Z_REAR - 1)))
    body = body.cut(cq.Workplane("XY").box(TOP_X1 - TOP_X0, 10, Z_TOP - Z_REAR + 3,
                                             centered=(True, True, False)).translate(((TOP_X0 + TOP_X1) / 2, PHONE_Y - 1, Z_REAR - 1)))
    body = body.cut(cq.Workplane("XY").box(10, RIGHT_Y1 - RIGHT_Y0, Z_TOP - 1.5,
                                             centered=(True, True, False)).translate((PHONE_X + 2.0, (RIGHT_Y0 + RIGHT_Y1) / 2, 1.5)))
    body = body.edges(cq.selectors.BoxSelector((1, 106, Z_REAR - 0.01), (71, 151, Z_REAR + 0.01))).fillet(0.40)
    body = body.edges(cq.selectors.BoxSelector((-10, -10, Z_TOP - 0.01), (90, 170, Z_TOP + 0.01))).fillet(0.80)
    if not body.val().isValid() or len(body.val().Solids()) != 1:
        raise RuntimeError("case boolean did not yield one valid solid")
    return body


def phone_reference():
    return rounded_box(CX, CY, PHONE_X, PHONE_Y, PHONE_R, 0, PHONE_Z)


def mesh_from_shape(shape):
    temp = OUT / "_render_tmp.stl"
    cq.exporters.export(shape, str(temp), tolerance=0.025, angularTolerance=0.15)
    m = trimesh.load_mesh(temp, process=True)
    temp.unlink(missing_ok=True)
    return m


def plot_mesh(ax, mesh, color, alpha=1.0, title=""):
    faces = mesh.triangles
    if len(faces) > 6000:
        faces = faces[np.linspace(0, len(faces) - 1, 6000, dtype=int)]
    pc = Poly3DCollection(faces, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_collection3d(pc)
    bounds = mesh.bounds
    center, extent = bounds.mean(axis=0), (bounds[1] - bounds[0]).max() * .58
    ax.set_xlim(center[0] - extent, center[0] + extent)
    ax.set_ylim(center[1] - extent, center[1] + extent)
    ax.set_zlim(center[2] - extent, center[2] + extent)
    ax.set_box_aspect((1, 1.8, .35))
    ax.set_axis_off(); ax.set_title(title, fontsize=9)


def save_render(path, meshes, elev, azim, title):
    fig = plt.figure(figsize=(7, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    for mesh, color, alpha in meshes:
        plot_mesh(ax, mesh, color, alpha, title)
    ax.view_init(elev=elev, azim=azim)
    fig.tight_layout(); fig.savefig(path, transparent=False); plt.close(fig)


def save_exterior_overlay(case_mesh):
    iso = OUT / "_exterior_iso.png"
    save_render(iso, [(case_mesh, "#285a88", 1.0)], 24, -55, "Exterior / isometric")
    evidence = Image.open(OUT / "../../../evidence/input/pixel10_official_hardware_diagram.png").convert("RGBA")
    rear = evidence.crop((1100, 220, 1720, 1080))
    layer = Image.new("RGBA", rear.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    scale, body_left, body_bottom = 5.0, 100.0, 830.0
    def point(x, y): return (body_left + x * scale, body_bottom - y * scale)
    x0, y0 = point(-2.1, -1.546); x1, y1 = point(74.1, 154.9)
    draw.rounded_rectangle((x0, y1, x1, y0), radius=OUTER_R * scale, outline=(0, 235, 255, 235), width=5)
    ax0, ay0 = point(CAM_X0, CAM_Y0); ax1, ay1 = point(CAM_X1, CAM_Y1)
    draw.rounded_rectangle((ax0, ay1, ax1, ay0), radius=CAM_R * scale, outline=(255, 170, 0, 245), width=5)
    draw.text((15, 15), "S2 rear same-view overlay", fill=(0, 235, 255, 255))
    draw.text((15, 38), "cyan: case exterior; amber: conservative shared F14 aperture", fill=(0, 235, 255, 255))
    draw.text((15, 61), "S2 is relative-layout-only; no feature coordinate is inferred", fill=(0, 235, 255, 255))
    rear.alpha_composite(layer)
    left = Image.open(iso).convert("RGBA")
    canvas = Image.new("RGBA", (left.width + rear.width, max(left.height, rear.height)), "white")
    canvas.alpha_composite(left, (0, 0)); canvas.alpha_composite(rear, (left.width, 0))
    canvas.convert("RGB").save(OUT / "render_exterior.png")
    iso.unlink(missing_ok=True)


def render_all(case):
    case_mesh = mesh_from_shape(case)
    phone_mesh = mesh_from_shape(phone_reference())
    save_exterior_overlay(case_mesh)
    save_render(OUT / "render_fit.png", [(phone_mesh, "#c7cbd1", .22), (case_mesh, "#3477a8", .62)], 20, -48,
                "Transparent installed fit — open front +Z")
    fig, ax = plt.subplots(figsize=(9, 3), dpi=180)
    for mesh, color, width in ((case_mesh, "#d26a36", 2.4), (phone_mesh, "#777f8b", 1.3)):
        plane = mesh.section(plane_origin=[CX, CY, 0], plane_normal=[0, 1, 0])
        for line in plane.discrete:
            ax.plot(line[:, 0], line[:, 2], color=color, linewidth=width)
    ax.axhline(0, color="#b7b7b7", linewidth=.7)
    ax.text(CX, PHONE_Z + .35, "open front +Z; lip proud 1.10 mm", ha="center", fontsize=8)
    ax.text(CX, Z_REAR - .8, "rear wall 1.30 mm; cavity rear clearance 0.30 mm", ha="center", fontsize=8)
    ax.set_aspect("equal"); ax.set_xlim(-3, 75); ax.set_ylim(-2.8, 11.2)
    ax.set_xlabel("X from B datum (mm)"); ax.set_ylabel("Z from rear datum A (mm)")
    ax.set_title("Installed-coordinate mid-Y section: orange case, grey nominal phone")
    fig.tight_layout(); fig.savefig(OUT / "render_section.png"); plt.close(fig)
    oriented = case_mesh.copy(); v = oriented.vertices - np.array(LAND_MID)
    oriented.vertices = v @ np.array([[math.sqrt(.5),0,math.sqrt(.5)],[0,1,0],[-math.sqrt(.5),0,math.sqrt(.5)]]) + np.array([128,128,0])
    save_render(OUT / "render_print_orientation.png", [(oriented, "#4f8d54", 1.0)], 20, -55,
                "Print orientation — L contact land at Z=0, R_y(-45°)")


if __name__ == "__main__":
    case = make_case()
    cq.exporters.export(case, str(OUT / "pixel10_case.stl"), tolerance=0.025, angularTolerance=0.15)
    cq.exporters.export(case, str(OUT / "pixel10_case.step"))
    render_all(case)
    print("exported", OUT / "pixel10_case.stl")
