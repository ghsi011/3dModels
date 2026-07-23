# /// script
# dependencies = ["cadquery==2.8.0"]
# ///
# ─── How to run ───
# python experiments/pixel-10-case/arms/team/model.py

from __future__ import annotations

import importlib.util
from pathlib import Path

import cadquery as cq


# Accepted contracts: dimensions.md r3, print_plan.md r1, ref-2 fixture.
BODY_WIDTH_MM = 72.0  # M-002
BODY_HEIGHT_MM = 152.8  # M-001
BODY_DEPTH_MM = 8.6  # M-003
PHONE_CORNER_RADIUS_MM = 10.0  # M-004 nominal; compliant relief covers 7--13 mm
CAVITY_CLEARANCE_MM = 0.35  # P-003 nominal per side; coupon variants 0.25/0.35/0.45
SIDE_WALL_MM = 1.6  # P-001, four 0.4 mm lines
BACK_WALL_MM = 1.4  # P-002, wireless-charging region
SCREEN_LIP_HEIGHT_MM = 1.2  # P-011
SCREEN_OPENING_OVERTRAVEL_MM = 1.0
BED_CHAMFER_MM = 0.3  # P-010
REAR_BACK_Z_MM = CAVITY_CLEARANCE_MM + BACK_WALL_MM

# F-003 / P-005: nominal plus 2.5 mm uncertainty per side plus 0.5 mm clearance.
CAMERA_OPENING_WIDTH_MM = 66.5
CAMERA_OPENING_HEIGHT_MM = 28.0
CAMERA_OPENING_TOP_Y_MM = 142.3  # >= M-008 nominal top + 3.0 mm
CAMERA_LIP_WALL_MM = 1.2  # P-011
CAMERA_LIP_TOP_Z_MM = REAR_BACK_Z_MM

# Bounded-relief geometry from P-006, P-007, and P-008.
CONTROL_RELIEF_Y_MIN_MM = 42.0
CONTROL_RELIEF_Y_MAX_MM = 122.0
BOTTOM_OPENING_WIDTH_MM = 58.0  # >=18 mm USB-C; leaves only protected corner returns
BOTTOM_OPENING_DEPTH_MM = 9.0
TOP_RELIEF_WIDTH_MM = 8.0
TOP_RELIEF_DEPTH_MM = 5.0


def rounded_rectangle(width: float, height: float, radius: float, z_min: float, depth: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .box(width, height, depth, centered=(True, True, False))
        .translate((0.0, height / 2.0, z_min))
        .edges("|Z")
        .fillet(radius)
    )


def horizontal_capsule(width: float, height: float, center_y: float, z_min: float, depth: float) -> cq.Workplane:
    straight_length = width - height
    core = (
        cq.Workplane("XY")
        .box(straight_length, height, depth, centered=(True, True, False))
        .translate((0.0, center_y, z_min))
    )
    left = cq.Workplane("XY").center(-straight_length / 2.0, center_y).circle(height / 2.0).extrude(depth).translate((0, 0, z_min))
    right = cq.Workplane("XY").center(straight_length / 2.0, center_y).circle(height / 2.0).extrude(depth).translate((0, 0, z_min))
    return core.union(left).union(right)


