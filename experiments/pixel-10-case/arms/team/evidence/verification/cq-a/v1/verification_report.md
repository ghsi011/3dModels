---
contract: verification-report
contract_version: 1
job_id: pixel-10-case-team
revision: 1
owner: verifier
status: REJECT
candidate_id: cq-a
candidate_stl: pixel10_case_cq_a.stl
candidate_stl_sha256: 957d50cd7e6bcb2521044d4aaed5b7be3015fc62f7ceeff4dbe28f564cfdfe1f
dimensions_revision: 3
print_plan_revision: 1
reference_sha256: c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91
fresh_context: true
updated_utc: 2026-07-23T22:36:50Z
---

# Verification report

## Input integrity
| Input | Expected revision/hash | Observed | Result |
|---|---|---|---|
| dimensions.md | accepted r3 | r3, owner metrologist, status ACCEPTED | pass |
| print_plan.md | accepted r1 bound to r3/ref-2 | r1, owner print-engineer, status ACCEPTED | pass |
| ref-2 STL | `c1a250...7e68d91` | same SHA-256 in MANIFEST and runtime input | pass |
| candidate STL | `957d50...64cfdfe1f` | SHA-256 recomputed before re-import: same | pass |
| candidate export | one case body, STL and STEP listed | re-import: one watertight 2,836-triangle mesh; 32,050.895 mm3 | pass |

## Upstream dimensions audit against photos
| Feature/dim ID | Photo observation | Sheet statement | Result | Evidence |
|---|---|---|---|---|
| F-001/M-001--M-003 | Official diagram is the base Pixel 10 with a tall rounded handset body. | 152.8 x 72.0 x 8.6 mm from the named bottom, centre, rear datums. | pass | `../../../../../evidence/input/pixel10_official_hardware_diagram.png`; `../../dimensions.md` |
| F-003/M-005--M-009 | Rear diagram shows one wide capsule camera island near the top. | Centred bounded 60.5 x 22.0 mm island, top Y=138.8 mm, protrusion bounded 0.5--3.5 mm. | pass | `../../evidence/reference/ref-2/overlay_camera_ref2.png`; ref-2 acceptance |
| F-004/F-005/M-010--M-011/M-019--M-026 | Diagram shows three cameras left-to-right and flash on the rear-view +X/right end. | Three bounded camera datums and one +X flash datum, with handedness explicit. | pass | `../../evidence/reference/ref-2/metrologist_acceptance.md` |
| F-006/F-007/M-012--M-013 | Buttons are on the rear-view right side. | Continuous authorised right-side relief Y=42--122; no invented individual covers. | pass | official diagram; `../../dimensions.md` |
| F-008--F-010/M-014--M-016 | Bottom has a centred USB-C region plus acoustic features. | Broad centred opening and no bridge except protected corner returns. | pass | official diagram; `../../dimensions.md` |
| F-013/M-017 | Top microphone is present but not calibrated by the diagram. | Bounded centred 8 mm top relief and physical-device confirmation requirement. | pass | official diagram; `../../dimensions.md` |

## Print-plan audit
| Constraint ID | Candidate observation | Result | Evidence |
|---|---|---|---|
| P-001/P-011 | Re-imported section shows a continuous 1.2 mm screen-side plate rather than an open front bounded by a protective lip. | fail | `check-3-section-plan.png`; check 2 CSV |
| P-002 | One watertight polymer mesh; no second body or embedded geometry in the re-imported export. | pass | `reimport_metrics.json` |
| P-003/P-004 | Seat pose has 0.000 mm3 Boolean interference, but the actual screenward insertion travel is blocked by the continuous front plate. | fail | `reimport_metrics.json`; `check-2-insertion-sweep.csv` |
| P-005 | Shared rear opening is remeasured as 66.5 x 28.0 mm, centred X=0, top Y=142.3 mm. | pass | re-imported STL datum inspection; `check-4-datum-overlay.png` |
| P-006--P-008 | Re-imported boundary positions retain the +X Y=42--122 relief, 58 mm centred bottom opening, and 8 mm centred top relief. | pass | `check-4-datum-overlay.png` |
| P-009 | 19,461.866 mm2 of downward-facing area lies above the bed; its largest continuous band is 10,429.653 mm2 at printer Z=13.750 mm. | fail | `check-7-printability.txt` |
| P-010 | Bed-contact perimeter is at printer Z=0; the intended 0.3 mm edge treatment is not the rejection cause. | pass | `reimport_metrics.json`; re-imported mesh section |
| P-012 | The fatal closure and unsupported roof are CAD mesh geometry, not slicer-only detail. | fail | `check-3-section-plan.png`; `check-7-printability.txt` |

