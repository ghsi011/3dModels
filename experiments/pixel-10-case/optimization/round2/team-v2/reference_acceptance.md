---
contract: reference-acceptance
contract_version: 2
job_id: pixel-10-base-case-v2
owner: metrologist
decision: ACCEPTED
dimensions_revision: 2
updated_utc: 2026-07-24T00:10:00Z
---

# Reference acceptance

| Evidence | Observation | Result |
|---|---|---|
| `reference_phone.stl` SHA-256 `81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48` | Blind body is D01--D04: X 0..72.0, Y 0..152.8, Z 0..8.6 mm; D04 remains the provisional 12.0 mm reference radius. | accepted |
| `reference_rear_overlay.png` SHA-256 `7e1b3cb8dc0e75ce8c5c2a563c8a3d073060cda7deaaa1bb74ddcf403baee2c9` | Red body frame follows the rear handset silhouette; amber D05/F14 X=2..70, Y=107..150 envelope contains the rear camera/flash field. | accepted |
| S2 non-calibrated official diagram | Used only for relative-layout overlay; no pixel-derived feature coordinate, radius, or protrusion is claimed. | accepted |

Decision: **ACCEPTED** for the blind mating-envelope round trip only. Q01--Q05 remain open and prohibit exact feature-placement acceptance.
