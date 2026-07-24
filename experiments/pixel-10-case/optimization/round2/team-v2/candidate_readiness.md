---
contract: candidate-readiness
contract_version: 2
job_id: pixel-10-base-case-v2
candidate_id: cq-v2
owner: cad-designer
status: READY
non_acceptance: true
dimensions_revision: 2
print_plan_revision: 4
reference_sha256: 81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48
candidate_stl_sha256: 255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960
updated_utc: 2026-07-24T02:25:00Z
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

This receipt is hash-bound designer evidence only. It is not independent verification or acceptance; Q01--Q05 in `dimensions.md` remain unresolved. `print_notes.md` and the actual TPU coupon are P2 post-verification work and are not D2 readiness criteria. Print-plan revision 4 assigns support eligibility/exclusion review to candidate verification; native slicer coverage/contact evidence remains P2 post-PASS and is not claimed here.

| Pre-dispatch check on re-imported STL | Required | Observed | Result | Evidence |
|---|---:|---|---|---|
| One watertight intended body and bounds | yes | `True`; one component; bounds X=-2.100..74.100, Y=-1.546..154.900, Z=-1.300..9.700 mm | PASS | `python verify.py`; `pixel10_case.stl` SHA-256 above |
| Seated interference | zero forbidden collision | 0.000 mm3 against the D01--D04 rounded nominal body | PASS | re-imported STL manifold boolean in `verify.py` |
| Full insertion/travel sweep | zero forbidden collision | 0.000 mm3 maximum at nine +Z positions from seated through +16.000 mm | PASS | re-imported STL manifold booleans in `verify.py` |
| Installed-coordinate section proves architecture/open face | yes | mid-Y render shows 1.300 mm back, 0.300 mm rear clearance, open +Z front, 1.100 mm lip proud, and a visibly rounded 0.800 mm lip/root transition | PASS | `render_section.png` SHA-256 `bdf3fd5fe517439b32686976babcd106269c6c389192003f685880cd235461e6` |
| Same-view candidate-to-S2 overlay | yes | exterior evidence contains an S2 rear same-view overlay: cyan case envelope and amber shared F14 aperture, explicitly labelled relative-layout-only | PASS | `render_exterior.png` SHA-256 `6560e2d7ac8edb94ae5ddb91f2b48c86083b6dd94fe459794109cbdf5a38ecad` |
| F23 exposed F14 rear-aperture rim | G04 r=0.40 +/-0.02 mm | source applies a 0.400 mm fillet to the F14 rear exposed edge; re-imported, tessellated STL is bound by hash above | PASS | `model.py`; `pixel10_case.stl` SHA-256 above |
| Named bed face at printer Z=0 after exact transform | yes | L midpoint=(-1.746447,76.400000,-0.946447) mm; transformed Z range -0.0000..60.8283 mm; 16 mesh vertices within 0.05 mm of bed | PASS | `python verify.py`; `render_print_orientation.png` SHA-256 `48b217a45b71b65efeb39452ea6a4484827b6db6111fae018c720aae191c4c74` |
| G05 part-only out-of-limit geometry | V3 numeric audit must be retained, never relabelled support-free | 4.408623 mm2 outside-F23 area; four F23 contour transitions 0.405512..43.587353 mm beyond self-support bound | PASS — accurately recorded for support planning | `print_plan.md` rev3; re-imported STL self-check in `verify.py` |
| Manual-support material eligibility/exclusions | support may touch only unexposed exterior underside; all listed functional/exposed faces forbidden | V3 G05 regions are retained as part-only facts and are support-eligible only on their nonfunctional exterior underside; no candidate support geometry is present or claimed | PASS — eligibility for independent V5 | `print_plan.md` rev4 G05; re-imported STL self-check |
| V3 manual support coverage/contact evidence | native sliced project, underside/contact image, F23 toolpath section, layer map | P2 post-PASS; no support, zero-support, or support-coverage claim is made by D2 | PENDING — print-prep evidence after V5 PASS | `print_plan.md` rev4 G05/G10 |
| Required renders/STEP/source present | yes | `model.py`, `verify.py`, STL, STEP, exactly four required renders | PASS | hashes below |

## Parameter mapping

| Contract IDs | Source parameter(s) |
|---|---|
| D01--D04, D10, G01 | `PHONE_X`, `PHONE_Y`, `PHONE_Z`, `PHONE_R`, `CLEAR_XY`, `CLEAR_REAR`, `CAV_X`, `CAV_Y`, `CAV_Z`, `CAV_R` |
| D05, F10--F15, G08 | `CAM_X0`, `CAM_X1`, `CAM_Y0`, `CAM_Y1`, `CAM_R` |
| D06, F07--F09 | `RIGHT_Y0`, `RIGHT_Y1` |
| D07--D09, F05--F06, F18--F21 | `BOTTOM_X0`, `BOTTOM_X1`, `TOP_X0`, `TOP_X1` |
| F22--F23, G02--G04, G09 | `WALL=1.80`, `BACK=1.30`, `LIP_PROUD=1.10` |
| G05--G07, G10 | `LAND_HALF_AXIS`, `LAND_SUM`, `LAND_MID`; exact `R_y(-45 degrees)` in source and self-check |

## Commands and hashes

```text
cd experiments/pixel-10-case/optimization/round2/team-v2
python model.py
python verify.py

model.py                         7ed03cba473a19849c1c419ab21b8cd4d137690970b8bebe91da23a494ad3e62
verify.py                        594687c9746eeeb8d8c0cc565b3382bad2902b9d531437e9bc4db71bb12bce1e
pixel10_case.stl                 255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960
pixel10_case.step                e178a4d87b85988b3457e5c25f3e44c03c7016c5e9c20d551dd3fcdaeac88689
render_exterior.png              dcda907b6e72b709df1b3e16e608a4b9921f415b7b30835be8de93c104baeb1d
render_fit.png                   32dcc1db102b06015cd6acf2be9a1a704701335312ecb4fbdd7ca15ab22f575d
render_section.png               a50c92b8540add381c2ab5ec107b79c36144bc706d3620e6c4d2f74122f98491
render_print_orientation.png     e44a1c243e06dd113633cdaae45aba0a0c6c8336a9dd1eba3d7040a19208c99c
```
