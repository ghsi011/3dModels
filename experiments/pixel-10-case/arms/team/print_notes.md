# Pixel 10 TPU case — designer notes (cq-a)

## Geometry and parameters

- Source: `model.py`, CadQuery candidate `cq-a`; contracts: dimensions r3, print plan r1, ref-2 fixture.
- Cavity clearance is the single `CAVITY_CLEARANCE_MM` parameter: 0.35 mm per side nominal, with 0.25/0.35/0.45 mm retained for the required paired TPU coupons.
- Nominal functional side/corner wall is 1.6 mm; back wall is 1.4 mm and contains no embedded geometry over the charging region.
- The camera/flash field is one shared 66.5 x 28.0 mm capsule opening. Its top edge is Y=142.3 mm, which reaches 3.5 mm above the nominal M-008 camera-island top; the 1.2 mm rim rises to Z=4.8 mm to clear the bounded island maximum.
- The right side has no button covers: it is continuously open from Y=42 to 122 mm. The bottom uses a 58 mm broad opening, leaving only corner returns. The centred top relief is 8 mm wide.

## Orientation and DFM risks

- Exported STL/STEP use print-plan orientation: installed pose rotated 180 degrees about X, exterior rear-back face on the bed, screen opening upward.
- The only bed-contact treatment is the 0.3 mm exterior rear perimeter chamfer. No supports are designed or expected.
- Primary physical uncertainty remains the actual phone's camera bar and top microphone. Do not treat this candidate as ready for full print until the mandated TPU coupon set confirms them.

## Coupon handoff

- Extract both plan-defined bands directly from this exact final geometry at `CAVITY_CLEARANCE_MM` values 0.25, 0.35, and 0.45 mm; do not hand-edit their mating features.
- Coupon acceptance and slicer/field-test instructions remain print-engineer-owned.

## cq-a-r2 correction

- CQ-A-V1-001 removed the continuous screen-side plate by extending the controlled cavity through the screen plane. The 1.6 mm perimeter remains the bounded continuous protective lip; it is not a functional roof.
- Fresh exports and correction-only evidence are in `evidence/candidates/cq-a-r2/`. A fresh independent verification remains required.

## cq-a-r3 correction

- CQ-A-R2-V1-001 makes the rear exterior plane and camera-opening rim coplanar at the 1.75 mm rear-back datum. The supplied print transform therefore places the actual rear-back face at Z=0 instead of suspending it below a raised camera rim.
- Fresh exports and correction evidence are in `evidence/candidates/cq-a-r3/`. A fresh independent verification remains required.

# Print-engineer final preparation (prep-1)

## Bound inputs and coupon artifacts

- Verification gate: `verification_report.md` r3, PASS, candidate `cq-a-r3`; final case STL SHA-256 is `71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44`.
- Print-plan gate: `print_plan.md` r1, TPU 95A, Bambu Lab X2D Combo main 0.4 mm nozzle, 0.20 mm layers, zero supports.
- Coupon generator: `pixel10_case_fit_coupon.py`, SHA-256 `370d3d1f407e18983d3709ccbae5416d155a72c6e88d913a47129ee9b2061898`.
- Coupon exports and re-import evidence: `fit_coupon_manifest.md`. Print each lower/right-control pair at 0.25, 0.35, and 0.45 mm per-side clearance before the full case. The right-control strip deliberately retains the full 80 mm Y=42-122 relief; an 80 mm functional relief cannot be represented by a 30 mm slice.

## X2D TPU 95A slicing and preparation

