# V3 fresh verifier evidence

All numerical geometry results below were obtained from a new `trimesh` re-import of
`pixel10_case.stl` (`255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960`).
No candidate source geometry was used for checks 1--7. `candidate_readiness.md` was
treated as untrusted completeness evidence only.

| Item | Independent result |
|---|---|
| Export integrity | One watertight component; Euler 2; bounds `[-2.100000,-1.545817,-1.300000]..[74.099998,154.899994,9.700000]` mm; mesh volume `15856.857053 mm3`. STL, STEP, and reference SHA-256 values are respectively `255945…5960`, `5aed8568…d536`, and `81aafa0f…7a48`. |
| Check 1 | Re-imported manifold boolean against re-imported reference: seated intersection `0.000000000 mm3`. |
| Check 2 | Re-imported manifold booleans at every 1 mm insertion position from `+Z=0` through `+Z=16`: maximum forbidden intersection `0.000000000 mm3`. |
| Check 3 | Re-imported mid-Y=76.4 section: 234 vertices, X `-2.100000..74.099998`, Z `-1.300000..9.700000` mm. Inspected `render_section.png`: rear wall, rear clearance, open front, and screen lip/root agree with the stated architecture. |
| Check 4 | Inspected `render_exterior.png`, `render_fit.png`, `render_section.png`, `render_print_orientation.png`, and `reference_rear_overlay.png`. The exterior image includes a cyan case/amber F14 S2 same-view overlay, correctly marked relative-layout-only. The strongly flattened iso views can obscure print-face problems; they were not substituted for check 7. |
| Check 5 | Re-imported boolean material in each inner response zone: F14 `0.000000000`, F21 `0.000000000`, F05/F06 `0.000000000`, F07/F08 `0.000000000 mm3`. Zones occur at rear/bottom/top/right and are not mirrored. |
| Check 6 | At X=36, the re-imported F23 cross-section has a quarter-arc centered at `(Y=106.600, Z=-0.900)` mm: 43 sampled points give radius `0.399717..0.400004` mm. This meets G04 `0.38..0.42` mm. Mid-Y section and bounds agree with the D01--D10 conservative-envelope dimensions; unmeasured physical-device questions remain open. |
| Check 7: exact transform | Exact plan transform about L `(-1.746446609,76.4,-0.946446609)` with `R_y(-45°)` gives printer-Z `-0.000000047..60.828264578` mm and 16 vertices within 0.05 mm of bed. |
| Check 7: outside F23 | With the plan's non-contact threshold (`printer Z>0.30`) and downward normal threshold (`n_z < -sqrt(0.5)`), total down-facing area is `27.541083 mm2`; F23-classified portion `23.132460 mm2`; **outside-F23 unsupported area `4.408623 mm2`**. This violates G05's required `0.0000 mm2`. |
| Check 7: F23 layers | Sliced the transformed re-import at 0.16 mm printer-Z intervals throughout F23. Each F23 slice point was compared in the lateral slice plane with the prior layer's resampled material contours (0.02 mm segments). 306 F23 layers were present. Four successive contour checks exceed the 0.35 mm maximum: `32.16<-32.00: 43.587353`, `50.40<-50.24: 0.405512`, `50.56<-50.40: 0.588098`, `50.72<-50.56: 14.581540` mm. The required maximum is `sqrt(2*0.42*0.16-0.16^2)=0.3298 mm`, with the plan's acceptance cap `<=0.3500 mm`; therefore G05 fails independently of the outside-F23 area. |

Visual-inspection conclusion: the new rounded F23 edge resolves the prior G04 defect, and
the section/overlay evidence supports checks 3--4. The supplied tilted iso render is
visually insufficient to demonstrate the no-support claim; the exact transformed,
re-imported mesh predicate is determinative and rejects this export.
