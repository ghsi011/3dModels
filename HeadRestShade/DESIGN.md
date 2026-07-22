# SandThrone — Portable Beach Headrest with Integrated Sunshade

A lightweight, collapsible, sand-stable head/neck rest for lying on the beach,
with an adjustable canopy. Designed for FDM printing on the X2D (256³ mm) in
UV-resistant PETG / ASA. Parametric CAD in [`parts.py`](parts.py); overview
geometry in [`assembly.py`](assembly.py).

Coordinate convention: **+X = toward the user's body/feet, +Z = up, Y = lateral
(left/right of the head).**

---

## 1. Overall design description

The product is a "node-and-strut" A-frame. Two open triangular **side frames**
stand on either side of the user's head. Each is an inverted V: a **front leg**
(leans toward the body, carries the head cloth) and a **rear leg** (leans away,
for stability), meeting at an adjustable **apex clutch**. There is no ground
rail — each of the four leg ends terminates in an **integrated sand-anchor
foot**.

The two side frames are tied together by **three removable crossbeams** (apex,
front-foot, rear-foot). All long straight members — the crossbeams, the shade
arms, and the shade-frame rails — are **commodity 16 mm tubes/dowels**
(aluminium or fibreglass). Everything clever and load-bearing is **printed**:
the apex clutch, the feet, the fabric rail, the quick-release fittings, and the
shade pivot + corners. This is the key engineering decision — FDM is weak in
inter-layer tension along a long thin beam, so we never print a long beam; we
print the *nodes* and let cheap, perfectly-straight, UV-stable stock take the
spans.

The **head cloth** spans the **entire front face of the triangles** — from near
the apex down to near the front feet, and the full width between the two front
legs. It is one fabric panel whose two side hems each capture a thin rod that
slides into a near-full-length printed **C-channel fabric rail** on the inboard
face of each front leg. The result is a single sloped support surface: the head
and neck rest near the top, the upper back is carried down the slope. Tension
across the ~360 mm gap gives a shallow cradle; the panel lifts, slides out and
washes in seconds, and swaps for different cloth/firmness.

The **sunshade** mounts at the apex on a **friction pivot with a hard arc-slot
stop** — the right tool here, since the shade is light-load and wants smooth fine
adjustment within a bounded range (unlike the apex, which needs a strong discrete
positive lock under head load). A fixed pin rides an arc slot whose ends are
mechanical stops. Two short tube arms hold a rectangular frame (printed corners +
tube rails) **horizontal by default** —
parallel to the ground, directly over the face and chest. The pivot allows only
a **limited tilt each way** (≈ ±30°) so the user can knock the sun back without
the panel becoming a wind sail; the limited arc deliberately keeps wind leverage
on the printed pivot low. The shade folds down flat against the frames for
transport.

Everything disassembles, without tools, into a flat bundle of struts plus a
small bag of printed nodes.

### How it carries load
The head pushes **down and forward** on the cloth. That force runs down the front
legs into the front feet. Each foot is a **collinear cruciform spade**: the spade
runs along the **same axis as the leg**, so it drives deep along the leg line and
a full inclined wedge of sand loads its broad **ballast plate** — that sand
weight is the ballast that stops the frame ploughing forward, and resists
pull-out far better than a shallow horizontal shelf. A crossed **keel fin**
handles side-to-side wobble. The **rear legs** form the third side of a tripod;
their (deeper, bigger-keel) spades resist backward tip and lateral sway. The
**apex clutch** is a positive (toothed) lock, not a friction joint, so it cannot
creep under sustained head pressure or gusts.

---

## 2. Labeled parts list

### Printed parts (PETG/ASA) — per complete unit
| # | Part (STL) | Qty | Role |
|---|------------|-----|------|
| 1 | `apex_hub_front` | 2 | Serrated clutch half on the front leg; male centring spigot + leg tongue |
| 2 | `apex_hub_rear` | 2 | Serrated clutch half on the rear leg; female recess + nut capture |
| 3 | `foot_front` | 2 | Collinear cruciform spade (broad ballast plate + keel) + leg socket |
| 4 | `foot_rear` | 2 | Deeper cruciform spade, bigger keel for anti-tip/wobble + leg socket |
| 5 | `fabric_rail` | 2 | Near-full-length keyhole C-channel capturing the cloth's side rod hem |
| 6 | `crossbeam_fitting` | 6 | Tube-end plug + tongue, one per crossbeam end |
| 7 | `captive_pin` | 6–8 | Quick-release pin with tether eye (shock-cord captive) |
| 8 | `shade_clutch` | 2 | Friction shade pivot + arc-slot stop (±30°, default horizontal) |
| 9 | `shade_corner` | 4 | 90° tube-socket corners of the shade frame |

