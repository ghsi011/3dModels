# J Class yacht base — translucent text sample coupon (print notes)

## What's in the folder
**Coupon A — the flat thickness ladder**
- `model.py` — the parametric CadQuery source (all knobs are named constants at the top)
- `verify.py` — Phase 4 verification; runs on the **exported STLs re-imported** with trimesh
- `sample_base.stl` — the translucent plate, with the text cut in as recesses → **MAIN nozzle**
- `sample_text_cf.stl` — the inlay bodies for the left column only → **AUX nozzle**
- `sample_text_all.stl` — every recess solid (both columns + zone labels), reference/debug
- `sample_coupon.step` — combined, for sharing / re-import
- `sample_readability.png` — top view (must read correctly) + bottom view (must mirror)
- `sample_section.png` — section along the ladder, text layer vs cover

**Coupon B — the real-sea reality check**
- `sea_model.py` — cuts a real chunk out of the source STL and recesses the same word into it
- `verify_sea.py` — Phase 4 verification for coupon B, plus the **ray-cast cover measurement**
- `sea_base.stl` — the sea chunk with the text cut in as recesses → **MAIN nozzle**
- `sea_text_cf.stl` — the inlay bodies for the left column only → **AUX nozzle**
- `sea_text_all.stl` — every recess solid (both columns), reference/debug
- `sea_readability.png` — top view (must read correctly) + bottom view (must mirror)
- `sea_coverage.png` — heightmap of the translucent cover over each letter, with coupon A's
  rungs drawn as dashed contours

**The print job**
- `place_coupons.py` — puts A and B side by side on one plate and checks the combined job;
  writes `sea_base_placed.stl` / `sea_text_cf_placed.stl` (the originals are never touched)
- `make_bambu_3mf.py` — welds the four STLs into a **Bambu Studio project 3MF with all print
  settings and the per-part filament assignment already baked in**
- `yacht_sample_FINAL.3mf` — **this is the file to print.** Import and slice; nothing to set
- `both_coupons.3mf` / `sample_coupon.3mf` / `bambu_test.3mf` — earlier geometry-only 3MFs, superseded
- `reference_x2d.3mf` — a project the **user actually saved from their own X2D**, used as the
  byte-shape ground truth for everything `make_bambu_3mf.py` emits

**Source**
- `jclass wcrew big.stl` — the source model (Printables 1093934, designer John Swamp)

## Why this coupon exists
The gift is the yacht printed with its **base in translucent filament and the birthday text
recessed into the underside, mirrored**, so it reads correctly when you look down through the
base. Three things are unknown and none of them can be answered in CAD: how much translucent
PETG you can still read through, whether a dark PETG-CF inlay beats a plain air-gap recess,
and whether the real font size survives CF fuzz. This coupon answers all three in one
~13 g print so the 150 mm+ yacht is only printed once.

Final base text (not on the coupon — it lives in `FINAL_LINES` in `model.py`):
`Oh the places you'll go!` / `Happy birthday Abba!` / `24.07.2026`

A **second coupon (B)** was added afterwards to close the one gap coupon A cannot cover —
the real base's top is a sculpted wavy sea, not a flat window. See *Coupon B* below. Both
coupons now print together as one job, ~20 g.

## Measured facts about the source STL
Established with trimesh on `jclass wcrew big.stl`, not estimated:
- Model is **149.55 mm tall**. The designer recommends printing **≥150 mm**, so 100 % scale is
  borderline; **105 % → 157 mm** is the safer pick. *(Scale is still open — see risks.)*
- The base is a rectangular slab, footprint **63.67 × 137.50 mm** (X 86.88–150.55,
  Y 40.67–178.17).
- The underside is **dead flat at z = 0** — cross-sections at z = 0.5 / 1.0 / 1.5 come back
  100 % solid rectangles. That is what makes bottom-face text possible at all.
- The top of the base is a sculpted wavy "sea", **not flat**. Its lowest up-facing flats sit at
  **z ≈ 2.1 mm**, so the slab is only ~2.1 mm thick at its thinnest, and only **~20 % of the top
  area is flat** — the rest is sloped wave. The final text is therefore read through a wavy
  surface, not a window.
