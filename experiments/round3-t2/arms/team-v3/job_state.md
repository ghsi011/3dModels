---
contract: job-state
contract_version: 3
job_id: round3-t2-team-v3
revision: 14
owner: orchestrator
mode: PIPELINE
profile: COMPACT
state: DELIVERY
backend: cadquery
active_candidate: cq-a
updated_utc: 2026-07-24T02:19:29Z
---

# Job state

## Route
PIPELINE / COMPACT: the one-piece tool has a fit-critical mating interface reconstructed from participant-facing schematic evidence; independent verification is mandatory.

## Bound inputs
| Contract/evidence | Revision/hash | Status |
|---|---|---|
| common/brief.md | sha256 e82b8a49c74797732abb795587ff57c4e29d6c647c832e944b0084d3c269ac26 | bound |
| common/evidence/fixture_views.svg | sha256 495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c | bound |
| common/common_manifest.json | input manifest | bound |
| team-contracts-v3.md | common manifest blob 588f23f2d9d3865368f6b8b47773198052a9c14b | bound |

## Gates
| Gate | Required receipt | Result | Evidence |
|---|---|---|---|
| M1 | dimensions.md r1 | pass | sha256 b57372a2b5e7204797d8a4afe744f3c3949a689bd443cfb8909dea4ae21f3286 |
| D1 | blind reference artifacts | pass | evidence/reference/manifest.md; reference STL sha256 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a |
| M2 | dimensions.md accepted round trip | pass | dimensions r2 sha256 c4a191705373c129b928dfbdd88b86db29455895a7e0bcadecb6fc85044b1510; overlay 50c092bbaaa526945ae30b501048c584d1f60dd8ef72c910702473c4d95f6d88 |
| P1 | print_plan.md r1 | pass | sha256 6adce7277f4348db86add4c06e918b7e8b390af821822b6e05840d6c8171dfe2 |
| D2 | candidate readiness READY | pass | corrected candidate STL sha256 b2b13f8a953a7e11d00d0d503f830715843f2e8463da9c173099188e505059ca |
| V4 | verification_report PASS | pass | verification report r4 sha256 18c6a90899de64f8fd1051d643827c03e09b8956e226c4ee2e92cadc34e47a3b |
| P2 | coupon, print notes, final_print_prep COMPLETE | pass | final_print_prep COMPLETE sha256 161823cd1cd68203c262b0e7c73af87c22cf68ee632c675051539a9317f399c0 |
| DELIVERY | all receipts | pass | candidate PASS; P2 COMPLETE; physical coupon remains mandatory first-print gate |

## Dispatches
| ID | Role/commission | Authorized inputs | Required output | Budget min | Status |
|---|---|---|---|---:|---|
| M1 | metrologist / initial sheet | common brief + SVG only | dimensions.md r1 | 6 | complete |
| D1 | designer / blind reference | dimensions.md r1 only | evidence/reference/* | 7 | complete |
| M2 | metrologist / reference acceptance | SVG + dimensions r1 + reference artifacts | dimensions.md accepted | 5 | complete |
| P1 | print engineer / pre-design | accepted sheet + reference artifacts + brief | print_plan.md | 6 | complete |
| D2 | designer / candidate cq-a | dimensions r2 + reference + print plan r1 + V2 report | corrected design artifacts + readiness | 12 | complete / corrected |
| V1 | verifier / candidate cq-a | all bound contracts + candidate artifacts | verification_report.md | 10 | complete / REJECT |
| V2 | verifier / candidate cq-a | all bound contracts + corrected candidate artifacts | verification_report.md | 10 | complete / REJECT |
| V3 | verifier / candidate cq-a | all bound contracts + corrected candidate artifacts | verification_report.md | 10 | complete / REJECT |
| V4 | verifier / candidate cq-a | all bound contracts + final audited candidate artifacts | verification_report.md | 10 | dispatched / fresh final |
| P2 | print engineer / final prep | V4 PASS + final exports + notes + plan | coupon + final_print_prep | 7 | dispatched / resumed context |
| P2 | print engineer / final prep | V1 PASS + exports + notes | coupon + final prep | 7 | queued |

## Open user questions
| ID | Question | Blocks |
|---|---|---|
| Q-001 | Notion Print Queue access is outside the participant-visible common package and no connected queue is authorized. | none; record omission |
