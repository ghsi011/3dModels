---
contract: dimensions
contract_version: 3
job_id: round3-t2-washer-filter-cap-tool
revision: 2
owner: metrologist
status: ACCEPTED
updated_utc: 2026-07-24T01:12:19Z
---

# Dimensions

## Frame
| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| `D0` / origin | Centre of the circular cap-face plane; `(0, 0, 0)` is the bar-side face of that plane. | `E2`, top and side schematic views | B |
| `DZ` | Cap-face plane; positive Z points away from the appliance, toward the raised bar and tool approach. | `E2`, side view and blue engagement arrow | B |
| `DX` | Bar long centreline in the cap-face plane; positive direction is arbitrary because the shown bar is symmetric about `D0`. | `E2`, top view | C |
| `DY` | In-plane axis normal to `DX`; completes a right-handed frame. | `E2`, top view | C |
| `D1` | Bar longitudinal centre plane, `Y=0`; the bar is shown centered on the cap. | `E2`, top view | C |
| `D2` | Bar transverse centre plane, `X=0`; the bar is shown centered on the cap. | `E2`, top view | C |

## Sources
| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| `E1` | `experiments/round3-t2/common/brief.md` | participant-visible brief | `e82b8a49c74797732abb795587ff57c4e29d6c647c832e944b0084d3c269ac26` | Declares tool intent, PETG final material, 0.4 mm nozzle, support-free requirement, and the four nominal fixture dimensions. |
| `E2` | `experiments/round3-t2/common/evidence/fixture_views.svg` | synthetic participant-facing caliper schematic | `495ad7bede3796f3707a6ad410a5d1b71ae2233d2d1d43c20912ea1364758c2c` | Numeric labels govern; geometry is schematic. No cap thickness, bar corner radius, underside, or production tolerance is supplied. |
| `E3` | `experiments/round3-t2/common/common_manifest.json` | common-input manifest | `33b6db717439dfad4656b0ee28dda9d88a74fc94` (frozen commit) | Binds `E1` and `E2`; the manifest itself supplies no fixture geometry. |
| `E4` | `experiments/round3-t2/arms/team-v3/evidence/reference/reference.stl` | blind reference, re-imported | `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a` | Verified watertight bounds are `[-31.00,-5.85,0.00]..[31.00,5.85,24.00]` mm; the cap-face circle remains an unexported construction datum per reference manifest. |

## Blind-build completeness
| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| `F01` | Cap-face circular boundary / 1 / appliance-facing mating envelope | `D0`, `Z=0`; circular face `Ø63.0` (radius 31.50).  No thickness or rear geometry is authorized. | `E1`, `E2` top view | B | Build a non-export reference envelope only; retain cap-face plane and circular outer keep-out. Do not infer a cap body. | yes |
| `F02` | Raised cross-bar / 1 / torque interface | Centred at `D0`; envelope `X=-31.00..+31.00`, `Y=-5.85..+5.85`, `Z=0..+24.00`; rectangular nominal profile. | `E1`, `E2` top/side views | B | Build blind reference as the stated rectangular engagement envelope only; candidate must envelop it without teeth or sharp appliance-contact edges. | yes |
| `F03` | Bar end-to-cap rim clearance / 2 / end collision keep-out | Each displayed bar end is 0.50 from the circular cap diameter along `DX`: `(63.0-62.0)/2`; exact end/rim clearance away from `DX` is not defined. | `E2` top view; derived from `D-001`, `D-002` | C | Preserve the cap circular keep-out at both bar ends; do not treat the 0.50 axial display margin as an all-direction clearance. | yes |
| `F04` | Bar top and side exterior edges / 4 long + 4 end / appliance-contact safety boundary | Nominally sharp rectangular schematic edges; actual radii/chamfers are unspecified. | `E2` schematic limit | C | Treat as unknown rounded-or-sharp within `F02` envelope; tool contact must be broad, smooth, and clearance-controlled rather than keyed to a presumed corner radius. | yes |
| `F05` | Cap face outside bar / 1 annular visible region / non-contact clearance surface | `Z=0`, inside `F01` and outside `F02`; visible face is planar in schematic, but cosmetic texture/curvature is unspecified. | `E2` top/side views | C | Reference only as a planar protected keep-out; candidate must not require contact outside the bar. | yes |
| `F06` | Tool approach direction / 1 / insertion-clearance feature | Approach is `-DZ` toward the cap face after engaging above the bar; tool rotates about `DZ`. | `E2` blue arrows | B | Candidate engagement opening must admit the bar along `-DZ`; design/verifier must sweep this full direction. | yes |
| `F07` | Torque axis / 1 / operating motion | `DZ` through `D0`; normal hand torque is shown about this axis. Required torque magnitude/direction are unspecified. | `E1`, `E2` motion arrow | B | Provide hand-turnable grip and symmetric bar engagement about `DZ`; do not claim load capacity. | yes |