- The STL is **not watertight** as supplied (276,010 faces). *Later finding, from coupon B:* as
  a face soup it is actually closed — what fails is **capping** a cut, and **manifold3d takes the
  raw file directly** (status `NoError`, volume 45,850 mm³). So booleans on the real base go
  through manifold3d, not through trimesh repair.
- The **hull body occupies X ≈ 99–115**, so it blocks anything read from above in that band.
  The usable clear sea strip is **X 115–150** — ~35 mm wide over the full 137.5 mm length, and
  the only place the final text can go. Sea top in that strip measures **z 1.62 – 5.49 mm**.

## Geometry summary (coupon A — the flat ladder)
Flat plate, **68.0 × 62.0 mm**, flat underside on z = 0, stepping up along +Y through four
zones of 15 mm each (plus 1 mm edge margin at both ends). Per zone the translucent cover left
**over** the text is 1.0 / 1.6 / 2.2 / 3.0 mm, so total plate thickness is
**1.6 / 2.2 / 2.8 / 3.6 mm** = **8 / 11 / 14 / 18 layers at 0.2 mm, all exact**. The real base's
measured minimum is 2.1 mm, and the ladder still brackets it on both sides.

The ladder is chosen so every zone top lands on a whole layer. The obvious rung would be the
measured 2.1 mm, but 2.1 + 0.6 recess = 2.7 mm = 13.5 layers, so the slicer would round it — and
zones 2 and 3 are precisely the ones closest to the real base, i.e. the measurements you least
want fudged. 2.2 mm vs the measured 2.1 mm is a 0.1 mm difference no legibility test can
resolve, so aligning to whole layers is strictly better.

Text recess is **0.6 mm deep = exactly 3 layers @ 0.2**, cut into the **bottom** face.

Each zone carries the word **"Abba" twice at true final size** (Arial Bold, 10 mm nominal,
measured 24.7 × 7.3 mm, stems p25 = 1.35 mm / median 1.45 mm):

| column | X centre | contents | what it tests |
|---|---|---|---|
| LEFT | −14.5 mm | filled with indigo **PETG-CF** | the dual-material inlay |
| RIGHT | +14.5 mm | left as an **open recess** | the single-material air gap |

A zone label (`1.0` / `1.6` / `2.2` / `3.0`, 6 mm, rotated 90°) is engraved as a **bare** recess
in the strip at x = −30. Deliberately never filled with CF: at 6 mm the stems are ~0.85 mm,
under the CF minimum, whereas an open recess that narrow prints fine.

Text is drawn normally in the top-down (+Z) view and recessed into the bottom face — so it
reads **correctly from above through the material** and looks **mirrored** when you look at the
underside directly. That is the whole point, and `sample_readability.png` proves it.

Material: translucent PETG **10.34 cm³ (~13.1 g)**, PETG-CF **0.194 cm³ (~0.25 g)**,
total **~13.4 g**. Target print time **under 1 hour**.

## Verification — coupon A (Phase 4, all checks pass)
- Both meshes watertight; underside flat on z = 0; extents 68.00 × 62.00; tallest zone 3.60 mm
- All four zone tops land on `TEXT_DEPTH + cover` within 0.02 mm
- **Every zone top is a whole number of 0.2 mm layers** (8 / 11 / 14 / 18), and the 0.6 mm text
  recess likewise (3 layers) — asserted, not assumed
- Text starts at z = 0 and stops exactly at 0.6 mm — it never breaks through the cover
- Text stays >1 mm inside the footprint in both X and Y
- Every zone has exactly one CF word, and it is on the LEFT column only
- CF stem width **p25 = 1.35 mm ≥ 1.2 mm** (3 × 0.4 nozzle); cap height 7.3 mm ≥ 6 mm
- Measurement audit: BASE_X 63.67, BASE_MIN_THK 2.1, TEXT_DEPTH 0.6 and WORD_SIZE 10 all
  accounted for in the geometry. The BASE_MIN_THK check now asserts a ladder rung sits **within
  0.15 mm** of the measured 2.1 mm (2.2 does), rather than requiring an exact match

