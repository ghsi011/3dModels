# Blind reference build — D1 receipt

## Scope and bound inputs

This D1 commission owns only `reference_model.py`, `reference_phone.stl`, and the single
rear matching-view evidence image `reference_rear_overlay.png`.

| Input | Use |
|---|---|
| `dimensions.md` rev. 1 | Sole source of model dimensions: D01--D05, frame O/A/B/C/D. |
| `../../../benchmark_brief.md` | Identifies the base Pixel 10 and CadQuery-only commission. |
| `../../../evidence/input/pixel10_official_hardware_diagram.png` | Identity and relative-layout comparison only; SHA-256 is asserted by the source. |

## Geometry and assumptions

`reference_phone.stl` is the nominal rounded body: X=0..72.0, Y=0..152.8,
Z=0..8.6 mm, with the D04 blind reference radius of 12.0 mm. It intentionally contains
no inferred buttons, port bores, lens circles, camera protrusion, or glass recess.
Those coordinates/heights are open Q01--Q05 items, not measurements.

`reference_rear_overlay.png` is the one decisive same-view rear comparison. Red is the
body silhouette; amber is only the contract's D05/F14 conservative shared rear-field
envelope. The supplied diagram is non-calibrated: its pixels normalize the visual overlay
only and do not create or alter any model dimension.

## Reproduction and hashes

```powershell
python reference_model.py
Get-FileHash reference_model.py, reference_phone.stl, reference_rear_overlay.png -Algorithm SHA256
```

| Artifact | SHA-256 |
|---|---|
| `reference_model.py` | `6ab360c504b516abf9cd67ca82af092809636ff06b4928773ecdb38c769409b0` |
| `reference_phone.stl` | `81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48` |
| `reference_rear_overlay.png` | `7e1b3cb8dc0e75ce8c5c2a563c8a3d073060cda7deaaa1bb74ddcf403baee2c9` |

The STL re-imported as one watertight body with bounds
`[[0, 0, 0], [72.0, 152.800003, 8.600000]]` mm. It is an exported nominal mating
envelope, not an acceptance claim.
