---
contract: dimensions
contract_version: 1
job_id: pixel-10-case-team
revision: 3
owner: metrologist
status: ACCEPTED
units: mm
source_photo_set: ../../evidence/input/
updated_utc: 2026-07-24T12:10:00Z
---

# Dimensions

## Coordinate frame and named datums
- Handedness: right-handed.
- +X: handset left to right when viewing the rear; +X is the handset's left side when viewing the front.
- +Y: bottom edge to top edge.
- +Z: rearward, normal out of the back cover; the phone body occupies Z = -8.6 to 0.0 at its nominal rear plane.
| Datum ID | Definition | Evidence |
|---|---|---|
| D0_REAR | Principal rear body plane, Z = 0 | M-003 and IMG-01 rear view |
| D1_XMID | Vertical centre plane, X = 0 | M-002 official width and IMG-01 symmetric body |
| D2_BOTTOM | Bottom exterior edge plane, Y = 0 | M-001 official height and IMG-01 |
| D3_RIGHT | Right side exterior tangent plane, X = +36.0 | M-002 official width; F-006/F-007 side identity from IMG-01 |
| D4_TOP | Top exterior edge plane, Y = +152.8 | M-001 official height |

## Source register
| Source ID | Type | Path/URL | Captured date | Variant relevance |
|---|---|---|---|---|
| IMG-01 | official hardware diagram, local capture | ../../evidence/input/pixel10_official_hardware_diagram.png | 2026-07-24 | base Pixel 10; identity/relative layout only |
| DOC-01 | common evidence register | ../../evidence/input/README.md | 2026-07-24 | records official links and immutable image hash |
| WEB-01 | official Google hardware specifications | https://support.google.com/pixelphone/answer/7158570/pixel-phone-hardware-tech-specs?hl=en-GB | 2026-07-24 | exact base Pixel 10 body dimensions |
| WEB-02 | official Google hardware diagram | https://support.google.com/pixelphone/answer/7157629?hl=en#Pixel10 | 2026-07-24 | feature identity and handedness; uncalibrated |
| WEB-03 | existing-model research lead, not adopted | https://www.printables.com/model/1391738-pixel-10-3d-model | 2026-07-24 | page unavailable to this runtime; no numbers used |
| WEB-04 | existing-model research lead, not adopted | https://makerworld.com/en/models/1754571-google-pixel-10-10-pro-case | 2026-07-24 | page unavailable to this runtime; no numbers used |
| MET-01 | visual annotation and research log | evidence/metrology/meta-1_evidence.md | 2026-07-24 | provenance for all photo-derived observations |
| MET-02 | frozen-diagram aperture measurement log | evidence/metrology/meta-3_camera_datums.md | 2026-07-24 | C-grade camera/flash location and outer-diameter estimates; no reference geometry used |

## Feature inventory
| Feature ID | Name/type | Count | Parent/region | Photo evidence | Functional role |
|---|---|---:|---|---|---|
| F-001 | handset body envelope, rounded rectangular prism | 1 | D0_REAR/D1_XMID/D2_BOTTOM | IMG-01 | primary mating object for compliant case cavity |
| F-002 | corner/edge rounding | 4 | F-001 perimeter | IMG-01 | corner capture and impact protection; no sharp internal mismatch |
| F-003 | raised rear camera island, rounded horizontal capsule | 1 | rear, near D4_TOP | ANN-01 | must be excluded from case back and protected by a lip |
| F-004 | rear camera apertures/lenses | 3 | within F-003 | ANN-02 | camera field must remain fully open; three-camera variant discriminator |
| F-005 | rear flash aperture | 1 | within F-003, +X side | ANN-02 | must remain fully open |
| F-006 | power control | 1 | right side D3_RIGHT | ANN-04 | must remain actuable or exposed |
| F-007 | volume controls | 1 assembly | right side D3_RIGHT | ANN-04 | must remain actuable or exposed |
| F-008 | bottom speaker opening(s) | 1 region | D2_BOTTOM | ANN-03 | acoustic clearance |
| F-009 | USB-C receptacle | 1 | D2_BOTTOM, approximately D1_XMID | ANN-03 | plug insertion envelope |
| F-010 | bottom microphone | 1 | D2_BOTTOM | ANN-03 | acoustic clearance |
| F-011 | top speaker | 1 | front/top region | ANN-05 | screen-lip clearance |
| F-012 | front camera aperture | 1 | front, near D4_TOP/D1_XMID | ANN-05 | screen-lip clearance |
| F-013 | top microphone | 1 | D4_TOP | ANN-06 | acoustic clearance |
| F-014 | Pixelsnap/Qi2 magnetic charging region | 1 | central rear | IMG-01 / benchmark brief | keep back wall thin and free of embedded geometry |

