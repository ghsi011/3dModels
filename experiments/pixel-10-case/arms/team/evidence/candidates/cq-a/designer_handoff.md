# cq-a designer handoff

Status: `CANDIDATE_READY` for independent verification only; this document makes no acceptance finding.

## Bound inputs

- `dimensions.md` revision 3, accepted.
- `print_plan.md` revision 1, accepted.
- Accepted reference fixture: `evidence/reference/ref-2/pixel10_reference_ref2.stl`, SHA-256 `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91`.

## Candidate artifacts

- `../../../../model.py`: parametric CadQuery case source. `ref_part` loads only the accepted fixture and is never exported.
- `../../../../verify.py`: designer self-check only, explicitly non-authoritative.
- `../../../../pixel10_case_cq_a.stl`: final case export in print-plan orientation.
- `../../../../pixel10_case_cq_a.step`: final case export in print-plan orientation.
- `exterior_isometric.png`: exterior evidence.
- `transparent_fit.png`: case versus accepted ref-2 fixture.
- `section_y_mid.png`: longitudinal half-section evidence; `section_y_mid.stl` is its source mesh.
- `print_orientation_multiview.png`: bed-facing rear-back orientation evidence.

## Reproducible designer self-check

```powershell
python experiments/pixel-10-case/arms/team/model.py
python experiments/pixel-10-case/arms/team/verify.py
python skills/3d-modeling/scripts/run_cadquery_model.py experiments/pixel-10-case/arms/team/model.py --preview --strict
```

Observed after final export: CadQuery case valid; exported STL watertight; 2,836 triangles; print-coordinate bounds `75.91 x 156.327 x 14.958 mm`; mesh volume `32050.895 mm3`.

## Contract-facing geometry

- `CAVITY_CLEARANCE_MM = 0.35` mm per side, with the named 0.25/0.35/0.45 mm coupon variants retained in source/notes.
- 1.6 mm functional side/corner walls; 1.4 mm charging-region back wall; 1.2 mm screen/camera lip walls.
- Shared 66.5 x 28.0 mm camera opening with top Y=142.3 mm and a 4.8 mm camera-lip top.
- Continuous right-side relief Y=42--122 mm, 58 mm broad bottom opening, and 8 mm centred top relief.
- No supports or non-case bodies are designed/exported.

## Verification scope remaining

Independent verifier must perform all seven Phase-4 checks on the re-imported STL, including full insertion sweep, datum remeasurement, and plan-orientation printability audit. The physical TPU coupon/real-device checks remain required before a full case print.
