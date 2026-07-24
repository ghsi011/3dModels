# Round 3 preregistration — T2-style export-integrity head-to-head

## Purpose

Test whether v3 preserves the team workflow's quality advantage while reducing time,
commissions, and artifact footprint. The task is deliberately smaller than Pixel 10 and
targets the historical source-to-export corruption class: a plausible source/self-check can
claim one slot width while the final STL contains another.

The original historical T2 participant photo package is not present in this checkout. This
round therefore uses a transparent synthetic caliper drawing built from the T2 fixture facts.
It is a T2-style regression, not a rerun of the original photo benchmark.

## Frozen arms

| Arm | Agent model | Skill | Allowed output |
|---|---|---|---|
| Monolith | `gpt-5.6-terra` | unchanged `skills/3d-modeling/` | `arms/monolith/` only |
| Team v3 | `gpt-5.6-terra` for orchestrator and every specialist | five slices at commit `33b6db7` | `arms/team-v3/` only |
| Grader | fresh `gpt-5.6-terra` after both arms freeze | hidden scorer plus this rubric | `grading/` only |

Both design arms start concurrently, use CadQuery only, and may read only `common/`, their
assigned skill, shared references named by that skill, and their own output. They may not read
the other arm, `experiments/scorer.py`, historical reports/outputs, tests, grader files, or
optimization artifacts. FreeCAD is forbidden because another session owns it.

## Team compact path

```text
M1 dimensions.md
-> D1 blind reference
-> M2 reference acceptance
-> P1 print_plan.md
-> D2 candidate + candidate_readiness.md
-> V1 fresh all-seven verification
-> P2 coupon + final_print_prep.md + print_notes.md
```

M2 and P1 may overlap after D1 when their file dependencies permit. `candidate_readiness.md`
must include the v3 edge inventory and support-sensitivity preflight. This support-free brief
must have zero out-of-limit region, so no conditional native-slicer review is expected.

## Independent 100-point rubric

| Category | Points |
|---|---:|
| Watertight/export/function hard gate | 35 |
| Hidden functional fit | 20 |
| Visual fidelity and usefulness | 15 |
| DFM/process, including support-free orientation and real coupon | 15 |
| Evidence and maintainability | 15 |

The hard gate requires one watertight intended tool body and all three T2 critical checks:
bar-slot width, engagement depth, and engagement length. A hard-gate failure caps the total
at 49.

## Adoption thresholds

Keep v3 only if all are true:

- hard functional/export gate passes;
- total score is at least 85 and not below the monolith arm;
- visual plus DFM is at least 22/30 and within two points of monolith;
- critical path is at most 30 minutes and at most 2× monolith;
- at most eight logged specialist commissions;
- one fresh verifier without correction, at most two after one real correction;
- at most one correction loop;
- at most 35 delivered files and 1,000,000 bytes excluding caches;
- readiness and the fresh verifier both measure the final exported slot, and hidden scoring
  confirms it; and
- all five role gates, actual visual inspection, and a real coupon are present.

If every quality threshold passes and only one time/footprint proxy misses by at most 10%,
run one identical repeat before deciding. Otherwise a miss triggers another skill refinement,
not a weakened acceptance gate.

Runtime token totals are reported only when telemetry exposes them. Commission count,
source/contract bytes, files, and output bytes are auditable proxies, never token estimates.
