# Method — broom holder grip metrology (step ①)

Scope: establish geometric ground truth for the round broom stick and the numeric
grip-fit band a future holder design must hit. No CAD, no FreeCAD, no reference model, no
holder design. This is the metrologist's `dimensions.md` step only.

## Inputs actually read

- `tests/broom holder/30mm broom stick.png` (only image supplied) - inspected at native
  resolution (416x572 px) and at 3-4x upscaled crops of the top (domed tip), middle
  (shaft), and bottom (frame-crop edge) regions.
- `skills/3d-metrologist/SKILL.md` (the updated slice run for this commission).
- `skills/team-design.md` §6.2 and `skills/3d-modeling/references/team-contracts-v4.md`
  (`dimensions.md` v4 schema and confidence-grade rules).
- `skills/3d-modeling/references/fdm-design.md` §4 (fits & tolerances, including the
  grip-fin/crush-rib guidance for a repeated-assembly rod grip).
- The task brief itself, which is the only source for "the stick is a round rod, ~30 mm
  diameter" - this is a **user statement**, not a measurement I made.

Not read (per commission scope): `tests/broom holder/BroomHolderVCD.3mf`, any other
`tests/` subfolder, any `experiments/` material. No web search was performed - the task
brief scoped inputs to the photo plus the named skill/reference docs, and this is a
generic (non-branded) stick, so there is no "official spec" to corroborate against.

## Where each number came from

**M-001 (shaft diameter, 30.0 mm nominal, 29.0-31.0 mm range).** The 30.0 mm figure is
the user's stated value from the task brief ("~30 mm diameter round rod"), carried
forward verbatim. I inspected the photo at 3-4x zoom across the top, middle, and bottom
regions specifically looking for a caliper jaw or a ruler in frame - there is none; the
photo is a plain product-style shot of the stick alone on a light background. Because
there is no scale reference of any kind in the image, I could not derive an independent
mm diameter from the photo itself, and I did not attempt to (that would have silently
converted an assumption into a measured fact). I bounded the nominal with a working
+/-1.0 mm range to give the downstream grip-fin band something to be honest about;
that range is my own conservative allowance for a generic hardware-store dowel with no
confirmed tolerance, not a value derived from any source - it is explicitly flagged
D-confidence and named in Q-01 as needing caliper or coupon confirmation.

**M-002 (pixel width constancy, no taper).** I wrote a short script
(`py -3`, PIL + numpy) that thresholds each row of the photo against the white
background (Euclidean RGB distance from (255,255,255) > 18) and records the left/right
silhouette edges every 20 rows. Excluding the dome-transition band (rows ~18-74), the
shaft silhouette holds to 84-90 px across rows 100-560 (median ~88 px over the 150-500
range) out of a 416-px-wide, 572-px-tall image. This is a relative/proportional check
only - there is no scale reference, so it cannot produce an mm figure - but it is direct,
reproducible evidence that the visible shaft does not taper, supporting a plain
constant-diameter cylinder as the correct reference shape.

**M-003 (dome height proportion).** Same script: the dome-transition band runs from the
apex row (row 18, the first row where any non-background pixel appears) to the row where
the silhouette first reaches 90% of the steady-state shaft width (row 74). That is a
~56 px dome height against an ~88 px steady shaft width, i.e. roughly 0.6-0.7x the shaft
diameter. This is informational only; the domed tip is not expected to be where a broom
holder actually grips the stick (that would be somewhere along the constant-diameter
shaft), so it is marked non-fit-critical.

**D0_AXIS / D1_TIP_APEX (frame datums).** Computed from the same per-row silhouette
edges: the axis is the median of the row-wise left/right midpoint over rows 150-500; the
tip apex is the topmost silhouette row (row 18), giving the Z=0 origin. No angular
(rotational) datum is defined - nothing in the single photo breaks the part's rotational
symmetry, and the user's own description ("round rod") is consistent with that.

