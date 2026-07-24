# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery==2.8.0", "matplotlib", "trimesh"]
# ///
# ─── How to run ───
# python .\model.py
from __future__ import annotations

from pathlib import Path

import cadquery as cq


OUT = Path(__file__).resolve().parent

BAR_LENGTH = 62.00
BAR_WIDTH = 11.70
BAR_HEIGHT = 24.00
CAP_RADIUS = 31.50
FIT_CLEAR_XY = 0.30
FIT_CLEAR_Z_TOP = 0.35
CAP_CLEARANCE = 0.60
MIN_WALL = 1.68
BED_CHAMFER = 0.30
CONTACT_RADIUS = 0.90
COMFORT_RADIUS = 1.50
GRIP_RIM_RADIUS = 1.60
BASE_EDGE_RADIUS = 1.80
BASE_SIDE_RADIUS = 1.60

CAVITY_X = BAR_LENGTH + 2.0 * FIT_CLEAR_XY
CAVITY_Y = BAR_WIDTH + 2.0 * FIT_CLEAR_XY
CAVITY_Z = BAR_HEIGHT + FIT_CLEAR_Z_TOP
CAVITY_FLOOR_Y = -CAVITY_Y / 2.0
CAVITY_TOP_Z = BAR_HEIGHT + FIT_CLEAR_Z_TOP
BASE_Y_MIN = -8.00
BASE_Y_MAX = -4.40
BODY_X = 84.00
BODY_Z_MIN = CAP_CLEARANCE
BODY_Z_MAX = 47.00
END_WALL = 2.40
RETAINING_Y = 8.00


def box(x_len: float, y_len: float, z_len: float, x: float, y: float, z: float) -> cq.Workplane:
    return cq.Workplane("XY").box(x_len, y_len, z_len).translate((x, y, z))


def make_tool() -> cq.Workplane:
    base = (cq.Workplane("XZ").center(0.0, (BODY_Z_MIN + BODY_Z_MAX) / 2.0).sketch()
            .rect(BODY_X, BODY_Z_MAX - BODY_Z_MIN).vertices().fillet(BASE_EDGE_RADIUS)
            .finalize().extrude(BASE_Y_MAX - BASE_Y_MIN).translate((0.0, BASE_Y_MAX, 0.0)))
    base = base.edges("<Y").chamfer(BED_CHAMFER)
    rail_z_min = BODY_Z_MIN + BASE_EDGE_RADIUS
    rail_z_len = BODY_Z_MAX - BODY_Z_MIN - 2.0 * BASE_EDGE_RADIUS
    rail_y = BASE_Y_MAX - BASE_SIDE_RADIUS
    relief_z = rail_z_min + rail_z_len / 2.0
    left_relief = box(BASE_SIDE_RADIUS, BASE_SIDE_RADIUS, rail_z_len,
                      -BODY_X / 2.0 + BASE_SIDE_RADIUS / 2.0, rail_y + BASE_SIDE_RADIUS / 2.0, relief_z)
    right_relief = box(BASE_SIDE_RADIUS, BASE_SIDE_RADIUS, rail_z_len,
                       BODY_X / 2.0 - BASE_SIDE_RADIUS / 2.0, rail_y + BASE_SIDE_RADIUS / 2.0, relief_z)
    left_round = cq.Workplane("XY").center(-BODY_X / 2.0 + BASE_SIDE_RADIUS, rail_y).circle(BASE_SIDE_RADIUS).extrude(rail_z_len).translate((0.0, 0.0, rail_z_min))
    right_round = cq.Workplane("XY").center(BODY_X / 2.0 - BASE_SIDE_RADIUS, rail_y).circle(BASE_SIDE_RADIUS).extrude(rail_z_len).translate((0.0, 0.0, rail_z_min))
    base = base.cut(left_relief).cut(right_relief).union(left_round).union(right_round)

    left_stop = box(END_WALL, RETAINING_Y - BASE_Y_MIN, CAVITY_Z - CAP_CLEARANCE,
                    -(CAVITY_X / 2.0 + END_WALL / 2.0), (RETAINING_Y + BASE_Y_MIN) / 2.0,
                    (CAVITY_TOP_Z + CAP_CLEARANCE) / 2.0).edges("|Y").fillet(CONTACT_RADIUS)
    right_stop = box(END_WALL, RETAINING_Y - BASE_Y_MIN, CAVITY_Z - CAP_CLEARANCE,
                     CAVITY_X / 2.0 + END_WALL / 2.0, (RETAINING_Y + BASE_Y_MIN) / 2.0,
                     (CAVITY_TOP_Z + CAP_CLEARANCE) / 2.0).edges("|Y").fillet(CONTACT_RADIUS)
    roof = box(CAVITY_X + 2.0 * END_WALL, RETAINING_Y - BASE_Y_MIN,
               MIN_WALL, 0.0, (RETAINING_Y + BASE_Y_MIN) / 2.0,
               CAVITY_TOP_Z + MIN_WALL / 2.0).edges("<Z").chamfer(CONTACT_RADIUS)
    grip = (cq.Workplane("XZ").circle(19.0).extrude(RETAINING_Y - BASE_Y_MIN)
            .edges("<Y").chamfer(BED_CHAMFER).edges(">Y").fillet(GRIP_RIM_RADIUS)
            .translate((0.0, RETAINING_Y, 46.0)))
    tool = base.union(left_stop).union(right_stop).union(roof).union(grip)
    mouth = box(CAVITY_X, CAVITY_Y, CAVITY_Z, 0.0,
                CAVITY_FLOOR_Y + CAVITY_Y / 2.0, CAVITY_TOP_Z / 2.0)
    tool = tool.cut(mouth)
    lead_in = (cq.Workplane("YZ").polyline([
        (CAVITY_FLOOR_Y, -0.01), (CAVITY_FLOOR_Y, CAP_CLEARANCE),
        (CAVITY_FLOOR_Y - CAP_CLEARANCE, -0.01),
    ]).close().extrude(CAVITY_X).translate((-CAVITY_X / 2.0, 0.0, 0.0)))
    tool = tool.cut(lead_in)
    if not tool.val().isValid():
        raise RuntimeError("CadQuery produced an invalid candidate solid")
    return tool


def export(tool: cq.Workplane) -> None:
    cq.exporters.export(tool, str(OUT / "cq-a-washer-filter-tool.stl"), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(tool, str(OUT / "cq-a-washer-filter-tool.step"))


if __name__ == "__main__":
    RESULT = make_tool()
    export(RESULT)
    print(f"volume_mm3={RESULT.val().Volume():.3f}")
    print(f"cavity_mm={CAVITY_X:.2f} x {CAVITY_Y:.2f} x {CAVITY_Z:.2f}")
