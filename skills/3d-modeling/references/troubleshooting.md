# Print troubleshooting — symptom → cause → fix

Rule out mechanical causes before touching slicer settings.

## Calibration order for every new filament
Temperature tower → pressure advance (PA depends on temp) → flow rate → retraction →
shrinkage cube (measure, store compensation) → save custom profile.
Shrinkage: scale per fdm-design §8's per-material table, or measure a test cube.

## First layer & adhesion
- Wash plate with degreasing dish soap — no aloe/moisturizer soaps.
- Z-offset 0.1 mm too high already ruins adhesion; too low → elephant foot, shifts.
  Enable a brim and babystep live at print start.
- Stubborn: Magigoo (material-specific), 3DLAC, Nano Polymer; brim/mouse-ears vs warp.
- Elephant foot: compensation setting + check bed temp against spool range.

## Extrusion
- Clogs: acupuncture needle or cold pull (~100 °C). Recurring clogs = heat creep →
  clean heatsink fan; open the door for PLA/PETG in enclosures.
- Under-extrusion, ranked: too fast > partial clog > slipping extruder gear > temp low.
  Fix flow with slicer's flow test; push temp toward manufacturer max.
- Pressure advance: corners gap = PA too high; corners round/mushy = PA too low.
- Stringing: temp too high, retraction wrong, or wet filament (popping sounds = wet).
  Last resorts: faster travel, avoid crossing perimeters.
- CF/GF wear: nozzle orifice no longer round → replace.

## Surfaces
- Poor top: over-extrusion on top layer → narrower top width, slower, +top layers,
  ironing. Pillowing over infill = cooling → +1–2 top layers cheapest fix.
- Weak layer bond: too fast / too cold / cold room / overcooled — lower fan but keep
  100 % on bridges & overhangs. Rotate part toward directional cooling ducts.
- Support scars: +Z-distance a notch, add interface layers (see materials.md §2).

## Motion artifacts
- Layer shifts: nozzle collisions (over-extrusion, curled edges, low/slow Z-hop),
  loose belts, debris in idlers, dry rails. Power off, move head by hand, feel for it.
- Ghosting/ringing: belt tension (check quarterly) + input shaping.
- Z-banding: bent lead screw, binding nut, temp fluctuation → clean/lube, PID tune.
