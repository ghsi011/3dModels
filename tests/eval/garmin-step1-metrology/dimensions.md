---
contract: dimensions
contract_version: 4
job_id: garmin-7x-charging-dock
revision: 1
owner: metrologist
status: DRAFT
updated_utc: 2026-07-24T21:30:00Z
---

# Dimensions

Scope note: this is step ① (metrology only) of a Garmin Fenix 7X charging dock/cradle
commission. No CAD, no reference build, and no round trip has been commissioned yet.
`Reference round trip` below is therefore `PENDING` by construction, not a finding.

## Frame

Right-handed. Origin: case center at the caseback plane (D0 ∩ D1). All 11 supplied photos
are top-down flat-lay shots with the band running horizontally in-frame; that photographed
band direction is used to define +Y below (it is not independently confirmed to be the
watch's cosmetic "12 o'clock", which does not affect a cradle's physical clearance needs).

| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|
| D0_CASEBACK | Flat rear plane of the case (Z=0); the surface that seats against a cradle pocket floor / charging puck | Inferred from case silhouette in all top-down photos; NOT independently confirmed by a side-profile photo | D |
| D1_AXIS (+Z) | Vertical axis through case center, perpendicular to D0_CASEBACK; +Z points from caseback toward the display crystal | Round bezel clearly visible/centered in every top-down photo (IMG-01..11) | A |
| D2_BUTTON_AXIS (+X) | In-plane axis through case center; +X toward the side-button/pusher-populated side of the bezel | Directly visible in caliper photos IMG-02, IMG-03, IMG-06 (button/pusher labels legible on bezel) | A |
| D3_BAND_AXIS (+Y) | In-plane axis through case center; +Y toward the open/perforated strap-tip end of the band, away from the buckle | Directly visible, IMG-01 overview | A |

## Sources

| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|
| IMG-01 | tests/garmin 7x stand/PXL_20260724_164312168.jpg | user's unit | photographed 2026-07-24 | overview, flat-lay, no caliper |
| IMG-02 | tests/garmin 7x stand/PXL_20260724_164329390.jpg | user's unit | photographed 2026-07-24 | caliper 56.8mm, near-feature (button axis, tip contact) |
| IMG-03 | tests/garmin 7x stand/PXL_20260724_164340814.jpg | user's unit | photographed 2026-07-24 | caliper 51.7mm, flat-bezel (button axis, flank contact) |
| IMG-04 | tests/garmin 7x stand/PXL_20260724_164405752.jpg | user's unit | photographed 2026-07-24 | caliper 92.8mm; jaw contact points not clearly resolvable in a 2D crop, ambiguous |
| IMG-05 | tests/garmin 7x stand/PXL_20260724_164421312.jpg | user's unit | photographed 2026-07-24 | caliper 111.4mm; jaws visually open in free air over the band, contact unclear |
| IMG-06 | tests/garmin 7x stand/PXL_20260724_164429315.jpg | user's unit | photographed 2026-07-24 | caliper 111.4mm (portrait re-shot of IMG-05's setup); same ambiguity |
| IMG-07 | tests/garmin 7x stand/PXL_20260724_164443613.jpg | user's unit | photographed 2026-07-24 | caliper 51.8mm, flat-bezel (button axis, flank contact) — confirms IMG-03 |
| IMG-08 | tests/garmin 7x stand/PXL_20260724_164457170.jpg | user's unit | photographed 2026-07-24 | caliper 26.0mm, band width at strap body |
| IMG-09 | tests/garmin 7x stand/PXL_20260724_164507881.jpg | user's unit | photographed 2026-07-24 | caliper 31.4mm, buckle/keeper frame width |
| IMG-10 | tests/garmin 7x stand/PXL_20260724_164555154.jpg | user's unit | photographed 2026-07-24 | caliper 142.3mm, strap-tip to strap-tip (buckle loop closed), clear jaw contact both ends |
| IMG-11 | tests/garmin 7x stand/PXL_20260724_164608666.jpg | user's unit | photographed 2026-07-24 | caliper 115.3mm; jaws visually open in free air, contact unclear |
| S-12 | https://www.gpscentral.ca/wp-content/uploads/Garmin_fenix7X_Series_Specifications.pdf (and garmin.com product page) | Fenix 7X family | accessed 2026-07-24 | official: case 51mm dia x 14.9mm thick |
| S-13 | https://www.garmin.com/en-US/p/560287/ (QuickFit 26 band product page) | Fenix 7X family (51mm models use QuickFit 26) | accessed 2026-07-24 | official: 26mm band width confirmed |
| S-14 | general web search on Garmin proprietary charging-clip contacts (no single authoritative spec page found with pin pattern/spacing) | Fenix/Instinct product family, not 7X-specific drawing | accessed 2026-07-24 | confirms "4 gold-plated pins," does NOT give geometry/spacing/offset — product-family knowledge only, not a measured or drawn spec |

