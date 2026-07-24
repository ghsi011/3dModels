# Round 5 — D2 model sweep, head-to-head (build123d, tightened commission)

Sweep start 2026-07-24T14:50:40Z. Both arms: identical frozen inputs, build123d backend,
harness, ≤3-iteration cap. Only the designer model differs. Token telemetry **is** exposed for
Claude subagents (measured, not estimated). Orchestrator (O1) independently reproduced every
gate result; hidden scorer T2 and renders inspected by the orchestrator.

## Results

| | Arm S — Sonnet 5 | Arm O — Opus 4.8 (attempt 2) | Reference: round-3 team-v3 |
|---|---|---|---|
| D2 result | **NOT_READY** (honest) | **READY** | delivered (93/100) |
| Executable gates (edges+supports+receipts) | **FAIL** — supports 0.275 mm²; E-01, E-04 short | **PASS** — supports 0.000 mm²; all edges | pass |
| Hidden functional scorer (T2 criticals) | **2/3** — width 16.9 FAIL; depth 25.0 ✓; length 63.0 ✓ | **1/3** — width 15.5 FAIL; depth 22.4 FAIL; length 63.2 ✓ | **3/3** |
| Fit character | too loose in Y (over-clearanced) | too loose **and** shallow — asymmetric +Y gable roof compromised the snug capture | snug |
| Attempts | 1 (clean process) | 2 (attempt 1 failed: ~64 min wander, 0 files, output-token cap) | n/a |
| Wall-clock | ~69.4 min | ~53.8 min (attempt 2); +~64 min wasted on attempt 1 | 74 min (3 loops) |
| Tokens (measured) | 395,811 | 259,365 (attempt 2) | not exposed (Terra) |
| Tool uses | 142 | 72 | n/a |
| STL size | 60 KB | **2.56 MB** (51,288 faces — over-tessellated) | n/a |
| Honesty | high (NOT_READY, flagged gaps) | high (flagged 0.317 mm gap) | n/a |
| persisted_early / harness | yes / yes | yes / yes (after mitigation) | n/a |

## Preregistered decision (applied without change)

- Adopt Sonnet 5 for D2 **iff** it passes gates + V1 PASS + all criticals + faster. Sonnet
  **failed its gates** → the locked rule says **keep Opus for D2**. But Opus's candidate
  **fails the hidden functional fit (2/3)**, so "keep Opus" is a hollow win — see meta-finding.

## Meta-findings (the real value of this round)

1. **Executable gates ≠ functional correctness.** Opus passed *every* designer-side executable
   gate (edges, supports, receipts) yet is functionally **worse** than Sonnet on the hidden fit
   (1/3 vs 2/3). Optimizing hard for the zero-support gate produced an asymmetric +Y gable that
   loosened and shortened the bar capture. The gates guarantee printability/edges, **not** a
   snug fit. This challenges the core v3/v4 thesis that executable designer gates make the part
   right — they make it *printable and gate-clean*, not *correct*.
2. **Both models over-clearanced.** The plan states a clearance **floor** (≥0.30 mm/side) and
   "designer may increase" — with no **upper** bound. Blind to the tight fit target, both arms
   loosened too much (16.9 / 15.5 mm vs the 12.1–14.2 window). Fix is a metrology/plan change:
   specify a clearance *band*, not just a minimum.
3. **The zero-support requirement distorts the fit.** Achieving 0.000 mm² via roofs/gables
   (Opus's asymmetric gable especially) trades away snug capture. The support-free constraint
   may be over-strict for this functional tool; a different orientation or minimal support could
   give a far better fit.
4. **Model tradeoff on the hard commission:** Sonnet = process-reliable (1 clean, honest run)
   but didn't converge; Opus = needed the persist-early/output-hygiene mitigation (attempt 1
   failed outright), then produced a gate-clean but functionally-flawed part faster/cheaper.
5. **Neither matched round-3 quality.** team-v3 passed 3/3 criticals; neither round-5 arm does.
   The tightened commission + build123d + ≤3 cap did not reach the prior quality bar on this
   hard part — the cap and the spec gaps (2,3) are the likely causes, not just the model.

## Process wins that held

- The harness prevented silent stalls: every build bounded (max ~7 s), no timeout/memory breach.
- build123d worked cleanly and its output plugged into the trimesh/CadQuery/scorer stack with
  zero changes; system CadQuery untouched.
- persist-early + iteration cap worked once enforced (Opus attempt 2); Opus attempt 1 shows the
  guardrails must be **in the prompt**, not just the commission file.
