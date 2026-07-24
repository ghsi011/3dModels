# Method — Garmin Fenix 7X charging dock, step ① metrology

Scope: this document explains provenance for every number in `dimensions.md` — which of
the 11 supplied photos it came from, whether it is a direct caliper read, an official-spec
figure, or an image-derived/assumed value — and records conflicts and open questions.
Inputs used: only `tests/garmin 7x stand/*.jpg` (11 photos) plus targeted web searches for
official Garmin Fenix 7X specifications, per the commission's allowed-inputs list. The held-
out `Fenix+7x+charging+dock.3mf` was not opened.

## Photo inventory and orientation note

All 11 photos are top-down flat-lay shots on a red cloth background, taken in one session
(watch clock visible, advancing from 19:43 to 19:46 across the sequence — consistent
ordering). Several caliper photos were shot with the phone rotated 180° relative to the
caliper's own upright text/display; those digits were only legible after generating a
180°-rotated working copy (script-based, in the session scratchpad, not committed) purely
to read the LCD — the underlying measurement is unchanged, only legibility. Affected files:
`PXL_20260724_164405752.jpg`, `PXL_20260724_164443613.jpg`, `PXL_20260724_164457170.jpg`,
`PXL_20260724_164507881.jpg`, `PXL_20260724_164555154.jpg`.

## Per-number provenance

| Value used in dimensions.md | Photo file | Read directly or after rotation | What the caliper is contacting |
|---|---|---|---|
| 56.8 mm (M-002) | PXL_20260724_164329390.jpg | direct | jaws bracket the case across the button/pusher axis, touching pusher/crown tips on at least one side — a **near-feature read**, explicitly flagged per the skill's rule (b), not used as the case-body envelope |
| 51.7 mm (M-001 component) | PXL_20260724_164340814.jpg | direct | jaws pinched by hand directly onto the flat bezel flank, same axis as the 56.8mm shot but contacting bezel material, not a button tip |
| 51.8 mm (M-001 component) | PXL_20260724_164443613.jpg | after 180° rotation | same setup/axis as the 51.7mm shot, independent repeat — used to corroborate M-001 as an averaged, twice-measured flat-bezel diameter (51.75mm) |
| 26.0 mm (M-005) | PXL_20260724_164457170.jpg | after 180° rotation | jaws across the width of the perforated/vented strap body, mid-span |
| 31.4 mm (M-006) | PXL_20260724_164507881.jpg | after 180° rotation | jaws around the outer frame of the pin buckle/keeper hardware at the strap tail |
| 142.3 mm (M-008) | PXL_20260724_164555154.jpg | after 180° rotation | jaws span from the closed buckle loop on one strap piece to the tip of the opposite strap piece — the only one of the "long" readings where both jaw contact points are clearly visible in the photo |
| 92.8 mm | PXL_20260724_164405752.jpg | after 180° rotation | **not used** — jaws are visibly open in free air relative to the watch/band in the 2D frame; no confident contact pair identified. Excluded from the dimension register entirely (not even carried as low-confidence, unlike the 111.4/115.3mm group, because there was no repeat shot to anchor it against) |
| 111.4 mm ×2 (M-007 component) | PXL_20260724_164421312.jpg, PXL_20260724_164429315.jpg | direct (both) | two shots (one landscape, one portrait) of what appears to be the same setup, same reading both times — jaws appear to bracket the band along its long axis, but the exact contact points (case edge vs. lug vs. somewhere on the strap) are not resolvable in a flat 2D photo. Carried as low-confidence (C), informational only |
| 115.3 mm | PXL_20260724_164608666.jpg | direct | same style of shot as the 111.4mm pair (jaws open in free air relative to the 2D frame), taken later in the sequence (watch clock reads 19:46 vs 19:44 for the 111.4mm pair) — grouped with M-007 as informational, not treated as a third confirmation of 111.4mm since it differs by ~4mm and the contact point is equally unclear |
| 51 mm case diameter, 14.9 mm thickness | none — official spec | web search | Garmin's official Fenix 7X series specification sheet (gpscentral.ca PDF mirror of Garmin's published spec) and garmin.com product page; cross-checked, both agree |
| 26 mm QuickFit band | none — official spec | web search | Garmin's official QuickFit 26 band product page confirms the 51mm Fenix 7X uses the QuickFit 26 band family — corroborates the 26.0mm caliper read exactly |
| "4 gold-plated pins" charging contacts | none | web search | third-party retail listings for Garmin-compatible charging cables mention "4-pin gold-plated contacts"; this is generic across several Garmin watch lines, not a Fenix-7X-specific drawing, and gives no pin spacing, pad size, or offset from the case center. No source found with the actual contact-pad geometry |
| Case-diameter / envelope, remaining derived numbers | — | arithmetic | see `dimensions.md` Derived dimensions (D-001) for the button-protrusion calculation; M-003 (band-axis diameter) is an explicit assumption from visible round-case symmetry, not a separate photo reading |