## Params → what they fix (top of `model.py`)
| symptom / want | change |
|---|---|
| text too faint at every thickness | `TEXT_DEPTH` 0.6 → 0.8 (4 layers) |
| CF letters fuzzy, counters filled in | `WORD_SIZE` 10 → 12 (stems scale ~0.14 × size) |
| want other cover thicknesses tested | `ZONE_COVER` `[1.0, 1.6, 2.2, 3.0]` — keep `cover + TEXT_DEPTH` a whole 0.2 mm layer |
| coupon too long / want a shorter print | `ZONE_Y` 15, or drop a `ZONE_COVER` entry |
| columns too close / too near the edge | `COL_OFFSET` 14.5 |
| zone label clipped at the left edge | `LABEL_X` −30.0 (leaves 1.67 mm of wall) |
| printing the yacht at 105 % | `SCALE` 1.0 → 1.05 — scales plate **and** text together |
| different font / weight | `FONT` / `FONT_KIND` (bold only — CF needs the stem width) |
| the real base wording | `FINAL_LINES` |
| reference-only, do not "fix" | `BASE_X` / `BASE_Y` / `BASE_MIN_THK` are measured values |

Re-run `python model.py` to export, then `python verify.py` — never export without the checks.

## Coupon B — the real-sea reality check (`sea_model.py`)
Coupon A is a flat plate. That is what makes it a clean experiment — it isolates cover
thickness with everything else held constant — and it is also its one blind spot: it cannot
show what the base's **sculpted wavy sea surface** does to the letters. That was the biggest
listed risk, and coupon B is the answer to it.

Coupon B cuts a **real chunk straight out of `jclass wcrew big.stl`** — the genuine sea
sculpt — and recesses the **same word, same font, same size, same 0.6 mm depth** into its
underside. Printed side by side with coupon A, the difference between them at equal local
cover **is** the wave effect. Nothing else changes between the two.

Where the chunk comes from — this is not an arbitrary crop:
- The **hull body occupies X ≈ 99–115** of the base's X 86.88–150.55, so it physically blocks
  anything read from above in that band. Text there is invisible no matter how thin the cover.
- The remaining **clear sea strip is X 115–150** — ~35 mm wide, running the full 137.5 mm
  length. **That is where the final text has to live anyway**: three lines at ~11 mm pitch is
  the only way they fit in 35 mm. So the chunk is representative of the real design, not of
  "some waves".
- The chunk is taken at **X 116–150, Y 60–122 → 34 × 62 mm** (`CUT_X0/X1`, `CUT_Y0/Y1`,
  `CUT_Z_TOP` 6.0 — above the highest sea point and below the rigging that overhangs the
  strip). 62 mm matches coupon A's length so the two sit level on the plate.

Layout mirrors the final design: the text **lines run along Y**. Two columns
(`COL_OFFSET` 7.5 mm) × two rows (`ROW_OFFSET` 15 mm) = **4 words**, with the same
convention as coupon A:

| column | X centre | contents | what it tests |
|---|---|---|---|
| LEFT | −7.5 mm | filled with indigo **PETG-CF** | the inlay, seen through waves |
| RIGHT | +7.5 mm | left as an **open recess** | the air gap, seen through waves |

### Measured local cover over the letters (ray-cast, not estimated)
Coupon A's ladder gives one number per zone. Coupon B has no such luxury — the cover over
every letter is whatever the sea sculpt happens to leave there — so `verify_sea.py` measures
it: rays fired straight up from just above the recess ceiling, first hit on the sea surface,
**882 samples on a 0.4 mm grid** falling inside a letter. That distance *is* the translucent
material each letter has to be read through.

| region | cover above the text (mm) |
|---|---|
| **ALL TEXT** (882 samples) | min **1.02** / p5 **1.24** / median **1.58** / p95 **2.77** / max **3.34** |
| word 1 LEFT/BOTTOM — PETG-CF | median **1.49** |
| word 2 LEFT/TOP — PETG-CF | median **1.47** |
| word 3 RIGHT/BOTTOM — bare | median **1.55** |
| word 4 RIGHT/TOP — bare | median **1.75** |

Two readings matter and both should be stated explicitly:
- **Each word spans roughly coupon A's rung 1 to rung 4 within itself** (1.0 → 3.0 mm). Coupon
  B is therefore not "one rung with waves added" — **every word is its own mini-ladder**, and
  you should expect letters of the same word to read differently.
