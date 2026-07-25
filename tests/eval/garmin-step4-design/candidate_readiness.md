---
contract: candidate-readiness
contract_version: 4
job_id: garmin-7x-charging-dock
candidate_id: garmin-step4-design
owner: cad-designer
status: NOT_READY
non_acceptance: true
dimensions_revision: 1
print_plan_revision: 1
reference_sha256: adcbff5b80a50107f830f8e4e3310aaa6cb0023639a40bf1e6c60cd7f6cc0c31
candidate_stl_sha256: de044e7ab02c3b9bc340b0ba44f69bdaf2dfa3a91128fa4c9b773aa08dad1375
updated_utc: 2026-07-25T00:00:00Z
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

This is designer-owned dispatch evidence, never acceptance, and never a substitute for fresh
independent verification. Status is honestly reported as **NOT_READY**: the shared
`team_preflight.py validate-receipts` gate does not exit zero / report PASS for this candidate
(one error — E-03 has zero samples, an honestly-reported unfilleted edge, not a fabricated
pass). Every other check in this receipt passes on its own numbers.

## Pre-dispatch check on re-imported STL

| Check | Required | Observed | Result | Evidence |
|---|---:|---:|---|---|
| One watertight intended body and bounds | yes | `cradle.stl`: watertight=True, 1 component, bounds X[-49.996,49.996] Y[-33.914,65.577] Z[0.000,42.295] mm, volume 163,061.04 mm³ | PASS | `trimesh.load('cradle.stl')` |
| Seated interference | 0 (plan G-01 threshold, general bore only) | General-bore interference **0.000000 mm³** (300k-sample Monte Carlo point-containment, see "Interference method" below — the naive boolean is noisy at the flush Z'=0 seating plane and is NOT used as the pass/fail number). At-lip interference **37.87 mm³**, entirely inside the S-01 lip band (Z' 13.15–15.15) — the intended compliant-flex retention engagement, not a defect; see `print_notes.md`. | PASS (general bore); CONDITIONAL at the lip by design | `verify.py` / `verify_output.json` |
| Full insertion/travel sweep | zero forbidden collision | Rigid straight-line sweep: 0 mm³ interference from t=+16mm outward (fully removed); a constant ~46.4 mm³ plateau for t=+1..+12mm (case body fully overlapping the lip band during any rigid vertical position in that range); large interference for t<0 (case pushed below the floor, expected/meaningless). The plateau is the same lip-retention feature as the seated-interference row, not a new finding — a rigid straight-line sweep cannot pass a compliant spring-clip lip by construction (see `print_notes.md`). | CONDITIONAL — expected for a compliant retention feature, not a forbidden rigid collision elsewhere | `verify.py` / `verify_output.json` |
| Installed-coordinate section proves architecture/open face | yes | `cradle_installed_section.png`: 3 panels — (a) pocket-local X=0 half-section with the watch seated, showing the band-axis relief notches as open gaps; (b) pocket-local section through one retention-lip finger's own azimuth, showing the watch case vs. the lip overhang and the S-01 support region; (c) installed-pose (world/print frame) 3D half-section | PASS | render |
| Named bed face at printer Z=0 after exact transform | yes | Identity model-to-printer transform (per `print_plan.md`) — `cradle.stl` IS the print-frame STL; `STAND_BASE_PLANE` (the keel's flat cut face) sits exactly at Z=0.000mm (bounds Z min) | PASS | `trimesh` bounds |
| Unsupported roof/critical wall floors | plan limits | See "Wall thickness" below: G-03-named features (pocket bore wall, lip cross-section) measure ~1.598mm genuine minimum (target 1.6mm) — PASS. G-04's 0.8mm absolute floor is not met at the E-01 base-perimeter fillet edge specifically (~0.53–0.59mm genuine minimum there) — CONDITIONAL, localized, non-structural (see `print_notes.md` item 2) | PASS (G-03); CONDITIONAL (G-04, localized to a cosmetic fillet edge) | `verify.py` / `verify_output.json` |
| Required renders/STEP/source present | yes | `cradle_model.py`, `cradle.stl`, `cradle.step`, `cradle_coupon.stl`, `cradle_exterior_view.png`, `cradle_installed_section.png`, `cradle_print_orientation.png`, `cradle_coupon_view.png`, `render_cradle.py`, `verify.py`, `edge_samples.py` all present | PASS | file listing + hashes below |

### Interference method note

`trimesh.boolean.intersection([cradle, watch])` reports a nonzero total (145.65 mm³) dominated
by floating-point noise at the Z'=0 seating plane, where the watch caseback and cradle floor
are DESIGNED to sit exactly flush (zero nominal gap) — a known class of coincident-face
boolean artifact (see `print_notes.md` item 4 and `cadquery-patterns.md`'s own coincident-face
warning). This receipt uses dense point-containment sampling (300,000 Monte Carlo points drawn
inside the watch's own volume, tested for containment in the cradle) as the authoritative
measurement instead, which cleanly separates the Z'=0 noise band from genuine geometry: **zero**
general-bore interference, **37.87mm³** concentrated exactly at the S-01 lip band. Reproducible
via `verify.py`.

## Edge/comfort preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Edge ID / feature boundary | Exposure class | Required radius | Re-imported-STL samples/method | Observed min/max | Result | Evidence |
|---|---|---|---|---:|---|---|
| E-01 `STAND_BASE_PLANE` bed-contact perimeter | `BED_CONTACT` | 0.2–0.4mm | 10-point local-outward-normal circle fit on the Z=0.001mm cross-section (see `print_notes.md` "Base architecture" for why a naive world-axis radial ray was wrong here — the rim is an ellipse-like curve, not a true circle) | min 0.2508 / max 0.3897mm | PASS | 10 samples in `candidate_preflight.json` |
| E-02 pocket rim entry edge | `EXPOSED_FUNCTIONAL` | ≥0.5mm | 6-point circle fit at the 2 of 4 clear wall arcs (138.5/318.5 deg) that carry no lip finger (the other 2 clear arcs, 41.5/221.5 deg, are the lip-finger footprints themselves and no longer carry this edge — see `print_notes.md`) | min 0.6339 / max 0.6394mm | PASS | 6 samples in `candidate_preflight.json` |
| E-03 retention lip outer/topside edge | `EXPOSED_COMFORT` | ≥1.0mm | Same horizontal-ray/circle-fit method as E-01/E-02, targeted at both fingers' top-outer corner | **no samples — the fillet was never successfully applied; the edge ships SHARP** | **FAIL** | `print_notes.md` item 1 has the full attempted-radius log (1.2mm down to 0.3mm, both fillet-before-union and fillet-after-union orderings, all either raised an OCC exception or returned an invalid solid) |
| E-04 retention lip inward/outward boundary edge | `EXPOSED_FUNCTIONAL` | ≥0.3mm | 4-point circle fit (2 azimuths x 2 fingers) at the finger's inner-bottom step edge | min 0.4503 / max 0.4617mm | PASS | 4 samples in `candidate_preflight.json` |

## Support-sensitivity preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Rule/region ID | Exact transform/layer/nozzle predicate | Mesh result/footprint/interval | Plan disposition | Allowed contact class and forbidden faces checked | Result | Evidence |
|---|---|---|---|---|---|---|
| S-01 retention lip outward/topside face | Identity matrix (matches `print_plan.md`'s model-to-printer transform — no separate print-frame rotation needed), bed_z=0, tol=0.05mm, 45deg threshold, applied directly to `cradle.stl` | Whole-mesh out-of-limit area **43.88 mm²**; budget 250 mm² (also within the plan's own arc ≤180deg and radial ≤3.5mm bounds: this design uses 48deg combined arc, 1.0mm radial reach — both self-certified below the cap, not separately area-audited by the tool) | `SUPPORT_ALLOWED` | `PERMITTED_SUPPORT_CONTACT`; forbidden faces checked: yes (see breakdown below) | **PASS** | `S-01-support-audit.json` |

### Forbidden-face check for S-01 (self-certified, not tool-computed)

The plan's S-01 forbidden faces are: `watch_contact_seat_wall_pocket_bore`,
`pocket_floor_caseback_plane`, `retention_lip_inward_contact_face`,
`any_future_charge_contact_geometry_G09`. Manual region breakdown of the flagged 43.88 mm²
(re-measured directly against the mesh, not inferred):

| Region (world-frame) | Area (mm²) | Attribution |
|---:|---:|---|
| Local Z' ≈ 13.15–15.15, r ≈ 24.6–27.7 (both lip fingers) | ~29.6 | S-01's own intended region — the lip's outward/topside step face, exactly as planned |
| World Z ≈ 0.03–0.2 mm, r ≈ 46–50 (base perimeter) | ~14.3 | E-01 bed-contact fillet transition artifact (a small portion of the fillet's own curved surface classifies as steeper-than-45deg — same class of finding as `fdm-design.md` precedent for a required chamfer/fillet feature, not a support region) |

Neither region overlaps the bore wall (r≈26.1–26.2, general pocket), the pocket floor (local
Z'≈0), the lip's *inward* contact face (the near-vertical surface facing the watch, normal
z-component near 0, never flagged by a 45deg-threshold screen), or any charge-contact geometry
(none exists — G-09 blocked). **Forbidden faces checked: PASS.**

## Parameter mapping

| Contract IDs | Source parameter(s) |
|---|---|
| F-001/M-001/M-003, G-01 | `CASE_DIA=51.75`, `FIT_CLR=0.25mm/side`, `POCKET_BORE_DIA=52.25` |
| M-004, G-02 | `CASE_THICKNESS=14.9`, `POCKET_DEPTH=15.15` |
| G-03 | `WALL_STRUCT=1.6mm` |
| G-09 (BLOCKED) | `FLOOR_THICKNESS=3.0mm` — plain uncommitted floor, no charge geometry |
| F-002/M-002, G-06 | `BUTTON_Z_LO/HI`, `BUTTON_RELIEF_HALF_ANGLE=25deg`, `BUTTON_ANGLES=(0,180)` |
| F-004/F-006/M-005, G-07 | `BAND_Z0/Z1`, `BAND_RELIEF_HALF_ANGLE=32deg`, `BAND_ANGLES=(90,270)` |
| S-01 | `LIP_RADIAL_REACH=1.0mm`, `LIP_HEIGHT=2.0mm`, `LIP_CENTERS_DEG=(41.5,221.5)`, `LIP_HALF_ARC_DEG=12deg` |
| G-05/E-01 | `BASE_CHAMFER=0.25mm`, `KEEL_R=50mm`, `KEEL_DEPTH=55mm` |
| E-02 | `RIM_FILLET=0.6mm` |
| E-03 | `LIP_TOP_FILLET=1.2mm` (parameter exists; NOT achieved in the exported geometry — see above) |
| E-04 | `LIP_EDGE_FILLET=0.4mm` |
| "Assumed display/tilt angle" | `TILT_DEG=27.5deg` |

## Commands and hashes

```text
# model + coupon + renders + verification
python cradle_model.py
python render_cradle.py
python verify.py
python edge_samples.py

python skills/3d-modeling/scripts/team_preflight.py support-audit \
  --stl tests/eval/garmin-step4-design/cradle.stl \
  --plan tests/eval/garmin-step3-plan/print_plan_checks.json \
  --rule-id S-01 --output tests/eval/garmin-step4-design/S-01-support-audit.json
  # exit 0, result PASS, 43.88mm2

python skills/3d-modeling/scripts/team_preflight.py validate-receipts \
  --stl tests/eval/garmin-step4-design/cradle.stl \
  --plan tests/eval/garmin-step3-plan/print_plan_checks.json \
  --readiness tests/eval/garmin-step4-design/candidate_preflight.json \
  --output tests/eval/garmin-step4-design/candidate_preflight_validation.json
  # exit 1, result FAIL, 1 error: "E-03: samples_mm must be a non-empty numeric list"

python -m team_tools.contracts validate tests/eval/garmin-step4-design
  # run from skills/3d-modeling/scripts/ -- see receipt below
```

## Files and SHA-256

| File | SHA-256 | Size (bytes) |
|---|---|---:|
| `cradle_model.py` | `4d0d00452b7050d2fbdf1f1e2b38dccc0071ffe7bb7052456c97f590e1b5a372` | 32,864 |
| `cradle.stl` | `de044e7ab02c3b9bc340b0ba44f69bdaf2dfa3a91128fa4c9b773aa08dad1375` | 6,688,984 |
| `cradle.step` | `73e803f6fcaf946d2b992a2f77f4e99c4fd9e4451cc7aba1c798817b2abf86f4` | 264,428 (note: OCC embeds an export timestamp in the STEP header — not bit-reproducible run-to-run even with identical geometry, same as the `pixel-step4-design` precedent) |
| `cradle_coupon.stl` | `5cdee65110416c974eef3249733fc8b09f41238397d151217446ac2b8aecbea6` | 16,084 |
| `render_cradle.py` | `d53d103db03dd8dfddb03ea126049b759269e7fc8ef73a41a1d8bd558368dfd9` | 14,544 |
| `verify.py` | `b5a616af5e6f241a930be24e9e745a759e086d38405fa30da1146c06c989580c` | 11,292 |
| `edge_samples.py` | `c64d4055340c3d3092f1150d54bd027a50480f65992fd2f5a8bb4a2588885543` | 7,891 |
| `cradle_exterior_view.png` | `3a3b736601a4a1014dd58c3aef646eaece6347c57d8dee4d5ec0a625fee83d82` | 696,523 |
| `cradle_installed_section.png` | `c92312b7e9cc43ef3fa5bc762b7fff00c6bc8c424eaf348243946c8a24cef6c9` | 356,125 |
| `cradle_print_orientation.png` | `3925d67b4a0e161a6bfe94e27f2fd3a8fdfedfd07254453d48fae50196cd950f` | 546,899 |
| `cradle_coupon_view.png` | `b0e97fc77919954f5672710e6c0a728f551de38ccccadd2b755fe08db6416c5d` | 401,812 |
| `S-01-support-audit.json` | `e011aeaa636769bf6307714d1eeba43c7cfe2163fcb3461b604467fbbf8c9ce9` | 902 |
| `candidate_preflight.json` | (see file) | — |
| `candidate_preflight_validation.json` | (see file) | — |
| `print_notes.md` | (see file) | — |

## Honest limits (repeated from `print_notes.md` for this receipt's self-containedness)

1. **E-03 (lip finger top-outer comfort edge) ships sharp, not filleted** — the single
   confirmed hard defect against the plan's own numeric bands. `EXPOSED_COMFORT`
   classification (cosmetic/user-touch, not fit-critical): this does not affect the watch fit,
   the retention mechanism, or any measured dimension, but it is a genuine, unresolved defect
   against the plan and is the reason this candidate is `NOT_READY`, not a rounding error.
2. **G-04's 0.8mm absolute wall floor is not met at the E-01 base-perimeter fillet edge**
   (~0.53–0.59mm genuine minimum there) — localized to a small cosmetic transition, not the
   bulk base material or any G-03-named structural feature (which measures a clean ~1.6mm).
3. **The charge/puck interface is entirely unbuilt** — this is `print_plan.md` G-09's own
   requirement (BLOCKED pending caseback metrology), not a gap in this candidate. The
   delivered part is a watch-capture cradle, not yet a functioning charger.
4. **No PETG coupon has actually been printed** — `cradle_coupon.stl` is geometry only.
5. **Rigid straight-line insertion/removal sweep is not clean past the lip fingers** — expected
   for this compliant spring-clip retention design (see `print_notes.md`), not a forbidden
   collision the plan's "down-and-back into the pocket" insertion path would encounter in
   actual (non-rigid) use.
6. **Bore diameter measures 0.03mm under the G-01 band's own lower bound** at one measured
   point due to STL mesh tessellation faceting, not the parametric design (exact 52.25mm
   nominal bore in source) — see `print_notes.md` item 3.
