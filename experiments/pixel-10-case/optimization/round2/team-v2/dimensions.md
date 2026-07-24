---
contract: dimensions
contract_version: 2
job_id: pixel-10-base-case-v2
revision: 2
owner: metrologist
status: ACCEPTED
updated_utc: 2026-07-24T00:10:00Z
---

# Dimensions

## Frame
| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| O / body frame | Origin O is the intersection of the rear-body plane, left exterior tangent plane, and bottom exterior tangent plane; nominal body occupies X=0..72.0, Y=0..152.8, Z=0..8.6. +X right when viewing rear, +Y top, +Z front. | S1 dimensions; frame convention | B / D |
| A: rear plane | Nominal phone rear, Z=0; all rear clearance/opening depths reference A. | Frame convention | D |
| B: left plane | Nominal left body tangent, X=0. | Frame convention | D |
| C: bottom plane | Nominal bottom body tangent, Y=0. | Frame convention | D |
| D: front plane | Nominal front glass/body plane, Z=8.6. | S1 depth + frame convention | B / D |

## Sources
| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| S1 | https://support.google.com/pixelphone/answer/7158570?hl=en-GB | Pixel 10 base | accessed 2026-07-24 | Google official specifications: 152.8 x 72.0 x 8.6 mm; no feature coordinates/radii. |
| S2 | `../../../evidence/input/pixel10_official_hardware_diagram.png` | Pixel 10 base | SHA-256 `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0` | Frozen local capture of Google official diagram (source URL https://support.google.com/pixelphone/answer/7157629?hl=en#Pixel10); identity/relative layout only, not calibrated. |
| S3 | `../../../benchmark_brief.md` | Pixel 10 base commission | frozen common input | Binds exact body envelope and functional requirements. |

## Blind-build completeness
| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| F01 | Body / one mating envelope | X 0..72.0; Y 0..152.8; Z 0..8.6 mm | S1 | B | Blind reference: rectangular rounded body envelope; case cavity applies D01 clearance. | yes |
| F02 | Four body corners / protection | Four corners of F01; physical corner radius unknown, use r=10.0..14.0 mm for blind reference only | S1 + D assumption | B / D | Case protects all corners; reference uses r=12.0 mm and labels it provisional. | yes |
| F03 | Front display / screen field | Front (near D), centered; exact active-area and camera coordinate unknown | S2 | C | Open front with continuous protective lip; no front window or feature cutout based on uncalibrated positions. | yes |
| F04 | Front-facing camera / one functional opening | On F03 near top center; exact envelope unknown | S2 | C | Remains inside open-front field; no separate hole. | yes |
| F05 | Top microphone / one | Top edge Y=152.8; exact X/Z and bore unknown | S2 | C | Top-edge clearance slot: X=28..44, Y=151.6..154.5, full edge/open-face response; must not seal. | yes |
| F06 | Top speaker / one | Top edge Y=152.8; exact X/Z and grille unknown | S2 | C | Shares F05 top-edge clearance slot; no micro-grille inferred. | yes |
| F07 | Power button / one, right-side operation | Right edge X=72.0; upper half; exact Y span unknown | S2 | C | Raised flexible cover or one conservative side opening in Y=88..130; preserve operation. | yes |
| F08 | Volume controls / two functions | Right edge X=72.0; below F07 in official relative order; exact Y spans unknown | S2 | C | Raised flexible two-button region or conservative side opening in Y=45..88; preserve both functions. | yes |
| F09 | Fingerprint sensor / one | Associated with right-side controls in S2; exact implementation/location unknown | S2 | C | Do not add a separate obstruction; F07 response must retain intended power/fingerprint access. | yes |
| F10 | Rear wide camera / one | Rear A; within upper camera/flash field; exact position/diameter/protrusion unknown | S2 | C | Included in shared rear aperture F14; no lens-specific bore inferred. | yes |
| F11 | Rear ultrawide camera / one | Rear A; within upper camera/flash field; exact position/diameter/protrusion unknown | S2 | C | Included in shared rear aperture F14. | yes |
| F12 | Rear 5x telephoto camera / one | Rear A; within upper camera/flash field; exact position/diameter/protrusion unknown | S2 | C | Included in shared rear aperture F14. | yes |
| F13 | Rear microphone / one | Rear A; near camera field; exact position/bore unknown | S2 | C | Included in shared rear aperture F14; never cover with solid back. | yes |
| F14 | Rear camera/flash/microphone field / one shared functional envelope | D assumption: X=2..70, Y=107..150, Z<=0 (rear-facing); clearance aperture, corner r=3.0 mm min | S2 + bounded assumption | C / D | Through-aperture or fully open upper rear field; edge stays >=2.0 mm from body tangencies; camera lip may surround the shared field. | yes |
| F15 | LED flash / one | Rear A; in F14; exact coordinate/diameter unknown | S2 | C | Included in F14, unobstructed. | yes |
| F16 | NFC / one | Rear internal region; coordinate/envelope unknown | S2 | C | Back remains thin/continuous outside F14; no embedded magnet or metal specified. | yes |
| F17 | Pixelsnap magnets / one array | Rear internal central region; coordinate/envelope unknown | S2 | C | No embedded magnets; continuous back outside F14; limit assumed back wall per D03. | yes |
| F18 | Bottom speaker / one | Bottom edge Y=0; exact X/Z and grille width unknown | S2 | C | Shared bottom opening F21; no inferred individual grille. | yes |
| F19 | USB-C port / one, plug clearance | Bottom edge Y=0; exact X/Z unknown | S2 | C | Central bottom opening F21, X=22..50, Y=-4..2; full depth/open-face response for plug. | yes |
| F20 | Bottom microphone / one | Bottom edge Y=0; exact X/Z/bore unknown | S2 | C | Included in F21; never use a sealed bottom rail. | yes |
| F21 | Bottom functional opening / one shared envelope | D assumption: X=8..64, Y=-4..2, full edge/open-face response | S2 + bounded assumption | C / D | Continuous bottom cutout; protects corners while leaving speaker/USB-C/mic unsealed. | yes |
| F22 | Screen-protection lip / one required case feature | D assumption: >=0.8 mm proud of D after case is seated; exact phone glass recess unknown | S3 | D | Continuous front perimeter lip, interrupted only by open front; avoid sharp edge. | yes |
| F23 | Camera-protection lip / one required case feature | D assumption: >=0.8 mm above the highest unknown camera stack; unknown stack means a shared aperture surround only, no flush claim | S3 | D | Raised rounded rim around F14; final height remains an open fit validation item. | yes |

## Dimensions
| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|
| D01 | Phone X width | 72.0 mm | B, exterior tangent planes | S1/S3 | B | Reference exact nominal; TPU cavity target X=72.6 mm (D), +0.6 total clearance. |
| D02 | Phone Y height | 152.8 mm | C, exterior tangent planes | S1/S3 | B | Reference exact nominal; TPU cavity target Y=153.4 mm (D), +0.6 total clearance. |
| D03 | Phone Z depth | 8.6 mm | A to D | S1/S3 | B | Reference exact nominal; rear interior target depth 8.9 mm (D), +0.3 clearance; case back wall target 1.2..1.5 mm (D) for Qi2 compatibility. |
| D04 | Body corner radius | 10.0..14.0 mm | F01 tangencies; visual-safe bound, not measured | S1/S2 | D | Use r=12.0 mm blind reference; do not claim fit at corners until overlay/coupon. |
| D05 | Rear shared aperture | X=2..70; Y=107..150 mm | A/B/C; deliberately oversized bound for F10..F15 | F14 | D | Rounded rectangle, r>=3.0 mm; retains minimum 2 mm left/right/top rim by nominal envelope. |
| D06 | Right controls zone | Y=45..130 mm | B/right exterior, broad official-order bound | S2 | D | Split zone as F07/F08 only after visual confirmation; one long compliant opening is permitted for reference. |
| D07 | Bottom opening | X=8..64 mm | C/bottom exterior; broad shared-function bound | F21 | D | Must encompass D08; retain corner rails. |
| D08 | USB-C plug zone | X=22..50; Y=-4..2 mm | C, centered conservative bound | S2 | D | No solid material in zone; final plug fit requires coupon. |
| D09 | Top opening | X=28..44; Y=151.6..154.5 mm | C/top exterior; shared function bound | F05/F06 | D | Do not replace with inferred holes/grille. |
| D10 | Nominal cavity clearance | X/Y +0.6 total; rear +0.3 | A/B/C/D; print-process starting assumption | D01..D03 | D | Fit coupon must test actual wall/edge geometry; tune after physical result. |

## Open questions
| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| Q01 | The bound official diagram is non-calibrated and is not a physical-device photo. | It supports identity/relative order, not feature coordinate extraction. | Use S2 visually for relative layout only; all feature coordinates remain C/D and F14/F21/D06 are conservative envelopes. | Does not block blind reference; blocks acceptance of exact feature placement. |
| Q02 | Camera bar/lens/flash/mic positions, protrusion, and field height. | A too-small aperture or lip can obstruct camera/flash/mic. | F14/D05 shared aperture; no lens-specific geometry. | Does not block blind reference; blocks fitted rear aperture acceptance. |
| Q03 | Button spans and fingerprint interaction geometry. | Button cover may bind or obstruct fingerprint use. | F07/F08/D06 conservative right-side response. | Does not block blind reference; blocks control-detail acceptance. |
| Q04 | Port, speaker, and microphone coordinates. | Bottom/top cutouts may obstruct function or weaken rails. | F21/D07/D08/D09 shared openings. | Does not block blind reference; blocks exact opening acceptance. |
| Q05 | Real device corner radius, glass recess, and camera-stack height. | Corner capture and protective-lip claims may be wrong. | D04; F22/F23 provisional values; validate with device/coupon and later overlay. | Does not block blind reference; blocks fit/protection acceptance. |

## Reference round trip
| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
| `reference_model.py` `6ab360c504b516abf9cd67ca82af092809636ff06b4928773ecdb38c769409b0`; `reference_phone.stl` `81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48` | `reference_rear_overlay.png` `7e1b3cb8dc0e75ce8c5c2a563c8a3d073060cda7deaaa1bb74ddcf403baee2c9`; rear same-view inspection | ACCEPTED — D01--D04 blind body frame/bounds and D05/F14 conservative rear envelope agree with this sheet. This is envelope-only acceptance; Q01--Q05 remain unresolved. | No. S2 remains relative-layout-only; no diagram pixel has been promoted to a measurement. |