- **The four words' medians are close** (1.47–1.75 mm). So any legibility difference *between*
  the four words is wave **shape** — crest vs trough vs slope — and **not** wave height. That
  is the comparison to make when the print comes off.

`sea_coverage.png` renders this as a heightmap with the letter outlines overlaid and coupon
A's 1.0 / 1.6 / 2.2 / 3.0 rungs drawn as dashed contours, so you can see which letters sit
under a crest and which under a trough before you even look at the plastic.

### Two deliberate geometry deviations (recorded honestly)
Coupon B is billed as "an unmodified chunk of the real STL". It is *almost* that. Two
knowingly-introduced departures, both far below print resolution, both worth writing down:
- **The chunk is cut 0.01 mm above the source's z-min** (`CUT_Z_BOT`) and then dropped back
  onto z = 0. The source underside carries ~1.4 µm of float noise, which is enough to stop any
  capping/boolean from closing cleanly there. This buys a genuinely planar 2-triangle underside
  for **10 µm of material — 1/20 of a layer**.
- **`_unpinch()` nudges 6 coincident vertices 2 µm apart** along their vertex normals. The sea
  sculpt is a marching-cubes surface that touches itself at **3 points** inside this chunk;
  manifold3d tolerates that (the vertices have different indices), but a binary STL has no
  indices, so on reload they merge by position and each contact becomes a non-manifold edge —
  the exported file would then read as *not* watertight. Cost: **0.0002 mm³** of volume.

### Why the extraction is a manifold3d boolean, not `slice_plane`
Worth recording so nobody "simplifies" it back. The obvious route — repeated
`trimesh.slice_plane(cap=True)` — does **not** work here. The source is reported non-watertight
(276,010 faces), but as a face soup it is actually closed; what breaks is the **capping**, which
leaves **3,461 unshared edges** (3,427 along the bottom, 34 on the +X cap). trimesh's repair
does not close them, and the text boolean then dies with *"Not all meshes are volumes!"*.
manifold3d ingests the raw source directly (status `NoError`, volume 45,850 mm³), so the whole
cut is done as **one boolean intersection against a box**.

### Verification — coupon B (`verify_sea.py`, all checks pass)
Same discipline as coupon A: everything runs on the **exported STLs re-imported**.
- Sea base watertight, **one connected body**, winding consistent, positive volume; chunk
  extents match `CUT_X1−CUT_X0` × `CUT_Y1−CUT_Y0`; volume sane against solid-box bounds
- Underside sits at **exactly z = 0**, is a **real down-facing face** (not a stray vertex), and
  its area + the text openings = the full 34 × 62 mm footprint
- Recess is exactly **z = 0 → 0.6 mm = 3 layers**; ray-casting confirms the recess ceiling is at
  0.6 mm **under every letter**, the plate starts at z = 0 **everywhere outside** them, and there
  is **no stray geometry inside the recess volume**
- Text stays **≥ 1.5 mm** clear of every chunk edge in X and Y
- CF text present, **LEFT column only**, present in both rows, and a **strict subset** of the
  full text volume; CF stem width ≥ 1.2 mm (3 × 0.4 nozzle), scanned along the rotated axis
- Every text sample sees sea surface above it, minimum cover > 0.3 mm, and the hit count above
  each letter is **odd** — i.e. a single solid shell, no internal voids in the light path
- Renders `sea_readability.png` (top reads correctly, bottom mirrors) and `sea_coverage.png`

### Params → what they fix (top of `sea_model.py`)
| symptom / want | change |
|---|---|
| want a different patch of sea (flatter, or more extreme waves) | `CUT_X0/CUT_X1`, `CUT_Y0/CUT_Y1` — **stay inside X 115–150**, the hull blocks anything below that |
| chunk catches the rigging above the strip | `CUT_Z_TOP` 6.0 (highest sea point is 5.49) |
| chunk fails to close / underside not planar | `CUT_Z_BOT` 0.01 — do not set it to 0 |
| STL reloads as not watertight | `_unpinch()`'s `eps` (2 µm) — the sea sculpt self-touches |
| words too close together / to the edges | `COL_OFFSET` 7.5, `ROW_OFFSET` 15.0 |
| must stay identical to coupon A, do not "improve" | `TEXT_DEPTH`, `FONT`, `FONT_KIND`, `WORD`, `WORD_SIZE` — the whole comparison depends on these matching `model.py` |

