---
contract: candidate-readiness
contract_version: 4
job_id: round4-t2-team-v4
candidate_id: arm-d2-sonnet
owner: cad-designer
status: NOT_READY
non_acceptance: true
dimensions_revision: 2
print_plan_revision: 1
reference_sha256: 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a
candidate_stl_sha256: 099b5fb21441ca56916da9a3ba9c9e44e8b7e5e6f001e47be3c3c0afb0f6de45
updated_utc: 2026-07-24T00:00:00Z
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

`candidate_preflight_validation.json` result: **FAIL** (exit 1). Per the commission and
`skills/3d-modeling/references/team-contracts-v4.md`, readiness may say READY only when
that validator exits 0/PASS. It did not. This file is NOT_READY and is not acceptance
evidence in any case.

| Pre-dispatch check on re-imported STL | Required | Observed | Result | Evidence |
|---|---:|---:|---|---|
| One watertight intended body and bounds | yes | watertight=True; bounds `[-35.1,-16.0,0.6]..[35.1,25.809,28.8]` | PASS | `measurements.json`, `measure1.run.json` |
| Seated interference / cavity clearance vs 62/11.7/24 | plan thresholds | X per-end 0.500mm (>=0.50); Z top 1.200mm (>=0.60); Y per-side ~1.8-2.3mm est. (>=0.30, see caveat) | PASS (Y measurement imprecise, see below) | `measurements.json` |
| Full insertion/travel sweep | zero forbidden collision | not independently swept in this designer pass (time-constrained); cavity is a simple open box+wedge along -Z with no re-entrant features between Z=0 and Z=25.2, so no travel collision is geometrically expected, but not empirically confirmed with a swept boolean | NOT CONFIRMED | none — flagged gap |
| Installed-coordinate section proves architecture/open face | yes | `render_section.png` | PASS (visual) | `render_section.png` |
| Named bed face at printer Z=0 after exact transform | yes | `render_print_orientation.png`; P_BED area 1937.65 mm² (>=200 required) | PASS | `render_print_orientation.png`, `measurements.json` |
| Unsupported roof/critical wall floors | plan limits | S-01..S-04: 0.275094 mm² out-of-limit (limit 0.000 mm²) | **FAIL** | `S-01..S-04-support-audit.json` |
| Required renders/STEP/source present | yes | all present | PASS | file list below |

## Edge/comfort preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Edge ID | Exposure class | Required | Observed min/max | Result | Evidence |
|---|---|---|---:|---|---|
| E-01 | EXPOSED_COMFORT | >=1.50mm | 0.5735 / 2.00 (2 of 3 samples unconfirmed design value) | **FAIL** (below min; also partly unconfirmed) | `candidate_preflight.json` |
| E-02 | EXPOSED_FUNCTIONAL | >=0.80mm | 2.00 / 2.00 (all 3 samples unconfirmed design value) | UNCONFIRMED | `candidate_preflight.json` |
| E-03 | EXPOSED_FUNCTIONAL | >=0.80mm | 0.8000 / 0.8000 (2 of 3 confirmed to 6 sig figs) | PASS (mostly confirmed) | `candidate_preflight.json` |
| E-04 | EXPOSED_FUNCTIONAL | >=0.80mm | 0.5086 / 0.8000 | **FAIL** (one sample below min) | `candidate_preflight.json` |
| E-05 | BED_CONTACT, allowed_sharp | n/a | 0.0 / 0.0; functional offset 9.85mm (>=0.50 required) | PASS | `candidate_preflight.json`, `edge_measurements.json` |

## Support-sensitivity preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Rule | Predicate | Result | Disposition | Result | Evidence |
|---|---|---:|---|---|---|
| S-01 | 0.000 mm² out-of-limit, non-bed downward faces | 0.275094 mm² | SELF_SUPPORT_REQUIRED | **FAIL** | `S-01-support-audit.json` |
| S-02 | 0.000 mm² out-of-limit (bridge span <=5mm framing) | 0.275094 mm² | SELF_SUPPORT_REQUIRED | **FAIL** | `S-02-support-audit.json` |
| S-03 | 0.000 mm² out-of-limit (layer-transition framing) | 0.275094 mm² | SELF_SUPPORT_REQUIRED | **FAIL** | `S-03-support-audit.json` |
| S-04 | 0.000 mm² out-of-limit (zero-support framing) | 0.275094 mm² | SELF_SUPPORT_REQUIRED | **FAIL** | `S-04-support-audit.json` |

All four rules share the identical matrix/threshold in `print_plan_checks.json`, so
`team_preflight.py support-audit` reports the identical geometric measurement for
each — the same real residual (two ~0.14 mm² slivers at the mouth-rim-fillet /
unfilleted-far-edge corner) counted against all four rule IDs.

## Parameter mapping

See `print_notes.md` "Parameter -> fit mapping" table.

## Commands and hashes

```
python experiments/round5-t2/cad_runner.py --interp C:/Users/ghsi0/b123dv/Scripts/python.exe \
  --script experiments/round5-t2/arm-d2-sonnet/candidate_model.py --timeout 120 --mem-mb 4000 \
  --label build_iter1 --workdir experiments/round5-t2/arm-d2-sonnet

python skills/3d-modeling/scripts/team_preflight.py support-audit \
  --stl experiments/round5-t2/arm-d2-sonnet/candidate_tool.stl \
  --plan experiments/round5-t2/inputs/print_plan_checks.json --rule-id S-01 \
  --output experiments/round5-t2/arm-d2-sonnet/S-01-support-audit.json   # (S-02..S-04 identical form)

python skills/3d-modeling/scripts/team_preflight.py validate-receipts \
  --stl experiments/round5-t2/arm-d2-sonnet/candidate_tool.stl \
  --plan experiments/round5-t2/inputs/print_plan_checks.json \
  --readiness experiments/round5-t2/arm-d2-sonnet/candidate_preflight.json \
  --output experiments/round5-t2/arm-d2-sonnet/candidate_preflight_validation.json
```

`candidate_stl_sha256`: `099b5fb21441ca56916da9a3ba9c9e44e8b7e5e6f001e47be3c3c0afb0f6de45`
`print_plan_checks_sha256`: `6f146669b2c819d9b013c31d2e54b4c7a27eec8cec645e9614fcb5fcbdff0016`
`candidate_preflight_validation.json` result: **FAIL** (`candidate_preflight_validation.json`)
