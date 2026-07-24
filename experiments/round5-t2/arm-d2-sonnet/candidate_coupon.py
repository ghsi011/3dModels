"""Round-5 D2 functional engagement coupon (Arm S / Sonnet 5) -- build123d source.

Per print_plan.md "Coupon": one support-free, one-piece engagement coupon generated
from the SAME named production bar-cavity, mouth lead-in, bearing-radius, wall, and
clearance parameters as candidate_model.py. Retains the complete 62.00mm F02 X span,
the exact production Y width/clearance, and >=20.00mm of production Z engagement
depth, with a rigid hand tab (not a peg/hole surrogate). Reuses candidate_model.py's
CONST cavity + mouth-rim-fillet construction verbatim (same parameters), trimmed to
a short, rigid coupon body instead of the full tapered/gripped tool.
"""
from pathlib import Path

from build123d import Align, Axis, Box, Pos, fillet, chamfer
from build123d import export_stl, export_step

import candidate_model as M

OUT = Path(__file__).parent

# ---- coupon-specific dims (reuse candidate_model's named parameters verbatim) ----
COUPON_Z_ENGAGE = M.Z_CEIL - M.Z_FLOOR          # 24.60 mm >= 20.00 required (full production depth)
COUPON_TAB_Y = 20.0                              # rigid hand tab beyond the cavity, Y direction
COUPON_Y_LO = M.Y_ROOT - COUPON_TAB_Y            # extra Y for a solid grip tab
COUPON_Y_HI = M.Y_TAPER_START + 3.0              # short rigid cap past the mouth (no taper needed;
                                                  # coupon is not print-orientation constrained the
                                                  # same way -- it reuses the SAME cavity parameters
                                                  # to test fit, per the plan's "same production
                                                  # bar-cavity ... parameters" requirement)


def build() -> "Part":
    outer = Box(
        2 * M.BODY_X_HALF, COUPON_Y_HI - COUPON_Y_LO, M.Z_TOP - M.Z_FLOOR,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    outer = Pos(0, COUPON_Y_LO, M.Z_FLOOR) * outer
    outer = fillet(outer.edges().filter_by(Axis.Y), radius=M.OUTER_FILLET)

    cav_const = Box(
        2 * M.CAV_X_HALF, M.Y_TAPER_START - M.Y_ROOT, M.Z_CEIL - M.Z_FLOOR,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    cav_const = Pos(0, M.Y_ROOT, M.Z_FLOOR) * cav_const
    part = outer - cav_const
    assert part.is_valid, "coupon boolean invalid after cavity cut"

    mouth_edges = M._select_mouth_rim_edges(part)
    if mouth_edges:
        part = fillet(mouth_edges, radius=M.MOUTH_R)

    pbed_edges = [e for e in part.edges() if abs(e.center().Y - COUPON_Y_LO) < 1e-3]
    if pbed_edges:
        part = chamfer(pbed_edges, length=M.PBED_CH1, length2=M.PBED_CH2)

    return part


if __name__ == "__main__":
    part = build()
    print("is_valid", part.is_valid)
    print("volume_mm3", part.volume)
    bb = part.bounding_box()
    print("bbox_min", bb.min, "bbox_max", bb.max)
    print("coupon Z engagement depth (Z_CEIL-Z_FLOOR):", COUPON_Z_ENGAGE, ">=20.00 required")
    print("coupon full F02 X span (2*CAV_X_HALF):", 2 * M.CAV_X_HALF, "== 62.00+2*CL_END required")

    export_stl(part, str(OUT / "candidate_coupon.stl"), tolerance=0.01, angular_tolerance=0.1)
    print("exported candidate_coupon.stl")
