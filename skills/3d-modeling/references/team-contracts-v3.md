# Team pipeline runtime contracts v3

This is the compact runtime schema for the five-role pipeline. It preserves the semantic
fields and gates in `skills/team-design.md` while avoiding rereading the full architecture
document on every commission.

Rules:

- Tables may add rows but may not remove columns.
- Every contract uses millimetres unless a row says otherwise.
- `A` = direct measurement, `B` = authoritative/corroborated, `C` = image-derived,
  `D` = assumption.
- Hashes bind agents to files. Chat is never a contract.
- Compact means fewer repeated words and images, not fewer datums, sources, checks, or
  uncertainties.

## `job_state.md`

```markdown
---
contract: job-state
contract_version: 3
job_id: <slug>
revision: <integer>
owner: orchestrator
mode: SOLO | PIPELINE
profile: COMPACT | FULL
state: INTAKE | METROLOGY | REFERENCE_BUILD | REFERENCE_ACCEPTANCE | PRINT_PLAN | CANDIDATE_BUILD | INDEPENDENT_VERIFICATION | PRINT_PREP | FINAL_PREP_REVIEW | DELIVERY | BLOCKED
backend: cadquery | freecad
active_candidate: <id-or-none>
updated_utc: <iso-8601>
---

# Job state

## Route
<criterion and reason>

## Bound inputs
| Contract/evidence | Revision/hash | Status |
|---|---|---|

## Gates
| Gate | Required receipt | Result | Evidence |
|---|---|---|---|

## Dispatches
| ID | Role/commission | Authorized inputs | Required output | Budget min | Status |
|---|---|---|---|---:|---|

## Open user questions
| ID | Question | Blocks |
|---|---|---|
```

Use `COMPACT` for a single candidate and one uncomplicated mating envelope. Use `FULL` for
multi-part/moving mechanisms, safety/load consequences, several independent interfaces,
multi-colour alignment, or parallel candidates. Both profiles run the same gates.

## `dimensions.md`

```markdown
---
contract: dimensions
contract_version: 3
job_id: <slug>
revision: <integer>
owner: metrologist
status: DRAFT | REFERENCE_REVIEW | ACCEPTED | BLOCKED
updated_utc: <iso-8601>
---

# Dimensions

## Frame
| Axis/datum | Definition | Source | Confidence |
|---|---|---|---|

## Sources
| ID | Evidence path/URL | Variant | SHA-256 or access date | Authority/limits |
|---|---|---|---|---|

## Blind-build completeness
| Feature ID | Name/count/function | Datum value or bounded envelope | Source | Confidence | Candidate response | Ready |
|---|---|---|---|---|---|---|

## Dimensions
| ID | Feature | Value/range | Datum/method | Source | Confidence | Tolerance/design response |
|---|---|---:|---|---|---|---|

## Open questions
| ID | Unknown | Risk | Approved bound/question | Blocks |
|---|---|---|---|---|

## Reference round trip
| Build ID/hash | Views/overlay | Verdict | Sheet revision required |
|---|---|---|---|
```

Every visible feature must appear in blind-build completeness. A cosmetic feature may use a
visual/bounded envelope, but cannot be omitted. Camera, control, connector, protective-lip,
handed, load, and clearance features are functional.

## `print_plan.md`

```markdown
---
contract: print-plan
contract_version: 3
job_id: <slug>
revision: <integer>
owner: print-engineer
status: DRAFT | ACCEPTED | BLOCKED
dimensions_revision: <integer>
reference_sha256: <hash>
updated_utc: <iso-8601>
---

# Print plan

## Process
| Printer/material/nozzle | Layer | Environment/load | Rationale |
|---|---:|---|---|

## Model-to-printer transform
| Item | Exact value |
|---|---|
| Transform/rotation | <matrix or ordered rotations> |
| Bed-contact landmark | <named face/datum> |
| Bed normal | <vector> |
| Open/insertion direction | <vector> |
| Forbidden downward faces | <feature IDs> |

## Geometry rules and phase scope
| ID | Rule | Numeric limit | Verification predicate | required_now | deferred_owner | final_gate |
|---|---|---:|---|---|---|---|

## Coupon
| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|

## Final-prep placeholders
<slicer/profile, order, inspection, field test>
```

The transform is a design input, not prose. Prefer one multi-lane coupon STL. Add separate
coupon files only when disjoint interfaces cannot be tested together.

