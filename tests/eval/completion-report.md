# Completion report — external-review implementation + optimization experiment

Autonomous run against the green-lit plan (Sprint 1, Sprint 1A, H-03, cheap Sprint 2 slices).
Pixel ④ was preserved untouched until it finished; all gate/contract edits landed after.
**COMPLETE.** Three clean commits: `2e59f9a` (Sprint 1 + 1A), `6416da0` (H-03), `2cddbf1` (Sprint 2).

## Final validation (all pass)
- **Solo monolith unchanged** — `skills/3d-modeling/SKILL.md` + `fdm-design.md` byte-identical to
  session start (empty diff vs `backup/pre-rebase-f8dac6`). Invariant held.
- Tests: `team_preflight` **49**, `mesh_io` **5**, `team_tools` **71** — all green; `ruff` clean;
  `git diff --check` clean; `team_preflight --help` exposes support-audit/validate-receipts/validate-interfaces.
- No skill code uncommitted; remaining uncommitted = experiment records (`tests/eval/`, round5) +
  the user's own `tests/` reorg (not mine to commit).
- **"lazycodex final gate review" (task #12):** lazycodex is a Codex-plugin tool not available in
  Claude Code; the **fresh-context Opus reviewer** (`sprint1-verification.md`) served that role —
  independent adversarial audit, verdict Sprint 1/1A PASS, 0 defects. Recorded honestly.

## Changes by requirement ID
| Req | What | Status |
|---|---|---|
| **Sprint 1 / C-02 / R-01** | Reject non-finite/negative/None/malformed numbers in the preflight gate (closed a confirmed NaN false-pass) | DONE, committed `2e59f9a` |
| **Sprint 1 / bug B** | Fix `float(None)`/S-03 crash (read cap only inside SELF_SUPPORT_REQUIRED) | DONE |
| **Sprint 1 / P-11** | Validate finite-rigid transforms; contain evidence paths (`..`/abs/symlink) | DONE |
| **Sprint 1 / C-03 / P-12** | Honestly relabel support-audit → "downward-facing-surface screen" (no supportability claim) | DONE |
| **Sprint 1 / C-01 / P-01** | `team-contracts-v4.md` sole normative; `team-design.md` historical notice; AGENTS.md guarded-pilot + judgment-vs-enforcement split | DONE |
| **Sprint 1A** | `team_tools` contract-automation CLI (validate/hash/status/render + artifact_manifest); auto SHA-256 + revision binding; finite/enum/ID/FK/path validation; 25.4× check; agent summary | DONE, committed `2e59f9a`, 68 tests |
| **H-03 / P-04 + rec 1** | Fit-strategy ownership metrologist → print engineer; structured per-interface declaration + `validate-interfaces` enforcement | DONE, committed `6416da0`, 49 tests |
| **Sprint 2A** | artifact_manifest + 25.4× adoption (required output; hard UNIT_SCALE reject) | DONE, committed `2cddbf1` |
| **Sprint 2B / P-03** | risk-classification gate (R0–R3) in orchestrator + optional `risk_class` field | DONE, committed `2cddbf1` |
| **Sprint 2C / P-14** | mesh raw-vs-normalized reporting (`load_mesh` unchanged; verifier uses raw) | DONE, committed `2cddbf1` |
| **Deferred** | `cad_runner` resource governor (reviewer: "not cheap, split, last"); motion/contact engine; 3MF rewrite; Bambu adapter; camera calibration; golden-fixture regression | out of green-lit scope |

## Files changed (committed)
`2e59f9a` — skills/: 3d-metrologist, 3d-print-engineer slices (spec fixes); 3d-modeling/references/team-contracts-v4.md; team_preflight.py + test_team_preflight.py (Sprint 1); team-design.md; AGENTS.md; make_3mf.py (cosmetic ruff); team_tools/ (13 files, Sprint 1A).
`6416da0` — skills/: all 5 role slices + team-contracts-v4.md + team_preflight.py + test_team_preflight.py (H-03).

## Tests
- `test_team_preflight.py`: 5 → 33 (Sprint 1) → **49** (H-03), all green.
- `team_tools/test_contracts.py`: **68** green.
- ruff clean across `skills/3d-modeling/scripts`; `git diff --check` clean.
- Fresh-context Opus reviewer independently re-broke every attack: **Sprint 1 PASS, Sprint 1A PASS, 0 correctness defects** (`tests/eval/sprint1-verification.md`).

## Bugs
- **Reproduced + fixed:** R-01 (NaN/±Inf/null/bool samples PASSed the gate — confirmed, now rejected); bug B (`float(None)` S-03 crash — confirmed on the real Pixel S-03 null cap, now a clean field-named error).
- **Not reproduced (noted):** R-02 (malformed-3MF-written-as-success) — plausible from the code shape (raw string XML), left to the deferred 3MF rewrite; the `make_3mf.py` change so far is cosmetic (does NOT fix R-02).

## Contract-migration implications
- `team-contracts-v4.md` is now the sole normative runtime contract; `team-design.md` "Exact template" sections are historical.
- Fit clearance moved out of `dimensions.md` (as-observed + uncertainty) into `print_plan.md` `interfaces` (owned by print engineer). Existing dimensions sheets that prescribed a fit band are superseded — the print plan now declares it. Backward-compatible: `interfaces` is optional in `print_plan_checks.json` (absent → skipped).
- New optional structured JSON mirror (`team_tools`) for job_state/dimensions/print_plan/verification_report/artifact_manifest — not a forced migration; adopt per new job.

## Experiment result (the optimization)
See `optimization-summary.md`. Two spec fixes validated across 3 parts / 3 fit types with no
regression; **the fit-band fix propagated to real Pixel-case geometry at 0.20 mm/side (in-band)**.
Design step ④ is the quality frontier. Meta-finding (executable gates ≠ functional correctness)
independently corroborated by the external review.

## Remaining manual agent steps / deferred / risks
- Remaining manual (by design — agent judgment): interpret photos, choose datums/geometry, choose
  fit/manufacturing strategy, accept/reject designs, high-risk sign-off.
- Deferred (need a decision on scope): resource governor, contact/motion model, 3MF fail-closed
  writer, Bambu adapter, camera calibration, golden-fixture v4 regression.
- Risk/assumption: `team_tools` structured JSON is adopted per-new-job, not back-migrated; the
  optimized repo skill is **not yet the registered/invocable skill** (install before real use).

## Exact next recommended slice
The `cad_runner` resource governor (split: (1) wrap CadQuery in an isolated child with wall/mem/
proc-tree/output/triangle/log caps + failure receipt; (2) wire it into the designer commission),
then the golden-fixture v4 regression, then the contact/motion model (the biggest correctness item).
