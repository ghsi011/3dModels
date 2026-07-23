# Verification postmortem — why obvious mismatches passed

Idan's observation: "none of the renders look like the references" (T3), "in T4 they
all failed in placing the camera window correctly" — and every one of those runs was
scored ✅ by my pipeline. Both observations are correct. Root causes, in order of damage:

## 1. The scorer measured sizes, never positions or layout
`holes_at()` computed each hole's center (`cx`, `cy`) — and no check ever read those
fields. T4's camera check was `size >= 44x22, area < 2500` → a camera window in the
wrong corner passes. T3's layout check was `count(pockets) >= 10` + size-class spread →
a grid of plain rectangles scores identically to the reference's stepped tool
silhouettes. Nothing anywhere compared candidate geometry *against the reference
geometry* — only against hand-derived scalar bands.

## 2. No mandatory look at candidate-vs-reference, same views
Every run produced renders, and `ref_preview.png` existed for every test — but no step
required putting them side by side from identical cameras, so nobody (me included)
ever *saw* the mismatch until Idan asked for the render gallery. Renders were treated
as artifacts to deliver, not as evidence to inspect. Worse, candidate and reference
renders used different cameras/orientations, so even a casual glance couldn't compare.

## 3. The judge never saw the reference
The design-quality judge got the candidate's renders + notes and scored "does this
look well-engineered" — it could not flag "this is not the same part" because it was
never shown the ground truth.

## 4. Prompt authoring had the same blindness (T3 root cause)
I wrote the T3 prompt from slice bounding boxes without viewing the photos, so the
prompt itself described rectangles. Agents followed the text. The verification layer
should have caught this too — reference-vs-prompt is a comparison as well.

## The fix (implemented in verify_visual.py + protocol change)
1. **Side-by-side composite from identical cameras** (top / front / iso), reference row
   above candidate row — generated for every run, and the grader (me) must view it and
   describe both before any score is recorded. "Looked at it" becomes an artifact, not
   an intention.
2. **Slice-layout IoU**: rasterized material + cavity overlap vs the reference at
   matched heights, after bbox alignment and best-of-4 rotation search. Cavity IoU is
   the layout-sensitive number the old scorer lacked. Mirror detection is explicit
   (mirrored-fit-better = red flag, not silent pass).
3. **Position-aware feature checks**: feature centers (e.g. T4 camera window) measured
   from named datums and compared to the *reference's* centers with a mm tolerance —
   size alone never passes a placement check again.
4. **Calibration rule extended**: reference-vs-itself must score IoU ≈ 1.0 and pass all
   position checks; known-bad runs (T3 v1) must FAIL the new verifier before we trust it
   on new runs. A verifier that can't reproduce the human's "these don't match" is not
   done.
5. **Skill Phase 4 gains the same rule**: render the part next to the user's photos /
   reference from matching viewpoints and compare feature-by-feature; verify every
   cutout's *position* from a named datum in the exported STL, not just its size.
