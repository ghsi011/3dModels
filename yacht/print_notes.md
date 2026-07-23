# J Class yacht base — translucent text sample coupon (print notes)

## What's in the folder
- `model.py` — the parametric CadQuery source (all knobs are named constants at the top)
- `verify.py` — Phase 4 verification; runs on the **exported STLs re-imported** with trimesh
- `sample_base.stl` — the translucent plate, with the text cut in as recesses → **MAIN nozzle**
- `sample_text_cf.stl` — the inlay bodies for the left column only → **AUX nozzle**
- `sample_text_all.stl` — every recess solid (both columns + zone labels), reference/debug
- `sample_coupon.step` — combined, for sharing / re-import
- `sample_readability.png` — top view (must read correctly) + bottom view (must mirror)
- `sample_section.png` — section along the ladder, text layer vs cover
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
- The STL is **not watertight** as supplied (276,010 faces). Repair before any boolean or
  multi-material split on the real base.

## Geometry summary (the coupon)
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

## Verification (Phase 4, all checks pass)
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

## Orientation
**TEXT-FACE DOWN on the build plate**, flat underside on z = 0, exactly as modelled. The text
recess then prints as the **first 3 layers**, which is where an FDM printer is sharpest, and the
stepped top faces up. No supports, no bridging, zero overhang. Printing it any other way puts
the read face against support or in mid-air and there is no reason to.

## Material & nozzle assignment (Bambu Lab X2D Combo, dual nozzle + AMS 2 Pro)
| body | material | nozzle | why |
|---|---|---|---|
| `sample_base.stl` | translucent PETG | **MAIN** | direct drive, 40 mm³/s, flow-calibrated, best surface finish. The base is the showpiece and ~98 % of the volume, so it gets the good nozzle. |
| `sample_text_cf.stl` | indigo PETG-CF | **AUX** | small volume, and the aux's limits don't bite here. |

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

## Slicing (Bambu Studio, X2D)
- **Layer height 0.2 mm.** `TEXT_DEPTH` 0.6 = exactly 3 layers, and every zone top is exactly
  8 / 11 / 14 / 18 layers, so nothing in the ladder gets rounded. Do not slice at another layer
  height without re-checking that.
- Grouping mode **Custom**; assign `sample_base` → translucent PETG (main),
  `sample_text_cf` → indigo PETG-CF (aux). **Verify the assignment preview before slicing** —
  it can't be reassigned afterwards; rearrange AMS slots instead.
- PETG: 250–260 °C, bed 70–80 °C, **Cool Mode** (chamber heat off), fan on. Dry PETG-CF before
  the run if it has been open.
- **Infill 100 %** — the plate is only 1.6–3.6 mm thick, so it's shells anyway and solid keeps
  the light path even. Walls 3.
- **No supports, no ironing** (the read face is on the plate, ironing would only touch the top).
- **Elephant-foot compensation ~0.15** — the first layer *is* the text layer; a bulged first
  layer smears the letter edges.
- Brim: prefer **none**. If adhesion needs it, keep it ≤3 mm — the zone labels sit only 1.67 mm
  from the left edge (label text reaches x = −32.33, edge at −34.00).
- Prime tower on, minimum size — the CF is a fraction of a gram.
- Expected: **~13 g, under 1 hour.**

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

## Honest risks
- **The coupon's top is flat; the real base's top is a wavy sea.** This is the biggest gap
  between the test and the real thing. Only ~20 % of the base's top area is flat; the rest is
  sloped wave, and light passing through a curved surface will diffuse and distort the text.
  The coupon gives the **best case**. Expect the yacht to read somewhat worse than whichever
  zone you pick, and prefer to place the text under the flattest region of the sea if the model
  allows it.
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
- **The STL is not watertight.** Any boolean against the real base (cutting the final text) must
  be done on a repaired mesh, or the cut will fail or produce garbage.
- **The deadline is tomorrow, 24.07.2026.** There is time for this coupon and *one* yacht print,
  not for an iteration loop. If the coupon is ambiguous, take the safe reading (thicker cover,
  CF inlay, larger font) rather than the optimal one.
