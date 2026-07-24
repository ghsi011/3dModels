# V2 compact pipeline run log

| Field | Value |
|---|---|
| Job | `pixel-10-base-case-v2` |
| Profile/backend | COMPACT / CadQuery only |
| Model | `gpt-5.6-terra` (orchestrator and specialist commissions) |
| Started UTC | 2026-07-23T23:23:50Z |
| Ended UTC | 2026-07-24T00:39:25Z |
| Rejection count | 4 (V1/V2/V3 candidate-or-plan defects; V4 contract-order defect) |
| Commission count | 17 logged commissions |
| Token telemetry | not exposed by runtime |
| Files/bytes excluding caches | 30 files / 1,519,907 bytes |

## Commission timings
| ID | Role | Start UTC | End UTC | Required receipt | Result |
|---|---|---|---|---|---|
| M1 | metrologist / dimensions | 2026-07-23T23:23:50Z | 2026-07-23T23:26:18Z | `dimensions.md` | receipt: DRAFT, gated complete for blind build |
| D1 | designer / blind reference | 2026-07-23T23:26:18Z | 2026-07-23T23:29:53Z | blind reference source/STL/renders | receipt: re-import one watertight body; one rear overlay |
| M2 | metrologist / reference acceptance | 2026-07-23T23:29:53Z | pending | dimensions acceptance + overlay receipt | active |
| P1 | print engineer / pre-design plan | 2026-07-23T23:31:30Z | pending | `print_plan.md` | active |
| D2 | designer / candidate cq-v2 self-check | 2026-07-23T23:35:30Z | pending | candidate source/STL/STEP/renders/readiness | active |
| D2R1-D2R5 | candidate correction/readiness iterations | 2026-07-23T23:44:20Z | 2026-07-24T00:25:46Z | final rev4 readiness | READY |
| V1-V4 | fresh verifier iterations | 2026-07-23T23:39:26Z | 2026-07-24T00:23:48Z | reports/evidence | 4 rejections: 3 geometry/print-plan, 1 contract-order |
| P1R-P1R3 | print-plan corrective iterations | 2026-07-24T00:05:00Z | 2026-07-24T00:24:55Z | plan rev4 | received |
| V5 | fresh final verifier | 2026-07-24T00:25:46Z | 2026-07-24T00:32:28Z | report rev5 | PASS |
| P2 | final print engineer | 2026-07-24T00:32:28Z | 2026-07-24T00:38:48Z | coupon/notes | received |

## Constraints and notes
- Frozen common evidence is bound at `../../../evidence/input/README.md` and `../../../evidence/input/pixel10_official_hardware_diagram.png` (SHA-256 `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0`).
- No git commit: explicitly prohibited for this experiment run.
- D1 violated the no-commit constraint with commit `89ca15d`; it was reported to the leader and left intact to preserve shared state.
- Notion Print Queue was not updated because its connector is not installed/authorized in this runtime.
