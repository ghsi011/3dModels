"""Berlingo (B9, 2014) gear shift knob — v4, designed from scratch (CadQuery backend).

Lever anatomy (photos 2026-07-23 + caliper set from earlier sessions):
  z=0 at the BOOT surface. A base PLATE (~Ø20 x 4) sits at the boot — the knob's
  natural seat is the plate TOP (z=4). Shaft Ø12.9 rises to 62.1, tapers to Ø6.5
  at 72.1 (tip). Two opposed RAILS (5.5 wide, Ø16.7 envelope) run plate→42.8.
  Above them: two dark WINDOWS (inner rod visible) 42.8→~47, then the clip BUTTON
  (Ø8.2, protrusion unmeasured ≤2 mm) at z≈47.5 on a face ~90° from the rails,
  then smooth Ø12.8 up to the dome tip. Reverse needs NO lift collar (user).

Fit strategy (why rev2 jammed / rev3 was never trusted):
  Every radial obstruction gets its own full-length channel — TWO rail channels
  (±X) and TWO button channels (±Y, so either 180° seating works), plus an annular
  click groove at the button's seated height. Insertion cannot jam even if the
  button is rigid; if it springs, it clicks into the groove.

Print: UPSIDE DOWN (flat top on bed) → recessed pattern crisp, bore prints clean,
no supports. Single color; shift pattern engraved 1.0 mm into the top face.
"""
import math
import cadquery as cq

# ==== PARAMETERS (mm; provenance in comments) ====
shaft_d      = 12.9   # caliper (today + earlier), smooth shaft & upper section (12.8~12.9)
fit_clr_side = 0.15   # per-side, sliding fit on shaft — fdm-design §4
rod_exposed  = 72.1   # caliper: boot → tip
plate_h      = 4.0    # base plate height above boot (photo estimate) — SEAT datum
plate_d      = 20.0   # base plate diameter (photo estimate, only used for ref/seat)
tip_d        = 6.5    # caliper: tip diameter
taper_len    = 10.0   # photo: tip taper length
rail_w       = 5.5    # caliper photo (earlier session)
rail_env     = 16.7   # caliper (today): envelope across both rails
rail_top     = 42.8   # rod_exposed - 29.3 caliper smooth-top; band bottom = rail end
btn_d        = 8.2    # caliper (earlier): clip button diameter
btn_z        = 47.5   # button center above boot (photo, ±2) — groove is wide to absorb
btn_prot     = 1.5    # button protrusion (UNMEASURED, ≤2 assumed; channels make it safe)

rail_clr_w   = 0.4    # per-side clearance in rail channel width  (6.3 total width)
env_clr_side = 0.45   # per-side on channel envelope (Ø17.6)
btn_ch_w     = btn_d + 1.2          # 9.4 button channel width
btn_ch_env   = 20.5   # button channel envelope: clears protrusion up to 2.8 mm
                      # (protrusion UNMEASURED — this is the robustness margin.
                      #  No click-groove: with the button riding its own channel a
                      #  groove can never click; retention = 68 mm engagement +
                      #  friction, tuned with the coupon via fit_clr_side.)

insertable   = rod_exposed - plate_h        # 68.1 rod above the seat plane
bore_d       = shaft_d + 2 * fit_clr_side   # 13.2
bore_depth   = insertable + 2.0             # 70.1 — +2 tip headroom
chan_env     = rail_env + 2 * env_clr_side  # 17.6
rail_ch_w    = rail_w + 2 * rail_clr_w      # 6.3
rail_ch_depth = (rail_top - plate_h) + 3.0  # 41.8 — rails enter 38.8, +3 margin
btn_ch_depth  = (btn_z - plate_h) + 4.5     # 48.0 — button path + margin

knob_h       = 95.0   # outer: Amazon-reference proportions (kept from rev3)
bulb_r       = 23.0   # Ø46 bulb
base_r       = 15.0   # Ø30 base
top_r        = 12.5   # flat top face radius (pattern area)
engrave_dp   = 1.0    # recessed pattern depth (user: single color, recessed)

# ==== MODEL: outer body (revolved profile, z=0 at knob bottom/seat) ====
prof = (cq.Workplane("XZ")
        .moveTo(0, 0).lineTo(base_r, 0)
        .lineTo(base_r, 2.0)
        .lineTo(base_r - 1.6, 3.2).lineTo(base_r - 1.6, 6.4)   # boot-lip groove
        .lineTo(base_r, 7.6).lineTo(base_r, 10.0)
        .spline([(base_r - 1.0, 16.0), (bulb_r - 6.0, 40.0), (bulb_r, 62.0),
                 (bulb_r - 1.5, 74.0), (top_r + 4.0, 88.0), (top_r, knob_h)],
                includeCurrent=True)
        .lineTo(0, knob_h).close())
