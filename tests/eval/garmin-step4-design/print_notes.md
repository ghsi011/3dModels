---
contract: print-notes
job_id: garmin-7x-charging-dock
candidate_id: garmin-step4-design
owner: cad-designer
status: designer notes -- NON-ACCEPTANCE
updated_utc: 2026-07-25T00:00:00Z
---

# Print notes — Garmin Fenix 7X charging dock/cradle candidate

## Scope and what is NOT built

This is a **watch-capture cradle**, not yet a functioning charger. Per `print_plan.md` G-09
(BLOCKED, citing `dimensions.md` OQ-01/F-003/M-009: no caseback photo exists, pin
location/spacing/pattern UNKNOWN): **zero charge-contact, pogo-pin keep-out, puck boss, or
cable-channel geometry was added anywhere.** The pocket floor is a plain, flat, uncommitted
disc at the caseback contact plane. Do not read the flat floor as "no contacts" — it means the
metrology has no evidence for where they are.

## Parameters and what drives them

| Parameter | Value | Source |
|---|---:|---|
| `CASE_DIA` | 51.75 mm | `dimensions.md` M-001/M-003; re-confirmed exact against `watch_reference.stl` |
| `CASE_THICKNESS` | 14.9 mm | `dimensions.md` M-004 |
| `FIT_CLR` | 0.25 mm/side | G-01 band [0.15, 0.35] midpoint |
| `POCKET_BORE_DIA` | 52.25 mm | `CASE_DIA + 2*FIT_CLR` |
| `POCKET_DEPTH` | 15.15 mm | G-02 band [15.05, 15.25] midpoint |
| `WALL_STRUCT` | 1.6 mm | G-03 |
| `FLOOR_THICKNESS` | 3.0 mm | designer choice, comfortably above G-03's 1.6mm structural floor (G-09 blocked pocket floor treated conservatively as structural) |
| `BUTTON_RELIEF_HALF_ANGLE` | 25 deg | > asin(9.0/26.125)=20.4 deg, `watch_reference.py`'s own button-pad half-width |
| `BAND_RELIEF_HALF_ANGLE` | 32 deg | > asin(13.0/26.125)=29.9 deg |
| `LIP_RADIAL_REACH` | 1.0 mm | inside the S-01 3.5mm cap; sized for a small, printable snap-clip deflection |
| `LIP_HEIGHT` | 2.0 mm | designer choice |
| `LIP_CENTERS_DEG` | 41.5, 221.5 | clear quadrants avoiding both relief notches |
| `LIP_HALF_ARC_DEG` | 12 deg | 24 deg per finger, 48 deg combined, inside S-01's 180 deg cap |
| `TILT_DEG` | 27.5 deg | print_plan.md assumed band [20, 35] midpoint |
| `BASE_CHAMFER` | 0.25 mm | inside E-01 band [0.2, 0.4], see "Base architecture" below for why not the band midpoint |
| `KEEL_R` / `KEEL_DEPTH` | 50.0 / 55.0 mm | see "Base architecture" below |

## Frame and orientation

Model-to-printer transform is **identity** (`print_plan.md`): the exported `cradle.stl` IS the
print-frame STL, `STAND_BASE_PLANE` at world Z=0. The pocket/wall/lip geometry ("puck") is
built in a **pocket-local frame** matching `watch_reference.py`'s own convention exactly (floor
at local Z'=0, +Z' = insertion axis), then rotated `TILT_DEG` about world X and translated by
`WEDGE_HEIGHT` to reach the installed pose — this lets Phase-4 checks compare the exported
cradle directly against `watch_reference.stl` with the identical transform applied to both.

## The retention lip is a compliant spring-clip, not a shelf over a bezel step

`dimensions.md` OQ-05: no evidence exists for any step/taper on the case — it is a plain right
cylinder for its full height. A literal "curl over the bezel edge" therefore has nothing to
catch. This design instead makes the lip two small (24 deg each) spring-clip fingers whose
inner radius (`lip_r_inner` = 25.125mm) is **smaller** than the case radius (25.875mm) — a
0.75mm/side overlap the fingers must flex past on insertion/removal, matching
`fdm-design.md` §4's snap-fit guidance (PETG tolerates a taper-to-tip flex arm; PLA would not).