## Dimension register
| Dim ID | Feature ID | Quantity | Value | Tol/uncertainty | Datum/from-to | Provenance | Confidence | Fit-critical | Approval/status |
|---|---|---|---:|---:|---|---|---|---|---|
| M-001 | F-001 | overall height | 152.8 | 0.2 | D2_BOTTOM to D4_TOP | WEB-01 official spec, corroborated by DOC-01 | B | yes | accepted for blind reference |
| M-002 | F-001 | overall width | 72.0 | 0.2 | left side to D3_RIGHT; D1_XMID at half width | WEB-01 official spec, corroborated by DOC-01 | B | yes | accepted for blind reference |
| M-003 | F-001 | body depth excluding camera island | 8.6 | 0.2 | front exterior to D0_REAR | WEB-01 official spec, corroborated by DOC-01 | B | yes | accepted for blind reference |
| M-004 | F-002 | plan corner radius envelope | 10.0 | 3.0 | F-001 perimeter, tangent to D2_BOTTOM/D3_RIGHT/D4_TOP | IMG-01 visual estimate; no calibrated drawing | C | yes | bounded: cavity must use generous compliant corner relief and coupon |
| M-005 | F-003 | camera-island overall X width | 60.5 | 2.5 | centred on D1_XMID; outer silhouette to outer silhouette | IMG-01 scaled rear silhouette; see MET-01 | C | yes | bounded: candidate opening must clear nominal plus uncertainty and TPU process clearance |
| M-006 | F-003 | camera-island overall Y height | 22.0 | 2.5 | outer silhouette to outer silhouette | IMG-01 scaled rear silhouette; see MET-01 | C | yes | bounded: candidate opening must clear nominal plus uncertainty and TPU process clearance |
| M-007 | F-003 | island X centre | 0.0 | 1.5 | D1_XMID to island centre | IMG-01 symmetric visual layout | C | yes | accepted as centred envelope; verify against real device before final print |
| M-008 | F-003 | island top-edge Y position | 138.8 | 3.0 | D2_BOTTOM to top outer silhouette | IMG-01 scaled from M-001; see MET-01 | C | yes | bounded: camera opening must extend toward D4_TOP by at least 3.0 mm beyond nominal |
| M-009 | F-003 | island rearward protrusion above D0_REAR | 2.0 | 1.5 | D0_REAR to maximum rear island surface | no official dimensional drawing; conservative reference assumption | C | yes | reference nominal only; camera-lip design must accommodate 0.5–3.5 mm and coupon/real-device check |
| M-010 | F-004 | camera count | 3 | 0 | inside F-003 | IMG-01 / benchmark brief official feature identity | B | yes | accepted; a two-camera layout is rejected |
| M-011 | F-005 | flash count | 1 | 0 | inside F-003 at +X side | IMG-01 official feature identity | B | yes | accepted |
| M-012 | F-006/F-007 | right-side control Y envelope | 82.0 | 30.0 | D2_BOTTOM to combined visible control region centre | IMG-01 front/right silhouette; no calibrated side drawing | C | yes | bounded: use a continuous/open side relief spanning Y = 42–122, or confirm exact covers by coupon |
| M-013 | F-006/F-007 | right-side control X face | 36.0 | 0.2 | D1_XMID to D3_RIGHT | M-002 derived | B | yes | accepted |
| M-014 | F-009 | USB-C centre X | 0.0 | 3.0 | D1_XMID to receptacle centre | IMG-01 bottom identity, symmetric-layout estimate | C | yes | bounded: bottom opening must be centred and at least 18 mm wide pending coupon |
| M-015 | F-009 | USB-C bottom-edge Y position | 0.0 | 1.0 | D2_BOTTOM | IMG-01 / normal bottom-edge feature relation | C | yes | bounded: case bottom must be open at D2_BOTTOM around port |
| M-016 | F-008/F-010 | speaker/microphone bottom envelope | full remaining bottom edge outside USB-C | 4.0 | D2_BOTTOM | IMG-01 identifies features but not slots | C | yes | bounded: avoid solid bottom bridge beyond protected corner returns; inspect actual device before final print |
| M-017 | F-013 | top microphone X envelope | 0.0 | 24.0 | D1_XMID, D4_TOP | official diagram identifies top microphone but no calibrated location | C | yes | bounded: include an 8 mm top-edge relief centred on D1_XMID or confirm exact point before final print |
| M-018 | F-014 | charging-back maximum added case wall | 2.0 max | 0.5 | normal to D0_REAR, excluding protective local camera lip | benchmark brief requirement; process constraint, not phone measurement | C | no | design constraint for print engineer/candidate; no embedded magnets |
| M-019 | F-004-A | camera A centre | X = -21.8; Y = 25.0 below D4_TOP | 2.0 each axis | D1_XMID signed X; D4_TOP downward Y | IMG-01 frozen-diagram scale; MET-02 | C | yes | accepted bounded datum for blind reference; candidate retains oversized shared opening |
| M-020 | F-004-A | camera A outer aperture diameter | 4.5 | 1.5 | concentric with M-019, in D0_REAR plane | IMG-01 frozen-diagram scale; MET-02 | C | yes | bounded datum; no tight individual case pocket |
| M-021 | F-004-B | camera B centre | X = -2.9; Y = 25.0 below D4_TOP | 2.0 each axis | D1_XMID signed X; D4_TOP downward Y | IMG-01 frozen-diagram scale; MET-02 | C | yes | accepted bounded datum for blind reference; candidate retains oversized shared opening |
| M-022 | F-004-B | camera B outer aperture diameter | 4.5 | 1.5 | concentric with M-021, in D0_REAR plane | IMG-01 frozen-diagram scale; MET-02 | C | yes | bounded datum; no tight individual case pocket |
| M-023 | F-004-C | camera C centre | X = +9.4; Y = 25.0 below D4_TOP | 2.0 each axis | D1_XMID signed X; D4_TOP downward Y | IMG-01 frozen-diagram scale; MET-02 | C | yes | accepted bounded datum for blind reference; candidate retains oversized shared opening |
| M-024 | F-004-C | camera C outer aperture diameter | 4.5 | 1.5 | concentric with M-023, in D0_REAR plane | IMG-01 frozen-diagram scale; MET-02 | C | yes | bounded datum; no tight individual case pocket |
| M-025 | F-005 | flash centre | X = +23.5; Y = 25.0 below D4_TOP | 2.0 each axis | D1_XMID signed X; D4_TOP downward Y | IMG-01 frozen-diagram scale; MET-02 | C | yes | accepted bounded datum for blind reference; candidate retains oversized shared opening |
| M-026 | F-005 | flash outer diameter | 6.0 | 1.5 | concentric with M-025, in D0_REAR plane | IMG-01 frozen-diagram scale; MET-02 | C | yes | bounded datum; no tight individual case pocket |

