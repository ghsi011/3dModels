# V5 fresh verifier evidence

The verifier independently re-imported `pixel10_case.stl`; `model.py` was not used to
establish any candidate geometry result. `verify_v5_reimport.py` constructs only the
D01--D04 reference from the accepted dimensions and evaluates the exported mesh.

| Item | Fresh result |
|---|---|
| Candidate identity | STL `255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960`; STEP `e178a4d87b85988b3457e5c25f3e44c03c7016c5e9c20d551dd3fcdaeac88689` |
| Export integrity | One watertight, winding-consistent component; bounds `[-2.100000,-1.545817,-1.300000]..[74.099998,154.899994,9.700000]` mm; volume `15856.857053 mm3` |
| Check 1 | Seated forbidden intersection with independent D01--D04 rounded reference: `0.000000000 mm3` |
| Check 2 | Seventeen re-imported sweep positions through model `+Z=0..16`: maximum forbidden intersection `0.000000000 mm3` |
| Check 3 | Re-imported `Y=76.4` section: one loop, 235 vertices. `render_section.png` shows rear wall, clearance, open front and lip architecture. |
| Check 4 | Inspected all four supplied renders and `reference_rear_overlay.png`. `render_exterior.png` labels S2 as relative-layout-only; it does not claim calibrated camera coordinates. The tilted iso views are visually foreshortened, so no support-contact conclusion was drawn from them. |
| Check 5 | Re-imported forbidden material was `0.000000000 mm3` in the conservative F14 centre, F21 centre, F05/F06 top slot, and F07/F08 front-side control zone. The supplied overlay retains rear/right/top/bottom handedness. |
| Check 6 | A fresh re-imported `Y=120` F23 section fitted 44 mesh points to radius `0.400008 mm`, within G04 `0.380000..0.420000 mm`. The section/render retain the 1.30 mm rear wall, 0.30 mm rear clearance, 1.80 mm rails, and 1.10 mm lip claim. Q01--Q05 remain physical-device/coupon gates. |
| Check 7 | Exact rev4 transform produced printer Z `-0.000000034..60.828264592 mm`; 16 vertices lie within 0.05 mm of the bed. The known part-only G05 facts remain `4.408623 mm2` and four F23 transitions `0.405512..43.587353 mm`; they are not relabelled self-supporting. The rev4 V scope was applied: the only support-eligible class is the unexposed exterior/nonfunctional underside, while cavity/capture lip, all functional openings, the visible exterior opposite L, and the exposed G04 radius are excluded. No support contact, slicer, or toolpath claim was made. |

Rev4 assigns native slicer project, support coverage/contact selection, F23 toolpath section,
and layer-map evidence to P2 after this candidate PASS. Their absence is not a V5 rejection
condition; it remains a mandatory final-print gate and must receive a fresh P2-artifact review.
