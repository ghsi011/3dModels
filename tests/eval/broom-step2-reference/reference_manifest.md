---
contract: reference-manifest
job_id: broom-holder-step1-metrology
step: broom-step2-reference
role: designer (reference commission, blind build)
input_read: tests/eval/broom-step1-metrology/dimensions.md (ONLY)
inputs_not_read: >
  tests/broom holder/30mm broom stick.png (source photo), tests/broom holder/BroomHolderVCD.3mf
  (held-out grader answer), tests/eval/broom-step1-metrology/evidence/ (photo copy + annotated
  metrology images), tests/eval/broom-step1-metrology/method.md, any other tests/ or
  experiments/ content. Per skills/3d-designer/SKILL.md reference-commission rule:
  "reconstruct the mating object from dimensions.md alone and do not inspect the source photos."
backend: CadQuery 2.8.0 (py -3, system Python), re-imported with trimesh 4.12.2 for measurement
status: built blind; PENDING metrologist round-trip (dimensions.md's own "Reference round trip"
  table stays PENDING until the metrologist overlays this build on the photo)
---

# Broom stick — blind mating reference, build receipt

`stick_reference.py` is the parametric CadQuery source; `stick_reference.stl` /
`stick_reference.step` are its exports. Both design-driving parameters cite the sheet's ID and
confidence grade, or are flagged `ASSUMPTION` where the sheet gave no numeric value.

Trivial part: a plain right-circular cylinder, no dome, no end feature, no angular datum (the
sheet defines none — the stick is treated as rotationally symmetric).

## Parameters

| Parameter | Value | Sheet citation | Confidence |
|---|---:|---|---|
| `STICK_DIAMETER` | 30.0 mm | M-001 nominal (bounded working range 29.0–31.0 mm, not modeled as a second variant) | D — user task-brief statement only, no caliper reading anywhere in the sheet's source photo |
| `STICK_LENGTH` | 150.0 mm | F-001 candidate response's own placeholder ("~150 mm placeholder, not a measured fact") | ASSUMPTION — F-003 (far end/total length) is explicitly "Not evidenced" in the sheet; the crop-frame bottom edge is not a confirmed physical end |

## Feature inventory: sheet vs built

| Sheet ID | Feature | Built? | Why |
|---|---|---|---|
| F-001 | Round shaft (primary grip surface) | **yes** | plain right cylinder, Ø30.0 × 150mm, true circle per F-004 |
| F-002 | Domed/rounded tip | **not built** | sheet marks this "Optional for the reference cylinder... or omit entirely if the reference is only needed to validate a mid-shaft grip coupon"; the commission brief also asks for "a clean Ø30.0mm cylinder" |
| F-003 | Far end / total stick length | **not built** | sheet: "Do not model an end feature at the crop edge. Leave the reference shaft open-ended / length-parametrized." Both Z faces are plain flat cuts, not a modeled physical end |
| F-004 | Cross-section roundness | **yes (true circle)** | `cq.Workplane.circle()` is exact-circular; sheet's candidate response is "Model F-001 as a true circle at the M-001 diameter" |

## Re-imported STL measurement receipt (trimesh, not the in-memory CadQuery solid)

| Property | Value |
|---|---|
| watertight | True |
| volume | 105,984.81 mm³ (in-memory CadQuery: 106,028.75 mm³; the ~0.04% gap is STL tessellation discretization at `tolerance=0.01`, expected for a curved surface) |
| bounds X | [-15.000, 15.000] mm |
| bounds Y | [-14.995, 14.995] mm |
| bounds Z | [0.000, 150.000] mm |
| extents (X, Y, Z) | 30.000 × 29.991 × 150.000 mm |

### Feature re-measurements (sliced from the exported/re-imported STL)

