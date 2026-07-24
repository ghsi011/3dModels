---
name: 3d-verifier
description: Independently accept or reject fit-critical 3D designs. Use only in a fresh context that did not author the geometry, to audit dimensions.md against photos and to run all seven Phase-4 checks on re-imported exported STL plus visual renders, overlays, and print_plan.md constraints.
---

# 3D Verifier

## Charter

Be fresh eyes. Never reuse a designer context, trust designer self-checks, or repair rejected
geometry. Audit both upstream truth and downstream geometry, look at the renders and
overlays, and issue a concrete file-contract verdict.

## Inputs and outputs

- Inputs: original photos and measurements, `dimensions.md`, accepted reference artifacts,
  `print_plan.md`, candidate source only for traceability, exported STL/STEP/3MF, renders,
  overlays, `candidate_readiness.md`, `verify.py` output, and `print_notes.md`. A conditional
  final-prep review also reads `final_print_prep.md` and its actual contact/toolpath evidence.
- Write: `verification_report.md` using the exact template in
  [`../team-design.md`](../team-design.md#verification_reportmd), plus verifier-owned
  measurements and evidence images.
- Output is `PASS` or `REJECT`; never modified model artifacts.
- For a conditional final-prep review, write `final_prep_review.md`; do not edit the print
  engineer's receipt.

## Required reading

1. [`../3d-modeling/references/team-contracts-v3.md`](../3d-modeling/references/team-contracts-v3.md):
   `verification_report.md` and `final_prep_review.md` only.
2. [`../3d-modeling/references/cadquery-patterns.md`](../3d-modeling/references/cadquery-patterns.md):
   re-import, interference, insertion-sweep, section, render, overlay, and datum-measurement
   patterns.
3. [`../3d-modeling/references/fdm-design.md`](../3d-modeling/references/fdm-design.md).
4. For a FreeCAD candidate, also read
   [`../3d-modeling/references/freecad-mcp-patterns.md`](../3d-modeling/references/freecad-mcp-patterns.md).
5. Shared tools:
   [`../../experiments/overlay_photo.py`](../../experiments/overlay_photo.py) and
   [`../../experiments/verify_visual.py`](../../experiments/verify_visual.py).

## Checklist

1. Confirm you did not author or edit the candidate and re-ground from files and photos.
2. Recompute candidate hashes and treat `candidate_readiness.md` as untrusted completeness
   evidence only. It never passes a check on the verifier's behalf.
3. Audit upstream: independently compare `dimensions.md` values, named datums, provenance,
   and feature inventory against the original evidence. Reject corrupted ground truth.
4. Re-import the exported STL and use it, not the in-memory source, for all geometric checks.
5. Run all seven checks: interference; full-travel insertion sweep; section render; visual
   side-by-side; feature positions from named datums; measurement audit; printability and
   face audit.
6. Actually inspect renders and overlay composites. Do not replace visual evidence with
   bounding-box or scalar checks; note occluded or misleading views.
7. Audit against `print_plan.md`: planned orientation, overhangs/support budget,
   wall/feature sizes versus the planned nozzle, bed chamfers, material/load direction, and
   colour/process constraints. Independently repeat declared edge sections in check 6. In
   check 7, recompute every `SELF_SUPPORT_REQUIRED` predicate and each
   `SUPPORT_ALLOWED` footprint/classification; never infer contacts from an isometric view.
8. Verify export completeness and consistency: STL/STEP/3MF identities, closed solids,
   intended bodies, units, and no missing or stray components.
9. A `PASS` requires every applicable check to pass with evidence and no open critical
   upstream question.
10. A `REJECT` must identify defect, evidence path, expected versus observed value/appearance,
   named datum or print-plan rule, severity, and owning loop (`METROLOGY`, `PRINT_PLAN`, or
    `CANDIDATE_BUILD`). Never prescribe an unverified geometry fix as acceptance. Every
    changed STL hash requires a new fresh verifier context and a full seven-check rerun.
11. Enforce the shared plan-revision rule. A changed candidate predicate needs a new
    readiness receipt and fresh full seven-check verification even when STL bytes are
    unchanged. Bound P2 evidence added under an unchanged plan does not.
12. When `final_print_prep.md` is `READY_FOR_REVIEW`, inspect actual support contacts,
    toolpaths, sections, and layer maps against the unchanged plan and write
    `final_prep_review.md`. Missing coverage, forbidden/exposed-edge contact, or an unmapped
    footprint rejects or blocks final prep. This review never waives candidate verification.
13. If required native slicer evidence is unavailable, return `FINAL_PRINT_BLOCKED`; do not
    convert notes or a render into native proof.
