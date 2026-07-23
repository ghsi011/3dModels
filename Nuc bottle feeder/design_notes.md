# Nuc bottle feeder — design notes

**Status:** v1 — modeled, script-verified, not yet printed. Print the two coupons first
(see `print_notes.md`), then bench-test per `bench_test_protocol.md` before any hive install.

## Architecture — "monolithic bulkhead tray"

One printed PETG **body** = drinking tray + hollow barrel that rises through the roof:

- The barrel carries an **external 2-start clamp thread (Ø40, lead 8) over its whole
  length**. The **PCO-1881 female socket is bored inside the barrel's top**, so nothing on
  the body is wider than the clamp thread and the big scalloped **nut** spins on from above
  with no obstruction — that is what makes tool-free clamping over 8–30 mm trivial.
- The roof+ceiling sandwich is clamped between the body's **Ø60 bearing flange** (against
  the ceiling underside) and the **Ø80 nut** (on the roof) — the joint is loaded in pure
  compression; printed threads only carry the modest clamp preload and the 1.3 kg bottle
  (~0.03 MPa on the thread bearing area — creep-irrelevant even at 40 °C).
- The **syrup outlet is integral with the tray** (bore mouth standing `POOL_DEPTH` above
  the tray floor on 4 ribs), so pool depth is **independent of roof thickness and clamp
  position** — an earlier idea (tray screwing onto the barrel and acting as the clamp nut)
  died precisely because outlet height would have varied 22 mm across the clamp range.
- The bottle screws into the socket top; a **TPU gasket washer** on an internal seat is
  the sealing element. **A printed transport plug** (male PCO-1881 stub + grip disc)
  seals the socket bee-tight whenever the bottle is off.

This is still "tray + tube + bulkhead clamp" in topology — the brief's §4 invitation to
reconsider was taken seriously; the winning insight was not a new topology but *merging
tray, tube, and bulkhead into one solid*, which reduces the airtight-joint count to one.

## The airtightness path, joint by joint (brief §1.3, §6)

Air entering anywhere upstream of the outlet dumps the bottle. The full path:

1. **Bottle wall / neck** — commercial PET, tight.
2. **Bottle lip → TPU gasket → printed seat** — the ONE mechanical joint. Seal is on the
   bottle's flat top land (usable annulus Ø22.3–23.8 per ISBT), the same surface its
   original cap seals on. Gasket: printed TPU washer Ø25×Ø17×2; field fallback: 3 mm
   silicone/EPDM sheet punched to size, or a disc cut from bicycle inner tube. The thread
   is positioned so the lip contacts the gasket 0.8 mm **before** the thread could bind
   (GASKET_CRUSH) — hand torque goes into gasket compression, exactly like a real cap.
3. **Barrel wall, socket → outlet mouth** — monolithic PETG. Print with 4 perimeters and
   ≥1.02 flow (see print notes); PETG at these wall thicknesses (≥3.5 mm) is reliably
   airtight. The 24 h submerged/leak bench test exists to catch a bad print, not a bad design.

There are **no other joints**. The nut, the roof interface, the tray — all are downstream
of the outlet or outside the sealed volume entirely.

## PCO-1881 — verified spec, and one important correction

Verified against the ISBT drawing 3784253-17 (imajeenyus.com mirror), a KIMEX preform QC
sheet, and patent WO2016019321A1 (all agree):