body = prof.revolve(360, (0, 0, 0), (0, 1, 0))  # local Y = global Z on the XZ plane

# ==== bore + channels (cut from bottom) ====
def channel(width, depth, env):
    """slot through the bore: box spanning `env` along X, `width` along Y"""
    return (cq.Workplane("XY")
            .box(env, width, depth, centered=(True, True, False))
            .intersect(cq.Workplane("XY").circle(env / 2).extrude(depth)))

cut = cq.Workplane("XY").circle(bore_d / 2).extrude(bore_depth)
cut = cut.union(channel(rail_ch_w, rail_ch_depth, chan_env))            # rails ±X
cut = cut.union(channel(btn_ch_w, btn_ch_depth, btn_ch_env)
                .rotate((0, 0, 0), (0, 0, 1), 90))                      # button ±Y
cut = cut.union(cq.Workplane("XY").circle(bore_d / 2 + 1.8).extrude(2.0))  # entry flare
body = body.cut(cut)

# ==== recessed 5+R shift pattern on the top face (engraved, single color) ====
# double-H gate: 3 verticals + crossbar, numbers 1/3/5 top, 2/4/R bottom
s = 3.4          # half-gap between vertical bars
bar_w, bar_l = 1.6, 11.0
z_eng = knob_h - engrave_dp
eng = None
for x in (-s * 2, 0.0, s * 2):
    r = (cq.Workplane("XY", origin=(x, 0, z_eng))
         .rect(bar_w, bar_l).extrude(engrave_dp + 0.2))
    eng = r if eng is None else eng.union(r)
eng = eng.union(cq.Workplane("XY", origin=(0, 0, z_eng))
                .rect(s * 4 + bar_w, bar_w).extrude(engrave_dp + 0.2))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
labels = [("1", -s * 2, bar_l / 2 + 2.9), ("2", -s * 2, -bar_l / 2 - 2.9),
          ("3", 0,      bar_l / 2 + 2.9), ("4", 0,      -bar_l / 2 - 2.9),
          ("5", s * 2,  bar_l / 2 + 2.9), ("R", s * 2,  -bar_l / 2 - 2.9)]
for ch, x, y in labels:
    t = (cq.Workplane("XY", origin=(x, y, z_eng))
         .text(ch, 4.6, engrave_dp + 0.2, fontPath=FONT, kind="bold",
               halign="center", valign="center"))
    eng = eng.union(t)
body = body.cut(eng)

# ==== REFERENCE (mating lever, seated: its boot z=0 maps to model z=-plate_h) ====
# model frame: knob bottom (seat plane) = z 0 = lever plate TOP (lever z 4)
def lever(at=0.0):
    """lever solid in knob frame, shifted `at` mm downward = knob raised by `at`"""
    z0 = -plate_h - at
    lv = (cq.Workplane("XY", origin=(0, 0, z0))
          .circle(plate_d / 2).extrude(plate_h))                       # base plate
    lv = lv.union(cq.Workplane("XY", origin=(0, 0, z0))
                  .circle(shaft_d / 2).extrude(rod_exposed - taper_len))
    tip = (cq.Workplane("XY", origin=(0, 0, z0 + rod_exposed - taper_len))
           .circle(shaft_d / 2).workplane(offset=taper_len).circle(tip_d / 2)
           .loft())
    lv = lv.union(tip)
    rails = (cq.Workplane("XY", origin=(0, 0, z0 + plate_h))
             .box(rail_env, rail_w, rail_top - plate_h, centered=(True, True, False))
             .intersect(cq.Workplane("XY", origin=(0, 0, z0 + plate_h))
                        .circle(rail_env / 2).extrude(rail_top - plate_h)))
    lv = lv.union(rails)
    btn = (cq.Workplane("XZ", origin=(0, -(shaft_d / 2 + btn_prot), z0 + btn_z))
           .circle(btn_d / 2).extrude(-(shaft_d / 2 + btn_prot)))      # along +Y to axis
    return lv.union(btn)

ref_part = lever(0.0)

# ==== EXPORT ====
cq.exporters.export(body, "knob_v4.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "knob_v4.step")
# fit coupon: 26 mm ring slice of the bore covering rail-channel end + groove + button path
ring = (cq.Workplane("XY", origin=(0, 0, 30.0)).circle(12.5).extrude(26.0))
coupon = body.intersect(ring).translate((0, 0, -30.0))
cq.exporters.export(coupon, "knob_v4_fit_coupon.stl", tolerance=0.01, angularTolerance=0.1)
print("body volume", round(body.val().Volume() / 1000, 1), "cm3")
print("bbox", body.val().BoundingBox().xlen, body.val().BoundingBox().ylen,
      body.val().BoundingBox().zlen)
print("coupon volume", round(coupon.val().Volume() / 1000, 1), "cm3")