## Derived dimensions
| Dim ID | Formula | Inputs | Result | Confidence rule |
|---|---|---|---:|---|
| D-001 | M-002 / 2 | M-002 | 36.0 | inherits B |
| D-002 | M-001 - M-008 | M-001, M-008 | 14.0 | lower input confidence C |
| D-003 | M-008 - M-006 / 2 | M-008, M-006 | 127.8 | lower input confidence C |
| D-004 | M-009 upper bound | M-009 | 3.5 | C bound, not nominal truth |
| D-005 | D4_TOP - camera/flash centre offset | M-019, M-021, M-023, M-025 | Y = 127.8 | lower input confidence C; each feature retains its own ±2.0 mm datum uncertainty |

## Assumptions and open questions
| ID | Feature/dim | Risk | Exact question or approved bound | Required response | Status |
|---|---|---|---|---|---|
| A-01 | M-004 F-002 corner radius | tight internal corner can prevent seating or cause stress whitening | C-grade 7–13 mm radius envelope; no caliper/photo measurement exists | reference uses 10 mm nominal; candidate uses compliant generous relief; coupon must include one corner | bounded, non-blocking for reference |
| A-02 | M-005–M-009 F-003 camera island | camera aperture/lip can collide or vignette | C-grade 58–63 mm wide, 19.5–24.5 mm high, top Y 135.8–141.8, protrusion 0.5–3.5 | reference nominal per register; candidate has oversized cutout and real-device/coupon camera-lip confirmation | bounded, non-blocking for reference |
| A-03 | M-012 F-006/F-007 controls | inaccurate button covers may jam or misalign | exact individual button sizes and centres unknown; only continuous 42–122 mm Y relief is approved | keep control side open/continuous in candidate or obtain caliper contacts at each button end and centre before covers | bounded, non-blocking for reference |
| A-04 | M-014–M-016 bottom features | plug, speaker, or mic can be obstructed | individual port/slot geometry unknown; only a broad bottom opening is approved | use centre USB-C opening ≥18 mm wide plus no solid bottom bridge except corner returns; inspect/coupon before final | bounded, non-blocking for reference |
| A-05 | M-017 top microphone | blocked microphone | exact X location unknown | temporary centred 8 mm top relief; real-device confirmation required before final TPU print | bounded, non-blocking for reference |
| A-06 | variant identity | Pixel 10 Pro shares body dimensions but has different rear hardware/finish; a wrong device invalidates fit | confirm the physical unit is the base Pixel 10 three-camera layout shown in IMG-01 | reject/revise before final case print if real device differs | open, downstream final-print blocker only |
| A-07 | M-019–M-026 camera/flash apertures | diagram-derived aperture locations can differ from manufactured hardware | C-grade locations/diameters are bounded by ±2.0 mm centre and ±1.5 mm diameter; never use as a tight individual pocket | rebuild blind reference from r3; use existing shared camera opening and real-device/coupon confirmation before final TPU print | bounded, non-blocking for reference |

