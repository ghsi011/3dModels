---
contract: designer-notes
job_id: pixel7-case-metrology
candidate_id: pixel-step4-design
owner: cad-designer
backend: CadQuery 2.8.0 (system python), re-imported with trimesh for measurement
dimensions_revision: 1
print_plan_revision: 1
reference_sha256: 5d683184b814d7089b4075354b81aa45aa8aaae35aa0bb45c12324aaea692b7f
updated_utc: 2026-07-24T23:30:00Z
---

# Print notes — Google Pixel 7 protective case (candidate)

`case_model.py` is the parametric CadQuery source. Every design-driving number cites its
sheet ID (`dimensions.md`) or plan rule (`print_plan.md` / `print_plan_checks.json`) inline
as a comment; ASSUMPTION-flagged values (e.g. `LIP_HEIGHT`) are non-fit-critical designer
choices where the sheet/plan explicitly left the decision open (OQ-08).

## Geometry summary

- **Body cavity**: rounded rect `W+2*FIT_SNUG` x `L+2*FIT_SNUG` (73.60 x 156.00 mm),
  `CAVITY_R = R_CORNER + FIT_SNUG = 9.70 mm`, open through-cut from the interior back
  contact plane (native Z=-0.05, a hair below the phone's own Z=0) up through the lip top
  (`Z_TOP = T + LIP_HEIGHT = 9.90 mm`).
- **Side walls**: `WALL_SIDE = 1.6 mm` nominal (G-05), wrapping the full perimeter.
- **Camera relief**: pocket `74.00 x 21.20 mm` (M-020 loose band, `CAM_CLR=0.40mm/side`
  applied on all 4 sides), floor at native Z=-3.14 (clears the 2.74mm bump by 0.40mm),
  protected by a raised boss standing proud to Z=-4.74 (the model's lowest point) - becomes
  the last-printed, self-supporting top feature in the plan's rim-down orientation (G-07).
- **Back plate: OPEN WINDOW, not a solid disc.** This is the single biggest design decision
  in this candidate and is NOT what a first pass produced - see "Back-plate architecture"
  below for the full story. The general back is a bumper-style opening (window reaching
  almost to the cavity boundary on every side, ~0.15mm clean-boolean clearance only);
  coverage is provided by the perimeter side walls (edge/corner protection) and the camera
  boss (lens protection), not a full back plate.
- **Button windows** (D4_RIGHT, F-006/F-007): one 38mm elongated relief per the sheet's own
  M-021 strategy (Y 17.8-55.8, native frame), split by a single 1.8mm self-supporting rib
  at Y=36.8 into two ~18.1mm segments (both <=25mm, G-08's "fine" bridge class).
- **USB-C / grilles / mic**: individual loose windows per M-022/F-009, each a few mm wide,
  trivially self-supporting (G-09/G-10).
- **Rim**: G-04 elephant-foot chamfer, `RIM_CHAMFER=0.30mm` at 45deg, both inner and outer
  edges of the open-rim annular face (bed-contact landmark in print orientation).
- **Exterior corners**: deliberately SHARP (no fillet) - see "Exterior corner treatment"
  below.
- **Fit coupon** (`case_coupon.stl`): D4_RIGHT x D2_TOP corner clip (X>=5, Y>=30, full Z
  height), per the plan's Coupon section - captures the corner radius, a segment of each
  adjacent wall, the rim chamfer, and a partial witness of the volume-rocker window.

## Parameter -> contract mapping (selected)

| Parameter | Value | Source |
|---|---:|---|
| `L`, `W`, `T`, `R_CORNER` | 155.6, 73.2, 8.7, 9.5 mm | re-confirmed against re-imported `phone_reference.stl` bounds/section measurements (M-001..M-004) |
| `FIT_SNUG` | 0.20 mm/side | M-019 band [0.10,0.30], midpoint |
| `CAM_CLR` | 0.40 mm/side | M-020 band [0.30,0.50], midpoint |
| `PORT_CLR` | 0.40 mm/side | M-022 band [0.30,0.50], midpoint |
| `WALL_SIDE`, `WALL_BACK`, `WALL_BOSS` | 1.6 mm each | G-05 nominal (4x0.4mm line width) |
| `RIM_CHAMFER` | 0.30 mm | G-04 band [0.2,0.4], midpoint, 45deg |
| `LIP_HEIGHT` | 1.2 mm | ASSUMPTION - OQ-08 leaves front-face lip as a designer decision |
| `BTN_RIB_WIDTH` | 1.8 mm | designer choice, self-supporting alternative to S-03 per G-08 |

## Honest limits and design decisions requiring a human read

### Back-plate architecture (the big one)

The first working version of this case had a solid, full-coverage back plate
(`WALL_BACK=1.6mm` everywhere except the camera relief). It passed interference and
clearance checks cleanly. It **failed printability catastrophically**: re-running
`team_preflight.py support-audit` against a *correctly Z-translated* copy of the STL (see
"Support-audit STL frame" below) measured **~9,200 mm² of unsupported horizontal area** -
essentially the entire interior cross-section appearing in one print layer with nothing
underneath it anywhere, because the plan's rim-down orientation makes the case a hollow
tube (open cavity) for its *entire* build height before the back plate would need to cap
it in a single step. This is not a 25-50mm-class bridge (fdm-design.md §1); it is the whole
opening at once, and no internal rib can fix it without the rib itself running the full
phone-insertion depth through the cavity, which would obstruct the phone.

`print_plan.md`'s own "Why this orientation" section reasons carefully about the camera
boss specifically (G-07) and does not address the general back plate. Per G-11 ("any newly
discovered downward face routes back to `PRE_DESIGN_PRINT_PLAN` for revision; never
silently added as late support"), this candidate does **not** silently add support and
does **not** unilaterally pick a different orientation (that is print-engineer/plan-owner
territory, out of a candidate designer's remit). Instead, staying fully inside the
accepted orientation/transform, this candidate mitigates by opening the back into a
bumper-style window (perimeter border + camera boss only, no back disc to bridge at all).
This is a legitimate, common case architecture, not a workaround that hides the finding -
both the broken-solid-back numbers and this mitigation's numbers are on the record (see
`candidate_readiness.md`). **This should still route back to a print-plan review**: the
plan's own DFM reasoning did not cover this case, and a future plan revision may choose a
different orientation, an explicit `SUPPORT_ALLOWED` disposition for the back, or accept
the open-back architecture as-is.

Iterating toward the final geometry surfaced (and fixed) two further real defects, both
caught by the wall-thickness ray-cast audit, not by the interference check:
- A prior cavity-cutter Z-range (`Z=-1` "for clean boolean overlap") silently left an
  unintended 0.6mm solid plug sitting *behind* the phone with a 1mm air gap in front of it
  - the phone never actually touched the case's back wall. Interference reported 0 exactly
  because nothing overlapped. Fixed by starting the cavity cut at Z=-0.05 (a hair below the
  phone's true Z=0 contact plane, only enough to dodge a coincident-face boolean sliver).
- Two corner-fillet-vs-sharp-corner conflicts (camera boss corner, then the back-window
  seam with the camera pocket): a rounded corner recedes diagonally and can undercut a
  sharp-cornered opening right at the corner, down to ~0.04-0.15mm locally. Both fixed by
  making the offending corners sharp instead of filleted (documented inline in
  `case_model.py` at each site).

### Exterior corner treatment

Exterior corners are sharp, not rounded. An 11.3mm exterior fillet (matching the cavity's
own scale) was tried first and undercut the camera-pocket-to-exterior wall to ~0.04mm
(caught by the same ray-cast audit) - the loose camera pocket reaches within 1.4mm of the
exterior boundary in X, and essentially any meaningfully-sized exterior fillet there drops
below the 1.2mm absolute wall floor at the diagonal. Only the CAVITY corner radius is
plan-gated (G-03/E-01); the exterior corner shape is a free designer choice, so sharp
corners were kept for simplicity and margin rather than chasing a small/regional fillet.
A future revision could locally fillet the 2 non-camera corners if a fully rounded
exterior is wanted.

### Insertion sweep (Phase-4 check 2) is not applicable in the classic straight-line sense

A straight-line rigid sweep (translate the phone along +Z from seated, check interference
at each offset) reports **zero interference from t=0 to ~1mm**, then contact starting
around t=1.5mm - not from the main body cavity (which stays open the whole way, snug band
intact) but from the phone's button-pad protrusion (a 0.6mm bump, fixed at a specific
Z-location on the phone) sliding outside the case's fixed button-window Z-band during
transit. This is expected and correct for a wrap-around TPU pocket case: assembly is by
flexing the case around the phone's profile (edge/corner-first), not a rigid axial slide -
exactly what the print plan's own coupon pass criteria says explicitly: "seats into the
coupon with firm hand pressure (**snug, not free-sliding**)". Reported honestly rather than
engineered around by oversizing the button window.

### Support-audit STL frame

`print_plan_checks.json`'s `support_rules[*].model_to_printer_matrix` is rotation-only
(`R=diag(1,-1,-1)`, zero translation). Applying it directly to `case.stl` (native frame,
`Z_TOP=9.9mm`) maps the open rim to printer Z=-9.9, not 0 - the tool then can't recognize
ANY of the rim as legitimate bed contact and flags the whole thing as unsupported
(~10,000mm² of false positives, confirmed empirically before this was understood). The
plan's own transform note explains why: translation is "not a fixed numeric offset because
final wall thickness is a CANDIDATE_BUILD decision, not a pre-design one" - i.e. the plan
intentionally left Z-translation out of the stored matrix since it can't know a candidate's
`Z_TOP` in advance. This candidate supplies it by feeding the shared tool a deterministic,
reproducible Z-only translation of `case.stl` (`case_printer_frame.stl` = `case.stl`
translated by `(0,0,-9.9mm)`, i.e. shifted so the rim lands at native Z=0) rather than a
pre-rotated file, so the plan's own rotation-only matrix does the rest correctly. Verified:
after the shift, `case_printer_frame.stl`'s bed-contact area under the plan's matrix comes
out to a physically sensible ~552mm² (a thin rim annulus), not ~9,900mm² (the whole part).
Full detail and the resulting hash-mismatch consequence for `validate-receipts` is in
`candidate_readiness.md`.

### Material / process

TPU 95A per the accepted plan (compliance strategy for OQ-01's thickness spread and the
M-019 snug band). No FreeCAD touched; CadQuery only, per commission scope.

## Files

See `candidate_readiness.md` "Commands and hashes" for the full file/hash table.
