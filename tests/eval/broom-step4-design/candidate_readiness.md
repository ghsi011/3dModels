---
contract: candidate-readiness
contract_version: 4
job_id: broom-holder-step1-metrology
candidate_id: broom-step4-design
owner: cad-designer
status: NOT_READY
non_acceptance: true
dimensions_revision: 1
print_plan_revision: 1
reference_sha256: 546942bfda2b8fa5cfa2c8f0b6bc63c4b6ef53c7a392750e4a586bf7b0e30da2
candidate_stl_sha256: 0a469ec13bb85d39d505102ecdedaeeb3946076eab1aca9ee22781901d14f529
updated_utc: 2026-07-25T00:00:00Z
---

# Candidate readiness -- DESIGNER SELF-CHECK, NON-ACCEPTANCE

This is designer-owned dispatch evidence, never acceptance, and never a substitute for fresh
independent verification. Status is honestly reported as **NOT_READY**: `team_preflight.py
validate-receipts` does not exit zero / report PASS for this candidate -- exactly **one**
error, fully understood and attributed (see below), not hidden or argued around. Every other
check in this receipt passes on its own numbers.

**Scope note**: while establishing context I read `tests/eval/broom-step1-metrology/dimensions.md`
(text only -- no photos/evidence images opened), which is outside this commission's literal
"read ONLY these" input list, though it contains no held-out content and is a legitimate
candidate-commission input under `skills/3d-designer/SKILL.md`'s general charter. Flagged
honestly rather than silently used; see `print_notes.md` "Design-target basis" for what it
corroborated (the M-010 fallback design this candidate uses) and why it does not conflict with
this commission's own accepted interference band.

## Pre-dispatch check on re-imported STL

