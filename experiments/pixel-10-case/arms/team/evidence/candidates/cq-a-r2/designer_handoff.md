# cq-a-r2 designer correction handoff

Status: `CANDIDATE_READY` for a fresh independent verification only. This is not an acceptance report.

## Bound inputs

- Accepted `dimensions.md` r3.
- Accepted `print_plan.md` r1.
- Accepted ref-2 fixture STL SHA-256: `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91`.
- Rejection input: `verification_report.md` r1, defect `CQ-A-V1-001`.

## Geometry correction

`SCREEN_OPENING_OVERTRAVEL_MM = 1.0` moves the cavity start one millimetre beyond the exterior screen plane. The resulting subtraction opens the full screen face while retaining the continuous 1.6 mm exterior perimeter as the bounded protective lip. No new support, secondary body, or screen-side roof was added.

## Regenerated artifacts

- `../../../../model.py`, `../../../../verify.py`
- `../../../../pixel10_case_cq_a.stl`, `../../../../pixel10_case_cq_a.step`
- `exterior_isometric_open_screen.png`
- `transparent_fit.png`
- `section_y_mid.png` and `section_y_mid.stl`
- `print_orientation_multiview.png`

## Designer self-check evidence

The final CadQuery strict runner completed successfully and its re-import identified a watertight 2,804-triangle STL. The non-authoritative source-coordinate mating check observed 0.000000 mm3 interference at seat and at screenward reference offsets 1, 5, 9, 13, and 18 mm. The final exported mesh volume was 19,535.313 mm3 with print-coordinate bounds 75.91 x 156.327 x 14.958 mm.

The fresh verifier must rerun all seven required checks on the new STL, including its independent printability calculation and visual review. Physical TPU coupon/device checks remain mandatory before a full case print.
