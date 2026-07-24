---
contract: dimensions
contract_version: 4
job_id: broom-holder-step1-metrology
revision: 1
owner: metrologist
status: DRAFT
updated_utc: 2026-07-24T21:40:00Z
---

# Dimensions

Scope note: this is metrology step ① only. Only the mating object (the round broom
stick) and the target grip-fit band for a future holder are established here. No holder
has been designed, no reference CAD exists yet, and the blind-reference round trip is
therefore `PENDING` (see below), not run.

## Frame

| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| D0_AXIS | Centerline of the round shaft (rotational symmetry axis). Computed as the pixel-row-wise midpoint between the left/right silhouette edges, median over rows 150-500 of S-01 (416x572 px raster). | S-01, script-measured | C - single 2D projection; a straight, non-wandering centerline across the full visible shaft is corroborating, not an independent 3D confirmation |
| D1_TIP_APEX | Z=0 origin: topmost pixel of the rod silhouette, i.e. the apex of the domed tip (feature F-002). | S-01, script-measured | C |
| +Z | From D1_TIP_APEX down the shaft axis, away from the tip, toward the frame-cropped bottom edge of the photo (far end/direction not otherwise evidenced). | S-01 (direction only; magnitude not evidenced) | C |
| Angular (rotational) datum | None defined. No flat, seam, label, or other asymmetric feature is visible in S-01 to fix a rotation reference. The stick is treated as rotationally symmetric about D0_AXIS for grip-fit purposes. | absence of evidence | D - assumption of symmetry, consistent with the user's "round rod" statement but not independently confirmed |

Handedness/+X/+Y: not fixed - the part is rotationally symmetric and no evidenced feature
breaks that symmetry, so no angular datum is defined. Any downstream fin/cradle layout is
free to choose its own angular reference.

## Sources

| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| S-01 | `evidence/input/30mm-broom-stick.png` (original: `tests/broom holder/30mm broom stick.png`) | user's actual stick; generic/unbranded wooden dowel | sha256 `3214476bf70b2cb12342a45b4342676631afd192f39bbb1046a2d8e10357bac3`; 416x572 px PNG | Single product-style photo on a plain light background. No ruler, caliper, or scale marker visible after inspection at 3-4x zoom of the top, middle, and bottom regions (see `evidence/metrology/`). Single view only - no second angle, no top-down cross-section. |
| S-02 | Task-brief text: "The stick is a ~30 mm diameter round rod (per the user)" | user's actual stick | task issuance date 2026-07-24 | Verbal/task-text assertion, not a caliper reading or official spec. Treated as Confidence D per the grading rule below. |

## Blind-build completeness

| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| F-001 | Round shaft, 1x - the primary surface the future holder grips | Ø30.0 mm nominal (bounded working range 29.0-31.0 mm), centered on D0_AXIS; visually constant diameter (no taper) over the full visible length | S-01 (constancy, M-002) + S-02 (nominal diameter) | D (diameter) / C (constancy) | Model as a plain right-circular cylinder at the M-001 diameter, of a length sufficient to host a grip-fin/cradle test coupon (axial length itself is not evidenced - parametrize, e.g. ~150 mm placeholder, not a measured fact) | Yes, with caveat: diameter is unconfirmed by caliper (Q-01) |
| F-002 | Domed/rounded tip, 1x - manufacturing detail at the visible top end, not a mating feature | Apex at D1_TIP_APEX (Z=0); dome transition spans roughly the top 56 px of the shaft's 88 px steady-state width (image-pixel proportion, M-003) | S-01 | C | Optional for the reference cylinder. Model as a simple rounded/hemispherical cap, or omit entirely if the reference is only needed to validate a mid-shaft grip coupon | Yes; non-fit-critical |
| F-003 | Far end / total stick length | Not evidenced. The bottom of S-01 is a photo frame-crop edge, not a confirmed physical end of the stick (no taper, chamfer, thread, or ferrule is visible there - it simply runs off-frame) | none | U | Do not model an end feature at the crop edge. Leave the reference shaft open-ended / length-parametrized | No - blocked by missing evidence; non-blocking for a mid-shaft grip reference (see Q-04) |
| F-004 | Cross-section roundness (true circularity vs. oval/faceted) | Assumed true circular. Single 2D photo cannot independently confirm 3D circularity; the smooth highlight/shadow gradient across the shaft width is consistent with a round (not faceted) surface | S-01 (shading, C) + S-02 (user states "round rod", D) | C / D | Model F-001 as a true circle at the M-001 diameter; flag for physical confirmation before final tolerance lock (Q-02) | Yes, with caveat |

