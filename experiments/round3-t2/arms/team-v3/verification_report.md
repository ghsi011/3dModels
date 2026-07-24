---
contract: verification-report
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
revision: 4
owner: verifier
status: PASS
candidate_id: cq-a
candidate_stl_sha256: 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
fresh_context: true
updated_utc: 2026-07-24T05:18:00Z
---

# Independent verification

## Input/upstream audit
| Input/claim | Expected revision/hash/datum | Independent observation | Result | Evidence |
|---|---|---|---|---|
| V4 full receipt | dimensions r2, plan r1, STL `39b305...889df` | All bound input, hash, re-import and regression checks pass. | PASS | `evidence/verification/cq-a/v4/verification_report.md` |
| Coupon disposition | P2 after candidate PASS | Still downstream only. | PASS (downstream gate) | `print_plan.md`, `print_notes.md` |

## Seven checks on re-imported exported STL
| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | V4 F02 lattice | `0` hits | Clear envelope. | PASS | `evidence/verification/cq-a/v4/metrics.json` |
| 2 full insertion/travel sweep | V4 121-step sweep | `0` collisions | Open -DZ mouth. | PASS | `evidence/verification/cq-a/v4/metrics.json` |
| 3 section | V4 re-import section | stated clearances pass | Architecture visible. | PASS | `evidence/verification/cq-a/v4/reimport_section_y0.png` |
| 4 same-view/photo overlay look | V4 SVG/render inspection | n/a | Centred and rounded. | PASS | `evidence/verification/cq-a/v4/svg_same_view_overlay.svg` |
| 5 named-datum feature positions/handedness | V4 datum audit | centred symmetric F02 | Correct frame. | PASS | `evidence/verification/cq-a/v4/metrics.json` |
| 6 measurement-to-geometry audit | V4 E-01..E-07 audit | all floors pass | No sharp exposed rim. | PASS | `evidence/verification/cq-a/v4/metrics.json` |
| 7 planned-orientation printability/faces | V4 SS-01..SS-04 audit | zero prohibited downfaces/supports | P_BED alone down. | PASS | `evidence/verification/cq-a/v4/metrics.json` |

## Defects
| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|
| none | n/a | n/a | No candidate-phase defect observed. | `evidence/verification/cq-a/v4/verification_report.md` | n/a |

## Verdict
PASS. P2 PETG coupon and native-slicer final-prep evidence remain downstream gates.
