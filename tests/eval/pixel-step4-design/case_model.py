"""
case_model.py - Google Pixel 7 protective TPU case, CANDIDATE commission (step 4)

Inputs read (per skills/3d-designer/SKILL.md candidate rule):
  tests/eval/step1-metrology-pixel7/dimensions.md        (rev 1, accepted)
  tests/eval/step2-reference-pixel7/phone_reference.stl   (mating object, blind reference)
  tests/eval/step2-reference-pixel7/reference_manifest.md
  tests/eval/step3-plan-pixel7/print_plan.md              (rev 1, ACCEPTED)
  tests/eval/step3-plan-pixel7/print_plan_checks.json
  skills/3d-modeling/references/{cadquery-patterns.md, fdm-design.md, team-contracts-v4.md}

Never read: the held-out oracle STL/3MF, photos, other tests/ or experiments/ material.

Coordinate frame: IDENTICAL to phone_reference.py / dimensions.md Frame table (native
design frame, NOT the printer frame). The print_plan's "180 deg about +X" transform is
applied only for orientation-specific renders/audits, matching how print_plan_checks.json
support_rules each carry their own model_to_printer_matrix for the auditor to apply -
the exported case.stl itself stays in this native frame so it composes directly with
phone_reference.stl for interference/clearance verification.
  X : D5_LEFT (-W/2, SIM-tray edge)  ->  D4_RIGHT (+W/2, button edge)
  Y : D3_BOT  (-L/2, USB-C edge)     ->  D2_TOP   (+L/2, earpiece/mic edge)
  Z : D0_BACK (0, flat back plane)   ->  D6_SCREEN (+T, front glass); camera bump
      protrudes into -Z beyond the flat back.
"""

import cadquery as cq

# ============================================================================
# PARAMETERS (mm) - phone geometry carried from the ACCEPTED reference/sheet
# ============================================================================

# --- F-001 body envelope, re-confirmed against the re-imported phone_reference.stl ---
L = 155.6       # M-001, phone_reference.stl Y extent (bounds Y [-77.8, 77.8])
W = 73.2        # M-002, phone_reference.stl straight-wall X width (bounds X [-36.6, 36.6]
                #  before the +0.6 button-pad protrusion baked into the reference mesh)
T = 8.7         # M-003, phone_reference.stl flat-body Z max (D0_BACK=0 to D6_SCREEN=T)
R_CORNER = 9.5  # M-004, phone_reference.stl re-measured corner radius (exact match)

# --- F-003 camera bar / bump, re-confirmed against phone_reference.stl ---
CAM_BAR_WIDTH = W          # M-008, full device width edge-to-edge
CAM_BAR_HEIGHT = 20.4       # M-005, D2_TOP along -Y to flush transition
CAM_BUMP_PROTRUSION = 2.74  # M-007, phone_reference.stl min(Z) = -2.74

# --- F-006 / F-007 buttons, D4_RIGHT edge (position C-grade, full stated RANGE per M-021) ---
# dimensions.md M-021 rationale text gives the sheet's own approved single-window bound:
# "one elongated relief spanning the full plausible zone (~= Y +22...+60mm on D4_RIGHT)"
# offset-from-D2_TOP convention -> actual Y = L/2 - offset:
BTN_WINDOW_Y_MIN = L / 2 - 60.0   # = 17.8  (covers PWR_BTN range +44..+58 incl. length/2)
BTN_WINDOW_Y_MAX = L / 2 - 22.0   # = 55.8  (covers VOL_BTN range +24..+40 incl. length/2)

# --- F-010 USB-C port, D3_BOT edge ---
USBC_CENTER_X = 0.0     # M-015, +/-2mm, visually centered
USBC_WIDTH = 8.5          # M-016 nominal of 8-9mm range
USBC_HEIGHT = 3.0         # M-016
USBC_CENTER_Z = T / 2     # matches phone_reference.py USBC_CENTER_Z assumption

# --- F-011 / F-012 bottom grilles, D3_BOT edge ---
GRILLE_L_CENTER_X = -W / 2 + 11.0   # M-017, inset from D5_LEFT corner
GRILLE_L_WIDTH = 6.0                  # M-017
GRILLE_R_CENTER_X = W / 2 - 12.0    # M-018, inset from D4_RIGHT corner
GRILLE_R_WIDTH = 6.0                  # M-018

