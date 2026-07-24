# Round 4 preregistration — executable-gate T2-style rerun

## Decision

Run one fresh team-v4 arm against the unchanged synthetic T2-style common package frozen in
`experiments/round3-t2/common/`. Compare it with the already frozen/graded round-3 monolith
and team-v3 arms; do not spend another monolith context.

Skill snapshot: commit `ae30407`.

Common input hashes remain:

- `brief.md`: `e82b8a49c74797732abb795587ff57c4e29d6c647c832e944b0084d3c269ac26`
- `fixture_views.svg`: `495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c`

Every specialist uses `gpt-5.6-terra`, CadQuery only. FreeCAD is forbidden because another
session owns it. The arm may read the frozen common package, its v4 slice, slice-required
shared references, and preceding contracts only. It may not read round-3 arms/grading,
historical outputs/reports, the hidden scorer, tests, other experiments, or web content.

## Required normal path

```text
M1 dimensions
-> D1 blind reference
-> M2 overlay acceptance
-> P1 print plan + print_plan_checks.json
-> D2 candidate + shared support audit + complete candidate_preflight validation
-> V1 fresh all-seven verification + independent shared support audit
-> P2 real coupon + COMPLETE final print prep
```

The orchestrator advances on validated file receipts, not chat completion messages. Suggested
commission budgets are 3, 4, 3, 4, 9, 8, and 5 minutes respectively.

Evidence is differential:

- the verifier re-imports the canonical STL in place and never copies it;
- a rejection retains only report, metrics, hashes, and the defect-specific visual;
- unchanged full renders/exports are never copied into per-verifier folders; and
- one decisive blind-reference overlay and one candidate same-view overlay are sufficient
  when they show all critical features.

## Adoption thresholds

Keep v4 as the optimized default only if:

- functional/export hard gate passes;
- independent score is at least 90 and no lower than the round-3 team-v3 score by more than
  three points;
- all five role gates, blind overlay, actual visual verification, seven checks, and real
  coupon remain present;
- normal path is exactly seven specialist commissions, one fresh verifier, and zero
  correction loops;
- critical path is at most 35 minutes;
- delivered footprint is at most 35 non-cache files and 1,000,000 bytes;
- designer, orchestrator, and verifier independently obtain shared support-audit/receipt
  passes for the same final STL and complete Edge ID/support-rule sets; and
- token telemetry is reported only if exposed, never estimated from proxies.

Any quality or independence failure rejects v4. A time-only miss of at most 10% may be kept
with a documented performance caveat if commissions, loops, footprint, and quality all pass.
