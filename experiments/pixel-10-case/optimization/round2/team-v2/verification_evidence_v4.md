# V4 fresh verifier evidence

Candidate identity was independently re-bound before the checks: `pixel10_case.stl`
SHA-256 is `255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960` and
`pixel10_case.step` SHA-256 is
`e178a4d87b85988b3457e5c25f3e44c03c7016c5e9c20d551dd3fcdaeac88689`.
The exported STL was re-imported for the numerical checks; no candidate source was
used to pass a check. The re-import has one watertight body, bounds
`[-2.100000,-1.545817,-1.300000]..[74.099998,154.899994,9.700000]` mm, and
volume `15856.857053 mm3`.

| Check | Fresh observation | Result |
|---|---|---|
| 1, interference | Re-imported boolean with the accepted nominal reference: seated forbidden intersection `0.000000000 mm3`. | PASS |
| 2, insertion sweep | Re-imported boolean sweep through model `+Z=0..16 mm`: maximum forbidden intersection `0.000000000 mm3`. | PASS |
| 3, section | Re-imported `Y=76.4 mm` section has 234 vertices and the stated X/Z bounds. `render_section.png` visibly shows the rear wall, clearance, open `+Z` front, and lip. | PASS |
| 4, visual/overlay | Inspected `render_exterior.png`, `render_fit.png`, `render_section.png`, `render_print_orientation.png`, and `reference_rear_overlay.png`. The S2 view is explicitly relative-layout-only, as required by the accepted reference. The thin tilted views do not demonstrate support contact. | PASS, limited to the accepted non-calibrated visual claim |
| 5, named datum features | Re-imported response-zone audit reports zero material in the F14, F21, F05/F06, and F07/F08 conservative zones; supplied views retain rear/bottom/top/right handedness. | PASS |
| 6, measurement audit | Re-imported F23 cross-section radius is `0.399717..0.400004 mm`, within G04 `0.38..0.42 mm`; back `1.30 mm`, lip proud `1.10 mm`, and rails `1.80 mm` agree with the accepted envelope. Q01--Q05 remain open. | PASS |
| 7, exact print orientation | Applying rev3's `R_y(-45 degrees)` transform about L yields Z `-0.000000047..60.828264578 mm`, 16 vertices within 0.05 mm of the bed. The part-only audit retains `4.408623 mm2` outside-F23 unsupported area and four F23 failures at `0.405512..43.587353 mm` beyond the `0.3500 mm` bound. | NOT SELF-SUPPORTING; remedy proof absent |

## Rev3 controlled exterior-only support remedy audit

`print_plan.md` rev3 G05/G10 requires all of the following for the controlled
exception: a saved native slicer project/toolpaths at 0.16-mm F23 intervals; complete
prior-layer support/interface coverage of every V3 failing footprint; an underside or
section support-contact image plus contact selection proving the contact set is disjoint
from all forbidden faces and the exposed G04 radius; and a layer map. The V4 directory
contains no native sliced project, toolpaths, support-contact image/selection, or layer
map. Therefore the exact predicates cannot be evaluated, no exterior-only/contact-clear
finding is possible, and the `4.408623 mm2` may not be relabelled as zero.

Per the orchestrator's current contract-order instruction, this missing P2 evidence is
recorded as a `PRINT_PLAN` sequencing defect, not a `CANDIDATE_BUILD` geometry defect.
It nevertheless prevents a PASS under rev3's stated G05/G10 acceptance predicate.
