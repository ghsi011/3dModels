# Team pipeline runtime contracts v2

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
contract_version: 2
job_id: <slug>
revision: <integer>
owner: orchestrator
mode: SOLO | PIPELINE
profile: COMPACT | FULL
state: INTAKE | METROLOGY | REFERENCE_BUILD | REFERENCE_ACCEPTANCE | PRINT_PLAN | CANDIDATE_BUILD | INDEPENDENT_VERIFICATION | PRINT_PREP | DELIVERY | BLOCKED
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
contract_version: 2
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
contract_version: 2
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

## Geometry rules
| ID | Wall/feature/clearance/support/chamfer rule | Numeric limit | Verification predicate |
|---|---|---:|---|

## Coupon
| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|

## Final-prep placeholders
<slicer/profile, order, inspection, field test>
```

The transform is a design input, not prose. Prefer one multi-lane coupon STL. Add separate
coupon files only when disjoint interfaces cannot be tested together.

## `candidate_readiness.md`

This is designer-owned dispatch evidence. It is never acceptance and never substitutes for
fresh verification.

```markdown
---
contract: candidate-readiness
contract_version: 2
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

## Parameter mapping
| Contract IDs | Source parameter(s) |
|---|---|

## Commands and hashes
<reproducible commands and output paths>
```

The orchestrator recomputes presence and hashes. `NOT_READY` stays inside the same designer
commission until corrected; no verifier is dispatched.

## `verification_report.md`

```markdown
---
contract: verification-report
contract_version: 2
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