# --- F-009 top mic hole, D2_TOP edge ---
MIC_OFFSET_X = -W / 2 + 14.0   # M-014 nominal of 10-18mm range from D5_LEFT corner

# ============================================================================
# PARAMETERS (mm) - case design decisions, driven by print_plan.md (ACCEPTED, rev 1)
# ============================================================================

# G-01 / M-019: body-envelope side-wall clearance, snug-sliding band 0.10-0.30 mm/side,
# NEVER a floor (over-clearance fails like interference). Chosen at the band midpoint for
# symmetric margin against measurement/print variance in either direction.
FIT_SNUG = 0.20  # mm/side

# G-03 / M-004: cavity corner radius must be >= 9.5mm (never undersized), <= 11.0mm relief.
CAVITY_R = R_CORNER + FIT_SNUG  # 9.70mm -> inside the E-01 band [9.5, 11.0]

# G-05: structural wall floor - nominal 1.6mm (4x0.4mm line width), 1.2mm absolute floor,
# 0.8mm hard floor never violated. All structural walls below use the 1.6mm nominal.
WALL_SIDE = 1.6   # mm, perimeter side wall (X/Y wrap around the phone body)
WALL_BACK = 1.6   # mm, general back-plate wall (flat body region)
WALL_BOSS = 1.6   # mm, camera-boss floor wall (protects the relief pocket)

# Exterior corner treatment: SHARP (no fillet), a deliberate simplification. A CASE_R
# matching the cavity (11.3mm) was tried first and empirically undercut the camera-pocket
# wall to ~0.04mm at the back corners (wall-thickness ray-cast audit) - the loose camera
# pocket reaches to within 1.4mm of the exterior boundary in X, and any exterior fillet
# above ~0.32mm there erodes below the 1.2mm absolute wall floor at that exact diagonal.
# Not gated by any plan rule (only the CAVITY radius, G-03/E-01, is contractual); see
# print_notes.md "Exterior corner treatment" for the honest limit and revision path.
CASE_R = CAVITY_R + WALL_SIDE  # 11.30mm, retained as a parameter for reference only

# G-06 / M-020: camera-bar relief, loose band 0.30-0.50 mm/side, band midpoint chosen.
# The camera bar's +Y edge is flush with the phone's own top edge (D2_TOP); the pocket
# gets the full loose band on all 4 sides, including +Y, which pushes the relief slightly
# past the general cavity's snug-band top boundary (L/2 + FIT_SNUG = 78.0) into open,
# already-past-the-phone-edge space - harmless there, and it also avoids a coincident-face
# boolean sliver against phone_reference.stl at the exact Y=L/2 tangency line.
CAM_CLR = 0.40  # mm/side
CAM_WINDOW_W = CAM_BAR_WIDTH + 2 * CAM_CLR       # 74.00mm
CAM_WINDOW_H = CAM_BAR_HEIGHT + 2 * CAM_CLR       # 21.20mm
CAM_WINDOW_Y_MAX = L / 2 + CAM_CLR                # 78.20mm
# No corner fillet on the pocket: phone_reference.py's cam_bar is a plain rect with SHARP
# corners (never filleted in the reference). A rounded pocket corner would arc inside the
# phone's sharp square corner whenever the fillet radius exceeds CAM_CLR, undercutting the
# clearance exactly there (caught empirically: 2.0mm fillet produced 0.25mm3 interference
# at both far corners of the bar). A plain rectangle keeps the uniform 0.40mm/side offset
# all the way into the corners.

CAM_POCKET_FLOOR_Z = -(CAM_BUMP_PROTRUSION + CAM_CLR)   # -3.14mm, clears the bump by 0.40
Z_BOSS_BOTTOM = CAM_POCKET_FLOOR_Z - WALL_BOSS            # -4.74mm, boss exterior (lowest pt)
BOSS_Y_MIN = (CAM_WINDOW_Y_MAX - CAM_WINDOW_H) - 1.5       # 55.50mm, boss step margin

# G-08 / M-021: button window bridge span. The sheet's single elongated window
# (BTN_WINDOW_Y_MIN..MAX = 38.0mm) exceeds the 25mm self-supporting "fine" bridge limit
# (fdm-design.md sec1), so G-08 requires either an internal self-supporting rib splitting
# it into <=25mm segments, or SUPPORT_ALLOWED (S-03) on the excess. This design chooses the
# rib: it needs no support material inside a hard-to-reach window cavity, and print_plan
# print_plan_checks.json's S-03 rule carries no numeric max_out_of_limit_area_mm2 (null) -
# team_preflight.py's support-audit cannot evaluate a null cap (see candidate_readiness.md),
# so avoiding S-03 activation is also the only path to a clean automated gate.
BTN_RIB_WIDTH = 1.8  # mm, Y-direction width of the splitting rib
BTN_RIB_CENTER_Y = (BTN_WINDOW_Y_MIN + BTN_WINDOW_Y_MAX) / 2  # 36.8mm
BTN_WINDOW_Z_MIN = 1.5
BTN_WINDOW_Z_MAX = 7.5