Annotated crops (derived evidence, originals untouched) are in
`evidence/metrology/`: `annot_overview.jpg`, `annot_56_8mm_button_axis.jpg`,
`annot_51_7mm_flat_bezel.jpg`, `annot_51_8mm_flat_bezel.jpg`,
`annot_26_0mm_band_width.jpg`, `annot_31_4mm_buckle.jpg`. Several source photos were
captured upside-down relative to their caliper display; 180°-rotated legibility copies used
only to read digits are not separately retained as evidence beyond the annotated crops above.

## Blind-build completeness

| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|
| F-001 | CASE_BODY — round case/bezel, 1, primary mating envelope | Ø51.75mm (D2_BUTTON_AXIS, flat-bezel region) x Ø51.75mm (D3_BAND_AXIS, assumed by round symmetry) x 14.9mm thick (D0→crystel apex along D1) | IMG-02/03/07 caliper + S-12 | A (button-axis dia) / C (band-axis dia, unmeasured) / B (thickness, spec-only) | cradle pocket bore ≈Ø51.75mm + fit band (see Dimensions); pocket depth ≥14.9mm + vertical clearance | Ready, with OQ-02/OQ-04 caveats |
| F-002 | BUTTON_PUSHER — side buttons/pushers, 5 per known Fenix 7X layout, keep-out along button axis | protrusion envelope Ø56.8mm tip-to-tip on D2_BUTTON_AXIS; ≈2.5mm radial protrusion per side beyond F-001's flat bezel (derived) | IMG-02 caliper (envelope) + product-family knowledge (5-button count/layout, individual button positions not re-measured) | A (protrusion envelope) / C (button count/layout) | if a cradle sidewall rises to button height, relieve/notch to ≥Ø56.8mm + clearance ONLY along D2_BUTTON_AXIS; a wall that stays below button height needs no relief | Ready (bounded) |
| F-003 | CASEBACK_CHARGE_PAD — proprietary 4-pin flat contact pad, 1, THE fit-critical charging interface | UNKNOWN exact location, offset from D1_AXIS, pin spacing/pattern, and OEM cable clip engagement geometry | S-14 (product-family knowledge only) — **no photo of the caseback exists in the supplied 11-photo set** | D, unconfirmed for this unit | none possible yet — see OQ-01 | **NOT READY — blocking for the charge-interface feature specifically** |
| F-004 | BAND_STRAP — QuickFit 26 silicone band, 2 pieces (buckle-side + tip-side) | width 26.0mm at strap body; exits case at the two D3_BAND_AXIS lugs | IMG-08 caliper + S-13 | A | if the cradle captures the watch WITH band attached, leave a channel ≥26mm + clearance wherever the band crosses cradle material; a case-only cradle needs no response | Ready |
| F-005 | BAND_BUCKLE — pin buckle/keeper hardware, 1, cosmetic | width 31.4mm, located at the strap tail beyond one lug | IMG-09 caliper | A | none required unless cradle geometry extends far enough along D3_BAND_AXIS to intersect typical worn buckle position | Ready (non-blocking) |
| F-006 | QUICKFIT_LUG — quick-release lever/collar, 2 (one at each D3_BAND_AXIS lug) | visible as a distinct rubber collar with a small triangular release tab next to the case; exact protrusion/offset not independently calipered | IMG-01 (visual only) | C | if a cradle wall approaches the lugs, leave clearance; bounded assumption: collar footprint stays within the 26mm band-width envelope, no extra radial protrusion, until contradicted by a closer photo | Ready (bounded, low confidence) |
| F-007 | DISPLAY_CRYSTAL — front lens/crystal, 1, cosmetic | round, effectively the case's inner bezel opening; not separately measured | IMG-01 (visual only) | C | none — a cradle normally does not contact the crystal | Ready |
| F-008 | CASE_LOGO/BEZEL_MARKINGS — "GARMIN" wordmark + bezel index ticks, cosmetic | visible on band and bezel, no functional role | IMG-01 through IMG-11 | C | none | Ready |

## Dimensions

| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|
| M-001 | F-001 case body diameter, button axis, flat-bezel region | 51.75 mm (mean of 51.7 / 51.8) | across D2_BUTTON_AXIS through case center, jaws on the flat bezel flank, NOT on a button tip | IMG-03 (51.7mm) + IMG-07 (51.8mm), two independent direct-caliper reads | A | primary cradle-pocket bore driver; see fit band below |
| M-002 | F-002 button/crown protrusion envelope, button axis, tip-to-tip | 56.8 mm | across D2_BUTTON_AXIS, jaws on button/pusher tips — explicitly a **near-feature read**, biased high vs. M-001 per skill rule (b) | IMG-02 direct caliper | A (as a protrusion-envelope reading; NOT usable as the case-body envelope) | only relevant if cradle wall height reaches the buttons (see F-002 candidate response) |
| M-003 | F-001 case body diameter, band axis | 51.75 mm (assumed = M-001) | across D3_BAND_AXIS through case center | not independently caliper-measured; assumed from the visibly circular bezel in every top-down photo (IMG-01) plus S-12's single "51mm" round-case spec | C | wider working tolerance ±0.5mm until confirmed; see OQ-04 |
| M-004 | F-001 case thickness (Z) | 14.9 mm | D0_CASEBACK to crystal apex along D1_AXIS | official spec S-12 only — no side-profile photo/caliper exists in this set | B | drives cradle-pocket depth / vertical clearance; see OQ-02 |
| M-005 | F-004 band width, strap body | 26.0 mm | across strap width, mid-span vented section | IMG-08 direct caliper | A, corroborated by official QuickFit-26 spec S-13 | non-fit-critical unless band stays attached inside the cradle |
| M-006 | F-005 buckle/keeper frame width | 31.4 mm | across buckle outer frame | IMG-09 direct caliper | A | informational/cosmetic only |
| M-007 | F-004 band overall extended length, one piece (tip side), case edge to strap tip | ≈111–115 mm (111.4mm ×2 reads, 115.3mm ×1 read) | approx. along D3_BAND_AXIS from case edge to strap tip | IMG-05, IMG-06, IMG-11 — caliper jaws visibly open in free air relative to the 2D photo frame; exact contact points NOT confirmable | C, low confidence | informational only, NOT fit-critical; excluded from the cradle envelope; see OQ-03 |
| M-008 | F-004+F-005 total watch length laid flat, buckle loop closed, to opposite strap tip | 142.3 mm | strap tip to strap tip, along D3_BAND_AXIS, through the case | IMG-10 direct caliper, both jaw contacts clearly visible | A | informational only, NOT fit-critical |
| M-009 | F-003 charge-contact pad location, pattern, pin spacing, offset from D1_AXIS | **UNKNOWN** | would be measured from D0_CASEBACK / D1_AXIS if a caseback photo existed | S-14 product-family knowledge only ("4 gold-plated pins" — generic across several Garmin lines) | D, unconfirmed for this exact unit | **BLOCKING** — see OQ-01. Do not assign a numeric offset/pattern to CAD without new evidence or explicit user approval of a bounded placeholder |

## Derived dimensions

| Dim ID | Formula | Inputs | Result | Confidence rule |
|---|---|---|---:|---|
| D-001 | (M-002 − M-001) / 2 | M-002, M-003 | 2.53 mm | button/pusher radial protrusion beyond the flat bezel, each side; inherits the lower of its two inputs' confidence (A and A, but is itself a difference of two approximate reads, so treat resulting figure as ±0.3mm, informative for a keep-out relief only) |

## Fit specification — watch case to cradle pocket (bounded band, not a floor)

Per `fdm-design.md` §4 and the skill's explicit guidance for "a snug non-moving capture
around a known feature": this is exactly that case — the cradle must hold a round, known-
diameter case (M-001, Ø51.75mm on the measured axis; M-003, Ø51.75mm assumed on the
unmeasured axis) firmly enough that the caseback stays flush and rotationally stable against
whatever holds the charging contacts, without becoming a press fit that resists daily
insertion/removal.

- **Fit class: snug–sliding**, per `fdm-design.md` §4 (snug 0.1–0.2mm/side, sliding
  0.15–0.3mm/side).
- **Radial clearance band, cradle pocket wall to case body (M-001/M-003, Ø51.75mm
  nominal): min 0.10 mm/side, max 0.30 mm/side** (diametral 0.20–0.60mm). Below 0.10mm/side
  risks a press fit against a case that is only Grade-A/C measured, not toleranced by Garmin;
  above 0.30mm/side risks rattle/wobble that can misalign the charge contacts — over-
  clearance is a failure mode here exactly as interference is, per the skill's explicit rule.
- Material note (for the later print-engineer pass, not decided here): PETG/ABS printed
  cradles want +0.05mm over a PLA-tuned value per `fdm-design.md` §4; this band is the
  geometric target before that per-material adjustment.
- **Rotational index**: the case is round and otherwise symmetric in the confirmed evidence,
  so the pocket alone cannot guarantee the charge pad (F-003, non-axisymmetric) lands under
  the puck contacts. The only independently photo-confirmed clocking features are
  D2_BUTTON_AXIS (F-002) and the two D3_BAND_AXIS lugs (F-006/F-004). A future designer will
  need one of these as a keying feature — this sheet does not select one, since doing so
  requires knowing where F-003 sits relative to them, which is exactly OQ-01.