## Seven checks
| Check | Method on re-imported STL | Numeric result | Visual observation | Result | Evidence |
|---|---|---|---|---|---|
| 1 interference | Manifold Boolean of ref-2 and inverse-print-transformed candidate at seat. | 0.000 mm3; threshold <=0.001 mm3. | Seated rear, island, control and opening geometry do not intersect. | pass | `reimport_metrics.json` |
| 2 insertion | Manifold Boolean sweep of ref-2 from +18 to 0 mm screenward offset in 1 mm increments. | non-zero at offsets 13 through 1 mm; maximum 12,709.099 mm3 at +8/+7 mm. | The handset cannot traverse the screen-side closure to the seated pose. | fail | `check-2-insertion-sweep.csv` |
| 3 section | XY section at installed rear datum Z=0 from the re-imported meshes. | candidate installed Z range -10.150 to +4.800 mm; closed screen-side plane maps to printer Z=13.750 mm. | Section/mesh inspection demonstrates a continuous full-face closure where an open screen face and lip are required. | fail | `check-3-section-plan.png`; `check-7-printability.txt` |
| 4 look/overlay | Same-datum rear-plan overlay plus direct inspection of ref-2, candidate exterior, transparent fit, section, and official diagram. | n/a | Camera capsule/opening is at the rear top and the right relief is on +X; however the candidate exterior/section visibly reads as a closed tray/cover plate, not an installable open-front case. | fail | `check-4-datum-overlay.png`; `../../evidence/candidates/cq-a/exterior_isometric.png`; `../../evidence/candidates/cq-a/section_y_mid.png` |
| 5 positions | Re-imported STL boundary/section measurement from D1_XMID, D2_BOTTOM, D4_TOP; mirrored alternative inspected. | camera opening X=0.0, Y centre=128.3, 66.5 x 28.0, top Y=142.3; control +X Y=42--122; bottom 58 centred; top 8 centred. | Camera and controls retain declared handedness. The positions do not cure the closed-front defect. | pass | `check-4-datum-overlay.png`; `reimport_metrics.json` |
| 6 measurement audit | Every M-ID mapped to the re-imported mesh or its bounded opening/clearance response. | 26/26 mappings reviewed; M-001--M-004/M-018 cannot satisfy their intended installable-case response because of the closure. | No upstream dimension is missing, but the body-envelope response is nonfunctional. | fail | measurement table below |
| 7 printability/faces | Exported STL in its supplied print orientation: watertightness, bbox, face-normal and bridge-area audit. | watertight; bbox 75.900 x 156.317 x 14.950 mm; unsupported downward area 19,461.866 mm2. | The 10,429.653 mm2 screen-side roof violates zero supports and <=5 mm functional bridge limits. | fail | `check-7-printability.txt` |

## Feature-position register
| Feature ID | Datum | Expected | Observed | Delta | Handedness check | Result |
|---|---|---:|---:|---:|---|---|
| F-003 camera opening | D1_XMID/D4_TOP | shared, X=0; top >=141.8 | X=0; top 142.3; 66.5 x 28.0 | +0.5 mm versus minimum top extension | symmetric about D1 | pass |
| F-006/F-007 relief | D3_RIGHT/D2_BOTTOM | +X, Y=42--122 | +X, Y=42--122 | 0.0 mm | mirror would place this relief on -X | pass |
| F-009 bottom opening | D1_XMID/D2_BOTTOM | centred, >=18 mm | centred, 58.0 mm | +40.0 mm margin | symmetric about D1 | pass |
| F-013 top relief | D1_XMID/D4_TOP | centred, 8.0 mm | centred, 8.0 mm | 0.0 mm | symmetric about D1 | pass |

