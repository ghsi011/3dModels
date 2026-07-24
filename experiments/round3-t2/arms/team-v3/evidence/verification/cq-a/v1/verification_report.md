---
contract: verification-report
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
revision: 1
owner: verifier
status: REJECT
candidate_id: cq-a
candidate_stl_sha256: f10cc046b6a6ff84063a265dcd1e2b2625c7617fa6f7eecc47e3bf864c0e96b4
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
fresh_context: true
updated_utc: 2026-07-24T01:35:24Z
---

# Independent verification

## Input/upstream audit
| Input/claim | Expected revision/hash/datum | Independent observation | Result | Evidence |
|---|---|---|---|---|
| Common fixture evidence | 63.00 cap; F02 = 62.00 x 11.70 x 24.00 mm centred at D0 | SVG numeric labels and r2 datum frame agree; no extra appliance geometry inferred. | PASS | `common/brief.md`, `common/evidence/fixture_views.svg`, `evidence/verification/cq-a/v1/svg_same_view_overlay.png` |
| Dimensions/reference binding | dimensions r2; reference hash `25fac0...303a` | Reference manifest binds a one-body F02 envelope with stated bounds. | PASS | `dimensions.md`, `evidence/reference/manifest.md` |
| Candidate export/identity | STL `f10cc...96b4`; STEP `cd1d...ebce` | Independently rehashed STL/STEP; STL re-imported as one watertight component, 28,390.083 mm3, bounds [-42,-24,0.600]..[42,8,64.998] mm. STEP imports as one valid solid, 84.0 x 32.0 x 64.4 mm. | PASS | `evidence/verification/cq-a/v1/metrics.json`, `evidence/verification/cq-a/v1/reimported.stl` |
| Required delivery set | Common brief requires fit-coupon STL from real engagement geometry | No coupon STL exists in the candidate delivery; `print_notes.md` explicitly says it was intentionally not exported. | REJECT | `print_notes.md`, candidate-root artifact inventory |

## Seven checks on re-imported exported STL
| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | Manifold boolean, exported STL against the authorised 62.00 x 11.70 x 24.00 mm F02 box at seated D0 coordinates | 0.000 mm3 intersection | No material enters the orange F02 envelope in the V1 section. | PASS | `evidence/verification/cq-a/v1/metrics.json`, `evidence/verification/cq-a/v1/reimport_section_y0.png` |
| 2 full insertion/travel sweep | Manifold boolean at 0.20-mm intervals over full -DZ approach: bar local shift -24.0..0.0 mm | 121 samples; maximum forbidden intersection 0.000 mm3 | The section retains the open -DZ approach and terminal +DZ roof. | PASS | `evidence/verification/cq-a/v1/metrics.json`, `evidence/verification/cq-a/v1/reimport_section_y0.png` |
| 3 section | Fresh y=0 section of re-imported STL; F02 and cap datum compared to r2/G-02/G-03 | Cavity XY 62.60 x 12.30 mm; X/Y clearance 0.300 mm per side; roof clearance 0.350 mm; lowest candidate Z 0.600 mm, cap clearance margin 0.100 mm above G-03 floor | Broad unkeyed end contacts, open approach, and protected cap plane are visible; no teeth seen. | PASS | `evidence/verification/cq-a/v1/reimport_section_y0.png`, `evidence/verification/cq-a/v1/metrics.json` |
| 4 same-view/photo overlay look | Re-imported cavity boundary at D0 mapped at the SVG governing 5 px/mm top-view scale; all four candidate renders also inspected | n/a | Red 62.60 x 12.30 mm cavity boundary uniformly surrounds the governing 62.00 x 11.70 mm bar by 0.30 mm/side; no mirror ambiguity for centred symmetric F02. Render views show a broad tray/end-stop arrangement, but do not establish the claimed printer-bed landmark. | PASS | `evidence/verification/cq-a/v1/svg_same_view_overlay.png`, `cq-a-exterior-isometric.png`, `cq-a-installed-engagement.png`, `cq-a-section.png`, `cq-a-print-orientation.png` |
| 5 named-datum feature positions/handedness | Exported-STL bounds/section and D0-centred F02 boolean; compare direct and X-mirrored frames | F02 direct placement centred at D0; X=-31..31, Y=-5.85..5.85, Z=0..24 is clear. Symmetric interface has no handed feature to mirror. | Section confirms both end-stop positions are symmetric about D2 and the roof is +DZ. | PASS | `evidence/verification/cq-a/v1/metrics.json`, `evidence/verification/cq-a/v1/reimport_section_y0.png` |
| 6 measurement-to-geometry audit | Re-imported STL dimensional/edge review: cavity and cap values above; endpoint/interior samples for E-01..E-07 against G-01/G-04/G-05/G-06 | Shell/engagement floors: base 1.85, roof 1.68, end walls 2.40 mm; E-01/E-02 R1.50, E-03/E-04 R0.80, E-05 0.80-mm lead-in, E-06 Z=0.600, E-07 0.30-mm chamfer at endpoint/interior samples | Exterior and section inspection show no teeth or exposed sharp engagement edge. | PASS | `evidence/verification/cq-a/v1/reimport_section_y0.png`, `evidence/verification/cq-a/v1/metrics.json` |
| 7 planned-orientation printability/faces | Apply exact Rx(+90) logic to re-imported face normals and extrema; evaluate G-06 and SS-01..SS-04 | Native min Y=-24.000 mm; declared P_BED Y=-8.000 mm is 16.000 mm above actual bed. The lowest non-P_BED grip face is 969.823 mm2; all non-P_BED transformed downface area is 1112.523 mm2. | The declared P_BED is not the lowest landing face; a hand-grip/show face reaches the bed. Thus G-06, SS-01 and SS-04 fail. SS-02 bridge/roof and SS-03 transition cannot cure this support-free-orientation failure. | REJECT | `evidence/verification/cq-a/v1/metrics.json`, `cq-a-print-orientation.png` |

## Defects
| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|
| V1-01 | CANDIDATE_BUILD | Check 7; G-06; SS-01; SS-04; P_BED | Exact transform requires P_BED at native Y=-8.000 to be the printer-bed landmark with no forbidden downward face. Re-imported STL reaches Y=-24.000 at a 969.823-mm2 grip face; P_BED is 16.000 mm above the actual bed and 1112.523 mm2 of non-P_BED downface remains. | `evidence/verification/cq-a/v1/metrics.json` | A newly exported candidate must satisfy the frozen transform: P_BED is the lowest intended contact and every SS required-now predicate passes on fresh re-import verification. |
| V1-02 | CANDIDATE_BUILD | Delivery completeness; common-brief fit coupon | Required: one fit-coupon STL generated from real bar-engagement geometry. Observed: no coupon STL delivered. | `print_notes.md`, candidate-root artifact inventory | Candidate delivery includes the required real-engagement coupon STL and binds it to the candidate parameters/export hash. |

## Verdict
REJECT to CANDIDATE_BUILD