### Commodity struts (cut to length)
| Member | Stock | Ø | Length |
|--------|-------|----|--------|
| Crossbeam ×3 | Al / fibreglass tube | 16 mm | ≈ `TRACK_WIDTH` = 360 mm |
| Legs ×4 (modular variant) | Al / fibreglass tube | 16 mm | front 250 / rear 230 mm |
| Shade arm ×2 | Al / fibreglass tube | 16 mm | ≈ 300 mm |
| Shade frame rail ×2 | tube | 16 mm | `SHADE_FRAME_W` = 520 mm |
| Shade frame rail ×2 | tube | 16 mm | `SHADE_FRAME_D` = 420 mm |
| Sling / shade rod hems | fibreglass rod or 6 mm cord | 6–8 mm | per fabric edge |

### Hardware (optional but recommended)
- 2× M6 × 45 mm bolt + 2× M6 wing knob (or printed wing knob + M6 heat-set
  insert / nyloc) — apex clutch compression.
- 2× M6 × 35 mm bolt + wing knob — shade clutch.
- 6–8× 6 mm stainless clevis pins **or** the printed `captive_pin` — quick
  releases. Shock cord to tether pins so nothing is lost in the sand.

### Fabric
- 1× head cloth panel spanning the full front face (~**360 wide × 250 long**
  finished to suit `TRACK_WIDTH` × `FRONT_LEG_LEN`; hem both side edges into rod
  pockets for the rails).
- 1× shade cloth (~540 × 480 mm, hemmed into the frame rails, or simple corner
  ties for the prototype). Use ripstop / solution-dyed acrylic (Sunbrella-class)
  for UV life.

---

## 3. Suggested first-prototype dimensions

| Quantity | Value |
|----------|-------|
| Track width (frame centreline spacing) | 360 mm |
| Outside width | ≈ 400 mm |
| Front leg length | 250 mm |
| Rear leg length | 230 mm |
| Front-leg angle from vertical | 30° |
| Rear-leg angle (derived, feet on ground) | ≈ 20° |
| Apex height (deployed) | ≈ 216 mm |
| Apex included angle (this setting) | ≈ 50° |
| Head support height above sand | ≈ 200 mm at top of cloth, sloping to ground |
| Front spade | 82 W × 120 L × 6 t mm cruciform (46 keel) |
| Rear spade | 62 W × 130 L × 6 t mm cruciform (60 keel) |
| Head cloth (front face) | full ~360 W × ~250 L |
| Shade frame | 520 × 460 mm, **horizontal default**, ±30° tilt |
| Shade height above apex | 205 mm |
| Tube stock | 16 mm OD |

Deployed stance footprint ≈ 200 mm (front-to-rear feet) × 400 mm (wide).
Packed: a flat bundle ≈ 400 × 90 × 90 mm (struts + a fist-sized bag of nodes).

---

## 4. Parametric variables

All live at the top of [`parts.py`](parts.py). The ones you'll actually tune:

| Variable | Default | Meaning |
|----------|---------|---------|
| `TRACK_WIDTH` | 360 | Frame spacing = crossbeam span = head-cloth width |
| `FRONT_LEG_LEN` | 250 | Apex → front foot |
| `REAR_LEG_LEN` | 230 | Apex → rear foot |
| `FRONT_LEG_ANGLE` | 30° | Front lean (rear derived for ground contact) |
| `CLUTCH_D` | 58 | Apex clutch disc diameter |
| `CLUTCH_TEETH` | 24 | Teeth → 360/24 = **15° recline increments** |
| `CLUTCH_TOOTH_H` | 3.2 | Tooth engagement depth |
| `RAIL_LEN` | 215 | Cloth-captured length along the front leg (~full leg) |
| `RAIL_BORE_D` / `RAIL_SLOT_W` | 9 / 5 | Rod-hem bore / fabric mouth |
| `FOOT_BLADE_W_F/L_F` | 82 / 120 | Front ballast-plate width / spade length |
| `FOOT_KEEL_W_F` | 46 | Front keel-fin span (lateral grip) |
| `FOOT_BLADE_W_R/L_R` | 62 / 130 | Rear ballast-plate width / spade length |
| `FOOT_KEEL_W_R` | 60 | Rear keel-fin span |
| `SHADE_FRAME_W/D` | 520 / 460 | Shade panel size |
| `SHADE_TILT_RANGE` | 30 | Shade tilt allowed each way from horizontal |
| `SHADE_HEIGHT` | 205 | Shade frame height above the apex |
| `TUBE_OD` | 16 | Strut diameter |
| `PIN_D` | 6 | Quick-release pin |
| `CLR_SLIDE / CLR_SAND / CLR_PIN` | 0.30 / 0.55 / 0.40 | Tolerances |

