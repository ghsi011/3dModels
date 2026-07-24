---
contract: verification-report
contract_version: 2
job_id: pixel-10-base-case-v2
revision: 5
owner: verifier
status: PASS
candidate_id: cq-v2
candidate_stl_sha256: 255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960
dimensions_revision: 2
print_plan_revision: 4
reference_sha256: 81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48
fresh_context: true
updated_utc: 2026-07-24T02:35:00Z
---

# Independent verification

## Input/upstream audit

| Input/claim | Expected revision/hash/datum | Independent observation | Result | Evidence |
|---|---|---|---|---|
| Candidate export | Current changed STL hash; v2 contracts | SHA-256 is `255945…5960`; STEP is `e178a4…88689`; re-import is one watertight, winding-consistent component with bounds `[-2.100,-1.545817,-1.300]..[74.099998,154.899994,9.700]` mm. | PASS | `verification_evidence_v5.md`; `verify_v5_reimport.py` |
| Accepted upstream | `dimensions.md` v2; accepted reference; `print_plan.md` v4 | Envelope-only acceptance and Q01--Q05 limits remain intact; S2 remains relative-layout-only. | PASS | `dimensions.md`; `reference_acceptance.md`; `verification_evidence_v5.md` |
| Readiness receipt | Non-acceptance only, rev4 plan | Receipt hash/revisions match. All check results were re-grounded. Rev4 assigns slicer/contact proof to P2 post-PASS, so readiness neither proves nor is required to contain it. | PASS | `candidate_readiness.md`; `verification_evidence_v5.md` |

## Seven checks on re-imported exported STL

| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | Re-imported manifold boolean against independently constructed D01--D04 reference | seated intersection `0.000000000 mm3` | Open-front seating architecture is visible. | PASS | `verification_evidence_v5.md`; `verify_v5_reimport.py`; `render_fit.png` |
| 2 full insertion/travel sweep | Re-imported manifold booleans at every `+Z` 1 mm step, 0..16 mm | maximum intersection `0.000000000 mm3` across 17 positions | No collision in the accepted conservative envelope. | PASS | `verification_evidence_v5.md`; `verify_v5_reimport.py` |
| 3 section | Re-imported STL mid-Y section at Y=76.4 plus render inspection | one loop; 235 section vertices | Render shows rear wall, clearance, open +Z front, and rounded screen lip/root. | PASS | `verification_evidence_v5.md`; `render_section.png` |
| 4 same-view/photo overlay look | Direct inspection of all supplied candidate views and S2 composite | n/a | Candidate exterior/F14 overlay is explicitly relative-layout-only; tilted iso views are foreshortened and were not used to infer support contact. | PASS | `verification_evidence_v5.md`; `render_exterior.png`; `reference_rear_overlay.png` |
| 5 named-datum feature positions/handedness | Re-imported mesh booleans against conservative response zones | F14 centre, F21 centre, F05/F06 top slot, and F07/F08 front-side control zone each `0.000000000 mm3` | Rear/bottom/top/right layout is not mirrored and retains the accepted broad response zones. | PASS | `verification_evidence_v5.md`; `verify_v5_reimport.py` |
| 6 measurement-to-geometry audit | Re-imported bounds/section/arc audit against D01--D10 and G02--G04 | F23 section radius `0.400008 mm`, within `0.380..0.420 mm`; rear wall 1.30 mm, clearance 0.30 mm, rails 1.80 mm, lip 1.10 mm | Rounded F23 edge is visible. Q01--Q05 are still open. | PASS | `verification_evidence_v5.md`; `render_section.png` |
| 7 planned-orientation printability/faces | Exact rev4 G05 transform plus re-imported part-only audit and exterior/nonfunctional eligibility/exclusion review | printer Z `-0.000000034..60.828264592 mm`; 16 bed vertices; known `4.408623 mm2` and 4 F23 failures retained | Support-required geometry is eligible only on the unexposed exterior/nonfunctional underside; G04 exposed radius and every stated forbidden functional/contact zone remain excluded. P2 slicer proof is downstream by rev4. | PASS | `verification_evidence_v5.md`; `verify_v5_reimport.py`; `render_print_orientation.png`; `print_plan.md` G05/G10 |

## Defects

| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|
| none | n/a | Rev4 resolves the prior contract-order defect. P2 evidence is intentionally downstream and remains mandatory before final-print acceptance. | `print_plan.md` G05/G10; `verification_evidence_v5.md` | P2 must supply the native sliced project, underside contact image, F23 section/toolpath image, and layer map; a fresh verifier must then assess those P2 artifacts. |

## Verdict

PASS. All seven candidate checks pass against `print_plan.md` rev4. The known G05 part-only failures are retained and are not self-supporting; their required native slicer/contact/toolpath/layer-map proof belongs to P2 post-PASS and is a final-print gate, not a candidate-verification rejection condition.
