# Metrologist reference-overlay acceptance — meta-2

## Verdict

**REVISE_SHEET.** The reference cannot be accepted from `dimensions.md` r1.  The defect is
an upstream-dimensions omission, not a geometry repair request: r1 identifies three cameras
and a flash but contains no per-aperture positions or diameters.  A blind implementer therefore
had no contract basis for the observed camera-proxy positions.

## Inputs and integrity

| Artifact | SHA-256 | Use |
|---|---|---|
| `pixel10_reference_r1.stl` | `d53245f5d18951a9e6988a338e321c86669e703501bf6bd35248c6f6c9797d77` | evaluated blind reference export |
| `pixel10_reference_r1.step` | `6c8269ca172464b62876fdaf9e3d559ded0b17420d615fe0977e6875d074cd5b` | manifest-correlated export |
| `reference_v-rear.png` | `6134a48d45adc827b182efe1060b081b9dca4e18f242651e24dacbc48534c123` | visual rear inspection |
| `reference_v-front-right.png` | `3cc278e98f934264c7adada19afce477e9af7ea4f03721b6ff10f89ce12b39b4` | visual right-side inspection |
| `reference_v-bottom.png` | `97aaa00237f4c514ed5fe18d828e3bfd5eb5644c2d15cab30065367ed01fb70a` | visual bottom inspection |
| `reference_v-top.png` | `96c695a26725d4697e0a868f2b26bf94d35d0a39f79957ac7c961ba81d65edef` | visual top inspection |
| `../../evidence/input/pixel10_official_hardware_diagram.png` | `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0` | official uncalibrated diagram |

The manifest identifies commission `ref-1`, source `reference.py` SHA-256
`4cd577eb00f05cca2f4f81809af20f2642695654065ef921b6f3242db9a42f49`, and declares
`dimensions.md r1` as its only dimensional input.

## Overlay method and observed evidence

- `diagram_rear_device_crop_r1.png` is a lossless crop of the rear handset drawing from
  the immutable official diagram; it removes the unrelated front handset from the overlay
  segmentation field but retains the official callout strokes.
- The shared `experiments/overlay_photo.py` was run on the blind STL and this crop with
  mesh-re-zeroed Z slices 8.7, 9.5, and 10.5 mm.  Those planes traverse the raised
  camera feature (the body is at re-zeroed Z 0.0–8.6 mm).  Environment: `PYOPENGL_PLATFORM=win32`,
  `PYTHONPATH=skills/3d-modeling/scripts`.
- `overlay_camera_r1.png` SHA-256
  `16970924d2a7ac289b514723cd8df25ef680c450af40f009d2566c5ac361bfa0`:
  red camera-island boundary follows the official island envelope; emitted residual is
  mean 0.55 mm, p90 1.52 mm.  This metric is only a trend; visual review decides.
- Visual review of that overlay: all three camera proxies and the flash proxy are present,
  with flash on the +X/right side.  The first and third camera proxy circles do not hug
  the official lens centres; the mismatch is several millimetres at diagram scale.  The
  centred overall island alone is therefore insufficient acceptance evidence.
- `overlay_rear_r1.png` came from a whole-diagram trial.  The supplied tool segmented both
  labelled phone drawings as one body, yielding a 5.80 mm mean / 8.54 mm p90 residual.
  It is retained for reproducibility but explicitly excluded from the verdict.

## Feature-by-feature review

| Feature IDs | Visual result | Gate result |
|---|---|---|
| F-001/F-002 | Rear render shows the expected rounded body; exported bbox supports M-001–M-003 after separating raised/proxy extents. | pass |
| F-003 | Camera-island silhouette/top placement agrees with r1's C-grade envelope. | pass |
| F-004/F-005 | Correct count/handedness, but individual camera locations are not specified in r1 and do not align visually. | **fail: upstream dimensions** |
| F-006/F-007 | Right-side render supports only the continuous control-envelope proxy approved in A-03, not tight cover geometry. | conditional |
| F-008/F-009/F-010 | Bottom render shows a three-region proxy consistent with the diagram order. | conditional |
| F-013 | Top render shows a single proxy; r1 intentionally has no precise location. | conditional |

## Required r2 corrective measurement commission

Before a fresh blind reference build, add C-grade IDs for each of the three camera aperture
centres and outer diameters, and the flash centre/diameter, all referenced to D1_XMID and
D4_TOP.  Derive them from the calibrated rear diagram scale, carry uncertainty explicitly,
and retain the existing conservative camera-window response/coupon.  Do not treat the current
blind reference's proxy locations as measurement evidence.
