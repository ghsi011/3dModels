---
name: 3d-orchestrator
description: Route and govern 3D-printable modeling jobs. Use for new modeling or print-prep requests to choose solo monolith versus the five-role file-contract pipeline, enforce phase gates, dispatch specialists, maintain job state, and deliver verified artifacts without authoring geometry.
---

# 3D Orchestrator

## Charter

Own routing, job state, phase gates, user questions, specialist dispatch, project/queue
housekeeping, and delivery. Never write or edit geometric source, STL, STEP, or 3MF content.
Specialists communicate through project files and source photos only, never chat summaries.

## Inputs and outputs

- Inputs: the user request, photos and measurements, repository state, printer constraints,
  and every current contract artifact in the project folder.
- Write: `job_state.md` using the exact schema in
  [`../team-design.md`](../team-design.md#job-statemd).
- Read and gate: `dimensions.md`, `print_plan.md`, `verification_report.md`, designer
  outputs, and final print-prep files.
- Housekeeping: the Notion Print Queue entry and physical-change git commits required by
  repository policy.
- Never substitute a chat summary for a contract. Before every dispatch, tell the agent to
  read the named files from disk.

## Required reading

1. [`../3d-modeling/references/team-contracts-v2.md`](../3d-modeling/references/team-contracts-v2.md).
2. For a solo job only, read and run [`../3d-modeling/SKILL.md`](../3d-modeling/SKILL.md)
   unchanged.

## Checklist

1. Create the project folder and compact `job_state.md`; create/update the Print Queue
   entry. Use `COMPACT` unless multi-part/moving/high-consequence work requires `FULL`.
2. Route to **solo** only when the part is simple, single-part, non-fit-critical, has no
   recreated mating geometry, and does not merit independent visual verification.
3. Route to **pipeline** when any condition holds: fit or datum criticality, recreated
   geometry from photos, multiple parts, mating or moving interfaces, safety/thermal/load
   consequences, multi-colour alignment, difficult DFM, or user-requested team/fresh review.
4. In pipeline mode, advance only through:
   `INTAKE -> METROLOGY -> REFERENCE_BUILD -> REFERENCE_ACCEPTANCE -> PRINT_PLAN ->
   CANDIDATE_BUILD -> INDEPENDENT_VERIFICATION -> PRINT_PREP -> DELIVERY`.
5. Dispatch the metrologist to create `dimensions.md`; gate on complete datum/provenance,
   confidence grades, resolved blockers, and one blind-build-completeness row for every
   visible feature before spending a reference build.
6. Dispatch one designer with the **reference** commission. Then dispatch the metrologist
   again to overlay-accept it. A failure returns to `METROLOGY`: fix the sheet, not the
   reference model.
7. Dispatch the print engineer for the pre-design `print_plan.md`; gate on orientation,
   material, nozzle-linked limits, support budget, chamfers, and colour constraints.
8. Dispatch candidate designer(s) against the sheet, accepted reference, and print plan.
   Require a hash-bound `candidate_readiness.md` with `status: READY` from the exported STL
   before verifier dispatch. `NOT_READY` remains inside the same designer commission. Only
   CadQuery candidates may run in parallel. Serialize all FreeCAD work through one instance.
9. Dispatch a fresh verifier that was never a designer and has no candidate-author history.
   Treat designer readiness as untrusted and require all seven checks. A `REJECT` returns to
   `CANDIDATE_BUILD` with the concrete defect list; never ask the verifier to fix it.
10. After `PASS`, dispatch the print engineer for coupon, slicing, print order, and field
    test details. Return a failed physical test to the owning upstream contract.
11. Deliver only when the exported/re-imported artifacts pass all gates, the queue is
    current, and the meaningful physical iteration is committed.
12. Advance from a commission as soon as its required file receipt is complete and valid;
    do not wait for a chat summary. Record a realistic minute budget per dispatch and ask
    for an exact blocker when it expires.

If this skill is loaded inside an agent runtime that cannot spawn nested subagents, keep the
orchestrator in the main session (or launch it as a top-level agent) and dispatch specialists
from there.
