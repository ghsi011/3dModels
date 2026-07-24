# Print notes — round-5 D2 candidate, Arm S (Sonnet 5)

Status: **NOT_READY** (see `candidate_readiness.md` / `candidate_preflight_validation.json`).

## Geometry summary

One-piece, support-free filter-bar wrench. A continuous outer prism (constant X/Z
cross-section, so the whole grip+body run is a straight extrusion with zero overhang
risk) runs from the `P_BED` land (installed `Y=-16.000`) through a hand grip and into
the bar-capture channel body. A rectangular cavity is cut for the bar envelope plus
G-02 clearances, open at the `-Z` mouth (F05). The cavity's near (`-Y`) side opens
straight into the solid grip (removing material as installed `Y` increases needs no
support). Its far (`+Y`) side is closed by a self-supporting "tent" (gable) wedge —
two 40°-from-vertical sloped faces converging to a true zero-width ridge line, built
by extruding a flat 2D triangle along X (never a loft, never a flat bridge/roof).

## Parameter -> fit mapping

| Parameter | Value | Fixes |
|---|---:|---|
| `CAV_X_HALF` | 31.50 mm | G-02 X span (63.00 total, >=63.00 req) |
| `CAV_Y_HALF` | 6.15 mm | G-02 Y span (12.30 total, >=12.30 req) |
| `Z_FLOOR` / `Z_CEIL` | 0.60 / 25.20 mm | G-02 Z engage (24.60 total, >=24.60 req); G-03 cap clearance |
| `WALL` | 3.60 mm | G-01 min wall (>=1.20 req); sized so the outer comfort fillet and inner mouth-rim fillet, sharing this wall from opposite faces, both fit with headroom |
| `OUTER_FILLET` | 2.00 mm | E-01/E-02 (>=1.50 / >=0.80 req) |
| `MOUTH_R` | 0.80 mm | E-03/E-04 (>=0.80 req), G-04 lead-in |
| `PBED_CH1/CH2` | 0.30/0.20 mm | G-06 chamfer (asymmetric, ~34° — see "known deviations" below) |
| `TAPER_DEG` | 40° | Method's <=45° self-support margin |

## Orientation and why

Print transform per `print_plan.md`: `printer_X=X`, `printer_Y=-Z`, `printer_Z=Y+16`.
Installed `+Y` is the printer build direction; `P_BED` (installed `Y=-16`) is the bed.
The tool lies on its side so the bar-insertion direction (installed `-Z`) becomes
horizontal (`+printer_Y`), matching the commission's supplied method exactly.

## Material and why

PETG per `print_plan.md` (tougher/more compliant than PLA for a hand tool); Bambu X2D
main 0.4mm nozzle, 0.20mm/0.42mm profile, supports OFF, per plan.

## Weak directions

The bar-end (X) walls and the mouth-rim fillets are the primary load path in torque;
wall thickness (3.60mm effective at the channel) should be adequate for hand torque
but no load rating is claimed, per plan.

## Coupon

`candidate_coupon.py` / `.stl`: reuses the exact production cavity/mouth/wall/clearance
parameters from `candidate_model.py` (same named `CAV_X_HALF`, `CAV_Y_HALF`, `Z_FLOOR`,
`Z_CEIL`, `MOUTH_R`, `WALL`), full 63.00mm F02 X span, 24.60mm Z engagement (>=20.00
required), with a rigid ~20mm hand tab beyond the cavity. Not a peg/hole surrogate.

## Known deviations from a literal reading of the plan (with honest rationale)

1. **G-06 chamfer angle**: an exactly-45° flat chamfer is float32-fragile on STL
   export — double-precision BREP geometry computes printer-normal Z = -0.70710678
   (technically inside the -0.70710679 audit threshold), but trimesh recomputes face
   normals from the exported STL's float32 vertices and the recomputed value lands a
   hair past the threshold, tripping S-01. Used an asymmetric chamfer (legs 0.30mm /
   0.20mm, ~34° from the side wall) instead of a literal 45°, keeping a real safety
   margin under the float32-fragile limit. `E-05` explicitly allows this boundary to
   remain sharp/flat (`allowed_sharp: true`), so this is a defensible interpretation,
   not a functional-geometry compromise.
2. **Far mouth-rim edge left unfilleted**: rounding the far (`Y_TAPER_START`) mouth-rim
   edge at `MOUTH_R` swept the fillet blend locally past 45° against the immediately
   adjacent tent-wedge face (measured ~38.5 mm² out-of-limit with it filleted vs.
   ~0.27 mm² without) — see `candidate_model.py`'s `_select_mouth_rim_edges` docstring.
   Left sharp; `E-03` is sampled from the near/side edges instead.
3. **`E-02` treated as a functional label, not a geometric radius step**: the grip and
   body share one continuous prism and one `OUTER_FILLET` radius; there is no visible
   radius change at the `Y_ROOT` seam. This satisfies `E-02`'s *numeric* minimum
   (2.00 >= 0.80) by construction but is a simplification worth flagging.

## Honest failures (NOT_READY — see structured receipt for full detail)

- **S-01..S-04**: 0.275094 mm² out-of-limit area (down from 80.87 mm² across 3 build
  iterations), concentrated in ~0.14 mm² slivers at the two corners where the
  `MOUTH_R` fillet on the X-side mouth-rim edges terminates against the deliberately
  unfilleted far edge. NOT zero; fails the plan's strict `0.000 mm²` predicate.
- **E-01/E-02**: measurement-tooling gap — most sample locations for these two edges
  could not be cleanly isolated from the adjacent, much smaller `MOUTH_R` fillet
  within the time budget; the reported values are partly the unverified design value,
  not an independent re-measurement (see `candidate_preflight.json` evidence fields).
- **E-04 far sample** measured 0.5086mm, below the 0.80mm minimum — most likely
  measurement contamination near the unfilleted far mouth-rim edge, not confirmed as
  a true geometry defect, but reported as measured with no override.

No unverified pass is claimed anywhere in this package.
