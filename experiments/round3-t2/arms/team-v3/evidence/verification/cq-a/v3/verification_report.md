---
contract: verification-report
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
revision: 3
owner: verifier
status: REJECT
candidate_id: cq-a
candidate_stl_sha256: bafb6b7e19a35c602ae105e3c79338db92c0e5a91cc7f2ce4563d8d1e4e0d112
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
fresh_context: true
updated_utc: 2026-07-24T03:00:00Z
---

# Independent verification

## Input/upstream audit
| Input/claim | Expected revision/hash/datum | Independent observation | Result | Evidence |
|---|---|---|---|---|
| Common fixture evidence | E1/E2/E3; F02 `62.00 x 11.70 x 24.00` mm centred on D0 | The brief, SVG labels and manifest agree with dimensions r2; no unsupported appliance geometry is used. | PASS | `common/brief.md`, `common/evidence/fixture_views.svg`, `common/common_manifest.json`, `dimensions.md` |
| Dimensions, reference, plan | dimensions r2; reference `25fac0...303a`; plan r1 | D0/DX/DY/DZ, `0.300` mm XY and `0.350` mm top clearance, `0.600` mm cap clearance, Rx(+90°), G-01..G-07 and SS-01..SS-04 are internally consistent. | PASS | `dimensions.md`, `print_plan.md`, `evidence/reference/manifest.md` |
| Candidate export identity | STL `bafb6b...d112`; STEP supplied | Fresh SHA-256 matches readiness. Fresh re-import is one watertight component, Euler 2, bounds `[-42,-8,0.600]..[42,8,64.994]` mm. | PASS | `evidence/verification/cq-a/v3/metrics.json`, `evidence/verification/cq-a/v3/reimported.stl`, `cq-a-washer-filter-tool.step` |
| V2-01 regression target | G-05 / E-02 `R>=1.50` at both endpoints and interior | Fresh E-02 edge-section samples are `1.500`, `1.5995..1.6001`, and `1.500` mm; all meet the floor. | PASS | `evidence/verification/cq-a/v3/metrics.json` |
| Coupon disposition | P2 production-geometry PETG coupon follows candidate PASS | This remains a downstream P2 gate and is not a candidate failure. Candidate REJECT means P2 must not proceed yet. | PASS (downstream gate) | `print_plan.md`, `print_notes.md` |

## Seven checks on re-imported exported STL
| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | Fresh re-imported STL dense F02 interior lattice | `0 / 77,175` F02 samples in candidate material | No candidate wall enters the nominal bar envelope. | PASS | `evidence/verification/cq-a/v3/metrics.json` |
| 2 full insertion/travel sweep | Fresh re-imported STL F02 lattice at `0.20` mm steps, `-24.00..0.00` DZ approach | `121` steps; `0` material hits at every step | The section has an open `-DZ` mouth with a `+DZ` roof stop. | PASS | `evidence/verification/cq-a/v3/metrics.json`, `evidence/verification/cq-a/v3/reimport_section_y0.png` |
| 3 section | Fresh DY=0 re-imported-STL section against F02/F01/G-02/G-03 | cavity `62.60 x 12.30 x 24.35` mm; XY clearance `0.300`/side; top `0.350`; cap `0.600` | Broad end stops, lateral mouth, and protected cap plane are visible. | PASS | `evidence/verification/cq-a/v3/reimport_section_y0.png` |
| 4 same-view/photo overlay look | Fresh D0 same-scale SVG overlay; inspected it and all four supplied candidate renders | n/a | The overlay shows centred uniform XY clearance. Exterior render also reveals the unrounded outer grip rim, consistent with check 6. | PASS | `evidence/verification/cq-a/v3/svg_same_view_overlay.svg`, `evidence/verification/cq-a/v3/svg_same_view_overlay.png`, `cq-a-exterior-isometric.png`, `cq-a-installed-engagement.png`, `cq-a-section.png`, `cq-a-print-orientation.png` |
| 5 named-datum feature positions/handedness | Re-imported F02 lattice/section and direct/mirrored frame review | centred F02: X=`-31..31`, Y=`-5.85..5.85`, Z=`0..24`; symmetric interface has no handed feature | End stops are symmetric about D2; roof is +DZ. | PASS | `evidence/verification/cq-a/v3/metrics.json`, `evidence/verification/cq-a/v3/reimport_section_y0.png` |
| 6 measurement-to-geometry audit | Re-imported bounds/sections and every declared E-01..E-07 endpoint/interior requirement; paired-face dihedral sampling | E-02 regression passes. E-01 exposed outer grip rim at DY=`+8.000` has `126` sampled `89.975..89.997°` junctions: R~0, not `>=1.50` mm. | Exterior/section views establish this is a user-touch outer rim, not P_BED or a permitted contact class. | REJECT | `evidence/verification/cq-a/v3/metrics.json`, `cq-a-exterior-isometric.png`, `evidence/verification/cq-a/v3/reimport_section_y0.png` |
| 7 planned-orientation printability/faces | Exact Rx(+90°) re-imported normal/extrema audit; repeat G-06, SS-01..SS-04 | native P_BED Y=`-8.000`; P_BED area `4342.624` mm2; non-P_BED downface `0.000` mm2; bridge `0.000` mm; transition excess `0.000` mm2; supports `0.000` mm3/0 contacts | The inspected orientation render agrees: P_BED alone is down, and mouth remains lateral. | PASS | `evidence/verification/cq-a/v3/metrics.json`, `cq-a-print-orientation.png` |

## Defects
| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|
| V3-01 | CANDIDATE_BUILD | Check 6; G-05; E-01 | Required: every hand-contact exterior edge `R>=1.50` mm. Observed: the exposed grip outer face rim at DY=`+8.000` is a re-imported STL `89.975..89.997°` sharp junction (R~0). | `evidence/verification/cq-a/v3/metrics.json`, `cq-a-exterior-isometric.png` | A new candidate STL must make every E-01 endpoint/interior sample meet G-05, retain V3's E-02 pass, and receive a fresh verifier's full seven-check rerun. |

## Verdict
REJECT to CANDIDATE_BUILD
