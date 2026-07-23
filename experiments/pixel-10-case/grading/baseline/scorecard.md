# Pixel 10 frozen-arm independent scorecard

## Result

**Winner: team, 91/100, versus monolith 62/100.** Both final arms pass the hard export/installability gate, so neither is capped. The team arm wins because it converts the uncertain device evidence into named, bounded datums; gives the camera and screen continuous protective lips; supplies exact-geometry TPU coupons; and leaves a fresh-verifier evidence trail. This is an artifact grade, not acceptance of either arm's self-reported result.

| Rubric (max) | Monolith | Team | Independent basis |
|---|---:|---:|---|
| Hard success/installability/export integrity (20) | 19 | 20 | Each final STL re-imported as one watertight, winding-consistent component; both combined STEPs re-import validly in CadQuery. |
| Dimensional/reference correctness (25) | 14 | 21 | Both use the official 72.0 x 152.8 x 8.6 mm body. Team has a metrologist-owned datum sheet and bounded camera/control response; monolith uses a simple body fixture and low-confidence feature estimates without a named-datum contract. |
| Protective/functional design quality (15) | 7 | 13 | Team has continuous 1.2 mm screen/camera protective lip intent, a raised camera rim, and bounded corner returns. Monolith has no raised camera lip and a very long open right-side relief. Both intentionally use broad access relief, so neither earns full credit. |
| FDM printability/physical process plan (20) | 13 | 18 | Both meshes are support-free in their planned pose by inspection and source intent. Team adds an X2D TPU plan and six direct-geometry clearance coupons; neither has a completed physical fit print. |
| Independent verification/visual evidence (15) | 5 | 14 | Monolith's verifier is self-authored and lacks an independent visual/reference comparison. Team has separate verifier-owned seven-check evidence and visually useful final fit/section/printer views; it still lacks physical-unit proof. |
| Artifact completeness/parametric maintainability (5) | 4 | 5 | Both have parametric source, verifier, STL, STEP, renders, and notes. Team also has durable contracts, reference source, coupon generator, coupon meshes, and an audit ledger. |
| **Total** | **62** | **91** | |

## Independent mesh/export results

The grader re-imported the two final exported STLs, not the in-memory CAD objects:

| Arm | STL SHA-256 | Re-imported bounds (mm) | Mesh | Re-imported STEP |
|---|---|---|---|---|
| Monolith | `211e8f29b5c1ca0c85e5edb4ab8b497feb4f02ec4758c228b73e826ec84b2553` | 76.2 x 157.0 x 11.25 | 1 component, watertight, winding-consistent, 2,040 faces | valid, 21,963.765 mm3 |
| Team | `71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44` | 75.9 x 156.3173 x 11.9 | 1 component, watertight, winding-consistent, 2,300 faces | valid, 18,921.937 mm3 |

The required community-only hidden reference was re-imported from outside the repository and hashed as `8ddc8c882a751c96e3b4a2219bfe67ee4a9105696a3537f537774fc218922dc3`. Its extents are 72.4584 x 152.7991 x 12.0034 mm. Height aligns with the official 152.8 mm, but width is +0.4584 mm and depth is +3.4034 mm against the official 72.0 x 8.6 mm body. The excess depth is consistent with a camera projection being included, but this is an inference. Because it is an unverified community model, it was treated as one evidence source, never absolute truth, and was not copied into this repository.

## Visual inspection

I opened the official hardware diagram and final arm renders by eye. Monolith's exterior and fit renders show a functional tray, but also show the right-side access opening running through much of the sidewall and a simple flat camera opening with no camera-protective raised rim. Its section render is a clipped half-case view, which makes lip assessment weaker than a matched longitudinal section.

The team's multiview and transparent-fit/section evidence show an open-screen tray, a continuous rear-to-screen lip response, an explicit camera-opening rim, large lower access opening, and a long continuous right-control relief. Its final STL is print-oriented, so the camera end appears at the opposite image end from an installed rear-view; this is a coordinate transform, not a handedness defect. The large reliefs deliberately trade some local protection for uncertainty tolerance.

## Concrete defects and advantages

Monolith defects: no independent verifier; no named-datum dimension contract; a basic phone fixture that omits camera projection; no final exported fit coupon; no visual overlay or same-view official-reference comparison; long right-side opening weakens edge/control protection; camera opening lacks a protective raised rim.

Team advantages: explicit metrology provenance/confidence and unresolved-risk gates; accepted hidden mating fixture; independent verifier contract; direct-geometry coupon source plus six exported variants; camera rim and screen lip; detailed TPU/X2D process and field-test plan; rejection ledger. Team defects: actual unit-specific camera, microphone, bottom-feature, and corner geometry remain low confidence; the broad right and lower reliefs reduce local coverage; no actual coupon/phone/charging physical-test result or reopened slicer 3MF is delivered.

## Comparative delivery/cost metrics

| Metric | Monolith | Team |
|---|---:|---:|
| Final delivered files, excluding `__pycache__` | 16 | 87 |
| Final delivered bytes, excluding `__pycache__` | 994,955 | 4,136,632 |
| Python source complexity | 2 files, 181 lines, 8,663 bytes | 8 files, 782 lines, 32,479 bytes |
| Logged elapsed / critical path | 8m 48s / 8m 48s inferred single-arm | 1h 11m 22s / 1h 11m 22s serial gate path |
| Rejections | no formal ledger; one recorded failed downface audit before correction | 3 |
| Per-agent token usage | not exposed | not exposed |
| Auditable non-token proxy | 1 logged role instance | 15 logged role instances |

The role count and contract/source sizes are only auditable proxies; they are not token estimates.

## Reproducibility

Commands run from the repository root:

```powershell
python experiments\pixel-10-case\grading\baseline\measure_meshes.py
python -c "import cadquery as cq; from pathlib import Path; paths=[Path(r'experiments/pixel-10-case/arms/monolith/pixel10_case.step'),Path(r'experiments/pixel-10-case/arms/team/pixel10_case_cq_a.step')]; [print(p, 'valid=',cq.importers.importStep(str(p)).val().isValid(), 'volume_mm3=',round(cq.importers.importStep(str(p)).val().Volume(),3)) for p in paths]"
```

The first command completed successfully and wrote `mesh_measurements.json`; its measured values are summarized above. The STEP command completed successfully: monolith valid at 21,963.765 mm3 and team valid at 18,921.937 mm3. I also used the local image viewer for the official diagram and final exterior, fit, section, and multiview renders listed in the visual inspection.

## Confidence, limitations, and optimization

Confidence is **high** for the export-integrity comparison and **medium** for final physical fit/protection: official dimensions constrain only the body, while the official diagram is explicitly uncalibrated for feature positions. Neither design has a real-device coupon result. The hidden community mesh adds context but is materially inconsistent with official thickness and therefore cannot settle that uncertainty.

For monolith, add a metrologist-owned datum/provenance sheet, actual geometry-derived coupons, a raised camera rim, then require a fresh designer-distinct verifier to inspect same-view photo/reference composites and the re-imported final STL. For the pipeline, keep the designer != verifier and visual-inspection gates, but reduce cost by retaining a compact metrology/print-plan contract, limiting artifact fan-out for rejected candidates, and dispatching only correction-scoped designer plus fresh verifier loops after a rejection. Do not remove the final visual review, fresh verifier, or physical coupon gate.
