---
contract: print-plan
contract_version: 1
job_id: pixel-10-case-team
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 3
reference_sha256: c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91
printer_profile: Bambu Lab X2D Combo / main 0.4 mm hardened nozzle / TPU 95A
updated_utc: 2026-07-24T12:30:00Z
---

# Print plan

## Process selection
- Printer: Bambu Lab X2D Combo, textured PEI plate, single-nozzle job.
- Effective build volume: 256 x 256 x 260 mm; use the main nozzle only, so the dual-nozzle envelope reduction does not apply. Candidate bbox must fit this envelope after the required orientation transform.
- Final material and reason: dry TPU 95A. It supplies the required compliant retention and drop protection; the user specified it and it is suitable for a one-piece phone case.
- Coupon material: the same dried TPU 95A from the same spool and main nozzle. PLA is not acceptable for the functional fit coupon because its stiffness, insertion force, and dimensional response cannot retire the TPU fit risk.
- Main/aux nozzle assignment: main nozzle only; TPU must be fed from an external spool, never through AMS 2 Pro. Auxiliary nozzle unused.
- Nozzle diameter: 0.4 mm hardened main nozzle.
- Layer-height assumption: 0.20 mm nominal; 0.16-0.20 mm is allowed only if the final slicer preview preserves all wall and lip floors in this contract. TPU speed target is 40-60 mm/s.

## Required print coordinate frame
- Bed-contact face/datum: the finished exterior rear-back face, parallel to D0_REAR, is the bed face; it is not a mating surface.
- Up axis after placement: installed model -Z (toward the phone screen/open front) is +Z of the printer.
- Orientation transform: rotate the installed-pose candidate 180 degrees about model X, then place the exterior rear-back face on the textured PEI plate; keep D1_XMID parallel to a plate axis.
- Load/layer rationale: continuous side walls and screen/camera lips grow upward without internal supports; repeated installation flexes the walls in their layer planes rather than peeling a support-scarred edge. The back panel is plate-supported and is not a load-bearing cantilever.
- Cosmetic rationale: all visible outer side walls and lips print unsupported. The exterior back receives the controlled textured-PEI finish; locate the seam on the lower-left exterior corner return, never in the cavity, camera opening, control relief, port opening, or screen lip.

## Geometry constraints
| Constraint ID | Requirement | Value/limit | Source/rationale | Verification method |
|---|---|---|---|---|
| P-001 | Functional walls | Nominal side and corner wall >= 1.6 mm (four 0.4 mm lines); no local functional wall < 1.2 mm (three lines). | 0.4 mm nozzle wall multiples; TPU case durability. | Re-imported STL wall/section audit. |
| P-002 | Back and charging region | Back wall is 1.2-2.0 mm normal to D0_REAR; no embedded magnet, metal, or local added geometry in F-014 charging region. | M-018 requires <= 2.0 mm; wireless charging needs a clear, thin back. | Re-imported STL thickness and material-body audit. |
| P-003 | Controlled body cavity | Nominal body-envelope clearance is 0.35 mm per side from M-001/M-002/M-003 surfaces; no intentional interference with the handset body. Candidate parameters must retain 0.25, 0.35, and 0.45 mm per-side coupon variants. | TPU deformation and ordinary FDM variation require a compliant, coupon-selected fit; clearance is per side. | Named-parameter/source audit and coupon measurements. |
| P-004 | Corners | Use compliant corner relief covering the full M-004 7-13 mm radius envelope plus the selected cavity clearance; do not create a rigid internal corner locator. | A-01 is C-grade and fit-critical. | STL section plus corner coupon insertion/removal test. |
| P-005 | Camera/flash opening | One shared, oversized rear opening; it must clear the full M-005/M-006 uncertainty envelope plus >= 0.5 mm per side, extend at least 3.0 mm toward D4_TOP beyond nominal as required by M-008, and accommodate M-009's 0.5-3.5 mm protrusion without contact. No tight individual camera or flash pockets. | A-02 and A-07 are bounded C-grade geometry. | Re-imported STL datum measurement, section, and real-device camera-lip coupon check. |
| P-006 | Controls | Right side is a continuous/open relief spanning Y = 42-122 mm; no tight individual button covers are authorized. | M-012/A-03. | Re-imported STL datum and insertion-sweep audit. |
| P-007 | Bottom and USB-C | Keep the bottom open around D2_BOTTOM: centred USB-C opening >= 18 mm wide, no solid bottom bridge outside protected corner returns, and no support-contact or seam in the opening. | M-014-M-016/A-04; preserves plug and acoustic clearance. | Re-imported STL bottom-view measurement and lower-band coupon test with the actual cable. |
| P-008 | Top microphone | Provide the temporary centred 8 mm top-edge relief at D1_XMID; no tight microphone hole is authorized. | M-017/A-05. | Re-imported STL top-view datum measurement; confirm against the physical phone before final print. |
| P-009 | Overhangs and transitions | All cavity, lip, camera, and port transitions must be self-supporting in the required orientation: <=45 degrees from vertical; unsupported bridges <=5 mm unless hidden and explicitly accepted. | FDM printability limits and zero-support functional-face policy. | Orientation-specific re-imported STL face/overhang and section audit. |
| P-010 | Bed-edge treatment | Add a 0.2-0.4 mm, 45-degree chamfer only to the exterior rear-back bed-contact perimeter; retain fit-critical cavity and rim dimensions clear of the first-layer perimeter. | Machine-independent elephant-foot immunity without altering the mating cavity. | Re-imported STL section and face audit. |
| P-011 | Screen/camera protective lips | Lip walls must be >=1.2 mm, continuous, and self-supporting in the planned orientation; no support scars on their exposed protective edges. | 0.4 mm nozzle minimum three-line durable lip; visible/functional face protection. | Re-imported STL section, wall, and support-face audit. |
| P-012 | Slicer independence | All clearances, openings, chamfers, and reinforcement above are CAD geometry; do not rely on slicer X-Y compensation, support painting, or elephant-foot compensation to establish function. | Portable fit and repeatable verification. | Source/3MF review and re-imported STL audit. |

