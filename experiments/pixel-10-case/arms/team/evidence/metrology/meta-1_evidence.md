# Meta-1 metrology evidence log

## Scope and preservation

- `IMG-01` is the immutable common input `../../evidence/input/pixel10_official_hardware_diagram.png`.
- SHA-256 recorded by the common evidence register: `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0`.
- It was inspected at original resolution on 2026-07-24.  This is a labelled official
  hardware diagram, not a calibrated manufacturing drawing.  It is used only for feature
  identity, handedness, and proportional/approximate location.

## Visual annotation register

| Annotation ID | Source region / callout | Visible feature and interpretation | Contract feature |
|---|---|---|---|
| ANN-01 | Rear, callout 12 | Rounded horizontal camera island, centred horizontally and close to the top edge | F-003 |
| ANN-02 | Rear, callouts 7–11 | Three distinct camera apertures and one flash within F-003; do not collapse this into a two-camera Pixel 9 layout | F-004, F-005 |
| ANN-03 | Rear, bottom callouts 13–15 | Bottom edge contains speaker, centred USB-C, and microphone; exact aperture sizes are not supplied | F-008, F-009, F-010 |
| ANN-04 | Front/right silhouette, callouts 4–5 | Power and volume controls are on the handset's right side when viewed from the front | F-006, F-007 |
| ANN-05 | Front top, callouts 1–3 | Top speaker and front camera exist; neither is part of the rear mating envelope, but the front lip must not intrude on their functional field | F-011, F-012 |
| ANN-06 | Diagram top / official feature list | Top microphone is required to remain clear | F-013 |

## Research record

| Source ID | Method | Result | Metrology treatment |
|---|---|---|---|
| WEB-01 | Google Pixel hardware technical specifications, searched 2026-07-24 | Official Pixel 10 entry reports 152.8 × 72.0 × 8.6 mm (H × W × D) | B confidence for M-001–M-003 |
| WEB-02 | Google official hardware diagram linked by the common evidence README | Confirms base-Pixel-10 triple rear cameras, flash, right-side controls, top/bottom audio and USB-C locations | B identity / C scaled layout only |
| WEB-03 | Printables lead in common evidence README, searched 2026-07-24 | Community 3D-model page was not fetchable in this runtime; no numeric value adopted | No geometry copied; no dimensions adopted |
| WEB-04 | MakerWorld lead in common evidence README, searched 2026-07-24 | Community case page was paywalled in this runtime; no numeric value adopted | No geometry copied; no dimensions adopted |

## Scaling and tolerance policy

The rear diagram is a rendered/diagrammatic view rather than a surveyed orthographic drawing.
The camera-island dimensions below are scaled from its silhouette using the official body
height as a reference, then deliberately widened to the stated uncertainty.  They are C-grade
envelope inputs, not manufacturing dimensions.  A candidate may not use them for a tight camera
lip; it must leave the stated clearance envelope and the print engineer must require a coupon or
real-device check before final TPU production.
