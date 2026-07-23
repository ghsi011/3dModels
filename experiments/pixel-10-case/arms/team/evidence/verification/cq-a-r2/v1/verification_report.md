---
contract: verification-report
contract_version: 1
job_id: pixel-10-case-team
revision: 2
owner: verifier
status: REJECT
candidate_id: cq-a-r2
candidate_stl: pixel10_case_cq_a.stl
candidate_stl_sha256: 0baa59672955e4f01a51df1f4a4c122b8b62d13839510e2bfe515da13d8a9d86
dimensions_revision: 3
print_plan_revision: 1
reference_sha256: c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91
fresh_context: true
updated_utc: 2026-07-23T22:46:55Z
---

# Verification report

## Input integrity
| Input | Expected revision/hash | Observed | Result |
|---|---|---|---|
| dimensions.md | accepted r3 | r3, metrologist-owned, ACCEPTED | pass |
| print_plan.md | accepted r1 bound to r3/ref-2 | r1, print-engineer-owned, ACCEPTED | pass |
| ref-2 STL | `c1a250...7e68d91` | SHA-256 recomputed: same | pass |
| candidate STL | `0baa596...3d8a9d86` | SHA-256 recomputed before re-import: same | pass |
| candidate export | one printable case body | one watertight, winding-consistent component; 2,804 triangles; 19,535.313 mm3 | pass |

## Upstream dimensions audit against photos
| Feature/dim ID | Photo observation | Sheet statement | Result | Evidence |
|---|---|---|---|---|
| F-001/M-001--M-003 | Official diagram shows the tall rounded base Pixel 10 body. | 152.8 x 72.0 x 8.6 mm from D2_BOTTOM/D1_XMID/D0_REAR. | pass | `../../../../../evidence/input/pixel10_official_hardware_diagram.png`; `../../dimensions.md` |
| F-003/M-005--M-009 | Rear is a broad top capsule. | Centred bounded 60.5 x 22.0 mm island with C-grade uncertainty and oversized-opening response. | pass | `../../reference/ref-2/overlay_camera_ref2.png`; ref-2 acceptance |
| F-004/F-005/M-010--M-011/M-019--M-026 | Three cameras span the island; flash is at rear-view +X/right. | Three camera and +X flash datums, each explicitly bounded. | pass | `../../reference/ref-2/metrologist_acceptance.md` |
| F-006--F-010/M-012--M-016 | Right controls and bottom port/acoustic region are visible but uncalibrated. | Continuous +X relief and broad open bottom are the authorised bounded response. | pass | official diagram; `../../dimensions.md` |
| F-013/M-017 | Top microphone exists but lacks calibrated location. | Temporary centred 8 mm relief and physical-device blocker. | pass | official diagram; `../../dimensions.md` |

## Print-plan audit
| Constraint ID | Candidate observation | Result | Evidence |
|---|---|---|---|
| P-001/P-002/P-011 | Re-imported sections show 1.6 mm nominal side response, a single thin charging back, and open screen face/lip architecture. | pass | `check-3-4-same-datum-sections.png`; candidate renders |
| P-003/P-004 | Seated Boolean is zero and the full screenward insertion path is open; compliant corner response remains coupon-gated. | pass | `reimport_metrics.json`; `check-2-insertion-sweep.csv` |
| P-005--P-008 | Shared camera opening is 66.492 x 28.000 mm, top Y=142.300; +X control relief, broad bottom opening, and centred top relief are retained. | pass | `check-3-4-same-datum-sections.png`; re-imported section audit |
| P-009 | 9,032.212 mm2 of downward-facing area is above the bed at Z=3.05--3.25 mm. | fail | `check-7-printability.txt` |
| P-010 | Required exterior rear-back bed face is not at the bed; the central rear panel is material only from Z=3.2--4.4 mm. | fail | `check-7-printability.txt` |
| P-012 | This unsupported roof follows the exported CAD geometry, not a slicer setting. | fail | `check-7-printability.txt`; `reimport_metrics.json` |

