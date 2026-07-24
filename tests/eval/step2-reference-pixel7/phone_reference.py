"""
phone_reference.py — Google Pixel 7 BLIND mating reference (step 2)

Built EXCLUSIVELY from tests/eval/step1-metrology-pixel7/dimensions.md
(contract_version 4, revision 1, status DRAFT). No source photos, no
pixel7_high_detail_reference_model.stl, no PixelCaseV4.3mf were read to
produce this file — per the reference-commission rule in
skills/3d-designer/SKILL.md ("reconstruct the mating object from
dimensions.md alone and do not inspect the source photos").

Every design-driving number below is either:
  (a) a datum value straight off the sheet (comment cites the M-/F-/D- id
      and confidence grade), or
  (b) an ASSUMPTION for a dimension the sheet deliberately left unbounded
      (no numeric value given at all) — flagged inline as ASSUMPTION and
      restated in reference_manifest.md. These never touch a fit-critical
      dimension; every fit-critical number (F-001 envelope, F-002 corner
      radius, F-003 camera-bar height/width/protrusion) comes straight off
      the sheet.

Coordinate system (per sheet's Frame table):
  X : D5_LEFT (-W/2, SIM-tray edge)  ->  D4_RIGHT (+W/2, button edge)
  Y : D3_BOT  (-L/2, USB-C edge)     ->  D2_TOP   (+L/2, earpiece/mic edge)
  Z : D0_BACK (0, flat back plane)   ->  D6_SCREEN (+T, front glass);
      the camera bump protrudes on the far side of the back plane, i.e.
      into -Z (it makes the device thicker there than the flat body T).
Right-handed, matches the sheet's stated Handedness row.
"""

import cadquery as cq

# ==== PARAMETERS (mm) — every value cites its sheet ID; ASSUMPTION = not in sheet ====

# --- F-001 body envelope (sheet: use SPEC nominal, corroborated by direct caliper) ---
L = 155.6   # M-001, D2_TOP<->D3_BOT, SPEC-01/02 grade B (caliper corroboration 155.0, IMG-07 grade A)
W = 73.2    # M-002, D4_RIGHT<->D5_LEFT, SPEC-01/02 grade B (caliper corroboration 71.9, IMG-08 grade A, OQ-06)
T = 8.7     # M-003, D0_BACK<->D6_SCREEN, SPEC-01/02 grade B — OQ-01 NOT silently resolved:
            # three independent caliper reads (IMG-09/10/12) cluster 9.5-9.8mm, ~0.8-1.1mm
            # above this nominal, all taken near a button/edge region. Sheet directs use of
            # 8.7 as provisional nominal pending a flat-region re-measurement. Recorded here,
            # NOT substituted, so the conflict stays visible (see reference_manifest.md).
THICKNESS_CALIPER_CLUSTER_MM = (9.5, 9.6, 9.8)  # IMG-09/10/12, OQ-01 — not used in geometry

# --- F-002 corner radius, all 4 vertical corners (M-004, grade B, bounded range) ---
R_CORNER = 9.5   # nominal of 9.5 +/- 1.5 mm (IMG-07 calibrated crop); range kept below for
R_CORNER_BAND = (8.0, 11.0)  # traceability per "model the nominal, keep ambiguity visible"

# --- F-003 camera bar / bump (mixed A/B/C, all case-relevant sub-values graded A/B) ---
CAM_BAR_HEIGHT = 20.4        # M-005, D2_TOP along -Y to flush transition, IMG-13 grade A
CAM_TRIM_SUBHEIGHT = 14.3    # M-006, D2_TOP along -Y to metal-trim/matte transition, IMG-17
                              # grade A; sheet: "cosmetic sub-detail only, not needed for case
                              # fit" -> modeled as a shallow witness groove only, no separate
                              # protrusion step (no measured step-height exists in the sheet).
CAM_BAR_WIDTH = W            # M-008, full device width edge-to-edge, grade C (IMG-04/16/17)
CAM_BUMP_PROTRUSION = 2.74   # M-007, arithmetic 11.44 (SPEC-01 hands-on) - 8.7, grade B (derived)

# --- F-004 lens-oval cutout (grade C size, grade A top-margin sub-measure) ---
LENS_OVAL_W = 33.0           # M-010, nominal of 30-36mm range, grade C
LENS_OVAL_H = 7.0            # M-010, nominal of 6-8mm range, grade C
LENS_OVAL_TOP_MARGIN = 6.2   # M-009, D2_TOP along -Y, IMG-14 grade A
LENS_OVAL_X = 0.0            # ASSUMPTION: no X-offset given in sheet; centered on camera bar
LENS_OVAL_RECESS_DEPTH = 1.0 # ASSUMPTION: no depth given; shallow cosmetic dish only
                              # (F-004 explicitly "non-fit-critical" per sheet)