def load_reference() -> cq.Workplane:
    """Load ref-2 only as a hidden mating fixture; it is never exported."""
    source_path = Path(__file__).parent / "evidence/reference/ref-2/reference_ref2.py"
    spec = importlib.util.spec_from_file_location("pixel10_ref2_fixture", source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load accepted reference fixture: {source_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixture = module.ref_part
    if not isinstance(fixture, cq.Workplane):
        raise TypeError("Accepted reference fixture did not expose a CadQuery Workplane")
    return fixture


OUTER_WIDTH_MM = BODY_WIDTH_MM + 2.0 * (CAVITY_CLEARANCE_MM + SIDE_WALL_MM)
OUTER_HEIGHT_MM = BODY_HEIGHT_MM + 2.0 * (CAVITY_CLEARANCE_MM + SIDE_WALL_MM)
OUTER_CORNER_RADIUS_MM = PHONE_CORNER_RADIUS_MM + CAVITY_CLEARANCE_MM + SIDE_WALL_MM
OUTER_Z_MIN_MM = -(BODY_DEPTH_MM + CAVITY_CLEARANCE_MM + SCREEN_LIP_HEIGHT_MM)
OUTER_DEPTH_MM = BODY_DEPTH_MM + 2.0 * CAVITY_CLEARANCE_MM + SCREEN_LIP_HEIGHT_MM + BACK_WALL_MM
CAVITY_Z_MIN_MM = OUTER_Z_MIN_MM - SCREEN_OPENING_OVERTRAVEL_MM
CAVITY_DEPTH_MM = CAVITY_CLEARANCE_MM - CAVITY_Z_MIN_MM
CAVITY_CORNER_RADIUS_MM = PHONE_CORNER_RADIUS_MM + CAVITY_CLEARANCE_MM

outer_shell = rounded_rectangle(
    OUTER_WIDTH_MM, OUTER_HEIGHT_MM, OUTER_CORNER_RADIUS_MM, OUTER_Z_MIN_MM, OUTER_DEPTH_MM
).faces(">Z").edges().chamfer(BED_CHAMFER_MM)
cavity = rounded_rectangle(
    BODY_WIDTH_MM + 2.0 * CAVITY_CLEARANCE_MM,
    BODY_HEIGHT_MM + 2.0 * CAVITY_CLEARANCE_MM,
    CAVITY_CORNER_RADIUS_MM,
    CAVITY_Z_MIN_MM,
    CAVITY_DEPTH_MM,
)
case = outer_shell.cut(cavity)

camera_center_y = CAMERA_OPENING_TOP_Y_MM - CAMERA_OPENING_HEIGHT_MM / 2.0
camera_opening = horizontal_capsule(CAMERA_OPENING_WIDTH_MM, CAMERA_OPENING_HEIGHT_MM, camera_center_y, -1.0, 12.0)
camera_rim_outer = horizontal_capsule(
    CAMERA_OPENING_WIDTH_MM + 2.0 * CAMERA_LIP_WALL_MM,
    CAMERA_OPENING_HEIGHT_MM + 2.0 * CAMERA_LIP_WALL_MM,
    camera_center_y,
    BACK_WALL_MM - CAMERA_LIP_WALL_MM,
    CAMERA_LIP_TOP_Z_MM - BACK_WALL_MM + CAMERA_LIP_WALL_MM,
)
camera_rim = camera_rim_outer.cut(camera_opening)
case = case.cut(camera_opening).union(camera_rim)

right_relief = cq.Workplane("XY").box(
    12.0,
    CONTROL_RELIEF_Y_MAX_MM - CONTROL_RELIEF_Y_MIN_MM,
    24.0,
    centered=(True, True, True),
).translate((OUTER_WIDTH_MM / 2.0, (CONTROL_RELIEF_Y_MIN_MM + CONTROL_RELIEF_Y_MAX_MM) / 2.0, -4.0))
bottom_opening = cq.Workplane("XY").box(BOTTOM_OPENING_WIDTH_MM, BOTTOM_OPENING_DEPTH_MM, 24.0, centered=(True, True, True)).translate((0.0, 0.0, -4.0))
top_relief = cq.Workplane("XY").box(TOP_RELIEF_WIDTH_MM, TOP_RELIEF_DEPTH_MM, 24.0, centered=(True, True, True)).translate((0.0, BODY_HEIGHT_MM, -4.0))
case = case.cut(right_relief).cut(bottom_opening).cut(top_relief)
if not case.val().isValid():
    raise RuntimeError("CadQuery generated an invalid candidate solid")

# Hidden verification fixture, retained in source coordinates and deliberately not exported.
ref_part = load_reference()


def print_oriented(part: cq.Workplane) -> cq.Workplane:
    """Apply P-001's installed-to-printer transform and place rear exterior on the bed."""
    rotated = part.rotate((0, 0, 0), (1, 0, 0), 180.0)
    return rotated.translate((0.0, 0.0, -rotated.val().BoundingBox().zmin))


def export() -> None:
    target = Path(__file__).resolve().parent
    printable_case = print_oriented(case)
    cq.exporters.export(printable_case, str(target / "pixel10_case_cq_a.stl"), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(printable_case, str(target / "pixel10_case_cq_a.step"))
    bbox = printable_case.val().BoundingBox()
    print("DESIGNER SELF-CHECK - NON-AUTHORITATIVE")
    print("valid", printable_case.val().isValid())
    print("print_bbox_mm", round(bbox.xlen, 3), round(bbox.ylen, 3), round(bbox.zlen, 3))
    print("volume_mm3", round(printable_case.val().Volume(), 3))


if __name__ == "__main__":
    export()
