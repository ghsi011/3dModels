# CAD-agent skill experiment — final report

**Question:** does the 3d-freecad skill (or its CadQuery variant) beat an unassisted agent
at turning a realistic request (photos + caliper numbers + prose) into a printable,
functional part — and at what cost?

**Design:** 4 ground-truth tests × 3 arms = 12 blind runs. Ground truth = real published
models (2 picked by Idan, 2 downloaded from MakerWorld) that agents never saw; prompts
contained only what a real user would supply (description, caliper diagrams, product
photos, real phone photos). Scoring by a geometric probe suite **calibrated so every
reference model passes its own spec** (this calibration caught 3 probe bugs and one
over-strict check before they contaminated results). T1–T2 ran on fable, T3–T4 on Opus 4.8
— compare arms within a test, not across tests. n=1 per cell: treat <15-point fit deltas
as noise.

## Results

| test | arm | success | fit | printability | judge/10 | tokens | tools | min |
|---|---|---|---|---|---|---|---|---|
| T1 broom clip | control | ✅ | 100 | 100 | 7.0 | 86k | 19 | 15 |
| T1 | cadquery | ✅ | 100 | 100 | 8.5 | 135k | 24 | 21 |
| T1 | freecad | ✅ | 100 | 100 | 8.5 | 484k | 44 | 14 |
| T2 filter tool | control | ✅ | 100 | 100 | 7.5 | 54k | 26 | 7 |
| T2 | cadquery | ❌ | 75 | 100 | 4.0 | 126k | 37 | 19 |
| T2 | freecad | ✅ | 100 | 100 | 9.0 | 514k | 40 | 21 |
| T3 X2D tray | control | ✅ | 100 | 100 | 7.0 | 56k | 11 | 7 |
| T3 | cadquery | ✅ | 89 | 100 | 8.0 | 93k | 22 | 12 |
| T3 | freecad | ✅ | 100 | 100 | 8.5 | 299k | 24 | 14 |
| T4 Pixel case | control | ✅ | 88 | 93 | 7.5 | 71k | 18 | 10 |
| T4 | cadquery | ✅ | 88 | 93 | 9.0 | 151k | 45 | 22 |
| T4 | freecad | ✅ | 88 | 93 | 8.0 | 402k | 27 | 14 |

| arm | success | avg fit | avg judge | total tokens | avg min/run |
|---|---|---|---|---|---|
| control | **4/4** | 97 | 7.2 | **266k** | 9.8 |
| cadquery | 3/4 | 88 | 7.4 | 505k | 18.5 |
| freecad | **4/4** | 97 | **8.5** | 1698k | 15.8 |

(T4: all arms lose the same 12 pts to a USB-probe limitation of the scorer; visual check
confirms all three cases have USB/speaker cutouts. Treat T4 as a three-way pass.)

## Conclusions

1. **Function isn't where the skill earns its keep — polish and resilience are.** The
   unassisted control passed every test at 1/2 to 1/6 the token cost: current models can
   already design simple-to-medium functional parts. What the skill arms consistently
   added: grip ribs (creep-safe retention), elephant-foot chamfers, teardrop holes,
   lead-in flares, parametrized fix tables ("if it's tight, change this one number"),
   printed-coupon suggestions, and honest risk notes. The judge gap (8.5 vs 7.2) is
   exactly the gap between "prints and works" and "feels engineered" — and it's where the
   next print iteration gets cheap.

2. **The one real failure produced the best lesson.** T2-cadquery's slot measured 12.5 in
   its self-verification but 15.4 in the exported STL — a late chamfer workaround widened
   it after the checks ran. **Phase 4 must verify the exported artifact, not the in-memory
   model.** Now written into both skills. (Also observed and now documented: OCC fillets
   silently corrupting scalloped solids; OCC exact-volume misreporting on periodic
   splines.)

