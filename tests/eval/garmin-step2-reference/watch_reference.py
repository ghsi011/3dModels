"""
watch_reference.py -- Garmin Fenix 7X BLIND mating reference (step 2)

Built EXCLUSIVELY from tests/eval/garmin-step1-metrology/dimensions.md
(contract_version 4, revision 1, status DRAFT). No source photos
(tests/garmin 7x stand/*.jpg), no Fenix+7x+charging+dock.3mf, no other
tests/ or experiments/ content were read to produce this file -- per the
reference-commission rule in skills/3d-designer/SKILL.md ("reconstruct the
mating object from dimensions.md alone and do not inspect the source
photos").

Every design-driving number below is either:
  (a) a datum value straight off the sheet (comment cites the M-/F-/D- id
      and confidence grade), or
  (b) an ASSUMPTION for a dimension the sheet deliberately left unbounded
      (no numeric value at all) -- flagged inline and restated in
      reference_manifest.md. ASSUMPTIONs never touch a fit-critical
      dimension: the only fit-critical feature per the sheet's own "Fit
      specification" section is F-001 (case body envelope), and every
      number driving it is a direct sheet citation.

THE CASEBACK CHARGE-CONTACT PAD (F-003 / M-009) IS DELIBERATELY NOT
MODELED. The sheet marks it "NOT READY -- blocking" (OQ-01): no photo of
the caseback exists in the supplied evidence set, so its location, pin
pattern, spacing, and offset from the case center are all UNKNOWN. This
build produces a plain flat caseback at Z=0 with no invented contact
geometry -- fabricating pin positions here would silently manufacture
"evidence" the metrology sheet explicitly says does not exist.

Coordinate system (per sheet's Frame table):
  Origin : case center at the caseback plane (D0_CASEBACK n D1_AXIS)
  +Z     : D1_AXIS, caseback (Z=0) -> crystal apex (Z=CASE_THICKNESS)
  +X     : D2_BUTTON_AXIS, toward the side-button/pusher-populated side
  +Y     : D3_BAND_AXIS, toward the open/perforated strap-tip end of the
           band, away from the buckle
Right-handed, matches the sheet's stated Frame table.
"""

import cadquery as cq

# ==== PARAMETERS (mm) -- every value cites its sheet ID; ASSUMPTION = not in sheet ====

# --- F-001 case body / bezel envelope (fit-critical; the ONLY fit-critical feature) ---
CASE_DIA_BUTTON_AXIS = 51.75   # M-001, mean of 51.7/51.8 direct caliper reads, grade A
CASE_DIA_BAND_AXIS = 51.75     # M-003, ASSUMED = M-001 by visible round-case symmetry,
                                 # grade C, OQ-04 (never independently calipered)
CASE_DIA = CASE_DIA_BUTTON_AXIS  # sheet: round case, both axes read/assumed equal ->
                                 # modeled as a true circle (radius reused for both axes)
CASE_THICKNESS = 14.9          # M-004, D0_CASEBACK -> crystal apex along D1_AXIS,
                                 # official spec S-12 only, grade B, OQ-02 (no side-profile
                                 # photo/caliper exists to corroborate)

# --- F-002 button/pusher protrusion envelope, D2_BUTTON_AXIS (bounded, grade A envelope) ---
BUTTON_ENVELOPE_DIA = 56.8     # M-002, direct caliper, tip-to-tip across D2_BUTTON_AXIS,
                                 # grade A AS AN ENVELOPE READING (explicitly not the
                                 # case-body diameter -- skill rule (b) near-feature read)
BUTTON_PROTRUSION = (BUTTON_ENVELOPE_DIA - CASE_DIA_BUTTON_AXIS) / 2   # D-001 = 2.53mm,
                                 # derived, radial protrusion beyond the flat bezel per side
# Sheet gives count (5, grade C, "known Fenix 7X layout") and the envelope diameter (grade A)
# but NO individual button positions, shapes, or angular spacing at all -- modeling 5 discrete
# button shapes would fabricate geometry the sheet does not contain. Instead this build
# reconstructs the ENVELOPE ONLY: a single symmetric keep-out boss on the D2_BUTTON_AXIS line
# (both +X and -X, since M-002 is itself a diametral/across reading), sized so the exported
# solid's own bounding box reproduces the 56.8mm envelope for a round-trip cross-check.
BUTTON_PAD_HALF_WIDTH_Y = 9.0   # ASSUMPTION: angular extent of the keep-out pad along Y;
                                 # not a real button footprint, just how far the envelope
                                 # circle's bulge is carried before blending back to the case
BUTTON_PAD_Z_LO_FRAC = 0.15     # ASSUMPTION: no button Z-band given; nominal band clear of
BUTTON_PAD_Z_HI_FRAC = 0.85     # both the caseback and crystal-apex edges

# --- F-004 band strap width at the two D3_BAND_AXIS lugs (bounded envelope, non-fit-critical) ---
BAND_WIDTH = 26.0              # M-005, direct caliper at strap body, grade A, corroborated
                                 # by official QuickFit-26 spec S-13
