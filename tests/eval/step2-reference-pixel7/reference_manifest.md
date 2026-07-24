---
contract: reference-manifest
job_id: pixel7-case-metrology
step: step2-reference-pixel7
role: designer (reference commission, blind build)
input_read: tests/eval/step1-metrology-pixel7/dimensions.md (ONLY)
inputs_not_read: >
  tests/Pixel 7 case/*.jpg (source photos), tests/Pixel 7 case/pixel7_high_detail_reference_model.stl
  (grader oracle), tests/Pixel 7 case/PixelCaseV4.3mf (case answer), any other tests/ or
  experiments/ content. Per skills/3d-designer/SKILL.md reference-commission rule: "reconstruct
  the mating object from dimensions.md alone and do not inspect the source photos."
backend: CadQuery 2.8.0 (system python), re-imported with trimesh for measurement
status: built blind; PENDING metrologist round-trip (dimensions.md's own "Reference round
  trip" table stays PENDING until the metrologist overlays this build on the photos)
---

# Google Pixel 7 — blind mating reference, build receipt

`phone_reference.py` is the parametric CadQuery source; `phone_reference.stl` /
`phone_reference.step` are its exports. Every design-driving number in the script cites the
sheet's M-/F-/D- id and confidence grade, or is flagged `ASSUMPTION` where the sheet gave no
numeric value at all (never on a fit-critical dimension — see the assumptions table below).

## Re-imported STL measurement receipt (trimesh, not the in-memory CadQuery solid)

| Property | Value |
|---|---|
| watertight | True |
| volume | 102,237.61 mm³ |
| bounds X | [-36.600, 37.200] mm |
| bounds Y | [-77.800, 77.800] mm |
| bounds Z | [-2.740, 8.700] mm |
| extents (X, Y, Z) | 73.800 × 155.600 × 11.440 mm |

- Y extent (155.600) = full L, exact match to M-001.
- X extent (73.800) = W (73.2) + one-sided button-pad protrusion (0.6, ASSUMPTION) on the
  D4_RIGHT face only — bounds are asymmetric `[-36.6, +37.2]` because the SIM-tray edge
  (D5_LEFT) has no protruding feature and the button edge does.
- Z extent (11.440) = T (8.7) + camera-bump protrusion (2.74) = **exact match** to SPEC-01's
  independently-stated hands-on figure "thickness rises to 11.44 mm at the camera bar" — this
  is a genuine cross-check the sheet noted only as an arithmetic derivation (M-007); the
  re-imported solid reproduces it geometrically.

### Feature re-measurements (sliced from the exported/re-imported STL, not asserted from parameters)

| Check | Method | Result | Sheet parameter | Match |
|---|---|---|---|---|
| Corner radius | Z=4 slice (clear of camera bar); min distance from the sharp D4_RIGHT/D2_TOP corner point to the actual boundary, R = d_min·(√2+1) | R = 9.500 mm | M-004 R_CORNER = 9.5 | exact |
| Camera-bar footprint | Z=-1 slice (below back plane) | x∈[-36.6, 36.6] (width 73.2), y∈[57.4, 77.8] | M-008 width=W=73.2; M-005 height=20.4 (77.8-57.4) | exact |
| Camera-bump peak | min(Z) over whole mesh | Z = -2.740 mm | M-007 = 2.74 | exact |
| Button pads | Z=4.35 (mid-thickness) slice, X>36.9 boundary points | Y-corners at {22.8, 32.8} and {37.8, 53.8} | Power [22.8,32.8] (M-012 ctr 27.8, len 10); Volume [37.8,53.8] (M-011 ctr 45.8, len 16) | exact |

`measure_receipt.py` (kept alongside the deliverables) reproduces this pass.

## Blind-build feature inventory: sheet vs built

| Sheet ID | Feature | Built? | How | Confidence carried over |
|---|---|---|---|---|
| F-001 | Body envelope, rounded-rect prism | **yes** | 155.6×73.2×8.7 mm slab, D1_CTR-centered | B (SPEC), A (caliper corroboration, unused per sheet's own guidance) |
| F-002 | Corner radius ×4 | **yes** | `.edges("|Z").fillet(9.5)` on the body — re-measured 9.500 mm exact | B, nominal of 9.5±1.5 band |
| F-003 | Camera bar / bump | **yes** | full-W×20.4mm box, top-anchored at D2_TOP, protrudes 2.74mm into -Z | mixed A(height)/B(protrusion)/C(width) |
| — | M-006 metal-trim sub-height (14.3mm) | **partial** | shallow 0.15mm witness groove at Y=63.5, not a separate protrusion step (sheet: "cosmetic sub-detail only, no measured step height exists") | A (position only; no step-height number in sheet) |
| F-004 | Lens-oval cutout | **yes (nominal)** | 33×7mm shallow recess (1.0mm, ASSUMPTION depth), top margin 6.2mm below D2_TOP, X centered (ASSUMPTION, no X offset given) | C (size), A (top margin) |
| F-005 | Small hole beside lens oval | **not built** | sheet gives no numeric size or position for F-005 (only "cosmetic-only bounded envelope") — fabricating a size would be an unlabeled magic number; omitted and documented instead | C, no digits at all |
| F-006 | Volume rocker | **yes (bounded)** | raised pad, center Y=45.8 (nominal of 37.8-53.8 range), length 16, ASSUMPTION protrusion/Z-span | C |
| F-007 | Power button | **yes (bounded)** | raised pad, center Y=27.8 (nominal of 19.8-33.8 range), length 10, ASSUMPTION protrusion/Z-span | C |
| F-008 | SIM tray | **yes (bounded)** | shallow recess, center Y=42.8 (nominal of 36.3-49.3 range), length 13, ASSUMPTION depth/Z-span | C |
| F-009 | Top mic hole | **yes (bounded)** | small dimple, X=-22.6 (nominal of 10-18mm offset range), ASSUMPTION diameter/depth | C |
| F-010 | USB-C port | **yes (bounded)** | 8.5×3mm cutout, X centered, ASSUMPTION depth/Z-position | B (center-X), C (size) |
| F-011 | Bottom-left grille | **yes (bounded)** | 6mm-wide cutout, X=-25.6 (nominal of "11mm inset from D5_LEFT corner"), ASSUMPTION depth/Z-span | C |
| F-012 | Bottom-right grille | **yes (bounded)** | 6mm-wide cutout, X=24.6 (nominal of "12mm inset from D4_RIGHT corner"), ASSUMPTION depth/Z-span | C |
| F-013 | Screen/front-glass plane | **yes (implicit)** | body's own top face at Z=+T; sheet resolves no separate lip (grade D, OQ-08) so no extra geometry added | D |
| F-014 | Back-panel finish step | **not built** | cosmetic only, sheet: "no case-fit effect", no numeric bound given | C |
| F-015 | Google "G" logo | **not built** | cosmetic only, no numeric bound given | C |

## Assumptions not sourced from the sheet (all non-fit-critical; every one is a named CadQuery
## parameter with an `ASSUMPTION` comment in `phone_reference.py`, not a silent magic number)

| Parameter | Value | Why an assumption |
|---|---|---|
| `LENS_OVAL_RECESS_DEPTH` | 1.0 mm | F-004 explicitly "non-fit-critical"; sheet gives no depth |
| `LENS_OVAL_X` | 0.0 (centered) | sheet gives no X-offset for the oval within the camera bar |
| `BTN_PROTRUSION` | 0.6 mm | sheet gives button Y-center/length only, no radial reveal |
| `BTN_Z_SPAN` | 4.0 mm | no button height across the frame thickness given |
| `SIM_TRAY_DEPTH` / `SIM_TRAY_Z_SPAN` | 0.3 / 2.0 mm | no tray recess depth or Z-band given |
| `MIC_HOLE_SIZE` / `MIC_HOLE_DEPTH` | 1.2 / 1.0 mm | no mic-hole diameter given |
| `USBC_DEPTH` / `USBC_CENTER_Z` | 4.0 mm / T/2 | no port bore depth or Z-position given |
| `GRILLE_Z_SPAN` / `GRILLE_DEPTH` | 1.5 / 2.0 mm | no grille height or depth given |

## Conflicts and open questions carried forward, not silently resolved

- **OQ-01 (thickness)**: sheet's own three independent caliper reads (9.5/9.6/9.8mm) cluster
  ~0.8-1.1mm above the 8.7mm SPEC nominal used here for `T`. Recorded in the script as
  `THICKNESS_CALIPER_CLUSTER_MM = (9.5, 9.6, 9.8)` (unused in geometry) so the conflict stays
  visible, per the sheet's explicit instruction not to silently resolve it.
- **OQ-07 (handedness)**: built exactly as the sheet states (buttons on D4_RIGHT/+X, SIM tray
  on D5_LEFT/-X) — this build does not itself re-confirm handedness; that is the metrologist's
  round-trip step, out of scope here.
- **F-005**: intentionally not modeled — no numeric bound exists in the sheet to model against.

## Renders

- `phone_reference_back_view.png` — 3/4 back view (looking up the -Z outward normal, D4_RIGHT
  edge toward camera): shows the camera bar, lens-oval recess, metal-trim witness groove,
  rounded corners, and the button/SIM-tray/mic notches at the edges.
- `phone_reference_side_section.png` — left panel: half-section solid (X≤0 kept), Z
  exaggerated 6× and labeled as such for legibility; right panel: true-proportion 2D outline
  of the X=0 cross-section (Y vs Z, both axes real mm) showing the flat body (Z=0 to 8.7),
  the camera-bump step down to Z=-2.74 near D2_TOP, and the USB-C notch near D3_BOT.
  Both were produced with matplotlib (`render_views.py`) per the commission's guidance that
  Chromium PNG capture is unreliable in this environment.

## Files and SHA-256

| File | SHA-256 | Size |
|---|---|---|
| `phone_reference.py` | `b51cb2df4066f72feff429e594801a8013582f232dbfb30fda56e50f774a64f7` | 10,832 B |
| `phone_reference.stl` | `5d683184b814d7089b4075354b81aa45aa8aaae35aa0bb45c12324aaea692b7f` | 66,684 B |
| `phone_reference.step` | `3378974398b8c5309c40633801e75e3b161eba5157fb502cc3e645d9a27e04a1` | 172,048 B |
| `phone_reference_back_view.png` | `5ae3c9bed0c8b8f4c45989eb0e744e97e532691722b07bda0aee5607878cffb4` | 539,075 B |
| `phone_reference_side_section.png` | `f4b06fb4d0bcab786cc497ca4b2484b98e920b62e78237a8dcf8e5d080524611` | 479,160 B |
| `render_views.py` (render helper, not a primary deliverable) | `f63fefaa2960a68524914ce57288dc27598359f36c751109617375aebfa49891` | 6,460 B |

## Honest limits

- This is a blind build: no photo comparison, no overlay, no ACCEPT/REVISE verdict — that is
  the metrologist's round-trip step against `dimensions.md`'s "Reference round trip" table,
  still PENDING as of this commission.
- Every C-grade / bounded-range feature (buttons, SIM tray, mic hole, USB-C, grilles, lens
  oval) is built at its **nominal** point estimate, not its full range — ambiguity is visible
  in the script's comments and this manifest's assumptions table, not hidden.
- Secondary/cosmetic feature depths and Z-spans (buttons, tray, mic, USB-C, grilles) are
  reasonable defaults, not sheet values — flagged `ASSUMPTION` throughout; none of them affect
  a fit-critical dimension (F-001, F-002, F-003 are the only fit-critical features and every
  number there is a direct sheet citation, independently re-measured off the exported STL
  above).
- F-005 and F-014/F-015 are intentionally not modeled (no numeric bound in the sheet).
- Not a candidate/printable part: no print-plan, no orientation/support/overhang design was
  applied — this file exists to be a mating-object test fixture and metrologist round-trip
  target, not a manufacturable part.