**This means a rigid straight-line insertion/removal sweep is not clean past the lip fingers**
by design — see `candidate_readiness.md`'s insertion-sweep row. This is inherent to any lip
retention feature over a non-stepped case (the print plan's own "why this orientation" section
calls the lip "a true undercut... no orientation... eliminates it"); it is not something this
candidate could design around without abandoning the retention feature the plan requires.

## Base architecture — three design attempts, in order

The wedge/base connecting the tilted puck to `STAND_BASE_PLANE` is entirely this designer's
own choice (not contract-numbered). It took three attempts to get right; all three and their
measured numbers are kept here rather than silently erased, because they are load-bearing
design history:

1. **Ellipse-to-tilted-circle loft** (wide flat bottom ellipse, small circular top profile
   itself tilted to match the puck). Measured wall thickness near the ellipse's own
   highest-curvature point (its back apex): 0.05–0.6mm — a genuine pinch (confirmed with the
   fillet removed and with an opposing-face-normal filter, not a measurement artifact),
   independent of how gentle the taper ratio was. **Rejected.**
2. **Circle-to-tilted-circle loft** (same idea, ellipse swapped for a circle to remove the
   curvature mismatch) avoided the pinch but still measured only 0.04–0.45mm near the tilted
   top profile's own boundary. A third variant with an **untilted flat top** fixed the wall
   thickness but exposed the tilted puck's own floor disc rising above the flat top plane on
   one side — a genuine new unsupported overhang (`team_preflight.py support-audit` jumped
   from 45mm² PASS to 932mm² FAIL, confirmed independent of base radius). **Rejected.**
3. **KEEL** (built): a plain, untilted cylinder unioned onto the puck **in local frame, before
   any tilt is applied** (zero shape mismatch, no loft at all), then the combined solid is
   rotated/translated with the single rigid transform every other body in this file uses, and
   cut flat at world Z=0. Because the keel shares the puck's own axis before tilting, the
   puck's floor can never rise above the keel's own material. **This is what `cradle.stl`
   ships.**

`STAND_BASE_PLANE`'s own rim is consequently an ellipse-like curve (the tilted keel cut flush
at Z=0), not a true circle. A uniform 3D E-01 fillet's *apparent* radius on that curve scales
with the curve's own local curvature (tightest on the "back" arc, where the tilt compresses
the ellipse most). `KEEL_R` was enlarged from an initial 36mm to 50mm specifically to flatten
that curvature until the measured E-01 samples (0.25–0.39mm, see `candidate_preflight.json`)
fit inside the plan's [0.2, 0.4]mm band everywhere sampled — at the smaller radius, the same
nominal fillet measured 0.24–0.65mm, exceeding the band on roughly a third of the perimeter.
The tradeoff is a materially larger base footprint (~100mm across) than a minimal design would
need; documented here as a deliberate, measured choice, not an oversight.

## Honest limits (non-exhaustive; see `candidate_readiness.md` for the full gated table)

1. **E-03 (lip finger top-outer comfort edge) ships SHARP, not filleted.** The `.fillet()`
   operation (attempted at radii from 1.2mm down to 0.3mm, both on the standalone finger
   before its union into the body and on the assembled body's edge afterward) failed OCC's
   fillet solver on this specific compound edge every time — either an exception
   (`BRep_API: command not done`) or a completed-but-`isValid()==False` result. The selected
   edge measured as OCC geometric type `CIRCLE` rather than the expected `LINE` for this
   finger's single-chord (`pie_wedge(..., n=1)`) construction, suggesting the boolean union
   reclassified/rebuilt the edge in a way this designer did not fully diagnose within this
   commission's time budget. `EXPOSED_COMFORT` classification (not `EXPOSED_FUNCTIONAL`) — a
   sharp edge here is a real but non-critical (cosmetic/comfort) defect, not a fit or
   structural one. Reported honestly rather than fabricating a passing sample.
2. **G-04 absolute wall floor (0.8mm) is not met at the E-01 base-perimeter fillet edge
   specifically** — genuine (opposing-face-normal-filtered) minimum ~0.53–0.59mm there. The
   **G-03-named structural features** (pocket bore wall, retention-lip cross-section) measure
   a clean ~1.598–1.60mm minimum, matching the 1.6mm nominal exactly — G-03 is satisfied. The
   base's *bulk* material away from the fillet edge is a large solid disc, confirmed
   comfortably thick in isolated keel-only tests during development (~1.5mm+ without the E-01
   fillet). The shortfall is localized to the small curved fillet transition itself, not a
   thin shell anywhere in the design.
3. **Bore diameter mesh-tessellation undershoot**: re-measured min diametral bore = 52.02mm
   vs. the G-01 target band's own lower bound of 52.05mm (52.25 nominal + 2×0.15mm min side
   clearance) — a 0.03mm shortfall attributable to the exported mesh's polygonal
   approximation of a true circle (`angularTolerance=0.1` faceting), not the parametric
   design (`POCKET_BORE_DIA` is exactly 52.25mm in source). The max side of the band
   (52.45mm) is met with room (52.453mm measured).