Re-run `python sea_model.py` to export, then `python verify_sea.py` — same rule as coupon A,
never export without the checks. Then re-run `python place_coupons.py` and rebuild the 3MF.

## The combined print job (`place_coupons.py`)
The two coupons only mean anything **compared with each other**, so they have to come off the
same plate, in the same session, with the same filament, the same first layer and the same
light when you hold them up. `place_coupons.py` drops coupon B to the right of coupon A, both
undersides on z = 0, both centred on Y = 0, and re-checks the whole job.

| | value |
|---|---|
| gap between the coupons | **6.000 mm** of clear plate |
| combined bounding box | **108.00 × 62.00 × 5.63 mm** |
| translucent PETG (**MAIN**) | **15.473 cm³ ≈ 19.65 g** |
| indigo PETG-CF (**AUX**) | **0.291 cm³ ≈ 0.37 g** |
| total | **15.764 cm³ ≈ 20.02 g** (at 1.27 g/cm³) |

It writes `*_placed.stl` copies rather than editing anything — `model.py` and `sea_model.py`
stay authoritative — and asserts the coupons do not overlap, both undersides are on z = 0, both
share a Y centre, and coupon B's CF text moved with its base.

## Orientation
**TEXT-FACE DOWN on the build plate**, flat underside on z = 0, exactly as modelled — **both
coupons**, which is why `place_coupons.py` asserts both undersides are on z = 0. The text
recess then prints as the **first 3 layers**, which is where an FDM printer is sharpest, and the
stepped top (A) / sea surface (B) faces up. No supports, no bridging, zero overhang. Printing it
any other way puts the read face against support or in mid-air and there is no reason to.

## Material & nozzle assignment (Bambu Lab X2D Combo, dual nozzle + AMS 2 Pro)
| body | material | nozzle | why |
|---|---|---|---|
| `sample_base.stl` (A) | translucent PETG | **MAIN** | direct drive, 40 mm³/s, flow-calibrated, best surface finish. The base is the showpiece and ~98 % of the volume, so it gets the good nozzle. |
| `sample_text_cf.stl` (A) | indigo PETG-CF | **AUX** | small volume, and the aux's limits don't bite here. |
| `sea_base_placed.stl` (B) | translucent PETG | **MAIN** | same reasoning; B must print in the same material as A or the comparison is worthless. |
| `sea_text_cf_placed.stl` (B) | indigo PETG-CF | **AUX** | same. |

**Which extruder is which — verified, not assumed.** The X2D machine profile declares
`extruder_type = ['Direct Drive', 'Bowden']`, so **extruder 1 = MAIN (direct drive)** and
**extruder 2 = AUX (Bowden)**. Confirmed three ways: that key; the process preset pairing the
four extruder variants with `print_extruder_id = ['1','1','2','2']`; and a real X2D project
saved by this Studio build carrying the same `printer_extruder_id`.

Reasoning worth keeping:
- Bambu's X2D filament-compatibility guide rates **CF/GF as "print with caution" on the aux**
  hotend — permitted, higher clog risk, not the primary recommendation. Both extruders' gears
  and the aux nozzle are **hardened steel (HRA ~74)**, so abrasives wear them gradually rather
  than instantly. Here the CF is **~0.25 g confined to the bottom 3 layers**, so exposure is
  negligible.
- The aux is capped at **200 mm/s and 1000 mm/s²** — irrelevant for 8 small words.
- **PETG-CF is chemically PETG**, so it welds to the translucent PETG perfectly: same
  temperatures, no delamination risk at the interface.
- **PETG-CF is matte**, and that matters. A glossy dark inlay would glare and wash out the
  contrast when read through the translucent layer; matte keeps it black.
- This is also the X2D near-zero-purge exploit: dominant volume + visible surface on main,
  tiny second material on aux.