## Supports and bridges
- Support budget: zero supports on the candidate; a support-dependent case is rejected for this plan revision.
- Allowed support regions: none.
- Forbidden support regions: entire phone cavity, screen lip, camera/flash opening and lip, right-control relief, USB-C/bottom opening, microphone reliefs, exterior cosmetic walls, and all bed-facing functional boundaries.
- Maximum unsupported bridge: 5 mm for a clean functional surface. A 5-25 mm span is permissible only when it is nonfunctional, hidden, and documented in the candidate evidence; no long bridge may define a fit edge.
- Designed-support requirement: if a candidate cannot meet P-009 without supports, it must be rejected and redesigned; do not add slicer or sacrificial supports to preserve fit geometry.

## Color/material plan
| Body/region | Material/color | Physical nozzle | Geometry requirement |
|---|---|---|---|
| Entire case, including lips and corner returns | single user-selected TPU 95A color | main 0.4 mm nozzle, external spool | one watertight CAD body; no colour split, embedded magnet, or secondary support material |

## Coupon contract
- Required before final print: yes; this is a mandatory gate. Print the coupon set from the exact selected candidate geometry, exported in TPU 95A, before the complete case.
- Actual mating region to extract: a two-piece coupon set, both cut directly from the selected final candidate with no simplified substitute: (A) a 30 mm-high lower band, D2_BOTTOM through Y=30 mm, containing the full actual back wall, both lower corner returns, both side walls, the real centred USB-C opening, and the adjacent speaker/microphone clearance; (B) a 30 mm-high right-side band centred at Y=82 mm, containing the actual D3_RIGHT wall, the continuous Y=42-122 control-relief geometry, back wall, and screen lip. Preserve final wall thicknesses, cavity clearances, chamfers, and local stiffness in both bands. Label each coupon body and its clearance value outside the mating surfaces.
- Variants/steps: manufacture A+B at 0.25, 0.35, and 0.45 mm per-side body-cavity clearance, with every other final parameter unchanged. The designer must expose this one clearance parameter and export a separately identifiable pair for each step; no one-off hand-edited coupon dimensions.
- Target duration: <=45 minutes total for the three paired TPU coupon variants at 0.20 mm layers and 40-60 mm/s, excluding warm-up; if this is exceeded, preserve the same mating cross-sections and reduce only nonfunctional coupon length.
- Pass/fail: select the lowest-clearance pair that (1) installs and removes by steady hand force without tools, tearing, whitening, or permanent deformation; (2) reaches its designed seated position with no corner lift; (3) leaves the USB-C opening clear for insertion of the intended charging plug without case contact; (4) leaves the complete Y=42-122 right control band free of binding; and (5) has no visible collision at the camera-lip envelope. Any failure is evidence: do not print the full case until the relevant dimensions, geometry, or plan owner resolves it.

## Post-verification prep placeholders
- Slicer profile: Bambu Studio X2D TPU 95A profile, main nozzle/external spool, 0.20 mm layers; create a print-ready project 3MF only after verification and round-trip it from a real Bambu Studio save.
- Walls/top-bottom/infill: start with four walls, five top/bottom layers where applicable, and 15-20% gyroid; final values require slice preview confirmation that P-001/P-002/P-011 are met without closing any required opening.
- Drying/preparation: dry TPU until extrusion is free of popping/stringing; run main-nozzle offset/flow checks with the dry spool, clean textured PEI, and use no AMS feed.
- Print order: TPU clearance coupon set -> document fit/plug/control/camera observations and select clearance -> final TPU case -> dimensional/visual inspection -> controlled installation on the confirmed base Pixel 10.
- Field-test protocol: after final verification and coupon pass, inspect every opening and lip, test charge-plug insertion/removal, button access, microphone/speaker clearance, wireless charging, ten gentle installation/removal cycles, then a controlled low-height corner-drop test over a non-damaging surface. Stop immediately for tearing, lip lift, port interference, button binding, camera-field obstruction, or charging failure; preserve photos, slicer settings, and measured stopping/contact locations for routing.
- Bambu after-import checks: confirm X2D preset and 0.4 mm main nozzle, TPU on external/main feed, textured PEI plate, required orientation, 0.20 mm layer height, wall count, top/bottom and infill, zero supports, seam location, brim only if it does not touch a functional face, and preview that all ports/reliefs remain open. Confirm no auxiliary/AMS assignment. Do not claim a generated 3MF accepted until it has been reopened and checked in Bambu Studio.

## Plan acceptance
- Blocking items: none for candidate design. The physical-unit variant (A-06), exact camera bar (A-02/A-07), and top-microphone position (A-05) remain final-print blockers that this coupon/real-device confirmation must retire; they do not authorize tight geometry before then. `job_state.md` names dimensions r4 in its dispatch/ledger, while the accepted on-disk dimensions contract header is r3; this plan binds the actual accepted file revision r3 and the stated ref-2 hash.
- Accepted by print engineer: plan-1, 2026-07-24.
