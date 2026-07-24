---
contract: print-plan
contract_version: 4
job_id: round4-t2-team-v4
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 2
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
updated_utc: 2026-07-24T02:56:46.5340827Z
---

# Print plan

## Process
| Printer/material/nozzle | Layer | Environment/load | Rationale |
|---|---:|---|---|
| Bambu Lab X2D Combo; dry, plain PETG; main direct-drive hardened 0.4 mm nozzle; single nozzle | 0.20 mm nominal; 0.42 mm line width | Hand-operated bar-engaging tool. Torque, duty cycle, and load rating are unknown: no load-capacity claim. | PETG is the required final material and has tougher, more compliant behavior than PLA. The main nozzle is selected for the functional/visible surface; a second nozzle, AMS change, and support interface are not required. The support-free side-land orientation keeps the open engagement mouth lateral and preserves all mating/hand faces from plate or support contact. |

## Model-to-printer transform
| Item | Exact value |
|---|---|
| Coordinate convention | CadQuery model coordinates are the accepted installed frame in mm: `X=D1` (bar long axis), `Y=D2` (bar short axis), `Z=D3` (cap normal); homogeneous points are column vectors `[X,Y,Z,1]^T`. Designer shall make the named exterior `P_BED` plane exactly `Y=-16.000 mm`; no candidate point may have `Y<-16.000 mm`. |
| Transform/rotation | Apply `T_printer_from_installed = [[1,0,0,0],[0,0,-1,0],[0,1,0,16.000],[0,0,0,1]]` to each CadQuery point. This is `Rx(+90.000 deg)` about D0 followed by `Tz(+16.000 mm)`: `printer_X=X`, `printer_Y=-Z`, `printer_Z=Y+16.000`. No mirroring, scale, additional rotation/tilt, or translation is permitted. |
| Bed-contact landmark | `P_BED`: a deliberately planar, nonfunctional exterior side land on `Y=-16.000 mm`, outward normal `-Y`, at least `20.00 x 10.00 mm` (>=`200.00 mm2`) after STL re-import. It is not an appliance-contact, bar-contact, lead-in, grip, or show surface. It is the sole bed-contact class. |
| Bed normal | `+printer_Z=+installed_Y`; the plate-facing outward normal is `-printer_Z=-installed_Y`. `P_BED` is at printer `Z=0.000 mm` under the stated matrix. |
| Open/insertion direction | The installed mouth remains open and tool insertion remains `-installed_Z`; after the transform this is `+printer_Y`, horizontal and parallel to the plate. It must never be blocked by a printer-down (`-printer_Z`) roof. |
| Forbidden downward faces | `F01` cap-face keep-out; every appliance-contact surface around `F02/F04`; every bar-engagement bearing face; all mouth/lead-in faces; all hand-grip/show faces; all functional clearance faces. Only `P_BED` may touch the plate. Slicer supports and support-contact faces are forbidden everywhere. |