- Note for the full yacht (not for this coupon): **dual-nozzle jobs shrink the build volume to
  235.5 × 256 × 256 mm.** Check the hull fits before slicing.

## Slicing (Bambu Studio, X2D) — the settings are already in the file
**This section used to be a list of things to set by hand. It isn't any more.** The deliverable
to print is **`yacht_sample_FINAL.3mf`**, produced by `make_bambu_3mf.py`. It is a real **Bambu
Studio project 3MF** — not bare geometry — targeting **Bambu Studio 02.07.01.62**, built against
a round-trip export from the user's own printer (`reference_x2d.3mf`) so that its members, XML
shape and array lengths match what Studio itself writes. So the job is now **import → eyeball →
slice**, and this section is a **verification checklist, not a configuration list**.

Profile identity, copied verbatim from the installed profile tree (not remembered, not guessed):

| | preset |
|---|---|
| printer | `Bambu Lab X2D 0.4 nozzle` |
| process | `0.20mm Standard @BBL X2D` |
| filament 1 (MAIN) | `Bambu PETG Translucent @BBL X2D 0.4 nozzle` — `filament_id` **GFG01** |
| filament 2 (AUX) | `Bambu PETG-CF @BBL X2D 0.4 nozzle` — `filament_id` **GFG50** |

Both X2D nozzles are **hardened steel**, and PETG-CF declares `required_nozzle_HRC = 40`, so the
abrasive is within spec on either nozzle.

**Baked in and verified present in the output:**
- `layer_height` **0.2**, `initial_layer_print_height` **0.2** — pinned, so no future preset
  change can silently re-round the ladder (`TEXT_DEPTH` 0.6 = 3 layers; zone tops 8/11/14/18)
- `sparse_infill_density` **100 %** — sparse infill inside a translucent plate prints a lattice
  straight through the viewing path
- `sparse_infill_pattern` **monotonic** — at 100 % the pattern still matters optically; `grid`
  (the preset default) crosses over itself and leaves a faint waffle
- `brim_type` **no_brim**, `brim_width` **0** — a brim would run over the engraved zone labels
- `curr_bed_type` **Textured PEI Plate**, bed **70 / 70 °C**
- `chamber_temperatures` **['0','0']**, nozzle **245 / 250 °C** for PETG and **255 °C** for
  PETG-CF
- `filament_map` **['1','2']** with `filament_map_mode` **Manual**
- **per-part filament assignment for all four parts** — `<metadata key="extruder" value="N"/>`
  at `<part>` level in `Metadata/model_settings.config` (Base parts → 1, Text parts → 2)
- **X2D-flavour machine G-code** in all five G-code blocks

**Two traps `make_bambu_3mf.py` had to work around** — recorded so they are not re-introduced:
1. **X2D machine G-code lives in five sidecar profiles** named `... template <key>.json` with
   `instantiation: false`. A naive `inherits` walk silently yields **generic X1/P1 G-code**
   instead — wrong dual-nozzle filament change, no X2D toolhead-offset calibration.
2. **`fdm_process_dual_common` ships `monotonic_travel_into_wall` as `"45.0"`**, which parses as
   45 **mm** rather than 45 **%**. A real Studio save contains `"45%"`, so it is pinned.

Still true and unchanged by any of the above:
- **No supports, no ironing** (the read face is on the plate, ironing would only touch the top).
- **Elephant-foot compensation ~0.15** — the first layer *is* the text layer; a bulged first
  layer smears the letter edges.
- Dry the PETG-CF before the run if it has been open.
- Prime tower on, minimum size — the CF is a fraction of a gram.
- Expected: **~20 g** for both coupons.

### "Chamber Cool Mode" — there is nothing to find
The setting was looked for in the UI and is not there for this job, and that is correct. The
X2D exposes `support_chamber_temp_control = 1`, and **both PETG filament profiles already
request `chamber_temperatures = 0` with `during_print_exhaust_fan_speed = 70`** — no chamber
heating plus active exhaust, which **is** the cool-running PETG configuration. Nothing needs
changing; do not go looking for it again.

