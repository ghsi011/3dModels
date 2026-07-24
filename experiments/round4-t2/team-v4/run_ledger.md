# Run ledger — round4-t2 team-v4

| UTC | Event | Commission/context | Evidence / command / result |
|---|---|---|---|
| 2026-07-24T02:43:20.6026717Z | output folder created | orchestrator | `experiments/round4-t2/team-v4` |
| 2026-07-24T02:43:26.8050992Z | common inputs hashed | orchestrator | brief `e82b8a49…`; schematic `495ad7be…` |
| 2026-07-24T02:44:01.6945150Z | manifest bound | orchestrator | `common_manifest.json` `ed4659f5…`; requested `.md` path absent, corrected participant-visible path provided by leader |
| 2026-07-24T02:44:15Z | pipeline initialized | orchestrator | COMPACT, CadQuery-only, seven planned commissions, token telemetry: not exposed |
| 2026-07-24T02:57:50Z | D2 start / usage-limit interruption | Terra runner (gpt-5.6-terra) | Prior `/root/round4_team_v4` runner hit a platform usage limit at the start of D2; no design or D2 output produced. INFRASTRUCTURE INTERRUPTION, not a design-correction loop; not a candidate commission. Prior M1/D1/M2/P1 artifacts preserved. |
| 2026-07-24T13:31:33Z | resume — durable runner migration | orchestrator (Claude Code main session) | Stale active member-A binding repaired via new durable record (`runner_migration.md`), retaining `.omo/teams/team-44ca6798/{team.json,guide.md}` unchanged. OMO/GPT team transport → Claude Code Agent-tool subagents. New specialists D2/O1/V1/P2 + grader run on Claude Opus (`claude-opus-4-8`), per user directive; arm is a disclosed mixed-model continuation (Terra M1–P1, Opus D2–P2). See `runner_migration.md`. |
| 2026-07-24T14:13Z | D2 (Opus) attempt aborted | orchestrator | First Claude Opus 4.8 D2 dispatch ran ~40 min and persisted zero artifacts (still in read/model phase, no exports). Aborted to stop non-converging spend. EFFICIENCY/INFRASTRUCTURE abort, not a design-correction loop; no candidate geometry was produced or verified. Approach + model policy under review with the user before re-dispatch. |
| 2026-07-24T13:31:33Z | resume verification | orchestrator | M1/D1/M2/P1 gates re-verified. STL geometry hash `25fac0c2…` matches everywhere (ledger/manifest/blob/worktree). dimensions r2 `1e233ca7…`, print_plan `1a54f2bc…`, plan_checks `ad6b910d…` match ledger as git-blob (LF) hashes. Text-file working-tree hashes differ from ledger only by `core.autocrlf` CRLF conversion on checkout; content intact. Toolchain OK: cadquery 2.8.0, trimesh 4.12.2, numpy 2.4.6, matplotlib 3.11.1, OCP 7.9.3.1. Checklist integration: main `6117f0d` rebased in (`preflight-checklist.md`). |

## Commission summary

| ID | Role | Context ID | Start UTC | End UTC | Budget min | Result | Correction |
|---|---|---|---|---|---:|---|---|
| M1 | metrologist | not exposed | 2026-07-24T02:45:12.4637354Z | 2026-07-24T02:46:26.4750280Z | 3 | complete | none |
| D1 | designer/reference | not exposed | 2026-07-24T02:48:25.0000000Z | 2026-07-24T02:50:11.8167364Z | 4 | complete; pending M2 acceptance | none |
| M2 | metrologist/acceptance | not exposed | 2026-07-24T02:52:37.0320848Z | 2026-07-24T02:52:56.7303401Z | 3 | complete; ACCEPTED | none |
| P1 | print engineer/plan | not exposed | 2026-07-24T02:53:30.0000000Z | 2026-07-24T02:56:46.5340827Z | 4 | complete; ACCEPTED | none |
| D2 | designer/candidate | pending | | | 9 | pending | none |
| V1 | verifier/fresh | pending | | | 8 | pending | none |
| P2 | print engineer/final prep | pending | | | 5 | pending | none |

## Runtime telemetry

Token counts: not exposed; never estimated.

## M1 execution receipt

| Item | Record |
|---|---|
| Commission | M1 / metrologist |
| Context ID | not exposed |
| Start UTC | 2026-07-24T02:45:12.4637354Z |
| End UTC | 2026-07-24T02:46:26.4750280Z |
| Commands | `Get-Content -Raw skills/3d-metrologist/SKILL.md`; `Get-Content -Raw` common brief, manifest, fixture SVG, `job_state.md`, `run_ledger.md`, v4 contracts, and CadQuery datum/overlay patterns; `apply_patch` dimensions and ledger; `Get-Date` UTC. |
| Failures | none |
| Token telemetry | not exposed |
| Output SHA-256 | `dimensions.md` `d84627a873ee4eb24d7fc151e645368b3c374d11bef58320773dcc0d8555329c` |

