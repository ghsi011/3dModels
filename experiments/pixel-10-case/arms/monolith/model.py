from pathlib import Path
import cadquery as cq

PARAMETER_PROVENANCE = {
    "PHONE_W/PHONE_H/PHONE_D": ["Google official specifications", "high"],
    "PHONE_CORNER_R/CAMERA_BAR_*": ["official hardware diagram visual proportion", "low"],
    "SIDE_CLEAR/END_CLEAR/WALL/BACK_THICKNESS": ["3d-modeling FDM design reference", "high"],
    "RIGHT_CONTROL_*/BOTTOM_OPEN_*/TOP_OPEN_*": ["official hardware diagram relative layout", "low"],
}

PHONE_W = 72.0
PHONE_H = 152.8
PHONE_D = 8.6
PHONE_CORNER_R = 12.0
CAMERA_BAR_W = 64.0
CAMERA_BAR_H = 24.0
CAMERA_BAR_Y = 50.0
SIDE_CLEAR = 0.30
END_CLEAR = 0.30
BACK_THICKNESS = 1.60
WALL = 1.80
SCREEN_LIP = 1.05
OUTER_CORNER_R = 14.4
INNER_CORNER_R = 12.6
RIGHT_CONTROL_Y = 17.0
RIGHT_CONTROL_H = 39.0
BOTTOM_USB_W = 15.0
BOTTOM_OPEN_Y = 7.0
TOP_MIC_W = 5.0
TOP_OPEN_Y = 5.0
BED_CHAMFER = 0.30

OUTER_W = PHONE_W + 2 * (WALL + SIDE_CLEAR)
OUTER_H = PHONE_H + 2 * (WALL + END_CLEAR)
INNER_W = PHONE_W + 2 * SIDE_CLEAR
INNER_H = PHONE_H + 2 * END_CLEAR
CASE_H = BACK_THICKNESS + PHONE_D + SCREEN_LIP


def rounded_rect(width, height, radius, z0, height_z):
    r = min(radius, width / 2, height / 2)
    solid = cq.Workplane("XY").box(width - 2*r, height, height_z,
                                    centered=(True, True, False)).translate((0, 0, z0))
    solid = solid.union(cq.Workplane("XY").box(width, height - 2*r, height_z,
                                                 centered=(True, True, False)).translate((0, 0, z0)))
    for x in (-width/2 + r, width/2 - r):
        for y in (-height/2 + r, height/2 - r):
            solid = solid.union(cq.Workplane("XY").circle(r).extrude(height_z).translate((x, y, z0)))
    return solid


ref_part = rounded_rect(PHONE_W, PHONE_H, PHONE_CORNER_R, BACK_THICKNESS, PHONE_D)

outer = rounded_rect(OUTER_W, OUTER_H, OUTER_CORNER_R, 0, CASE_H)
inner = rounded_rect(INNER_W, INNER_H, INNER_CORNER_R, BACK_THICKNESS, CASE_H + 1)
case = outer.cut(inner)

camera_window = rounded_rect(CAMERA_BAR_W, CAMERA_BAR_H, 4.0, -0.1, BACK_THICKNESS + 0.2)
camera_window = camera_window.translate((0, CAMERA_BAR_Y, 0))
case = case.cut(camera_window)

right_open = cq.Workplane("XY").box(WALL + 2.0, RIGHT_CONTROL_H, CASE_H,
                                     centered=(False, True, False))
right_open = right_open.translate((INNER_W/2 - 0.5, RIGHT_CONTROL_Y, BACK_THICKNESS - 0.1))
case = case.cut(right_open)

bottom_open = cq.Workplane("XY").box(OUTER_W - 10.0, BOTTOM_OPEN_Y, CASE_H,
                                      centered=(True, False, False))
bottom_open = bottom_open.translate((0, -OUTER_H/2 - 0.2, BACK_THICKNESS - 0.1))
case = case.cut(bottom_open)
top_open = cq.Workplane("XY").box(TOP_MIC_W, TOP_OPEN_Y, CASE_H,
                                   centered=(True, False, False))
top_open = top_open.translate((0, OUTER_H/2 - TOP_OPEN_Y + 0.2, BACK_THICKNESS - 0.1))
case = case.cut(top_open)

try:
    case = case.edges("<Z").chamfer(BED_CHAMFER)
except Exception:
    pass

assert case.val().isValid(), "CadQuery generated an invalid solid"
assert case.val().Volume() > 1000, "Case volume unexpectedly small"

OUT = Path(__file__).resolve().parent
cq.exporters.export(case, str(OUT / "pixel10_case.stl"), tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(case, str(OUT / "pixel10_case.step"))
cq.exporters.export(ref_part, str(OUT / "phone_reference.stl"), tolerance=0.01, angularTolerance=0.1)
section = case.intersect(cq.Workplane("XY").box(OUTER_W + 2, OUTER_H + 2, CASE_H + 2,
                                                centered=(False, True, False)))
cq.exporters.export(section, str(OUT / "case_section.stl"), tolerance=0.01, angularTolerance=0.1)
print({"case_bbox": (OUTER_W, OUTER_H, CASE_H), "case_volume_mm3": round(case.val().Volume(), 1)})