## Dimensions

| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|
| M-001 | F-001 shaft diameter | 30.0 mm nominal; working range 29.0-31.0 mm | Diameter perpendicular to D0_AXIS, read at the flat shaft band (image rows ~114-314 of 572, roughly 17-55% down the frame - see `evidence/metrology/annotated_datums.png`), deliberately offset from the F-002 dome transition (ends ~row 74) and from the bottom frame-crop edge (row 571), per the skill's flat-region reading rule | user task-brief statement ("~30 mm diameter round rod"); no caliper reading visible anywhere in S-01 at 3-4x zoom | D | **Fit-critical.** Carry the full 29.0-31.0 mm range forward through the grip-fin band's compliant range (M-011). Require caliper confirmation, or retire via the PLA fit coupon (repo workflow rule), before locking final candidate geometry. |
| M-002 | F-001 shaft width constancy | Silhouette width 84-90 px across sampled rows 100-560 of S-01 (416x572 px), median ~88 px over rows 150-500, vs. 78-85 px through the rows 40-80 dome-transition band. No in-image scale reference, so no mm value is derivable from this alone. | Perpendicular pixel span of the rod silhouette, background-threshold segmented (Euclidean RGB distance from white > 18), sampled every 20 rows | S-01, direct pixel measurement (script-derived, reproducible) | C | Non-fit-critical corroboration only. Supports "no significant taper" over the visible shaft - i.e. a constant-diameter cylinder is the correct reference shape, not a tapered handle. Do **not** convert this pixel figure into an mm diameter; it has no scale reference. |
| M-003 | F-002 dome height proportion | Dome transition: apex at row 18, reaches 90% of steady-state width at row 74 -> ~56 px of dome height vs. ~88 px steady shaft width -> dome height is roughly 0.6-0.7x the shaft diameter (proportion only) | Pixel rows from apex to the 90%-of-steady-width row | S-01, pixel measurement | C | Informational only, not fit-critical. F-002 is not the presumed grip zone. |
| M-010 | F-001 grip strategy | Spring/grip-fin, partial-wrap capture, sized for constant/repeated-assembly grip (explicitly not single-assembly crush ribs) | Recommendation basis: `fdm-design.md` §4 - "For repeated assembly use grip fins ... constant grip that also absorbs shrinkage." A broom holder is inherently insert/remove-repeated, which rules out crush-rib (single-assembly) capture. | Metrologist design-target recommendation, grounded in `fdm-design.md` §4, produced per this commission's explicit instruction | N/A (strategy choice, not a measured dimension) | Binding design-target for the CAD phase. Fallback alternate = snug-wrap open C-cradle (single elastic ring, opening narrower than the rod) if discrete fins prove impractical at this diameter/material - see rationale below. |
| M-011 | F-001 grip diametral interference band (fit-critical) | Interference 0.6 mm min / 1.0 mm nominal / 1.4 mm max, diametral (0.3 / 0.5 / 0.7 mm per side, radial) under M-001's nominal 30.0 mm => fin-tip relaxed-ID target band **29.4 mm (loosest) / 29.0 mm (nominal) / 28.6 mm (tightest)** | Derived: M-001 nominal minus the interference band; per-side clearance convention per `fdm-design.md` §4 | `fdm-design.md` §4 grip-fin heuristic ("fin ID 1 mm under the rod diameter ... 0.3 mm clearance gap behind each fin") bounded into an explicit min/max band per the 3d-metrologist skill's mandatory-band rule (never a one-sided floor) | C (derived; inherits M-001's D-confidence) | **Fit-critical.** Re-derive 1:1 against M-001 if that value changes. A PLA fit coupon is required before final material (repo `AGENTS.md` workflow rule) to retire the residual D-confidence carried from M-001. |

## Grip fit rationale (M-010/M-011)

- This is a **retention** grip - the holder must hold the stick against gravity and knocks
  through repeated insert/remove cycles - not a slip or rotating fit. The generic
  press/snug/sliding/loose/free clearance table in `fdm-design.md` §4 assumes
  machined-tolerance mating parts and does not directly apply. The applicable rule is the
  same section's named **grip-fin** strategy: thin elastic fins undersized relative to the
  rod, sized to flex open on insertion and spring back to hold constant contact pressure -
  explicitly recommended there over crush ribs for repeated assembly.
- `fdm-design.md` gives one worked example as a single nominal point (11 mm fin ID grips a
  12 mm rod = 1.0 mm diametral undersize, with a 0.3 mm clearance gap behind each fin), not
  a band. Per the 3d-metrologist skill's explicit rule - "a fit-driving clearance is a
  bounded fit BAND ... never an open-ended floor" - that single point was bounded into:
  - **Floor: 0.6 mm diametral / 0.3 mm per side.** The least interference that should still
    guarantee a positive, constant grip once print shrinkage, fin creep, and (per Q-01) up
    to +/-1 mm of unconfirmed stick-diameter variance stack against it. Below this the grip
    risks going slack - an over-clearance failure (rattle/slip) that is exactly as real a
    failure mode as interference, per the skill's explicit framing.
  - **Ceiling: 1.4 mm diametral / 0.7 mm per side.** The most interference that should keep
    hand-insertion force reasonable and stay inside the elastic range of a PETG/ABS/PA fin
    (`fdm-design.md`'s snap-fit/grip-fin material guidance - "PLA arms shatter") without
    plastic set over repeated cycles.
  - **Nominal: 1.0 mm diametral / 0.5 mm per side** reproduces `fdm-design.md`'s literal
    worked example, sitting mid-band.
- This band is anchored to M-001's stated nominal (30.0 mm). Because M-001 itself is
  D-confidence (user-stated, no caliper, no scale reference in the photo), the **band width
  (0.6-1.4 mm diametral) is the portable recommendation**, not the anchored 28.6-29.4 mm ID
  numbers - re-anchor those once a caliper reading or coupon confirms the real diameter.
- Alternate strategy flagged for the design phase: a **snug-wrap open C-cradle** (one
  continuous elastic ring with an opening narrower than the rod, sized by the same
  min/nominal/max logic) is a viable fallback if discrete fins prove awkward to lay out at
  30 mm diameter and the eventual wall thickness. This dimensions sheet does not choose
  between fin-count/spacing/geometry variants - that is CAD-designer territory - it only
  fixes the numeric interference target the design must hit.
- Full-wrap C-clip vs. partial wrap, and any mounting/back face, are **not evidenced** by
  the single stick photo (no holder, no wall, no mount is shown in S-01). I have not
  inferred a clip/wrap architecture from evidence - the recommendation above concerns only
  the fin/interference sizing rule, which is architecture-agnostic and applies whether the
  eventual holder is a full ring, a partial C-wrap, or a two-point cradle. See Q-03.

## Open questions

| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| Q-01 | Stick diameter not caliper-confirmed - only the user's "~30 mm" statement; no scale reference anywhere in S-01 | Wrong nominal shifts the whole grip-fin band 1:1; could produce a grip that ends up outside the 0.6-1.4 mm interference band (too loose = rattle/slip, too tight = unprintable insertion force or fin overstress) | Please provide a caliper reading (jaws closed flat on the shaft, away from the domed tip - i.e. in the M-001 read zone) or a photo showing a caliper display | Blocks upgrading M-001/M-011 to Confidence A/B. Does **not** block starting a blind reference cylinder build at the stated D-confidence nominal. |
| Q-02 | True cross-section roundness not confirmed - single 2D photo/single view; could be oval or faceted and still look round from this angle | An out-of-round or faceted stick would make a fixed-ID fin ring bind on the long axis and gap on the short axis | A second photo rotated ~90 deg about the shaft axis, or explicit user confirmation the stock is lathe-turned round dowel | Non-blocking for this deliverable (user already asserts "round rod"). Should be confirmed with the fit coupon if precision matters. |
| Q-03 | Grip location and mount context unknown - single stick photo only; no holder, no wall, no mounting hardware photographed | Cannot yet decide single-point vs. two-point capture, storage orientation (horizontal/vertical), or a screw-mount vs. adhesive back face | Ask the user: wall-mounted or freestanding? one grip point or two (for anti-rock stability)? screw-mount, adhesive, or hook-over back? | Blocks full holder design (out of scope for this step). Does **not** block this `dimensions.md` deliverable, which is scoped to the stick + grip-fit band. |
| Q-04 | Overall stick length and far-end geometry unknown - the visible photo bottom is a frame-crop edge, not necessarily the stick's physical end | None for a mid-shaft grip fit. Would matter only if the holder needs to reference total stick length or the far (broom-head) end geometry | None needed for this step; ask only if a later design needs an end-stop or a length-dependent feature | Non-blocking. |

## Reference round trip

| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
| - | - | `PENDING` - no reference model has been commissioned. This deliverable is metrology-only (commission step ①); no CAD, no FreeCAD, and no reference build occurred. | - |