Every geometry rule freezes what must be proved before candidate verification and what, if
anything, is deferred:

- `required_now` names the exact candidate/readiness and verifier evidence required in the
  current phase.
- `deferred_owner` is `none` or one later owner with concrete artifact names.
- `final_gate` is `none` or the exact later state blocked until those artifacts are reviewed.
- An accepted plan revision may not move a failed or omitted `required_now` predicate to a
  later owner for the same candidate hash.

Classify every transformed downface, bridge, roof, or layer-transition predicate as
`SELF_SUPPORT_REQUIRED` or `SUPPORT_ALLOWED`. `SELF_SUPPORT_REQUIRED` requires a zero
out-of-limit result in both readiness and check 7. `SUPPORT_ALLOWED` requires a named mesh
region, exact transform/nozzle/line-width/layer range, quantified footprint or interval,
one permitted nonfunctional contact class, enumerated forbidden faces, and named post-print
artifacts. No unplanned region may become support-allowed after it fails verification.

## `candidate_readiness.md`

This is designer-owned dispatch evidence. It is never acceptance and never substitutes for
fresh verification.

```markdown
---
contract: candidate-readiness
contract_version: 3
job_id: <slug>
candidate_id: <id>
owner: cad-designer
status: READY | NOT_READY
non_acceptance: true
dimensions_revision: <integer>
print_plan_revision: <integer>
reference_sha256: <hash>
candidate_stl_sha256: <hash>
updated_utc: <iso-8601>
---

# Candidate readiness — DESIGNER SELF-CHECK, NON-ACCEPTANCE

| Pre-dispatch check on re-imported STL | Required | Observed | Result | Evidence |
|---|---:|---:|---|---|
| One watertight intended body and bounds | yes | | | |
| Seated interference | plan threshold | | | |
| Full insertion/travel sweep | zero forbidden collision | | | |
| Installed-coordinate section proves architecture/open face | yes | | | |
| Named bed face at printer Z=0 after exact transform | yes | | | |
| Unsupported roof/critical wall floors | plan limits | | | |
| Required renders/STEP/source present | yes | | | |

## Edge/comfort preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE
| Edge ID / feature boundary | Exposure class | Required radius or allowed-sharp condition | Re-imported-STL samples/method | Observed min/max | Result | Evidence |
|---|---|---|---|---:|---|---|

## Support-sensitivity preflight — DESIGNER SELF-CHECK, NON-ACCEPTANCE
| Rule/region ID | Exact transform/layer/nozzle predicate | Mesh result/footprint/interval | Plan disposition | Allowed contact class and forbidden faces checked | Result | Evidence |
|---|---|---|---|---|---|---|

## Parameter mapping
| Contract IDs | Source parameter(s) |
|---|---|

## Commands and hashes
<reproducible commands and output paths>
```

The orchestrator recomputes presence and hashes. `NOT_READY` stays inside the same designer
commission until corrected; no verifier is dispatched.

Give every opening boundary, protective lip, exterior user-touch boundary, removal/grip edge,
and plan-named exposed edge an Edge ID. Classify it as `EXPOSED_FUNCTIONAL`,
`EXPOSED_COMFORT`, `HIDDEN`, `BED_CONTACT`, or `PERMITTED_SUPPORT_CONTACT`. An exposed edge
may remain sharp only with a feature-specific plan reason and allowed-sharp condition.
Otherwise sample the re-imported STL at both endpoints and one interior point. A nominal
0.40 mm round must measure 0.38–0.42 mm at every sample. Source fillets, renders, and global
sharp-edge counts are not measurements. These checks are dispatch preflight only; the fresh
verifier independently repeats the applicable sections.

## `verification_report.md`

