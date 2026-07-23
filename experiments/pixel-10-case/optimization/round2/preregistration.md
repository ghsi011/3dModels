# Round 2 preregistration: compact/readiness v2

- Skill commit: `5833d67`
- Model: `gpt-5.6-terra` for orchestrator and every role.
- Backend: CadQuery only; FreeCAD remains occupied and out of scope.
- Input: the unchanged Pixel 10 `benchmark_brief.md` and common official evidence.
- Output: `optimization/round2/team-v2/`.
- Isolation: the run may not read baseline arms, baseline grading, hidden references, or
  optimization analysis. It sees only the current skills and frozen common input.

## Hypotheses

The final artifact must still receive an independent score of at least 88/100 and pass all
seven fresh-verifier checks on the re-imported exported STL. Compared with the baseline team
run, v2 targets:

- critical path at most 35 minutes (baseline 71m22s);
- at most eight logged commissions (baseline 15);
- one fresh verifier commission if designer readiness prevents avoidable defects;
- zero avoidable reference or verifier rejection loops;
- at most 43 delivered files and 2,068,316 bytes, excluding caches (50% below baseline);
- full designer/verifier separation and actual visual inspection;
- token count reported only if exposed; commission count and bytes remain labeled proxies.

Failure of a time/size target does not authorize weakening metrology ownership, the blind
reference round trip, the pre-design print plan, fresh independent verification, any of the
seven checks, or the physical coupon gate.
