# Berlingo gear shift knob — print & fit notes

## What's in the folder
- `berlingo_gear_knob.FCStd` — the parametric FreeCAD model
- `berlingo_knob_body.stl` — the knob body (print in black / colour A)
- `berlingo_knob_pattern.stl` — the 5-speed gate pattern inlay (white / colour B)
- `berlingo_knob.step` — both parts together, for other CAD
- `render_iso.png`, `render_front.png`, `render_top.png` — previews

## Geometry (bottom to top)
- **Outer shape:** copied from the Amazon reference knob — 95 mm tall, Ø46 mm bulb, Ø30 mm base collar with a boot-grip groove near the bottom.
- **Bore (from the bottom):** lead-in chamfer → **Ø17.4 × 32 mm counterbore** (clears the rod's measured Ø16.7 × 29.3 mm base collar) → **Ø13.2 main bore** (your Ø12.9 shaft + 0.3 mm clearance), **74 mm deep** (measured 72.1 mm exposed rod + 2 mm headroom). The rod's Ø6.5 tapered tip needs no special relief.
- **Top:** flat Ø30 face with the 1-3-5 / 2-4-R gate recessed 0.6 mm. The pattern STL fills the recess exactly flush.

## Two-colour printing
- **Easiest (X2D):** import the single file `berlingo_knob_2color.3mf` — it loads as one object with two parts. Assign white to *ShiftPattern*, black to *KnobBody*. With the X2D's dual nozzle each colour gets its own nozzle: no purge waste, no grey-tinged white.
- Alternative: load both STLs together as one object with two parts, or import `berlingo_knob.step` and choose "single object with multiple parts".
- **Single-colour fallback:** print the body alone; the recess reads fine as plain engraving.

## Changing dimensions
Open the FCStd in FreeCAD and edit the **Params** spreadsheet (double-click it in the tree). Every number updates on recompute:

- `fit_clr` — press-fit tightness on the shaft. Increase to 0.4–0.5 if too tight, decrease to 0.2 if sloppy.
- `collar_clr` — same idea for the counterbore.
- `bore_depth` (74) / `collar_depth` (32) — set from the measured rod: 72.1 mm exposed, 29.3 mm collar. Re-measure if the boot or rod ever changes.

After editing, re-export: select **KnobBody** → File → Export → STL (and **PatternInlay** separately if using two colours).

## Printing
- **Orientation: UPSIDE DOWN** — pattern face on the plate, bore opening up. This keeps the prime tower 3 layers tall (the two-colour layers are layers 1–3 instead of at 95 mm), removes all internal bridging in the bore (the hole only widens going up), gives a full Ø30 first-layer contact patch, and prints the pattern face razor-sharp against the plate. Layer direction (strength) is identical either way. Watch first-layer squish: keep elephant-foot compensation ≥ 0.15 so the white digits don't fatten into the black. No supports in either orientation.
- **Material:** PETG minimum, **ASA/ABS preferred** — a black knob in a parked car in summer gets hot enough to soften PLA.
- **Walls/infill:** 4 perimeters, 25–40 % gyroid. 100 % not needed — the part is nearly solid at the neck anyway.
- **Fit:** push on by hand with a twist; warming the knob (hair dryer, not heat gun) helps. If it ever works loose, a drop of epoxy in the bore is permanent.

## Honest note
The press fit relies on the white plastic rod being in decent shape. Since the old knob broke off it, check the rod for cracks before pressing hard — if it's chewed up, a bead of epoxy inside the bore turns this into a glue-on knob, which is just as usable (but removal becomes destructive).