## Measurement audit
| Dimension ID | Geometry mapping | Result |
|---|---|---|
| M-001 | Y body/cavity response from D2_BOTTOM to D4_TOP; candidate outer extent 156.317 mm. | fail: full-face closure prevents use as a case |
| M-002 | X cavity envelope around 72.0 mm phone width. | fail: full-face closure prevents use as a case |
| M-003 | Z cavity response around 8.6 mm body depth. | fail: full-face closure prevents installation |
| M-004 | Rounded corner relief in re-imported perimeter. | fail: unusable before coupon test |
| M-005 | Shared opening 66.5 mm exceeds bounded island envelope plus clearance. | pass |
| M-006 | Shared opening 28.0 mm exceeds bounded island envelope plus clearance. | pass |
| M-007 | Opening centre on D1_XMID. | pass |
| M-008 | Opening top Y=142.3, 3.5 mm beyond nominal 138.8. | pass |
| M-009 | Opening/lip height accommodates the bounded island at seat. | pass |
| M-010 | One shared opening is compatible with three-camera layout. | pass |
| M-011 | One shared opening includes the +X flash region. | pass |
| M-012 | Continuous +X relief spans Y=42--122. | pass |
| M-013 | Relief is on D3_RIGHT/+X. | pass |
| M-014 | Bottom opening is centred on D1_XMID and 58.0 mm wide. | pass |
| M-015 | Bottom boundary is open at D2_BOTTOM. | pass |
| M-016 | Broad bottom opening has no central bridge. | pass |
| M-017 | Centred 8.0 mm top relief. | pass |
| M-018 | No second mesh or added magnetic body in back export. | pass |
| M-019 | A datum falls inside the shared opening. | pass |
| M-020 | Camera-A bounded diameter falls inside the shared opening. | pass |
| M-021 | B datum falls inside the shared opening. | pass |
| M-022 | Camera-B bounded diameter falls inside the shared opening. | pass |
| M-023 | C datum falls inside the shared opening. | pass |
| M-024 | Camera-C bounded diameter falls inside the shared opening. | pass |
| M-025 | +X flash datum falls inside the shared opening. | pass |
| M-026 | Flash bounded diameter falls inside the shared opening. | pass |

## Visual inspection narrative
- Reference/photo row: the official diagram and accepted ref-2 show a rounded phone with a rear-top camera capsule, three camera apertures, +X flash, and front screen that must remain exposed.
- Candidate row: the rear opening, right-control relief, and broad bottom/top relief appear in the correct datum locations, but the candidate/section shows a continuous screen-side sheet.
- Differences: that sheet closes the entire handset entry face. It creates both a rigid sweep obstruction and a large unsupported printer roof.
- Overlay observations: `check-4-datum-overlay.png` confirms the camera capsule/opening alignment rather than a mirror error; it also cannot redeem the missing open-front architecture. The overlay is visual evidence, not a nearest-edge score.

## Defects
| Defect ID | Owning contract | Feature/check IDs | Concrete defect | Required acceptance condition |
|---|---|---|---|---|
| CQ-A-V1-001 | CANDIDATE_GEOMETRY | F-001; P-001/P-003/P-009/P-011/P-012; checks 2, 3, 4, 6, 7 | The re-imported export has a continuous screen-side closure. It blocks the rigid full entry sweep by up to 12,709.099 mm3 and produces a 10,429.653 mm2 unsupported roof in a zero-support plan. | Candidate designer must provide a new exported STL whose re-imported geometry has an open screen face with only the bounded protective lip, passes the full documented sweep, and has no unsupported functional roof; a fresh verifier must rerun all seven checks. |

## Verdict
- Result: REJECT.
- Passed candidate ranking, if comparing candidates: none.
- Rerun scope: CANDIDATE_BUILD for cq-a or a replacement candidate, then a fresh independent verification run of all seven checks on the new exported STL.
- Verifier commission: cq-a-v1.
