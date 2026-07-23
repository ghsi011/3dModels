---
contract: job-state
contract_version: 1
job_id: pixel-10-case-team
revision: 16
owner: orchestrator
mode: PIPELINE
state: DELIVERED
backend: CADQUERY
active_commission: none
freecad_owner: none
dimensions_revision: 3
print_plan_revision: 1
candidate_id: cq-a-r3
verification_revision: 3
updated_utc: 2026-07-23T23:04:24Z
---

# Job state

## Routing
- Fit-critical: yes; this TPU case must install around and clear the exact Pixel 10 body, controls, camera field, ports, and microphones.
- Multi-part: no; one-piece case around a non-printed mating object.
- Explicit team request: yes; frozen benchmark commission requires the five-role pipeline.
- Decision: PIPELINE by fit-critical rule (also explicit team request).

## User requirements
- Function: slim, protective one-piece TPU 95A case for the base Google Pixel 10.
- Loads and directions: repeated elastic installation/removal; drops/corner impacts; side-button actuation; charging load at USB-C; rear wireless charging through the back.
- Environment: ordinary consumer use; thermal exposure not further specified.
- Printer: Bambu Lab X2D Combo, 0.4 mm main nozzle.
- Filaments: TPU 95A final; coupon material to be set by print engineer.
- Visible/cosmetic faces: all exterior faces; no decorative text; preserve screen and camera lips.
- Text/colors: single-color TPU; no text.
- Project folder: experiments/pixel-10-case/arms/team/.
- Print Queue page: unavailable in this benchmark runtime; no connected Notion authority.

## Gate ledger
| Gate | Required revision/hash | Result | Evidence |
|---|---|---|---|
| Intake/backend | CadQuery 2.8.0 | PASS | runtime import recorded in run_log.md |
| Dimensions | dimensions r1 | PASS | evidence/metrology/meta-1_evidence.md |
| Reference build | dimensions r1 | PASS | reference.py; evidence/reference/reference_manifest.json |
| Reference overlay r1 | reference STL sha256 d53245f5d18951a9e6988a338e321c86669e703501bf6bd35248c6f6c9797d77 | REJECT: upstream dimensions | evidence/reference/metrologist_acceptance.md |
| Dimensions correction | dimensions r3 | PASS | dimensions.md; evidence/metrology/meta-3_camera_datums.md |
| Reference build r2 | dimensions r3 | PASS | evidence/reference/ref-2/MANIFEST.md |
| Reference overlay r2 | reference STL sha256 c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91 | PASS | dimensions.md r3; evidence/reference/ref-2/metrologist_acceptance.md |
| Candidate build | candidate STL sha256 957d50cd7e6bcb2521044d4aaed5b7be3015fc62f7ceeff4dbe28f564cfdfe1f | PASS | evidence/candidates/cq-a/designer_handoff.md |
| Fresh verification cq-a-v1 | verification report r1 | REJECT: CANDIDATE_GEOMETRY CQ-A-V1-001 | verification_report.md |
| Candidate correction | candidate STL sha256 0baa59672955e4f01a51df1f4a4c122b8b62d13839510e2bfe515da13d8a9d86 | PASS | evidence/candidates/cq-a-r2/designer_handoff.md |
| Fresh verification cq-a-r2-v1 | verification report r2 | REJECT: CANDIDATE_GEOMETRY CQ-A-R2-V1-001 | verification_report.md |
| Candidate orientation correction | candidate STL sha256 71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44 | PASS | evidence/candidates/cq-a-r3/designer_handoff.md |
| Fresh verification cq-a-r3-v1 | verification report r3 | PASS | verification_report.md; evidence/verification/cq-a-r3/v1/ |
| Print plan | print plan r1 | PASS | print_plan.md |
| Independent verification | verification report r3 | PASS | verification_report.md |
| Final print prep | six TPU coupon STLs and final notes | PASS | fit_coupon_manifest.md; print_notes.md |
| Delivery audit | final STL SHA-256 71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44 | PASS | run_log.md final artifact/hash audit |

## Open user questions
| ID | Blocking state | Question | Answer/status |
|---|---|---|---|
| Q-01 | none | Which base-Pixel-10 production sub-variant and exact camera-bar dimensions apply? | Bounded from official evidence/public research; must remain explicit in dimensions.md and coupon plan. |

## Dispatch ledger
| Commission | Role | Authorized inputs | Required output | Status |
|---|---|---|---|---|
| meta-1 | metrologist | benchmark brief; common evidence/input; role references | dimensions.md and metrology evidence | complete |
| ref-1 | designer REFERENCE | dimensions.md r1; selected CadQuery/FDM role references only | reference.py, reference exports/renders | complete |
| meta-2 | metrologist reference acceptance | dimensions.md r1; input diagram; reference artifacts/renders | revised dimensions.md and overlay evidence | complete: REVISE_SHEET |
| meta-3 | metrologist correction | dimensions.md r2; input diagram; r1 acceptance finding | dimensions.md r3 plus evidence | complete |
| ref-2 | designer REFERENCE | dimensions.md r3; selected CadQuery/FDM role references only | reference source, exports/renders for ref-2 | complete |
| meta-4 | metrologist reference acceptance | dimensions.md r3; input diagram; ref-2 artifacts/renders | accepted/revised dimensions.md and overlay evidence | complete: ACCEPTED |
| plan-1 | print engineer pre-design | job_state.md r7; dimensions.md r3; accepted ref-2 | print_plan.md r1 | complete: ACCEPTED |
| cq-a | designer CANDIDATE | dimensions.md r3; accepted ref-2; print_plan.md r1 | model.py, verify.py, STL, STEP, renders, designer notes | complete: CANDIDATE_READY |
| cq-a-v1 | fresh verifier | photos; dimensions r3; plan r1; accepted ref-2; cq-a exported artifacts | verification_report.md | complete: REJECT CQ-A-V1-001 |
| cq-a-r2 | designer CANDIDATE correction | dimensions r3; ref-2; plan r1; verification_report.md r1 | corrected model/exports/renders and designer handoff | complete: CANDIDATE_READY |
| cq-a-r2-v1 | fresh verifier | photos; dimensions r3; plan r1; accepted ref-2; cq-a-r2 exported artifacts | verification_report.md r2 | complete: REJECT CQ-A-R2-V1-001 |
| cq-a-r3 | designer CANDIDATE correction | dimensions r3; ref-2; plan r1; verification_report.md r2 | supplied-print-orientation corrected artifacts and handoff | complete: CANDIDATE_READY |
| cq-a-r3-v1 | fresh verifier | photos; dimensions r3; plan r1; accepted ref-2; cq-a-r3 exported artifacts | verification_report.md r3 | complete: PASS |
| prep-1 | print engineer post-pass | verification_report.md r3; final exported artifacts; print_plan.md r1 | finalized print_notes.md; actual coupon; slicing/order/field test | complete |
