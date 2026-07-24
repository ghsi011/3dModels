---
contract: dimensions
contract_version: 4
job_id: pixel7-case-metrology
revision: 1
owner: metrologist
status: DRAFT
updated_utc: 2026-07-24T21:00:00Z
---

# Dimensions

Google Pixel 7 (known product). All values mm unless noted. This sheet covers the phone's
mating envelope and case-relevant features only; it does not design or plan the case.
`PixelCaseV4.3mf` and `pixel7_high_detail_reference_model.stl` were NOT read (held-out
ground truth, out of scope for this commission).

## Frame
| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| Handedness | Right-handed | — | — |
| D0_BACK | Back-surface plane at the flat (non-camera-bump) region; Z=0 | IMG-07,08 (caliper thickness shots), IMG-04 (back overview) | B |
| +Z | From D0_BACK toward the front screen glass (out of the back) | IMG-04 vs IMG-01 | B |
| D1_CTR | Geometric center of the L×W body footprint projected on D0_BACK; X=0,Y=0 | derived from M-001/M-002 | B |
| D2_TOP | Top edge line (edge nearer the earpiece/front camera and the single mic hole); Y=+L/2 | IMG-05 (top edge, mic hole) | A |
| D3_BOT | Bottom edge line (USB-C edge); Y=−L/2 | IMG-06 (bottom edge, USB-C+grilles) | A |
| +Y | From D3_BOT toward D2_TOP | IMG-01 orientation, consistent across IMG-02/03/05/06 | A |
| D4_RIGHT | Right edge (volume rocker + power button), screen facing viewer, top away; X=+W/2 | IMG-02 (buttons) | A |
| D5_LEFT | Left edge (SIM tray), screen facing viewer, top away; X=−W/2 | IMG-03 (SIM tray) | A |
| +X | From D5_LEFT toward D4_RIGHT | IMG-02/03 consistent handedness (buttons right, SIM left, standard phone convention) | A |
| D6_SCREEN | Front screen/glass plane, nominal Z=+T | IMG-01 and side-edge photos | B |

Handedness note: established by cross-referencing IMG-02 (buttons on one edge) and IMG-03
(SIM tray on the other edge) against the front-face overview IMG-01 and the standard phone
convention (screen facing user, top edge away → buttons right, SIM left). No photo shows
front face and an edge simultaneously in one frame, so this is inferred from consistent
edge-to-edge correspondence across five separate photos, not a single confirmed shot —
noted, not blocking (see OQ-07).

