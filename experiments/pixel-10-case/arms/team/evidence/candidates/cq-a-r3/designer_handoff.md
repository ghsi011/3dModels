# cq-a-r3 export-orientation correction handoff

Status: `CANDIDATE_READY` for fresh independent verification only. This document makes no acceptance claim.

## Bound inputs

- Accepted `dimensions.md` r3.
- Accepted `print_plan.md` r1.
- Accepted ref-2 fixture SHA-256: `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91`.
- Rejection input: `verification_report.md` r2, defect `CQ-A-R2-V1-001`.

## Correction

`REAR_BACK_Z_MM` is the rear external surface at 1.75 mm from the installed rear datum. The camera-opening rim is now coplanar with that exterior rear-back face, so the existing 180-degree X rotation places the rear-back face at supplied printer Z=0. The open screen face, 0.35 mm cavity clearance, shared 66.5 x 28.0 mm camera opening, +X Y=42--122 relief, broad bottom opening, and centred 8 mm top relief are unchanged.

## Regenerated artifacts

- `../../../../model.py`, `../../../../verify.py`
- `../../../../pixel10_case_cq_a.stl`, `../../../../pixel10_case_cq_a.step`
- `exterior_isometric.png`
- `print_orientation_multiview.png`
- `section_y_mid.png` and `section_y_mid.stl`
- `transparent_fit.png`

## Designer self-check evidence

The CadQuery strict runner completed successfully. Re-imported final STL: watertight, 2,300 triangles, 18,921.621 mm3 volume, and printer bounds 75.91 x 156.327 x 11.909 mm with Z minimum 0.000 mm. The non-authoritative exported-mesh calculation reports 0.000 mm2 of downward-facing area above Z=0.3 mm.

The independent verifier must rerun all seven checks on the new export. TPU coupon and real-device confirmation remain required before a final full case print.