**M-010 / M-011 (grip strategy and diametral interference band).** This is the
task-mandated design-target handoff, not an observed feature. `fdm-design.md` §4 states,
for round-rod capture: *"For repeated assembly use grip fins (thin elastic fins that
flex, not crush): fin ID 1 mm under the rod diameter (11 mm ID grips a 12 mm rod), 0.3 mm
clearance gap behind each fin - constant grip that also absorbs shrinkage."* That is a
single worked point (1.0 mm diametral undersize), not a band. `skills/3d-metrologist/SKILL.md`
explicitly requires turning any fit-driving clearance into a bounded band with a stated
min **and** max, reasoning that over-clearance (a captured part that slips or rattles) is
its own failure mode, not just interference. I built the band around the reference's
1.0 mm nominal:
- floor 0.6 mm diametral (0.3 mm/side) - my own margin against M-001's uncertainty,
  print shrinkage, and fin creep, so the grip does not go slack;
- ceiling 1.4 mm diametral (0.7 mm/side) - my own margin against `fdm-design.md`'s
  material warning that repeated-cycle elastic fins need PETG/ABS/PA and that "PLA arms
  shatter," i.e. don't push interference so far the fin overstresses.

Both bounds are my engineering judgment applied to the cited source rule, not a number
pulled from any document - this is stated explicitly in `dimensions.md`'s rationale
section so it is not mistaken for a measured or sourced figure. A snug-wrap open C-cradle
is named as a fallback strategy per the task brief's "or a snug wrap" option, but grip
fins are the primary recommendation because `fdm-design.md` names them specifically for
repeated assembly (which a broom holder inherently is).

## Confidence grading used

Per `fdm-design.md`/skill convention: `A` = direct measurement, `B` =
official/corroborated, `C` = image-derived, `D` = assumed/user-stated.

| Value | Grade | Why |
|---|---|---|
| M-001 shaft diameter | D | User-stated in the task brief; no caliper or scale reference anywhere in the photo |
| M-002 width constancy | C | Direct pixel measurement on the photo, but unscaled (relative only) |
| M-003 dome proportion | C | Direct pixel measurement on the photo, unscaled proportion |
| F-004 roundness | C (shading) / D (user says "round") | Single-view shading is suggestive, not conclusive |
| M-011 interference band | C | Derived from a cited source rule (fdm-design.md §4) bounded by my own margins; inherits M-001's D-confidence for its absolute mm anchor |

## Open questions (see `dimensions.md` for the full table)

1. **Q-01 - diameter not caliper-confirmed.** Highest-impact open item: the entire
   grip-fin band is anchored to a user-stated, unverified number. Recommended resolution:
   a caliper photo, or the PLA fit coupon the repo's `AGENTS.md` already requires before
   any final-material fit part.
2. **Q-02 - roundness not confirmed from a second angle.** Low risk given the user's own
   description, but worth a rotated photo or coupon check before finalizing a tight-ID
   fin ring.
3. **Q-03 - mount/back-face/orientation entirely unknown.** No holder, wall, or mount
   appears in the only supplied photo. Out of scope for this metrology step but blocking
   for full holder design; needs direct user answers.
4. **Q-04 - total stick length / far-end geometry unknown.** The photo's bottom edge is a
   frame crop, not a confirmed physical stick end. Non-blocking for a mid-shaft grip
   fit; would only matter for an end-stop or length-dependent feature later.

## Evidence produced

- `evidence/input/30mm-broom-stick.png` - byte-identical copy of the only source photo
  (sha256 `3214476bf70b2cb12342a45b4342676631afd192f39bbb1046a2d8e10357bac3`), preserved
  unmodified per the immutable-input rule.
- `evidence/metrology/annotated_datums.png` - annotated 3x-upscaled photo marking
  D0_AXIS (centerline), D1_TIP_APEX (Z=0), the F-002 dome-transition band, and the M-001
  flat-region read zone used for the diameter callout. I visually inspected this
  composite before relying on the coordinates in `dimensions.md` (not just the numeric
  script output): the axis line hugs the shaft's visual centerline through the full
  straight section, the apex marker sits on the true top of the dome, and the read-zone
  box sits inside the constant-width band, clear of both the dome transition and the
  bottom crop edge.

## What this step does not do

- Does not build, overlay, or accept a reference CAD model - there is no `REFERENCE_BUILD`
  yet, so the "Reference round trip" table in `dimensions.md` is `PENDING`, not run.
- Does not design the holder, choose fin count/spacing, or touch FreeCAD/CadQuery.
- Does not silently promote any D/C-confidence number to A/B - every value above states
  its actual provenance and the confidence table is honest about what is and is not
  measured.