| Check | Method | Result | Sheet parameter | Match |
|---|---|---|---|---|
| Diameter, X | Z=75 mid-shaft slice | 30.0000 mm | M-001 = 30.0 | exact |
| Diameter, Y | Z=75 mid-shaft slice | 29.9907 mm | M-001 = 30.0 | within STL facet tolerance (<0.01mm) |
| Length | overall Z extent | 150.0000 mm | `STICK_LENGTH` = 150.0 (ASSUMPTION) | exact |
| Roundness | mid-shaft loop radii (min/max/mean) | 14.9361 / 15.0593 / 14.9975 mm | nominal R=15.0 | within STL facet tolerance; true circle in the CAD solid, faceting from `angularTolerance=0.1` |

`measure_receipt.py` (kept alongside the deliverables) reproduces this pass.

## Assumptions

| Parameter | Value | Why an assumption |
|---|---:|---|
| `STICK_LENGTH` | 150.0 mm | sheet's F-001 candidate response supplies this exact figure as its own placeholder — "axial length itself is not evidenced — parametrize, e.g. ~150mm placeholder, not a measured fact." Carried through unchanged, not re-derived. |

## Conflicts and open questions carried forward, not silently resolved

- **Q-01 (M-001, diameter)**: 30.0mm is a D-confidence user statement, not a caliper reading —
  no scale reference exists anywhere in the sheet's source photo. This build uses the stated
  nominal only; the sheet's own bounded working range (29.0–31.0mm) is not modeled as a second
  geometry variant here. Blocks upgrading to Confidence A/B; does not block this blind build.
- **F-003 (far end)**: entirely unmodeled, per sheet instruction — both Z faces of this cylinder
  are plain open cuts, not evidence of the stick's real physical end.
- **F-002 (domed tip)**: entirely unmodeled — deliberately omitted per the sheet's own "optional/
  omit" framing and the commission's request for a clean cylinder.

## Render

- `stick_reference_view.png` — left panel: isometric 3D view of the plain cylinder; right panel:
  true-proportion mid-shaft (Z=75) cross-section outline confirming the constant Ø30.0mm circular
  section. Produced with matplotlib (`render_views.py`) per the commission's guidance that
  Chromium PNG capture is unreliable in this environment.

## Files and SHA-256

| File | SHA-256 | Size |
|---|---|---:|
| `stick_reference.py` | `416d0da1d8ac7c20f93da6db85952c36457edbe19018783dc79238d0b7bad973` | 4,539 B |
| `stick_reference.stl` | `546942bfda2b8fa5cfa2c8f0b6bc63c4b6ef53c7a392750e4a586bf7b0e30da2` | 25,084 B |
| `stick_reference.step` | `7e0fc6c78b7c8cc1783a86c2edbd530ca93c92c29526f176308dc1760656f788` | 5,754 B |
| `stick_reference_view.png` | `5d628004914561cfcb483ee5fd986a440c25b7f77d55cef0a9dbddf9b6f17050` | 333,301 B |
| `measure_receipt.py` (helper, not a primary deliverable) | `a5b0631c75eab2525fbd172253a899912fb6a3ba8f0b5669a1899bf25b5d9b85` | 1,499 B |
| `render_views.py` (helper, not a primary deliverable) | `39c7220a7c02f15a12cf32391d732d588bbc836df83510b537e8ff6e39c35281` | 3,289 B |

## Honest limits

- This is a blind build: no photo comparison, no overlay, no ACCEPT/REVISE verdict — that is the
  metrologist's round-trip step against `dimensions.md`'s "Reference round trip" table, still
  `PENDING` as of this commission.
- Diameter is anchored to a D-confidence (user-statement-only) nominal — no caliper reading
  exists in the underlying evidence. Treat 30.0mm as provisional until a caliper reading or the
  repo's PLA fit-coupon workflow retires that uncertainty (sheet Q-01).
- Length (150mm) is a placeholder carried verbatim from the sheet's own candidate response, not a
  measured fact — do not read it as the real stick's length.
- No dome (F-002) or end feature (F-003) is modeled; both ends are plain flat cuts of an
  open-ended shaft, not a claim about the real stick's tip or far-end geometry.
- Not a candidate/printable holder part: no print plan, no orientation/support/overhang design —
  this file exists to be the mating-object test fixture and metrologist round-trip target only.