# Loose port/grille windows (M-022), each kept individually well under the 25mm bridge
# threshold per G-09 -> SELF_SUPPORT_REQUIRED trivially satisfied, S-02 governs.
PORT_CLR = 0.40  # mm/side, band midpoint of 0.30-0.50
USBC_WINDOW_WIDTH = USBC_WIDTH + 2 * PORT_CLR     # 9.30mm
USBC_WINDOW_HEIGHT = USBC_HEIGHT + 2 * PORT_CLR    # 3.80mm
GRILLE_WINDOW_WIDTH = GRILLE_L_WIDTH + 2 * PORT_CLR  # 6.80mm (same for both grilles)
BOTTOM_WINDOW_Z_MIN = USBC_CENTER_Z - USBC_WINDOW_HEIGHT / 2 - 0.6  # small extra margin
BOTTOM_WINDOW_Z_MAX = USBC_CENTER_Z + USBC_WINDOW_HEIGHT / 2 + 0.6

MIC_WINDOW_WIDTH = 3.0   # mm, small relief per F-009 (bounded, no numeric size in sheet)
MIC_WINDOW_Z_MIN = 3.35
MIC_WINDOW_Z_MAX = 5.35
# F-008 SIM tray: dimensions.md/print_plan explicitly mark this "non-fit-critical,
# access-only, none required" -> intentionally NOT modeled (no case action mandated).

# G-04: elephant-foot chamfer at the open rim (bed-contact landmark in print orientation),
# 0.2-0.4mm at 45deg, band midpoint.
RIM_CHAMFER = 0.30  # mm

# OQ-08 (F-013, grade D): sheet leaves the front-face lip an explicit "designer decision,
# not specified here". Chosen: a modest straight (non-overhanging) raised bezel above the
# screen plane - protects the screen face-down without needing an inward taper/overhang,
# keeping the whole cavity a constant cross-section (no internal bridge risk). ASSUMPTION,
# non-fit-critical.
LIP_HEIGHT = 1.2  # mm, raised bezel above D6_SCREEN

Z_TOP = T + LIP_HEIGHT  # 9.90mm, open-rim / bed-contact plane in print orientation

# --- Back-plate architecture: OPEN WINDOW (bumper-style), not a solid disc ---
# Discovered empirically (team_preflight.py support-audit + a wall-thickness ray-cast,
# after correctly Z-translating the STL into the plan's print frame): a SOLID full-
# coverage back plate is a ~155x74mm horizontal disc that appears mid-print with nothing
# below it anywhere in its interior - the "tube" (side walls around the open cavity) is
# hollow for the plan's ENTIRE rim-down build height before the back would need to cap it
# in one shot. That is not a 25mm/40mm-class bridge (S-02's own footprint_note), it is the
# whole interior cross-section (~9200mm2) - no internal rib can fix this without the rib
# itself running the full insertion depth through the phone cavity, which would obstruct
# the phone. The print_plan's own "why this orientation" reasoning addresses only the
# camera boss (G-07); it does not address the general back plate, and G-11 requires this
# class of newly-discovered downward face to route back to plan revision, not be silently
# supported or silently redesigned into a different orientation. Pending that revision,
# this design mitigates within the ACCEPTED orientation/transform by opening a window in
# the general back (bumper-case architecture: perimeter border + camera boss only) - a
# legitimate, common case design that has no disc left to bridge at all, not a workaround
# that hides the problem. See print_notes.md and candidate_readiness.md for the full
# empirical record (both the flawed-solid-back numbers and this mitigation's numbers).
# BACK_BORDER_WIDTH started at 10.0mm (a "real" structural border) - re-audited with
# team_preflight.py support-audit against a correctly Z-shifted STL (see
# case_printer_frame.stl below) and found the SAME problem at smaller scale: a flat
# horizontal shelf, no matter how narrow relative to the whole back, still appears in a
# single step with nothing under it in print order (widening only self-supports on the
# OUTER boundary of an opening, e.g. the camera pocket vs. the general cavity - not on an
# INNER shelf projecting from an already-vertical wall). A true taper self-supports but
# only reaches ~1.2-1.4mm within this case's 1.6mm WALL_BACK depth at <=45 deg, too little
# to bother with over a plain edge. Set to a near-zero clearance (not a structural border):
# the window reaches almost to the cavity boundary on every side, leaving only the WALL_SIDE
# perimeter walls (continuous, unchanged width, self-supporting) and the camera boss.
BACK_BORDER_WIDTH = 0.15  # mm, clean-boolean clearance only, not a structural shelf
# (no corner fillet on the window - see the sharp-corners note at the cut site below)
# Toward the camera pocket: a nonzero-but-small gap (0.15mm, matching the other 3 sides)
# left an ISOLATED 0.15mm-thin freestanding sliver between the two openings (caught by the
# wall-thickness ray-cast: 0.15mm, below the 0.8mm hard floor) - unlike the other 3 sides,
# this edge isn't grafted onto an already-thick continuous wall, so any gap here is a
# standalone thin wall. Fix: overlap the two cuts (negative margin) so they merge into one
# continuous opening with no sliver at all.
BACK_WINDOW_MARGIN_TO_CAM = -0.5  # mm, deliberate overlap into the camera pocket's cut

