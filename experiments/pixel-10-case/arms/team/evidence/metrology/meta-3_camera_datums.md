# Meta-3 corrective camera/flash datum evidence

## Purpose and source lock

This record corrects the r1/r2 omission identified in the meta-2 round trip.  It uses only
the immutable official diagram `../../evidence/input/pixel10_official_hardware_diagram.png`
(SHA-256 `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0`), scaled from the
official M-001/M-002 overall dimensions.  No rejected blind-reference artifact, render,
export, or proxy feature was used to determine a datum.

## Pixel measurement method

The near-orthographic rear handset drawing was inspected at original resolution.  Approximate
outer-body image bounds were left/right = 1385/1801 px and top/bottom = 307/1194 px, giving
independent diagram scales of 5.778 px/mm across the 72.0 mm official width and 5.805 px/mm
along the 152.8 mm official height.  The datum origin is the body centreline at X = 1593 px and
the top edge D4_TOP at Y = 307 px.  Camera/flash centres were read from visible circular
aperture centres.  A common 5.79 px/mm conversion is reported below, while the contract keeps
±2.0 mm centre uncertainty to cover rendered-edge selection, annotation overlap, and the
explicitly uncalibrated nature of the hardware diagram.

| Contract feature | Diagram centre (px) | Diameter (px) | Scaled centre from D1_XMID / below D4_TOP (mm) | Scaled outer diameter (mm) | Contract IDs |
|---|---:|---:|---:|---:|---|
| F-004-A, left camera | (1467, 452) | 26 | X = -21.8; Y = 25.0 | 4.5 | M-019, M-020 |
| F-004-B, centre camera | (1576, 452) | 26 | X = -2.9; Y = 25.0 | 4.5 | M-021, M-022 |
| F-004-C, right camera | (1647, 452) | 26 | X = +9.4; Y = 25.0 | 4.5 | M-023, M-024 |
| F-005, flash | (1729, 452) | 35 | X = +23.5; Y = 25.0 | 6.0 | M-025, M-026 |

## Confidence and required response

All eight values are C-grade image-derived datums, not manufacturing measurements.  They are
adequate to make a blind reference testable for count, handedness, and relative layout only.
The reference uses the stated nominal values; the candidate still uses the existing conservative
shared camera opening, all bounds in A-02 remain unchanged, and final TPU fit remains subject
to real-device/coupon confirmation.  A fresh ref-2 must be built from `dimensions.md` r3 and
reviewed against IMG-01 before `ACCEPTED` can be recorded.
