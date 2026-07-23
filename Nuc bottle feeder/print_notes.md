# Print notes — Nuc bottle feeder (Bambu Lab X2D Combo)

## Order of printing

1. **`coupon_socket.stl`** (PLA is fine, ~15–20 min) — the real top 16 mm of the barrel.
   Test: bottle spins on freely by hand, seats on a gasket (drop the TPU gasket or any
   2 mm rubber disc in first), stops with the bottle's white bead ring at/above the rim,
   no wobble. Also spin the nut ring coupon onto its clamp thread.
2. **`coupon_nut_ring.stl`** (PLA, ~15 min) — threads onto the coupon's clamp thread;
   must run the full length by fingers, snug but never binding.
3. Only after both pass → the real parts in PETG/TPU.

If the bottle thread binds: raise `PCO_CLR_RADIAL` 0.32→0.40 and `PCO_CLR_AXIAL`
0.25→0.30 in `model.py`, re-run, reprint coupon. If the nut binds: `CLAMP_CLR_RADIAL`
0.30→0.40. One-line fixes by design.

## Per-part settings

| Part | Material | Orientation (as exported) | Walls | Infill | Notes |
|---|---|---|---|---|---|
| body | **PETG** (white/light!) | tray floor on bed, barrel up | **4** | 30% gyroid | ≥5 bottom layers; slight over-extrusion (flow ×1.02) for airtight walls; NO supports — cone is 45°, socket internals are vertical or bridged ring only |
| clamp_nut | PETG | exported upside-down (skirt flares up) — print as exported | 3 | 25% | no supports; skirt is 45° |
| plug | PETG | disc on bed, stub up | 3 | 25% | |
| bottle_adapter | PETG | stub (seal lip) on bed, cap opening up — print as exported | **4** | 30% | flow ×1.02 like the body — this part must be airtight; 45° cone under the disc, no supports |
| gasket_tpu | **TPU 95A** | flat | 2 | 100% | X2D: TPU on MAIN nozzle, external spool, 40–60 mm/s — **print 2**: one for the feeder seat, one for the adapter's internal seat |
| coupons | PLA | as exported | 3 | 15% | fit tests only — PLA never goes on the hive |

- **Why PETG:** 40 °C+ full-sun roof kills PLA (Tg ~57 °C); PETG (Tg ~80) + decent UV
  tolerance + syrup-safe + airtight-printable. ASA would also work; PETG chosen for food-
  adjacency and because the part is shaded by bottle+skirt. **Choose white or light silver
  filament** — halves solar gain on the barrel vs dark colors (thermal-flood margin).
- **Layer lines & hygiene:** 0.2 mm layers; the tray is open and smooth-walled — a bottle
  brush reaches everything; no blind pockets by design.
- Dual-nozzle job option: body PETG on main + gasket TPU cannot share a plate usefully —
  print separately (TPU wants slow speeds anyway).
- Bed: textured PEI, PETG default plate temps; no brim needed (150 mm disc + 1 mm chamfer).

## Print-order sanity checks in the slicer

- Body: confirm the slicer shows **zero support material**; the only bridge is the small
  ring between the 4 outlet ribs (~14 mm spans) at z≈7 mm and the flange's 0.6 mm ledge
  ring at z≈23–26 mm.
- Confirm seam position set to "aligned, rear" or hidden — a bulging seam inside the
  socket thread is the one slicer artifact that can tighten the bottle fit.
- Nut: prints on its (assembled) top face; bore chamfers both ends are modeled.

## Approx. plate times (0.4 nozzle, 0.2 mm, PETG defaults)

body ~4–5 h · nut ~1.5 h · plug ~40 min · adapter ~50 min · gaskets ~15 min · coupons ~35 min total.