# --- F-005 small hole beside lens oval: NOT MODELED ---
# Sheet gives no numeric size or position for F-005, only "cosmetic-only bounded envelope,
# inside F-003" with no digits. Fabricating a size would be an unlabeled magic number, so
# per "model at stated datum value or bounded envelope" this feature is intentionally
# omitted from geometry and left as a documented gap (see reference_manifest.md).

# --- F-006 volume rocker / F-007 power button (grade C position, D4_RIGHT edge) ---
VOL_BTN_CENTER_Y = L / 2 - 32.0   # M-011 nominal (range Y=+24..+40 from D2_TOP), IMG-02 grade C
VOL_BTN_LEN = 16.0                 # M-011
PWR_BTN_CENTER_Y = L / 2 - 50.0   # M-012 nominal (range Y=+44..+58 from D2_TOP), IMG-02 grade C
PWR_BTN_LEN = 10.0                 # M-012
BTN_PROTRUSION = 0.6   # ASSUMPTION: sheet gives Y-center/length only, no radial protrusion;
                        # typical phone side-button reveal, non-fit-critical (M-021 is LOOSE)
BTN_Z_SPAN = 4.0        # ASSUMPTION: no Z-height given; nominal band centered on mid-thickness

# --- F-008 SIM tray (grade C position, D5_LEFT edge) ---
SIM_TRAY_CENTER_Y = L / 2 - 35.0   # M-013 nominal (range Y=+25..+45 from D2_TOP), grade C
SIM_TRAY_LEN = 13.0                 # M-013
SIM_TRAY_DEPTH = 0.3    # ASSUMPTION: recess depth not given; shallow witness slot
SIM_TRAY_Z_SPAN = 2.0   # ASSUMPTION: not given; nominal band centered on mid-thickness

# --- F-009 top mic hole (grade C, D2_TOP edge, offset from D5_LEFT corner) ---
MIC_OFFSET_X = -W / 2 + 14.0   # M-014 nominal of 10-18mm range from D5_LEFT corner, grade C
MIC_HOLE_SIZE = 1.2      # ASSUMPTION: no diameter given; typical mic-hole size, cosmetic
MIC_HOLE_DEPTH = 1.0     # ASSUMPTION: shallow dimple only

# --- F-010 USB-C port (grade B center-X, grade C size, D3_BOT edge) ---
USBC_CENTER_X = 0.0     # M-015, +/-2mm, visually centered, grade B
USBC_WIDTH = 8.5         # M-016 nominal of 8-9mm range, grade C
USBC_HEIGHT = 3.0        # M-016, grade C
USBC_DEPTH = 4.0         # ASSUMPTION: port bore depth not given; nominal port-body depth
USBC_CENTER_Z = T / 2    # ASSUMPTION: no Z-position given; mid-thickness default

# --- F-011 / F-012 bottom speaker/mic grilles (grade C, D3_BOT edge) ---
GRILLE_L_CENTER_X = -W / 2 + 11.0   # M-017 nominal, "inset from D5_LEFT corner", grade C
GRILLE_L_WIDTH = 6.0                 # M-017
GRILLE_R_CENTER_X = W / 2 - 12.0    # M-018 nominal, "inset from D4_RIGHT corner", grade C
GRILLE_R_WIDTH = 6.0                 # M-018
GRILLE_Z_SPAN = 1.5     # ASSUMPTION: not given
GRILLE_DEPTH = 2.0       # ASSUMPTION: not given

# --- F-013 screen/front-glass plane (grade D, flush, no native lip) ---
# D6_SCREEN is simply the body's top face at Z=+T; sheet resolves no separate lip geometry
# (F-013 explicitly bounded conservatively as flush -- see OQ-08). No extra geometry needed.

# --- F-014 back-panel finish step, F-015 logo: cosmetic only, no case-fit effect ---
# Not modeled — sheet marks both "none required" for case fit and gives no numeric bounds.


# ==== MODEL ====

# F-001 + F-002: rounded-rect body prism, D0_BACK (Z=0) to D6_SCREEN (Z=+T)
body = (
    cq.Workplane("XY")
    .rect(W, L)
    .extrude(T)
)
body = body.edges("|Z").fillet(R_CORNER)
assert body.val().isValid(), "body fillet produced an invalid solid"

