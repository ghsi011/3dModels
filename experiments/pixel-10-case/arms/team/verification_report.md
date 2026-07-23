---
contract: verification-report
contract_version: 1
job_id: pixel-10-case-team
revision: 3
owner: verifier
status: PASS
candidate_id: cq-a-r3
candidate_stl: pixel10_case_cq_a.stl
candidate_stl_sha256: 71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44
dimensions_revision: 3
print_plan_revision: 1
reference_sha256: c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91
fresh_context: true
updated_utc: 2026-07-24T12:55:00Z
---

# Verification report

## Input integrity
| Input | Expected revision/hash | Observed | Result |
|---|---|---|---|
| job state | FRESH_VERIFICATION; commission cq-a-r3-v1 | r13, active commission matches | pass |
| dimensions.md | accepted r3 | r3, metrologist-owned, ACCEPTED | pass |
| print_plan.md | accepted r1 bound to r3/ref-2 | r1, print-engineer-owned, ACCEPTED | pass |
| ref-2 STL | `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91` | SHA-256 recomputed: same | pass |
| candidate STL | `71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44` | SHA-256 recomputed before STL re-import: same | pass |
| candidate export | one printable case body | one watertight, winding-consistent component; 2,300 triangles; 18,921.621 mm3 | pass |

## Upstream dimensions audit against photos
| Feature/dim ID | Photo observation | Sheet statement | Result | Evidence |
|---|---|---|---|---|
| F-001/F-002; M-001--M-004 | Official diagram shows the tall rounded base Pixel 10 body. | 152.8 x 72.0 x 8.6 mm from D2_BOTTOM/D1_XMID/D0_REAR, with bounded 7--13 mm corner response. | pass | `../../../../../evidence/input/pixel10_official_hardware_diagram.png`; `../../dimensions.md` |
| F-003; M-005--M-009 | Rear is a broad top capsule. | Centred bounded 60.5 x 22.0 mm island, with a shared oversized candidate opening. | pass | `../../reference/ref-2/overlay_camera_ref2.png`; ref-2 acceptance |
| F-004/F-005; M-010--M-011/M-019--M-026 | Three cameras run left-to-right and flash is rear-view +X/right. | Three camera and one +X flash datums, all bounded and explicitly handed. | pass | official diagram; `../../reference/ref-2/metrologist_acceptance.md` |
| F-006--F-010; M-012--M-016 | Right controls and lower port/acoustic region are visible but uncalibrated. | Continuous +X relief and broad open lower edge are the authorised bounded response. | pass | official diagram; `../../dimensions.md` |
| F-013; M-017 | Top microphone is present but uncalibrated. | Temporary centred 8 mm relief and physical-device confirmation requirement. | pass | official diagram; `../../dimensions.md` |

## Print-plan audit
| Constraint ID | Candidate observation | Result | Evidence |
|---|---|---|---|
| P-001/P-002/P-011 | Re-imported sections/ray probes show 1.6 mm side/lip response, one body, 1.4 mm central rear wall, and an open screen face. | pass | `check-1-2-7-metrics.json`; r3 section/render evidence |
| P-003/P-004 | Seat Boolean and every documented screenward sweep step are 0.000000000 mm3. Corner remains correctly coupon-gated. | pass | `check-1-2-7-metrics.json`; `check-2-insertion-sweep.csv` |
| P-005--P-008 | Re-imported datum rings show 66.492 x 28.000 shared camera opening/top 142.300, +X control relief, 58 mm lower opening, and 8 mm top relief. | pass | `check-5-feature-positions.md` |
| P-009/P-010 | In supplied printer orientation, Z minimum is 0.000; downward area above Z=0.3 is 0.000 mm2. The exterior rear back is bed-facing and the re-imported multiview shows no roof. | pass | `check-1-2-7-metrics.json`; `check-7-candidate-printer-multiview.png` |
| P-012 | Openings, face placement, cavity and bed orientation are in the exported mesh; no slicer-only repair claimed. | pass | re-imported STL checks 1--7 |

