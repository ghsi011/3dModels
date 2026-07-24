# Method — Pixel 7 case metrology

Companion to `dimensions.md` (the authoritative contract). This file explains *how* each
key number was obtained and lists conflicts/open questions in narrative form. Full
per-dimension source/confidence/datum detail lives in `dimensions.md`; this file does not
duplicate that table, it explains the reasoning behind it.

## Inputs read

- All 17 user photos in `tests/Pixel 7 case/*.jpg` — inspected at native resolution via
  cropped zooms (crops saved under `evidence/metrology/` in this folder).
- Google Pixel 7 official/aggregated specs (GSMArena spec + hands-on review, cross-checked
  against o2.co.uk, dimensions.com, phonesbysize.com) — see Sources table in
  `dimensions.md` for URLs and access date.
- **Not read**: `PixelCaseV4.3mf`, `pixel7_high_detail_reference_model.stl`, any other
  `tests/` folder, `experiments/`, round-5 arms — all out of scope per the commission.

## Photo inventory and what each one shows

| Photo (PXL_...) | Content |
|---|---|
| 161758905 | Front/screen overview, held at an angle |
| 161805402 | Right edge — volume rocker + power button |
| 161809053 | Left edge — SIM tray |
| 161811840 | Back overview — camera bar, dual lens, "G" logo |
| 161814868 | Top edge — single mic hole |
| 161817658 | Bottom edge — left speaker grille, USB-C, right speaker/mic grille |
| 162140395 | Caliper: **155.0 mm** — overall length, screen-face up |
| 162156525 | Caliper: **71.9 mm** — overall width, jaw set near the top corner |
| 162226348 | Caliper: **9.6 mm** — thickness, needle jaws at the corner near USB-C |
| 162250060 | Caliper: **9.8 mm** — thickness, jaws at a side button |
| 162333722 | Caliper: reading ≈20–27 mm, **excluded** — middle digit illegible on the 7-segment display and the jaw's contact points don't clearly correspond to a named feature |
| 162415355 | Caliper: **9.5 mm** — thickness, jaws at a side button |
| 162610764 | Caliper: **20.4 mm** — top edge to the camera-bar/matte-back transition (full bar height) |
| 162707747 | Caliper: **6.2 mm** — top edge to the top of the lens-oval cutout |
| 162943302 | Caliper: **84.2 mm**, **excluded** — positioned as if measuring width at camera-bar level, but 11 mm over the 73.2 mm spec; most likely the caliper wasn't zeroed before this reading (a suspiciously round excess). Not used. |
| 162947392 | Ruler beam laid across the camera bar, no new digit captured — used only to corroborate that the bar runs close to full device width |
| 163021288 | Caliper: **14.3 mm** — top edge to the metal-trim/matte-back transition (metal insert sub-height, nested inside the 20.4 mm figure) |

Reading method: every caliper LCD was re-cropped and upscaled from the native ~12 MP
source (not just eyeballed at thumbnail size) before the digit was recorded, and the jaw
contact points were separately cropped and inspected to identify *what* was being measured,
not just the number. This caught the digit-format convention this caliper always uses
(one decimal place immediately before the last digit — e.g. a raw "062" display is 6.2 mm,
not 0.62 mm), which matters for the 6.2 mm and 20.4/14.3 mm readings.

## How the fit band was decided

`fdm-design.md` §4 fit classes (per side): press 0.0–0.1, snug 0.1–0.2, sliding 0.15–0.3,
loose 0.3–0.5, free-rotation 0.4–0.7 mm. The case cavity around the phone body is a
**captured, non-moving fit** (the skill's own worked example for this situation targets
snug–sliding, ≈0.1–0.3 mm/side) — so `dimensions.md` M-019 specifies **snug–sliding,
0.10–0.30 mm/side**, explicit min and max, not a one-sided floor. Camera-bar and
button/port windows are separately specified as **loose, 0.30–0.50 mm/side** (M-020/021/022)
because those are non-structural clearance openings where guaranteed margin matters more
than a snug hold, and because button/port position confidence is only grade C.

## Conflicts and open questions (see `dimensions.md` for the full table)