## Sources
| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| IMG-01 | tests/Pixel 7 case/PXL_20260724_161758905.jpg | user's unit | 113bc3a1d53564d65d5cc7f16914c1c0ec3fd381d5f5bae47c285221b2caf5b9 | front/screen overview, held at angle (not orthographic) |
| IMG-02 | tests/Pixel 7 case/PXL_20260724_161805402.jpg | user's unit | 389477f944ae1c7e310503dca363b81fb9fb2dafbb83cf6a2bc07867df9b94f6 | right edge, buttons; hand partly occludes; angled |
| IMG-03 | tests/Pixel 7 case/PXL_20260724_161809053.jpg | user's unit | 23e1fff86c710929415053763bbd16b482104ae9e2dec2b31ccbd3af3435f8de | left edge, SIM tray; angled |
| IMG-04 | tests/Pixel 7 case/PXL_20260724_161811840.jpg | user's unit | aca99de4bf8b477a530e9809d0f88be756fec314ae424e407733c083a2a4a2f4 | back overview, camera bar; angled, hand covers lower half |
| IMG-05 | tests/Pixel 7 case/PXL_20260724_161814868.jpg | user's unit | a258dac619c99f5b504eb8aac91044c7cfa78e99b441470b3d7c3b6d62028988 | top edge, mic hole; angled |
| IMG-06 | tests/Pixel 7 case/PXL_20260724_161817658.jpg | user's unit | 2b2083149089bed4b776811c17f9e42d90bd5b979cfbf0c4bb597869210f39e0 | bottom edge, USB-C + grilles; angled, unobstructed |
| IMG-07 | tests/Pixel 7 case/PXL_20260724_162140395.jpg | user's unit | 98e58b7f0c1f4483e51d808c006b481462e82b31869e511311ad8be6e2d3fbc1 | caliper: length = 155.0 mm, screen-face up |
| IMG-08 | tests/Pixel 7 case/PXL_20260724_162156525.jpg | user's unit | e435f0b56ea3ff9e6cc2a889d6ad3def07916b54a4dc2d850e6bf5fdcd418186 | caliper: width = 71.9 mm, jaw near top corner |
| IMG-09 | tests/Pixel 7 case/PXL_20260724_162226348.jpg | user's unit | 767cb39239308e0c321586475ec2553c609704f6eec5c0e6a01ec40578b656ff | caliper: thickness = 9.6 mm, right-edge/USB-C-corner region |
| IMG-10 | tests/Pixel 7 case/PXL_20260724_162250060.jpg | user's unit | ec2817ae07323767829377f54d2fa17b484d6f2fa329ed8068920cf9607773cb | caliper: thickness = 9.8 mm, near a side button |
| IMG-11 | tests/Pixel 7 case/PXL_20260724_162333722.jpg | user's unit | 7caa963fb81f1f811221fa3b13689295ee8be693e5c17945ae8c49b9f0b49818 | caliper: reading ~20–27 mm, illegible middle digit, feature unclear — excluded |
| IMG-12 | tests/Pixel 7 case/PXL_20260724_162415355.jpg | user's unit | dac2d2fc2b22ba763bf6197e5128cf9af103dbab53ac1db92065bcda082f9c13 | caliper: thickness = 9.5 mm, near a side button |
| IMG-13 | tests/Pixel 7 case/PXL_20260724_162610764.jpg | user's unit | f472e1f034a5793a00bbcb744b72f96d85a47be4d860b2727390c75fe3d83e63 | caliper: 20.4 mm, top edge to camera-bar/matte transition |
| IMG-14 | tests/Pixel 7 case/PXL_20260724_162707747.jpg | user's unit | 6df36ba4d17ff954112cc65fb672ef48eeaa31fc8569911c27790dc4e234b7c1 | caliper: 6.2 mm, top edge to top of lens-oval cutout |
| IMG-15 | tests/Pixel 7 case/PXL_20260724_162943302.jpg | user's unit | 26b10cfd0307b025890aa146d9a18180d066276588f73f969e698a187234c25f | caliper: 84.2 mm at camera-bar level — excluded, likely un-zeroed |
| IMG-16 | tests/Pixel 7 case/PXL_20260724_162947392.jpg | user's unit | ae0a52c018b78c216b00b80b863a1a38aa24f527ffd10df460ada8386ce50227 | ruler-only context shot, no new digit; corroborates camera bar spans full width |
| IMG-17 | tests/Pixel 7 case/PXL_20260724_163021288.jpg | user's unit | ac8cc06c188e4b134488f16fa75a1876541f3004ac03091e30335d9f866af500 | caliper: 14.3 mm, top edge to metal-trim/matte transition |
| SPEC-01 | https://www.gsmarena.com/google_pixel_7-11903.php | family spec + hands-on | accessed 2026-07-24 | 155.6×73.2×8.7 mm, 197 g, Gorilla Glass Victus front/back, aluminum frame, IP68; hands-on section separately states thickness rises to 11.44 mm at the camera bar |
| SPEC-02 | aggregator cross-check (o2.co.uk, dimensions.com, phonesbysize.com) | family spec | accessed 2026-07-24 | corroborates 155.6×73.2×8.7 mm, 197 g; no camera-bump or button/port drawing dimensions found on any source checked |

