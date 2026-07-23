"""
J Class yacht base — translucent text sample coupon (SMALL, <1 h print).

Purpose: settle every open question about putting mirrored text under the
translucent base BEFORE committing to the 150 mm+ yacht print.

What it tests, in one ~25 min print:
  1. How much translucent PETG you can still read through. The plate steps
     through four cover thicknesses over the text: 1.0 / 1.5 / 2.1 / 3.0 mm.
     2.1 mm is the real base's thinnest point (measured), so the ladder
     brackets reality on both sides.
  2. PETG-CF inlay vs. bare air-gap recess, side by side at every thickness:
     the LEFT column of each zone gets a matching PETG-CF body, the RIGHT
     column is left as an open recess (single-material engraving).
  3. Real font size. "Abba" is set at the same size the final base will use,
     so the stem widths and counters are representative of the CF fuzz risk.

Orientation / mirroring:
  Text is recessed into the BOTTOM face (z = 0..TEXT_DEPTH) and drawn normally
  in the top-down (+Z) view. So read from ABOVE, through the material, it is
  correct; looked at directly from below it is mirrored. That is exactly the
  "mirrored text underneath" the brief asks for. verify.py renders both views.

Print it text-face down on the plate.
  Base = translucent PETG  -> MAIN nozzle (direct drive, best finish, 98% of volume)
  Text = indigo PETG-CF    -> AUX nozzle  (Bambu rates CF "print with caution" on
                              the aux; both extruders are hardened steel, and this
                              is ~0.5 g in the bottom 3 layers, so exposure is tiny)
"""

import cadquery as cq
from cadquery import exporters
import os

# ============================== PARAMETERS ==================================

# --- Real base, MEASURED from 'jclass wcrew big.stl' (for reference/scaling) --
# Flat rectangular underside, 100% solid at z=0.5/1.0/1.5 (trimesh sections).
BASE_X = 63.67          # mm, measured: X 86.88 .. 150.55
BASE_Y = 137.50         # mm, measured: Y 40.67 .. 178.17
BASE_MIN_THK = 2.1      # mm, measured: lowest up-facing sea flats sit at z~2.1
                        #     -> the real base is ~2.1 mm at its thinnest point.

SCALE = 1.0             # Match whatever scale you print the yacht at. Model is
                        # 149.55 mm tall and the designer wants >=150 mm, so 1.00
                        # is borderline and 1.05 (-> 157 mm) is the safe pick.
                        # Scaling the yacht scales the base thickness too, which
                        # is why the ladder below goes past 2.1 mm.

# --- Coupon size: kept small deliberately, target < 1 h ----------------------
COUPON_X = 68.0         # mm. Near the real base width (63.67) so the text reads
                        #     at true scale, plus a strip for the zone labels.
ZONE_Y = 15.0           # mm per thickness zone
EDGE_Y = 1.0            # mm margin at each end of the ladder

# --- Text recess ------------------------------------------------------------
TEXT_DEPTH = 0.6        # mm, 3 layers @ 0.2 -- enough for the CF to read fully
                        #     opaque, shallow enough to leave material above.

# --- Thickness ladder: translucent material ABOVE the text ------------------
ZONE_COVER = [1.0, 1.6, 2.2, 3.0]   # mm; 2.2 straddles the real base minimum (2.1)
# Chosen so that cover + TEXT_DEPTH is a whole number of 0.2 mm layers in EVERY
# zone: 1.6 / 2.2 / 2.8 / 3.6 = 8 / 11 / 14 / 18 layers. The obvious ladder
# (1.0/1.5/2.1/3.0) puts zones 2 and 3 on half-layers, so the slicer rounds them
# by up to 0.1 mm -- and those are the two zones closest to the real base, i.e.
# exactly the measurements you least want fudged. 2.2 vs the measured 2.1 is a
# 0.1 mm difference that no legibility test can resolve.

# --- Typography -------------------------------------------------------------
# Bold only: PETG-CF fuzzes fine detail, so stems must stay >= ~1.2 mm
# (3 x 0.4 nozzle). Arial Bold stem ~= 0.14 * fontsize -> 10 mm size ~ 1.4 mm.
FONT = "Arial"
FONT_KIND = "bold"
WORD = "Abba"           # has caps, lowercase, and counters -- representative
WORD_SIZE = 10.0        # mm, the size line 1 of the real base will use
COL_OFFSET = 14.5       # mm, column centres at -/+ this in X
LABEL_SIZE = 6.0        # mm, zone labels. Left as bare recesses, never CF: at this
                        #     size the stems are ~0.85 mm, under the CF minimum, but
                        #     an open recess that narrow prints fine.