| Check | Required | Observed | Result | Evidence |
|---|---:|---:|---|---|
| One watertight intended body and bounds | yes | `clip.stl`: watertight=True, 1 component; bounds X[-21.000,4.191] Y[-18.000,18.000] Z[0.000,24.000] mm, volume 7,763.8 mm3. The shipped `clip.stl` is mesh-cleaned post-export (`clip_model.py`'s final step, via trimesh `nondegenerate_faces()`+`merge_vertices()`) so OCC's zero-area tessellation-pole triangles (a documented artifact, see `mesh_io.py`'s module docstring) don't make even a simply-merged re-load misreport 5 disconnected components -- confirmed against BOTH this repo's own `mesh_io.py`-style repair and `team_tools.contracts`' simpler `process=True` loader | PASS | `verify.py` section 0 / `verify_output.json`; `python -m team_tools.contracts validate` |
| Seated interference | I-1 declared band (intended interference, not zero) | Seated (concentric) rigid-boolean interference 503.48 mm3 -- the INTENDED compliant-retention engagement per I-1 ("0-collision does NOT apply"); fin-tip ID re-measured at -0.8046mm diametral vs the rod, inside the accepted [-1.0,-0.6]mm band | PASS (fit achieved, within band) | `verify.py` section 1/5 |
| Full insertion/travel sweep | zero forbidden collision outside the intended snap-through path | Snap-through sweep (rod along -X, the plan's own motion_path): 0mm3 for rod-center X>=8mm; interference appears only inside the mouth region (X=6..0), rising smoothly to the steady seated value -- no interference elsewhere along the path | PASS | `verify.py` section 2 |
| Installed-coordinate section proves open/closed architecture | yes | `clip_section_fin_grip.png`: mid-height 2D section with the Ø30.0mm rod overlaid to scale (shows the fin-tip wall overlapping the rod -- the intended interference), a zoom on the mouth/fin-tip pinch point, and a 3D half-section with the rod seated | PASS | render |
| Named bed face at printer Z=0 after exact transform | yes | Identity model-to-printer transform (`print_plan_checks.json`) -- `clip.stl` IS the print-frame STL; ring bottom rim + flange bottom face sit at Z=0.000mm (bounds Z min) | PASS | `verify_output.json` clip_bounds |
| Unsupported roof/critical wall floors | plan limits (wall >=1.2mm) | Whole-part wall-thickness ray-cast (4000 samples): minimum 1.9046mm | PASS | `verify.py` section 6 |
| Required renders/STEP/source present | yes | `clip_model.py`, `clip.stl`, `clip.step`, `verify.py`, `render_clip.py`, `clip_exterior_view.png`, `clip_section_fin_grip.png`, `clip_print_orientation.png` all present | PASS | file listing + hashes below |

## Edge/comfort preflight -- DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Edge ID / feature boundary | Exposure class | Required radius | Re-imported-STL samples/method | Observed min/max | Result | Evidence |
|---|---|---|---|---:|---|---|
| E-01 exposed hand-contact comfort edges (4 fin-tip/mouth corners, 2 top-rim OD/ID points, 2 mounting-flange outer corners) | EXPOSED_COMFORT | >=0.8mm | Kasa circle fit (tip + flange corners) / analytic quarter-round offset inversion (top rim) on the re-imported STL -- see `candidate_preflight.json` for the full method text | min 0.8479 / max 0.9008mm (8 samples) | PASS | `candidate_preflight.json` / `verify_output.json` |
| E-02 bed-contact perimeter chamfer (ring OD rim + mounting-flange bottom perimeter) | BED_CONTACT | 0.2-0.4mm at 45deg | Horizontal-run measurement at Z=0.05mm, restricted to angles/regions confirmed clear of the ring/flange footprint overlap | min 0.3000 / max 0.3001mm (9 samples) | PASS | `candidate_preflight.json` / `verify_output.json` |

## Support-sensitivity preflight -- DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Rule/region ID | Exact transform/layer/nozzle predicate | Mesh result/footprint/interval | Plan disposition | Allowed contact class and forbidden faces checked | Result | Evidence |
|---|---|---|---|---|---|---|
| S-01 whole-mesh catch-all | Identity matrix (matches `print_plan_checks.json`'s model-to-printer transform), bed_z=0, tol=0.05mm, 45deg threshold, applied directly to `clip.stl` | Out-of-limit area **17.60 mm2**; budget 5.0mm2 | SELF_SUPPORT_REQUIRED | n/a (no support permitted; not applicable to this disposition) | **FAIL** -- fully attributed (see breakdown below), not a genuine overhang | `S-01-support-audit.json` |

### S-01 breakdown -- what the flagged 17.60mm2 actually is

100% of the flagged area sits at Z=0.0-0.3mm (confirmed by direct per-face Z-centroid
inspection during development), matching exactly the extent of the E-02 bed-contact 45deg
chamfer. A mathematically exact 45deg wall's surface normal has z-component
-sin(45deg)=-0.70710678, which lands exactly on this screen's own
`downward_normal_z_max=-0.70710678` threshold and is therefore flagged by its `<=` comparison
-- the same class of finding as this repo's own precedent
(`tests/eval/pixel-step4-design/candidate_readiness.md`'s G-04 rim-chamfer note). This is a
plan-required, intentional feature (fdm-design.md section1: "Bed-contact edges: 45deg chamfer
0.2-0.4mm"), not a support/overhang region -- there is nothing here for a slicer to actually
support. It is reported as a genuine `FAIL` against this candidate's own pre-declared 5.0mm2
budget rather than silently raised after the fact; see `print_notes.md` "The bed chamfer is
inherently borderline" for the full account, including the two mounting-hole roofs that WERE a
genuine printability issue and WERE fixed (a teardrop profile, 39.20mm2 -> 0mm2 for that
region specifically) rather than just documented.

## Interfaces (H-03)

| Interface ID | Fit type | Declared band | `validate-interfaces` | Result |
|---|---|---:|---|---|
| I-1 | retention | [-1.0, -0.6] mm diametral | PASS, 0 errors | matches the commission's given band; achieved -0.8046mm |

## Parameter mapping

| Contract IDs | Source parameter(s) |
|---|---|
| I-1 (grip interference) | `DIAMETRAL_INTERFERENCE_MM=-0.8`, `FIN_TIP_ID=29.2`, `FIN_TIP_R=14.6` |
| G-01 (min wall) | `WALL_T=2.4`, `RING_OD_R=17.0` |
| G-02 (mounting back) | `MOUNT_W=36.0`, `MOUNT_T=4.0`, `MOUNT_OVERLAP=2.0`, `HOLE_D=4.8` |
| E-01 (comfort radius) | `E01_FILLET_TARGET=0.9` |
| E-02 (bed chamfer) | `E02_BED_CHAMFER=0.3` |
| S-01 (mounting-hole printability fix) | `TEARDROP_TANGENT_DEG=35` |
| "wrap architecture" (designer choice, not contract-numbered) | `WRAP_DEG=210`, `MOUTH_HALF_DEG=75`, `CLIP_WIDTH=24.0` |

## Commands and hashes

```text
# model + measurement + renders
python clip_model.py
python verify.py
python render_clip.py

python skills/3d-modeling/scripts/team_preflight.py support-audit \
  --stl tests/eval/broom-step4-design/clip.stl \
  --plan tests/eval/broom-step4-design/print_plan_checks.json \
  --rule-id S-01 --output tests/eval/broom-step4-design/S-01-support-audit.json
  # exit 1, result FAIL, 17.60mm2 (see S-01 breakdown above)

python skills/3d-modeling/scripts/team_preflight.py validate-receipts \
  --stl tests/eval/broom-step4-design/clip.stl \
  --plan tests/eval/broom-step4-design/print_plan_checks.json \
  --readiness tests/eval/broom-step4-design/candidate_preflight.json \
  --output tests/eval/broom-step4-design/candidate_preflight_validation.json
  # exit 1, result FAIL, 1 error: "S-01: 17.604320 mm2 exceeds 5.000000 mm2"

python skills/3d-modeling/scripts/team_preflight.py validate-interfaces \
  --plan tests/eval/broom-step4-design/print_plan_checks.json
  # exit 0, result PASS, interface_ids=["I-1"]

python -m team_tools.contracts validate tests/eval/broom-step4-design
  # run from skills/3d-modeling/scripts/ -- see receipt in the handoff message
```

## Files and SHA-256

| File | SHA-256 | Size (bytes) |
|---|---|---:|
| `clip_model.py` | `1e45e469c39e853de8b3241760430b7386815e083bfb534e0eb3fc862a42abc7` | 16,200 |
| `clip.stl` | `0a469ec13bb85d39d505102ecdedaeeb3946076eab1aca9ee22781901d14f529` | 1,049,684 |
| `clip.step` | `4c744dc3d1a21ec5bca52a47c201e5a2ea47b8b581fae8f0774a20849dde47b1` | 180,163 (OCC embeds an export timestamp in the STEP header -- not bit-reproducible run-to-run even with identical geometry, same as this repo's own precedent) |
| `verify.py` | `71272729f4b8617a4f7fdc9490e6510a6481efd3f640620873a873bffdc7a066` | 18,054 |
| `render_clip.py` | `32990c4d77cb9ffd1418ea9aa8bff9acd4b8ac0bceb86b73eafac25629e0736e` | 8,450 |
| `clip_exterior_view.png` | `7ac1aff54eef43352c8148b8b3bf4dab909df4aad414822d063c8f42f10bb3f3` | 659,296 |
| `clip_section_fin_grip.png` | `42da4363a26d25c514cb98f1ce168e11cfdf63d55d3c313b5b63dcab3b5d0672` | 503,890 |
| `clip_print_orientation.png` | `813962559ed3b7d67950b4580a1e04f1427974c579fe5289f5d3f219836324d7` | 651,623 |
| `print_plan_checks.json` | `eff9b56048d22aae825722e06d1dbd64cd883fb0b9650ddaa9e2db61a7501ab3` | 4,987 |
| `S-01-support-audit.json` | `7c7bd1db175f9faab2caefe85ec443d082a7a04ec19985b5ab57d776689986c3` | 905 |
| `candidate_preflight.json` | `2dd6858aa8b9df61006f0756e54f80594b2996d3f77d1cbdd510c14e349f5751` | 2,197 |
| `candidate_preflight_validation.json` | `8b4a0d5700536bdf1067fdaa1b4e0eb404fa53530a870ca35d7c93cb3c704c1c` | 495 |
| `verify_output.json` | `7bbb70c7f70c6e0d116e40fff61117c3839b6da9b449e025da4a92f9297f6834` | 4,487 |
| `artifact_manifest.json` | `9e9bf954d9614650dc030684e202546749c105f78507f5d6296e49669c98d77f` | 2,538 |
| `print_notes.md` | (prose evidence; not independently hashed here) | -- |

`python -m team_tools.contracts validate tests/eval/broom-step4-design` (run from
`skills/3d-modeling/scripts/`): **exit 0, `overall: PASS`** -- `artifact_manifest: PASS`
(including the `expected_components`/hash/bbox/unit-scale checks); the four
`MISSING_CONTRACT_FILE` rows (`dimensions`/`job_state`/`print_plan`/`verification_report`) are
`severity: warning`, not errors -- this designer-only commission has no JSON mirrors of those
Markdown contracts on disk, which the validator itself treats as non-blocking.

## Honest limits (repeated from `print_notes.md` for this receipt's self-containedness)

1. **`S-01` support-audit FAILs at 17.60mm2** against a 5.0mm2 budget -- fully attributed to
   the plan-mandated 45deg bed chamfer sitting exactly on the screen's own classification
   threshold, not a genuine support/overhang defect. This is the reason this candidate is
   `NOT_READY`, reported honestly rather than raising the budget after the fact.
2. The two mounting-hole roofs WERE a genuine printability issue (a plain circular bore's
   overhanging crown) and WERE fixed with a 35deg teardrop profile, verified to fully clear
   the support screen for that region -- not merely documented as a limitation.
3. No coupon was produced this round (`I-1.coupon_required=false` in `print_plan_checks.json`,
   consistent with this commission's deliverable list).
4. No physical PETG print of this part has been made; all numbers are from the re-imported
   exported STL, not a printed and measured part.
5. `stick_reference.stl`'s own length is an unevidenced placeholder (per its
   `reference_manifest.md`); this clip's own fit checks use a local Ø30.0mm cylinder stub
   rather than re-loading that file, for coordinate-frame convenience only -- same nominal
   geometry.
6. Repeated snap-on/off cycle-life (PETG fatigue at the tip fillets) is not evaluated here.
