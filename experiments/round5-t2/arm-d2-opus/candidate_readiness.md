---
contract: candidate-readiness
contract_version: 4
job_id: round4-t2-team-v4
candidate_id: D2-arm-d2-opus
owner: cad-designer
status: READY
non_acceptance: true
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
candidate_stl_sha256: 390d7eed0869df9fc66f89a46ce49c678deb9dfdbb41c3eb7d2238cd6e89f725
updated_utc: 2026-07-24T20:05:00Z
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

This is designer self-check evidence only. It is never acceptance and never substitutes for
fresh independent verification. `candidate_preflight_validation.json` = **PASS** (exit 0).

| Pre-dispatch check on re-imported STL | Required | Observed | Result | Evidence |
|---|---:|---:|---|---|
| One watertight intended body and bounds | yes | watertight; bounds `[-34.6,-16,3]…[34.6,22.137,26.7]`, extents `69.2×38.137×23.7` | PASS | measure.json |
| Seated interference | zero collision | max signed dist −0.317 mm (0 pts inside tool) | PASS | interference sweep (728 bar-surface pts) |
| Full insertion/travel sweep | zero forbidden collision | prismatic −Z slide; 0 collision to seated; ceiling = 0.70 mm over-travel stop | PASS | sweep + wall positions |
| Installed-coordinate section proves architecture/open face | yes | mouth open toward −Z; +Y gable; cavity encloses bar | PASS | render_mating_section.png |
| Named bed face at printer Z=0 after exact transform | yes | P_BED = installed Y=−16 → printer_Z=0; area 1582 mm² (≥200); sole plate face | PASS | render_print_orientation.png; S-01 audit |
| Unsupported roof/critical wall floors | plan limits | S-01..S-04 out-of-limit = 0.000 mm²; min structural wall 2.0 mm (≥1.20) | PASS | S-0x-support-audit.json; measure.json |
| Required renders/STEP/source present | yes | model.py, coupon.py, STL, STEP, coupon STL, 4 renders, JSON receipts | PASS | arm folder listing |

## Edge/comfort preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE
| Edge ID / feature boundary | Exposure class | Required radius or allowed-sharp condition | Re-imported-STL samples/method | Observed min/max | Result | Evidence |
|---|---|---|---|---:|---|---|
| E-01 hand-grip exterior perimeter | EXPOSED_COMFORT | ≥1.50 mm, 3 samples | circle-fit on X-Z sections at Y=−6,4,12: [2.0,2.0,2.0] | 2.0 / 2.0 | PASS | measure.json E01_grip_R |
| E-02 grip/handle-root transitions | EXPOSED_FUNCTIONAL | ≥0.80 mm, 3 samples | circle-fit on Y-Z sections at X=−22,0,22: [1.0,1.0,1.0] | 1.0 / 1.0 | PASS | measure.json E02_top_R |
| E-03 exterior mouth rim + lead-in | EXPOSED_FUNCTIONAL | ≥0.80 mm, 3 samples | circle-fit on Y-Z sections at X=−25,0,25: [0.9,0.9,0.9] | 0.9 / 0.9 | PASS | measure.json E03_mouth_R |
| E-04 bar-engagement bearing boundaries | EXPOSED_FUNCTIONAL | ≥0.80 mm, no keyed feature | circle-fit on X-Y sections at Z=8,14,22: [0.9,0.9,0.9] | 0.9 / 0.9 | PASS | measure.json E04_bear_R |
| E-05 P_BED chamfer | BED_CONTACT | allowed sharp; 0.30 mm × ≥45° relief, ≥0.5 mm off functional | 0.30 mm relief at 48°; nearest functional geom at Z=3 (printer_Z≥9.85) | allowed | PASS | render_print_orientation.png |

## Support-sensitivity preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE
| Rule/region ID | Exact transform/layer/nozzle predicate | Mesh result/footprint/interval | Plan disposition | Allowed contact class and forbidden faces checked | Result | Evidence |
|---|---|---|---|---|---|---|
| S-01 non-bed downfaces | matrix as plan; normal_z≤−0.70710679 non-bed | out-of-limit 0.000 mm²; 0 faces; bed 1583 mm² | SELF_SUPPORT_REQUIRED | only P_BED touches; forbidden faces none | PASS | S-01-support-audit.json |
| S-02 roofs/bridges | free bridge ≤5.0 mm | 0.000 mm²; gable roof self-supports; top slab vertical in print | SELF_SUPPORT_REQUIRED | no mating/grip/lead-in face is a bridge underside | PASS | S-02-support-audit.json |
| S-03 layer transitions | outward step ≤0.20 mm/layer (≥45°) | 0.000 mm²; all transitions ≥45° | SELF_SUPPORT_REQUIRED | chamfers/fillets ≥45° from horizontal | PASS | S-03-support-audit.json |
| S-04 zero-support policy | 0 mm³ support, supports OFF | 0.000 mm²; supports OFF | SELF_SUPPORT_REQUIRED | 0 interface/contact faces | PASS | S-04-support-audit.json |

## Parameter mapping
| Contract IDs | Source parameter(s) |
|---|---|
| M02/F02 length, G-02 end | `BAR_L=62`, `CL_END=0.60` → cavity X half `CX=31.6` |
| M03 width, G-02 side | `BAR_W=11.7`, `CL_SIDE=0.40` → cavity Y half `CY=6.25` |
| M04 height, G-02 top | `BAR_H=24`, `CL_TOP=0.70` → ceiling `CZ_TOP=24.7` |
| M05/G-03 cap protection | mouth `Z_MOUTH=3.0` → 3.0 mm to D0 outside F02 |
| G-01 wall floor | `WALL=2.0`, `WALL_END=3.0` (all ≥1.20) |
| G-04/E-03/E-04 | `ROOT_R=0.90` lead-in/bearing radius |
| E-01 comfort | `GRIP_R=2.0` |
| G-06/E-05 | `PBED_Y=-16.0`, `PBED_CH=0.30`, `PBED_CH_DEG=48` |
| S-01..S-04 self-support | gable `ROOF_DEG=52` (ridge along X); transform per plan |

## Commands and hashes
```text
# build (build123d venv via harness)
python experiments/round5-t2/cad_runner.py --interp C:/Users/ghsi0/b123dv/Scripts/python.exe \
  --script .../arm-d2-opus/candidate_model.py --timeout 120 --mem-mb 4000 --label build_final \
  --workdir .../arm-d2-opus
python .../cad_runner.py --interp <venv> --script .../candidate_coupon.py ... --label coupon
# measure + gates (system python)
python .../arm-d2-opus/measure.py
python skills/3d-modeling/scripts/team_preflight.py support-audit --stl candidate_tool.stl \
  --plan inputs/print_plan_checks.json --rule-id S-0x --output S-0x-support-audit.json
python skills/3d-modeling/scripts/team_preflight.py validate-receipts --stl candidate_tool.stl \
  --plan inputs/print_plan_checks.json --readiness candidate_preflight.json \
  --output candidate_preflight_validation.json   # => PASS

candidate_tool.stl   sha256 390d7eed0869df9fc66f89a46ce49c678deb9dfdbb41c3eb7d2238cd6e89f725
print_plan_checks.json sha256 6f146669b2c819d9b013c31d2e54b4c7a27eec8cec645e9614fcb5fcbdff0016
```
