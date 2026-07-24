---
contract: D1-reference-manifest
contract_version: 4
job_id: round4-t2-team-v4
commission: D1
status: COMPLETE_PENDING_M2_ACCEPTANCE
---

# Blind reference receipt

| Item | Record |
|---|---|
| Input contract | `dimensions.md` r1, SHA-256 `d84627a873ee4eb24d7fc151e645368b3c374d11bef58320773dcc0d8555329c` |
| Matching evidence use | `fixture_views.svg` top and side matching views only; fixture SHA-256 `495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c` |
| Frame/units | mm; D0=`Z=0`, D1=`X=0`, D2=`Y=0`, D3=`+Z` |
| Exported bounded geometry | F02 only: centred box `62.0 × 11.7 × 24.0 mm`, `X=-31…31`, `Y=-5.85…5.85`, `Z=0…24.0` |
| Explicitly unknown/bounded | F01 cap thickness/rim/underside, F03 end treatment, F04 root transition. The nominal F01 Ø63 D0 envelope is shown only in views and is not export geometry. |
| Re-import check | `trimesh` STL bounds `62.000 × 11.700 × 24.000 mm`; min `[-31.0,-5.85,0.0]`; max `[31.0,5.85,24.0]`; watertight, 12 faces. |
| Overlay result | `reference_overlay_top.svg` and `reference_overlay_side.svg` align D0–D3 and the stated F02 envelope to the matching fixture views; M2 owns acceptance. |

## Outputs and SHA-256

| File | SHA-256 |
|---|---|
| `reference_model.py` | `6f013cd607884b8131ced70f08d88b53e496b6fb8f649070dff517c3abda51b0` |
| `reference_bar.stl` | `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a` |
| `reference_bar.step` | `ddf9cf63f86c11f083fbed824c64f8148384d5bb6e9551dc446402c7553c80dc` |
| `reference_top.svg` | `62869c56a7d05295fa8d333ec4ebfc3d334c7fdea5c604f181eb7d8fb3a72e82` |
| `reference_side.svg` | `d59e31da3c32db8fa1159b8b6b79c44cd2dc37fd3036b0c179808ddd303137c1` |
| `reference_isometric.svg` | `033582adf3a25f34326759c72aebd9920e9d0b0e0be7bd36a8118f9fd204a829` |
| `reference_overlay_top.svg` | `11fefffdcb920a8fb57852e6143e6cca6bd6e04c948f41d528354d8f46b1894f` |
| `reference_overlay_side.svg` | `c9a49c14d31c5603cd53e4672cb3e424eec9171c26671da6445de81cf35da0dd` |

## Commands

`python reference_model.py`; `python -c "import trimesh; ... trimesh.load_mesh('reference_bar.stl') ..."`; `Get-FileHash ... -Algorithm SHA256`.

Failures: CadQuery has no `importSTL` helper; the re-import measurement used installed `trimesh`. Two Chromium headless preview-capture attempts emitted no PNG; SVG views are the durable opaque renders. Token telemetry: not exposed.
