# 3D-modeling skill optimization — summary (real-part program)

Evidence-backed summary of the optimization run on real printed parts (Pixel 7 case, Garmin 7X
dock, broom holder) with the user's final 3MFs / reference model as held-out oracles. Full
per-step scores + method are in `optimization_log.md`; the external-review plan is in
`implementation-plan.md` / `external-review-backlog.md`.

## Method (validated)
Real parts with **held-out** ground truth (3MF answer + downloaded reference model); agents run
**blind** (photos + calipers + public specs only); orchestrator scores each **single pipeline
step** against the oracle; skill fixes are **general CAD/DFM principles**, promoted only after
re-test on ≥1 different part with **no regression** (anti-overfit gate); scorer/editor separated;
firewall enforced (a real leak was caught and discarded). Token telemetry IS exposed for Claude
subagents (measured, not estimated).

## Skill fixes made + validation
| Fix | Where | Validated |
|---|---|---|
| **Fit = bounded band, not a floor** (over-clearance is a failure) | metrologist + print-engineer slices + `team-contracts-v4.md` | Pixel ① ③, Garmin ① ③, Broom ① (grip/interference), and **propagated to Pixel-case geometry at 0.20 mm/side, in-band** ④. 3 parts / 3 fit types, zero regression. |
| **Support-free = default, not absolute** (function/fit wins over support-purity) | print-engineer slice + contract | Garmin ③ dock: bounded support confined to the lip's *nonfunctional* face — the exact opposite of round-5's fit-distorting gable. Hardest test passed. |
| **Measure envelopes at flat regions** (near-feature caliper reads are biased) | metrologist slice | Garmin ① rejected a 56.8 mm over-the-buttons read; kept the flat-bezel 51.75 mm. |

## Key measured results (blind vs oracle)
- **Metrology** reconstructs to sub-0.5 mm from photos+calipers (Pixel 155.6/73.2/11.44 vs
  155.61/73.56/11.46; Garmin case 51.75 mm — a true Fenix 7X, correctly overriding a wrong spec
  hint by evidence rank).
- **Blind reference build** works (Pixel phone, Garmin watch to-spec; honest about unmodeled
  unknowns — no confabulated caseback contacts).
- **Print plan** carries the bounded band + applies the support principle correctly, and blocks
  honestly when evidence is missing (Garmin charge interface).
- **Design step ④ is the hardest and weakest link.** Pixel case NOT_READY: fit is right (band
  propagated), but achieving snug + support-free + camera-relieved geometry is genuinely hard,
  and the support-audit tool over-flags (45° chamfer faces) — see meta-finding.

## Meta-findings
1. **Executable designer gates ≠ functional correctness** (round-5 + Pixel ④, and independently
   corroborated by the external review C-03/C-05). The support-audit is a crude downward-normal
   screen, not a supportability proof; a valid 45° chamfer trips it. → honestly relabeled in
   Sprint 1; a real contact/motion model is deferred (backlog C-05).
2. **The problem, not the model, is the bottleneck** on hard geometry: both Sonnet and Opus spent
   ~1 h on the round-5 support-free channel. Opus is stronger on hard geometry but failed twice on
   process (wander / output-cap) until guarded; Sonnet is process-reliable and honest. Verifier
   should stay strong (Opus); deterministic stages go fast (Sonnet).
3. **Downloaded "reference models" can be coarse** (the Pixel 7 model is a uniform-thickness
   shell — the blind reconstruction was more accurate). Always validate oracle validity first
   (done for the Garmin dock: it fits a 51 mm 7X).
4. **Provenance/hash discipline matters** — Pixel ④ failed partly on stale audit hashes (STL
   changed after audits), exactly what the new `team_tools` auto-hash/binding prevents.

## Automation added (Sprint 1A)
`team_tools` deterministic contract layer (validate/hash/status/render + artifact-manifest,
68 tests): auto-SHA-256 + revision binding (no agent-entered hashes), stale-dependency detection,
finite-number/enum/ID/FK/path-safety validation, 25.4× unit-scale check, agent-facing summary —
moving clerical work off the agents. Passing it is *necessary evidence, not proof of correctness.*

## Gate hardening (Sprint 1)
Closed a confirmed **NaN/±Inf/None false-pass** and a **`float(None)` crash**; added finite-rigid
transform validation + evidence-path containment; honestly relabeled the support screen. 33 tests,
no regression on valid data.

## Adoption posture
Team v4 remains a **guarded pilot** (now stated in AGENTS.md). The two spec fixes are adopted
(validated across parts). The design step and the deferred contact/motion model are the next
quality frontier. Deployment note: the optimized repo skill is not yet the registered/invocable
one — install it as the registered skill before real use.