## Dimensions
| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|
| `D-001` | Cap-face diameter | 63.00 mm nominal | `D0`; labelled top-view diameter | `E1`, `E2` | B | Source tolerance absent. Use the 63.00-mm circular keep-out for reference; candidate may not rely on contact with this face. |
| `D-002` | Raised-bar overall length | 62.00 mm nominal | `DX`, from `X=-31.00` to `+31.00`; labelled top-view span | `E1`, `E2` | B | Source tolerance absent. Preserve as full blind engagement span; fit clearance is a downstream print-design parameter, not a measurement substitute. |
| `D-003` | Raised-bar overall width | 11.70 mm nominal | `DY`, from `Y=-5.85` to `+5.85`; labelled top-view span | `E1`, `E2` | B | Source tolerance absent. Candidate must declare a positive per-side fit clearance before export. |
| `D-004` | Raised-bar height above cap face | 24.00 mm nominal | `DZ`, from `Z=0` cap face to `Z=+24.00`; labelled side-view span | `E1`, `E2` | B | Source tolerance absent. Candidate must retain insertion depth to engage this full height without cap-face interference. |
| `D-005` | Axial bar-end margin to cap diameter | 0.50 mm derived nominal, each end | `DX`; `(D-001-D-002)/2` | `E2`; derived | C | Inherits absence of input tolerance. Reference may use only this axial derivation; circular-rim clearance elsewhere remains unknown. |
| `D-006` | Bar placement | centred: bar midpoint coincident with `D0`; `D1` and `D2` coincide with cap diametral planes | Top-view graphical alignment; no separate numeric callout | `E2` | C | Treat as visual placement with no numerical alignment tolerance; blind reference uses coincident centres and round-trip review must challenge it. |

## Open questions
| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| `Q-001` | Production/measurement tolerance for the nominal cap and bar dimensions. | A nominal-only reference can be too tight or loose. | No tolerance is stated. Designer must choose and record a positive PETG fit clearance; verifier must evaluate the resulting nominal-envelope fit. | candidate fit parameter selection, not blind reference |
| `Q-002` | Actual bar corner radii/chamfers and cap-face/bar-root fillets. | A hard keyed profile could gouge or bind. | Bound only by `F02` rectangular envelope; smooth non-toothed contact is required. | no |
| `Q-003` | Cap thickness, rear geometry, nearby appliance geometry, and removal travel beyond shown approach. | A closed or deep tool could collide with unseen geometry. | Only `Z=0` face and `F02` above-face envelope may be referenced. Candidate must avoid claims about unseen geometry. | no |
| `Q-004` | Required torque and handedness of removal. | Grip section and strength cannot be load-certified. | Rotation about `DZ` only; bidirectional/torque value not supplied. | load certification only |

## Reference round trip
| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
| `reference.stl` `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a` | Visually inspected `reference_top.png` `5b1dcbb45a811da3de6478d59fae51970a899a4bbdae5cf7b8d2ae3de602e81f` and `reference_side.png` `bb7ababc8b981a3b41285748b478c08702f4712543725f701a1156575d04983a`; decisive matching top overlay receipt: `evidence/reference/reference_top_overlay.png` `50c092bbaaa526945ae30b501048c584d1f60dd8ef72c910702473c4d95f6d88`, red re-imported `F02` boundary mapped at the schematic's 5 px/mm scale. It hugs the governing `62.00 × 11.70` outline; side render spans `Z=0..24.00`. `F01` is correctly retained only as the authorized non-exported `Ø63.00` keep-out. Rounded drawn corners remain non-governing per `E2` and `Q-002`. | ACCEPTED | no |