## Seven checks
| Check | Method on re-imported STL | Numeric result | Visual observation | Result | Evidence |
|---|---|---|---|---|---|
| 1 interference | Exact inverse of supplied printer transform, then manifold Boolean with accepted ref-2 at seat; threshold <=0.001 mm3. | 0.000000000 mm3 | Fixture fits in cavity without material intersection. | pass | `check-1-2-7-metrics.json` |
| 2 insertion | Manifold Boolean at every 1 mm screenward offset from -18 through 0 mm, including relief/camera transition travel. | 19/19 steps are 0.000000000 mm3; maximum 0.000000000 mm3. | Open screen face, right relief and camera region remain clear. | pass | `check-2-insertion-sweep.csv` |
| 3 section | Re-imported installed-coordinate XY ring audit plus r3 longitudinal section inspected. | central rear-wall ray intersections: Z=0.350 and 1.750 (1.400 mm); open-front cavity. | Section visibly has an open screen face, shared camera opening and no closed roof. | pass | `check-5-feature-positions.md`; `../../candidates/cq-a-r3/section_y_mid.png` |
| 4 look/overlay | Opened official diagram, accepted cropped ref-2 photo overlay, ref-2 technical views, r3 candidate exterior/transparent/section/orientation renders, and this re-imported printer multiview. | n/a | Silhouette, rear-top capsule, three-camera/+X-flash architecture, open screen face, openings, and handedness agree; no mirror found. | pass | `visual_inspection.md`; `../../reference/ref-2/overlay_camera_ref2.png`; `../../candidates/cq-a-r3/transparent_fit.png` |
| 5 positions | Explicit-plane-transform section rings from re-imported STL; direct versus mirrored handedness inspected. | camera 66.492 x 28.000, X=-0.000, top Y=142.300; lower opening 58.000; top relief 8.000. | +X control/flash location matches official rear view; mirror would fail. | pass | `check-5-feature-positions.md` |
| 6 measurement audit | Each M-001--M-026 mapped to a re-imported response, bounded opening, or required real-device coupon gate. | 26/26 mapped. | No input dimension/feature omitted; C-grade device-specific items remain explicitly coupon/physical-unit gates. | pass | measurement table below |
| 7 printability/faces | Supplied printer-oriented re-import: watertightness/components/bounds, face-normal audit, bed relation, section/ray wall audit. | watertight; one component; 75.900 x 156.317 x 11.900 mm; unsupported downward area above Z=0.3 = 0.000 mm2. | Rear back is bed-facing; cavity/lips grow support-free; no functional roof. | pass | `reimport_integrity.json`; `check-1-2-7-metrics.json`; `check-7-candidate-printer-multiview.png` |

## Feature-position register
| Feature ID | Datum | Expected | Observed | Delta | Handedness check | Result |
|---|---|---:|---:|---:|---|---|
| F-003 camera opening | D1_XMID/D4_TOP | X=0; top >=141.8; oversized shared opening | X=-0.000; top=142.300; 66.492 x 28.000 | +0.500 mm top margin | symmetric about D1 | pass |
| F-004/F-005 apertures | D1_XMID/D4_TOP | all bounded camera/flash datums inside shared opening; flash +X | all four bounded positions are inside opening | n/a | flash remains +X | pass |
| F-006/F-007 relief | D3_RIGHT/D2_BOTTOM | +X; Y=42--122 | +X continuous gap through Y=42--122 | 0.0 within section tolerance | mirror moves it to -X | pass |
| F-009 lower opening | D1_XMID/D2_BOTTOM | centred; >=18 mm | centred 58.000 mm | +40.000 mm margin | symmetric about D1 | pass |
| F-013 top relief | D1_XMID/D4_TOP | centred 8 mm | X=-4..+4 at upper edge | 0.0 | symmetric about D1 | pass |

## Measurement audit
| Dimension ID | Geometry mapping | Result |
|---|---|---|
| M-001--M-004 | Re-imported case envelope/cavity has 0.35 mm controlled clearance, rounded corner response and an explicitly required TPU coupon. | pass |
| M-005--M-009 | Re-imported shared camera opening is 66.492 x 28.000, centred, top Y=142.300, with protected rear response. | pass |
| M-010--M-011 | One shared opening covers the three-camera and +X-flash layout. | pass |
| M-012--M-013 | Re-imported +X continuous control relief spans the authorised Y=42--122 band. | pass |
| M-014--M-016 | Re-imported centred 58.000 mm lower opening is open at D2_BOTTOM with corner returns only. | pass |
| M-017 | Re-imported centred 8.000 mm top relief. | pass |
| M-018 | Single watertight mesh; 1.400 mm rear wall ray result; no extra magnetic/secondary body. | pass |
| M-019--M-026 | Every bounded camera and flash datum falls inside the re-imported oversized shared opening. | pass |

## Visual inspection narrative
- Reference/photo row: official diagram and accepted ref-2 show the rounded handset, rear-top capsule, three cameras and rear-view +X flash, with screen exposed.
- Candidate row: r3 visibly has an open screen tray, shared camera opening, continuous right-side relief, broad lower opening and centred top relief.
- Differences: candidate material is larger by permitted wall/clearance; its shared opening intentionally exceeds the C-grade individual-aperture estimates.
- Overlay observations: accepted ref-2 cropped camera overlay visibly matches the official camera silhouette; r3 transparent-fit and same-datum re-imported measurements place the candidate opening around that fixture. No mirror alternative matches the +X controls/flash.

## Defects
| Defect ID | Owning contract | Feature/check IDs | Concrete defect | Required acceptance condition |
|---|---|---|---|---|
| none | n/a | n/a | n/a | n/a |

## Verdict
- Result: PASS
- Passed candidate ranking, if comparing candidates: cq-a-r3 is the only candidate in this commission.
- Rerun scope: all seven checks after any upstream contract, fixture, source, or exported-STL byte change; TPU coupon and physical-device gates remain mandatory before final print.
- Verifier commission: cq-a-r3-v1
