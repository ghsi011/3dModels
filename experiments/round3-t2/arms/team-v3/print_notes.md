# cq-a print notes — P2 ownership transfer

## Frozen production setup

Print the coupon first, then the final `cq-a-washer-filter-tool.stl` only after the physical coupon gate passes.  Use dry PETG on the X2D main 0.4 mm nozzle, single-nozzle mode, textured PEI, Bambu Studio's X2D Generic PETG profile, 0.20 mm layers, 0.42 mm line width, four perimeters, five top/bottom layers, and 35% gyroid infill.  Dry the PETG in AMS 2 Pro at up to 65 C before the job; it does not dry while printing.  Run the X2D nozzle-offset and flow calibration with that dry spool.  Brim is OFF.

Place both files using the frozen transform: right-handed `Rx(+90.0 deg)` about `D0`, then translate only in printer Z until `P_BED` (the native `Y=-8.000 mm` nonfunctional side land) is at printer `Z=0.000 mm`.  `+DY` is printer `+Z`, `+DZ` is printer `-Y`, and the installed mouth remains lateral, opening along printer `-Y`.  Use seam placement restricted to `P_BED` or the nonfunctional outer base rail.  Never place a seam on a bar-bearing face, mouth/lead-in, grip rim, or cap-protection boundary.

Supports are OFF: generated support must be `0.000 mm3`, support interface layers `0`, and support-contact faces `0`.  No native 3MF is required because verification r4 passed SS-01 through SS-04 with zero out-of-limit regions, zero bridge span, and `P_BED` as the sole bed-facing region.  No other face may be reoriented to the plate.

## Production geometry and coupon gate

The source parameters remain `FIT_CLEAR_XY=0.300 mm` per side, `FIT_CLEAR_Z_TOP=0.350 mm`, `CAP_CLEARANCE=0.600 mm`, `CAVITY_X=62.60 mm`, `CAVITY_Y=12.30 mm`, and `CAVITY_Z=24.35 mm`.  `coupon.py` cuts its engagement core directly from `model.make_tool()` and preserves the full nominal 62.00 mm span, actual 62.60 mm production cavity span, the 24.00 mm bar engagement depth, production mouth lead-in, 0.90 mm contact radius, and 2.40 mm end walls.  Its PETG STL is `cq-a-real-bar-engagement-coupon.stl`, SHA-256 `2a08ab48731ad4e1a305cf06d4d45d736c0f1c22fd2f8519a58ed1a7805b0f84`.

After printing the coupon in the frozen setup, insert it over the real bar along `-DZ` through the full available travel to its seating datum.  Pass requires hand-force insertion, at least +10 deg and -10 deg rotation about `DZ` without lift-off, cracking, permanent whitening, gouging, or contact with the cap plane outside `F02`; measured cap-plane clearance must remain at least 0.50 mm.  Record cavity and, when safely measurable, bar dimensions; seating depth; cap clearance; and a photo after each direction.  A failure stops the final print: preserve the coupon, photos, slicer profile, and measurements, then route fit/clearance or slicing failure to `PRINT_PLAN` and geometry/contact failure to `CANDIDATE_BUILD`.

## Final tool inspection and field test

After a passing coupon, print the final tool in the identical setup.  Before installation, verify the final file hash is `39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df`; inspect `P_BED` for elephant foot, the mouth/lead-in and end stops for seam/stringing, the roof/end-stop junction for layer separation, and every grip rim for sharpness.  Reject visible cracking, whitening, voids at the contact geometry, warped `P_BED`, any support material, or a measured cavity/cap clearance outside the coupon-pass conditions.

For field use, seat the tool without force, turn gently in each direction while watching for lift-off and cap contact, and stop immediately on slipping, binding, visible cap marking, crackling, or deformation.  Torque and duty are unspecified, so do not use tools, impact force, or leverage extensions and do not claim a torque rating.  Preserve photos, machine profile, filament condition, coupon/final measurements, and failed parts; revert to the relevant `PRINT_PLAN` or `CANDIDATE_BUILD` gate instead of reprinting unchanged.
