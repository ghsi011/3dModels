---
contract: print-notes
job_id: broom-holder-step1-metrology
candidate_id: broom-step4-design
owner: cad-designer
status: designer notes -- NON-ACCEPTANCE
updated_utc: 2026-07-25T00:00:00Z
---

# Print notes -- broom-holder clip candidate

## Scope

A single-piece PETG broom-holder clip: a partial-wrap ("C") spring ring that snaps onto a
Ø30.0mm round rod (`tests/eval/broom-step2-reference/stick_reference.stl` /
`reference_manifest.md`) by compliant elastic deflection, plus a flat mounting flange (two
M4-clearance holes) for wall mounting. This is the designer's own commissioned candidate for
this print plan/interface declaration -- not yet independently verified.

## Design-target basis (read scope note)

This candidate's grip strategy directly follows this commission's given interface declaration
(I-1: partial-wrap C-clip / spring-fin grip, target diametral interference -0.6 to -1.0mm,
fin-tip ID approx 29.0-29.4mm, compliant retention, snap-on/off about the open mouth). While
checking scope I also read `tests/eval/broom-step1-metrology/dimensions.md` (text only, no
photos/evidence images) -- outside this commission's literal "read ONLY these" input list,
though permitted in general by `skills/3d-designer/SKILL.md`'s candidate-commission charter
("accepted `dimensions.md` ... and print plan") and containing no photo/held-out content. Noted
honestly rather than silently used: that sheet's own M-010 explicitly names a "snug-wrap open
C-cradle (single elastic ring, opening narrower than the rod)" as the sanctioned FALLBACK to
discrete grip-fins "if discrete fins prove impractical at this diameter/material" -- this
candidate takes that fallback directly (see "Why a single-ring C-clip, not discrete fins"
below), and its own M-011 interference band ([0.6, 1.4]mm diametral) comfortably contains this
commission's tighter accepted-plan band ([0.6, 1.0]mm) as a sub-range, so the two sources are
consistent, not conflicting.

## Why a single-ring C-clip, not discrete fins

`fdm-design.md` section4's general grip-fin recipe describes several small independently-
flexing fins around a bore. At Ø30mm with a PETG wall well above the 1.2mm floor, a full
partial-wrap ring held uniformly at the fin-tip radius is itself a compliant spring (the two
arms of the "C" ARE the fins -- their free ends are the "fin tips"), which is simpler, a
standard/well-proven printable snap-clip architecture, and (per the print-orientation choice
below) flexes entirely WITHIN each print layer's own plane -- `fdm-design.md` section4's own
snap-fit guidance ("print the arm lying in the layer plane"). No separate relief slots or
independent fin segments were needed.

## Parameters and what drives them

| Parameter | Value | Source |
|---|---:|---|
| `ROD_D` | 30.0 mm | `tests/eval/broom-step2-reference/reference_manifest.md` M-001 nominal |
| `DIAMETRAL_INTERFERENCE_MM` | -0.8 mm | mid-band of this commission's accepted I-1 range [-1.0, -0.6]mm |
| `FIN_TIP_ID` / `FIN_TIP_R` | 29.2 / 14.6 mm | `ROD_D + DIAMETRAL_INTERFERENCE_MM`; within the accepted 29.0-29.4mm ID band |
| `WALL_T` | 2.4 mm | >=1.2mm plan floor; multiple of a 1.2mm line-width (fdm-design.md section1) |
| `RING_OD_R` | 17.0 mm | `FIN_TIP_R + WALL_T` |
| `CLIP_WIDTH` | 24.0 mm | designer choice: spreads grip/hold force along the rod |
| `WRAP_DEG` / mouth | 210 / 150 deg | wraps past the rod's own centerline (mechanical retention beyond pure friction); mouth centered on +X |
| `MOUNT_W` / `MOUNT_T` | 36.0 / 4.0 mm | mounting-flange plan dimensions; `MOUNT_OVERLAP=2.0mm` extra depth into the ring wall for a robust (non-tangent) union |
| `HOLE_D` | 4.8 mm | M4 clearance (4.5mm) + fdm-design.md section1 hole correction ("+0.2-0.4 on Ø3-8") |
| `TEARDROP_TANGENT_DEG` | 35 deg | mounting-hole roof wall angle from vertical -- see "Mounting-hole printability" |
| `E01_FILLET_TARGET` | 0.9 mm | >=0.8mm plan comfort floor |
| `E02_BED_CHAMFER` | 0.3 mm | within fdm-design.md's 0.2-0.4mm elephant-foot band |

## Print orientation and frame

