# External review — prioritized backlog (PLAN ONLY, nothing applied)

Source: senior-engineering review of the team-version skill bundle (git `75211b2`), provided by
the user (`chatgpt-5.6-sol`). Per user decision: **produce a full prioritized plan and change
nothing** until approved. This document maps every finding + the 22 patches to sprints with
effort and experiment-impact flags. **No skill/contract/script has been edited.**

## Verification status of the review's key claims
- **R-01 (NaN passes the gate): CONFIRMED** — reproduced `validate-receipts` returning
  `PASS / errors:[]` for `samples_mm:[nan,nan,nan]`. Real false-pass.
- **R-02 (malformed 3MF written + "success"): plausible, not yet reproduced** — the writer does
  raw string XML interpolation and treats round-trip failure as non-fatal (matches the code
  shape); verify when we touch it.
- **R-03 (green tests overstate coverage): agrees** — our 5 preflight tests don't cover
  NaN/units/path-escape/reflected transforms/multi-component/etc.

## Framing
The review targets **production-acceptance authority**; our current program targets
**quality+speed optimization via real-part testing**. Both agree the team pipeline is a *guarded
pilot*, not production. Items below are tagged **Exp** when they affect our in-flight experiment's
validity, and **Prod** when they are production-hardening beyond the current optimization scope.

## Decisions locked (from this round)
- **H-03 → move fit ownership to the print engineer** (patch P-04). Metrologist records
  as-observed geometry + uncertainty only; print engineer owns fit class/band; designer combines.
  This **re-opens the just-promoted fit-band change** (currently in the metrologist slice), so it
  requires re-running the affected steps on ≥2 parts before re-promotion. Scheduled in Sprint 2.

## Alignment with our own findings (independent corroboration)
- C-03 / C-05 (support-audit ≠ supportability; no intended-contact model) = our round-5
  "executable gates ≠ functional correctness."
- H-01 (v4 adoption still a hypothesis; guarded rollout) = our not-yet-adopted stance.
- H-08 (FDM numbers profile-bound, not universal) = spirit of our fit-band work.

---

## Sprint 1 — release-blocking + cheap + protects experiment validity
| ID | Finding / patch | Effort | Exp/Prod | Notes |
|---|---|---|---|---|
| S1-1 | **C-02/P-10 — reject non-finite/negative samples & thresholds** | S | **Exp** | Verified bug; small `math.isfinite` guard + tests. Highest priority. |
| S1-2 | **C-03/P-12 — relabel `support-audit` → `orientation-screen`; state it does NOT prove supportability** | S | **Exp** | Honest claim; aligns with our finding. Keep it as an early hard-fail only for zero-allowed-downface rules. |
| S1-3 | **P-11 — validate transforms (finite rigid, det≈+1, no shear/reflection/scale) + contain evidence paths (no `..`/abs/symlink escape) + hash evidence** | S | **Exp** | Cheap robustness/security in `team_preflight.py`. |
| S1-4 | **C-01/P-01 — make `team-contracts-v4.md` sole normative; add "historical/non-normative" notice to `team-design.md`; relabel v1 "Exact template"** | S | **Exp** | Removes the split-authority ambiguity agents follow in good faith. |
| S1-5 | **H-01/P-02 — add explicit "team v4 = guarded pilot until adoption regression passes" note** | S | Prod | Matches reality; one paragraph in AGENTS.md. |
| S1-6 | **H-12/P-22 — adversarial test suite** (NaN/Inf, empty samples, min>max, reflected/scaled matrix, path escape, malformed JSON, wrong body count, non-watertight, multi-component, stale hash) | M | **Exp** | Turns S1-1..S1-3 into regressions; closes R-03. |

