"""Functional engagement coupon (build123d) — same named production parameters as
candidate_model.py: full 62 mm F02 X span, production Y width/clearance, >=20 mm Z
engagement, rigid hand tab, support-free (gable roof + 48 deg P_BED bevel).
It is the real capture channel (not a peg/hole surrogate); comfort fillets are
omitted so it reads as a fit-test coupon. Prints on P_BED (installed Y=-16)."""
from pathlib import Path
from build123d import *
import candidate_model as cm   # reuses identical named parameters

OUT = Path(__file__).parent

# production capture channel (identical cavity / gable / walls / clearances)
body = cm.box_bounds(-cm.X_OUT, cm.X_OUT, cm.PBED_Y, cm.Y_TOP, cm.Z_MOUTH, cm.Z1)
slot = cm.box_bounds(-cm.CX, cm.CX, -cm.CY, cm.CY, cm.Z_MOUTH - 5.0, cm.CZ_TOP)
tri = Plane.YZ * Polygon((cm.CY, cm.Z_MOUTH), (cm.CY, cm.CZ_TOP), (cm.Y_RIDGE, cm.Z_MID))
attic = extrude(tri, amount=cm.CX, both=True)
coupon = body - (slot + attic)

# rigid hand tab = the solid +Y block above the channel (already present); add a
# shallow finger relief slot on the +Y show face is intentionally omitted to keep
# the coupon fully support-free and rigid for the insert/rotate fit test.

# P_BED elephant-foot bevel (same 48 deg self-supporting relief)
bf = coupon.faces().filter_by(Axis.Y).group_by(Axis.Y)[0][0]
coupon = chamfer(bf.edges(), length=cm.PBED_CH, angle=cm.PBED_CH_DEG, reference=bf)

if __name__ == "__main__":
    export_stl(coupon, str(OUT / "candidate_coupon.stl"), tolerance=0.01, angular_tolerance=0.05)
    bb = coupon.bounding_box()
    eng = cm.BAR_H - cm.Z_MOUTH
    print("COUPON bbox", bb.min, bb.max, "engagement_mm", round(eng, 2),
          "Xspan", round(2 * cm.CX, 2))
