---
contract: final-print-prep
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
owner: print-engineer
status: COMPLETE
candidate_stl_sha256: 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df
print_plan_revision: 1
verification_report_revision: 4
updated_utc: 2026-07-24T05:45:00Z
---

# Final print preparation

| Required P2 item | Plan rule/final gate | Observed artifact/hash | Result |
|---|---|---|---|
| Coupon source/export and pass/fail lanes | Coupon; `PRINT_PREP` | `coupon.py`; `cq-a-real-bar-engagement-coupon.stl` SHA-256 `2a08ab48731ad4e1a305cf06d4d45d736c0f1c22fd2f8519a58ed1a7805b0f84`; re-import: watertight `true`, 1 component, bounds `[-33.700,-8.000,0.600]..[33.700,13.500,31.850]` mm, volume `8921.792 mm3`; source prints nominal span `62.00 mm`, retained depth `24.00 mm`, cavity `62.60 x 12.30 x 24.35 mm`. | COMPLETE; the physical PETG coupon remains the mandatory first print and must pass before final-tool slicing. |
| Slicer/profile or reproducible settings | G-07; SS-04 / `PRINT_PREP` | X2D single-nozzle, dry PETG main 0.4 mm nozzle, textured PEI, X2D Generic PETG profile, 0.20 mm layer, 0.42 mm line, 4 walls, 5 top/bottom layers, 35% gyroid, brim OFF, seam on `P_BED`/nonfunctional base. | COMPLETE |
| Underside support-contact view, when required | SS-01, SS-04 | Not required: support-free plan r1, verification r4 check 7 PASS, zero prohibited downfaces/supports and only `P_BED` bed-facing. | N/A |
| Section/toolpath view per support interval, when required | SS-02, SS-03 | Not required: zero support intervals; re-imported candidate audit reports bridge `0.000 mm` and transition excess `0.000 mm2`. | N/A |
| Layer/contact map per support footprint, when required | SS-01..SS-04 | Not required: zero out-of-limit footprint and no `SUPPORT_ALLOWED` region exists. | N/A |
| Transform/profile/nozzle/material match | Process, G-06, SS-01..SS-04 | Exact `Rx(+90.0 deg)` about `D0`; translate only so `P_BED`, native `Y=-8.000 mm`, is printer `Z=0.000 mm`; `+DY -> +printer Z`, `+DZ -> -printer Y`; PETG main 0.4 mm, 0.20 mm/0.42 mm process; supports OFF, `0.000 mm3`. | COMPLETE |
| Print order, inspection, and field-test protocol | Coupon; G-02/G-03/G-05/G-07 / `PRINT_PREP` | `print_notes.md` P2 transfer: PETG coupon first; real-bar seat/±10 deg/no-damage/>=0.50 mm cap-clearance gate; final-file hash check; inspection; gentle bidirectional field test; stop/route procedure. | COMPLETE |

No deferred visual slicer predicate remains.  This is a support-free plan with zero out-of-limit regions, so a native project and `final_prep_review.md` are not required.  `COMPLETE` records manufacturing-preparation completion only; the documented real-bar PETG coupon pass is still the physical authorization gate for the final-tool print.