# ============================================================================
# MODEL
# ============================================================================

W_ext = W + 2 * FIT_SNUG + 2 * WALL_SIDE
L_ext = L + 2 * FIT_SNUG + 2 * WALL_SIDE

# --- exterior shell: side walls + lip + general back plate, one uniform-footprint prism
shell = (
    cq.Workplane("XY")
    .rect(W_ext, L_ext)
    .extrude(Z_TOP - (-WALL_BACK))
    .translate((0, 0, -WALL_BACK))
)
assert shell.val().isValid(), "exterior shell produced an invalid solid"

# --- camera boss: same exterior footprint, extended further into -Z, clipped to the
#     camera Y-band only (a stepped-down back region, not a narrow separate post - this
#     keeps the boss silhouette flush with the side walls above it, zero lateral overhang).
# Deliberately SHARP corners here (no CASE_R fillet): the camera pocket (below) reaches to
# within 1.4mm of the exterior boundary in X (37.0 vs 38.4). CASE_R=11.3mm was sized for
# the phone body's own corner radius and is far too aggressive for this footprint - caught
# empirically via a wall-thickness ray-cast audit, a rounded boss corner there undercut the
# pocket-to-exterior wall to ~0.05mm. A sharp corner keeps the full ~1.4mm margin (above
# both the 1.2mm absolute floor and 0.8mm hard floor); see print_notes.md.
boss_full = (
    cq.Workplane("XY")
    .rect(W_ext, L_ext)
    .extrude(-WALL_BACK - Z_BOSS_BOTTOM)
    .translate((0, 0, Z_BOSS_BOTTOM))
)
boss_yband = (
    cq.Workplane("XY")
    .center(0, (BOSS_Y_MIN + (L_ext / 2 + 5)) / 2)
    .rect(W_ext + 10, (L_ext / 2 + 5) - BOSS_Y_MIN)
    .extrude(2 * (Z_BOSS_BOTTOM - (-WALL_BACK) - 1), both=True)
)
boss = boss_full.intersect(boss_yband)
assert boss.val().isValid(), "camera boss clip produced an invalid solid"

body = shell.union(boss)
assert body.val().isValid(), "shell+boss union produced an invalid solid"

# --- main phone cavity: through-cut, open at the top (insertion mouth), snug band M-019.
# Bottom of the cut is Z=-0.05 (a hair below the phone's own back-contact plane, Z=0) -
# NOT further down: an earlier version started this cut at Z=-1 "for clean boolean
# overlap" and it silently left an unintended 0.6mm solid plug sitting behind the phone
# (Z=-1.6..-1) with a 1mm AIR GAP between it and the phone's actual back (Z=0) - caught by
# re-measuring the wall-thickness ray-cast, not by the interference check (which reported
# 0 precisely because the phone and case never touched there at all). The small -0.05mm
# epsilon here is only to dodge an exact-coincident-face boolean sliver against
# phone_reference.stl at Z=0 during verification, not a real design gap.
cavity = (
    cq.Workplane("XY")
    .rect(W + 2 * FIT_SNUG, L + 2 * FIT_SNUG)
    .extrude(Z_TOP + 2)
    .translate((0, 0, -0.05))
)
cavity = cavity.edges("|Z").fillet(CAVITY_R)
body = body.cut(cavity)
assert body.val().isValid(), "main cavity cut produced an invalid solid"

