# Pixel 10 round-2 v2 independent scorecard

## Result

**80/100.** The frozen candidate passes the hard export-integrity gate but misses the preregistered `>=88` independent-score target. It is higher than the frozen monolith baseline (`62`) and lower than the frozen baseline-team result (`91`). This is an artifact grade, not adoption of the candidate's self-report.

| Rubric | Score | Independent basis |
|---|---:|---|
| Hard export integrity (20) | 20 | Fresh STL re-import is one watertight, winding-consistent component. Fresh CadQuery STEP import is valid. |
| Dimensional fidelity (25) | 20 | The cavity and overall reference use the official `72.0 x 152.8 x 8.6 mm` body with a named datum sheet and deliberate clearance. Camera, controls, ports, corner radius, glass recess, and camera-stack height remain unresolved and are represented by broad envelopes rather than verified device geometry. |
| Design quality (15) | 10 | The mesh has a continuous screen-lip architecture, corner returns, and a rounded aperture edge, but it uses a very broad rear camera aperture and a long right-side relief. Those choices protect against uncertain data yet reduce local protection; no device test substantiates the provisional camera-lip claim. |
| Printability/process (20) | 13 | The X2D/TPU plan, exact tilted transform, single multi-lane coupon, and exterior-only support exclusions are concrete. The re-imported candidate still has known G05 non-self-supporting geometry, and the required native slicer project, support contacts, toolpath section, layer map, and fresh P2 review are explicitly pending. |
| Verification/evidence (15) | 12 | Fresh v5 verification re-imports the STL and records all seven candidate checks. I also inspected the official diagram, rear overlay, exterior, fit, section, and orientation PNGs. The section is useful; the exterior/fit/orientation views are highly foreshortened and cannot independently establish print-face/support contact. The only same-view overlay is correctly limited to non-calibrated relative layout. |
| Artifact/maintainability (5) | 5 | Parametric source, independent re-import script, STL, STEP, four renders, reference source/export, contracts, and a geometry-derived coupon are present and hash-bound. |
| **Total** | **80** | No hard cap. |

## Fresh export measurements

I did not access FreeCAD. `measure_v2.py` freshly re-imported the delivered exports:

| Export | SHA-256 | Result |
|---|---|---|
| `pixel10_case.stl` | `255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960` | 1 component, watertight, winding-consistent; bounds `[-2.1, -1.5458, -1.3]..[74.1, 154.9, 9.7]` mm; extents `76.2 x 156.4458 x 11.0` mm; `15,856.857 mm³`. |
| `pixel10_case.step` | `e178a4d87b85988b3457e5c25f3e44c03c7016c5e9c20d551dd3fcdaeac88689` | CadQuery re-import valid; `15,858.722 mm³`. |

The small STL/STEP volume difference is expected from tessellated versus B-rep measurement and does not affect the export-integrity result.

## Preregistered runtime and compactness results

| Metric | Target | Logged/independent result | Result |
|---|---:|---:|---|
| Critical path | <=35m | **1h 15m 35s** (`23:23:50Z` to `00:39:25Z`) | Miss |
| Logged commissions | <=8 | **17** | Miss |
| Fresh verifier commissions | 1 | **5** (`V1` through `V5`) | Miss |
| Rejections | 0 avoidable loops | **4** | Miss |
| Delivered files excluding caches | <=43 | **30** | Pass |
| Delivered bytes excluding caches | <=2,068,316 | **1,519,980** | Pass |
| Independent score | >=88 | **80** | Miss |

The run log reports `1,519,907` bytes, 73 fewer than my direct recursive inventory. This minor discrepancy does not change the compactness pass. The run log explicitly says runtime token telemetry was **not exposed**. I did not estimate tokens from bytes, source size, or commission count.

The source/contract proxies are six Python files, 531 Python lines, 25,663 Python bytes, and seven canonical contract files (`job_state`, `dimensions`, `print_plan`, `candidate_readiness`, `verification_report`, `print_notes`, and `reference_acceptance`). These are auditable proxies only, not token measures.

## Critical acceptance limitation

`print_notes.md` correctly marks final printing as pending. Before a real print can be accepted, P2 must produce the native Bambu project, support-contact underside view, F23 toolpath section, and layer map for the known G05 regions; a new verifier must review those exact artifacts. The score does not treat the candidate-verification PASS as final-print acceptance.

## Reproducibility

From the repository root:

```powershell
uv run experiments/pixel-10-case/optimization/round2/grading/measure_v2.py
```

The resulting raw measurements are in `mesh_measurements.json`.
