# Metrologist reference-overlay acceptance — meta-4 / ref-2

## Verdict

**ACCEPTED** for `dimensions.md` r3 as a bounded blind mating-reference contract.  The
acceptance does not upgrade any diagram-derived dimensions beyond C confidence and does not
replace the final-device/coupon requirements in A-02, A-04, A-05, or A-07.

## Inputs and integrity

| Artifact | SHA-256 | Use |
|---|---|---|
| `pixel10_reference_ref2.stl` | `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91` | evaluated blind export |
| `pixel10_reference_ref2.step` | `6a5e8ae693dc3ce3906b9067e20102c9e6e3311200b4b5706a01dec1da10aa25` | correlated export |
| `v-rear.png` | `515fbfdb00d1c8121250e5eec5c43b6c197df3e4be2c07860d31066c33c342bd` | required rear view |
| `v-front-right.png` | `e4772e9feb16693096288fd117ee45c2c304f7e86efec2b2db4950a1e106201e` | required right-control view |
| `v-bottom.png` | `0326ffe1abbb7312102700bd70511658f94c407a3b2322d58489910fa525691b` | required bottom proxy view |
| `v-top.png` | `5f19c0bb6ff99ad50923b15db3f8fb0fd04b118a3a975a12eb5a80c9b3eb8fe6` | required top proxy view |
| `reference_ref2_technical.png` | `0eacce927a8461a8e072efc0536a1dd6e662681171002de02eb9ac76a697ccfc` | multi-view visual cross-check |
| `../../../../../evidence/input/pixel10_official_hardware_diagram.png` | `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0` | frozen official diagram |

`MANIFEST.md` binds these artifacts to commission `ref-2` and `dimensions.md` r3 only.

## Overlay method

- `diagram_rear_device_crop_ref2.png` is a lossless rear-device crop from IMG-01, created
  solely to exclude the unrelated front-handset drawing from the shared tool's segmentation.
- The shared `experiments/overlay_photo.py` was run against the ref-2 STL and the crop at
  mesh-re-zeroed Z = 8.7, 9.5, and 10.5 mm, the camera-feature planes above the 8.6 mm body.
  Environment: `PYOPENGL_PLATFORM=win32`, `PYTHONPATH=skills/3d-modeling/scripts`.
- `overlay_camera_ref2.png` SHA-256
  `cb5a9bd8051789683ea6cfbb32baf00e1e66315014036726f19631d52788af32`
  reports a 0.58 mm mean and 1.18 mm p90 nearest-edge trend residual.  Visual comparison,
  rather than the residual, determines the verdict.

## Inspection record

| Feature IDs | Observation | Result |
|---|---|---|
| F-001/F-002 | V-REAR and technical sheet show the rounded handset body; exported extent 73.0 × 152.8 × 10.6 mm includes the bounded raised/proxy features. | pass |
| F-003 | Red island boundary hugs the official island silhouette in `overlay_camera_ref2.png`. | pass |
| F-004 | Red aperture circles visually land on A/B/C in the frozen diagram within the explicit ±2.0 mm centre and ±1.5 mm diameter C-grade bounds. | pass |
| F-005 | Flash circle is correctly at the +X/right end.  Mirroring would move it to the left and clearly fail the diagram. | pass, handedness confirmed |
| F-006/F-007 | Required front-right and technical right views show only the authorised continuous control proxy; no individual-button claim is accepted. | pass, bounded |
| F-008/F-009/F-010 | Bottom view is consistent with the intentionally broad bottom fixture relationship; exact slots remain outside r3's evidence. | pass, bounded |
| F-013 | Top view is consistent with the centred broad microphone proxy; exact location remains open under A-05. | pass, bounded |

## Downstream constraint

The accepted fixture may be used for print-plan and candidate work only with the unchanged
bounded-response rules: a shared oversize camera opening, continuous/open right control relief,
broad bottom opening, and real-device/coupon confirmation before final TPU production.