## Geometry rules and phase scope
| ID | Rule | Numeric limit | Verification predicate | required_now | deferred_owner | final_gate |
|---|---|---:|---|---|---|---|
| G-01 | PETG shell, engagement wall, grip-root and torque-path minimum thickness | >=`1.20 mm` (3 x `0.42 mm` lines) | Re-imported STL thickness samples at every shell, bar-engagement wall, grip root, and rib are >=`1.20 mm`; geometry does not rely on infill for this floor. | Candidate-readiness thickness map and parameter mapping; fresh verifier repeats on exported STL. | none | none |
| G-02 | Full F02 cavity clearance from named D0/D1/D2/D3 datums | `X` clearance >=`0.50 mm` per end; `Y` clearance >=`0.30 mm` per side; seated-top `Z` clearance >=`0.60 mm`; no negative clearance | Sections and datum measurements prove a channel enclosing `62.00 x 11.70 x 24.00 mm` plus these allowances, centre-aligned to D1/D2; interference and full `-Z` insertion sweep have zero collision. | Candidate parameter map, re-imported-STL datum table, interference and sweep. Fresh verifier repeats checks 1, 2, 5, and 6. | none | none |
| G-03 | Appliance/cap protection outside the authorized bar | >=`0.60 mm` normal clearance to D0 outside F02; zero candidate contact outside F02 | Re-imported STL installed-coordinate section and full insertion sweep report the clearance and zero collision with F01/F04. | Candidate section/sweep; fresh verifier repeats checks 1–3. | none | none |
| G-04 | Broad, smooth, non-keyed bar capture and lead-in | bar-contact/lead-in radius >=`0.80 mm`; lead-in chamfer >=`0.50 mm` at <=45 deg; 0 teeth, points, or contact protrusions <`1.20 mm` | Re-imported STL sections enumerate bar-contact boundaries and show that no feature keys unknown F03/F04 geometry. | Candidate edge table and section; verifier repeats visual/section inspection. | none | none |
| G-05 | Exposed-edge and comfort set `E-01`…`E-05` | Exact IDs, classes, radii and allowed-sharp condition are frozen in the next table and in `print_plan_checks.json`. | Exact ID-set equality; each non-sharp edge is sampled at two endpoints plus one interior location on the re-imported STL. | Candidate readiness JSON/Markdown edge audit; verifier independently repeats applicable edge sections. | none | none |
| G-06 | Plate-interface tolerance | `P_BED` perimeter has a `0.30 mm x 45 deg` chamfer; no functional geometry is within `0.50 mm` of printer Z=0 except the nonfunctional `P_BED` land/chamfer | Exact-transform re-imported sections prove the landmark plane, chamfer, and offset. | Candidate planned-orientation face audit; verifier check 7. | none | none |
| G-07 | Final structural slicing floor | >=4 perimeters (>=`1.68 mm` nominal), >=5 top/bottom layers, `30–40%` gyroid infill | P2 native profile records all floors; geometry has already passed G-01 without slicer-only reinforcement. | Candidate source/sections prove G-01 independently; verifier confirms no geometry rule relies on slicer reinforcement. | print-engineer: `final_print_prep.md` profile receipt | PRINT_PREP |
| S-01 | `SELF_SUPPORT_REQUIRED`: transformed non-bed downward faces | `0.000 mm2` out-of-limit area; no non-bed face with normal `printer_Z <= -0.70710679` | `team_preflight.py support-audit` on the re-imported STL with the exact matrix returns zero out-of-limit faces/area; visual render identifies `P_BED` as sole plate face. | Candidate runs `support-audit` for S-01, supports OFF, and records exact JSON; verifier check 7 independently repeats. | none | none |
| S-02 | `SELF_SUPPORT_REQUIRED`: every roof and bridge, including bar-cavity ceiling, handle opening, relief, and transition roof | each free bridge <=`5.00 mm`; `0.00 mm` functional droop allowance | Exact-orientation section/layer map lists every roof/bridge and span; no functional mating, cap-clearance, grip, or lead-in face is a bridge underside. | Candidate bridge map plus S-02 audit JSON; verifier repeats sections/check 7. | none | none |
| S-03 | `SELF_SUPPORT_REQUIRED`: layer-transition features, including steps, cavity transitions, chamfers, fillets, ribs, and protrusions | outward step <=`0.20 mm` per `0.20 mm` layer (>=45 deg from horizontal); `0.000 mm2` horizontal unsupported-step area | Exact-transform sliced-layer/mesh map lists all transition regions/layer intervals and reports none outside the limit. | Candidate layer-transition map plus S-03 audit JSON; verifier repeats check 7. | none | none |
| S-04 | `SELF_SUPPORT_REQUIRED`: zero-support policy | `0.00 mm3` generated support; 0 interface layers; 0 support-contact faces; supports OFF | Re-imported exact-transform audit is compliant and native-slicer preview at P2 will show supports disabled/zero volume. | Candidate records supports OFF and S-04 audit JSON; verifier check 7 confirms no support exception. | print-engineer: `final_print_prep.md` native preview/settings after verifier PASS | PRINT_PREP |