- **Charge-contact alignment tolerance — NOT SPECIFIED.** The band above bounds how much the
  case body itself can shift inside the pocket; it is not a substitute for the actual
  pogo-pin engagement tolerance (pin travel/compliance, pad size, keep-out around the pad),
  which is unknown (M-009/OQ-01). Do not assume pin spring travel silently absorbs cradle
  slop beyond the stated 0.10–0.30mm/side band.

## Open questions

| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|
| OQ-01 | F-003/M-009: exact charge-contact pad location, pattern, pin spacing, and OEM charging-cable clip engagement geometry | HIGH — this is the commission's stated fit-critical feature; the puck must seat on the contacts | Need one of: (a) a photo of the watch caseback with the pin pad visible, ideally with a caliper on it; (b) a photo/measurement of the OEM charging cable's contact clip and its retention "wings"; (c) explicit user sign-off on a stated bounded placeholder pad location/size if no such photo can be obtained | Blocks reference/candidate CAD of the charging-interface feature specifically. Case body/band envelope (F-001, F-004–F-008) is not blocked by this |
| OQ-02 | M-004: case thickness (14.9mm) has zero photographic corroboration | MEDIUM — drives cradle pocket depth/vertical clearance | No side-profile photo/caliper exists; relying solely on official spec S-12 | Does not block — S-12 is an authoritative, well-documented figure for a known, confirmed model — but flagged; one side-profile caliper photo would upgrade M-004 from B to A |
| OQ-03 | M-007: ambiguous band-length caliper reads (111.4mm ×2, 115.3mm) | LOW — band length is not fit-critical for a case-focused cradle | Caliper jaw contact points are not clearly resolvable in the supplied 2D photos (jaws appear open in free air relative to the band/case) | Does not block; excluded from the fit-critical dimension set, recorded as informational only |
| OQ-04 | M-003: case diameter along the band axis was never independently caliper-measured | LOW-MEDIUM | Assumed equal to the button-axis reading (51.75mm) by visible round-case symmetry | Does not block (case is visibly circular in every overview photo) but recommend one more caliper photo, jaws only on the bare case across the band axis, to upgrade C→A |
| OQ-05 | Cradle seating/display angle | LOW, informational | None of the 11 photos show the watch mounted or propped at any angle — all are flat-lay | Not evidenced by this photo set; any angle is a downstream design decision, not a metrology fact. Flagging explicitly so a later designer does not assume a photographed angle exists |
| OQ-06 | Commission brief mentioned "case ≈47mm diameter" as background product knowledge; this conflicts with M-001 (51.75mm caliper) and S-12 (51mm official spec) | MEDIUM, resolved in this sheet | Two independent higher-confidence sources (Grade A direct caliper on this exact unit, Grade B official spec sheet) agree closely at ≈51–51.8mm and disagree with the brief's ≈47mm figure. This sheet uses 51.75mm and treats the brief's figure as an imprecise placeholder, not measured evidence. Orchestrator subsequently corrected the same figure independently (47mm is the plain Fenix 7's smallest case variant, not the 7X) and directed that the caliper reading is ground truth. A ≈51–52mm case reading is consistent with a Fenix **7X**; a ≈47mm reading would instead indicate a plain Fenix 7 (42/47mm variants) and would need to be flagged back explicitly — this unit's calipers (51.7/51.8mm) and the user's own product identification both point to 7X, not plain 7 | Does not block; recorded for traceability per the skill's "never silently average conflicts" rule — the conflict is resolved by evidence rank (caliper + official spec over the approximate brief note), not averaged |

## Required reference views

| View ID | Photo | Camera/view cue | Features that must align |
|---|---|---|---|
| V-TOP | IMG-01 | top-down, band horizontal, display face up | F-001 case silhouette, F-004 band width/exit, F-005 buckle, F-006 lug collars |
| V-BUTTON-AXIS | IMG-03 / IMG-07 | top-down, case only, button axis vertical in frame | F-001 flat-bezel diameter (M-001), F-002 button protrusion envelope (M-002) |
| V-CASEBACK | none supplied — **required before F-003 can be referenced** | flip watch over, caseback facing camera, ideally with a caliper on the pin pad | F-003 charge-contact pad location/pattern |

## Blind reference round trip

- Reference commission: none dispatched — out of scope for this step per commission
  ("This is a metrology-only commission (step ①)").
- Reference artifact SHA-256: n/a
- Sheet revision built: n/a
- Overlay evidence: n/a
| Feature ID | Observation against photo | Result | Sheet action |
|---|---|---|---|
| n/a | not yet dispatched | n/a | n/a |
- Round-trip verdict: PENDING
- Accepted by metrologist: not applicable at this step — sheet is DRAFT, not ACCEPTED
