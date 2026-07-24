"""Support-free PETG hand tool for the Round 3 washer-filter fixture.

Native exported coordinates are the planned print orientation.  ``to_print`` rotates
the installed tool about X by +90 degrees, so the engagement pocket is open sideways
while printing rather than bridged from above.
"""
from pathlib import Path
import cadquery as cq

# ==== FIT-DRIVING PARAMETERS (mm; common brief / FDM sliding PETG fit) ====
CAP_DIAMETER = 63.0       # participant-visible fixture fact
BAR_LENGTH = 62.0         # participant-visible fixture fact, installed X axis
BAR_WIDTH = 11.7          # participant-visible fixture fact, installed Y axis
BAR_HEIGHT = 24.0         # participant-visible fixture fact, installed Z axis
CLEARANCE_SIDE = 0.35     # PETG sliding clearance, per side (fdm-design §4)
CLEARANCE_TOP = 0.50      # protects cap/bar from a hard ceiling contact
SLOT_LENGTH = BAR_LENGTH + 2 * CLEARANCE_SIDE
SLOT_WIDTH = BAR_WIDTH + 2 * CLEARANCE_SIDE
SLOT_DEPTH = BAR_HEIGHT + CLEARANCE_TOP

# ==== Ergonomic/structural parameters (mm) ====
HANDLE_LENGTH = 116.0
HANDLE_WIDTH = 55.0
HANDLE_HEIGHT = 46.0
EDGE_CHAMFER = 1.2
COUPON_WIDTH = 26.0
COUPON_HEIGHT = 29.0
OUT = Path(__file__).resolve().parent


def installed_body(handle_length=HANDLE_LENGTH, handle_width=HANDLE_WIDTH,
                   handle_height=HANDLE_HEIGHT):
    """Tool in installed coordinates: X=bar length, Y=bar width, Z=bar height.

    The long rounded paddle is comfortable in a hand.  The real engagement cavity
    is a bottom-open rectangular socket; its broad, smooth walls distribute torque
    over the whole cross-bar without teeth.
    """
    outer = (cq.Workplane("XY")
             .box(handle_length, handle_width, handle_height,
                  centered=(True, True, False))
             .edges("|Z").fillet(5.0)
             .edges("<Z").chamfer(EDGE_CHAMFER))
    # Pocket begins at the appliance side (Z=0), so the tool lowers over the bar.
    engagement = (cq.Workplane("XY")
                  .box(SLOT_LENGTH, SLOT_WIDTH, SLOT_DEPTH,
                       centered=(True, True, False)))
    result = outer.cut(engagement)
    if not result.val().isValid():
        raise RuntimeError("invalid tool solid after engagement cut")
    return result


def installed_coupon():
    """Physical PLA coupon using the exact same slot parameters as the final tool."""
    blank = (cq.Workplane("XY")
             .box(SLOT_LENGTH + 12.0, COUPON_WIDTH, COUPON_HEIGHT,
                  centered=(True, True, False))
             .edges("|Z").fillet(2.0)
             .edges("<Z").chamfer(0.8))
    engagement = (cq.Workplane("XY")
                  .box(SLOT_LENGTH, SLOT_WIDTH, SLOT_DEPTH,
                       centered=(True, True, False)))
    return blank.cut(engagement)


def to_print(shape):
    """Map installed coordinates to support-free planned print coordinates."""
    # The wide end face is on the bed.  The only downward pocket face is a
    # designed 24.5-mm bridge, within the 5–25-mm FDM bridge guidance.
    return shape.rotate((0, 0, 0), (0, 1, 0), 90).translate((0, 0, 58.0))


body_installed = installed_body()
coupon_installed = installed_coupon()
body = to_print(body_installed)
coupon = to_print(coupon_installed)

if __name__ == "__main__":
    cq.exporters.export(body, str(OUT / "filter_cap_tool.stl"),
                        tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(body, str(OUT / "filter_cap_tool.step"))
    cq.exporters.export(coupon, str(OUT / "bar_engagement_coupon.stl"),
                        tolerance=0.01, angularTolerance=0.1)
    print(f"tool volume={body.val().Volume():.2f} mm^3")
    print(f"slot LxWxD={SLOT_LENGTH:.2f} x {SLOT_WIDTH:.2f} x {SLOT_DEPTH:.2f} mm")
