# V3 runtime ledger — round3-t2-team-v3

| UTC | Event | Detail |
|---|---|---|
| 2026-07-23T22:15:00Z | intake | PIPELINE/COMPACT route; CadQuery only; FreeCAD/web/prohibited artifacts excluded. |
| 2026-07-23T22:15:00Z | telemetry | Runtime token telemetry: not exposed. No estimates will be made. |
| 2026-07-23T22:15:00Z | commissions | Specialist commission count: 0 completed / 0 dispatched at ledger creation. |
| 2026-07-24T01:05:11Z | M1 receipt | dimensions.md r1 received; SHA-256 b57372a2b5e7204797d8a4afe744f3c3949a689bd443cfb8909dea4ae21f3286; status REFERENCE_REVIEW. |
| 2026-07-24T01:06:22Z | commissions | Specialist commission count: 1 completed / 2 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:09:40Z | D1 receipt | Blind reference receipt complete; reference.stl SHA-256 25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a. |
| 2026-07-24T01:09:40Z | commissions | Specialist commission count: 2 completed / 3 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:12:19Z | M2 receipt | dimensions.md r2 ACCEPTED after matching top overlay; dimensions SHA-256 c4a191705373c129b928dfbdd88b86db29455895a7e0bcadecb6fc85044b1510. |
| 2026-07-24T01:13:05Z | commissions | Specialist commission count: 3 completed / 4 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:15:00Z | P1 receipt | print_plan.md r1 ACCEPTED; SHA-256 6adce7277f4348db86add4c06e918b7e8b390af821822b6e05840d6c8171dfe2. |
| 2026-07-24T01:16:01Z | commissions | Specialist commission count: 4 completed / 5 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:27:43Z | D2 receipt | candidate_readiness.md READY for cq-a; recomputed final STL SHA-256 f10cc046b6a6ff84063a265dcd1e2b2625c7617fa6f7eecc47e3bf864c0e96b4. |
| 2026-07-24T01:27:43Z | commissions | Specialist commission count: 5 completed / 6 dispatched; fresh verifier contexts: 1 (`v3_verifier`). Token telemetry: not exposed. |
| 2026-07-24T01:35:24Z | V1 receipt | REJECT on candidate STL f10cc046b6a6ff84063a265dcd1e2b2625c7617fa6f7eecc47e3bf864c0e96b4: V1-01 P_BED is not lowest and 1112.523 mm2 non-P_BED downface violates G-06/SS-01/SS-04. V1-02 coupon completeness is deferred to P2 by the explicit task sequence and print-plan final gate. |
| 2026-07-24T01:37:06Z | loops | Candidate correction loop 1: D2 re-engaged for V1-01 only; candidate bytes will change and require a new fresh full verifier. Specialist commission count: 6 completed / 7 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:40:21Z | D2 correction receipt | corrected candidate readiness READY; recomputed STL SHA-256 b2b13f8a953a7e11d00d0d503f830715843f2e8463da9c173099188e505059ca. |
| 2026-07-24T01:40:21Z | commissions | Specialist commission count: 7 completed / 8 dispatched; fresh verifier contexts: 2 (`v3_verifier`, `v3_verifier_v2`). Token telemetry: not exposed. |
| 2026-07-24T01:45:01Z | V2 receipt | REJECT on candidate STL b2b13f8a953a7e11d00d0d503f830715843f2e8463da9c173099188e505059ca: V2-01 E-02 re-imported edge samples are sharp 90-degree junctions, violating G-05. |
| 2026-07-24T01:46:07Z | loops | Candidate correction loop 2: D2 re-engaged for V2-01; changed bytes require a third fresh seven-check verifier. Specialist commission count: 8 completed / 9 dispatched. Token telemetry: not exposed. |
| 2026-07-24T01:55:27Z | D2 correction receipt | corrected candidate readiness READY; E-02 re-imported samples 1.599570..1.799519 mm; recomputed STL SHA-256 bafb6b7e19a35c602ae105e3c79338db92c0e5a91cc7f2ce4563d8d1e4e0d112. |
| 2026-07-24T01:55:27Z | commissions | Compact-path hypothesis failed: 9 completed / 10 dispatched specialist commissions exceeds the <=8 target; correction loops 2 exceeds normal one-candidate expectations. Fresh verifier contexts: 3 (`v3_verifier`, `v3_verifier_v2`, `v3_verifier_v3`). Token telemetry: not exposed. |
| 2026-07-24T02:03:25Z | V3 receipt | REJECT on candidate STL bafb6b7e19a35c602ae105e3c79338db92c0e5a91cc7f2ce4563d8d1e4e0d112: V3-01 re-imported E-01 grip rim samples remain sharp, violating G-05. |
| 2026-07-24T02:03:25Z | loops | Candidate correction loop 3 begins; compact-run threshold remains failed. A changed STL requires a fourth fresh verifier. Specialist commission count: 10 completed / 11 dispatched. Token telemetry: not exposed. |
| 2026-07-24T02:08:20Z | D2 final diagnostic receipt | Final candidate readiness READY, complete E-01..E-07 re-imported edge audit recorded; STL SHA-256 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df. |
| 2026-07-24T02:08:20Z | commissions | Specialist commission count: 11 completed / 12 dispatched; fresh verifier contexts: 4 (`v3_verifier`, `v3_verifier_v2`, `v3_verifier_v3`, `v3_verifier_v4`). Compact-path hypothesis remains failed. Token telemetry: not exposed. |
| 2026-07-24T02:15:12Z | V4 receipt | PASS on candidate STL 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df; verification report SHA-256 18c6a90899de64f8fd1051d643827c03e09b8956e226c4ee2e92cadc34e47a3b. |
| 2026-07-24T02:15:12Z | commissions | Specialist commission count: 12 completed / 13 dispatched; P2 resumes original print engineer `v3_print`; fresh verifier contexts: 4. Token telemetry: not exposed. |
| 2026-07-24T02:19:29Z | P2 receipt | COMPLETE final_print_prep; real production-geometry coupon STL SHA-256 2a08ab48731ad4e1a305cf06d4d45d736c0f1c22fd2f8519a58ed1a7805b0f84; final STEP SHA-256 ecafce833ab955e8f945b0c644388615806b6a9deda24d68f24b43b238accf21. |
| 2026-07-24T02:19:29Z | delivery | DELIVERY: final STL SHA-256 39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df; verification report PASS SHA-256 18c6a90899de64f8fd1051d643827c03e09b8956e226c4ee2e92cadc34e47a3b; final prep COMPLETE SHA-256 161823cd1cd68203c262b0e7c73af87c22cf68ee632c675051539a9317f399c0. |
| 2026-07-24T02:19:29Z | footprint | Non-cache output: 61 files, 3,658,970 bytes (recursive files excluding `__pycache__`). This includes retained isolated reference/verifier evidence and rejected-loop artifacts. |
| 2026-07-24T02:19:29Z | final telemetry | Specialist commissions: 13 dispatched / 13 completed. Fresh verifier contexts: 4. Candidate correction loops: 3. Compact-path gate: FAIL (>8 commissions and >normal correction loops). Runtime token telemetry: not exposed; no estimate made. |
| 2026-07-24T02:19:29Z | physical gate | Delivery is design/preparation complete. PETG coupon must be physically printed and pass the documented real-bar engagement test before final-tool slicing/printing. |
