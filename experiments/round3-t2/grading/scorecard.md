# Round 3 T2 independent scorecard

Grading was performed after both frozen arms reported delivery. I re-imported each final STL with trimesh and each STEP with CadQuery/OCCT, then re-imported the STEP tessellation. Both intended tool bodies and both coupons are one-component watertight meshes. The reproducible record is `measure_round3.py` and `mesh_measurements.json`.

## Functional gate

| Arm | Tool STL / STEP / coupon | Historical raw T2 result | Controlled installed-frame T2 result | Gate |
|---|---|---|---|---|
| Monolith | watertight / valid + watertight tessellation / watertight | Fails 0/3 criticals only in its documented printer coordinate frame | width 12.4 mm; depth 24.7 mm; length 62.7 mm; 3/3 criticals pass | PASS |
| Team v3 | watertight / valid + watertight tessellation / watertight | width 14.2 mm; depth 24.7 mm; length 63.7 mm; 3/3 criticals pass | Same 3/3 critical pass | PASS |

The historical `scorer.py` assumes a Z-up installed orientation. The monolith intentionally exports a rotated print frame (`(x,y,z) -> (58-z,y,x)` on inverse), so raw scoring cannot see its slot. I preserved that raw failure in `mesh_measurements.json`, then applied the unchanged historical scorer to a temporary re-export in the common installed fixture frame. This is a coordinate correction, not a substituted geometric test. Team v3 was already in that frame. Its direct geometric score is at the acceptance boundary on slot width (14.2 mm); its own documented cavity is 62.6 x 12.3 x 24.35 mm, while the scorer’s free-region predicate reports 14.2 x 24.7 x 63.7.

Each coupon was also freshly re-imported, watertight, and one component. This validates delivered coupon geometry, not the required physical real-bar print test; neither arm records a completed physical coupon result.

## Visual inspection and manufacturing observations

I opened the common SVG and all four required renders from each arm. The SVG shows a centred long rectangular 62.0 x 11.7 mm bar across a Ø63 cap, rising 24.0 mm above the protected cap face; engagement lowers along the displayed axis and torque is about the cap centre.

Monolith’s exterior render shows a very large rounded rectangular paddle. Its installed and section views do show a full-length bottom-open socket around the bar, but the translucent, heavily triangulated rendering makes the fit boundaries difficult to inspect and the 116 mm installed-frame length appears materially bulkier than the fixture. Its print view clearly shows the broad rectangular bed face; the process relies on a 24.5 mm bridge, near its stated 25 mm guidance.

Team v3’s exterior render shows an 84 mm-wide rectangular body with a raised circular hand grip and rounded outer edges. Its installed view shows the bar inside the central channel, and its section shows the lateral opening/roof architecture. These renders are also translucent and visually busy, but the distinct grip is more immediately hand-tool-like. Its print view shows the declared flat P_BED side, and its evidence reports no bridge or non-bed support-required downface.

## 100-point rubric

| Category | Monolith | Team v3 | Basis |
|---|---:|---:|---|
| Watertight/export/function hard gate (35) | 35 | 35 | Tool and STEP import integrity plus all three controlled T2 critical checks pass. |
| Hidden functional fit (20) | 20 | 20 | Both pass the frozen scorer’s installed-frame width, depth, and engagement checks. |
| Visual fidelity and usefulness (15) | 8 | 11 | Both engage the correct centred cross-bar; team has a more recognizable ergonomic grip, while both render sets obscure some geometry. |
| DFM/process (15) | 11 | 14 | Both deliver fit-derived coupons and PETG-oriented instructions. Monolith’s 24.5 mm bridge and unusually massive body add risk; team has a documented support-free P_BED orientation but still awaits its physical PETG coupon gate. |
| Evidence and maintainability (15) | 12 | 13 | Monolith is compact and reproducible but its current STEP SHA-256 differs from its ledger. Team has unusually complete contracts and validation receipts but retained three rejected loops and a large evidence footprint. |
| **Total** | **86** | **93** | Hard-gate cap does not apply. |

## Ledger and adoption audit

| Threshold | Monolith | Team v3 | Result for v3 |
|---|---:|---:|---|
| Hard functional/export gate | pass | pass | pass |
| Score at least 85 and not below monolith | 86 | 93 | pass |
| Visual + DFM at least 22/30 and no worse than monolith by more than 2 | 19 | 25 | pass |
| Critical path at most 30 min and 2x monolith | 6m 00s | 74m 18s from first design receipt to delivery | fail |
| Specialist commissions at most 8 | 1 context | 13 | fail |
| Fresh verifier rule | n/a solo arm | 4 fresh verifier contexts, 3 correction loops | fail |
| Delivered files at most 35 / bytes at most 1,000,000 | 12 / 451,351 | 61 / 3,660,471 | fail |
| Readiness and fresh verifier measure final export; hidden confirmation | final verifier present | present; hidden scorer confirms | pass |
| Five role gates, actual visual inspection, real coupon artifact | n/a solo path | present | pass; physical coupon still pending |

Token telemetry is `not exposed` for both arms; no token estimate was made. The monolith ledger claims final STEP hash `b9354aa...145a`, but the frozen file hashes to `60dd4c...042a`; its STL and coupon hashes match the ledger. Team’s logged total is 61 files / 3,658,970 bytes; a fresh recursive count excluding `__pycache__` is 61 files / 3,660,471 bytes, a 1,501-byte discrepancy that does not affect the threshold failure.

## Decision

Team v3 meets the functional and quality score requirements but fails multiple non-waivable adoption thresholds: critical-path time, commissions, verifier/correction count, and artifact count/bytes. The preregistration says this is not the single-proxy-within-10% repeat case. **Do not adopt v3 unchanged; refine the workflow rather than weaken the gate.**
