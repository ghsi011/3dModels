---
contract: print-plan
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 2
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
updated_utc: 2026-07-24T01:25:00Z
---

# Print plan

## Process
| Printer/material/nozzle | Layer | Environment/load | Rationale |
|---|---:|---|---|
| Bambu Lab X2D Combo / dry PETG, main 0.4 mm nozzle, single-nozzle | 0.20 mm; 0.42 mm nominal line width | Hand-operated washer filter-cap bar; torque and duty are unspecified; no load-capacity claim | PETG is the specified final material.  Single nozzle retains the 256 x 256 x 260 mm envelope and places the visible/functional PETG surface on the direct-drive main nozzle.  The chosen transform makes the engagement mouth lateral and permits a support-free build. |

## Model-to-printer transform
| Item | Exact value |
|---|---|
| Transform/rotation | Candidate coordinates use the accepted `D0, DX, DY, DZ` frame. Apply right-handed `Rx(+90.0 deg)` about `D0`, then translate only in printer Z so the lowest point of `P_BED` is printer `Z=0.000 mm`; no X/Y rotation, mirroring, scaling, or additional tilt. Thus `+DZ -> -printer Y`, `+DY -> +printer Z`, and `+DX -> +printer X`. |
| Bed-contact landmark | `P_BED`: one deliberately planar, nonfunctional exterior side land with outward normal `-DY`, at least 20.0 mm long by 10.0 mm wide (>=200 mm2 total bed contact). It is not an appliance-contact, bar-contact, grip, or cosmetic show face. |
| Bed normal | `+printer Z = +DY` after the stated rotation; the bed-facing outward normal of `P_BED` is `-printer Z = -DY`. |
| Open/insertion direction | Installed engagement opens and inserts along `-DZ`; under this transform it is `-printer Y` (horizontal, parallel to the bed), never toward `-printer Z`. |
| Forbidden downward faces | `F01` cap-face keep-out; every appliance-contact surface on/adjacent to `F02`; all bar-engagement bearing faces; the installed mouth rim/lead-in; all hand-grip/show surfaces. Only `P_BED` may contact the plate. No slicer support contact is permitted on any face. |