```markdown
---
contract: verification-report
contract_version: 3
job_id: <slug>
revision: <integer>
owner: verifier
status: PASS | REJECT
candidate_id: <id>
candidate_stl_sha256: <hash>
dimensions_revision: <integer>
print_plan_revision: <integer>
reference_sha256: <hash>
fresh_context: true
updated_utc: <iso-8601>
---

# Independent verification

## Input/upstream audit
| Input/claim | Expected revision/hash/datum | Independent observation | Result | Evidence |
|---|---|---|---|---|

## Seven checks on re-imported exported STL
| Check | Method | Numeric result | Visual observation | Result | Evidence |
|---|---|---:|---|---|---|
| 1 interference | | | | | |
| 2 full insertion/travel sweep | | | | | |
| 3 section | | | | | |
| 4 same-view/photo overlay look | | n/a | | | |
| 5 named-datum feature positions/handedness | | | | | |
| 6 measurement-to-geometry audit | | | | | |
| 7 planned-orientation printability/faces | | | | | |

## Defects
| ID | Owning loop | Feature/check IDs | Expected vs observed | Evidence | Required acceptance condition |
|---|---|---|---|---|---|

## Verdict
<PASS, or REJECT to METROLOGY / PRINT_PLAN / CANDIDATE_BUILD>
```

The verifier treats `candidate_readiness.md` as untrusted completeness evidence and reruns
all seven checks. Every changed STL hash requires a new fresh verifier context.

The verifier also independently repeats declared edge sections in check 6. In check 7 it
recomputes every `SELF_SUPPORT_REQUIRED` predicate and every `SUPPORT_ALLOWED`
footprint/classification. Visual inspection, not an isometric scalar claim, establishes
whether a support contact class is plausible.

## Plan-revision rule

A plan revision requires a new candidate-readiness receipt and a new fresh full seven-check
verification, even for the same STL hash, when it changes transform, bed landmark, open
direction, material, nozzle, layer or line width, shrink/clearance, walls, overhangs,
bridges, edge/comfort rules, loads, colour, support disposition, permitted contact class,
forbidden faces, or any acceptance threshold/evidence scope. A revision that only adds
post-verification artifacts under an unchanged bound plan requires the applicable final-prep
review, not seven checks. Metadata or coupon elaboration that changes no candidate predicate
requires neither. A failed `required_now` predicate can never be downgraded to deferred.

## `final_print_prep.md`

This is print-engineer-owned manufacturing evidence. Candidate `PASS` is not permission to
claim this receipt is complete.

```markdown
---
contract: final-print-prep
contract_version: 3
job_id: <slug>
owner: print-engineer
status: COMPLETE | READY_FOR_REVIEW | BLOCKED_NATIVE_SLICER | REJECTED
candidate_stl_sha256: <hash>
print_plan_revision: <integer>
verification_report_revision: <integer>
updated_utc: <iso-8601>
---

# Final print preparation

| Required P2 item | Plan rule/final gate | Observed artifact/hash | Result |
|---|---|---|---|
| Coupon source/export and pass/fail lanes | | | |
| Slicer/profile or reproducible settings | | | |
| Underside support-contact view, when required | | | |
| Section/toolpath view per support interval, when required | | | |
| Layer/contact map per support footprint, when required | | | |
| Transform/profile/nozzle/material match | | | |
| Print order, inspection, and field-test protocol | | | |
```

Use `COMPLETE` only when every plan-deferred item is satisfied and none requires independent
visual contact/toolpath review. Use `READY_FOR_REVIEW` when the plan relies on
`SUPPORT_ALLOWED` or another slicer-dependent visual predicate; the verifier then writes
`final_prep_review.md`. Support-free parts with zero out-of-limit regions need concrete
slicer settings and a coupon, but not a native project solely for ceremony.

## `final_prep_review.md`

```markdown
---
contract: final-prep-review
contract_version: 3
job_id: <slug>
owner: verifier
status: FINAL_PRINT_PASS | FINAL_PRINT_REJECT | FINAL_PRINT_BLOCKED
candidate_stl_sha256: <hash>
print_plan_revision: <integer>
final_print_prep_sha256: <hash>
updated_utc: <iso-8601>
---

| Deferred plan predicate | Independent visual/numeric observation | Result | Evidence |
|---|---|---|---|
```

This review does not rerun all seven candidate checks unless the STL or a candidate predicate
changed. It inspects actual support contacts, toolpaths, and layer maps against the unchanged
accepted plan. Missing coverage, forbidden/exposed-edge contact, or an unmapped footprint
rejects final prep.

If a plan-required native slicer cannot launch, import the candidate, save its project, or
show contacts/toolpaths, write `BLOCKED_NATIVE_SLICER` with command/version, candidate and
plan hashes, missing capability, and required owner action. Do not claim native proof or
Ready to Print. A reproducible portable fallback may be labelled `NON_NATIVE`, but it remains
`FINAL_PRINT_BLOCKED` unless the user explicitly approves that exception.
