from pathlib import Path

import cadquery as cq


OUT = Path(__file__).resolve().parent

PHONE_Z = 8.60
BACK = 1.30
WALL = 1.80
LIP_PROUD = 1.10
LANE_LENGTH = 35.0
LANE_CENTERS = (0.0, 12.0, 24.0, 36.0, 48.0)
CLEARANCE_PAIRS = ((0.20, 0.20), (0.25, 0.25), (0.30, 0.30), (0.35, 0.35), (0.40, 0.40))

REAR_PAD_INBOARD = 8.0
BASE_THICKNESS = 1.0
BRIDGE_Y_WIDTH = 2.0


def lane(center_x: float, side_clear: float, rear_clear: float) -> cq.Workplane:
    y0 = -LANE_LENGTH / 2
    inner_x = -side_clear
    outer_x = inner_x - WALL
    rear_outer_z = rear_clear - BACK
    top_z = PHONE_Z + LIP_PROUD

    rear = cq.Workplane("XY").box(WALL + REAR_PAD_INBOARD, LANE_LENGTH, BACK,
                                  centered=(False, False, False)).translate(
                                      (center_x + outer_x, y0, rear_outer_z))
    rail = cq.Workplane("XY").box(WALL, LANE_LENGTH, top_z - rear_outer_z,
                                  centered=(False, False, False)).translate(
                                      (center_x + outer_x, y0, rear_outer_z))
    return rear.union(rail).edges("|Y").fillet(0.40)


def make_coupon() -> cq.Workplane:
    result = None
    for center, (side_clear, rear_clear) in zip(LANE_CENTERS, CLEARANCE_PAIRS, strict=True):
        part = lane(center, side_clear, rear_clear)
        base = cq.Workplane("XY").box(WALL + REAR_PAD_INBOARD, LANE_LENGTH, BASE_THICKNESS,
                                       centered=(False, False, False)).translate(
                                           (center - side_clear - WALL, -LANE_LENGTH / 2,
                                            rear_clear - BACK - BASE_THICKNESS))
        result = part.union(base) if result is not None else part.union(base)

    bridge_z = min(rear - BACK - BASE_THICKNESS for _, rear in CLEARANCE_PAIRS)
    for left, right in zip(LANE_CENTERS, LANE_CENTERS[1:]):
        bridge = cq.Workplane("XY").box(right - left, BRIDGE_Y_WIDTH, BASE_THICKNESS,
                                         centered=(False, False, False)).translate(
                                             (left, -BRIDGE_Y_WIDTH / 2, bridge_z))
        result = result.union(bridge)

    if not result.val().isValid() or len(result.val().Solids()) != 1:
        raise RuntimeError("coupon must be one valid joined solid")
    return result


if __name__ == "__main__":
    coupon = make_coupon()
    out = OUT / "tpu_multilane_coupon.stl"
    cq.exporters.export(coupon, str(out), tolerance=0.025, angularTolerance=0.15)
    print(f"exported {out}")