### Confidence — read this before trusting anything above
**Nobody has been able to launch Bambu Studio to confirm the file imports as intended.** Every
claim in this section is *"the file says what was intended, and matches a real save
byte-shape-wise"* — never *"Studio accepted it"*. The highest-uncertainty item is
**`filament_map_mode = Manual`**: the enum was extracted from `BambuStudio.dll`, but every real
save on disk used `Auto For Flush`, so `Manual` has **never been observed in the wild**.

Relatedly, and more important: when the user configured the reference export by hand, **Bambu
Studio's auto-mapper left BOTH filaments on extruder 1** (`filament_map = ['1','1']`), and
`Bambu PETG-CF` carries `filament_extruder_compatibility = ['16']` — a flag whose meaning could
**not** be decoded from the installed profiles. So **whether Bambu Studio will actually permit
PETG-CF on the Bowden aux nozzle is UNRESOLVED and must be checked in the UI.**

**Fallback if it refuses:** run both filaments on the main nozzle with tool changes and a purge
tower (flush volumes 207 and 580 mm³). That still prints correctly — it just wastes filament.

### Post-import checklist (do these in the Bambu Studio UI, in order)
1. **Filament slots.** Slot 1 = translucent PETG, slot 2 = indigo PETG-CF. Check the
   nozzle/extruder icon on each slot: **slot 1 → left/main**, **slot 2 → right/aux**. This is the
   unresolved item above — if Studio has re-mapped both to one nozzle, see the fallback.
2. **Per-part filament chips.** Expand the object tree and confirm the filament chip on each of
   the four parts: **1 for both `Base` parts, 2 for both `Text` parts.**
3. **Quality → Layer height 0.2 mm, Initial layer height 0.2 mm.**
4. **Strength → Sparse infill density 100 %**, **Sparse infill pattern Monotonic.**
5. **Others → Adhesion → Brim type: No brim.**
6. **Plate-type selector = Textured PEI Plate**, bed **70 °C**.
7. **Prime tower** — check it does not overlap either coupon; move it if it does.
8. **Scrub the slice preview.** Layers 1–3 must show the **CF letters**; a mid layer must show
   **solid infill with no lattice**. If either is wrong, stop and fix it before printing.

## How to read the result
Print it, then take it to a window and look **down through the plate**, and answer these in
order. Write the answers straight into this file before the yacht is sliced.

1. **Which cover thickness wins.** Compare the four zones for legibility and contrast. Is 1.0 mm
   too thin to look good (letters visible but the plate looks cheap/translucent-thin)? Is 3.0 mm
   already too milky? Where does it stop improving?
2. **Inlay vs air gap.** In each zone, compare the LEFT (PETG-CF filled) word against the RIGHT
   (bare recess) word. Does the inlay win, and by enough to justify a dual-material print? If the
   air gap reads nearly as well, the yacht can be single-material and much simpler.
3. **Is 0.6 mm of CF opaque?** Hold it up to a bright light. Do the CF letters go fully black, or
   does light still come through 3 layers? If it glows, `TEXT_DEPTH` goes to 0.8.
4. **Does Arial Bold at 10 mm survive CF fuzz?** Look specifically at the **counters in the "a"
   and the "b"**, and the **bowl of the capital "A"**. If they close up or fur over, the final
   text needs a larger size (and line 1 of `FINAL_LINES` is the longest, so it will be the tightest).
5. **Does the textured PEI help or hurt?** The plate ships with textured PEI only, so the read
   face comes out **frosted**. Does that diffuse the text pleasantly (soft, even, no glare) or
   does it blur the letters? This decides whether a smooth plate needs buying before the yacht.
6. **Did the aux nozzle string or blob?** Look for CF wisps or specks dragged into the
   surrounding translucent area, and for CF bleeding outside the recess outline. Dark specks in
   a clear base are very visible and are the main cosmetic failure mode of this approach.

Then, with coupon B beside it — this is the whole reason B exists:

7. **How much worse is B than A at the same cover?** B's letters sit under a measured median of
   ~1.5 mm, i.e. between A's 1.0 and 1.6 rungs. Compare them directly. **Whatever legibility B
   loses relative to that part of A's ladder IS the wave penalty**, and it is the number that
   tells you how much thicker the real yacht's cover needs to be to compensate.