3. **The FreeCAD arm is the quality leader and the cost outlier.** Best judge score on 3
   of 4 tests, 4/4 success — at ~425k tokens/run, dominated by the viewport screenshot
   every `execute_code` returns. The skill now instructs ≤8 large chunks per job; a
   no-screenshot execution mode in the FreeCAD MCP would be the single biggest win.

4. **CadQuery variant is the best cost/quality frontier when it works** (cloud-only, no
   desktop dependency, previews included) but showed the only defect and scored mid-pack
   on probes. Its strength: T4, where it alone caught the front/back mirroring trap in
   camera placement and padded uncertain dimensions deliberately.

5. **Where all arms were weakest:** dimensions the prompt left fuzzy (button positions
   estimated from a generic side photo) — every arm padded and disclaimed, none asked-by-
   proxy (e.g., offering two variants). A future skill idea: when a fit-critical number is
   a guess, ship the coupon/variant automatically.

## Verdict
By the stated formula (least time/work × highest quality): **control wins on cost,
freecad wins on quality, and the honest answer is the skill's value scales with part
difficulty and iteration count.** For one-shot simple parts, skip the skill. For fit
parts you'll iterate on physical hardware — the user's actual project profile — the
freecad skill's params + verification + notes pay for themselves the first time a print
doesn't fit. Immediate roadmap: cut FreeCAD screenshot cost, keep the export-verification
rule, re-run T2/T4 after fixes to confirm the cadquery defect class is closed.

---

# Redo under grading v2 (2026-07-23)