- Filament/nozzle: one dry TPU 95A spool on the external feed into the X2D main 0.4 mm hardened nozzle. Do not use AMS 2 Pro or the auxiliary nozzle for TPU.
- Drying: dry the spool at 55 C for 6 hours immediately before the coupon set and keep it dry during the print. Reject a wet spool showing popping, bubbles, unstable stringing, or ooze on the calibration pad.
- Machine preparation: clean the textured PEI with the plate-safe method, load the dry external spool, and run the X2D main-nozzle offset/flow calibration. Use the X2D TPU-95A material preset as the base; set 230 C nozzle, 35 C bed, no active chamber heat, 20 mm/s first layer, 40 mm/s outer wall, 50 mm/s inner wall/infill, and 0.20 mm layers.
- Process: 0.40 mm line width; 4 walls; 5 top and 5 bottom layers where the geometry has horizontal skin; 15% gyroid infill; normal TPU cooling from the material preset; seam fixed to the lower-left exterior corner return. Do not enable X-Y size compensation, hole compensation, support painting, or elephant-foot compensation for functional geometry.
- Orientation: preserve the verified STL orientation exactly: exterior rear-back face on textured PEI, screen opening upward, D1_XMID parallel to a plate axis. The 0.3 mm exterior rear-perimeter chamfer is already in the mesh.
- Supports and brim: supports disabled. Start with no brim. If a coupon shows edge lift, use a 3 mm outside-only brim on the exterior rear-back perimeter, then recheck that it cannot touch a cavity, port opening, control relief, camera opening, or lip. Do not use a raft.
- Bambu Studio check: import the STL, confirm the X2D/0.4-main TPU profile, external/main filament assignment, textured PEI, stated orientation, walls/top-bottom/infill, zero supports, seam location, and all open features in layer preview. Save the real Studio project, reopen it, and reconfirm these settings before starting any print; no generated 3MF is claimed as Studio-accepted yet.

## Coupon-first procedure and acceptance

1. Slice and print the 0.45 mm pair first, then 0.35 mm, then 0.25 mm, all from the same prepared spool and settings. Mark each physical coupon on the exterior back with its clearance and region name.
2. For each lower band, install over the real confirmed base Pixel 10 with steady hand force only. Record whether both lower corners seat, whether the 58 mm bottom opening clears the intended USB-C plug, and any lift, whitening, tearing, permanent deformation, or contact point.
3. For each right-control strip, align it at the real right-side control region and verify the complete relief remains open, does not rub controls, and has no residual stringing or brim at the relief edge.
4. Select the lowest clearance whose paired coupons install/remove without tools, damage, or corner lift and leave the plug/control regions clear. A coupon that binds, tears, deforms permanently, blocks the plug, or contacts a control is a failure; stop before the complete case.
5. Before the final case, hold the shared camera-opening/lip region against the actual phone and confirm no camera/flash obstruction or camera-bar collision. Confirm the physical unit is the base three-camera Pixel 10 and locate the top microphone relative to the centred 8 mm relief.

## Full-case print, inspection, and field test

- Print order: coupon pairs -> record selected clearance and observations -> one final TPU case -> inspection -> controlled phone installation.
- Final-print inspection: compare final STL hash to the bound hash above before slicing; inspect the plate-facing rear back, 1.2 mm lips, shared camera opening, 58 mm lower opening, Y=42-122 right relief, 8 mm top relief, and all seam locations. Reject any support material, closed opening, lip tear, warped corner, or string trapped on a functional edge.
- Functional test: install once without tools; verify USB-C insertion/removal, button access, microphone/speaker clearance, camera/flash field, and wireless charging. Then perform ten gentle install/remove cycles and a controlled low-height corner-drop test over a non-damaging surface. Stop for tearing, permanent set, lip lift, port interference, control binding, camera obstruction, or charging failure.

## Rollback and remaining risks

- Preserve failure photos, the Studio project/settings, material/drying information, the selected coupon, clearance label, and exact stopping/contact location. Route a mismatch with the physical camera bar, microphone, ports, corners, or variant to `dimensions.md`; route a clean geometry that fails only through flow, shrink, adhesion, stringing, or seam process to this print-engineering handoff; route a clearance-specific candidate mismatch to the candidate geometry owner for a parameter revision and fresh verification.
- Remaining C-grade final-print gates: exact base-Pixel-10 production variant (A-06), camera-bar/aperture location and protrusion (A-02/A-07), corner radius (A-01), individual bottom-feature geometry (A-04), and top-microphone location (A-05). Coupon/physical-device confirmation is mandatory; the verification PASS does not waive these gates.