## Blind-build completeness
| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| F-001 | Body envelope, rounded-rect prism ×1 — primary mating envelope | 155.6(L) × 73.2(W) × 8.7(T) mm, D1_CTR-centered | SPEC-01/02 + IMG-07/08 | B | cavity = envelope + M-018 fit band | yes |
| F-002 | Corner radius ×4 (screen-side and back-side corners, assumed symmetric) | R ≈ 9.5 mm ± 1.5 mm at each of the 4 vertical corners | IMG-07 (calibrated crop) | B | round cavity corners to same R; chamfer per fdm-design.md §9 since corners are the least-accurate region | yes |
| F-003 | Camera bar / bump ×1 — full-width raised band on back, metal insert + color-matched shelf | height 20.4 mm from D2_TOP (full bump) / 14.3 mm (metal insert only); width = full W (edge-to-edge); protrusion ≈2.7 mm above D0_BACK | IMG-13,17 (A); width+protrusion C/B, see M-007/M-008 | mixed A/B/C | camera cutout/raised ring sized to full-bar footprint + LOOSE band (M-019) | yes |
| F-004 | Camera lens-oval cutout ×1 (houses 50MP main + 12MP ultra-wide) | oval ≈ 30–36 mm wide × 6–8 mm tall, set within F-003, top margin ≈6.2 mm below D2_TOP | IMG-14 (A for the 6.2 mm sub-measure); oval size C | C/A mixed | non-fit-critical; case only needs to clear F-003's full footprint, not the individual oval | yes |
| F-005 | Small drilled hole beside the lens oval (likely mic or ambient/flicker sensor) ×1 | cosmetic-only bounded envelope, inside F-003 | IMG-16,17 | C | no case action required (covered if F-003 relief covers whole bar) | yes |
| F-006 | Volume rocker button ×1 | right edge (D4_RIGHT), center ≈ Y=+32 mm from D2_TOP (range +24…+40 mm), length ≈16 mm | IMG-02 | C | LOOSE window (M-020), see OQ-04 | yes (bounded) |
| F-007 | Power button ×1 | right edge (D4_RIGHT), center ≈ Y=+50 mm from D2_TOP (range +44…+58 mm), length ≈10 mm, directly below F-006 | IMG-02 | C | LOOSE window (M-020), see OQ-04 | yes (bounded) |
| F-008 | SIM tray + eject pinhole ×1 | left edge (D5_LEFT), center ≈ Y=+35 mm from D2_TOP (range +25…+45 mm), tray length ≈13 mm | IMG-03 | C | non-fit-critical; access-only, no snug cutout needed | yes (bounded) |
| F-009 | Top mic hole ×1 | top edge (D2_TOP), offset toward D5_LEFT side, ≈10–18 mm from the D5_LEFT corner | IMG-05 | C | small LOOSE relief or leave top edge open in case design | yes (bounded) |
| F-010 | USB-C port ×1 | bottom edge (D3_BOT), centered on X (±2 mm), width ≈8–9 mm, height ≈3 mm | IMG-06 | B (centered), C (exact size) | LOOSE window (M-021) | yes |
| F-011 | Bottom-left speaker/mic grille ×1 | bottom edge (D3_BOT), ≈11 mm inset from D5_LEFT corner, width ≈6 mm | IMG-06 | C | LOOSE window or shared bottom slot (M-021) | yes (bounded) |
| F-012 | Bottom-right speaker/mic grille ×1 | bottom edge (D3_BOT), ≈12 mm inset from D4_RIGHT corner, width ≈6 mm | IMG-06 | C | LOOSE window or shared bottom slot (M-021) | yes (bounded) |
| F-013 | Screen/front-glass plane ×1, incl. front camera hole-punch (cosmetic) | D6_SCREEN, substantially flush to the aluminum frame (no measurable native lip resolved) | IMG-01 + IMG-09/10/12 (edge profile) | D | phone provides negligible native face protection; case should add its own lip (designer decision, not specified here) | yes (bounded, low confidence) |
| F-014 | Back-panel finish step: glossy/metallic camera bar vs. matte back shell | cosmetic only, no case-fit effect beyond F-003's envelope | IMG-04,17 | C | none required | yes |
| F-015 | Google "G" logo, back center (cosmetic) | cosmetic only | IMG-04 | C | none required | yes |