## Edge ID set
| ID | Boundary / exposure class | Re-imported-STL requirement and samples | JSON projection |
|---|---|---|---|
| E-01 | Hand-grip exterior perimeter — `EXPOSED_COMFORT` | radius >=`1.50 mm`; samples at both endpoints plus one interior point. | `min_radius_mm: 1.50`, 3 samples |
| E-02 | Grip-to-body and exterior handle-root transitions — `EXPOSED_FUNCTIONAL` | radius >=`0.80 mm`; samples at every distinct root boundary, with at least three samples per boundary. | `min_radius_mm: 0.80`, 3 samples |
| E-03 | Exterior mouth rim and lead-in outer boundary — `EXPOSED_FUNCTIONAL` | radius >=`0.80 mm`; samples at both mouth ends and midspan. The inner bar-contact/lead-in edge also satisfies G-04. | `min_radius_mm: 0.80`, 3 samples |
| E-04 | Bar-engagement bearing/clearance boundaries — `EXPOSED_FUNCTIONAL` | radius >=`0.80 mm`; samples at both ends and midspan; no sharp/keyed feature is allowed. | `min_radius_mm: 0.80`, 3 samples |
| E-05 | `P_BED` chamfer boundaries — `BED_CONTACT` | Deliberately sharp after the required `0.30 mm x 45 deg` chamfer is allowed only because it is nonfunctional, plate-facing, and separated >=`0.50 mm` from all functional geometry; section must prove that condition. | `allowed_sharp: true`; reason and 3 sample locations required |

## Coupon
| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|
| One support-free, one-piece engagement coupon generated from the **same named production bar-cavity, mouth lead-in, bearing-radius, wall, and clearance parameters**. It retains the complete `62.00 mm` F02 X span, the exact production Y width/clearance, and >=`20.00 mm` of production Z engagement depth with a rigid hand tab. It is not a nominal peg/hole surrogate. | One production lane only: the exact final G-02 end/side/top clearance values. A clearance ladder may be exploratory only and cannot substitute for this actual-geometry coupon. | Intended final dry PETG spool, X2D main 0.4 mm nozzle, `0.20 mm` / `0.42 mm` profile, exact transform, supports OFF. PLA may be an additional exploratory test only and cannot pass this PETG gate. | Before final-tool slicing: coupon inserts on the real bar through full available `-Z` travel to its designed seating datum with hand force; rotates at least `+10 deg` and `-10 deg` about D3 without lift-off, cracking, whitening, gouging, or cap contact outside F02. Record selected cavity X/Y/Z, safely measured actual bar X/Y/Z, seating depth, cap-face clearance (>=`0.60 mm`), and photos after both rotations. Any failure blocks final printing and routes to PRINT_PLAN/candidate fit parameters. |

## Final-prep placeholders
P2 is allowed only after a PASS verifier report bound to this plan/candidate hash and a passing real-bar PETG coupon. It will record the native X2D PETG profile and version; dry-filament and main-nozzle offset/flow-calibration receipt; the exact matrix and P_BED landmark; supports OFF/`0.00 mm3`; 0.20 mm layers, 0.42 mm line width, >=4 walls, >=5 top/bottom, 30–40% gyroid; brim decision from preview; seam placement away from E-01/E-03/E-04 and all mating faces; and an exported sliced-file hash. Print order is calibration/dryness check, PETG coupon, fit inspection, then one final tool. Final inspection measures G-02/G-03 clearances, P_BED/chamfer, all edge evidence, visual surface quality, and zero support scars. Field test is low-force engagement followed by `+10/-10 deg` hand turns, then gradual hand torque only; stop on slip, cracking, whitening, bar/cap gouging, or unexpected interference. Do not claim a torque rating; retain photos/settings/measurements and route any failure to metrology, candidate geometry, material/slicing, or machine as evidence indicates.
