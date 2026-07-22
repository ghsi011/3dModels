# Berlingo gear shift knob — print notes (rev3, rail-channel bore)

## What changed rev2 → rev3
Rev2 jammed 20 mm down: the 16.7 mm caliper reading was across **two rails** on the
Ø12.9 shaft, not a solid collar. Rev3 models the rod itself (`RefRod`, hidden in the
FCStd) and cuts a bore that matches every measured feature.

## Bore geometry (from bottom / entry)
- Entry chamfer → **Ø13.2 main bore**, 74 mm deep (shaft Ø12.9 + 0.3 clearance)
- **Two rail channels**: 6.3 mm wide (rail 5.5 + 0.8), Ø17.4 envelope (rails 16.7 + 0.7),
  47 mm deep (rails end at 42.8 + margin). Opposed, along the knob's X axis.
- **Annular button groove**: Ø18, depth band 45–55 mm — works at any angle, so the clip
  button (Ø8.2, center 47.5 above boot) clears and clicks in regardless of its
  orientation relative to the rails. Button pops out fully if it protrudes ≤1.5 mm;
  prouder buttons stay slightly sprung = extra retention. Never a jam.

## Verification (Phase 4, passed)
- Seated interference: 0 except 3.4 mm³ at the modeled button-tip corners (= 0.6 mm
  spring compression; intended click retention)
- Insertion sweep (7 positions, button depressed): 0.000 mm³ everywhere
- Measurement audit: all 8 measured values present in geometry (12.9 / 16.7 / 5.5 /
  72.1 / 42.8 / 6.5 tip / 8.2 btn @47.5 / 46-95-30 outer)
- Cylindrical radii in part: 6.6, 8.7, 9.0, 15.0 ✓

## Params → fit fixes (Params spreadsheet in FCStd)
| symptom | cell to change |
|---|---|
| shaft too tight/loose | `fit_clr` (0.3) |
| rails bind in channels | `rail_clr` (0.8) or `collar_clr` (0.7) |
| button doesn't click | `btn_groove_d` (18) / `btn_groove_z` (45) |
| knob sits too high | `bore_depth` (74) |

## PRINT THE COUPON FIRST
`berlingo_fit_coupon.stl` — 22 mm ring slice of the actual bore (rail-channel ends +
button groove + shaft bore). ~15 min in PLA, slide it down the rod: it must pass the
rails, click on the button, and seat without wobble. Adjust Params, re-export, only
then print the full knob.

## Slicing (Bambu X2D)
- File: `berlingo_knob_2color.3mf` — one object, assign KnobBody→black (main nozzle),
  ShiftPattern→white (auxiliary). Grouping mode **Custom**, check assignment preview.
- Orientation: **UPSIDE DOWN** (top face on plate) — color layers 1–3, tiny prime tower,
  sharp pattern. Elephant-foot compensation ≥0.15.
- Material: **ASA** for the final (parked-car temps kill PLA): 240–255 °C, bed 90–100,
  Heat Mode 60–65, fan 0, dry 4–6 h @80. PLA only for the coupon/fit test.

## Honest risks
- Rail width read 5.5 from caliper photo — if snug, +0.2 on `rail_clr` fixes it.
- Button protrusion unmeasured; annular groove design tolerates any value.
- Two possible seatings (180° apart) — install with the pattern facing the driver.