# --- back window (bumper-style, see "Back-plate architecture" note above): opens the
# general back plate so there is no large horizontal disc left to bridge. Leaves a solid
# perimeter border (BACK_BORDER_WIDTH) connecting to all 4 side walls, and stays clear of
# the camera pocket/boss by BACK_WINDOW_MARGIN_TO_CAM. Cut straight through the back wall
# (Z -1.6 to -0.05) - vertical walls only, no new horizontal roof/floor introduced.
cavity_half_w = W / 2 + FIT_SNUG   # 36.80mm, cavity boundary (not exterior)
cavity_half_l = L / 2 + FIT_SNUG   # 78.00mm
# X half-width matches the camera pocket's own half-width (CAM_WINDOW_W/2), not the
# cavity's - a mismatched, narrower X boundary at the pocket seam left another isolated
# thin sliver (down to 0.078mm, caught the same way as the Y-seam above) where the two
# cuts' side edges didn't line up. Same X boundary on both cuts means one continuous
# opening with no seam geometry at all.
back_window_x = CAM_WINDOW_W / 2                           # 37.00mm half-width
back_window_y_min = -cavity_half_l + BACK_BORDER_WIDTH      # -68.00mm
back_window_y_max = (CAM_WINDOW_Y_MAX - CAM_WINDOW_H) - BACK_WINDOW_MARGIN_TO_CAM  # 49.65mm
back_window = (
    cq.Workplane("XY")
    .center(0, (back_window_y_min + back_window_y_max) / 2)
    .rect(2 * back_window_x, back_window_y_max - back_window_y_min)
    .extrude((WALL_BACK + 0.5) + 0.5)  # spans generously past both faces of the back wall
    .translate((0, 0, -WALL_BACK - 0.5))
)
# Deliberately SHARP corners (no fillet): same corner-conflict pattern as the boss and the
# camera pocket earlier in this file - a rounded corner here recedes from the shared seam
# with the (sharp-cornered) camera pocket and reopens a thin/near-zero sliver right at the
# seam (caught at 0.05mm via the wall-thickness ray-cast, same technique as before).
body = body.cut(back_window)
assert body.val().isValid(), "back window cut produced an invalid solid"

# --- camera relief pocket: loose band M-020, clears the bump + protects it with the boss
cam_pocket = (
    cq.Workplane("XY")
    .center(0, CAM_WINDOW_Y_MAX - CAM_WINDOW_H / 2)
    .rect(CAM_WINDOW_W, CAM_WINDOW_H)
    .extrude(1 - (Z_BOSS_BOTTOM - 1))
    .translate((0, 0, Z_BOSS_BOTTOM - 1))
)
body = body.cut(cam_pocket)
assert body.val().isValid(), "camera relief pocket cut produced an invalid solid"

# --- button windows (D4_RIGHT wall), split by a self-supporting rib -> each segment
#     <=25mm bridge span, SELF_SUPPORT_REQUIRED per G-08, avoids S-03 entirely
btn_cut_x_min = W / 2 + FIT_SNUG - 0.5   # start just inside the cavity wall
btn_cut_x_max = W_ext / 2 + 0.5           # through and past the exterior face
btn_segments = [
    (BTN_WINDOW_Y_MIN, BTN_RIB_CENTER_Y - BTN_RIB_WIDTH / 2),
    (BTN_RIB_CENTER_Y + BTN_RIB_WIDTH / 2, BTN_WINDOW_Y_MAX),
]
for y_min, y_max in btn_segments:
    cut = (
        cq.Workplane("XY")
        .center((btn_cut_x_min + btn_cut_x_max) / 2, (y_min + y_max) / 2)
        .rect(btn_cut_x_max - btn_cut_x_min, y_max - y_min)
        .extrude(BTN_WINDOW_Z_MAX - BTN_WINDOW_Z_MIN)
        .translate((0, 0, BTN_WINDOW_Z_MIN))
    )
    body = body.cut(cut)
assert body.val().isValid(), "button window cuts produced an invalid solid"