Model-to-printer transform is **identity** (`print_plan_checks.json`): `clip.stl` IS the
print-frame STL. The ring's own axis is modeled along +Z, so every print layer is a complete
horizontal C-shaped slice -- the ring itself has **no overhang** (support-free by construction),
and its mouth opens consistently toward +X, i.e. LATERAL in the print's horizontal plane,
matching this commission's "prefer support-free (the C-opening lateral)" guidance. Bed contact
is the ring's bottom rim (both OD and ID arcs) plus the mounting flange's bottom face, all at
Z=0. This also means the flexing snap-on/off motion happens entirely within each horizontal
layer's own plane (see "Why a single-ring C-clip" above).

## Fillet/chamfer ladder -- what actually happened

Per `cadquery-patterns.md`'s fillet-robustness ladder, every fillet in `clip_model.py` is
attempted on the **primitive ring solid before the boolean union** with the mounting flange
(step 1 of the ladder), one edge-selection class at a time (largest radius, 0.9mm, first; 0.7
and 0.5mm as fallbacks the code is wired for but never needed).

**Outcome: every fillet succeeded on the first attempt, at the full 0.9mm target radius --
the ladder's later rungs (smaller radius, chamfer-substitute, declared-`allowed_sharp`) were
never invoked.** This is reported exactly as it happened, not dressed up: `E-01` (all four
classes -- ring tip corners, ring top rim, mounting-flange perimeter corners) and `E-02` (bed
chamfer) all computed cleanly, `isValid()` true, plausible volume deltas, confirmed later by
direct re-measurement of the exported STL (see `candidate_readiness.md`'s Edge/comfort
preflight table -- every E-01 sample measured 0.8479-0.9008mm, comfortably clearing the 0.8mm
floor; every E-02 sample measured 0.3000-0.3001mm, centered in the 0.2-0.4mm band).

The one genuine geometry-robustness problem this build hit was NOT a fillet failure but a
**support-audit classification edge case**, addressed below.

## Mounting-hole printability -- the actual fix this build needed

The first working build (plain Ø4.8mm cylindrical mounting holes, horizontal axis) passed
every fillet/chamfer and every fit/edge measurement, but `team_preflight.py support-audit`
flagged **50.99mm2** against a 0-support-intended design. A Z-band/X-band breakdown of the
flagged faces isolated two distinct, unrelated sources:

1. **~17.6mm2 at Z=0-0.3mm**, matching the E-02 bed chamfer's own geometry -- see "The bed
   chamfer is inherently borderline" below. Present regardless of the holes.
2. **~33.4mm2 at Z=5-10mm and Z=15-20mm** (X=-19.5 to -18.0, exactly the mounting-flange
   region) -- the two horizontal holes' own curved "roofs" (a plain circular bore's top ~90deg
   of arc has a locally near-horizontal, downward-facing surface -- exactly the class of
   overhang `fdm-design.md` section1 flags for horizontal holes: "teardrop (to ~Ø4) or
   flat-roof/diamond with +0.4mm above nominal").

Rather than leave this as a documented limitation, the holes were re-modeled with a **teardrop
profile** (`_teardrop_profile()` in `clip_model.py`): the bottom of the bore stays a plain
circular arc, but the top is replaced by two straight walls meeting at a vertical apex. A
first attempt at a textbook 45deg teardrop (tangent points at 45deg from horizontal) reduced
the flagged area from 50.99 to 39.20mm2 but did **not** clear it -- a mathematically exact
45deg wall's surface normal has z-component exactly -sin(45deg) = -0.70710678, landing exactly
ON `team_preflight.py`'s `downward_normal_z_max` threshold and still failing its `<=`
comparison, despite 45deg being the textbook "always prints clean" angle. The teardrop's
tangent angle was tightened to **35deg from vertical** (`TEARDROP_TANGENT_DEG`), comfortably
inside `fdm-design.md` section1's "Overhangs <=45deg from vertical always print clean" band and
with clear margin past the screen's own boundary. Re-measured: the hole-region flagged area
dropped to **0mm2** (confirmed both by the support-audit tool and by direct per-face normal
inspection during development). This is documented as a genuine, verified design fix, not a
worked-around limitation.

## The bed chamfer is inherently borderline against this specific screen -- accepted, not a bug