After the verification overhaul (verification_postmortem.md; protocol.md "Grading
procedure v2"), the T3/T4 cells were redone. Grading now requires: side-by-side
composite viewed and described, layout IoU + boundary-F1 vs the reference, and
position checks from named datums. Skill arms use the combined **3d-modeling** skill.
All redo runs on Opus; freecad arms pending (desktop offline at run time).

## Two prompt bugs found and owned
1. **T3 v1** described rectangles the photos didn't show (known).
2. **T4** told agents the camera center is "37 mm from the top edge" — a
   frame-contaminated number. Truth (from the reference): **24 mm**. The v2 prompt fixed
   the height but then mis-stated the side ("9 mm right as you look at the back" —
   should be LEFT, matching the photo). Both v2 arms followed the text, flagged the
   photo/text ambiguity as their #1 risk, and shipped a one-line fix parameter.
   **Lesson: agents execute the spec they're given with ~0.5 mm precision — datum
   quality, not modeling skill, was the binding constraint in both failures.**

## Results (layout IoU / boundary-F1 / camera Δ where applicable)

| cell | scorer | layout | verdict | notes |
|---|---|---|---|---|
| T3 v1 control | pass | 0.40 / 0.31 | **MISMATCH** | rectangles-for-silhouettes |
| T3 v1 cadquery | pass | 0.39 / 0.35 | **MISMATCH** | " |
| T3 v1 freecad | pass | 0.36 / 0.29 | **MISMATCH** | " |
| T3v2 control | fit 67 (6 pockets) | 0.59 / 0.47 | **PARTIAL** | right character, rows shifted |
| T3v2 cadquery (old skill) | pass | 0.43 / 0.36 | **MISMATCH** | false mirror-symmetry assumption |
| T3v2 cadquery (combined skill) | pass | 0.59 / **0.58** | **PARTIAL** — best shape fidelity of all six | pixel-mapped pockets; triplets/notch on correct side |
| T4 v1 all arms | pass | — | **POSITION FAIL** | Δ≈(−6..−13, +15.5): followed the bad 37 mm datum |
| T4v2 control | pass | 0.39 / 0.23 | POSITION FAIL Δx −18.1 | wrong side per prompt text; flagged it |
| T4v2 cadquery (combined) | pass | 0.39 / 0.23 | POSITION FAIL Δx −18.1 | same; Δy now +0.5 (height datum fixed) |
| T4v2 control **+ own 1-line fix** | pass | 0.89 / 0.78 | **MATCH**, camera Δ(−0.1, +0.6) | fix cost: 1 line, 0 tokens |
| T4v2 cadquery **+ own 1-line fix** | pass | 0.90 / 0.78 | **MATCH**, camera Δ(−0.1, +0.5) | " |

Agentic cost (redo runs): T4v2 control 76k/15 tools/13 min · T4v2 cadquery 166k/52/24 min ·
T3v2 cadquery-combined 149k/67/24 min (full ledger: runs/agentic.csv).

## What the redo established
1. **The combined skill's visual-verification phase measurably improves recreation
   fidelity**: same task, same model, same photos — old skill 0.43/0.36 (false symmetry
   shortcut), combined skill 0.59/0.58 with correct handedness on every asymmetric
   feature. Control without a skill: PARTIAL but only 6 of 10 pockets.
2. **Both T4v2 arms park within 0.5 mm of every numeric datum they're given** — and both
   independently flagged the one ambiguous datum and parametrized it so the fix cost one
   line. That's the skill's "failed fit = one-parameter fix" promise working end-to-end
   (control, notably, did the same without the skill — Opus parametrizes by default).
3. **The verifier earns its keep on its own output too**: during the redo it caught its
   coordinate-frame bug (to_2D re-origining) and a rim-slice artifact that had inverted
   the T3 ranking — both found because a human-readable composite made wrong numbers
   look wrong. Numbers alone had passed both.
4. ~~Pocket positions drift 3-8 mm~~ — **RETRACTED, and the retraction is the finding.**
   The render-over-photo overlay (below) showed the best candidate's pocket positions
   were essentially correct all along (boundaries land 0.39 mm mean from the photo's
   features; the reference's own render lands 0.15 mm). The 0.59 IoU came from pocket-
   mouth chamfer widths, corner treatment, and a raised-end vertical architecture the
   candidate had missed — architecture differences, not position drift. My earlier
   claim came from eyeballing composites; the overlay measured it.

## Render-over-photo overlay loop (tried 2026-07-23, works)

Technique: segment the part in a near-orthographic photo, map the model's slice
boundaries into photo pixels, draw them ON the photo, look, adjust parameters, repeat.
Photo-only discipline (the scoring reference never enters the loop).

- Iteration 0 audit: refuted the drift claim above and localized the true gaps
  (mouth chamfers ~1.4 mm, low body + raised ramped ends with U-dips, corner posts).
- Iteration 1 (all photo-derived: chamfer rings from the top photo, end architecture
  from the iso photo): layout IoU 0.594 → **0.697**, boundary-F1 0.575 → **0.676** —
  from a hair under the MATCH bar (0.70) vs 0.55-0.58 for every agent arm. Cost: two
  script edits, zero agent tokens.
- Iteration 2 (dip depth, from comparing my iso render to their iso photo): improves
  the side view; top-projection metrics unchanged — a measured limit of the metric,
  noted.
- Caveat found: a mean-distance-to-nearest-edge residual is too forgiving to decide
  with (busy photos put SOME edge near any line) — the overlay image decides, the
  number only trends.
- Folded into the skill: cadquery-patterns.md §"Render-over-photo overlay loop" +
  Phase 2 pointer. Tool: experiments/overlay_photo.py.

## Pending
- T3v2 + T4v2 freecad arms (desktop/FreeCAD offline at redo time — same prompts, queued).
- Design-judge re-scoring of redo runs (blind, with reference shown this time).

## Artifacts
- runs/: all outputs + score.json + renders · scorer.py (calibrated) · protocol.md
- verify/: side-by-side composites + verify.json per run · verify_visual.py
- prompts/: benchmark packages (T4 datum corrected; change log in T3v2 prompt file)
- tests/: ground truth · Updated skills: 3d-modeling v1 (combined; supersedes both)