## Conflicts found and how they were resolved

1. **Commission brief's "case ≈47mm diameter" vs. measured/spec ≈51–51.8mm.** The
   commission text supplied "case ≈47 mm diameter" as background product knowledge for a
   known product. Two independent caliper reads on the user's actual unit (51.7mm and
   51.8mm, on the flat bezel, button axis) and Garmin's own published spec (51mm) agree
   closely with each other and disagree with the brief's figure. Per the skill's explicit
   rule ("never silently average conflicts"), this sheet does **not** split the difference
   — it uses the caliper-confirmed 51.75mm and records the brief's figure as an unconfirmed
   placeholder in `dimensions.md` open question OQ-06. Mid-task, the orchestrator sent a
   correction confirming the same conclusion independently: ~47mm belongs to the plain
   Fenix 7 (42/47mm case variants), not the 7X, and directed that caliper evidence be
   treated as ground truth. This is consistent with what the measurements already showed;
   no numbers changed as a result, only OQ-06's wording was strengthened to note the
   variant-identification implication (a ~51–52mm case reading is consistent with 7X; a
   ~47mm reading would instead flag a plain Fenix 7 and would need to be reported back).
2. **Near-feature vs. flat-region bezel reads (56.8mm vs. 51.7/51.8mm).** Both are on the
   same physical axis (button/pusher axis) and both are genuine direct caliper reads — this
   is not a measurement error, it is two different features on the same line. Per the
   skill's rule (b), the flat-bezel reads (51.7/51.8mm, repeated and mutually consistent)
   are treated as the case-body envelope; the wider read (56.8mm) is kept as its own
   dimension (M-002) describing the button/pusher protrusion envelope, not folded into or
   averaged with the case diameter.
3. **Three ambiguous long readings (92.8, 111.4×2, 115.3mm).** These did not conflict with
   each other in a way that could be resolved — they simply lack confirmable jaw-contact
   points in a 2D photo, unlike the case-diameter and band-width reads, which show the jaws
   pinched directly onto identifiable material. Rather than guess a contact pair to force a
   confident number, they are carried at low confidence (C) or, for the 92.8mm outlier,
   excluded outright. None of the three matter for a case-focused charging cradle (band
   length is not fit-critical to a cradle that captures the case body).

## Open questions (see `dimensions.md` for the full table)

The single blocking gap for this commission's stated fit-critical feature: **no photo in
the supplied set shows the watch caseback.** All 11 photos are top-down shots of the front
face/band. The charging contact pad, its pin pattern/spacing, its offset from the case
center, and the OEM charging cable's retention-clip geometry are therefore entirely
undocumented by photographic evidence — only generic "4-pin" product-family knowledge could
be found by web search, with no spacing or pad-size figures. This is recorded as OQ-01 and
marked `NOT READY` in the blind-build completeness table for feature F-003 specifically; it
does not block the case-body/band envelope (F-001, F-004–F-008), which is otherwise Ready.

Secondary, non-blocking gaps: case thickness (14.9mm) has zero photographic corroboration
(OQ-02, spec-only); the case diameter along the band axis was never independently
calipered and is assumed equal to the button-axis reading by visible round-case symmetry
(OQ-04); and no photo shows the watch mounted at any angle, so a cradle "seating angle" is
not evidenced by this photo set at all (OQ-05) — any angle is a downstream design choice,
not a metrology fact.

## Visual inspection performed

Every one of the 11 photos was opened and inspected at native/near-native resolution (not
just described from a thumbnail), including generating and inspecting 180°-rotated
legibility copies for the five caliper photos that were shot upside-down. Six annotated
crops were produced and visually re-checked against their source photos to confirm the
markers land on the actual jaw-contact region before being cited in `dimensions.md`; they
are stored in `evidence/metrology/`. No round-trip overlay work applies at this step
(no reference model has been built yet).
