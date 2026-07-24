---
contract: dimensions
contract_version: 4
job_id: round4-t2-team-v4
revision: 2
owner: metrologist
status: ACCEPTED
updated_utc: 2026-07-24T02:52:37.0320848Z
---

# Dimensions

## Frame

| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| Installed frame | Cap face is plane `Z=0`; cap axis is `+Z`; bar long axis is `+X`; bar short axis is `+Y`; origin is bar/cap common projected centre. The installed tool approaches along `-Z` until its protective stop/clearance plane is above `Z=0`. | schematic top and side views | B official/corroborated |
| D0 | `Z=0`, nominal appliance-facing cap face. | schematic side view | B official/corroborated |
| D1 | `X=0`, bar longitudinal centre plane; bar spans symmetrically in `X`. | schematic top view | B official/corroborated |
| D2 | `Y=0`, bar transverse centre plane; bar spans symmetrically in `Y`. | schematic top view | B official/corroborated |
| D3 | Cap axis, normal to D0 through D1/D2 intersection; torque axis. | schematic top/motion view | B official/corroborated |

## Sources

| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| S1 | `experiments/round3-t2/common/brief.md` | participant-visible brief | `e82b8a49c74797732abb795587ff57c4e29d6c647c832e944b0084d3c269ac26` | Declares purpose, material, printer/nozzle, support-free constraint, and approximate cap diameter. |
| S2 | `experiments/round3-t2/common/evidence/fixture_views.svg` | participant-facing synthetic caliper schematic | `495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c` | Explicitly says numeric dimensions govern; schematic proportions, cap thickness, corner radii, and unseen underside do not govern. |
| S3 | `experiments/round3-t2/common/common_manifest.json` | common-package manifest | supplied input | Confirms S1/S2 hashes and that S2 is synthetic evidence, not a historical photo. |

## Blind-build completeness

| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| F01 | Circular cap face / 1 / protected clearance envelope and torque axis | On D0, centre D3, nominal `Ø63.0`; thickness and rim form unknown. | S1, S2 | B official/corroborated | Do not clamp, tooth, or score cap; keep all appliance-contact geometry above D0 by a named positive clearance. Do not rely on cap OD for retention. | yes |
| F02 | Raised cross-bar / 1 / primary mating and torque-transfer feature | Centre D1/D2; `X=±31.0`, `Y=±5.85`, `Z=0…24.0`; rectangular plan envelope. | S1, S2 | B official/corroborated | Blind reference is a centred `62.0 × 11.7 × 24.0` bar on D0. Candidate must use an open-bottom, smooth capture channel around this envelope. | yes |
| F03 | Bar end treatment / 2 / local insertion/retention boundary | End-corner radius/chamfer is not dimensioned; contained within F02 envelope. | S2 | C image-derived | Reference uses square bounded envelope; candidate entrance must tolerate unknown end treatment without touching/teething. | yes |
| F04 | Cap-to-bar root transition / 1 continuous interface / appliance-protection boundary | Root fillet/ramp unknown; lies at F02-to-D0 intersection. | S2 | C image-derived | Maintain a no-contact relief plane above D0 and avoid interior edges at bar root. | yes |
| F05 | Tool approach/torque directions / 1 functional relation | Engagement is along `-Z`; hand torque is about D3. | S1, S2 | B official/corroborated | Channel must remain open in `-Z` and provide hand-turnable exterior; no inference of a hidden locking feature. | yes |

## Dimensions

| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|
| M01 | Cap outer diameter | nominal `63.0 mm`; metrology tolerance not supplied | D0, D3; schematic callout, brief says approximately 63 | S1, S2 | B official/corroborated | Non-fit-driving: candidate must not depend on cap-OD interference or circumferential retention. |
| M02 | Bar overall length | `62.0 mm` | Along X from D1: `X=-31.0…+31.0` | S1, S2 | B official/corroborated | Fit-driving. Specify `bar_length_clearance_per_end >= 0.50 mm` (D PETG FDM guidance); nominal channel X span `>=63.0 mm`. |
| M03 | Bar width | `11.7 mm` | Along Y from D2: `Y=-5.85…+5.85` | S1, S2 | B official/corroborated | Fit-driving. Specify `bar_width_clearance_per_side >=0.30 mm` (D); nominal channel Y width `>=12.30 mm`. |
| M04 | Bar height above cap face | `24.0 mm` | D0 to bar top, +Z | S1, S2 | B official/corroborated | Fit-driving. Specify `bar_top_clearance >=0.60 mm` (D); channel interior height from protective lower plane `>=24.60 mm`. |
| M05 | Appliance-contact clearance | `>0 mm`; target `>=0.60 mm` at all non-bar interior surfaces in installed position | Normal to D0; design allowance, not a fixture measurement | S1, S2 | D assumed | Fit-driving protective rule. Candidate/reference verifies no cap intersection; designer may increase clearance but not reduce below target without revised metrology. |
| M06 | Bar centring/handedness | centred on D1/D2; no handed feature evidenced | D1/D2 top-view alignment | S2 | B official/corroborated | Fit-driving. Mirror-symmetric reference only; verify channel centre is D1/D2, not merely the correct size. |
| M07 | Surface safety | no teeth or sharp appliance-contact edges | qualitative requirement at F01–F04 | S1, S2 | B official/corroborated | Fit-driving. Smooth/relieved mating surfaces; no pointed retention geometry. |

## Open questions

| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| Q01 | Actual manufacturing tolerances, bar corner radii, and root fillet | A near-zero-clearance channel could bind or gouge the bar/root. | Use the M02–M05 conservative clearances and F03/F04 bounded-envelope response; record any larger design allowance. | no |
| Q02 | Cap thickness/underside geometry | An enclosing or cap-supported tool could collide with unseen geometry. | Candidate must be bar-engaging/open-bottom and not rely on unknown cap thickness. | no |
| Q03 | Required operating torque and hand size | Handle strength/ergonomics cannot be numerically sized from supplied evidence. | Print engineer/designer may choose a conservative hand grip; do not claim a load rating. | no |

## Reference round trip

| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
| D1 `reference_bar.stl` `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a` | Look-first review: top PNG/SVG and side SVG overlay aligned on D0–D3; re-imported STL bounds `[-31,-5.85,0]…[31,5.85,24]`, extents `62.0 × 11.7 × 24.0 mm`, watertight/12 faces. | ACCEPTED: specified F02 envelope coincides in top and side; F01/F03/F04 remain explicitly bounded, not falsely reconstructed. | no |

## M1 completion receipt

| Commission | Result | Evidence | Token telemetry |
|---|---|---|---|
| M1 metrologist | COMPLETE — reference-build-ready dimensions revision 1; M2 acceptance subsequently recorded in revision 2. | F01–F05 complete; M02–M05 are named fit parameters with uncertainty/clearance guidance; S1–S3 bound. | not exposed |

## M2 acceptance receipt

| Commission | Result | Evidence | Token telemetry |
|---|---|---|---|
| M2 metrologist/reuse context | ACCEPTED — D1 blind reference conforms to the declared F02 bounded envelope; no sheet correction required. | Existing `reference_overlay_top.png` visually inspected first; `reference_overlay_top.svg`/`reference_overlay_side.svg` inspected with D0–D3 alignments; independent `trimesh` STL re-import bounds audit. No additional evidence artifact needed. | not exposed |
