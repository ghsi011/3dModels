# Broom clip — wall-mounted snap clip for Ø25.0 mm wooden handle

**Deliverable:** `broom_clip_25mm.stl` (this folder)
**Source files (Windows):** `C:/github/3D/experiments-scratch/T1_freecad/` — `broom_clip_t1.FCStd`
(parametric, Params spreadsheet, reference handle hidden inside), the same STL, `render_iso.png`, `render_section.png`.

## What it is
A one-piece C-clip per the reference product photo: flat back plate with a single central
screw hole, two curved snap arms with full-round tips. The broom handle pushes in from the
front, the arms flex apart, and the handle seats in a cradle against the back plate.

## Key dimensions (all driven by the Params spreadsheet in the FCStd)
| Feature | Value | Why |
|---|---|---|
| Overall envelope | 40.0 W x 27.6 D x 12.0 H mm | user asked ~40 wide, ~12 tall; depth stays discreet |
| Handle (measured) | Ø25.0 mm (caliper photo) | mating dimension |
| Cradle bore | Ø25.6 mm (0.3 mm/side clearance) | sliding fit in PETG; tolerates wood swelling |
| Mouth/throat opening | 20.0 mm between tip bulbs | 0.8 x handle dia — snaps in/out with ~2.5 mm arm deflection each |
| Arm wall | 2.4 mm (3 x 0.8 mm lines) | flexible enough (~1.7 % peak strain, momentary; fine for PETG), stiff enough to hold |
| Tip bulbs | R1.2 full-round | smooth cam surface both inserting and pulling out; no sharp edges on the wood |
| Seat recess | cradle sunk 0.3 mm into plate face | kills the tangency knife-edge, centers the handle |
| Back plate | 5.5 mm thick, corners R2, arm-root fillets R4 | screw depth + crack-resistant arm roots |
| Screw hole | Ø4.5 through, teardrop roof; 90-deg countersink Ø9.5 x 2.5 | for one 4–4.5 mm (#8/#9) FLAT-HEAD wood screw; head sits flush so the handle never touches it |
| Chamfers | 0.3 mm on bottom & top perimeters | elephant-foot protection, no slicer compensation needed |

## Verification performed (in FreeCAD, before export)
1. Interference of seated Ø25.0 handle vs clip = 0.000 mm³ (0.3 mm gap all around).
2. Insertion sweep: max deflection 2.50 mm/arm exactly at the throat; arms fully relax when seated (0.3 mm bulb clearance).
3. Half-section render checked (see `render_section.png` on the Windows machine).
4. Measurement audit: cylindrical radii found = 1.2 / 2.0 / 2.25 / 4.0 / 12.8 / 15.2 — every measured/param number present, none orphaned.
5. Printability audit: face-normal scan found **no** downward face steeper than 45 deg above the bed → prints support-free as oriented.
6. Bbox/face audit: 40.00 x 27.60 x 12.00 mm as intended. STL is watertight (1828 facets).

## Printing instructions
- **Orientation: as exported — back plate + arms flat on the bed** (12 mm extrusion pointing up). Do not reorient: this puts the snap-flex in the layer plane (arms can't delaminate) and needs **no supports**.
- **Material: PETG** (as requested). 4 perimeters, 30 % infill, 5 top/bottom layers, 0.2 mm layers. PLA would work as a quick fit test but will creep/crack as a snap fit long-term.
- Skip elephant-foot compensation if your slicer applies it by default — the 0.3 mm chamfer already handles it.
- ~5.3 g, ~25–35 min print.

## Mounting
One 4 x 30 mm (or 4.5 x 40) **countersunk flat-head** wood screw + wall plug, driven from the cradle side; head lands flush in the countersink. Teardrop hole apex points to the printed top — either way up works on the wall. Mount so the broom head hangs above the clip or rest it on the clip's top edge.

## Assumptions made (user was away)
- Caliper value 25.0 mm taken as the handle diameter; wood assumed round and reasonably straight. Cradle gives 0.3 mm/side so up to ~Ø25.4 still snaps in; a swollen ≥Ø25.8 handle would grip very tightly.
- "Holds firmly but pulls out easily": targeted opening = 0.8 x diameter (commercial-clip norm). If YOUR pull-out feels too tight/loose, edit **Params → mouth_gap** (20.0; larger = looser) in the FCStd and re-run the build (one-cell fix), or just print at ±2 % X-Y scale for a quick tweak.
- Screw type assumed flat-head countersunk (needed so the head is flush under the handle). If only pan-heads are on hand, add a washerless pan head only if ≤ Ø9.5 and accept slight handle stand-off — flat-head strongly preferred.
- Printer not specified for this job; design is slicer/printer-agnostic (no supports, no bridges > 4.5 mm teardrop, 45-deg max overhang). Fits the Bambu X2D on file with default PETG profile.
- Indoors use assumed (PETG is fine; for outdoor/sun use ASA and scale X-Y +0.3 %).

## Honest risks
- Wooden handles vary; if the handle measures > 25.4 mm where the clip grabs, insertion force rises quickly. Cheap fix: `mouth_gap` 20 → 21, or scale the part.
- Repeated daily snap cycles at ~1.7 % strain are within PETG's comfort zone but will slowly relax the grip over years; arms are 2.4 mm thick to compensate. If grip relaxes, print another (5 g).
- One-screw mount can rotate under a hard sideways yank; the 40 mm-wide plate resists this, but use a second clip lower down if the broom gets knocked around.
