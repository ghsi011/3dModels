# Arm S (Sonnet 5) — measured D2 result

Sweep start 2026-07-24T14:50:40Z. Arm S completed with an honest **NOT_READY** self-report;
orchestrator (O1) independently reproduced every failure. Candidate never advanced to V1
because it fails its own executable gates (correct pipeline behavior — only READY candidates
are verified).

## Cost / process (token telemetry IS exposed for Claude subagents — measured, not estimated)

| Metric | Value |
|---|---|
| Wall-clock (D2) | ~69.4 min (4,163,055 ms) |
| Tokens (subagent) | 395,811 |
| Tool uses | 142 |
| Iterations | 3 of 3 (cap reached) |
| persisted_early | yes (candidate_model.py + STL in iteration 1) |
| harness used | yes (build_iter1/2, coupon, measure, render receipts) |
| honesty | high — reported NOT_READY, flagged its own measurement gaps, no false pass |

## Gates — FAIL (O1 independently confirmed)

| Gate | Result | Detail |
|---|---|---|
| candidate_preflight_validation | **FAIL** (exit 1) | orchestrator re-ran → identical |
| S-01..S-04 support-audit | **FAIL** | 0.275094 mm² out-of-limit (64 faces) vs 0.000 required; down from 80.87 mm² (294× reduction). Residual = fillet-to-far-edge slivers, not a flat roof. |
| E-01 (grip ≥1.50) | FAIL | one sample 0.5735 mm |
| E-04 (bearing ≥0.80) | FAIL | one sample 0.5086 mm |

## Quality proxy — hidden scorer T2 (2 of 3 criticals)

| Critical | Result | Value |
|---|---|---|
| slot width 12.1–14.2 (bar 11.7) | **FAIL** | 16.9 mm — over-clearanced ~2 mm/side (functionally loose) |
| slot depth ≥23 (bar 24) | PASS | 25.0 mm |
| slot length ≥58 | PASS | 63.0 mm |

## Visual inspection (orchestrator looked at all renders)

- **Architecture correct**: open-bottom capture channel with a peaked self-supporting (≤45°)
  roof — the support-free method was implemented; the 0.275 mm² is slivers, not a flat ceiling.
- **Print orientation correct**: P_BED is the sole plate-touching face at printer Z=0; part
  laid on its side (bulky ~70×42 mm print footprint).
- **Fit**: X/length and Z/depth wrap the bar well (~0.5 mm/end, 25 mm depth); **Y/width is too
  loose** (channel too wide) — matches the scorer's width FAIL.

## Verdict for the sweep

Sonnet 5 followed the tightened process cleanly and honestly but did **not** converge to a
passing candidate within the ≤3-iteration cap: support residual, two edge misses, and an
over-loose Y fit. Per the locked rule it does **not** meet the D2 adoption bar (needs gate pass
→ V1 PASS → all criticals). Bounded honesty > false pass.