- T Ø27.40 ±0.13, pitch 2.70 single-start RH, wrap 650°, S (lip→thread) 1.70, X 17.00,
  Z = **support-ledge OD 33.0** (the brief's "Z = 33.0" is the ledge diameter, not a height).
- **Correction: E (thread root) = 24.20, not 24.94.** 24.94 is ØF — the unthreaded collar
  under the sealing land (ØG 25.07 max). A female thread sized off "root + clearance"
  **jams on that collar**; it is the classic printed-cap mistake. Our female crest ID is
  25.55 (= BOSL2's validated 25.5): clears the collar and still engages 0.92 mm radially.
- Male tooth: depth 1.60, axial 1.66 root / 0.80 crest, asymmetric 20°/10° flanks
  (we cut the female groove with a trapezoid dilated 0.32 radial / 0.25 per flank —
  within the community-validated snug range).
- TE bead Ø28.0 sits 9.0–13.0 below the lip: at full gasket crush the lip is 8.8 deep, so
  the bead grazes the barrel-top plane — the socket entry has a Ø29.2×2 relief for it.

## Thermal flooding (§3.7) — analysis, and why there is no valve

Worst case: near-empty bottle (~900 ml headspace air), sun heats it ΔT ≈ 30 K.

- **Rigid reservoir:** expelled volume ≈ V·ΔT/T ≈ 900 × 0.1 ≈ **90 ml** pushed into the tray.
- **Compliant still-water bottle (our case):** two buffers act first. (a) In operation the
  regulation vacuum has already paneled the bottle inward — stored recoverable volume that
  simply un-panels as pressure rises, absorbing expansion at near-zero ΔP. (b) Past neutral,
  a thin-walled (~0.2 mm) still bottle bulges outward ~30–50 ml at only 1–3 kPa. Together
  they absorb most of the 90 ml; realistic expulsion is a few tens of ml.
- **The tray absorbs the remainder by design:** flood reserve = wall height (15) minus pool
  (4.5) minus margin ≈ 8.5 mm of freeboard over ~14,000 mm² of open annulus ≈ **≥100 ml**
  before anything overflows into the hive. Overflow into the hive is the colony-killing
  event; bees getting wet feet in a temporarily deeper pool is not — the 4 full-height
  rescue ridges and the 45° center cone give them walk-out ramps, so even a submerged boss
  field is survivable.
- **Collapse-and-rebound pumping** (the brief's open question): cooling re-panels the bottle
  and *sucks air back in through the outlet* (a reverse glug) — it does not pump syrup out.
  Only the heating half-cycle expels; each day's cycle expels once into a tray that drains
  back down to pool level as bees drink. No ratchet mechanism exists. **Conclusion: the
  compliant bottle is net-protective; no check valve or vent labyrinth is warranted.**
  Cheap additional mitigations (field notes): fill bottles full (small headspace), feed in
  the evening, use white/foil-wrapped bottles.

Verdict on §2's question: the still-water bottle is *safer* here than a rigid one.

## Drowning prevention (§3.8)

Hex boss field (5 AF, 1.8 mm channels, tops 1.2 mm above the equilibrium level) — bees
stand dry and drink from capillary channels; pool depth is a parameter (`POOL_DEPTH`,
default 4.5, sane 3–6). Rescue ridges (4 radial, full wall height) + the 45° cone are
climb-out paths if a thermal event ever raises the level above the bosses.

## Bee access (§3.9) and bee space (§3.3) — stated assumptions

- **HEADSPACE IS UNMEASURED** (brief §2). Assumed **≥35 mm** below the ceiling.
  With 35 mm: tray hangs 28.8 mm (`HANG_DEPTH` 26.4 + floor 2.4), leaving **6.2 mm** under
  the tray to the frame top bars — inside bee space, so bees pass under and nothing gets
  burr-combed. **Idan: measure the real headspace.** If < 33 mm, shrink `WALL_H` (costs
  flood reserve) or `RIM_GAP`; both are one-line parameter edits.
- Access route: bees walk the ceiling and enter over the rim through the **9 mm rim-to-
  ceiling gap** (`RIM_GAP`, bee space); 8 vertical grip ribs on the tray's outer wall give
  a climbing route from below as well. FDM layer texture itself is very climbable.
- Gaps audit: rim→ceiling 9 (pass), under-tray 6.2 at assumed headspace (pass), barrel→
  drill-hole annulus ~2 mm (below propolis threshold, and sealed above/below by the clamp
  faces — inaccessible), tray interior fully open (no <4.5 mm crevices except the drink
  channels, which are the point).
- **Bee-tightness with bottle off (§3.2):** the plug. Without it the Ø16 bore is an open
  door — the plug lives on the hive (parked in the socket) whenever a bottle isn't.

## Loads, wind, creep (§3.4, §3.5)

- Weight path: bottle → gasket seat → barrel → **nut bears on roof top** (compression into
  wood). Thread shear stress from 2.5 kg ≈ 0.03 MPa over the engaged area — negligible vs
  PETG creep limits even at 40 °C+.
- Wind: 1 L bottle ≈ 0.027 m² at ~200 mm lever; 60 km/h gust ≈ 0.9 N·m moment at the roof.
  The clamp couple (≥300 N hand preload across the Ø44 hole, faces at Ø60/Ø80) resists
  ≥7 N·m before rocking. Re-snug the nut at routine inspections (PETG preload relaxes).
- Torque cross-talk: screwing the bottle in/out (~0.5–1 N·m at the gasket) is far below
  the clamp's ~2.5+ N·m friction, so bottle swaps cannot rotate/loosen the feeder.

## Other §4 items

- **Refill ergonomics:** feeder stays clamped and sealed; only the bottle turns. The 2-turn
  engagement means ~1–2 s of open-mouth glug while screwing in — the tray's flood reserve
  absorbs that (~30 ml) harmlessly. One hand holds the bottle, no tools. See field notes
  for the exact swap sequence.
- **Syrup level visibility:** inherent — the translucent PET bottle stands above the roof.
  Glance = level.
- **Anti-ant:** the nut carries a 45° **skirt** (Ø96) whose underside stays 3 mm off the
  roof: smear a ring of barrier grease (Vaseline/Tanglefoot) on the barrel *under the
  skirt*, where rain and dust can't degrade it. The only path to the syrup is across that
  band. (Ant moats need water maintenance; grease under a rain shield doesn't.)
- **Flow rate (§4.6):** regulation is demand-driven (bees drinking = glugs); the tunable
  is `POOL_DEPTH` per print. No moving parts earn their keep here.
- **Print efficiency (§4.7):** the body is a wide stable dish + one Ø40 column — no tall
  thin tube ringing. Everything prints support-free in its natural orientation.

## Known weaknesses / test-first list

1. **Printed female PCO thread + seat** — the highest-risk feature. That's why
   `coupon_socket` exists (real top 16 mm of the barrel): bottle must spin on freely and
   the lip must land on the gasket with the bead clearing the relief. If tight, raise
   `PCO_CLR_RADIAL/AXIAL` one step (0.40/0.30); if the lip doesn't reach, deepen
   `GASKET_CRUSH`.
2. **PETG wall airtightness** depends on print quality → 24 h leak watch in the bench
   protocol is mandatory, not optional.
3. **Headspace assumption** (above) — measure before installing.
4. TPU gasket compression set over months in heat — carry the inner-tube/silicone fallback.
5. The Ø44 hole is committal on the hive; confirm the roof material actually takes a hole
   saw cleanly (plywood: yes; polystyrene nuc boxes: drill gently, the clamp faces are
   wide enough to spread load).

## Departures from the brief

- None structural. Additions beyond the letter of the brief: monolithic body (airtight-
  joint minimization), nut ant-skirt, rescue ridges, transport plug doubling as the §3.2
  bee-tight cap, gasket-crush thread positioning (ISBT-style seat-before-bottom).
