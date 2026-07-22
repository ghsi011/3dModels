# Tractor seat pin — print & fit notes

## What's in the folder
- `tractor_seat_pin.FCStd` — the parametric FreeCAD model
- `tractor_seat_pin.stl` — ready to slice
- `tractor_seat_pin.step` — for sharing with a machinist / other CAD
- `render_iso.png`, `render_front.png` — previews

## Geometry (top to bottom)
- **D-head:** half-cylinder, Ø16 mm with flat face through the center, 18 mm tall (matches the working bolt — mount it with the flat facing the front of the tractor)
- **Shank:** full cylinder, prints at Ø15.7 mm (16 mm minus 0.3 mm fit clearance), 6 mm tall — this is the part that sits in the bracket hole
- **Tail:** Ø10 mm × 14 mm, with a Ø4 mm cross-hole 5 mm from the end — slide a washer on and lock it with a 4 mm R-clip or split pin from the hardware store

## Changing dimensions
Open the FCStd in FreeCAD and edit the **Params** spreadsheet (double-click it in the model tree). Every number updates the model on recompute. Things worth checking against the real tractor before printing the final part:

- `shank_h` — set it to the actual bracket plate thickness (default 6 mm is a guess from the photos)
- `tail_d` — must fit through the hole in the arm. The sheared threads in your photos look ~10 mm, but measure the broken stub or the hole to be sure
- `fit_clr` — increase to 0.4–0.5 if the shank is too tight in the hole, decrease if sloppy

After editing, re-export: select **SeatPin** in the tree → File → Export → STL.

## Printing
- **Material:** PETG, ABS, or ideally polycarbonate / carbon-fiber nylon. PLA will creep and snap.
- **Infill:** 100%, 4+ perimeters.
- **Orientation:** lay it on the flat D-face. This puts the print layers along the pin's axis, so the seat load doesn't try to split it between layers at the plate line (which is exactly where the steel one sheared).

## Honest warning
The original **steel** pin sheared here — this joint sees the full bouncing weight of the rider through the seat springs. A printed pin is great for test-fitting and will work as a get-you-going part, but expect it to be temporary. Once the printed one confirms the dimensions, consider having a steel one turned from the STEP file, or adapting an M16 bolt: cut the head off, grind half the shank away to make the D, drill a 4 mm cross-hole.