# --- USB-C port window (D3_BOT wall)
bottom_cut_y_min = -L_ext / 2 - 0.5
bottom_cut_y_max = -L / 2 - FIT_SNUG + 0.5
usbc_cut = (
    cq.Workplane("XY")
    .center(USBC_CENTER_X, (bottom_cut_y_min + bottom_cut_y_max) / 2)
    .rect(USBC_WINDOW_WIDTH, bottom_cut_y_max - bottom_cut_y_min)
    .extrude(BOTTOM_WINDOW_Z_MAX - BOTTOM_WINDOW_Z_MIN)
    .translate((0, 0, BOTTOM_WINDOW_Z_MIN))
)
body = body.cut(usbc_cut)

# --- bottom-left / bottom-right grille windows (D3_BOT wall)
for center_x in (GRILLE_L_CENTER_X, GRILLE_R_CENTER_X):
    grille_cut = (
        cq.Workplane("XY")
        .center(center_x, (bottom_cut_y_min + bottom_cut_y_max) / 2)
        .rect(GRILLE_WINDOW_WIDTH, bottom_cut_y_max - bottom_cut_y_min)
        .extrude(BOTTOM_WINDOW_Z_MAX - BOTTOM_WINDOW_Z_MIN)
        .translate((0, 0, BOTTOM_WINDOW_Z_MIN))
    )
    body = body.cut(grille_cut)
assert body.val().isValid(), "USB-C/grille window cuts produced an invalid solid"

# --- top mic relief (D2_TOP wall)
top_cut_y_min = L / 2 + FIT_SNUG - 0.5
top_cut_y_max = L_ext / 2 + 0.5
mic_cut = (
    cq.Workplane("XY")
    .center(MIC_OFFSET_X, (top_cut_y_min + top_cut_y_max) / 2)
    .rect(MIC_WINDOW_WIDTH, top_cut_y_max - top_cut_y_min)
    .extrude(MIC_WINDOW_Z_MAX - MIC_WINDOW_Z_MIN)
    .translate((0, 0, MIC_WINDOW_Z_MIN))
)
body = body.cut(mic_cut)
assert body.val().isValid(), "mic relief cut produced an invalid solid"

# --- G-04 elephant-foot chamfer at the open rim (bed-contact landmark, Z = Z_TOP)
rim_edges = body.edges(cq.selectors.NearestToPointSelector((0, 0, Z_TOP)))
body_chamfered = None
try:
    body_chamfered = body.faces(">Z").edges().chamfer(RIM_CHAMFER)
    assert body_chamfered.val().isValid()
    body = body_chamfered
except Exception as exc:  # pragma: no cover - fallback path, reported in print_notes.md
    print("WARNING: top-face chamfer failed, shipping without it:", exc)

vol_final = body.val().Volume()
bb = body.val().BoundingBox()
print("in-memory volume mm3:", vol_final)
print("in-memory bbox: x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" %
      (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))

# ============================================================================
# FIT COUPON (plan's Coupon section): D4_RIGHT x D2_TOP corner + one full-height segment
# of each adjacent wall (F-002 corner radius + M-019 snug band on 2 orthogonal walls),
# the G-04 rim chamfer base, and a partial witness of the F-006 volume-rocker window.
# ============================================================================
COUPON_X_MIN = 5.0
COUPON_Y_MIN = 30.0
coupon_box = (
    cq.Workplane("XY")
    .center((COUPON_X_MIN + W_ext / 2 + 2) / 2, (COUPON_Y_MIN + L_ext / 2 + 2) / 2)
    .rect(W_ext / 2 + 2 - COUPON_X_MIN, L_ext / 2 + 2 - COUPON_Y_MIN)
    .extrude(Z_TOP + 2 - (Z_BOSS_BOTTOM - 2))
    .translate((0, 0, Z_BOSS_BOTTOM - 2))
)
coupon = body.intersect(coupon_box)
assert coupon.val().isValid(), "coupon clip produced an invalid solid"
coupon_bb = coupon.val().BoundingBox()
print("coupon bbox: x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" %
      (coupon_bb.xmin, coupon_bb.xmax, coupon_bb.ymin, coupon_bb.ymax,
       coupon_bb.zmin, coupon_bb.zmax))

# ============================================================================
# EXPORT (native design frame - matches phone_reference.stl for direct verification)
# ============================================================================
cq.exporters.export(body, "case.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "case.step")
cq.exporters.export(coupon, "case_coupon.stl", tolerance=0.01, angularTolerance=0.1)
print("exported case.stl, case.step, case_coupon.stl")
