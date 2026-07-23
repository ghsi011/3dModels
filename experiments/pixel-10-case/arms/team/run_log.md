# Pixel 10 case team-pipeline run log

- Job ID: `pixel-10-case-team`
- Root orchestrator model: `gpt-5.6-terra`
- UTC start: `2026-07-23T21:53:01.9704657Z`
- UTC end: `2026-07-23T23:04:24.1874010Z`
- Elapsed wall time: `01:11:22` (from recorded start/end).
- Critical-path time: `01:11:22` (the gated pipeline was serial; no candidate branch overlapped the gate path).
- Rejection count: `3` (one upstream-sheet rejection during blind-reference acceptance; two exported-candidate geometry rejections).
- Common input diagram SHA-256: `9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0`
- CadQuery runtime: `2.8.0`
- FreeCAD: not used.

## Role instances

| Commission | Role | Model | UTC start | UTC end | Files produced | Checks run | Tokens |
|---|---|---|---|---|---|---|---|
| orchestration | orchestrator | gpt-5.6-terra | 21:53:01Z | 23:04:24Z | job_state.md; run_log.md | route, gate, artifact/hash audit | not exposed |
| meta-1 | metrologist | gpt-5.6-terra | 21:53:42Z | 21:57:43Z | dimensions.md; meta-1 evidence | datum/provenance/inventory | not exposed |
| ref-1 | blind reference designer | gpt-5.6-terra | 21:57:43Z | 22:02:48Z | reference.py; r1 reference artifacts | CadQuery strict export | not exposed |
| meta-2 | metrologist overlay | gpt-5.6-terra | 22:02:48Z | 22:07:41Z | r1 overlay/rejection evidence | visual overlay; upstream audit | not exposed |
| meta-3 | metrologist correction | gpt-5.6-terra | 22:07:41Z | 22:10:26Z | r3 camera/flash datums | frozen-diagram scale/provenance | not exposed |
| ref-2 | blind reference designer | gpt-5.6-terra | 22:10:26Z | 22:15:43Z | ref-2 source, STL, STEP, renders, manifest | CadQuery strict export | not exposed |
| meta-4 | metrologist overlay | gpt-5.6-terra | 22:15:43Z | 22:18:55Z | accepted r3 overlay evidence | visual overlay/handedness | not exposed |
| plan-1 | print engineer, pre-design | gpt-5.6-terra | 22:18:55Z | 22:22:27Z | print_plan.md | TPU/X2D/DFM/coupon constraints | not exposed |
| cq-a | candidate designer | gpt-5.6-terra | 22:22:27Z | 22:30:26Z | initial candidate exports/renders | CadQuery strict self-check | not exposed |
| cq-a-v1 | fresh verifier | gpt-5.6-terra | 22:30:26Z | 22:37:10Z | verification report r1/evidence | seven re-imported-STL checks: REJECT | not exposed |
| cq-a-r2 | candidate designer correction | gpt-5.6-terra | 22:37:10Z | 22:40:48Z | corrected exports/renders | open-screen self-check | not exposed |
| cq-a-r2-v1 | fresh verifier | gpt-5.6-terra | 22:40:48Z | 22:48:15Z | verification report r2/evidence | seven re-imported-STL checks: REJECT | not exposed |
| cq-a-r3 | candidate designer correction | gpt-5.6-terra | 22:48:15Z | 22:50:58Z | final exports/renders | print-orientation self-check | not exposed |
| cq-a-r3-v1 | fresh verifier | gpt-5.6-terra | 22:50:58Z | 22:57:53Z | verification report r3/evidence | all seven re-imported-STL checks: PASS | not exposed |
| prep-1 | print engineer, post-pass | gpt-5.6-terra | 22:57:53Z | 23:04:24Z | coupon source, six coupon STLs, manifest, final notes | coupon re-import; slicing/field-test preparation | not exposed |

## Terminal artifact/hash audit

| Artifact | SHA-256 / evidence | Result |
|---|---|---|
| `model.py` | `8152dfd59b0b3b5acf2a930c22a4a8da855f0b175148e6cfa2ea996ed9f1dceb` | present |
| `verify.py` | `6e639060cc73b6e8fe25ec63b996ead1c186c07276f64a52863a74a84a07b4e5` | present; non-authoritative designer evidence |
| final STL | `71b02364941f10cf1d6f097ecdae677f8cfc550c34af393f1355dc3283d7fa44` | re-imported and passed in verification r3 |
| final STEP | `fd54b83e9bdcbc177e7ca5dd8a87478a68210494b498a2f9f14cc2636ebde257` | present |
| verification report | `08cf6b7f9017b82331fb4f6660fad4168237b97fa817cf26562396f1239a4d80` | r3 PASS; canonical equals verifier artifact |
| final print notes | `0b7cb1a16ba22474ce127c7e7b1c35347c9cd6d55371a181b90e7998aa963bda` | present |
| fit coupons | `fit_coupon_manifest.md` lists six re-imported watertight TPU coupon STLs | present |

## Pipeline ledger

| Phase | Terminal state | Evidence |
|---|---|---|
| Metrology and blind reference | PASS after r1 sheet rejection/correction | dimensions.md r3; evidence/reference/ref-2/metrologist_acceptance.md |
| Pre-design print plan | PASS | print_plan.md r1 |
| Candidate and correction loops | PASS after two geometry rejections | evidence/candidates/cq-a-r3/designer_handoff.md |
| Fresh verification | PASS | verification_report.md r3; evidence/verification/cq-a-r3/v1/ |
| Post-pass preparation | PASS | fit_coupon_manifest.md; print_notes.md |
| Delivery | DELIVERED | job_state.md r16 |