## Final inventory

Pending after delivery: exact file count, bytes, canonical hashes, command results, and failures.

## D1 execution receipt

| Item | Record |
|---|---|
| Commission | D1 / blind reference designer |
| Context ID | not exposed |
| Start UTC | 2026-07-24T02:48:25.0000000Z |
| End UTC | 2026-07-24T02:50:11.8167364Z |
| Inputs | `dimensions.md` r1 only for geometry; matching top/side fixture SVG solely for requested aligned views |
| Commands | `Get-Content -Raw skills/3d-designer/SKILL.md`; `Get-Content -Raw` dimensions/job_state/run_ledger and fixture SVG; `python reference_model.py`; `Get-FileHash`; `python -c` `trimesh` re-import bounds audit |
| Outputs | `reference_model.py`, `reference_bar.stl`, `reference_bar.step`, five SVG views, `reference_manifest.md` |
| Results | F02 exact re-import bounds `62.000 × 11.700 × 24.000 mm`; watertight STL, 12 faces; M2 acceptance pending |
| Failures | CadQuery `importSTL` helper absent, replaced with installed `trimesh`; two Chromium SVG-to-PNG captures produced no file, SVG renders retained |
| Token telemetry | not exposed |
| Inventory at receipt | 13 files / 71,040 bytes; within the 35-file / 1,000,000-byte limit |

## M2 execution receipt

| Item | Record |
|---|---|
| Commission | M2 / metrologist acceptance |
| Context ID | not exposed |
| Start UTC | 2026-07-24T02:52:37.0320848Z |
| End UTC | 2026-07-24T02:52:56.7303401Z |
| Commands | `Get-Content -Raw` M2-authorized contracts/artifacts and fixture SVG; `Get-ChildItem -Recurse -File` team output inventory; `view_image reference_overlay_top.png`; `python -c` `trimesh` STL re-import bounds/watertight audit; `Get-FileHash`; `apply_patch` dimensions and ledger; `Get-Date` UTC. |
| Acceptance | Look-first top overlay and matching side overlay coincide on D0–D3/F02; independent re-import reports `62.0 × 11.7 × 24.0 mm`, min `[-31,-5.85,0]`, max `[31,5.85,24]`, watertight, 12 faces. |
| Hashes | reference STL `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a`; top/side overlays `11fefffdcb920a8fb57852e6143e6cca6bd6e04c948f41d528354d8f46b1894f` / `c9a49c14d31c5603cd53e4672cb3e424eec9171c26671da6445de81cf35da0dd`; accepted dimensions r2 `1e233ca7c2041c7a6583c62b910ef39fee4cfefd3868db14fedb26e6208783c6`. |
| Failures | none |
| Token telemetry | not exposed |

## P1 execution receipt

| Item | Record |
|---|---|
| Commission | P1 / print engineer pre-design plan |
| Context ID | not exposed |
| Start UTC | 2026-07-24T02:53:30.0000000Z |
| End UTC | 2026-07-24T02:56:46.5340827Z |
| Inputs | `dimensions.md` r2; `reference_manifest.md`; `reference_bar.stl`; `job_state.md`; `run_ledger.md`; v4 print-plan contract; FDM, X2D, and materials references. |
| Commands | `Get-Content -Raw skills/3d-print-engineer/SKILL.md`; `Get-Content -Raw` authorized contracts/artifacts and required references; `Get-Item`/`Get-FileHash` reference STL; `apply_patch` plan/check projection/ledger; PowerShell `ConvertFrom-Json` schema, exact ID-set, and disposition checks; `Get-FileHash -Algorithm SHA256`. |
| Result | ACCEPTED r1: CadQuery installed-to-printer matrix freezes `P_BED` at installed `Y=-16.000 mm`; PETG main 0.4 mm, 0.20/0.42 profile; five Edge IDs E-01..E-05; four SELF_SUPPORT_REQUIRED rules S-01..S-04; supports prohibited; actual-engagement PETG coupon required before final printing. |
| Failures | none |
| Token telemetry | not exposed |
| Output SHA-256 | `print_plan.md` `1a54f2bcdffe3b0689501b1cd757d5aa33deac19ec7fedd035f54794ddb4bd9e`; `print_plan_checks.json` `ad6b910db21664f5a5e7f81f78500b33da7ef062a8925dc8080dfdb6182e5f53` |
