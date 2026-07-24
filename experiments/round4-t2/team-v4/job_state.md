---
contract: job-state
contract_version: 4
job_id: round4-t2-team-v4
revision: 5
owner: orchestrator
mode: PIPELINE
profile: COMPACT
state: CANDIDATE_BUILD
backend: cadquery
active_candidate: none
updated_utc: 2026-07-24T02:57:50Z
---

# Job state

## Route

PIPELINE / COMPACT: a fitted, photo/schematic-reconstructed bar interface needs named-datum accuracy, a blind reference round trip, PETG DFM, and one fresh independent verification. CadQuery is mandatory; FreeCAD is prohibited.

## Bound inputs

| Contract/evidence | Revision/hash | Status |
|---|---|---|
| common brief | SHA-256 e82b8a49c74797732abb795587ff57c4e29d6c647c832e944b0084d3c269ac26 | bound |
| fixture schematic | SHA-256 495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c | bound |
| common manifest | SHA-256 ed4659f5c3cd6401f98c7cfd8fb27189c649c4d679968b494d3e754cef3b77ce | bound |
| requested `common_manifest.md` | path absent; participant-facing `common_manifest.json` supplied by leader | transparent path mismatch |

## Gates

| Gate | Required receipt | Result | Evidence |
|---|---|---|---|
| M1 | complete dimensions and inventory | PASS | dimensions.md SHA-256 d84627a873ee4eb24d7fc151e645368b3c374d11bef58320773dcc0d8555329c |
| D1/M2 | blind reference and overlay acceptance | PASS | accepted dimensions r2 SHA-256 1e233ca7c2041c7a6583c62b910ef39fee4cfefd3868db14fedb26e6208783c6 |
| P1 | accepted plan and machine projection | PASS | plan SHA-256 1a54f2bcdffe3b0689501b1cd757d5aa33deac19ec7fedd035f54794ddb4bd9e; checks SHA-256 ad6b910db21664f5a5e7f81f78500b33da7ef062a8925dc8080dfdb6182e5f53 |
| D2 | complete candidate preflight | pending | candidate readiness/JSON |
| O1 | independent receipt validation | pending | orchestrator_validation.json |
| V1 | fresh seven-check verification | pending | verification_report.md |
| P2 | PETG preparation | pending | final_print_prep.md |

## Dispatches

| ID | Role/commission | Authorized inputs | Required output | Budget min | Status |
|---|---|---|---|---:|---|
| M1 | metrologist | common package only | dimensions.md, evidence inventory | 3 | complete |
| D1 | designer, blind reference | dimensions r1 only | reference CAD/export/renders | 4 | complete |
| M2 | metrologist, same context | dimensions + reference + fixture | dimensions acceptance/overlay | 3 | complete |
| P1 | print engineer | accepted dimensions/reference | plan + machine projection | 4 | complete |
| D2 | designer, candidate | dimensions r2/reference/plan r1 | candidate + complete preflight | 9 | dispatched |
| V1 | verifier, fresh | contracts + canonical output in place | seven-check report + own audit JSON | 8 | queued |
| P2 | print engineer, reuse P1 context | bound candidate/plan/V1 | final PETG preparation | 5 | queued |

## Open user questions

| ID | Question | Blocks |
|---|---|---|
| none | none | none |