8. **Within a single word on B, which letters read and which don't?** Each word spans ~1.0 to
   ~3.0 mm of cover within itself. Cross-reference against `sea_coverage.png`: if the letters
   under the troughs are the only ones failing, the fix is cover thickness (scale the yacht up).
   If letters under **sloped** wave fail while equally-thin letters under **flat** wave read,
   the problem is refraction and no thickness change will fix it — the text must be placed under
   the flattest sea instead.
9. **Does the CF inlay still beat the bare recess once waves are involved?** Compare B's LEFT
   column against its RIGHT. The four words' medians are within 1.47–1.75 mm of each other, so
   this comparison is fair.

## Honest risks
- **Coupon A's top is flat; the real base's top is a wavy sea. — now directly tested.** Only
  ~20 % of the base's top area is flat; the rest is sloped wave, and light passing through a
  curved surface will diffuse and distort the text. Coupon A gives the **best case**; **coupon B
  gives the real case**, cut from the actual strip the text will occupy. Read the two together
  (questions 7–9 above) rather than assuming a penalty. Residual risk: coupon B samples **one**
  34 × 62 mm patch of sea, and the final three lines will span more length than that.
- **The hull blocks X ≈ 99–115.** The final text has no choice but to live in the **X 115–150**
  clear sea strip, ~35 mm wide. Three lines at ~11 mm pitch only just fit. Line 1
  (`Oh the places you'll go!`) is the longest and will be the tightest — if the coupon says the
  font must go larger to survive CF fuzz, that constraint bites here first.
- **Whether Bambu Studio will route PETG-CF to the aux nozzle is unresolved.** `filament_map`
  says `['1','2']` with `filament_map_mode = Manual`, but Studio's own auto-mapper put both
  filaments on extruder 1 when the reference project was configured by hand, and
  `filament_extruder_compatibility = ['16']` on the PETG-CF profile could not be decoded.
  **Check it in the UI (checklist item 1).** Fallback: both filaments on the main nozzle with
  tool changes and a purge tower — correct print, wasted filament.
- **Nothing about `yacht_sample_FINAL.3mf` has been confirmed by actually opening it in Bambu
  Studio.** It is internally verified and byte-shape-matched against a real save, which is not
  the same thing. Work through the post-import checklist rather than trusting it.
- **The real base is only ~2.1 mm at its thinnest** — thinner than ideal for a clean read, and
  that is exactly why the 2.2 mm zone is on the ladder. If 2.2 reads badly and 3.0 reads well,
  the fix is to **scale the yacht up** (105 % takes the thin point to ~2.2 mm, which is barely
  anything) or to accept the compromise. There is no room to add material without editing the
  sea surface.
- **Layer quantisation — resolved.** The ladder is layer-aligned at 0.2 mm by construction:
  1.6 / 2.2 / 2.8 / 3.6 mm = 8 / 11 / 14 / 18 layers, and the 0.6 mm recess is 3. Nothing gets
  rounded, so the engraved labels mean what they say. If you change `ZONE_COVER` or
  `TEXT_DEPTH`, keep every `cover + TEXT_DEPTH` a whole multiple of 0.2 mm — `verify.py` now
  asserts this and will fail if you don't.
- **Textured PEI frosts the read face.** Unavoidable on this machine as shipped. Check item 5
  above; a smooth PEI plate is the only remedy and there is no time to buy one.
- **CF on the aux nozzle carries a clog risk** (Bambu rates it "print with caution"). Mitigated
  by volume — 0.25 g — but if the aux jams mid-print, the fallback is the **single-material
  air-gap version**, which is why the right column exists.
- **The STL is not watertight — but the route through it is now known.** trimesh repair does not
  fix it and `slice_plane(cap=True)` produces a chunk no CSG engine will accept. **manifold3d
  ingests the raw source as-is** and the cut for the final text should be done the same way
  coupon B's was: one boolean against the target volume. See *Why the extraction is a manifold3d
  boolean* above.
- **The deadline is tomorrow, 24.07.2026.** There is time for this coupon and *one* yacht print,
  not for an iteration loop. If the coupon is ambiguous, take the safe reading (thicker cover,
  CF inlay, larger font) rather than the optimal one.