## Dimensions
| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---|---:|---|---|---|
| M-001 | F-001 length (L) | 155.6 mm nominal (caliper corroboration 155.0 mm) | D2_TOP to D3_BOT | SPEC-01/02 (B); IMG-07 direct caliper (A) | B (nominal) / A (corroboration) | use 155.6 as cavity-floor nominal (larger of the two, safer for a case cavity); do not shrink below 155.0 |
| M-002 | F-001 width (W) | 73.2 mm nominal (caliper corroboration 71.9 mm, jaw set near the top corner) | D4_RIGHT to D5_LEFT | SPEC-01/02 (B); IMG-08 direct caliper (A) | B (nominal) / A (corroboration, position caveat) | use 73.2 as cavity-floor nominal; caliper likely under-read at the corner-radius tangent, see OQ-06 |
| M-003 | F-001 thickness, flat body (T) | 8.7 mm official; 3 independent caliper reads cluster 9.5–9.8 mm | D0_BACK to D6_SCREEN | SPEC-01/02 (B); IMG-09/10/12 direct caliper (A) | B (nominal) / A (conflicting) | conflict not silently resolved — see OQ-01; use 8.7 mm as provisional nominal, confirm with a flat-region (non-button) coupon re-measurement before finalizing wall clearance |
| M-004 | F-002 corner radius (R), all 4 corners | 9.5 mm ± 1.5 mm | horizontal projection of the arc vs. the embedded caliper-ruler scale in the same frame, top-left corner | IMG-07 calibrated crop | B | fdm-design.md corners are least-accurate — chamfer/relieve rather than chase a tight R |
| M-005 | F-003 camera-bar total height (top edge to flush transition on back) | 20.4 mm | D2_TOP, along −Y, direct caliper | IMG-13 | A | drives camera-relief length on the case back |
| M-006 | F-003 camera-bar metal-insert sub-height | 14.3 mm | D2_TOP, along −Y, direct caliper | IMG-17 | A | cosmetic sub-detail only; not needed for case fit |
| M-007 | F-003 camera-bump protrusion above D0_BACK | ≈2.74 mm (11.44 mm max device thickness at bump − 8.7 mm body) | arithmetic from SPEC-01 hands-on figure | SPEC-01 | B (derived, not directly calipered) | see OQ-02; needed to size the case's raised camera ring/lip height |
| M-008 | F-003 camera-bar width | full device width, edge-to-edge (≈ M-002) | visual, both back photos | IMG-04, IMG-16, IMG-17 | C | direct caliper attempt (IMG-15, 84.2 mm) excluded as unreliable — see OQ-03 |
| M-009 | F-004 lens-oval top margin below D2_TOP | 6.2 mm | D2_TOP, along −Y, direct caliper | IMG-14 | A | cosmetic; not case-fit-critical |
| M-010 | F-004 lens-oval approximate footprint | ≈30–36 mm wide × 6–8 mm tall | visual proportion, cross-checked against M-005/M-006/M-009 | IMG-04,14,16,17 | C | non-fit-critical, see F-004 response |
| M-011 | F-006 volume-rocker center / length | Y=+32 mm (range +24…+40), length ≈16 mm | D2_TOP along −Y, D4_RIGHT | IMG-02 | C | see OQ-04; bounded LOOSE window M-020 |
| M-012 | F-007 power-button center / length | Y=+50 mm (range +44…+58), length ≈10 mm | D2_TOP along −Y, D4_RIGHT | IMG-02 | C | see OQ-04; bounded LOOSE window M-020 |
| M-013 | F-008 SIM-tray center / length | Y=+35 mm (range +25…+45), length ≈13 mm | D2_TOP along −Y, D5_LEFT | IMG-03 | C | non-fit-critical |
| M-014 | F-009 top-mic offset from D5_LEFT corner | ≈10–18 mm | D2_TOP, along +X from D5_LEFT | IMG-05 | C | small relief or leave open |
| M-015 | F-010 USB-C center (X) | ≈0 mm (±2 mm) — visually centered | D3_BOT, X from D1_CTR | IMG-06 | B | LOOSE window M-021 |
| M-016 | F-010 USB-C width / height | ≈8–9 mm / ≈3 mm | D3_BOT | IMG-06 | C | LOOSE window M-021 |
| M-017 | F-011 bottom-left grille inset / width | ≈11 mm from D5_LEFT corner / ≈6 mm | D3_BOT | IMG-06 | C | LOOSE window or shared slot M-021 |
| M-018 | F-012 bottom-right grille inset / width | ≈12 mm from D4_RIGHT corner / ≈6 mm | D3_BOT | IMG-06 | C | LOOSE window or shared slot M-021 |

### Case-to-phone fit — bounded bands (fdm-design.md §4 fit classes; per-side, never a floor)

| ID | Applies to | Fit class | Band (min–max, per side) | Rationale |
|---|---|---:|---|---|
| M-019 | Body-envelope side walls (M-001×M-002×M-003 cavity around F-001) | snug–sliding | 0.10–0.30 mm/side | Captured, non-moving fit: must not rattle/wobble (over-clearance is a failure exactly like interference) but must still permit assembly insertion without stretching a rigid wall at the widest cross-section. Matches the skill's own worked example for a snug non-moving capture. |
| M-020 | Camera-bar relief around F-003 footprint (M-005/M-008) | loose | 0.30–0.50 mm/side | Must clear the bump and lens rim with guaranteed margin; a tight camera window risks rubbing/scratching the lens glass and misaligning against position uncertainty in M-007/M-008. |
| M-021 | Button windows around F-006/F-007 nominal positions | loose | 0.30–0.50 mm/side, applied to the full stated position RANGE (not just the point estimate) | Position confidence is C (±8 mm uncertainty per button, see OQ-04). Named robustness strategy: one elongated relief spanning the full plausible zone (≈ Y +22…+60 mm on D4_RIGHT) rather than two tight punctual holes, until a coupon or a ruler-referenced photo confirms exact centers. |
| M-022 | Port/grille windows around F-010/F-011/F-012 | loose | 0.30–0.50 mm/side, or one shared bottom slot spanning all three given position uncertainty | Same rationale as M-021; ports are functional but do not need precision cutouts. |