LABEL_X = -30.0         # mm, in the strip left free outside the columns. Leaves
                        #     ~1.9 mm of wall to the edge and ~1.0 mm to the word.

# --- The real base text, kept here for the final print (not on this coupon) --
FINAL_LINES = [
    ("Oh the places you'll go!", 10.0),
    ("Happy birthday Abba!",     11.0),
    ("24.07.2026",               12.0),
]

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================== DERIVED =====================================
cx = COUPON_X * SCALE
zone_len = ZONE_Y * SCALE
cy = zone_len * len(ZONE_COVER) + 2 * EDGE_Y * SCALE
zone_cover = [c * SCALE for c in ZONE_COVER]
tdepth = TEXT_DEPTH * SCALE
n_zones = len(zone_cover)


def text_solid(txt, size, rot=0):
    """Text solid at z = 0..tdepth, drawn to read correctly looking down from +Z."""
    s = cq.Workplane("XY").text(
        txt, size, tdepth, font=FONT, kind=FONT_KIND,
        halign="center", valign="center",
    )
    return s.rotate((0, 0, 0), (0, 0, 1), rot) if rot else s


# ---------------------------------------------------------------------------
# Stepped plate: flat bottom at z=0, top steps up zone by zone along +Y.
# ---------------------------------------------------------------------------
plate = None
for i, cover in enumerate(zone_cover):
    y0 = -cy / 2 + EDGE_Y * SCALE + i * zone_len
    ylen = zone_len + (EDGE_Y * SCALE if i in (0, n_zones - 1) else 0)
    if i == 0:
        y0 -= EDGE_Y * SCALE
    zone = (
        cq.Workplane("XY")
        .box(cx, ylen, tdepth + cover, centered=(True, False, False))
        .translate((0, y0, 0))
    )
    plate = zone if plate is None else plate.union(zone)

# ---------------------------------------------------------------------------
# Text: per zone, LEFT column = CF inlay, RIGHT column = bare recess.
# ---------------------------------------------------------------------------
text_all = None     # everything -> cut from the plate to form the recesses
text_cf = None      # left column only -> printed in PETG-CF on the aux nozzle
report = []


def add(acc, s):
    return s if acc is None else acc.union(s)


for i, cover in enumerate(zone_cover):
    yc = -cy / 2 + EDGE_Y * SCALE + (i + 0.5) * zone_len

    left = text_solid(WORD, WORD_SIZE * SCALE).translate((-COL_OFFSET * SCALE, yc, 0))
    right = text_solid(WORD, WORD_SIZE * SCALE).translate((COL_OFFSET * SCALE, yc, 0))
    # Zone label, rotated so it runs along Y in the narrow free strip.
    label = text_solid(f"{ZONE_COVER[i]:.1f}", LABEL_SIZE * SCALE, rot=90) \
        .translate((LABEL_X * SCALE, yc, 0))

    text_all = add(add(add(text_all, left), right), label)
    text_cf = add(text_cf, left)          # labels stay bare so thin stems are fine

    bb = left.val().BoundingBox()
    report.append((ZONE_COVER[i], cover, bb.xlen, bb.ylen))

base_body = plate.cut(text_all)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    exporters.export(base_body, os.path.join(OUT_DIR, "sample_base.stl"),
                     tolerance=0.01, angularTolerance=0.1)
    exporters.export(text_cf, os.path.join(OUT_DIR, "sample_text_cf.stl"),
                     tolerance=0.01, angularTolerance=0.1)
    exporters.export(text_all, os.path.join(OUT_DIR, "sample_text_all.stl"),
                     tolerance=0.01, angularTolerance=0.1)
    exporters.export(base_body.union(text_all),
                     os.path.join(OUT_DIR, "sample_coupon.step"))

    vb = base_body.val().Volume() / 1000
    vt = text_cf.val().Volume() / 1000
    print(f"coupon footprint : {cx:.2f} x {cy:.2f} mm")
    print(f"zone cover (mm)  : {[round(c,2) for c in zone_cover]}")
    print(f"plate thickness  : {[round(tdepth+c,2) for c in zone_cover]} mm")
    print(f"text recess      : {tdepth:.2f} mm")
    print(f"translucent PETG : {vb:.2f} cm3  (~{vb*1.27:.1f} g)   MAIN nozzle")
    print(f"PETG-CF text     : {vt:.3f} cm3  (~{vt*1.27:.2f} g)   AUX nozzle")
    print(f"total            : {vb+vt:.2f} cm3  (~{(vb+vt)*1.27:.1f} g)")
    print(f"word '{WORD}' @ {WORD_SIZE} mm: {report[0][2]:.1f} x {report[0][3]:.1f} mm")
