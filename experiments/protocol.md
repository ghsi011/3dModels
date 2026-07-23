# CAD-agent skill experiment — protocol

## Question
Does the 3d-freecad skill (and its CadQuery variant) improve an agent's ability to turn a
realistic user request (photos + caliper numbers + prose) into a printable, functional part?

## Arms (identical prompt package; only tooling mandate differs)
- **control** — same environment briefing, explicitly no skills. Baseline.
- **freecad** — must follow /home/user/skills/3d-freecad (FreeCAD MCP on user machine).
- **cadquery** — must follow /home/user/skills/3d-cadquery (code-first, cloud).

## Tests (ground truth = real published/purchased models, never shown to agents)
| id | job | source of truth | difficulty |
|---|---|---|---|
| T1 | broom-handle wall clip (Ø25 handle, 1 screw) | MakerWorld Eneo3D clip | easy-med |
| T2 | washer fluff-filter opening tool (Ø63 cap, 11.7 bar) | MakerWorld Gorilla Labs tool | medium |
| T3 | X2D toolbox organizer tray insert (101×165.5×25.6) | user's toolbox model | med-hard |
| T4 | Pixel 9a phone case (154.7×73.3×8.9 + cutouts) | user's downloaded case | hard |

Prompt packages in prompts/T*/: prompt.md + caliper diagrams + product photos (+ real
phone photos for T4). Reference STLs live only in tests/ — agents are never pointed there.

## Metrics
- **success** (binary): watertight AND all CRITICAL functional checks pass (scorer.py;
  calibrated so each reference model passes its own spec).
- **fit_score** 0-100: weighted pass-rate of functional checks (critical ×2).
- **printability** 0-100: overhang/watertight-based (scorer) — proxy for "slices cleanly".
- **design_judge** 0-10: manual rubric at analysis time (chamfers/orientation/DFM
  features/spirit-of-request), judged blind on renders before unblinding arms.
- **agentic cost**: subagent_tokens, tool_uses, duration_ms from the Agent harness.

## Procedure
Per test: run control + cadquery in parallel (independent toolchains), then freecad alone
(exclusive owner of the FreeCAD instance). One repetition per cell (n=1 pilot; note
variance caveat). Outputs land in runs/<test>_<arm>/; scorer runs after each arm; renders
generated for judging. No mid-run coaching — agents get one prompt, zero follow-ups.

## Grading procedure v2 (after the T3/T4 verification failure — see verification_postmortem.md)

The v1 pipeline scored sizes but not positions/layout and never forced a human-style look.
v2 adds a mandatory visual + layout stage; **no run may be graded from scorer.py alone.**

1. **verify_visual.py ref cand out [--test Tn]** runs for every candidate. It renders
   reference and candidate from IDENTICAL cameras (top/front/iso) into one composite,
   plus slice overlays and a projected-pocket overlay (red=ref, blue=cand, dark=match).
2. **The grader must open the composite and describe both rows** (features seen in ref,
   features seen in cand, differences) BEFORE recording any score. The description goes
   in the run's score notes. No look, no grade.
3. **Layout metrics** (all calibrated: reference-vs-itself = 1.0):
   - layout IoU — projected-cavity overlap after best-of-4-rotation alignment (position/coverage)
   - boundary-F1 (1.5 mm tol) — do pocket OUTLINES coincide (shape detail; punishes
     rectangle-for-silhouette substitutions that area IoU forgives)
   - verdict: MATCH ≥0.7 IoU AND ≥0.55 BF1 · PARTIAL ≥0.5/0.35 · else LAYOUT MISMATCH
   - mirrored candidate evaluated explicitly; if it beats direct by >0.05 → mirror flag
     (never silently accepted).
4. **Position-aware feature checks**: feature centers measured from named datums and
   compared to the REFERENCE's centers (e.g. T4 camera window: Δx from footprint center,
   Δy from top edge, tol ±2 mm, crit). Size alone never passes a placement check.
5. **success (v2)** = scorer.py criticals AND watertight AND layout verdict ∈
   {MATCH, PARTIAL} AND all position checks pass AND no unexplained mirror flag.
6. Acceptance test for the verifier itself: it must FAIL the runs a human flagged
   (T3 v1 layout, T4 camera placement) and PASS reference-vs-itself. Verified 2026-07-23.

## Threats to validity (acknowledged)
- n=1 per cell; treat deltas < ~15 fit points as noise.
- Judge (me) designed one of the skills — design_judge scored blind on shuffled renders.
- T2 mating dims reverse-derived from the reference tool (clearance-aware scoring bands).
- T1-T2 subagents ran on the session model (fable), T3-T4 on Opus 4.8 (user request) — compare arms within a test, not across tests. Subagents inherit + a warm token cache; costs comparable across arms
  within this session, not across sessions.