4. **Raw boolean interference total is noisy at the Z'=0 seating plane.** The watch caseback
   and the cradle floor are designed to sit exactly flush (zero nominal gap) — a
   `trimesh.boolean.intersection` there reports a nonzero sliver from floating-point
   coincident-face noise (~65–105mm³ across different runs of the same geometry), not real
   interference. `verify.py` uses dense Monte Carlo point-containment sampling instead, which
   confirms **zero** genuine general-bore interference and **~37.9mm³** concentrated exactly
   at the S-01 lip band (the intended engagement) — see `candidate_readiness.md`.
5. **No PETG (or any) coupon has actually been printed.** `cradle_coupon.stl` is geometry
   only — a standalone ~110 deg bore-arc segment at this design's G-03 wall thickness and G-02
   pocket depth, per `print_plan.md`'s Coupon section. It has not been validated by test
   printing within this commission.
6. **G-06/G-07 keep-out reliefs are full open notches**, not bulges to exactly the required
   diameter — trivially satisfies "≥ Ø56.8mm" (G-06) and "not pinched/trapped" (G-07) since
   an open notch has no material at all in that window, but is a more material-removing
   response than a minimal relief bulge would be. Chosen because a local OD bulge to 57.5mm
   would have exceeded this design's own wall OD (55.45mm at the smaller first-pass keel;
   moot at the final larger keel, but the notch was already built and validated by then, and
   an open notch also doubles as a button/band-lug viewing and access window).
7. **Charge interface is entirely unbuilt** (see "Scope" above) — this is the plan's own
   G-09 requirement, not a limitation of this candidate specifically, but it means the part
   this commission delivers is a capture cradle, not a functioning charger.

## Coupon

`cradle_coupon.stl`: a standalone ~110 deg arc segment of the general bore wall, at
`POCKET_BORE_DIA`/`WALL_STRUCT`/`POCKET_DEPTH` identical to the full cradle, independent of the
stand/tilt architecture — matches `print_plan.md`'s Coupon section (a standalone fixture
buildable against the accepted `watch_reference.stl` case geometry, testable with the printed
Ø51.75mm reference gauge or the real watch). Does not include the retention lip, notches, or
base — those require the full candidate geometry to test meaningfully per the plan's own
"what this coupon does not cover" note, and belong to a post-verification pass.

## Material and process

PETG, per `print_plan.md` (0.20mm layers, 4 walls min around the pocket/seat/lip region, 5
top/bottom, 30–40% gyroid elsewhere, X2D main nozzle only). Slicer profile finalization,
temperature/fan/flow, and the field-test insert/remove-cycle protocol are explicitly deferred
to post-verification per the plan — not decided here.

## Weak directions / risks for a follow-up designer or verifier

- The two lip fingers are the only load path resisting the watch lifting straight out; a
  finger crack (thin, ~2.6mm radial cross-section, PETG, repeated flex) is the most likely
  long-term failure mode. Not a print defect, a material-fatigue risk over many insert/remove
  cycles — flagged for the plan's own deferred field-test protocol.
- The base is large (~100mm across) relative to the watch (~52mm) — a deliberate tradeoff for
  E-01 compliance (see "Base architecture"), but a real material/print-time cost a future
  revision could reduce with a more sophisticated (non-uniform) fillet strategy instead of a
  bigger footprint.
- `.fillet()` on booleaned/unioned edges was unreliable throughout this build (E-02 initially
  failed fillet-then-cut order; the lip fingers' own E-03/E-04 needed fillet-after-union
  instead of fillet-before-union; E-03 never succeeded at any tested radius). Any further
  geometry changes near the lip fingers or the notch/rim boundary should expect the same
  class of OCC fillet fragility and budget time to diagnose it via the exported mesh directly
  (vertex/edge inspection), not just trust `isValid()`/no-exception as proof a fillet applied
  where intended.