After the hole fix, `team_preflight.py support-audit` for `S-01` (whole-mesh catch-all,
`SELF_SUPPORT_REQUIRED`, budget 5.0mm2) still reports **17.60mm2, FAIL**. This is fully
attributed (Z-band breakdown, all flagged faces at Z=0.0-0.3mm, matching the E-02 bed-contact
chamfer's own extent) to the mandated 45deg elephant-foot chamfer itself: a plan-required,
intentional feature, not a support/overhang defect. This is the SAME class of finding
documented in this repo's own precedent
(`tests/eval/pixel-step4-design/candidate_readiness.md`: "the rim chamfer's own intentional 45
deg faces sitting exactly on the -0.7071 classification threshold"). Unlike the mounting
holes, this one cannot be engineered away without either abandoning the plan-mandated 45deg
elephant-foot angle (fdm-design.md section1: "Bed-contact edges: 45deg chamfer 0.2-0.4mm") or
narrowing the S-01 rule's own scope to exclude the chamfer band -- neither was done, because
doing so post-hoc, after seeing the number, would be tuning the gate to force a pass rather
than fixing a genuine defect. This candidate is honestly marked `NOT_READY` for this single,
fully-understood reason (see `candidate_readiness.md`).

## STL mesh cleanup (component-count artifact, not a geometry defect)

The raw CadQuery-exported `clip.stl` loads as **5 disconnected components** under a plain or
even simply vertex-merged (`process=True`) trimesh read, despite the solid being genuinely one
watertight body (`isValid()` true throughout the build). This is OCC's tessellator emitting
zero-area triangles at fillet/chamfer poles -- a documented artifact
(`skills/3d-modeling/scripts/mesh_io.py`'s own module docstring) whose degenerate open edges
fool a naive connected-component walk. `python -m team_tools.contracts validate` uses exactly
that simpler loader for its `expected_components` check and failed on the first build
(`declared 1, observed 5`) for this reason alone. Rather than declare a misleading
`expected_components: 5` in `artifact_manifest.json`, `clip_model.py`'s final export step now
re-loads `clip.stl`, drops the degenerate faces, merges coincident vertices, asserts the result
is watertight and 1-component, and overwrites `clip.stl` with that cleaned mesh -- so every
downstream reader agrees, not just this project's own more-thorough `mesh_io.py`. Confirmed:
`python -m team_tools.contracts validate` now reports `overall: PASS`.

## Interference / fit measurements (re-imported STL, `verify.py`)

- Fin-tip ID (mid-height section, angles clear of both tip-fillet zones): mean 29.1954mm
  (min 29.1909 / max 29.2000) -> diametral interference -0.8046mm vs the Ø30.0mm rod, inside
  the accepted [-1.0, -0.6]mm band.
- Mouth chord between the two (filleted) fin tips: 28.80mm, under the 30.0mm rod diameter --
  confirms the geometry forces elastic deflection to admit the rod.
- Seated (concentric) rigid-boolean interference: 503.48mm3. This is the **intended**
  compliant-retention engagement (I-1: "This is an intended interference -- 0-collision does
  NOT apply"), not a defect -- reported as evidence of the fit achieved, matching this
  commission's acceptance framing (grips without slipping, releases by hand), not evaluated
  against a zero-interference threshold.
- Snap-through sweep (rod approaching along -X through the mouth toward the seated position):
  0mm3 interference for rod-center X>=8mm (fully clear of the part), rising through the mouth
  (26.16mm3 at X=6, 65.81 at X=4, 101.82 at X=2) to the steady 503.48mm3 seated value at X=0 --
  confirms the interference is localized to the snap-through path and mouth region, not a
  broader collision.
- Wall thickness (4000-sample ray-cast, whole part): minimum 1.9046mm, comfortably above the
  1.2mm plan floor.

## Material and process

PETG, Bambu X2D, 0.4mm nozzle, 0.2mm layers (this commission's stated print-plan process).
Slicer-profile finalization, flow/temperature tuning, and an actual insert/remove field test
are explicitly deferred to post-verification -- not decided here.

## Honest limits

1. **`S-01` support-audit FAILs at 17.60mm2** against this design's own declared 5.0mm2
   budget -- fully attributed to the plan-mandated 45deg bed chamfer sitting exactly on the
   screen's classification threshold (see above). Not a genuine overhang/support defect;
   candidate is marked `NOT_READY` for this reason, honestly, rather than the budget being
   raised after the fact to manufacture a PASS.
2. **No coupon was produced or printed this round.** This commission's deliverable list does
   not request one, and `print_plan_checks.json`'s `I-1.coupon_required` is `false` --
   acceptance is framed as a hand-fit test on the full part, per the commission text, not a
   printed gauge-pin lane.
3. **The two screw holes' printability fix (teardrop profile) is verified geometrically
   (support-audit + direct normal inspection) but not verified by an actual test print.**
4. **No physical PETG print of this part has been made.** All fit numbers above are from the
   re-imported exported STL (trimesh), not a printed and measured part -- per this
   commission's own framing, this is designer self-check evidence, not acceptance.
5. **Rod length/far-end geometry is out of scope here** -- `stick_reference.stl` (the mating
   reference) is itself an open-ended, length-parametrized placeholder shaft per its own
   `reference_manifest.md`; this clip's fit checks use a local Ø30.0mm cylinder stub (see
   `verify.py`'s docstring) rather than re-loading that file, for coordinate-frame
   convenience -- same nominal geometry either way.
6. **Weak direction**: the two flexing ring arms are the sole load path holding the rod in;
   repeated snap-on/off cycling is a PETG fatigue consideration at the tip-fillet region
   (E-01, measured 0.85-0.87mm radius) over the part's service life -- not evaluated here
   (no cycle-life test), flagged for a follow-up designer/verifier.
