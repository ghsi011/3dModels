---
contract: job-state
contract_version: 2
job_id: pixel-10-base-case-v2
revision: 10
owner: orchestrator
mode: PIPELINE
profile: COMPACT
state: DELIVERY
active_candidate: none
backend: cadquery
updated_utc: 2026-07-24T00:39:25Z
---

# Job state

Delivery status: **DELIVERED** (the v2 schema state remains `DELIVERY`).

## Route
PIPELINE / COMPACT: a fit-critical, photo-evidenced, protective TPU phone case requires named datums, a blind reference round trip, print planning, and independent verification. CadQuery only by commission constraint.

## Bound inputs
| Contract/evidence | Revision/hash | Status |
|---|---|---|
| `../../../benchmark_brief.md` | frozen common input | bound |
| `../../../evidence/input/README.md` | frozen common evidence index | bound |
| `../../../evidence/input/pixel10_official_hardware_diagram.png` | `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0` | bound |
| `../preregistration.md` | frozen round-2 input | bound |
| `../../../../skills/3d-modeling/references/team-contracts-v2.md` | v2 | bound |

## Gates
| Gate | Required receipt | Result | Evidence |
|---|---|---|---|
| metrology | dimensions with complete blind-build table | PASS | `dimensions.md` SHA-256 `9f9e0dfc6600534c8562e7f3f94b1697b37d2fa9d14d88e4e41307e94741d82b` |
| reference build | blind CadQuery reference + source/overlay | PASS | `reference_phone.stl` SHA-256 `81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48`; one decisive rear overlay |
| reference acceptance | metrologist overlay acceptance | PASS | `reference_acceptance.md`: ACCEPTED envelope-only |
| print plan | exact transform and coupon lane plan | PASS | `print_plan.md` rev4; transformed support restrictions are P2-owned after verification |
| readiness | hash-bound READY on re-imported STL | PASS | D2R5 READY against plan rev4 and exported hash bound |
| independent verification | fresh seven-check report | PASS | `verification_report.md` rev5: V5 fresh seven-check PASS |
| print prep | one coupon and field-test plan | PASS | P2 one joined TPU coupon plus `print_notes.md`; physical printing honestly pending |
| delivery | terminal contracts and inventory | PASS | run log reconciled; no commit made by orchestrator |

## Dispatches
| ID | Role/commission | Authorized inputs | Required output | Budget min | Status |
|---|---|---|---|---:|---|
| M1 | metrologist / dimensions | benchmark brief; frozen common evidence; v2 contract | dimensions.md | 5 | RECEIVED |
| D1 | designer / blind reference build | dimensions v1; benchmark brief; official evidence | reference source/STL/renders | 5 | RECEIVED |
| M2 | metrologist / reference overlay acceptance | dimensions v1; reference build; official evidence | dimensions acceptance + overlay receipt | 5 | RECEIVED (ACCEPTED) |
| P1 | print engineer / pre-design plan | dimensions v2; accepted reference; benchmark | print_plan.md | 5 | RECEIVED |
| D2 | designer / candidate cq-v2 through self-check | dimensions v2; accepted reference; print plan v1 | source/STL/STEP/renders/readiness | 10 | RECEIVED READY |
| V1 | verifier / fresh seven checks | all contracts; candidate exports/renders | verification_report.md + evidence | 10 | RECEIVED REJECT |
| D2R1-D2R5 | designer / correction-scoped readiness loops | verifier defects and plan revisions | changed source/STL/renders/readiness | 10 each | RECEIVED; final READY rev4 |
| V2-V4 | fresh verifier / rejected loops | changed exports and bound plans | reports/evidence | 10 each | RECEIVED REJECT; defects routed correctly |
| P1R-P1R3 | print engineer / G04-G05 and ordering corrections | plan defects/evidence | print plans rev2-rev4 | 5 each | RECEIVED |
| V5 | fresh verifier / final seven checks | final rev4 candidate and contracts | verification_report.md rev5 | 10 | RECEIVED PASS |
| P2 | print engineer / final prep | plan rev4; V5 PASS; candidate | coupon/source/manifest/notes | 10 | RECEIVED |

## Open user questions
| ID | Question | Blocks |
|---|---|---|
| none | none | none |
