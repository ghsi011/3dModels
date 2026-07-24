---
contract: candidate-readiness
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
candidate_id: cq-a
owner: cad-designer
status: READY
non_acceptance: true
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
candidate_stl_sha256: 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df
updated_utc: 2026-07-24T03:16:00Z
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Pre-dispatch check on re-imported STL | Required | Observed | Result | Evidence |
|---|---:|---|---|---|
| One watertight intended body and bounds | yes | watertight; 1 component; `[-42.000,-8.000,0.600]..[42.000,8.000,64.994]` mm | PASS | `evidence/candidates/cq-a/reimport_metrics.txt` |
| Seated interference | plan threshold | rectangular `F02` occupies the `62.60 × 12.30 × 24.35` cavity; clearance X/Y `0.300`, top Z `0.350` mm; zero material in F02 | PASS | `evidence/candidates/cq-a/reimport_metrics.txt`, `cq-a-section.png` |
| Full insertion/travel sweep | zero forbidden collision | seated candidate translated `+DZ` in 0.20-mm increments through 24.00 mm leaves bar travel toward the open `-DZ` mouth; zero forbidden collision; roof is the terminal positive-DZ stop | PASS | `cq-a-installed-engagement.png`, source parameters |
| Installed-coordinate section proves architecture/open face | yes | `-DZ` mouth, protected `Z=0` cap plane, X end stops, positive-DZ roof, and open `+DY` inspection side shown | PASS | `cq-a-section.png` |
| Named bed face at printer Z=0 after exact transform | yes | native minimum `Y=-8.000`; all lowest planar contact belongs to `P_BED`; `Rx(+90°)` makes it printer `Z=0`; planar contact exceeds 200 mm2 | PASS | `evidence/candidates/cq-a/reimport_metrics.txt`, `cq-a-print-orientation.png` |
| Unsupported roof/critical wall floors | plan limits | native min Y equals P_BED exactly; forbidden/non-P_BED transformed downface area `0.000000 mm2`; bridge span `0.000 mm`; transition excess `0.000 mm2` | PASS | `evidence/candidates/cq-a/reimport_metrics.txt` |
| Required renders/STEP/source present | yes | model, verifier, STL, STEP and four required PNGs present | PASS | `evidence/candidates/cq-a/manifest.md` |

## Edge/comfort preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Edge ID / feature boundary | Exposure class | Required radius or allowed-sharp condition | Re-imported-STL samples/method | Observed min/max | Result | Evidence |
|---|---|---|---|---:|---|---|
| E-01 grip circular perimeter, top hand-contact rim | EXPOSED_COMFORT | R >= 1.50 | re-imported STL toroidal triangle-ring samples at +DZ/top, +DX/right and -DZ/bottom sectors | top `1.594322..1.601218`; right `1.594323..1.602598`; bottom `1.594323..1.601218` mm | PASS | `evidence/candidates/cq-a/reimport_metrics.txt`, `evidence/candidates/cq-a/v3-01-correction.md` |
| E-02 base outer XZ perimeter | EXPOSED_COMFORT | R >= 1.50 | re-imported STL triangle-ring samples: lower endpoint, interior rail and upper endpoint | lower `1.799517..1.799519`; interior `1.599570..1.599573`; upper `1.799517..1.799519` mm | PASS | `evidence/candidates/cq-a/reimport_metrics.txt`, `evidence/candidates/cq-a/v2-01-correction.md` |
| E-03 left end-stop bar bearing boundary | EXPOSED_FUNCTIONAL | R >= 0.80 | re-imported STL lower, middle and upper cylindrical-ring samples | 0.899744 / 0.899758 mm minimum/maximum | PASS | `evidence/candidates/cq-a/edge_audit.md` |
| E-04 right end-stop bar bearing boundary | EXPOSED_FUNCTIONAL | R >= 0.80 | re-imported STL lower, middle and upper cylindrical-ring samples | 0.899745 / 0.899758 mm minimum/maximum | PASS | `evidence/candidates/cq-a/edge_audit.md` |
| E-05 mouth/roof lead-in boundary | EXPOSED_FUNCTIONAL | >=0.50-mm 45-degree lead-in; no tooth or point | re-imported section at left endpoint, centre and right endpoint | 0.900 / 0.900 mm chamfer leg | PASS | `evidence/candidates/cq-a/edge_audit.md`, `cq-a-section.png` |
| E-06 cap-protective lower boundary | EXPOSED_FUNCTIONAL | kept at least 0.50 mm from cap plane; no cap contact | re-imported lower-Z extrema at left endpoint, centre and right endpoint | 0.600 / 0.600 mm clearance | PASS | `evidence/candidates/cq-a/edge_audit.md` |
| E-07 P_BED perimeter | BED_CONTACT | 0.30 mm x 45 degree chamfer | re-imported endpoint/interior sections on P_BED perimeter | 0.300 / 0.300 mm chamfer leg | PASS | `evidence/candidates/cq-a/edge_audit.md`, `cq-a-print-orientation.png` |

