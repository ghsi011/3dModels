# Pixel 10 TPU 95A case — print notes

## Geometry and fit

`model.py` is the parametric source. Its coordinate system is X = width, Y = height, and Z = rear-to-screen. The protected body envelope is 72.0 × 152.8 × 8.6 mm, sourced from Google's official Pixel specifications (high confidence). The exported case measures 76.2 × 157.0 × 11.25 mm.

- Side/end clearance: 0.30 mm per side for compliant TPU installation.
- Back: 1.60 mm; side wall: 1.80 mm; screen lip: 1.05 mm above the nominal phone body.
- The broad rear camera aperture is 64 × 24 mm, centred 50 mm above the phone centreline. Those camera-bar dimensions and all individual access-opening locations are low-confidence proportions from the official hardware diagram, which is explicitly not a calibrated manufacturing drawing. The aperture is intentionally generous so an uncertain camera projection cannot bind.
- The back is a thin, uninterrupted non-magnetic TPU plate outside the camera opening; it keeps a small charging gap compatible with ordinary Pixelsnap/Qi2 use.
- The right side has a broad power/volume access relief. Bottom relief clears USB-C, speaker, and microphone. Top relief clears the top microphone/speaker region.

No finished third-party case was copied. Research sources considered: [Google hardware specifications](https://support.google.com/pixelphone/answer/7158570?hl=en-GB), [Google Pixel 10 hardware diagram](https://support.google.com/pixelphone/answer/7157629?hl=en#Pixel10), and the benchmark-listed Printables/MakerWorld leads. Only the frozen official 72.0/152.8/8.6 mm dimensions were treated as high confidence.

## Orientation and slicer setup

Place the rear face flat on the textured PEI plate, open screen side upward. This gives a stable large contact face, keeps the exterior back clean, and needs no supports; the exported-STL face audit found 0.0 mm² of unsupported downward-facing area above the bed chamfer threshold.

Use TPU 95A from a dry external spool on the X2D main 0.4 mm nozzle. Start at 0.20 mm layers, 0.42–0.45 mm line width, four walls, five bottom layers, and 15–20% gyroid infill. Use 40–60 mm/s, modest cooling, seam on the left/rear edge, and a 3–5 mm brim only if the first-layer preview shows corner lift. Do not use the auxiliary nozzle or AMS for TPU. No support is planned.

## Fit-test coupon and risks

Before the full TPU part, print a short PLA coupon sliced from the right-side wall plus the bottom USB-C opening. Include three clearance variants: 0.20, 0.30, and 0.40 mm per side. Confirm insertion force, button reach, cable plug clearance, and that the camera bar sits below the surrounding rear bezel before printing the full case in TPU.

Unresolved risk: Google’s supplied feature diagram is not a calibrated feature drawing, so exact camera-bar projection, individual button centres, and port widths remain low confidence. The case deliberately uses broad access relief, but the coupon and a physical visual check are mandatory before final production. TPU shrink/flow and a screen protector can also require a one-line adjustment to `SIDE_CLEAR`, `END_CLEAR`, or `SCREEN_LIP`.

## Verification evidence

`verify.py` re-imports `pixel10_case.stl`, `phone_reference.stl`, and `case_section.stl`; it does not make acceptance claims from the in-memory CAD solid. The final report records watertightness, exported-STL dimensions, seated interference, a 45/30/15/5/0 mm insertion sweep, a watertight section, feature/datum evidence, the measurement audit, and the printability face audit. The independent STEP re-import contained one valid solid.
