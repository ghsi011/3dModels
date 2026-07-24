---
contract: reference-manifest
job_id: garmin-7x-charging-dock
step: garmin-step2-reference
role: designer (reference commission, blind build)
input_read: tests/eval/garmin-step1-metrology/dimensions.md (ONLY)
inputs_not_read: >
  tests/garmin 7x stand/*.jpg (11 source photos), tests/garmin 7x stand/Fenix+7x+charging+dock.3mf
  (grader oracle/answer), any other tests/ or experiments/ content. Per skills/3d-designer/SKILL.md
  reference-commission rule: "reconstruct the mating object from dimensions.md alone and do not
  inspect the source photos."
backend: CadQuery 2.8.0 (system python), re-imported with trimesh for measurement
status: built blind; PENDING metrologist round-trip (dimensions.md's own "Blind reference round
  trip" table stays PENDING until the metrologist overlays this build on the photos)
---

# Garmin Fenix 7X — blind mating reference, build receipt

`watch_reference.py` is the parametric CadQuery source; `watch_reference.stl` /
`watch_reference.step` are its exports. Every design-driving number in the script cites the
sheet's M-/F-/D- id and confidence grade, or is flagged `ASSUMPTION` where the sheet gave no
numeric value at all. **The caseback charge-contact pad (F-003/M-009) is deliberately NOT
modeled** — the sheet marks it `NOT READY — blocking` (OQ-01: no caseback photo exists in the
supplied evidence), and this build produces a plain flat caseback rather than fabricate contact
geometry.

## Re-imported STL measurement receipt (trimesh, not the in-memory CadQuery solid)

| Property | Value |
|---|---|
| watertight | True |
| volume | 33,642.00 mm³ |
| bounds X | [-28.391, 28.391] mm |
| bounds Y | [-33.375, 33.375] mm |
| bounds Z | [0.000, 14.900] mm |
| extents (X, Y, Z) | 56.783 × 66.750 × 14.900 mm |

- Z extent (14.900) = exact match to `CASE_THICKNESS` (M-004).
- X extent (56.783 ≈ 56.8) = exact match to `BUTTON_ENVELOPE_DIA` (M-002) — this is the
  button/pusher keep-out envelope, not the bare case diameter (see feature re-measurements
  below for the bare-case cross-check).
- Y extent (66.750) = `CASE_DIA_BAND_AXIS` (51.75) + `BAND_STUB_LENGTH` (15.0, ASSUMPTION) —
  the band stubs are the widest feature on this axis, not the case body itself.

### Feature re-measurements (sliced from the exported/re-imported STL, not asserted from parameters)

| Check | Method | Result | Sheet parameter | Match |
|---|---|---|---|---|
| Case diameter, button axis | Z=1.0 slice (clear of button pads/band stubs) | 51.747 mm | M-001 = 51.75 | exact |
| Case diameter, band axis | Z=1.0 slice | 51.737 mm | M-003 = 51.75 (assumed) | exact |
| Button envelope diameter | Z=7.45 slice (mid-height, through pads) | 56.783 mm | M-002 = 56.8 | exact |
| Case thickness | overall Z extent | 14.900 mm | M-004 = 14.9 | exact |
| Band stub width | Y=30.875 slice plane (through +Y stub) | 26.000 mm | M-005 = 26.0 | exact |
| Caseback flatness | min Z over whole mesh | 0.000000 mm | — (no F-003 geometry) | flat, as intended |

`measure_receipt.py` (kept alongside the deliverables) reproduces this pass.

## Blind-build feature inventory: sheet vs built

| Sheet ID | Feature | Built? | How | Confidence carried over |
|---|---|---|---|---|
| F-001 | Case body/bezel, round envelope | **yes** | plain right cylinder, Ø51.75 × 14.9mm, origin at case center/caseback | A (button-axis dia M-001), C (band-axis dia M-003, OQ-04), B (thickness M-004, OQ-02) |
| F-002 | Button/pusher protrusion envelope | **yes (envelope only)** | symmetric keep-out boss on D2_BUTTON_AXIS (+X/-X), built as env-circle ∩ Y/Z-limited slab; re-measured 56.783mm exact | A (envelope diameter M-002/D-001); C (count=5, individual layout — NOT modeled, see below) |
| F-003 | Caseback charge-contact pad | **NOT built (deliberate)** | plain flat caseback at Z=0, zero cuts/bumps | D, unconfirmed — sheet marks this **NOT READY — blocking** (OQ-01); no evidence, no user-approved placeholder exists |
| F-004 | Band strap width at the two lugs | **yes (bounded stub)** | two 26mm-wide × 15mm-long (ASSUMPTION) × 3mm-thick (ASSUMPTION) stub slabs at ±Y, half-embedded in the case for a robust union | A (width M-005); band overall length explicitly excluded per OQ-03, not modeled |
| F-005 | Buckle/keeper hardware | **not built** | sheet: "cosmetic only... none required unless cradle geometry extends... intersect typical worn buckle position"; non-blocking, no fit role in this case-focused reference | A (width M-006=31.4mm, recorded here for traceability, not geometrized) |
| F-006 | QuickFit lug/release collar | **not built separately** | sheet's own bounded assumption is that the collar footprint "stays within the 26mm band-width envelope, no extra radial protrusion" — i.e. it adds no information beyond the F-004 band-stub width already built | C, bounded/low-confidence |
| F-007 | Display crystal | **implicit** | body's own top face at Z=CASE_THICKNESS; no separate bezel/lens step geometry (no side-profile evidence exists to justify one — OQ-05) | C |
| F-008 | Case logo/bezel markings | **not built** | cosmetic only, no numeric bound in sheet | C |

## Assumptions not sourced from the sheet (all non-fit-critical; every one is a named CadQuery
## parameter with an `ASSUMPTION` comment in `watch_reference.py`, not a silent magic number)

| Parameter | Value | Why an assumption |
|---|---|---|
| `BUTTON_PAD_HALF_WIDTH_Y` | 9.0 mm | sheet gives an envelope diameter and a button count (5), but no individual button positions/shapes/spacing at all; this controls how far the envelope-circle bulge is carried before blending back into the case — it is NOT a claim about real button footprints |
| `BUTTON_PAD_Z_LO_FRAC` / `BUTTON_PAD_Z_HI_FRAC` | 0.15 / 0.85 | no button Z-band given; nominal band clear of both case edges |
| `BAND_STUB_LENGTH` | 15.0 mm | sheet's band-length reads (M-007, 111–115mm) are explicitly low-confidence/ambiguous (OQ-03) and marked "excluded from the cradle envelope, NOT fit-critical" — a short representative stub is modeled instead of a full-length band |
| `BAND_THICKNESS` | 3.0 mm | band cross-section thickness not given anywhere in the sheet |
| band stub Z-position (`band_z0`) | centered on case height | no lug Z-position given in the sheet |

## Conflicts and open questions carried forward, not silently resolved

- **OQ-01 (F-003, blocking)**: the caseback charge-contact pad location, pin pattern, spacing,
  and OEM cable-clip engagement geometry are entirely undocumented — no caseback photo exists in
  the 11-photo evidence set, and only generic "4-pin" product-family knowledge (no geometry) was
  found by web search. This build does **not** invent a pad location, size, or pin pattern. A
  future candidate/dock design cannot proceed on the charge-interface feature specifically until
  this is resolved (photo, cable-clip measurement, or explicit user-approved placeholder).
- **OQ-02 (M-004, thickness)**: 14.9mm is spec-only (S-12), zero photographic corroboration.
  Used as-is per the sheet; flagged here, not silently upgraded in confidence.
- **OQ-04 (M-003, band-axis diameter)**: assumed equal to the button-axis reading by visible
  round-case symmetry, never independently calipered. The model uses one shared `CASE_DIA`
  value for both axes (a true circle) rather than an ellipse, matching the sheet's own
  assumption — not a stronger claim than the sheet makes.
- **OQ-05 (seating angle / side profile)**: no side-profile photo exists at all. The case is
  modeled as a plain right cylinder for its full thickness — no taper, no bezel/crystal step,
  no seating angle — because inventing any of those would go beyond what the sheet supports.
  This is called out explicitly in the side-view render's title.
- **F-002 button count/layout (grade C)**: "5 per known Fenix 7X layout" is recorded in the
  sheet but with zero individual position data. Rather than fabricate 5 button shapes at guessed
  coordinates, this build reconstructs only the measured envelope (a symmetric keep-out boss),
  which is what the sheet's own candidate response for F-002 actually calls for ("relieve/notch
  to ≥Ø56.8mm... ONLY along D2_BUTTON_AXIS").

## Renders

- `watch_reference_top_view.png` — near-top-down view (crystal side up, looking down -Z): shows
  the round case/bezel (F-001), the symmetric button-envelope bosses on the D2_BUTTON_AXIS
  (+X/-X, F-002), and the band stubs on the D3_BAND_AXIS (+Y/-Y, F-004).
- `watch_reference_side_view.png` — left panel: side/profile 3D view, Z exaggerated 3× for
  legibility (labeled as such); right panel: true-proportion 2D cross-section outline (X=0
  plane, Y vs Z, both axes real mm) showing the plain-cylinder case profile, the flat caseback
  at Z=0 with **no charge-pad geometry**, and the band-stub exit height. Both produced with
  matplotlib (`render_views.py`) per the commission's guidance that Chromium PNG capture is
  unreliable in this environment.

## Files and SHA-256

| File | SHA-256 | Size |
|---|---|---|
| `watch_reference.py` | `3175c1e2118d0e1419a58822100cb444e1d4f0fd99c82ebd7a57267a74886958` | 9,529 B |
| `watch_reference.stl` | `adcbff5b80a50107f830f8e4e3310aaa6cb0023639a40bf1e6c60cd7f6cc0c31` | 47,284 B |
| `watch_reference.step` | `65a0f57e5e5cd4f77aa59b1163ab589c3404318409890e595659938c3d3a0536` | 76,697 B |
| `watch_reference_top_view.png` | `8c7291e6d186041a7a5ec1e26e0ae037066e2ccf15db3eff8fa3a7dc7de0d05d` | 789,215 B |
| `watch_reference_side_view.png` | `91d98f28b0aba3d9a04019071a62774add4a36b105f474693919744d4d72461c` | 534,107 B |
| `measure_receipt.py` (helper, not a primary deliverable) | `daabcceb3b98daedb1531aca35ef9e7cbafb140a4b41a3c6b7703090859463ca` | 2,674 B |
| `render_views.py` (helper, not a primary deliverable) | `69fd2810ea878726a25917d8277aabc4d132a9be4143c593ae0d44e5eda06196` | 6,691 B |

## Honest limits

- This is a blind build: no photo comparison, no overlay, no ACCEPT/REVISE verdict — that is the
  metrologist's round-trip step against `dimensions.md`'s "Blind reference round trip" table,
  still PENDING as of this commission.
- **The charge-contact interface (F-003) is entirely unmodeled.** Anyone using this reference to
  design a cradle/dock must not assume the flat caseback implies "no contacts" physically — it
  means the metrology sheet has no evidence for where they are. This is the single most
  important limitation of this file.
- F-002 (buttons) is built as an envelope-only keep-out boss, not real button geometry — do not
  read individual button shapes/positions off this model.
- F-004 band stubs are short representative placeholders (15mm), not full-length band geometry —
  band overall length is explicitly excluded from the fit-critical envelope per the sheet.
- F-005 (buckle) and F-006 (QuickFit lug collar) are not modeled as separate geometry; their
  sheet values are recorded above for traceability only.
- Case body is a plain right cylinder for its full thickness — no evidence exists for any
  taper, step, or bezel/crystal transition, so none was invented (OQ-05).
- Not a candidate/printable part: no print-plan, no orientation/support/overhang design applied
  — this file exists to be a mating-object test fixture and metrologist round-trip target, not a
  manufacturable dock part.