1. **Thickness conflict (OQ-01).** Three independent caliper reads (9.5/9.6/9.8 mm) all
   cluster about 0.8–1.1 mm above the 8.7 mm official body thickness. All three were taken
   at or near a side button, and the caliper used pointed ("internal") jaws rather than
   flat external jaws pressed perpendicular to the faces — both are plausible sources of a
   systematic over-read, but the consistency across three independent photos (spread only
   0.3 mm) means this isn't simple random error either. I did **not** average this away.
   `dimensions.md` uses 8.7 mm as the provisional nominal and flags a flat-region
   re-measurement (away from any button, jaws perpendicular) as required before the case
   wall-clearance number is finalized.
2. **Width under-read (OQ-06).** Direct caliper width (71.9 mm) sits 1.3 mm under the
   73.2 mm official spec — a bigger gap than length's 0.6 mm gap. The photo shows the jaw
   set very close to the top corner's radius, which would explain an under-read versus the
   true straight-side maximum. Resolved by using the larger, spec-corroborated 73.2 mm as
   the cavity-floor nominal rather than picking one value arbitrarily.
3. **Two excluded caliper photos (OQ-03).** 162333722 (illegible middle digit, unclear
   feature) and 162943302 (84.2 mm, ~11 mm over spec, most likely a non-zeroed jaw) are
   both left out of the dimension register rather than force-fit to a feature.
4. **Camera-bump protrusion (OQ-02).** No photo directly calipers how far the camera bar
   stands proud of the back panel. `dimensions.md` M-007 uses arithmetic from a third-party
   hands-on figure (11.44 mm max device thickness at the bump, GSMArena) minus the 8.7 mm
   spec body thickness ≈ 2.74 mm — graded B (derived), not A, and flagged as needing a
   direct step-height caliper reading before the case's camera-ring height is finalized.
5. **Button/port positions (OQ-04).** No photo has a ruler or caliper reading anchored at
   the exact button/port location, so Y-positions for the volume rocker, power button, top
   mic, and the two bottom grilles are photo-proportional estimates only (grade C, wide
   ranges stated in `dimensions.md`). The named bounded response is a loose window sized to
   the full stated range (or one shared bottom slot) rather than a tight punctual cutout —
   not a claim that the point estimate is precise.
6. **Corner radius (OQ-05).** Measured once, from one corner, using the embedded caliper
   ruler in the same frame as a scale reference (155.0 mm length photo) — R ≈ 9.5 ± 1.5 mm.
   Not cross-checked against a second corner. `fdm-design.md` already treats box corners as
   the least-accurate region to fit tightly, so the wide uncertainty band is an acceptable
   starting point rather than a blocker.
7. **Handedness (OQ-07).** No single photo shows the front face and a labeled edge in the
   same frame, so "buttons on the right, SIM on the left" is inferred by chaining five
   separate photos together against the standard phone convention, not confirmed in one
   shot. Internally consistent, low risk, but named for the round-trip pass to re-check.

## Round-trip status

Not applicable to this commission. This is step ① (metrology only) — no CAD reference
model was or should be built here, and none was read. `dimensions.md`'s "Reference round
trip" section is marked PENDING. A later designer commission would build the mating
reference blind from `dimensions.md` alone, after which this role would overlay that
result on the photos above and record ACCEPT/REVISE before the sheet can move past DRAFT.

## Honest limits of this pass

- All photos are handheld and taken at an angle, not orthographic — every image-derived
  (grade C) number carries meaningful uncertainty, stated as ranges rather than false
  precision.
- No photo isolates camera-bump protrusion, button positions, or port positions with an
  adjacent ruler/caliper — those numbers are the weakest in the sheet and are named
  explicitly rather than hidden inside a confident-looking table.
- This was a single autonomous metrology pass with no live user Q&A; the C-grade
  assumptions carry a named bounded design response (per the confidence-grade rules) but
  have not been explicitly user-approved. `dimensions.md` status is `DRAFT`, not
  `ACCEPTED`, for that reason — a human should review OQ-01 through OQ-08 before this sheet
  is used to commission a blind reference build.
