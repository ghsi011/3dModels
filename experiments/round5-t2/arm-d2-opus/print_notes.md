# Print notes — round-5 D2 candidate (Arm O / Opus)

**DESIGNER SELF-CHECK — NON-ACCEPTANCE.** Bar-engaging, open-bottom hand tool that captures the
F02 cross-bar (`62.0 × 11.7 × 24.0 mm`) and transfers hand torque about D3, printed support-free
on its side.

## Material / process
- Bambu Lab X2D, dry plain PETG, main 0.4 mm hardened nozzle, single nozzle.
- 0.20 mm layers, 0.42 mm line width. G-07 slicing floor (final owner = print engineer):
  ≥4 perimeters, ≥5 top/bottom, 30–40 % gyroid. Geometry meets G-01 (≥1.20 mm) independently of
  infill; the thinnest structural wall is 2.0 mm.
- No load/torque rating is claimed (Q03).

## Orientation and transform (fixed by plan)
- `T_printer_from_installed = [[1,0,0,0],[0,0,-1,0],[0,1,0,16],[0,0,0,1]]` → `printer_X=X`,
  `printer_Y=-Z`, `printer_Z=Y+16`. The part prints lying on its installed **-Y** face.
- **P_BED** = the installed `Y=-16.000` land (`printer_Z=0`), the sole bed-contact face
  (`1582 mm²` ≥ 200). Elephant-foot relief: 0.30 mm bevel at **48° from horizontal** (≥45°,
  self-supporting; transformed `normal_z=-0.669 > -0.70710679`). The nominal "0.30 mm × 45°"
  chamfer is cut slightly steeper on purpose so the tessellated facet clears the S-01 downface
  threshold with margin.

## Why it is support-free (the hard constraint)
Because `printer_Z ∝ installed_Y`, any surface facing installed **-Y** points down while printing.
- The installed **+Y** channel wall would be a flat horizontal roof (`printer_Z=const`, area
  `≈24×63 mm`). It is replaced by a **gable ridge running along X** (apex at installed
  `Y≈20.1, Z≈13.85`, slopes at 52° from horizontal → `normal_z≈-0.62`), so the roof self-supports.
- The bar-cavity **top** wall (installed `Z=24.7`) transforms to a vertical printer wall
  (`+printer_Y`), so it needs no support.
- The **mouth** stays open toward installed `-Z` → `+printer_Y` (horizontal), never roofed.
- Mouth lead-in and bearing fillets are placed only on edges whose normals stay `> -0.7071` in
  printer Z (`-Y` rim, X-ends, `-Y` inner corners).
- `team_preflight.py support-audit` S-01..S-04 = **0.000 mm² out-of-limit**, supports OFF.

## Fit / clearances (re-imported STL, vs bar 62 / 11.7 / 24)
- End (X) per side: **0.60 mm** (wall ±31.6). Side (Y) per side: **0.40 mm** (-Y wall -6.25,
  +Y eave +6.25). Seated top (Z): **0.70 mm** (ceiling 24.7).
- Cap-face (D0) clearance outside F02: **3.0 mm** (tool never below `Z=3`), ≥0.60 (G-03).
- Seated interference: none (max signed distance −0.317 mm; the tight point is the diagonal at
  the -Y/end inner fillet corner, flats hold full clearance). Insertion is a straight `-Z`
  prismatic slide; the ceiling gives 0.70 mm over-travel as the seating stop.

## Weak directions / cautions
- Torque is reacted mainly by the two ±Y bearing walls and the X-end walls; the +Y wall bears
  near the gable eaves (top and mouth ends of the bar). Layer lines run in `printer_XY`; the
  weakest direction is delamination across `printer_Z` (installed +Y) — the gable and top slab
  keep the load path in-plane.
- F03/F04 (bar end treatment, root fillet) are unknown/bounded: the entrance is smooth and
  radiused, contacts nothing below `Z=3`, and keys no hidden feature.

## Coupon
`candidate_coupon.py` → `candidate_coupon.stl`: the same named production cavity/gable/wall/
clearance parameters, full 62 mm F02 X span, production Y width/clearance, **21.0 mm** Z
engagement, rigid hand tab, comfort fillets omitted. Support-free (S-01 = 0.000 mm²). Use it for
the real-bar PETG insert + ±10° rotation fit test before the final tool print.

## Files
Source: `candidate_model.py`, `candidate_coupon.py`. Exports: `candidate_tool.stl/.step`,
`candidate_coupon.stl`. Measurement: `measure.py`/`measure.json`. Audits:
`S-0x-support-audit.json`, `candidate_preflight.json`, `candidate_preflight_validation.json`
(PASS). Renders: `render_exterior.png`, `render_mating_section.png`,
`render_print_orientation.png`, `render_overlay.png`.
