# Common benchmark brief: protective case for Google Pixel 10

## Commission

Design a slim but protective, one-piece case for the **base Google Pixel 10** (not Pixel 10
Pro, Pro XL, Fold, or Pixel 10a). Use **CadQuery only**; FreeCAD is in use by another
session and must not be opened, queried, or changed.

The case is intended for TPU 95A on the Bambu Lab X2D Combo using the 0.4 mm main nozzle. It
must be realistically printable and installable, not merely a phone-sized box.

## Fixed product facts

- Overall phone body: **152.8 mm high × 72.0 mm wide × 8.6 mm deep**.
- Variant: base Pixel 10.
- Official feature diagram identifies a top microphone and speaker; right-side power and
  volume controls; rear wide, ultrawide, and 5× telephoto cameras plus flash; NFC and
  Pixelsnap magnets; bottom speaker, USB-C, and microphone.
- The supplied official hardware diagram is evidence of feature identity and approximate
  relative position, not a calibrated manufacturing drawing.

Every further number must identify its source and confidence. Public web research is
allowed and expected. Existing phone/reference models may be researched as dimensional
evidence, but do not copy or submit an existing finished case.

## Functional requirements

1. Capture the phone with credible TPU clearances and an install/removal strategy.
2. Protect all four corners and edges; include a screen lip and a camera lip.
3. Do not cover the rear camera/flash field, power/volume operation, USB-C plug envelope,
   bottom speaker/microphone, or top microphone/speaker.
4. Keep the back compatible with ordinary Pixelsnap/Qi2 charging. No embedded magnets are
   required; avoid an unnecessarily thick charging gap.
5. Avoid razor edges, non-manifold details, trapped support, decorative text, and fake
   microfeatures unsupported by evidence.
6. Design for the stated TPU/nozzle/process, including wall thickness, overhangs,
   bed-facing edges, layer/load direction, and a fit-test coupon.

## Required deliverables

- Parametric `model.py` with a centralized parameter block.
- Independent-useful `verify.py`.
- Final case STL and combined STEP.
- At least four renders: exterior/isometric, phone/case fit or transparent fit, section,
  and planned print orientation.
- `print_notes.md` with dimensions/clearances, material, orientation, slicer guidance,
  risks, and fit-coupon plan.
- Any workflow contracts required by the assigned skill.

All acceptance claims must be based on the exported STL re-imported. Record unresolved
assumptions honestly.