## Open questions
| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| OQ-01 | M-003 thickness conflict: 3 independent caliper reads (9.5/9.6/9.8 mm, IMG-09/10/12) all cluster ~0.8–1.1 mm above the 8.7 mm official spec, all taken at/near the right-edge button region | if real, case side-wall clearance budget is thinner than assumed; if a caliper-tilt/button-protrusion artifact, no risk | use 8.7 mm as provisional nominal (M-003); re-measure thickness at a plain flat region away from any button, jaws perpendicular, before finalizing wall clearance | wall-clearance sign-off for M-019 |
| OQ-02 | M-007 camera-bump protrusion (2.74 mm) is arithmetic from a third-party hands-on figure, not directly calipered on this unit | case camera-ring/lip height could be under- or over-sized | take a direct caliper step-height reading (flat back to top of camera-bar surface) on this unit | sizing the case's raised camera surround |
| OQ-03 | Two caliper photos did not reconcile to a known feature: IMG-15 (84.2 mm, width-adjacent, likely a non-zeroed jaw — expected ~73 mm) and IMG-11 (~20–27 mm, illegible middle digit, unclear jaw placement) | none currently (both excluded from the register) | if precision on camera-bar width or this unresolved ~20–27 mm feature matters, retake with the caliper explicitly zeroed and the jaw contact points photographed in-frame | none (excluded, not load-bearing) |
| OQ-04 | Button (F-006/F-007) and port/grille (F-009/F-011/F-012) Y/X positions are single-photo proportional estimates only (grade C, no ruler/caliper in that exact frame) | a tight, individually-cut window could miss the real button/port | approved bound: use the stated ranges with the LOOSE 0.30–0.50 mm/side bands and, for buttons, the single-elongated-window strategy (M-021) until confirmed | tight/individual cutout confidence only — does not block a generously bounded first pass |
| OQ-05 | M-004 corner radius (9.5±1.5 mm) comes from one calibrated crop of one corner only | the other 3 corners are assumed symmetric, unverified | approved bound: treat as symmetric per typical Pixel design language; chamfer/relieve per fdm-design.md rather than chase a tight R | none (design already tolerant of this uncertainty) |
| OQ-06 | M-002 width: direct caliper (71.9 mm) sits 1.3 mm under official spec (73.2 mm), larger than the 0.6 mm gap seen on length | jaw likely contacted the corner-radius tangent rather than the true widest straight-side cross-section, but not confirmed | use 73.2 mm (SPEC) as the width nominal; caliper reading corroborates "not narrower than ~72 mm" | none (resolved by using the larger, spec-corroborated value) |
| OQ-07 | Handedness (buttons-right / SIM-left) is inferred by cross-referencing 5 separate photos, no single frame shows front face + an edge together | low — matches standard phone convention and is internally consistent across all edge photos | none required; flagging for the round-trip pass to re-confirm against the reference render | none currently |
| OQ-08 | Screen-to-frame flush/lip relationship (F-013) is grade D — not clearly resolved from available photos | designer might wrongly assume some native screen protection exists | treat as flush / no native lip; case should add its own face lip (a design decision, out of scope here) | none (bounded conservatively) |

## Reference round trip
| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
| — | — | PENDING — out of scope for this commission (metrology-only step; no reference has been built) | n/a |

Round-trip verdict: PENDING. This step produced the datum-based sheet only. No CAD reference
model exists yet for this job folder (`tests/eval/step1-metrology-pixel7/`), so overlay
evidence and an ACCEPT/REVISE verdict cannot be produced now. When a designer builds the
mating reference blind from this sheet, the metrologist must render matching photo
viewpoints, overlay each fit-critical view, and record the verdict here before status can
move past DRAFT.
