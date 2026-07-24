# Washer filter-cap cross-bar tool

Final material: PETG. The one-piece rounded paddle uses a smooth, full-length socket rather than teeth, so normal hand torque is spread along the 62.0 mm raised bar. The only fit-driving values are at the top of `model.py`: adjust `CLEARANCE_SIDE` for lateral fit and `CLEARANCE_TOP` for cap-face/top clearance.

Print `filter_cap_tool.stl` on its 46 x 55 mm end face, exactly as exported. This is a 46 x 55 x 116 mm native print envelope. It needs no supports: the socket ceiling is a single designed 24.5 mm bridge (within the machine's 25 mm bridge guidance). Use the 0.4 mm nozzle, 0.20 mm layers, 4 walls, 5 top/bottom layers, 30% gyroid, and place the seam on an outside rounded end. Dry PETG first; run the X2D flow/nozzle-offset calibration.

First print `bar_engagement_coupon.stl` in PLA. It is generated with the same `SLOT_LENGTH`, `SLOT_WIDTH`, and `SLOT_DEPTH` as the final tool, not a substitute geometry. Test that it lowers over the bar without force and rocks neither on the bar nor on the cap face. If it is tight, increase `CLEARANCE_SIDE` by 0.10 mm and regenerate both artifacts; if the top touches, increase `CLEARANCE_TOP` by 0.10 mm.

The exported-STL evidence in `verification.json` records 62.70 mm slot length, 12.40 mm slot width, 24.50 mm depth, 62.0 mm engagement length, zero seated/swept bar intersection, watertight meshes, and the planned-orientation bridge area. The bar/cap dimensions came only from the participant-visible fixture schematic. A physical coupon remains necessary because the fixture measurement is approximate and printer shrinkage can vary.