## Required reference views
| View ID | Photo | Camera/view cue | Features that must align |
|---|---|---|---|
| V-REAR | IMG-01 | near-orthographic rear, body long axis vertical | F-001 outline, F-003 silhouette/top offset, F-004 three-camera count, F-005 flash side |
| V-FRONT-RIGHT | IMG-01 | near-orthographic front/right silhouette | F-001 outline, F-006/F-007 right-side placement, F-011/F-012 identity |
| V-BOTTOM | IMG-01 | bottom-edge diagram region | F-008/F-009/F-010 ordering and D1_XMID USB-C relation |
| V-TOP | IMG-01 | top-edge diagram region | F-013 top microphone clearance relation |

## Blind reference round-trip
- Reference commission: ref-2, built blind from dimensions.md r3 only. ref-1 remains rejected historical evidence for the r1 sheet omission.
- Reference artifact SHA-256: `evidence/reference/ref-2/pixel10_reference_ref2.stl` `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91`; `evidence/reference/ref-2/pixel10_reference_ref2.step` `6a5e8ae693dc3ce3906b9067e20102c9e6e3311200b4b5706a01dec1da10aa25`.
- Sheet revision built: 3.
- Overlay evidence: `evidence/reference/ref-2/diagram_rear_device_crop_ref2.png`; `evidence/reference/ref-2/overlay_camera_ref2.png`; review record `evidence/reference/ref-2/metrologist_acceptance.md`. The crop derives only from immutable IMG-01; corrective source evidence remains `evidence/metrology/meta-3_camera_datums.md`.
| Feature ID | Observation against photo | Result | Sheet action |
|---|---|---|---|
| F-001 | Ref-2 export bbox is 73.0 × 152.8 × 10.6 mm; 72.0 × 152.8 body and 8.6 mm body-depth contract values are present, with the extra X/Z extent accounted for by the bounded edge/camera proxies. V-REAR silhouette follows IMG-01. | pass | none |
| F-003 | At re-zeroed STL Z=8.7–10.5 mm, ref-2's red island outline visually hugs the frozen diagram island. Overlay residual is mean 0.58 mm, p90 1.18 mm. | pass | retain M-005–M-009 C-grade bounds and real-device coupon requirement |
| F-004/F-005 | Overlay circles land within r3 M-019–M-026 centre/diameter uncertainties: three camera apertures appear in left-to-right A/B/C order and flash is on the +X/right side. A mirrored arrangement would put F-005 on the opposite side and fails the diagram. | pass | none; preserve A-07 bounded shared-opening response |
| F-006/F-007 | V-FRONT-RIGHT plus the ref-2 technical right view show the continuous right-control proxy required by M-012; r3 does not authorize individual tight button geometry. | pass, bounded | retain approved continuous/open candidate relief and coupon requirement |
| F-008/F-009/F-010 | V-BOTTOM was inspected. r3 specifies only a broad bottom-feature envelope and centred USB-C relationship, not individual hole dimensions; ref-2 is adequate as that proxy fixture. | pass, bounded | retain A-04 broad-bottom-opening and real-device confirmation requirement |
| F-013 | V-TOP was inspected; the single top-edge proxy is consistent with A-05's deliberately broad centred relief. | pass, bounded | retain A-05; no exact-microphone certification |
- Round-trip verdict: ACCEPTED
- Accepted by metrologist: meta-4, dimensions.md r3 / ref-2 overlay review.
