# Pixel 10 TPU coupon manifest

Source: `pixel10_case_fit_coupon.py`, derived only from the accepted `model.py` candidate
with the declared `CAVITY_CLEARANCE_MM` value substituted to 0.25, 0.35, or 0.45 mm.
The accepted full-case STL is unchanged: SHA-256
`71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44`.

Every exported coupon was re-imported with vertex processing and is one watertight body.
The lower band is the exact D2_BOTTOM-to-Y=30 portion of the final case. The right-control
strip preserves the full actual Y=42-122 continuous relief; it is 80 mm long because a
30 mm slice cannot contain that 80 mm functional feature.

| Artifact | Per-side clearance (mm) | Region | Bounds (mm) | Triangles | SHA-256 |
|---|---:|---|---|---:|---|
| `pixel10_case_fit_coupon_lower_0p25.stl` | 0.25 | lower band: both corners, cavity, 58 mm bottom opening | 75.700 x 29.614 x 11.700 | 584 | `bd149a0cff7e34330f3f12b28aa7dac5ee0631d38d555ae851589a78e6342eaa` |
| `pixel10_case_fit_coupon_right_control_0p25.stl` | 0.25 | +X continuous control relief | 13.850 x 80.000 x 1.450 | 196 | `9b035bba58fb860f7c781ee0c293d33640875b087997455fd00c44c8ff4c6e4e` |
| `pixel10_case_fit_coupon_lower_0p35.stl` | 0.35 | lower band: both corners, cavity, 58 mm bottom opening | 75.900 x 29.617 x 11.900 | 584 | `28d43b9afa43e26dd5848da9d635bdc1e25b20f3aee5db47027583177caa92f7` |
| `pixel10_case_fit_coupon_right_control_0p35.stl` | 0.35 | +X continuous control relief | 13.950 x 80.000 x 1.550 | 196 | `ee60bbc2e940d18b8c821de5f1d083eb54113f745f9fa71e9d08f71f91b28962` |
| `pixel10_case_fit_coupon_lower_0p45.stl` | 0.45 | lower band: both corners, cavity, 58 mm bottom opening | 76.100 x 29.621 x 12.100 | 584 | `9d7b817de6d7f5dac8d57fa96c411f86ea46b9e97d9627bd080d09b8219ff0fa` |
| `pixel10_case_fit_coupon_right_control_0p45.stl` | 0.45 | +X continuous control relief | 14.050 x 80.000 x 1.650 | 200 | `ceebc609b20cfbf34fcaa463b9ff4d2dfb744edcbfa13dba2a2ca6ab50bd424a` |

Before slicing, put the clearance value and region name on the exterior back of each physical
coupon with a permanent marker. The marker must never enter the cavity, port opening, or
control-relief edge.