## Geometry rules and phase scope
| ID | Rule | Numeric limit | Verification predicate | required_now | deferred_owner | final_gate |
|---|---|---:|---|---|---|---|
| G-01 | Minimum PETG shell, rib, and torque-path wall thickness | >=1.20 mm (3 x 0.42 mm lines) | Re-imported STL wall/thickness samples at every shell, bar-engagement wall, grip root, and rib are >=1.20 mm. | Candidate readiness thickness receipt; independent verifier repeats on re-imported STL. | none | none |
| G-02 | Fit-driving bar cavity, including its full `F02` span, is generated from named parameters and has positive PETG clearance | 0.25-0.35 mm per side in `DX` and `DY`; 0.30-0.40 mm in `DZ` at the seated top; no negative clearance | Sectioned re-imported STL, measured from `D0/DX/DY/DZ`, encloses the nominal `62.00 x 11.70 x 24.00 mm` bar plus the stated clearance; no candidate material intersects `F02`. | Candidate parameter map and datum measurements; verifier interference and full `-DZ` insertion sweep. | none | none |
| G-03 | Appliance protection at full insertion | >=0.50 mm normal clearance from every candidate point to the authorized `Z=0` cap-face keep-out outside `F02`; 0.00 appliance-contact allowance outside `F02` | Re-imported STL section plus full `-DZ` insertion sweep shows the stated clearance and zero collision with `F01/F05`. | Candidate readiness section/sweep; verifier repeats checks 1, 2, and 3 on re-imported STL. | none | none |
| G-04 | Bar contact geometry is broad and smooth, not keyed to unknown `F04` corners | Contact/lead-in edge radius >=0.80 mm; lead-in chamfer >=0.50 mm at 45 deg; 0 teeth, points, or contact protrusions narrower than 1.20 mm | Re-imported-STL section identifies all bar-contact boundaries, radii/chamfers, and confirms no keyed/sharp feature enters the `F02` envelope. | Candidate readiness edge table and section; verifier repeats visual/section inspection. | none | none |
| G-05 | Hand comfort and safe exposed edges | Every hand-contact exterior edge R>=1.50 mm; every other exposed non-bed exterior edge R>=0.80 mm; no exposed edge may be sharp (<0.80 mm radius) | Re-imported STL edge audit samples every grip perimeter, mouth exterior, handle root, and end edge; values meet the stated class. | Candidate readiness edge/comfort preflight; verifier independently inspects rendered exterior and STL samples. | none | none |
| G-06 | Bed-edge elephant-foot control | 0.30 mm x 45 deg chamfer on every `P_BED` perimeter edge; no functional geometry within 0.50 mm of the bed plane | Re-imported STL section at every bed edge finds the 0.30 mm chamfer and >=0.50 mm functional offset. | Candidate readiness planned-orientation face audit; verifier check 7. | none | none |
| SS-01 | `SELF_SUPPORT_REQUIRED`: every transformed non-bed downface, including exterior undersides, cavity undersides, mouth rims, and all nonfunctional decorative geometry | Zero facets/regions that need support; each local underside is self-supporting at >=45 deg above the printer XY plane (equivalently no unsupported overhang beyond 45 deg from vertical) | With the exact transform, re-imported STL face analysis enumerates all downward-facing regions except `P_BED` and reports zero out-of-limit area/footprint; render shows the same regions. | Candidate readiness support-sensitivity preflight with exact transform, 0.4 mm nozzle, 0.42 mm line width, 0.20 mm layer; verifier check 7 repeats it. | none | none |
| SS-02 | `SELF_SUPPORT_REQUIRED`: every roof and bridge, including any bar-cavity ceiling, handle opening, internal relief, and transition roof | Each unsupported bridge span <=5.00 mm; 0 functional roof/bridge droop allowance | Section/layer analysis lists every roof/bridge and its free span; each is <=5.00 mm and no functional face is a bridge underside. | Candidate readiness bridge map/sections; verifier check 7 and section render. | none | none |
| SS-03 | `SELF_SUPPORT_REQUIRED`: every layer-transition feature, including narrowing-upward steps, internal cavity transitions, chamfers, fillets, ribs, and boss-like protrusions | Each unsupported layer-to-layer outward transition is <=0.20 mm per 0.20 mm layer (<=45 deg); 0 horizontal unsupported step area | Exact-orientation sliced-layer or mesh analysis maps every transition and reports zero transition outside the limit. | Candidate readiness layer-transition receipt with regions and layer intervals; verifier check 7 repeats it. | none | none |
| SS-04 | `SELF_SUPPORT_REQUIRED`: support policy | 0.00 mm3 generated support; 0 support interface layers; 0 support-contact faces; 0 support allowance | Native-slicer preview/settings and re-imported STL planned-orientation audit both report supports OFF and no out-of-limit region. | Candidate readiness records supports disabled and all SS results; verifier check 7 validates zero support-required exceptions. | print-engineer: `final_print_prep.md` records the final slicer preview/settings after verifier PASS. | PRINT_PREP |
| G-07 | Structural slicing floor for the specified hand tool | >=4 perimeters (>=1.68 mm nominal perimeter envelope), >=5 top/bottom layers, 30-40% gyroid infill | Final slicer profile records all three values; geometry remains valid under G-01 without relying on infill. | Candidate source/section proves G-01 independently of infill; verifier confirms no geometry rule relies on slicer-only reinforcement. | print-engineer: `final_print_prep.md` profile receipt. | PRINT_PREP |

## Coupon
| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|
| One support-free, one-piece engagement coupon generated from the **same named production bar-cavity, mouth lead-in, contact radii, wall, and clearance parameters**. It shall retain the full 62.00 mm `DX` engagement span and at least 20.00 mm of the production `DZ` engagement depth, plus a rigid hand tab; it is not a nominal surrogate peg/hole coupon. | Production lane only: the exact selected `DX/DY` per-side and `DZ` clearance values from G-02 (no clearance ladder may substitute for this gate). | PETG from the intended final dry spool, main 0.4 mm nozzle, same transform, 0.20 mm layers, and supports OFF. PLA may be printed only as an additional exploratory coupon and cannot pass this PETG gate. | Before final-tool slicing, the coupon must insert on the real bar through the full available `-DZ` travel to its designed seating datum using hand force only; it must rotate at least +10 deg and -10 deg about `DZ` without lift-off, cracking, permanent whitening, gouging, or contact with the cap face outside `F02`. Measure/record: selected cavity `DX/DY/DZ` values, actual bar `DX/DY/DZ` if safely measurable, seating depth, cap-face clearance (>=0.50 mm), and a photo after both directions. Any failure blocks final-tool print and routes to `PRINT_PLAN`/candidate fit parameters. |

## Final-prep placeholders
After verifier PASS, print engineer will issue `final_print_prep.md` with the native X2D PETG profile, dry-filament/offset-calibration receipt, supports OFF/0.00 mm3 preview, the same `Rx(+90.0 deg)` transform and `P_BED` landmark, brim decision, seam placement away from the mouth/contact/grip faces, coupon-first order, final inspection, and a bidirectional field-use observation.  No final print is authorized until the PETG real-bar coupon gate passes.  This accepted r1 plan has no unresolved manufacturing blocker; `Q-004` prevents a torque-capacity claim only, not candidate design or print planning.