BAND_STUB_LENGTH = 15.0        # ASSUMPTION: sheet's own band-length reads (M-007, 111-115mm)
                                 # are explicitly low-confidence/ambiguous (OQ-03) and marked
                                 # "excluded from the cradle envelope, NOT fit-critical" -- this
                                 # build therefore models only a short representative stub at
                                 # each lug (enough to show the band-exit width/position for the
                                 # round trip), not a full-length band
BAND_THICKNESS = 3.0           # ASSUMPTION: band cross-section thickness not given anywhere
                                 # in the sheet; nominal QuickFit-silicone-band figure
# F-005 (buckle, M-006=31.4mm) and F-006 (QuickFit lug collar, bounded/low-confidence) are
# intentionally NOT modeled as separate geometry -- see reference_manifest.md. The sheet marks
# both non-blocking/cosmetic-adjacent and F-006's own bounded assumption is that its footprint
# "stays within the 26mm band-width envelope" (i.e. adds no information beyond BAND_WIDTH above).

# --- F-003 caseback charge-contact pad: NOT MODELED -- see module docstring and OQ-01 ---
# Sheet: "Do not assign a numeric offset/pattern to CAD without new evidence or explicit user
# approval of a bounded placeholder." No such evidence or approval exists at this step, so the
# caseback (Z=0 face) is left perfectly flat.

# --- F-007 display crystal, F-008 logo/markings: cosmetic only, no numeric bound in sheet ---
# Represented implicitly by the body's own top face (Z=CASE_THICKNESS); no separate bezel/lens
# step geometry is added (mirrors the "flush, no native lip" treatment used for a screen plane
# absent any measured step -- same reasoning as OQ-05: no side-profile evidence exists at all
# for any stepped/tapered case silhouette, so the case is modeled as a plain right cylinder for
# its full thickness, not tapered or radiused at the bezel/crystal transition).


# ==== MODEL ====

# F-001: case body / bezel -- plain right cylinder, D0_CASEBACK (Z=0) to crystal apex (Z=CASE_THICKNESS)
body = (
    cq.Workplane("XY")
    .circle(CASE_DIA / 2)
    .extrude(CASE_THICKNESS)
)
assert body.val().isValid(), "case cylinder is invalid"

# F-002: button/pusher keep-out envelope -- symmetric boss on D2_BUTTON_AXIS (+X and -X),
# built as (large envelope-diameter cylinder) INTERSECT (Y-limited, Z-limited slab), which
# yields the envelope circle's own curvature at the case surface without asserting any
# individual button shape or position.
env_r = BUTTON_ENVELOPE_DIA / 2
button_pad_h = CASE_THICKNESS * (BUTTON_PAD_Z_HI_FRAC - BUTTON_PAD_Z_LO_FRAC)
button_pad_z0 = CASE_THICKNESS * BUTTON_PAD_Z_LO_FRAC

env_cyl = cq.Workplane("XY").circle(env_r).extrude(CASE_THICKNESS)
button_slab = (
    cq.Workplane("XY")
    .box(2 * env_r + 10, 2 * BUTTON_PAD_HALF_WIDTH_Y, button_pad_h, centered=(True, True, False))
    .translate((0, 0, button_pad_z0))
)
button_boss = env_cyl.intersect(button_slab)
body = body.union(button_boss)
assert body.val().isValid(), "button-envelope union produced an invalid solid"
vol_after_buttons = body.val().Volume()

# F-004: band strap width at the two D3_BAND_AXIS lugs -- short representative stubs, half
# embedded in the case body (robust union, no coincident-face sliver) and half protruding.
case_r = CASE_DIA / 2
band_z0 = CASE_THICKNESS / 2 - BAND_THICKNESS / 2   # ASSUMPTION: centered on case height,
                                                       # no lug Z-position given in sheet

band_plus_y = (   # +Y: open/perforated strap-tip end (D3_BAND_AXIS)
    cq.Workplane("XY")
    .center(0, case_r)
    .rect(BAND_WIDTH, BAND_STUB_LENGTH)
    .extrude(BAND_THICKNESS)
    .translate((0, 0, band_z0))
)
band_minus_y = (   # -Y: buckle end (D3_BAND_AXIS)
    cq.Workplane("XY")
    .center(0, -case_r)
    .rect(BAND_WIDTH, BAND_STUB_LENGTH)
    .extrude(BAND_THICKNESS)
    .translate((0, 0, band_z0))
)
body = body.union(band_plus_y).union(band_minus_y)
assert body.val().isValid(), "band-stub union produced an invalid solid"

# Caseback (Z=0 face) stays exactly as extruded above -- flat, no cuts, no contact geometry.
# This is a deliberate omission, not an oversight: see F-003 note above and OQ-01.

# ==== SANITY PRINT (in-memory CadQuery solid; the manifest re-measures the EXPORTED STL) ====
bb = body.val().BoundingBox()
print("in-memory volume mm3:", body.val().Volume())
print("in-memory bbox: x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" %
      (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
print("volume after button-envelope union mm3:", vol_after_buttons)

# ==== EXPORT ====
cq.exporters.export(body, "watch_reference.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "watch_reference.step")
print("exported watch_reference.stl and watch_reference.step")