## Seven checks
| Check | Method on re-imported STL | Numeric result | Visual observation | Result | Evidence |
|---|---|---|---|---|---|
| 1 interference | Manifold Boolean between inverse-print-transformed case and ref-2 at seat. | 0.000 mm3; threshold <=0.001 mm3. | Rear, island, side and opening geometry do not intersect at seat. | pass | `reimport_metrics.json` |
| 2 insertion | Manifold sweep of ref-2 from -18 to 0 mm screenward in 1 mm steps; negative Z is the documented screen/open-front direction. | 19/19 steps 0.000 mm3; maximum 0.000 mm3. | The corrected screen face is open through full travel. | pass | `check-2-insertion-sweep.csv`; `reimport_metrics.json` |
| 3 section | Same-datum XY sections at installed Z=0 and Z=2. | Two rings at each plane; camera opening encloses the ref-2 island. | Screen face is open; section also exposes the broad back panel separated from the printer bed after supplied orientation. | fail | `check-3-4-same-datum-sections.png`; `check-7-printability.txt` |
| 4 look/overlay | Opened official diagram, accepted ref-2/photo overlay, candidate open-screen/transparent/section/orientation renders, and verifier same-datum overlay. | n/a | Rear-top capsule, three-camera/+X-flash architecture, open screen face, camera opening and right-hand relief visually agree; no mirror error. The raw full-diagram overlay has a 4.79/9.94 mm trend only because it contains two handsets and callout art, so it is not used as a decision scalar. | pass | `check-4-photo-overlay.png`; `check-3-4-same-datum-sections.png`; `../../candidates/cq-a-r2/exterior_isometric_open_screen.png`; `../../reference/ref-2/overlay_camera_ref2.png` |
| 5 positions | Re-imported model-frame sections with explicit plane transform, compared from D1_XMID/D2_BOTTOM/D4_TOP; mirror alternative inspected. | Camera opening X=-0.000, width 66.492, height 28.000, top Y=142.300; top relief X=-4..+4, Y=150.3..155.3; +X relief handedness retained. | Shared opening covers the accepted three-camera/+X-flash datum envelope; mirror would put control relief on -X. | pass | `check-3-4-same-datum-sections.png`; `reimport_metrics.json` |
| 6 measurement audit | All M-001 through M-026 mapped to exported body, bounded openings, or required coupon response. | 26/26 mapped. | No measured input is omitted; physical-device/coupon bounds remain explicitly unresolved final-print gates. | pass | measurement table below |
| 7 printability/faces | Re-imported STL in supplied printer orientation: watertightness, components, bbox, face normals, bed relation and central vertical probe. | watertight; one component; bbox 75.900 x 156.317 x 14.950 mm; unsupported downward area 9,032.212 mm2. | The rear panel is a large unsupported roof, not the stipulated bed-contact face. | fail | `check-7-printability.txt`; `reimport_metrics.json` |

## Feature-position register
| Feature ID | Datum | Expected | Observed | Delta | Handedness check | Result |
|---|---|---:|---:|---:|---|---|
| F-003 camera opening | D1_XMID/D4_TOP | X=0; top >=141.8; oversized shared opening | X=-0.000; top=142.300; 66.492 x 28.000 | +0.500 mm top margin | symmetric about D1 | pass |
| F-006/F-007 relief | D3_RIGHT/D2_BOTTOM | +X; Y=42--122 | +X opening from the bounded control band | 0.0 within section tolerance | mirror would move it to -X | pass |
| F-009 bottom opening | D1_XMID/D2_BOTTOM | centred; >=18 mm | broad centred opening retained | >=40 mm nominal margin | symmetric about D1 | pass |
| F-013 top relief | D1_XMID/D4_TOP | centred; 8 mm | X=-4..+4 at top edge | 0.0 | symmetric about D1 | pass |

## Measurement audit
| Dimension ID | Geometry mapping | Result |
|---|---|---|
| M-001--M-004 | 152.8 x 72.0 x 8.6 body envelope and compliant rounded cavity/corner response. | pass; coupon remains required |
| M-005--M-009 | 66.492 x 28.000 shared centred camera opening, top Y=142.300, raised rim. | pass |
| M-010--M-011 | Shared opening covers all three-camera and +X-flash bounds. | pass |
| M-012--M-013 | Continuous +X control relief. | pass |
| M-014--M-016 | Broad centred open lower edge with protected returns. | pass |
| M-017 | Centred 8 mm top relief. | pass |
| M-018 | Single TPU mesh; no magnetic/secondary body; thin rear wall response. | pass |
| M-019--M-026 | All three camera and flash bounded datums fall inside shared opening. | pass |

## Visual inspection narrative
- Reference/photo row: official diagram and accepted ref-2 show a rounded handset, rear-top capsule, three cameras and +X flash, with the front screen exposed.
- Candidate row: r2 visibly removes the r1 screen closure, retains a shared camera capsule opening, continuous right-side control relief, broad bottom opening, and top relief.
- Differences: case material is intentionally larger than the reference by wall/clearance allowance; no camera/layout mirror was observed.
- Overlay observations: the accepted ref-2 overlay visibly hugs the official camera silhouette; verifier same-datum sections show the candidate opening surrounding that fixture. The full official-diagram candidate overlay is visually unsuitable for scalar acceptance because its source includes two handset drawings and annotation lines.

## Defects
| Defect ID | Owning contract | Feature/check IDs | Concrete defect | Required acceptance condition |
|---|---|---|---|---|
| CQ-A-R2-V1-001 | CANDIDATE_GEOMETRY | P-009/P-010/P-012; checks 3 and 7 | In the supplied print orientation, the re-imported case's broad rear panel is a 9,032.212 mm2 downward-facing roof at Z=3.05--3.25 mm instead of the required bed-contact exterior rear-back face. It violates the zero-support plan. | Candidate designer must re-export a case whose re-imported supplied printer orientation puts the exterior rear-back face on Z=0 and has no unsupported functional roof; fresh verification must rerun all seven checks. |

## Verdict
- Result: REJECT.
- Passed candidate ranking, if comparing candidates: none.
- Rerun scope: CANDIDATE_BUILD for cq-a-r2 or a replacement candidate, then a fresh verifier reruns every check on the new exported STL.
- Verifier commission: cq-a-r2-v1.
