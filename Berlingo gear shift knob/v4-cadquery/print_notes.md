# Berlingo gear shift knob — v4 print notes (from-scratch, CadQuery)

## Geometry summary
Outer: Ø46 bulb, 95 mm tall, Ø30 base with boot-lip groove; flat top with the 5+R
gate pattern **recessed 1.0 mm** (single color, per your choice). Bore, from the seat:
entry flare → Ø13.2 shaft bore, 70.1 deep (tip gets 2 mm headroom) → two **rail
channels** ±X (6.3 wide, Ø17.6 envelope, 41.8 deep) → two **button channels** ±Y
(9.4 wide, **Ø20.5 envelope**, 48 deep). The knob seats on the lever's **base plate**
(the wide disc at the boot — a feature rev2/rev3 never modeled; it is the natural
depth stop). Either 180° orientation fits; install with the pattern facing you.

## Why this won't repeat rev2
Every radial obstruction has its own full-length escape: rails ride the ±X channels,
the clip button rides the ±Y channels with clearance for up to **2.8 mm protrusion**
(the one value we never measured). Insertion was swept in CAD in 4 mm steps over the
full 68 mm travel with zero interference — including the button riding its channel.
There is **no click-groove**: with a channel under the button a groove can't click, so
retention is friction + 68 mm of engagement (rev2 taught us friction here is abundant).
No lift-collar needed (you confirmed reverse is push-in).

## Params → fit fixes (top of model.py)
| symptom | change |
|---|---|
| knob slides on too loose / rotates | `fit_clr_side` 0.15 → 0.10 (or 0.08) |
| shaft binds before seating | `fit_clr_side` → 0.20 |
| rails bind | `rail_clr_w` 0.4 → 0.6, or `env_clr_side` 0.45 → 0.6 |
| button scrapes | `btn_ch_env` 20.5 → 21.5 |
| sits high on the plate | `plate_h` 4.0 → measured value |

## PRINT THE COUPON FIRST — `knob_v4_fit_coupon.stl`
26 mm ring slice of the real bore (rail-channel ends + button path + upper bore
transition). ~15 min in PLA. Slide it down the lever: it must pass rails and button
without force and reach flush. Report where it stops if it stops — that names the
feature, and the table above names the fix.

## Slicing (Bambu X2D)
- Orientation: **UPSIDE DOWN** — flat top on the plate. Pattern recess prints as
  first layers = crisp. No supports anywhere (overhang audit: 0.0%).
- Walls 4, infill 25–40 % gyroid (solid feel: 50 %), elephant-foot comp ≥ 0.15.
- Material: **ASA** for the final — parked-car temps will creep PLA (240–255 °C,
  bed 90–100, Heat Mode 60–65, fan 0, dry 4–6 h @ 80). PETG acceptable. PLA only
  for the coupon.

## Honest risks
- `plate_h` 4.0 and `btn_z` 47.5 are photo estimates (±2 mm). Both are absorbed by
  margins (channel depth +4.5, tip headroom +2), not by luck.
- Button protrusion unmeasured → covered to 2.8 mm by the Ø20.5 channel envelope.
- If you ever want a positive click instead of friction: measure the button
  protrusion with calipers and I'll add a sprung lip above the channel end.
