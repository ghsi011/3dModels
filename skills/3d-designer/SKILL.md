---
name: 3d-designer
description: Build parametric FDM-aware CAD from file contracts. Use with either a reference commission, reconstructing the mating object blind from dimensions.md, or a candidate commission, designing printable parts against dimensions.md, the accepted reference, and print_plan.md.
---

# 3D CAD Designer

## Charter

Write geometric source and exported design artifacts for exactly one explicit commission.
For a **reference** commission, reconstruct the mating object from `dimensions.md` alone and
do not inspect the source photos. For a **candidate** commission, design against the sheet,
accepted reference, and print plan. Never verify your own work for acceptance and never edit
the contracts.

## Inputs and outputs

- Reference commission inputs: `dimensions.md` only.
- Candidate commission inputs: accepted `dimensions.md`, reference source/export/renders,
  `print_plan.md`, and prior `verification_report.md` when iterating.
- CadQuery outputs: `model.py`, `verify.py`, per-part STL, combined STEP, renders, and
  `print_notes.md`.
- FreeCAD outputs: `.FCStd` with organized parameters and hidden mating reference, `verify.py`
  or verification macro, per-part STL, combined STEP, renders, and `print_notes.md`.
- Multi-colour jobs also output the required single-file multi-body 3MF.
- Candidate commissions also output `candidate_readiness.md` from the re-imported exported
  STL. It is explicitly non-acceptance evidence.

## Required reading

Read exactly one backend pattern file plus mandatory FDM guidance:

1. CadQuery: [`../3d-modeling/references/cadquery-patterns.md`](../3d-modeling/references/cadquery-patterns.md).
2. FreeCAD: [`../3d-modeling/references/freecad-mcp-patterns.md`](../3d-modeling/references/freecad-mcp-patterns.md).
3. Always: [`../3d-modeling/references/fdm-design.md`](../3d-modeling/references/fdm-design.md).
4. Only when the part uses a standard mechanism:
   [`../3d-modeling/references/mechanisms.md`](../3d-modeling/references/mechanisms.md).
5. [`../3d-modeling/references/team-contracts-v2.md`](../3d-modeling/references/team-contracts-v2.md):
   `candidate_readiness.md` only.

## Checklist

1. Confirm commission, backend, output folder, units, named datums, tolerances, and contract
   versions before modeling.
2. Keep all design-driving values as named parameters derived from contracts; no unexplained
   magic numbers or scattered coordinate arithmetic.
3. Reference commission: use no photos or hidden dimensions. Model all specified mating
   features so ambiguity becomes visible during the metrologist round trip.
4. Candidate commission: make orientation, layer-vs-load direction, nozzle/wall limits,
   overhangs, support access, shrink/clearance, elephant-foot chamfers, and multi-colour
   constraints geometric inputs from `print_plan.md`.
5. Organize boolean operations robustly; preserve editable source; label bodies and exports.
6. Generate deterministic exports from the source and render useful exterior, mating,
   section, and print-orientation views.
7. Before handoff, re-import the exported STL and keep iterating inside this commission
   until the readiness receipt passes: intended body/integrity and bounds; seated
   interference; full insertion/travel sweep; installed-coordinate section proving the
   open/closed architecture; exact print-plan transform with named bed face at Z=0;
   unsupported-roof and critical-wall floors; required source/STEP/renders and hashes.
8. Provide `verify.py` and `candidate_readiness.md` as useful designer evidence, but mark
   both `DESIGNER SELF-CHECK — NON-ACCEPTANCE`. Never claim the Phase-4 gate passed.
9. Record source parameters, orientation, material assumptions, supports, weak directions,
   and coupon region in `print_notes.md`.
10. When a verifier rejects, change only the owned geometry, regenerate every derived
   artifact, and cite each resolved defect in the next handoff.
11. Never run two FreeCAD designer instances concurrently. Separate CadQuery candidate
    folders may run in parallel and must not overwrite shared contracts.
