---
contract: print-plan
contract_version: 4
job_id: pixel7-case-metrology
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 1
reference_sha256: 5d683184b814d7089b4075354b81aa45aa8aaae35aa0bb45c12324aaea692b7f
updated_utc: 2026-07-24T22:00:00Z
---

# Print plan — Google Pixel 7 protective case

Pre-design commission (step ③). Inputs read: `tests/eval/step1-metrology-pixel7/dimensions.md`
(rev 1), `tests/eval/step2-reference-pixel7/phone_reference.stl` +
`reference_manifest.md`, `skills/3d-print-engineer/SKILL.md`,
`skills/3d-modeling/references/{team-contracts-v4.md, fdm-design.md, printers.md,
materials.md}`. No case geometry was designed; this issues the manufacturing contract the
CAD designer must build to.

## Process

| Printer/material/nozzle | Layer | Environment/load | Rationale |
|---|---:|---|---|
| Bambu Lab X2D Combo — main nozzle only, TPU 95A shore (external spool; no soft TPU through AMS per printer profile), 0.4 mm hardened, single-nozzle job → full 256×256×260 mm envelope (not the dual-nozzle-reduced 235.5×256×256; case footprint 155.6×73.8×~14 mm fits either way but no second material/color is planned) | 0.16 mm (0.12–0.20 acceptable) | Worn on the phone (pocket/hand/bag); core load is drop/impact absorption, not sustained structural load. Incidental hot-car cabin exposure (60–80 °C ambient per fdm-design.md §7) is possible but the case is normally attached to the phone, not left loose on a black dash (105 °C) | See "Material choice" below |

### Material choice: TPU over PETG, justified

- **Core function is impact absorption, not rigidity.** A protective case's job is to flex
  and dissipate drop energy. Rigid PETG is tougher than PLA but still an engineering
  plastic that cracks/chips at thin corner sections under impact rather than yielding;
  TPU compresses and rebounds. This is the primary reason nearly all functional printed
  and commercial phone cases use TPU/silicone, not a rigid polymer, and it is the
  deciding factor here.
- **Compliance buys margin against a live, unresolved dimensional conflict.** OQ-01 in
  `dimensions.md` is open: three independent caliper reads (9.5/9.6/9.8 mm) cluster
  0.8–1.1 mm above the 8.7 mm spec nominal used to build the accepted reference. Per
  fdm-design.md §4 ("Compliance beats precision... build in flex"), TPU's elasticity
  gives the M-019 snug-sliding band (0.10–0.30 mm/side) real headroom against that spread
  — a rigid PETG case at the same nominal band has no way to absorb a thicker real phone
  short of hard interference, and a PETG case built loose to be safe would rattle. TPU
  turns an unresolved metrology question into a survivable manufacturing risk instead of a
  binary pass/fail.
- **Honest environmental caveat (not silently dropped):** TPU's stated service range tops
  out at +80 °C; ASA/PETG tolerate the 105 °C dash-surface extreme from fdm-design.md §7
  better. This plan accepts that trade because the case is normally attached to and used
  with the phone (which itself throttles/shuts down well below 80 °C), not stored loose
  on a dashboard — a genuine but low-probability residual risk, stated here rather than
  hidden. If the user reports leaving the assembled phone+case directly on a sun-heated
  dash for extended periods, this material choice should be revisited.
- **PETG would win only if** the case needed to resist sustained high heat with no drop
  risk (e.g., a dash mount) or needed tighter dimensional repeatability than TPU offers —
  neither is this job's dominant requirement.

### Drying / prep

Dry TPU 4–6 h @ 55–60 °C before printing (lower than ASA/PETG — TPU deforms if dried too
hot). Cool Mode (no active chamber heat) — TPU does not need the 65 °C Heat Mode ASA/PA
use, and excess chamber heat softens TPU mid-print. Print speed 40–60 mm/s per the
printer profile's TPU recipe; moderate-high part cooling so each thin bridge (button/port
window roofs, §"Clearance features" below) solidifies before the next layer.

## Model-to-printer transform