### Recline range (apex clutch)
With `FRONT_LEG_ANGLE` and the 15° clutch increments the practical apex included
angle band is **≈ 35°–80°**, giving three natural use positions:
- **Low / flat (~75–80°):** apex low, head barely raised — lying flat, dozing.
- **Medium (~55–60°):** relaxed head + neck support — the default.
- **High / upright (~35–45°):** apex tall, head lifted — reading, watching the water.

---

## 5. Assembly sequence

1. **Build each side frame.** Slot a front leg (printed leg or 16 mm tube) into
   `apex_hub_front`'s tongue fork, drop a pin. Repeat with the rear leg into
   `apex_hub_rear`. Press the two hubs together (spigot into recess, teeth
   meshed), pass the M6 bolt, thread the wing knob. Do both sides.
2. **Set recline.** Loosen each wing knob, swing front/rear legs to the chosen
   detent, re-tighten by hand.
3. **Fit the feet.** Push a `foot_front` onto each front leg end, `foot_rear`
   onto each rear leg. (Integral on the printed-leg variant.)
4. **Tie the frames together.** Insert the three crossbeams: each tube already
   carries a `crossbeam_fitting`; drop its tongue into the matching clevis on
   apex hub / front foot / rear foot and pin. The unit is now rigid.
5. **Hang the head cloth.** Clip a `fabric_rail` onto each front leg (they run
   nearly the full leg length); slide the cloth's two side rod-hems down into the
   rails from the top so the panel covers the whole front face. Tension is set by
   crossbeam spacing / cloth width.
6. **Mount the shade.** Bolt a `shade_clutch` to each apex hub's outboard boss.
   Plug a shade arm into each — they hold the frame **horizontal** by default.
   Build the shade frame (`shade_corner` ×4 + four rails), drop the shade cloth's
   rods into the frame rails, clip the frame onto the arm ends. Tilt is limited
   to ≈ ±30° from horizontal by the clutch stop.
7. **Stake it.** Press the four feet into the sand; scuff sand back over the two
   front sand-shelves to load them.

Disassembly is the reverse; pins are shock-cord-captive so nothing is dropped.

---

## 6. Recommended print orientation (per part)

| Part | Orientation | Supports | Why |
|------|-------------|----------|-----|
| `apex_hub_front/rear` | Disc flat on bed, **teeth up** | None | V-flank teeth print as <45° ridges; tongue lies flat; bolt bore vertical |
| `foot_front/rear` | **Socket flat on bed, spade pointing up** (as modelled) | None | Spade tapers to a point so every layer is narrower than the one below — zero overhang, wide stable socket base |
| `fabric_rail` | **Stand vertical** (axis = Z), 215 mm tall | None | Constant cross-section extruded in Z = perfect walls; bore/slot are vertical; print 2 per plate |
| `crossbeam_fitting` | Plug down, **tongue up** | None | Round plug prints as a vertical cylinder; tongue + pin holes clean |
| `captive_pin` | **Stand on head** (shaft up) | None | Round shaft prints cleanest vertically; layer lines don't shear the pin |
| `shade_clutch` | Disc flat on bed | None | Friction grooves, arc slot, bolt bore and tongue pin all print vertical |
| `shade_corner` | One socket flat on bed, **diagonal** | Light | Both sockets ≥45°; or split orientation, glue — it's low-load |

General: align layer lines **across** the principal tension in each part; add a
1–2 line brim on the feet (tall narrow sockets on a thin blade).

---

## 7. Recommended material & print settings