# F-003: camera bar / bump, full width, top-anchored at D2_TOP, protruding into -Z
cam_bar = (
    cq.Workplane("XY")
    .center(0, L / 2 - CAM_BAR_HEIGHT / 2)
    .rect(CAM_BAR_WIDTH, CAM_BAR_HEIGHT)
    .extrude(-CAM_BUMP_PROTRUSION)
)
body = body.union(cam_bar)
assert body.val().isValid(), "camera-bar union produced an invalid solid"
vol_after_bar = body.val().Volume()

# M-006 metal-trim/matte witness groove (cosmetic only, no separate protrusion — see note above)
groove_y = L / 2 - CAM_TRIM_SUBHEIGHT
groove_cut = (
    cq.Workplane("XY")
    .center(0, groove_y)
    .rect(CAM_BAR_WIDTH + 2, 0.5)
    .extrude(0.15)
    .translate((0, 0, -CAM_BUMP_PROTRUSION))
)
body = body.cut(groove_cut)

# F-004: lens-oval shallow recess within the camera bar (non-fit-critical, cosmetic dish)
lens_center_y = L / 2 - LENS_OVAL_TOP_MARGIN - LENS_OVAL_H / 2
lens_cut = (
    cq.Workplane("XY")
    .center(LENS_OVAL_X, lens_center_y)
    .ellipse(LENS_OVAL_W / 2, LENS_OVAL_H / 2)
    .extrude(LENS_OVAL_RECESS_DEPTH)
    .translate((0, 0, -CAM_BUMP_PROTRUSION))
)
body = body.cut(lens_cut)
assert body.val().isValid(), "camera-bar detail cuts produced an invalid solid"

# F-006 volume rocker, F-007 power button: raised pads on the D4_RIGHT edge
for center_y, length in ((VOL_BTN_CENTER_Y, VOL_BTN_LEN), (PWR_BTN_CENTER_Y, PWR_BTN_LEN)):
    btn = (
        cq.Workplane("XY")
        .box(BTN_PROTRUSION, length, BTN_Z_SPAN, centered=(True, True, True))
        .translate((W / 2 + BTN_PROTRUSION / 2, center_y, T / 2))
    )
    body = body.union(btn)
assert body.val().isValid(), "button union produced an invalid solid"

# F-008: SIM tray, shallow recess on the D5_LEFT edge
sim_cut = (
    cq.Workplane("XY")
    .box(SIM_TRAY_DEPTH, SIM_TRAY_LEN, SIM_TRAY_Z_SPAN, centered=(True, True, True))
    .translate((-W / 2 + SIM_TRAY_DEPTH / 2, SIM_TRAY_CENTER_Y, T / 2))
)
body = body.cut(sim_cut)

# F-009: top mic hole, shallow dimple on the D2_TOP edge
mic_cut = (
    cq.Workplane("XY")
    .box(MIC_HOLE_SIZE, MIC_HOLE_DEPTH, MIC_HOLE_SIZE, centered=(True, True, True))
    .translate((MIC_OFFSET_X, L / 2 - MIC_HOLE_DEPTH / 2, T / 2))
)
body = body.cut(mic_cut)

# F-010: USB-C port cutout on the D3_BOT edge
usbc_cut = (
    cq.Workplane("XY")
    .box(USBC_WIDTH, USBC_DEPTH, USBC_HEIGHT, centered=(True, True, True))
    .translate((USBC_CENTER_X, -L / 2 + USBC_DEPTH / 2, USBC_CENTER_Z))
)
body = body.cut(usbc_cut)

# F-011 / F-012: bottom-left / bottom-right speaker/mic grilles on the D3_BOT edge
for center_x, width in ((GRILLE_L_CENTER_X, GRILLE_L_WIDTH), (GRILLE_R_CENTER_X, GRILLE_R_WIDTH)):
    grille_cut = (
        cq.Workplane("XY")
        .box(width, GRILLE_DEPTH, GRILLE_Z_SPAN, centered=(True, True, True))
        .translate((center_x, -L / 2 + GRILLE_DEPTH / 2, T / 2))
    )
    body = body.cut(grille_cut)

assert body.val().isValid(), "final solid is invalid after all cuts"

# ==== SANITY PRINT (in-memory CadQuery solid; the manifest re-measures the EXPORTED STL) ====
bb = body.val().BoundingBox()
print("in-memory volume mm3:", body.val().Volume())
print("in-memory bbox: x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" %
      (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
print("camera-bar union volume mm3:", vol_after_bar)

# ==== EXPORT ====
cq.exporters.export(body, "phone_reference.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "phone_reference.step")
print("exported phone_reference.stl and phone_reference.step")