| Item | Exact value |
|---|---|
| Transform/rotation | 180° rotation about the model **+X axis** (width axis, D5_LEFT→D4_RIGHT) applied to the coordinate frame defined in `dimensions.md` §Frame / `phone_reference.py`. Rotation matrix `R = diag(1, -1, -1)`, i.e. `(x, y, z) → (x, -y, -z)`. This is a proper rotation (det = +1): no mirroring, handedness and D4_RIGHT/D5_LEFT (button/SIM sidedness) are preserved. Translation: Z-only, chosen so the bed-contact landmark below lands exactly at printer Z=0; no X/Y translation (part stays centered on D1_CTR's X,Y projection). |
| Bed-contact landmark | **Open-rim plane** — the planar loop at the outer boundary of the case's front (phone-insertion) opening: the case's own front face, beyond D6_SCREEN at maximum model +Z, spanning the full wall cross-section around the opening (all four sides + four corners). |
| Bed normal | Printer **+Z** `[0,0,1]`. Equals the model's original **−Z** direction after rotation — the case's back (camera bar, logo) points toward printer +Z and is the last-printed, topmost feature. |
| Open/insertion direction | Physical use (not print build): phone travels along model **−Z**, entering at the open rim (max model Z) and seating against the case's back wall (min model Z, beyond D0_BACK). This is unrelated to build direction; stated for the designer/verifier's installed-pose checks. |
| Forbidden downward faces | All interior faces of the fit-critical cavity (D4_RIGHT/D5_LEFT/D2_TOP/D3_BOT walls), the camera-bar relief walls (F-003 relief), and all button/port/mic window edges, evaluated in the exact transform above. The **only** permitted downward/bed-contact geometry is the open-rim perimeter itself (G-04 below). Any other face returning a downward-facing normal beyond the 45° threshold is a print-plan violation, not a silent support add — see G-11. |

### Why this orientation (not back-down)

Two orientations were compared: **rim-down** (chosen) vs. **back-down** (back plate flat
on the bed, rim up). Back-down gives a larger first-layer footprint (lower warp risk) but
loses on the feature that actually drives this case's DFM: the camera-bar relief needs a
raised protective ring standing proud of the general back plane (so the case, not the
lens, contacts a table when set face-down). In back-down orientation that ring is the
*lowest* point of the model — the rest of the back plate floats above the bed by the
ring's height and needs support under a large, cosmetically visible span. In **rim-down**
orientation the same ring becomes an upward-protruding boss on the last-printed top face —
a normal, self-supporting print feature (§G-07). This is the "support-free is the
default, not an absolute" trade in practice: rather than reach for `SUPPORT_ALLOWED` on a
cosmetic-but-visible back panel, the orientation itself removes the need. The fit-critical
cavity walls are vertical in *either* orientation, so this choice costs nothing on fit —
it only wins the camera boss. The rim being bed-contact does put the elephant-foot risk at
the insertion mouth, which is why G-04 requires the chamfer there explicitly (and why a
chamfer at an entry rim is a net *insertion aid*, not a defect, when sized inside the
M-019 band).

## Geometry rules and phase scope

| ID | Rule | Numeric limit | Disposition | Verification predicate | required_now | deferred_owner | final_gate |
|---|---|---:|---|---|---|---|---|
| G-01 | Body-envelope cavity clearance (M-019 carried, bounded band, never a floor) | 0.10–0.30 mm/side, both bounds enforced | N/A (clearance, not support) | Per-side gap between candidate cavity wall and `phone_reference.stl`, sampled ≥8 zones (4 walls + 4 corners) on re-imported STL | Candidate reports min AND max per-side gap at all 8 zones; over-clearance fails exactly like interference | none | none |
| G-02 | Body-thickness planning nominal (OQ-01 carried, not silently resolved) | Cavity built against reference T = 8.7 mm (phone_reference.stl Z ∈ [−2.74, 8.7]); NOT the 9.5–9.8 mm caliper cluster | N/A | Candidate Z-span audit vs. reference; TPU compliance (not a widened nominal) is the stated mitigation for the 0.8–1.1 mm spread | Candidate builds cavity against the frozen reference envelope only | metrologist (flat-region re-measurement per OQ-01's own approved bound) + print engineer (coupon confirmation) | PRINT_PREP — coupon must confirm actual unit thickness at a flat, button-free region before final-material (TPU) full-part commitment; if actual exceeds 8.7+0.30 mm this plan revision is invalidated per the plan-revision rule (acceptance threshold change) |
| G-03 | Corner radius carry-through (F-002/M-004) — least-accurate region, relieve rather than chase | cavity R ≥ 9.5 mm (never undersized), up to 11.0 mm relief permitted | N/A (edge) | Candidate corner radius sampled at each of 4 corners (start/mid/end of arc) on exported STL | 4 corners measured, all within band | none | none |
| G-04 | Elephant-foot chamfer at the open rim (bed-contact landmark) | 0.2–0.4 mm, 45°, around the full rim loop | N/A (edge) | Section render at ≥4 rim locations (one per side) on the exact planned-orientation STL | Chamfer present and measured at all 4 locations | none | none |
| G-05 | Minimum wall / feature floor | Nominal 1.6 mm (4×0.4 mm line width) structural walls; 1.2 mm absolute structural floor; 0.8 mm (2×nozzle) hard floor never violated anywhere | N/A | Wall-thickness ray-cast/section audit on exported STL in planned orientation | Full-body audit, zero sub-0.8 mm regions | none | none |
| G-06 | Camera-bar relief clearance (M-020 carried) | 0.30–0.50 mm/side around F-003 footprint (full W × 20.4 mm, 2.74 mm protrusion) | N/A (clearance) | Measured clearance vs. reference camera-bar geometry, ≥6 sample points (perimeter + roof) | Reported at all 6 points | none | none |
| G-07 | Camera-bar relief boss — self-support (orientation-driven, see "Why this orientation") | Boss taper ≤45° from vertical in the planned transform | **SELF_SUPPORT_REQUIRED** | Printability check 7 (planned-orientation face audit): zero out-of-limit downward area within the boss footprint | Proven now — the orientation makes this achievable at zero support; no deferral | none | none |
| G-08 | Button windows (F-006/F-007, M-021 carried: 0.30–0.50 mm/side over the full stated range; sheet's own strategy is one elongated window ≈38 mm rather than two tight holes) | Bridge span ≤25 mm ("fine" per fdm-design.md §1) is self-supporting; a span >25 mm (e.g. the full elongated M-021 zone) requires either an internal self-supporting rib splitting it into ≤25 mm segments, or explicit bounded support on the opening only | **SELF_SUPPORT_REQUIRED** for any span ≤25 mm; **SUPPORT_ALLOWED** (bounded, nonfunctional region only) for the excess if a span >25 mm is built unribbed | Candidate reports actual chosen span(s); printability check 7 + support-audit for any span >25 mm | Candidate must state its chosen span and disposition; if >25 mm, must produce the support-audit artifact | candidate designer chooses rib vs. support at CANDIDATE_BUILD | INDEPENDENT_VERIFICATION — verifier reruns support-audit for any span >25 mm before PASS; the opening (a loose pass-through clearance, not a mating face) is the only permitted contact region — never the exterior cosmetic face or the button-rocker contact pad |
| G-09 | Port/grille cutouts (F-010/F-011/F-012, M-022 carried: 0.30–0.50 mm/side or one shared bottom slot) | Spans 6–9 mm, well under the 25 mm bridge threshold | **SELF_SUPPORT_REQUIRED** | Printability check 7, trivial bridge | Reported, zero out-of-limit area expected | none | none |
| G-10 | Ancillary reliefs — top mic hole (F-009), SIM-tray access (F-008, non-fit-critical per sheet, access-only) | Trivial size, no fit action required beyond bounded position per dimensions.md | **SELF_SUPPORT_REQUIRED** if modeled at all | Printability check 7 | Reported if present | none | none |
| G-11 | Forbidden downward faces — catch-all | Zero unplanned downward-facing area (beyond G-07/G-08/G-09/rim chamfer) anywhere, in the exact planned transform | **SELF_SUPPORT_REQUIRED** | Full-body printability check 7 | Full-body audit, zero unplanned downward area | none | none — any newly discovered downward face routes back to `PRE_DESIGN_PRINT_PLAN` (this contract) for revision; never silently added as late support |

### Clearance features — camera cutout, button windows, port/speaker cutouts

| Feature | Sheet source | Clearance band | Max unribbed bridge span in this orientation | Disposition |
|---|---|---|---|---|
| Camera cutout + raised protective boss (F-003 relief) | M-020 | 0.30–0.50 mm/side | boss is a self-supporting upward protrusion, not a bridge (see G-07/"Why this orientation") | SELF_SUPPORT_REQUIRED |
| Volume-rocker window (F-006) | M-021 | 0.30–0.50 mm/side over the full ±8 mm-uncertainty range | ≤25 mm self-supporting; sheet's elongated-window strategy (≈38 mm) needs a rib or bounded support | SELF_SUPPORT_REQUIRED ≤25 mm / SUPPORT_ALLOWED beyond (G-08) |
| Power-button window (F-007) | M-021 | 0.30–0.50 mm/side over the full ±7 mm-uncertainty range | same as above; nominal 10 mm span alone is trivially self-supporting | SELF_SUPPORT_REQUIRED ≤25 mm / SUPPORT_ALLOWED beyond (G-08) |
| USB-C port (F-010) | M-022 | 0.30–0.50 mm/side | ~8.5 mm, trivial | SELF_SUPPORT_REQUIRED |
| Bottom-left / bottom-right speaker-mic grilles (F-011/F-012) | M-022 | 0.30–0.50 mm/side, or one shared bottom slot | ~6 mm each / shared slot still well under 25 mm | SELF_SUPPORT_REQUIRED |
| Top mic relief (F-009) | dimensions.md, bounded C-grade | small relief or leave open | trivial | SELF_SUPPORT_REQUIRED |
| SIM-tray region (F-008) | dimensions.md — non-fit-critical, access-only | none required | n/a | n/a — no case action mandated |

## Coupon

| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|
| D4_RIGHT × D2_TOP corner + one full-height segment of each adjacent wall (captures F-002 corner radius and the M-019 snug-sliding band on two orthogonal walls at once), the G-04 elephant-foot rim-chamfer base, and a partial witness of the F-006 volume-rocker window (to empirically test the ≤25 mm self-supporting bridge call in G-08) | M-019 snug-sliding 0.10–0.30 mm/side on both wall lanes (step a 0.10/0.20/0.30 mm ladder into the coupon if the corner section is large enough for more than one lane per wall) | Same coupon STL, printed twice — **not** two files: (1) **PLA** rapid pass (~15 min) for pure geometry/self-support proof (camera-boss taper if included in the corner, button-window bridge cleanliness, rim-chamfer profile, corner-radius accuracy) — does not validate the elastic fit; (2) **TPU** (final material) pass for the actual compliant snug fit AND to close OQ-01 by direct caliper measurement of the real phone at a flat, button-free region before the full case is committed | PLA lane: prints with zero support, chamfer measures 0.2–0.4 mm at 45°, corner radius measures 9.5 ± 0.3 mm, button-window bridge shows no visible sag/gap. TPU lane: the phone's real corner seats into the coupon with firm hand pressure (snug, not free-sliding), stays captured without user support (no gravity slip-out), no visible gap or rock at either wall face, and the coupon session records the phone's actual flat-region thickness reading — this closes G-02/OQ-01 and is a required input to the post-verification pass, not optional polish |

## Final-prep placeholders

These are owned by the print engineer's post-verification pass (`final_print_prep.md`),
once `verification_report.md` exists — out of scope for this pre-design commission, noted
here only as the plan's forward intent:

- **Slicer profile:** Bambu Studio, TPU 95A preset as a base, main-nozzle-only, 0.16 mm
  layer, Cool Mode; final wall/top-bottom/infill counts confirmed against the accepted
  candidate's actual measured wall thickness (G-05).
- **Order:** PLA geometry coupon → TPU fit-and-thickness coupon (closes G-02/OQ-01) →
  full case in TPU only once both coupon lanes pass.
- **Inspection:** dimensional recheck of G-01/G-03/G-06 bands and G-04 chamfer on the
  finished part; visual audit of G-07/G-08/G-09 printed faces against the planned
  disposition (no unplanned support scarring).
- **Field test:** phone insertion/removal without tool assistance, no rattle at rest, one
  supervised drop test from pocket height onto a hard floor observing case + phone for
  cracking or separation, and reporting pass/fail plus any stopping point if insertion
  binds.

## Plan acceptance

- **Blocking items:** none. G-02 (thickness/OQ-01) and G-08 (button-window span choice)
  are deferred with named owners and final gates above, not blockers to candidate CAD.
- **Accepted by print engineer:** print-plan-1

## Open questions carried forward (not silently resolved)

- **OQ-01 (thickness):** see G-02. Plan proceeds on the reference's frozen 8.7 mm nominal
  and relies on TPU's compliance plus a mandatory coupon confirmation — not a redesign of
  the reference and not a widened clearance floor.
- **OQ-08 (screen-side lip, F-013, grade D):** `dimensions.md` explicitly leaves whether
  the case should add its own front-face lip as a "designer decision, not specified here."
  This print plan does not resolve it (it is a geometry question, out of this commission's
  scope) — flagged so the candidate designer and verifier see it, not silently dropped.
- **OQ-04 (button/port position uncertainty, C-grade):** carried through unchanged via the
  full-range LOOSE bands in G-08/G-09 above; no tightening attempted here.