> **Material:** PETG (tough, cheap, decent UV) or **ASA** (best UV + heat, the
> right call for a product that bakes on a beach). Avoid PLA — it creeps and
> goes brittle in sun/heat.
>
> **Structural parts** (hubs, feet, fittings): 0.24 mm layer, **4–5 walls**,
> **40–55 % gyroid** infill, no supports (per orientation table). Hubs and feet
> are the load path — do not skimp on walls here.
>
> **Fabric rail / shade corners:** 0.24 mm, 3 walls, 25 % infill.
>
> **Pins:** 0.2 mm, 4 walls, 60 % infill — or just use 6 mm stainless.

ASA prints best in an enclosure (warping); PETG is more forgiving open-air.
Add **0.55 mm** clearance on all tube-into-socket fits for sand tolerance, and
keep the printed-in **drainage holes** at the bottom of every socket so wet sand
washes out.

---

## 8. Likely failure points & reinforcement

| Risk | Mode | Reinforcement |
|------|------|---------------|
| **Apex tongue/fork root** | Highest bending moment in the whole product | Keep `CLUTCH_HUB_TONGUE_T ≥ 11 mm`, 5 walls, generous root fillet; use a steel cross-pin, not printed, at this joint |
| **Spade root** | Snaps where the cruciform meets the socket under forward load | The crossed keel + ballast plate self-gusset each other at the root; 5 walls; widen `FOOT_BLADE_T` to 7–8 mm in ASA; printing socket-down keeps layers along the spade, not across the root |
| **Clutch teeth shear** | Stripping under accidental 15–20 kg load | 24 coarse teeth share load; raise `CLUTCH_TOOTH_H` to 4 mm and `CLUTCH_D` to 64 mm for a heavy-duty variant; the positive lock means no creep |
| **Pin holes wallow out** | Repeated assembly + sand abrasion | Steel pins in printed holes; add 0.4 mm clearance + a chamfered lead-in; consider a brass eyelet |
| **Shade arm leverage in wind** | Long lever cracks the shade clutch | Keep arms short, let the cloth spill wind (don't over-tension); friction clutch should *slip before it breaks* — size the wing knob torque accordingly |
| **Sling rail splitting** | Fabric tension pries the C-channel open | Closed keyhole bore (not an open hook); back wall ≥4 mm; vertical print resists the splitting load in-plane |
| **UV embrittlement** | Surface crazing over seasons | ASA over PETG; darker pigments; treat printed parts as field-replaceable — that's the point of the modular nodes |

---

## 9. Prototype path

**V1 — print-everything prototype (faithful to brief).**
Printed legs (250/230 mm, flat-printed bars with integrated fork at the apex end
and integrated foot at the bottom), printed crossbeams allowed but better as
tubes. Goal: validate the clutch detents, the cloth cradle shape, foot holding
power in real sand. Cheapest to iterate; expect to reprint feet and tune
`FOOT_BLADE_W/L`, `FOOT_KEEL_W` and tooth count after the first beach test.

**V2 — improved hybrid (recommended production form).**
Swap printed legs for 16 mm fibreglass/aluminium tubes into the printed
foot/apex nodes. Outcome: lighter, far stronger (no layer-line bending failures),
smaller packed bundle, and the printed parts shrink to just the high-value nodes.
Add the steel cross-pins at the apex, a printed wing-knob with heat-set M6
insert, and shock-cord-captive pins. This is the version to actually carry to the
beach.

---

## 10. Optional simplified version (fewest parts)

Strip to the essential headrest, drop the shade and the rear crossbeam:

- **2× side frame** (each: 1 printed apex clutch pair + 2 tubes + 2 feet)
- **2× crossbeam** (apex + front only — the front sand-shelves + rear feet give
  enough stability without the rear tie for calm days)
- **1× head cloth** + 2 rails
- Replace the apex clutch with a **single friction pivot**: one M6 bolt + wing
  knob clamping two flat discs with a knurled (ring-of-bumps) friction face
  instead of teeth. Fewer features, hand-set to any angle, slightly less
  slip-proof — fine for a light-duty / kids version.

Part count drops from ~30 printed pieces to **~12**, no shade hardware, one
fabric panel. Prints in an afternoon.

---

### Files
- [`parts.py`](parts.py) — all 9 printed parts, parametric. `python parts.py` → `stl/`
- [`assembly.py`](assembly.py) — overview stance render
- `stl/` — ready-to-slice STLs
- `preview/` — multi-view renders