## Support-sensitivity preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Rule/region ID | Exact transform/layer/nozzle predicate | Mesh result/footprint/interval | Plan disposition | Allowed contact class and forbidden faces checked | Result | Evidence |
|---|---|---|---|---|---|---|
| SS-01 | `Rx(+90°)`; `+DY -> printer +Z`; 0.20-mm layer, 0.4-mm nozzle, 0.42-mm line | native min Y/P_BED `-8.000/-8.000 mm`; non-P_BED downface area `0.000000 mm2`; no out-of-limit footprint | SELF_SUPPORT_REQUIRED | only P_BED and its 0.30-mm perimeter chamfer are bed-facing; no appliance, F02, mouth, grip, or show face contact | PASS | `evidence/candidates/cq-a/reimport_metrics.txt`, `evidence/candidates/cq-a/v1-01-correction.md` |
| SS-02 | same exact transform/process | open lateral channel; no roof/bridge underside; maximum free bridge `0.000 mm` | SELF_SUPPORT_REQUIRED | no support contact class exists | PASS | `cq-a-section.png` |
| SS-03 | same exact transform/process | monotonic material growth in `+DY`; transition excess `0.000 mm2`; no horizontal unsupported step | SELF_SUPPORT_REQUIRED | no support contact class exists | PASS | `evidence/candidates/cq-a/reimport_metrics.txt` |
| SS-04 | same exact transform/process | supports OFF; generated support `0.000 mm3`; interface layers `0`; contact faces `0` | SELF_SUPPORT_REQUIRED | all plan-forbidden faces remain free of support contact | PASS | `evidence/candidates/cq-a/reimport_metrics.txt` |

## Parameter mapping

| Contract IDs | Source parameter(s) |
|---|---|
| D-001 / F01 / G-03 | `CAP_RADIUS`, `CAP_CLEARANCE` |
| D-002 / G-02 | `BAR_LENGTH`, `FIT_CLEAR_XY`, `CAVITY_X` |
| D-003 / G-02 | `BAR_WIDTH`, `FIT_CLEAR_XY`, `CAVITY_Y` |
| D-004 / G-02 | `BAR_HEIGHT`, `FIT_CLEAR_Z_TOP`, `CAVITY_Z`, `CAVITY_TOP_Z` |
| G-01 / G-07 | `MIN_WALL` |
| G-04 | `CONTACT_RADIUS`, `END_WALL`, roof `CONTACT_RADIUS` chamfer |
| G-05 | `COMFORT_RADIUS`, `GRIP_RIM_RADIUS`, `BASE_EDGE_RADIUS`, `BASE_SIDE_RADIUS` |
| G-06 / SS-01..SS-04 | `BED_CHAMFER`, `BASE_Y_MIN`, print-plan transform |

## Commands and hashes

```powershell
python .\model.py
python .\verify.py
Get-FileHash .\cq-a-washer-filter-tool.stl -Algorithm SHA256
```

Final STL: `39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df`.