## Sprint 2 — engineering completeness (correctness the gates currently overstate)
| ID | Finding / patch | Effort | Exp/Prod | Notes |
|---|---|---|---|---|
| S2-1 | **H-03/P-04 — move fit ownership to print engineer** (decided) | M | **Exp** | Edit metrologist + print-eng + designer slices + contract; **re-test on ≥2 parts** before re-promote. |
| S2-2 | **C-06/P-08 — artifact manifest (units, per-part hashes, transforms, body count) + unit/25.4× scale hard-reject** | M–L | **Exp** | The unit-scale check alone is cheap + high-value; full manifest supports multi-part. |
| S2-3 | **C-05/P-06,P-07 — intended-contact + motion-path contracts; replace "≈zero intersection"/linear-sweep verifier checks** | L | Prod | Foundational for press/snap/thread/hinge/seal; directly fixes our meta-finding. Big. |
| S2-4 | **C-07/P-03 — risk classification gate (R0–R3) in orchestrator; prohibit autonomous safety acceptance** | M | Prod | Safety; blocks "ready for use" claims on high-consequence parts. |
| S2-5 | **H-04/P-05 — provisional→frozen orientation stages** | S–M | Prod | Avoids locking a bad orientation before feasibility. |
| S2-6 | **H-06/P-14 — separate raw audit mesh from normalized (mesh_io); mutation log; never silently repair a fail→pass** | S–M | **Exp** | Makes the verifier's "exact exported STL" claim true. |
| S2-7 | **C-08/P-13 — resource governor** (mem/CPU/triangle/log caps + fallback) | M–L | Prod | Partly covered by our `cad_runner.py` (timeout+mem); extend to renderer/mesher/booleans + `run_cadquery_model.py`. |
| S2-8 | **H-02/P-09 — one canonical machine-readable contract; generate/validate Markdown against it** | M | Prod | Fixes MD/JSON drift; hash MD+JSON+schema+generator together. |

## Sprint 3 — hardening, portability, validation
| ID | Finding / patch | Effort | Exp/Prod | Notes |
|---|---|---|---|---|
| S3-1 | **C-04/P-17 — rewrite `make_3mf.py` fail-closed (XML lib, validate package, atomic write, fatal round-trip)** | M | Prod | Not on our current path; delivery-corruption risk. |
| S3-2 | **H-07/P-18 — reclassify `make_bambu_3mf.py` as versioned adapter; deterministic IDs; fail-closed mapping; native smoke test** | L | Prod | Machine/version-specific fixture, not a generic writer. |
| S3-3 | **H-08/P-19 — mark FDM/material numbers as profile-bound starting points; require profile ID + coupon for fit/process gates** | M | Prod | Reference-material relabel across fdm-design/materials/preflight-checklist. |
| S3-4 | **H-05/P-15 — camera calibration classes; orthographic/calibrated overlay only for metric claims** | M–L | Prod | Metrologist + `preview.py`. |
| S3-5 | **Printer/material profile schema (printers.md/materials.md versioned + sourced); resolve aux-nozzle fiber-filled conflict** | M | Prod | "accepted profile governs, not last-read file." |
| S3-6 | **Golden-fixture library + frozen clean v4 regression** (clearance/press/snap/helical/mirror/unit-error/multi-part/support-contact) | L | Prod | The review's validation sprint; also our own adoption evidence. |

## Medium/Low backlog (batch when convenient)
M-01 feature criticality classes · M-02 Notion/git → optional adapters (P-20) · M-03 "five roles"
as design choice not invariant · M-04 dedupe FDM rule tables · M-05 pin solo-mode to a tested
reference revision · M-06 recovery-action error messages · M-07 per-stage cost/latency gates ·
M-08 downloaded-model license/provenance · M-09 dependency/environment lock · M-10/P-21 structured
post-print results contract · H-09 runtime blindness/write-authority enforcement · H-10 atomic
writes/crash recovery · H-11 derive evidence from canonical artifacts.

## Recommended order (my suggestion, for your approval)
1. **Sprint 1 in full** — cheap, protects the experiment we're running now, closes the confirmed
   false-pass. ~1 focused session.
2. **S2-1 (H-03 fit move)** next, since it re-opens a just-promoted change and should settle before
   more part-by-part optimization.
3. **S2-2 unit-scale check + S2-6 mesh raw/normalized** — cheap slices of larger items, high value.
4. Then decide Sprint 2/3 depth based on whether the goal stays "optimize" or shifts toward
   "production acceptance."

**Nothing above is applied.** On approval (whole plan, a sprint, or individual IDs) I'll implement
with the anti-overfit gates (general edits, re-test on ≥2 parts, scorer/editor separation).
