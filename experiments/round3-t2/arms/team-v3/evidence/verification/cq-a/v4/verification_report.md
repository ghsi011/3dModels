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
| Common fixture evidence | E1/E2/E3; F02 `62.00 x 11.70 x 24.00` at D0 | Brief, SVG, manifest, dimensions r2 and blind reference agree; no unprovided appliance geometry used. | PASS | `common/brief.md`, `common/evidence/fixture_views.svg`, `common/common_manifest.json`, `dimensions.md`, `evidence/reference/manifest.md` |
| Candidate export identity | STL `39b305...889df`; STEP supplied | Fresh hash matches. Re-import is one watertight component, Euler 2, bounds `[-42,-8,0.600]..[42,8,64.994118]` mm. | PASS | `metrics.json`, `reimported.stl`, `cq-a-washer-filter-tool.step` |
| Plan predicates | r1: Rx(+90°), G-01..G-07, SS-01..SS-04 | Dimensions, datums, clearance ranges, transform and frozen candidate predicates are consistent. | PASS | `dimensions.md`, `print_plan.md` |
| V3 regression | E-01 `R>=1.50` at endpoint/interior sectors | Fresh top/right/bottom re-import samples are `1.594322..1.601218`, `1.594323..1.602598`, and `1.594323..1.601218` mm. | PASS | `metrics.json` |
| Coupon disposition | P2 production-geometry PETG coupon follows candidate PASS | Downstream gate only. | PASS (downstream gate) | `print_plan.md`, `print_notes.md` |

## Seven checks on re-imported exported STL
| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | Fresh F02 interior lattice | `0` material hits; XY clearance `0.300`/side; top `0.350` mm | No wall enters F02. | PASS | `metrics.json` |
| 2 full insertion/travel sweep | Fresh F02 lattice, 121 positions at `0.20` mm | `0` collisions | Open `-DZ` mouth and `+DZ` roof stop visible. | PASS | `metrics.json`, `reimport_section_y0.png`, `cq-a-installed-engagement.png` |
| 3 section | Fresh re-imported DY=0 section | cavity `62.60 x 12.30 x 24.35` mm; cap `0.600` mm | Lateral channel, end stops, roof and cap clearance visible. | PASS | `reimport_section_y0.png` |
| 4 same-view/photo overlay look | Fresh D0 same-scale SVG overlay; all final renders inspected | n/a | F02 is uniformly inside the cavity; repaired rounded grip rim, lateral mouth and orientation agree. | PASS | `svg_same_view_overlay.svg`, `svg_same_view_overlay.png`, `cq-a-exterior-isometric.png`, `cq-a-installed-engagement.png`, `cq-a-section.png`, `cq-a-print-orientation.png` |
| 5 named-datum feature positions/handedness | Re-imported F02 lattice/section; direct/mirrored review | centred X=`-31..31`, Y=`-5.85..5.85`, Z=`0..24` | Symmetric D2 stops, +DZ roof, -DZ opening. | PASS | `metrics.json`, `reimport_section_y0.png` |
| 6 measurement-to-geometry audit | Re-imported sections/triangle rings; all E-01..E-07 endpoint/interior rows | E-01 `1.594..1.603`; E-02 `1.800/1.600/1.800`; E-03/E-04 `0.900`; E-05 `0.900` 45°; E-06 `0.600`; E-07 `0.300` mm | Every exposed/function/bed boundary passes; G-01 floor `>=1.68` mm independent of infill. | PASS | `metrics.json`, `reimport_section_y0.png`, `cq-a-exterior-isometric.png` |
| 7 planned-orientation printability/faces | Exact transform normal/extrema/section audit; every SS predicate repeated | P_BED Y=`-8.000`, area `4341.602`; non-P_BED downface `0`; bridge `0`; transition excess `0`; supports `0` mm3/`0` contacts | P_BED alone down; mouth remains lateral. SS-01..SS-04 each pass. | PASS | `metrics.json`, `reimport_print_orientation.png`, `cq-a-print-orientation.png` |

## Defects
| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|
| none | n/a | n/a | No candidate-phase defect observed. | `metrics.json` | n/a |

## Verdict
PASS. Candidate verification is complete. P2 PETG production-geometry coupon and native-slicer final-prep receipts remain downstream gates.
