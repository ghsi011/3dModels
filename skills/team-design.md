# Multi-agent split design for `3d-modeling`

Status: approved and implemented. The existing `skills/3d-modeling/` skill remains the
unchanged solo workflow; the five slices and their runtime definitions implement team mode.

## 1. Decision and invariants

The team mode has exactly five roles:

1. Orchestrator
2. Metrologist
3. CAD designer
4. Verifier
5. Print engineer

No sixth role is planned. A separate reference modeler, visual grader, or delivery clerk
would create another lossy handoff. Reference modeling is a CAD designer commission,
visual grading is part of verification, and delivery remains with the orchestrator.

The architecture is built around four non-negotiable findings:

- **One owner for ground truth.** The metrologist is the only writer of
  `dimensions.md`. A number without a feature name, datum, provenance, and confidence is
  not usable geometry.
- **The specification is round-tripped.** A designer builds the mating reference model
  without seeing the photos. The metrologist overlays that result on the photos. A
  mismatch normally means the sheet is incomplete or ambiguous, so the metrologist fixes
  the sheet and commissions a rebuild. The designer does not receive photo-based coaching.
- **Designer and verifier are never the same context.** The verifier starts fresh, looks
  at same-view renders and photo overlays, and does not trust the designer's `verify.py`
  or prose. It may reject but may not repair.
- **DFM starts before CAD.** The print engineer issues orientation, material, nozzle,
  wall, feature, support, and bed-edge constraints before candidate modeling. The designer
  still reads `fdm-design.md`; the verifier checks the exported STL against the actual
  print plan.

All role-to-role communication is through versioned files in the project folder. Chat
summaries, agent return messages, and hidden context are not contracts and must not be used
to continue the job.

## 2. Runtime modes

### 2.1 Routing rule

The orchestrator records one routing decision before dispatch:

| Question | Yes | No |
|---|---|---|
| Does the part mate with, replace, enclose, align to, or travel over a real object where a dimensional error can prevent function? | Pipeline | Continue |
| Are there two or more interacting printed or non-printed parts, including print-in-place mechanisms? | Pipeline | Continue |
| Did the user explicitly request team mode? | Pipeline | Continue |
| Otherwise |  | Solo |

The first two criteria are the agreed scope: fit-critical or multi-part work uses the
pipeline. A decorative, single-body, non-mating part stays solo even if it is visually
elaborate. When uncertain whether a dimension can cause functional failure, route to the
pipeline and record the reason.

### 2.2 Solo mode

- One agent runs the existing `skills/3d-modeling/SKILL.md` end to end.
- No slice replaces or wraps the monolith.
- The monolith, its references, and scripts remain unchanged.
- Existing Phase 4 and delivery rules still apply.

### 2.3 Pipeline mode

- The orchestrator uses only the role slices and the file contracts below.
- Each dispatch names the authorized input paths, output paths, contract revisions, and
  candidate ID.
- A role re-reads its inputs from disk at the start of every commission.
- A completed agent message is only a completion signal. The next role reads the files,
  not the message.

### 2.4 Invocation contract

`AGENTS.md` defines these entry points:

- A normal new modeling request enters through the `3d-orchestrator` skill in the main/root
  session. It records the routing decision and either dispatches one monolith agent or
  starts the pipeline.
- Explicit `/3d-modeling <request>` means direct solo mode with the unchanged monolith.
- Explicit `/3d-orchestrator <request>` or "use the 3D team" means pipeline mode and
  records the explicit-team routing criterion.
- A follow-up on an already-routed project resumes from `job_state.md`; it does not
  silently reroute from prose.

Claude Code currently does not permit a nested subagent to spawn other subagents. Therefore
Claude users keep orchestration in the main session or launch
`claude --agent 3d-orchestrator`; its specialist definitions are then dispatched by that
top-level context. Codex runtimes may dispatch the slices directly from the root agent.
Runtime model selection belongs to the launcher: the contract architecture does not depend
on a vendor model name.

## 3. Project file protocol

### 3.1 Canonical layout

```text
<project>/
  job_state.md
  dimensions.md
  print_plan.md
  verification_report.md
  print_notes.md
  evidence/
    input/                         # original photos and caliper images, immutable
    metrology/                     # crops, annotations, source captures
    reference/                     # reference renders, STL/STEP, overlays
    candidates/
      cq-a/                        # or freecad-a
      cq-b/
    verification/
      cq-a/
      cq-b/
  reference.py                     # CadQuery pipeline intermediate, if used
  model.py                         # selected CadQuery candidate source
  verify.py
  <project>.FCStd                  # FreeCAD alternative, with hidden RefPart
  <part>.stl
  <part>.step
  <part>_fit_coupon.stl
  <project>.3mf
```

Parallel CadQuery candidates write only inside their own `evidence/candidates/<id>/`
folders until one is selected. The orchestrator promotes the selected source and exports
to the project root. No two agents write the same path concurrently.

### 3.2 Contract rules

- `job_state.md` has one writer: the orchestrator.
- `dimensions.md` has one writer: the metrologist.
- `print_plan.md` has one writer: the print engineer.
- Each fresh verifier writes
  `evidence/verification/<candidate>/<run>/verification_report.md` in its isolated run
  folder. After selection, the orchestrator promotes that file byte-for-byte to canonical
  `verification_report.md`; it does not edit or reinterpret the verifier's content.
- Every contract has `contract_version`, `job_id`, `revision`, `status`, and `owner`.
- Downstream contracts bind the exact upstream revisions and SHA-256 hashes they used.
- A changed upstream contract invalidates every downstream gate. The orchestrator marks
  those states stale and redispatches from the earliest changed contract.
- Original input photos are immutable. Derived crops, renders, composites, and overlays
  are append-only evidence.
- Every artifact path is project-relative. Runtime hashes are computed, never guessed.
- `model.py`, `reference.py`, `.FCStd`, `verify.py`, and geometric exports are authored
  only by the active designer commission. Promotion copies bytes without changing them;
  the verifier never edits them.
- Each candidate designer owns its isolated
  `evidence/candidates/<id>/print_notes.md` through `CANDIDATE_READY` and writes geometry,
  parameter-fix, and geometric-risk sections. After a candidate passes and is selected,
  the orchestrator promotes the file to the root. Ownership then transfers once to the
  print engineer, who finalizes coupon, slicing, print-order, and field-test sections.
  There is never simultaneous ownership.

## 4. Role charters

### 4.1 Orchestrator

**Charter**

Own control flow, not geometry. Choose solo or pipeline, maintain state, ask the user the
smallest blocking questions, dispatch role commissions, enforce revision gates, serialize
FreeCAD, select among verified candidates, update the Notion Print Queue, deliver files,
and commit meaningful iterations.

**Inputs**

- User request and answers
- Repository `AGENTS.md`
- All contract headers and gate results
- Agent completion signals, used only to know when to read files

**Outputs**

- `job_state.md`
- Dispatch commissions naming file paths and revisions
- Notion queue transitions
- Git commits and final delivery

**Required reading**

- Its own slice, including the routing and state tables in this document
- Existing `skills/3d-modeling/SKILL.md` only when it selects solo mode
- No geometry-pattern reference in pipeline mode

**Checklist**

- Record solo or pipeline with the triggering criterion.
- Gather function, loads, environment, printer, filament, visible faces, color/text needs,
  project path, and queue target in one pointed round where possible.
- Create or update the queue entry to `To Design / Tweak` when design starts.
- Reject dispatch if an input contract is not at the required accepted revision.
- Give the blind reference designer only `dimensions.md` plus its skill references.
- Never send a chat summary as design input.
- Allow at most one active FreeCAD owner.
- Route every rejection to the contract owner named by the report.
- Commit after each meaningful physical design iteration with a message describing the
  physical change.
- Deliver all required files and move the queue to `Ready to Print` only after final prep.
- Never create, edit, repair, or approve geometry.

### 4.2 Metrologist

**Charter**

Own the job's real-world truth. Convert photos, calipers, official specifications, and
approved assumptions into a feature-complete, datum-based `dimensions.md`. Specify the
mating object but do not model it. Own photo crops, annotations, and the operational
render-over-photo overlay method.

**Inputs**

- Original photos and caliper images
- Product identifiers and user answers
- Official specifications and existing third-party model evidence
- Blind reference exports and renders during the round-trip gate

**Outputs**

- `dimensions.md`
- Annotated crops in `evidence/metrology/`
- Reference overlay evidence and round-trip acceptance in `evidence/reference/`

**Required reading**

- `skills/3d-modeling/references/cadquery-patterns.md`, only the named-datum,
  same-camera, and render-over-photo overlay sections
- `skills/3d-modeling/scripts/preview.py`
- `experiments/overlay_photo.py` as the existing operational overlay tool

**Checklist**

- Inspect every photo at maximum useful zoom and save relevant crops.
- Inventory steps, collars, rails, ribs, clips, buttons, windows, tapers, flats, threads,
  and all other visible features before recording dimensions.
- Define a right-handed coordinate frame and named datums before feature positions.
- Give every feature a stable ID and every number a unit, tolerance or uncertainty,
  provenance, confidence grade, and datum relationship.
- Distinguish a solid collar from the envelope across discrete rails or ribs.
- Record every pocket and cutout center from named datums, including handedness.
- For a known product, search official drawings/specifications, cross-check two sources,
  search model repositories, and still confirm the user's unit and variant from photos and
  calipers.
- Ask ambiguous measurement questions by naming the feature and exact caliper contact
  points.
- Block fit-critical unapproved assumptions. An approved bounded assumption must name the
  robustness strategy or coupon that will retire it.
- For the blind reference round trip, overlay exported reference boundaries on the photos
  from top/front/side or iso views as available and actually inspect the images.
- If the reference misses a photo feature, revise the sheet first. If a clear sheet was
  implemented incorrectly, reject by feature ID without revealing new photo geometry.
- Never edit `reference.py`, `.FCStd`, candidate source, or verification code.

**Confidence grades**

| Grade | Meaning | Gate treatment |
|---|---|---|
| A | Direct caliper measurement or an official drawing with an unambiguous datum, confirmed against the user's variant | Fit-critical use allowed |
| B | Derived from two independent sources or a scaled/orthographic photo with a known reference, cross-checked visually | Allowed with stated tolerance |
| C | Single-photo estimate, third-party model, family-level spec, or user-approved assumption | Fit-critical use requires a bounded design response and coupon, variant, or user approval |
| U | Unknown, contradictory, or missing | Blocks the dimensions gate |

### 4.3 CAD designer

**Charter**

Build geometry from file contracts. The same slim slice is instantiated with one of two
commissions: `REFERENCE` or `CANDIDATE`. A hard CadQuery job may use two or three isolated
candidate instances with different stated approaches.

**REFERENCE commission**

- Read `dimensions.md` but not input photos, metrology crops, or photo-derived chat.
- Build the complete mating object, including every feature ID.
- Export a reference STL/STEP and same-view renders requested by `dimensions.md`.
- For CadQuery, write `reference.py` exposing `ref_part`; the selected candidate
  `model.py` imports it and does not export it as a deliverable part.
- For FreeCAD, create `RefPart` in the project `.FCStd`; later candidate work continues
  serially in that document and hides `RefPart` for final renders and exports.

**CANDIDATE commission**

- Read the user-requirement section of `job_state.md`, accepted `dimensions.md`, the
  accepted reference model, and accepted `print_plan.md`.
- Build the functional part to all three contracts.
- Keep every measured dimension and clearance as a named parameter with units and
  provenance.
- Produce source, `verify.py`, exports, renders, and the designer-owned sections of
  `print_notes.md`.

**Required reading**

- Exactly one backend file per part:
  - `skills/3d-modeling/references/cadquery-patterns.md`, or
  - `skills/3d-modeling/references/freecad-mcp-patterns.md`
- Always `skills/3d-modeling/references/fdm-design.md`
- `skills/3d-modeling/references/mechanisms.md` only when the contract includes a hinge,
  spring, flexure, magnet, pin, or printed motion

**Checklist**

- Do not mix backends within a part.
- Choose geometry consistent with the plan's already-decided print orientation.
- Encode support avoidance, bed chamfers, layer-versus-load direction, compliant fits,
  clearances, and color boundaries in CAD.
- Keep function slicer-agnostic.
- Build in small steps; after each boolean/chamfer/fillet, check validity, volume, bbox,
  and a preview. CadQuery work must account for the documented OCC corruption and volume
  traps.
- Use per-side clearance convention.
- Make a failed fit a named one-parameter correction.
- Export CadQuery STLs with tolerance `0.01` and angular tolerance `0.1`.
- Produce self-checks, but label them `DESIGNER SELF-CHECK - NON-AUTHORITATIVE`.
- Never write `verification_report.md` or claim acceptance.

### 4.4 Verifier

**Charter**

Act as an independent acceptance authority in a fresh context. Audit the upstream
dimensions against the photos, audit geometry against the print plan, and run all seven
Phase 4 checks on the exported STL re-imported. Reject with evidence and concrete defect
IDs. Never fix source or contracts.

**Inputs**

- Original photos
- User requirements from `job_state.md`
- Accepted `dimensions.md`
- Accepted `print_plan.md`
- Accepted reference artifacts
- Candidate source for audit, but exported STL/STEP as the measured artifact
- Designer renders and `verify.py` as untrusted evidence

**Outputs**

- `verification_report.md`
- Same-camera composites, section images, photo overlays, and check logs under
  `evidence/verification/<candidate>/<run>/`

**Required reading**

- `skills/3d-modeling/references/cadquery-patterns.md`, Phase 4, named-datum,
  overlay, and exported-STL printability sections. These trimesh patterns are
  backend-neutral.
- `skills/3d-modeling/references/fdm-design.md`, especially printability, orientation,
  supports, fits, multi-material, environment, and production rules
- For a FreeCAD candidate only,
  `skills/3d-modeling/references/freecad-mcp-patterns.md`, fit verification, renders, and
  exports sections
- `skills/3d-modeling/scripts/preview.py`

**Checklist**

- Start with no designer conversation history.
- Compute and record the candidate STL hash before checking.
- Confirm the dimensions sheet itself matches the photos and that every visible feature
  is present, named, and correctly datum-positioned.
- Confirm the print plan is internally consistent with the printer/nozzle/material.
- Re-import the exported STL and run all seven checks below.
- Open each visual composite and write a feature-by-feature observation before deciding.
- Explicitly test mirror/handedness alternatives.
- Treat a designer self-check as a lead, never as a pass.
- Report `PASS` only when upstream audits and all seven checks pass.
- On failure, identify the owning contract and concrete feature/check IDs.
- Never edit CAD, dimensions, print plan, `verify.py`, or exports.

**Seven required checks**

1. **Seated interference:** candidate intersection with the accepted reference is
   approximately zero at the seated pose, with the numeric tolerance declared.
2. **Full insertion sweep:** test stepped offsets over the entire documented travel,
   including rails, buttons, clips, and taper transitions. A clear seated pose alone does
   not pass.
3. **Section render:** cut the assembly in a useful plane, render it, open it, and record
   what the section demonstrates.
4. **Visual side-by-side and photo overlay:** render from the same cameras as the photos
   or accepted reference, compose one image, and actually compare silhouette, feature
   shape, count, architecture, and position. Use the photo overlay for millimeter-scale
   recreation checks. Visual evidence decides; a nearest-edge score may only trend.
5. **Feature positions:** remeasure every pocket/cutout center from its named datum on the
   exported STL, compare with `dimensions.md`, and check handedness.
6. **Measurement audit:** map every measured or approved dimension ID to geometry.
   An unused value or missing feature is a rejection.
7. **Printability and face audit:** in the exact `print_plan.md` orientation, audit
   overhangs, bridges, walls against planned nozzle/line width, bed chamfers, radii,
   bbox, watertightness, material-sensitive features, and required color bodies.

### 4.5 Print engineer

**Charter**

Own the machine and process in two passes. Before design, issue the geometry-affecting
print contract. After verification, finalize the coupon, slicer notes, print order, and
field-test protocol. Triage failed prints as data.

**Inputs**

- Job function, loads, environment, appearance, printer, and available filament
- Accepted `dimensions.md` and reference envelope
- After verification: accepted candidate exports and `verification_report.md`
- After a print: failure photos, stopping travel, measurements, and slicer observations

**Outputs**

- Pre-design `print_plan.md`
- Final process sections of `print_notes.md`
- Fit coupon STL or an exact coupon extraction commission
- Slicing/project 3MF, print order, and field-test protocol
- Failed-print classification and requested upstream revision

**Required reading**

- `skills/3d-modeling/references/fdm-design.md`
- `skills/3d-modeling/references/printers.md`
- `skills/3d-modeling/references/materials.md`
- `skills/3d-modeling/references/bambu-3mf-authoring.md` only for a print-ready Bambu
  project 3MF
- `skills/3d-modeling/references/troubleshooting.md` only for calibration or failure work
- `skills/3d-modeling/scripts/make_3mf.py` and `make_bambu_3mf.py` when applicable

**Pre-design checklist**

- Confirm the exact printer profile; research and persist a missing profile.
- Select final material from environment and load, never defaulting a car part to PLA.
- Fix the print orientation before CAD and explain load/layer and cosmetic tradeoffs.
- Name nozzle, line/layer assumptions, minimum walls/features, bridge/overhang limits,
  support budget, bed-contact chamfers, seam/cosmetic constraints, and color/nozzle plan.
- On the X2D, reserve main for the model, TPU, and primary CF/finish; use auxiliary for
  limited second color/support, and enforce the dual-nozzle build volume.
- Require function in CAD, not slicer-only rescue settings.

**Post-verification checklist**

- Create a PLA fit coupon from the actual bore/mating region for every fit job.
- State slicing settings, preparation/drying, support interface, print order, and an
  after-import checklist.
- For Bambu project 3MF, round-trip the installed slicer profile, verify the archive
  structurally, and never claim Studio acceptance without launching it.
- Define a physical field test with observable pass/fail and what measurement to report
  if it stops or binds.
- For a failed print, classify `GEOMETRY`, `PROCESS`, or `MIXED`.
  - `GEOMETRY`: send the job back to metrology first when a mating feature was missed,
    rebuild the reference, redesign, and reverify.
  - `PROCESS`: update the print plan/notes using `troubleshooting.md`; do not alter CAD
    unless the plan now imposes a geometric constraint.
  - `MIXED`: reopen both paths.
- Record the lesson in `print_notes.md`.

## 5. Implemented agent definitions

`.claude/agents/` contains one definition per role. The definitions use Claude Code's native
frontmatter and preload exactly one matching slice. Their least-privilege policy is:

| Agent | Tools | Deliberately absent | Model note |
|---|---|---|---|
| `3d-orchestrator` | Read/search, contract write/edit, user questions, Agent dispatch, git, Notion, FreeCAD availability-only call | FreeCAD geometry execution | Inherit the session's capable reasoning model; this role is control-heavy, not vision-heavy |
| `3d-metrologist` | Read/search, image inspection, crops/overlay scripts, web search/fetch, write/edit only its contract/evidence | FreeCAD/CAD editing, Agent dispatch | Highest-accuracy vision/reasoning tier |
| `3d-designer` | Read/search, write/edit, Bash/Python, selected backend tools; FreeCAD MCP only for a FreeCAD commission | Notion, Agent dispatch, verifier authority | Highest-accuracy coding/spatial tier |
| `3d-verifier` | Read/search, image inspection, Bash/Python, write its report/evidence | CAD edit tools, Notion, Agent dispatch | Highest-accuracy reasoning/vision tier in a fresh context |
| `3d-print-engineer` | Read/search, write/edit its files, web search/fetch, slicer/3MF scripts | Agent dispatch, candidate CAD editing, Notion | Capable general reasoning tier; elevate for novel materials or failure forensics |

Each definition wires to exactly its matching slice. The agent definition contains tool
and model policy plus an instruction to load the slice; it does not duplicate the workflow.
Each slice itself is limited to charter, inputs/outputs, required shared reading, and
checklist.

For Codex execution, the root loads the same slice path into a dedicated subagent and may
select `gpt-5.6-terra` (as used by the Pixel 10 experiment). The checked-in Claude
definitions use Claude-native `inherit` or `opus` aliases because Claude Code does not
accept Codex model identifiers.

Tool permissions cannot enforce path-level blindness by themselves. The designer skill and
commission therefore make the authorized input list normative. A `REFERENCE` commission
that opens `evidence/input/` is a contract violation and its output is discarded.

## 6. Contract templates

Angle-bracketed values are required substitutions. Literal enum values are shown with
`|`. Tables may gain rows but may not lose columns.

All filled examples are paper examples of the required format. Their placeholder hashes,
evidence paths, timestamps, and verdicts are not claims that those runtime checks already
occurred.

### 6.1 `job_state.md`

This is the orchestrator's control contract. It is not a substitute for any technical
contract.

#### Exact template

```markdown
---
contract: job-state
contract_version: 1
job_id: <stable-slug>
revision: <integer>
owner: orchestrator
mode: SOLO | PIPELINE
state: <state-enum>
backend: FREECAD | CADQUERY | UNDECIDED
active_commission: <role:id | none>
freecad_owner: <commission-id | none>
dimensions_revision: <integer | none>
print_plan_revision: <integer | none>
candidate_id: <id | none>
verification_revision: <integer | none>
updated_utc: <ISO-8601>
---

# Job state

## Routing
- Fit-critical: <yes/no and reason>
- Multi-part: <yes/no and reason>
- Explicit team request: <yes/no>
- Decision: <SOLO/PIPELINE and first matching rule>

## User requirements
- Function:
- Loads and directions:
- Environment:
- Printer:
- Filaments:
- Visible/cosmetic faces:
- Text/colors:
- Project folder:
- Print Queue page:

## Gate ledger
| Gate | Required revision/hash | Result | Evidence |
|---|---|---|---|

## Open user questions
| ID | Blocking state | Question | Answer/status |
|---|---|---|---|

## Dispatch ledger
| Commission | Role | Authorized inputs | Required output | Status |
|---|---|---|---|---|
```

#### Filled example: Berlingo knob v4

```markdown
---
contract: job-state
contract_version: 1
job_id: berlingo-knob-v4
revision: 12
owner: orchestrator
mode: PIPELINE
state: CANDIDATE_VERIFYING
backend: CADQUERY
active_commission: verifier:cq-a-v1
freecad_owner: none
dimensions_revision: 4
print_plan_revision: 1
candidate_id: cq-a
verification_revision: none
updated_utc: 2026-07-24T10:00:00Z
---

# Job state

## Routing
- Fit-critical: yes; the bore must traverse and seat on a photographed gear lever.
- Multi-part: no printed multi-part assembly.
- Explicit team request: no.
- Decision: PIPELINE by fit-critical rule.

## User requirements
- Function: replacement gear-shift knob.
- Loads and directions: hand torque around Z and push/pull during shifting.
- Environment: parked car in Israeli summer.
- Printer: Bambu Lab X2D Combo.
- Filaments: ASA final; PLA coupon.
- Visible/cosmetic faces: bulb and top shift pattern.
- Text/colors: recessed single-color 5+R pattern.
- Project folder: Berlingo gear shift knob/v4-cadquery/
- Print Queue page: <runtime Notion page ID>

## Gate ledger
| Gate | Required revision/hash | Result | Evidence |
|---|---|---|---|
| Dimensions | dimensions r4 | PASS | dimensions.md round-trip section |
| Reference overlay | reference STL runtime hash | PASS | evidence/reference/overlay-side.png |
| Print plan | print plan r1 | PASS | print_plan.md |

## Open user questions
| ID | Blocking state | Question | Answer/status |
|---|---|---|---|
| Q-01 | DIMENSIONS_DRAFT | Does reverse require lifting the collar? | Answered: no, reverse is push-in |

## Dispatch ledger
| Commission | Role | Authorized inputs | Required output | Status |
|---|---|---|---|---|
| ref-1 | designer REFERENCE | dimensions.md r4; selected skill refs | reference.py, reference exports/renders | complete |
| plan-1 | print engineer pre-design | job_state.md r10; dimensions.md r4; accepted ref | print_plan.md r1 | complete |
| cq-a | designer CANDIDATE | dimensions r4; ref hash; print plan r1 | candidate folder | complete |
| cq-a-v1 | fresh verifier | photos; dimensions r4; plan r1; ref; cq-a | verification_report.md | running |
```

### 6.2 `dimensions.md`

#### Exact template

```markdown
---
contract: dimensions
contract_version: 1
job_id: <stable-slug>
revision: <integer>
owner: metrologist
status: DRAFT | BLOCKED | REFERENCE_REVIEW | ACCEPTED
units: mm
source_photo_set: <path>
updated_utc: <ISO-8601>
---

# Dimensions

## Coordinate frame and named datums
- Handedness: right-handed
- +X:
- +Y:
- +Z:
| Datum ID | Definition | Evidence |
|---|---|---|

## Source register
| Source ID | Type | Path/URL | Captured date | Variant relevance |
|---|---|---|---|---|

## Feature inventory
| Feature ID | Name/type | Count | Parent/region | Photo evidence | Functional role |
|---|---|---:|---|---|---|

## Dimension register
| Dim ID | Feature ID | Quantity | Value | Tol/uncertainty | Datum/from-to | Provenance | Confidence | Fit-critical | Approval/status |
|---|---|---|---:|---:|---|---|---|---|---|

## Derived dimensions
| Dim ID | Formula | Inputs | Result | Confidence rule |
|---|---|---|---:|---|

## Assumptions and open questions
| ID | Feature/dim | Risk | Exact question or approved bound | Required response | Status |
|---|---|---|---|---|---|

## Required reference views
| View ID | Photo | Camera/view cue | Features that must align |
|---|---|---|---|

## Blind reference round-trip
- Reference commission:
- Reference artifact SHA-256:
- Sheet revision built:
- Overlay evidence:
| Feature ID | Observation against photo | Result | Sheet action |
|---|---|---|---|
- Round-trip verdict: PENDING | REVISE_SHEET | ACCEPTED
- Accepted by metrologist:
```

#### Filled example: Berlingo lever

```markdown
---
contract: dimensions
contract_version: 1
job_id: berlingo-knob-v4
revision: 4
owner: metrologist
status: ACCEPTED
units: mm
source_photo_set: evidence/input/
updated_utc: 2026-07-24T09:00:00Z
---

# Dimensions

## Coordinate frame and named datums
- Handedness: right-handed
- +X: across the two opposed rails.
- +Y: from lever axis toward the visible clip button.
- +Z: from boot toward lever tip.
| Datum ID | Definition | Evidence |
|---|---|---|
| D0_BOOT | boot surface plane, Z=0 | IMG-01 side |
| D1_AXIS | centerline of Ø12.9 shaft | CAL-01, IMG-02 |
| D2_SEAT | top plane of base plate | IMG-01 side |
| D3_RAIL | midplane through both rails, X axis | IMG-03 top crop |

## Source register
| Source ID | Type | Path/URL | Captured date | Variant relevance |
|---|---|---|---|---|
| IMG-01 | user photo | evidence/input/lever-side.jpg | 2026-07-23 | exact vehicle lever |
| IMG-03 | user photo | evidence/input/lever-rails.jpg | 2026-07-23 | exact rail/button layout |
| CAL-01 | caliper image | evidence/input/caliper-shaft.jpg | 2026-07-23 | direct measurement |

## Feature inventory
| Feature ID | Name/type | Count | Parent/region | Photo evidence | Functional role |
|---|---|---:|---|---|---|
| F-001 | base plate, solid disc | 1 | D0_BOOT to D2_SEAT | IMG-01 | seating depth stop |
| F-002 | smooth shaft | 1 | axis D1_AXIS | CAL-01 | primary sliding mate |
| F-003 | opposed longitudinal rails | 2 | ±X from D1_AXIS | IMG-03 | insertion obstruction/anti-rotation |
| F-004 | dark windows above rails | 2 | above F-003 | IMG-03 | proves rails end before button band |
| F-005 | clip button | 1 | +Y side | IMG-01 | insertion obstruction/possible retention |
| F-006 | tapered tip | 1 | top of F-002 | IMG-01 | bore end clearance |

## Dimension register
| Dim ID | Feature ID | Quantity | Value | Tol/uncertainty | Datum/from-to | Provenance | Confidence | Fit-critical | Approval/status |
|---|---|---|---:|---:|---|---|---|---|---|
| M-001 | F-002 | shaft diameter | 12.9 | 0.1 | across D1_AXIS | CAL-01 direct caliper | A | yes | accepted |
| M-002 | F-002 | exposed length | 72.1 | 0.2 | D0_BOOT to tip | direct caliper record | A | yes | accepted |
| M-003 | F-001 | plate height | 4.0 | 2.0 | D0_BOOT to D2_SEAT | IMG-01 estimate | C | yes | user-approved bound; coupon must confirm seat |
| M-004 | F-001 | plate diameter | 20.0 | 2.0 | centered on D1_AXIS | IMG-01 estimate | C | no | reference-only |
| M-005 | F-003 | one rail width | 5.5 | 0.2 | across each rail | caliper photo | A | yes | accepted |
| M-006 | F-003 | total rail envelope | 16.7 | 0.2 | outer rail face to outer rail face across X | direct caliper; IMG-03 shows two discrete rails | A | yes | accepted; not a collar diameter |
| M-007 | F-003 | rail top Z | 42.8 | 0.4 | D0_BOOT to top of rails | 72.1 - 29.3 direct measurements | A | yes | accepted |
| M-008 | F-005 | button diameter | 8.2 | 0.2 | button circle | caliper photo | A | yes | accepted |
| M-009 | F-005 | button center Z | 47.5 | 2.0 | D0_BOOT to center | IMG-01 estimate | C | yes | approved bound; full path channel required |
| M-010 | F-006 | tip diameter | 6.5 | 0.2 | across tip | direct caliper | A | yes | accepted |
| M-011 | F-005 | button protrusion | 2.0 max | 0.8 | radial from shaft surface | photo-bound assumption, user approved | C | yes | channel must clear at least 2.8 protrusion and coupon must test |

## Derived dimensions
| Dim ID | Formula | Inputs | Result | Confidence rule |
|---|---|---|---:|---|
| D-001 | exposed length - plate height | M-002, M-003 | 68.1 | lower input confidence C |

## Assumptions and open questions
| ID | Feature/dim | Risk | Exact question or approved bound | Required response | Status |
|---|---|---|---|---|---|
| A-01 | M-011 button protrusion | button can jam during insertion | approved upper bound 2.0 mm with 0.8 mm design margin | full-length button channel plus real-bore coupon | approved |

## Required reference views
| View ID | Photo | Camera/view cue | Features that must align |
|---|---|---|---|
| V-SIDE | IMG-01 | side, shaft axis vertical | plate, rail end, window band, button center, taper |
| V-RAIL | IMG-03 | near-orthographic across +Y | two rail silhouettes and 16.7 envelope |

## Blind reference round-trip
- Reference commission: ref-1
- Reference artifact SHA-256: <computed at runtime>
- Sheet revision built: 4
- Overlay evidence: evidence/reference/overlay-side.png; evidence/reference/overlay-rails.png
| Feature ID | Observation against photo | Result | Sheet action |
|---|---|---|---|
| F-001 | plate top aligns with seating plane | pass | none |
| F-003 | two separate rails, width and end height hug photo | pass | none |
| F-005 | button center falls inside approved ±2.0 band | pass | none |
- Round-trip verdict: ACCEPTED
- Accepted by metrologist: metrologist commission meta-r4
```

### 6.3 `print_plan.md`

#### Exact template

```markdown
---
contract: print-plan
contract_version: 1
job_id: <stable-slug>
revision: <integer>
owner: print-engineer
status: DRAFT | BLOCKED | ACCEPTED | FINALIZED
dimensions_revision: <integer>
reference_sha256: <hash>
printer_profile: <exact profile>
updated_utc: <ISO-8601>
---

# Print plan

## Process selection
- Printer:
- Effective build volume:
- Final material and reason:
- Coupon material:
- Main/aux nozzle assignment:
- Nozzle diameter:
- Layer-height assumption:

## Required print coordinate frame
- Bed-contact face/datum:
- Up axis after placement:
- Orientation transform:
- Load/layer rationale:
- Cosmetic rationale:

## Geometry constraints
| Constraint ID | Requirement | Value/limit | Source/rationale | Verification method |
|---|---|---|---|---|

## Supports and bridges
- Support budget:
- Allowed support regions:
- Forbidden support regions:
- Maximum unsupported bridge:
- Designed-support requirement:

## Color/material plan
| Body/region | Material/color | Physical nozzle | Geometry requirement |
|---|---|---|---|

## Coupon contract
- Required before final print:
- Actual mating region to extract:
- Variants/steps:
- Target duration:
- Pass/fail:

## Post-verification prep placeholders
- Slicer profile:
- Walls/top-bottom/infill:
- Drying/preparation:
- Print order:
- Field-test protocol:
- Bambu after-import checks:

## Plan acceptance
- Blocking items:
- Accepted by print engineer:
```

#### Filled example: Berlingo knob v4

```markdown
---
contract: print-plan
contract_version: 1
job_id: berlingo-knob-v4
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 4
reference_sha256: <computed reference STL SHA-256>
printer_profile: Bambu Lab X2D Combo / 0.4 mm
updated_utc: 2026-07-24T09:20:00Z
---

# Print plan

## Process selection
- Printer: Bambu Lab X2D Combo.
- Effective build volume: single-nozzle job; candidate bbox must fit the selected plate.
- Final material and reason: ASA; parked-car temperatures rule out PLA and make PETG marginal.
- Coupon material: PLA.
- Main/aux nozzle assignment: main only; single-color part.
- Nozzle diameter: 0.4 mm hardened nozzle.
- Layer-height assumption: 0.2 mm.

## Required print coordinate frame
- Bed-contact face/datum: knob's flat cosmetic top face.
- Up axis after placement: model -Z points away from bed; knob prints upside down.
- Orientation transform: 180 degrees about model X from its installed pose.
- Load/layer rationale: circumferential hand torque remains primarily in layer planes.
- Cosmetic rationale: recessed 5+R pattern forms in first layers and requires no supports.

## Geometry constraints
| Constraint ID | Requirement | Value/limit | Source/rationale | Verification method |
|---|---|---|---|---|
| P-001 | structural wall | >=1.6 mm or 4 planned lines around bore | fdm-design walls and torque load | exported-STL sections |
| P-002 | absolute wall floor | >=0.8 mm | 2 x 0.4 nozzle | mesh thickness audit |
| P-003 | bed-contact edge chamfer | 0.2-0.4 mm where fit-critical; >=1.0 mm where noncritical | elephant-foot immunity | face/section audit |
| P-004 | engraved stroke | >=0.5 mm wide, 0.5-1.0 mm deep | single-color detail floor | exported-STL measurement |
| P-005 | internal transition | widening upward in print orientation or <=45 degree chamfer | no trapped internal support | overhang/section audit |
| P-006 | functional geometry | no slicer-only bore or channel correction | portable function | source and STL audit |

## Supports and bridges
- Support budget: zero support inside the functional bore; target zero support overall.
- Allowed support regions: none in the accepted concept.
- Forbidden support regions: bore, rail channels, button channels, engraved top.
- Maximum unsupported bridge: 5 mm pristine; longer spans require an accepted designed response.
- Designed-support requirement: none if all internal transitions comply with P-005.

## Color/material plan
| Body/region | Material/color | Physical nozzle | Geometry requirement |
|---|---|---|---|
| knob and recessed pattern | ASA, user color | main | one watertight body; pattern is a recess |

## Coupon contract
- Required before final print: yes.
- Actual mating region to extract: 26 mm slice spanning rail-channel ends, button path,
  upper-bore transition, and enough wall to preserve real stiffness.
- Variants/steps: nominal first; clearance ladder only if nominal binds.
- Target duration: about 15 minutes in PLA.
- Pass/fail: slides over both rails and button without force, reaches the seat flush, and
  has no unacceptable rotational play.

## Post-verification prep placeholders
- Slicer profile: 0.20 mm standard, final selection after verification.
- Walls/top-bottom/infill: 4 walls, 5 top/bottom, 30-40% gyroid unless slice review changes it.
- Drying/preparation: ASA 4-6 h at 80 C; clean textured PEI; Heat Mode 60-65 C.
- Print order: PLA coupon, inspect/measure, then ASA full part.
- Field-test protocol: record stopping distance from seat if the coupon binds.
- Bambu after-import checks: orientation, main nozzle assignment, bed, walls, infill, no internal support.

## Plan acceptance
- Blocking items: none.
- Accepted by print engineer: print-plan-1
```

### 6.4 `verification_report.md`

#### Exact template

```markdown
---
contract: verification-report
contract_version: 1
job_id: <stable-slug>
revision: <integer>
owner: verifier
status: PASS | REJECT | BLOCKED
candidate_id: <id>
candidate_stl: <relative path>
candidate_stl_sha256: <hash>
dimensions_revision: <integer>
print_plan_revision: <integer>
reference_sha256: <hash>
fresh_context: true
updated_utc: <ISO-8601>
---

# Verification report

## Input integrity
| Input | Expected revision/hash | Observed | Result |
|---|---|---|---|

## Upstream dimensions audit against photos
| Feature/dim ID | Photo observation | Sheet statement | Result | Evidence |
|---|---|---|---|---|

## Print-plan audit
| Constraint ID | Candidate observation | Result | Evidence |
|---|---|---|---|

## Seven checks
| Check | Method on re-imported STL | Numeric result | Visual observation | Result | Evidence |
|---|---|---|---|---|---|

## Feature-position register
| Feature ID | Datum | Expected | Observed | Delta | Handedness check | Result |
|---|---|---:|---:|---:|---|---|

## Measurement audit
| Dimension ID | Geometry mapping | Result |
|---|---|---|

## Visual inspection narrative
- Reference/photo row:
- Candidate row:
- Differences:
- Overlay observations:

## Defects
| Defect ID | Owning contract | Feature/check IDs | Concrete defect | Required acceptance condition |
|---|---|---|---|---|

## Verdict
- Result:
- Passed candidate ranking, if comparing candidates:
- Rerun scope:
- Verifier commission:
```

#### Filled example: Berlingo candidate `cq-a`

```markdown
---
contract: verification-report
contract_version: 1
job_id: berlingo-knob-v4
revision: 1
owner: verifier
status: PASS
candidate_id: cq-a
candidate_stl: evidence/candidates/cq-a/knob_v4.stl
candidate_stl_sha256: <computed candidate STL SHA-256>
dimensions_revision: 4
print_plan_revision: 1
reference_sha256: <computed accepted reference STL SHA-256>
fresh_context: true
updated_utc: 2026-07-24T10:30:00Z
---

# Verification report

## Input integrity
| Input | Expected revision/hash | Observed | Result |
|---|---|---|---|
| dimensions.md | r4 | r4 | pass |
| print_plan.md | r1 | r1 | pass |
| reference STL | accepted runtime hash | same runtime hash | pass |
| candidate STL | hash at verification start | unchanged through run | pass |

## Upstream dimensions audit against photos
| Feature/dim ID | Photo observation | Sheet statement | Result | Evidence |
|---|---|---|---|---|
| F-003/M-006 | two distinct rails span 16.7, not one collar | two rails, 16.7 total envelope | pass | evidence/verification/cq-a/v1/upstream-rails.png |
| F-005/M-009 | button is about 90 degrees from rail plane | +Y button vs ±X rails | pass | evidence/verification/cq-a/v1/upstream-button.png |

## Print-plan audit
| Constraint ID | Candidate observation | Result | Evidence |
|---|---|---|---|
| P-001 | minimum structural bore wall 6.2 mm | pass | wall-thickness.csv |
| P-003 | bed-contact critical edges have 0.3 mm chamfer | pass | section-bed-edge.png |
| P-005 | no unsupported narrowing transition in planned orientation | pass | overhang.png |

## Seven checks
| Check | Method on re-imported STL | Numeric result | Visual observation | Result | Evidence |
|---|---|---|---|---|---|
| 1 interference | mesh/reference intersection at seat | 0.000 mm3 | section shows clearance and plate stop | pass | check-1.txt |
| 2 insertion | 4 mm steps over 68 mm travel | worst 0.000 mm3 | rail and button paths stay open | pass | insertion.csv |
| 3 section | half assembly render | n/a | plate is the stop; tip has headroom | pass | section.png |
| 4 look/overlay | same side/rail cameras plus photo overlay | n/a | two rails, button, taper, and counts match | pass | composite.png; overlay.png |
| 5 positions | named-datum STL slices with explicit plane transform | max delta 0.4 mm | no mirrored layout | pass | positions.csv |
| 6 measurement audit | all M-001 through M-011 mapped | 11/11 | no visible feature omitted | pass | audit table below |
| 7 printability/faces | STL in upside-down plan orientation | watertight; unsupported area within plan | bore support-free; bbox 46 x 46 x 95 mm | pass | printability.txt |

## Feature-position register
| Feature ID | Datum | Expected | Observed | Delta | Handedness check | Result |
|---|---|---:|---:|---:|---|---|
| F-003 rail top | D0_BOOT | 42.8 | 42.8 | 0.0 | ±X pair present | pass |
| F-005 button center | D0_BOOT/+Y | 47.5 ±2.0 | 47.7 | +0.2 | mirror fit is worse | pass |

## Measurement audit
| Dimension ID | Geometry mapping | Result |
|---|---|---|
| M-001 | named bore parameter plus per-side clearance | pass |
| M-006 | reference rail envelope and candidate channel envelope | pass |
| M-011 | full button channel clears approved bound plus margin | pass |

## Visual inspection narrative
- Reference/photo row: two narrow opposed rails end below a window band; one button sits
  about 90 degrees around the shaft; a base plate defines the seat.
- Candidate row: the internal escape channels preserve those counts and orientations.
- Differences: candidate adds only documented clearances and headroom.
- Overlay observations: reference boundaries hug rail sides, rail ends, button band, and taper.

## Defects
| Defect ID | Owning contract | Feature/check IDs | Concrete defect | Required acceptance condition |
|---|---|---|---|---|
| none | n/a | n/a | n/a | n/a |

## Verdict
- Result: PASS
- Passed candidate ranking, if comparing candidates: cq-a is the only candidate in this example.
- Rerun scope: all checks after any upstream or geometry revision.
- Verifier commission: verifier:cq-a-v1
```

## 7. Orchestrator state machine

### 7.1 States and transitions

```text
INTAKE
  -> ROUTED_SOLO -> SOLO_ACTIVE -> SOLO_PHASE4_GATE -> SOLO_DELIVERY -> DELIVERED
  -> PIPELINE_DIMENSIONS
       -> DIMENSIONS_BLOCKED -> PIPELINE_DIMENSIONS
       -> REFERENCE_BUILD
            -> REFERENCE_OVERLAY_REVIEW
                 -> PIPELINE_DIMENSIONS        [sheet incomplete/ambiguous]
                 -> REFERENCE_BUILD            [clear sheet implemented incorrectly]
                 -> PRE_DESIGN_PRINT_PLAN
                      -> PRINT_PLAN_BLOCKED -> PRE_DESIGN_PRINT_PLAN
                      -> CANDIDATE_BUILD
                           -> FRESH_VERIFICATION
                                -> PIPELINE_DIMENSIONS    [upstream dimensions reject]
                                -> PRE_DESIGN_PRINT_PLAN [print-plan reject]
                                -> CANDIDATE_BUILD       [geometry reject]
                                -> FINAL_PRINT_PREP      [pass]
                                     -> FIELD_COUPON_READY
                                          -> DELIVERY
                                               -> DELIVERED
```

Post-delivery feedback reopens the earliest owning state:

```text
FAILED_PRINT
  -> PIPELINE_DIMENSIONS      [missed/misdescribed mating feature]
  -> PRE_DESIGN_PRINT_PLAN   [process-only cause]
  -> both, dimensions first  [mixed]
```

### 7.2 Gate table

| State | Owner/commission | Entry requirements | Exit gate |
|---|---|---|---|
| `INTAKE` | Orchestrator | User request | Requirements recorded; queue entry created if used |
| `ROUTED_SOLO` | Orchestrator | Routing checklist | Decision recorded |
| `SOLO_ACTIVE` | One monolith agent | Existing skill available | Monolith Phase 1-3 complete |
| `SOLO_PHASE4_GATE` | Same monolith agent | Export exists | Existing seven checks pass |
| `PIPELINE_DIMENSIONS` | Metrologist | Photos/calipers/product ID available | No U fit dimensions; assumptions approved/bounded |
| `REFERENCE_BUILD` | Blind designer | Accepted sheet revision; backend chosen | Reference source, export, required renders exist |
| `REFERENCE_OVERLAY_REVIEW` | Metrologist | Reference hash and renders | Overlay accepted and written into sheet |
| `PRE_DESIGN_PRINT_PLAN` | Print engineer pass 1 | Accepted sheet and reference | Plan accepted with all geometry constraints |
| `CANDIDATE_BUILD` | One or more designers | Bound sheet/ref/plan revisions | Candidate contract outputs complete |
| `FRESH_VERIFICATION` | New verifier context per candidate/run | Export hashes frozen | Upstream audits plus all seven checks pass |
| `FINAL_PRINT_PREP` | Print engineer pass 2 | Passing report | Coupon, notes, slicing/3MF, order, field test ready |
| `DELIVERY` | Orchestrator | All artifacts and queue target known | Files delivered/committed; queue set Ready to Print |

### 7.3 Rejection routing

The verifier uses exactly one primary rejection class per defect:

| Rejection class | Owner | Required loop |
|---|---|---|
| `UPSTREAM_DIMENSIONS` | Metrologist | Revise sheet, rebuild reference blind, repeat overlay and every downstream gate |
| `REFERENCE_IMPLEMENTATION` | Reference designer | Rebuild from unchanged sheet; repeat overlay |
| `PRINT_PLAN` | Print engineer | Revise plan; invalidate and rebuild candidates affected by the change |
| `CANDIDATE_GEOMETRY` | Candidate designer | Fix named parameter/feature; re-export; fresh verifier reruns all checks |
| `VERIFICATION_INFRA` | Orchestrator | No candidate verdict; correct or replace the verifier commission and rerun |

For two or three CadQuery candidates, the verifier reports pass/reject for each and may
rank passing candidates only on contract-backed criteria such as clearance robustness,
support area, wall margin, and material/time estimate. The orchestrator selects the
highest-ranked pass or asks the user when the remaining tradeoff is subjective.

## 8. FreeCAD serialization and candidate parallelism

- The orchestrator acquires a repo-wide FreeCAD lease at `.claude/3d-freecad.lock` before
  any FreeCAD MCP call that can mutate a document. The lock records `job_id`, commission,
  and acquisition time; `job_state.md.freecad_owner` mirrors it.
- There is exactly one active FreeCAD designer commission across all jobs, including
  reference and candidate work. A second FreeCAD candidate or project waits; it never
  opens in parallel.
- FreeCAD reference modeling completes and passes metrologist review before candidate
  modeling begins in the same `.FCStd`.
- The designer plans at most eight substantive `execute_code` chunks per job, prints
  validity/volume/bbox checks in each, and looks at returned screenshots.
- The verifier works from staged exported STL/renders in a fresh context and does not need
  the FreeCAD mutation lock.
- CadQuery reference work is still serial before print planning. After that gate, two or
  three candidate instances may run in parallel in isolated folders.
- Parallel candidates never share filenames, Python import state, or output directories.

## 9. Shared-reference reading and sufficiency

References stay in `skills/3d-modeling/references/`. Slices link there by relative path;
no file is copied or forked.

| Shared reference/script | Primary rule owner | Other authorized readers | Why each reader needs it |
|---|---|---|---|
| `freecad-mcp-patterns.md` | CAD designer | Verifier, FreeCAD sections only | Designer builds/exports; verifier understands FreeCAD render/export evidence |
| `cadquery-patterns.md` | CAD designer for CadQuery patterns | Metrologist for overlay; verifier for backend-neutral STL checks/overlay | Contains the only tested named-datum and overlay patterns |
| `fdm-design.md` | Print engineer for process decisions | CAD designer always; verifier for conformance | Keeps DFM in the plan, geometry, and independent audit without duplicating decision ownership |
| `mechanisms.md` | CAD designer | None by default | Needed only when a mechanism is in the contract |
| `materials.md` | Print engineer | None | Material and support-interface decisions |
| `troubleshooting.md` | Print engineer | None | Calibration and failed-print forensics |
| `printers.md` | Print engineer | Orchestrator consumes only the chosen profile name/availability | Machine envelope, nozzle, chamber, and process quirks |
| `bambu-3mf-authoring.md` | Print engineer | None | Project 3MF round trip, structural validation, honesty rule |
| `scripts/run_cadquery_model.py` | CAD designer | None | Strict model execution and preview |
| `scripts/preview.py` | CAD designer | Metrologist, verifier | Same-camera render evidence |
| `scripts/make_3mf.py` | Print engineer | None | Final multi-color container |
| `scripts/make_bambu_3mf.py` | Print engineer | None | Final X2D project 3MF |
| `scripts/mesh_io.py` | CAD designer where imported by shared scripts | Verifier where imported by shared scripts | Shared mesh transport implementation, not a separate workflow owner |

The same reference may be read by several roles, but every decision and workflow rule has
one owner in the coverage table below. Reading does not grant write authority over another
role's contract.

## 10. Zero-loss coverage of the monolith

Each row is one atomic obligation from `skills/3d-modeling/SKILL.md`. The `Owner` column
contains exactly one slice. Other roles may consume the result but do not own the rule.

| ID | Monolith obligation | Owner | Pipeline location |
|---|---|---|---|
| S-01 | Use the workflow because missed real geometry and ignored FDM cause failures; track visible progress | Orchestrator | State ledger and routing |
| S-02 | Read only task-relevant references from the shared index | Orchestrator | Dispatch reading manifests |
| P0-01 | Choose one backend per part and never mix mid-part | Orchestrator | Backend field and dispatch gate |
| P0-02 | Apply FreeCAD pros/cons and selection criteria | Orchestrator | Backend decision |
| P0-03 | Apply CadQuery pros/cons and selection criteria | Orchestrator | Backend decision |
| P0-04 | Check FreeCAD with `list_documents`; ask for desktop/addon if unavailable | Orchestrator | Intake/backend gate |
| P0-05 | Check/install CadQuery dependencies before dispatch | Orchestrator | Intake/backend gate |
| P0-06 | If neither backend exists, stop rather than guess geometry | Orchestrator | Blocked backend state |
| P0-07 | Limit FreeCAD work to one instance and plan for screenshot cost | CAD designer | FreeCAD checklist and lock |
| P1-01 | Ask missing job questions in one pointed round | Orchestrator | Intake checklist |
| P1-02 | Capture function, loads, and load directions | Orchestrator | `job_state.md` |
| P1-03 | Capture heat, UV, moisture, and other environment | Orchestrator | `job_state.md` input to print plan |
| P1-04 | Make Phase 2 mandatory for a real-object fit | Orchestrator | Pipeline routing |
| P1-05 | For a known product, search official specs/drawings, cross-check two sources, search existing models, and confirm the user's variant | Metrologist | Source register and dimensions gate |
| P1-06 | Capture exact printer; research and persist a missing printer profile | Print engineer | Pre-design plan |
| P1-07 | Capture filaments, visible faces, text/logos, and color count | Orchestrator | `job_state.md` |
| P1-08 | Capture project folder and print queue early | Orchestrator | Intake and delivery state |
| P1-09 | Gate on every fit-critical dimension being measured, sourced, or user-approved | Metrologist | `dimensions.md` acceptance |
| P2-01 | Inspect photos via max-zoom crops and block fit work without mating-object photos | Metrologist | Source evidence |
| P2-02 | Inventory every visible feature, not idealized primitives | Metrologist | Feature inventory |
| P2-03 | Pin every measurement to a named feature and ask exact ambiguous caliper questions | Metrologist | Dimension register/open questions |
| P2-04 | Position every cutout/pocket center from named datums | Metrologist | Datum and dimension registers |
| P2-05 | Treat every commercial counterpart feature as functional documentation | Metrologist | Feature inventory |
| P2-06 | Model the mating object before the candidate | CAD designer | `REFERENCE` commission |
| P2-07 | Compare the reference with photos and obtain acceptance before candidate design | Metrologist | Blind round-trip gate |
| P2-08 | Preserve the accepted reference as the verification fixture and hide/do not export it as a final part | CAD designer | Reference output contract |
| P2-09 | Use the render-over-photo loop for photo recreation, including side/iso architecture | Metrologist | Overlay evidence |
| P3-01 | Choose print orientation before modeling because it drives geometry | Print engineer | Pre-design `print_plan.md` |
| P3-02 | Keep function slicer-agnostic and prefer compliant fits over precision-only fits | CAD designer | Candidate checklist |
| P3-03 | Store measured values and clearances as named parameters with units/provenance and one-line fit fixes | CAD designer | Source and notes contract |
| P3-04 | Use per-side clearances from `fdm-design.md` | CAD designer | Candidate parameters |
| P3-05 | Require a printed coupon for a tight/unknown fit | Print engineer | Coupon contract |
| P3-06 | Build in small verified steps and inspect validity, volume, bbox, and previews after booleans | CAD designer | Backend checklist |
| P4-01 | Make all seven checks mandatory and measure the exported STL re-imported | Verifier | Acceptance checklist |
| P4-02 | On any failure, fix parameter-first where applicable and rerun all seven | Orchestrator | Rejection state loop |
| P4-03 | Check seated interference | Verifier | Check 1 |
| P4-04 | Sweep the full insertion travel | Verifier | Check 2 |
| P4-05 | Produce and inspect a section render | Verifier | Check 3 |
| P4-06 | Compose same-view side-by-side visuals and actually compare silhouette, shapes, and counts | Verifier | Check 4 |
| P4-07 | Remeasure feature positions from named datums on STL and check handedness | Verifier | Check 5 |
| P4-08 | Audit every measured number into geometry and reject unused values | Verifier | Check 6 |
| P4-09 | Audit printability and faces against chosen orientation, radii, and bbox | Verifier | Check 7 |
| P5-01 | Put FreeCAD output directly in the confirmed project folder; explicitly deliver/commit container-built files | Orchestrator | Delivery checklist |
| P5-02 | Deliver parametric source with reference hidden/not exported | CAD designer | Source outputs |
| P5-03 | Deliver per-part STL at required CadQuery tolerances, combined STEP, and renders | CAD designer | Candidate outputs |
| P5-04 | Document geometry, named fit fixes, and honest geometric risks in `print_notes.md` | CAD designer | Designer-owned notes stage |
| P5-05 | Document orientation, material, slicer settings, and process risks in `print_notes.md` | Print engineer | Final notes stage |
| P5-06 | Build a single multi-color 3MF with per-part assignment when applicable | Print engineer | Final prep |
| P5-07 | For a print-ready Bambu project 3MF, round-trip machine keys, verify structure, and ship an honest after-import checklist | Print engineer | Final prep |
| P5-08 | Update the user's print queue at start and every transition/design change | Orchestrator | Queue ledger |
| P5-09 | Propose and prepare a cheap PLA fit test before final material | Print engineer | Coupon and print order |
| P5-10 | Treat a failed print as measured data; fix the reference first for missed geometry, reverify/re-export, and record the lesson | Print engineer | Failure triage entry point |
| P5-11 | Diagnose adhesion/stringing/shifts/banding from `troubleshooting.md`, not guesses | Print engineer | Process-failure path |

This table assigns all 53 atomic obligations once. Shared reference readers and downstream
consumers do not create second ownership.

## 11. Berlingo knob v4 dry run

This is a paper trace using `Berlingo gear shift knob/v4-cadquery/`.

### Step 1: route and intake

The orchestrator sees a replacement knob whose bore must traverse and seat on a real gear
lever, so it records `PIPELINE` by the fit-critical rule. It creates/updates the Print Queue
entry to `To Design / Tweak`, records the Bambu X2D, parked-car environment, single-color
recessed pattern, project path, and the user's statement that reverse is push-in.

### Step 2: metrology

The metrologist writes the example `dimensions.md` above. Crucially, it records:

- F-001 base plate as the seat datum
- F-003 as **two discrete 5.5 mm rails** whose total envelope is 16.7 mm
- rail top at 42.8 mm
- F-005 button at about 90 degrees to the rail plane
- uncertain plate height, button Z, and button protrusion as C-grade bounded assumptions

This is where the old input-corruption class first becomes visible: the value 16.7 is not
allowed to exist without the words "outer rail face to outer rail face across two rails."

### Step 3: blind reference round trip

A CadQuery reference designer receives only `dimensions.md` plus its backend/FDM reading
and builds `reference.py`, an STL/STEP, and requested views. The metrologist overlays the
rail view and side view on the source photos.

The historical rev2 failure would be caught here. Rev2 interpreted 16.7 mm as a solid
collar and jammed about 20 mm down. A blind model built from an ambiguous "Ø16.7" row would
show a collar where the photo shows two rails. The metrologist, not the designer, would
rewrite the sheet to say two rails, add their width/count/end position and named axis, and
commission a rebuild. If that ownership check somehow failed, the verifier's upstream
photo audit and full insertion sweep are later independent backstops.

### Step 4: pre-design print plan

After the reference overlay passes, the print engineer issues `print_plan.md`:

- ASA final, PLA coupon
- flat top on the bed, knob upside down
- no support in the bore
- wall/nozzle/detail floors
- elephant-foot bed chamfers
- main nozzle, single color
- coupon must contain the real rail end, button path, and upper-bore transition

The designer now receives a geometry contract, not a later slicing suggestion.

### Step 5: candidate design

One CadQuery designer builds `cq-a` from dimensions r4, accepted reference hash, and print
plan r1. It produces the existing-form outputs:

- `model.py`
- `verify.py`
- `knob_v4.stl`
- `knob_v4.step`
- preview and section renders
- geometry sections of `print_notes.md`

For a harder alternative study, `cq-b` and `cq-c` could run in parallel in isolated
folders. They would share contracts but not code or chat.

### Step 6: fresh verification

A new verifier context hashes and re-imports the candidate STL. It:

1. rechecks the sheet against the original lever photos;
2. rechecks walls, chamfers, overhangs, orientation, and nozzle limits against the plan;
3. checks seated interference;
4. sweeps all 68 mm of insertion travel, including both rail and button paths;
5. opens a section showing the base plate stop and tip headroom;
6. opens same-view composites/overlays and describes feature counts and layout;
7. measures rail/channel ends and button layout from named datums;
8. maps every M-ID into geometry; and
9. audits the upside-down exported mesh for printability and faces.

The designer's existing `verify.py` is useful input but cannot supply the verdict. This is
the direct control for self-verification blindness.

### Step 7: final print prep and delivery

After `PASS`, the print engineer extracts the 26 mm real-bore coupon, finalizes ASA slicing
notes and the field test, and requires the coupon first. The test says to report stopping
distance from the seat; that distance localizes a rail, button, or upper-bore defect. The
orchestrator promotes the selected artifacts, updates the queue to `Ready to Print`,
commits the physical iteration, and delivers the files.

### Where the T4 camera-datum failure would be caught

The T4 benchmark's prompt said the camera center was 37 mm from the top when the reference
truth was 24 mm, and a later revision also stated the wrong left/right side. Designers
followed those corrupt numbers with roughly 0.5 mm precision.

In this pipeline:

1. The metrologist must place the camera feature from named top/centerline datums and
   compare the statement with the actual photo before accepting `dimensions.md`.
2. If the bad 37 mm or wrong-side statement survives, the blind reference will put the
   camera window in that wrong location. The metrologist's photo overlay rejects the
   round trip and corrects the sheet before candidate CAD begins.
3. If both upstream gates fail, the fresh verifier independently audits
   `dimensions.md` against the photos and checks the exported candidate's camera center
   and handedness. It rejects `UPSTREAM_DIMENSIONS`, not `CANDIDATE_GEOMETRY`.

The designer is intentionally not expected to "use judgment" to override the bad datum.
Ground-truth corruption belongs to the metrologist, and self-check blindness belongs to
the fresh verifier.

## 12. Proposed evaluation, not run

Use `experiments/protocol.md` and the existing harness to rerun T1-T4. Keep prompts,
photos, model, tool availability, and grading v2 fixed.

### Arms

Run both backends where available:

1. `monolith-cadquery`
2. `team-cadquery`
3. `monolith-freecad`
4. `team-freecad`

The team orchestrator must route all four tests to pipeline mode because they are
fit-critical and/or multi-part. CadQuery candidate branches may parallelize. FreeCAD arms
and all FreeCAD designers serialize. Preserve the historical unassisted results as context,
but the decision comparison is team versus monolith on the same backend.

Prefer three repetitions per cell with randomized arm order. If cost forces the original
`n=1` pilot shape, treat small cost/score deltas as descriptive only.

### Procedure

- Agents see only the original prompt packages, not reference STLs.
- Team roles communicate only with the proposed contracts.
- Grading remains blind until outputs and ledgers are frozen.
- Apply grading v2: scorer criticals, watertightness, same-camera visual narrative,
  layout IoU, boundary-F1, named-datum position checks, and mirror flags.
- Add two acceptance injections for the architecture:
  - ambiguous `16.7` rail envelope must fail before candidate acceptance;
  - corrupt T4 camera height/side must be assigned to `UPSTREAM_DIMENSIONS`.
- Record per run:
  - grading-v2 success and failure class
  - fit score, layout IoU, boundary-F1, position error, mirror flag
  - DFM/design rubric: orientation, support avoidance, bed chamfers, layer/load,
    compliant fit, coupon quality, parameter-fix table, honest risks
  - total and per-role tokens
  - wall time, active compute time, and critical-path time
  - number of user questions, contract revisions, rejected loops, and successful exports

### Keep/sunset criteria

Keep team mode only if all of the following hold:

- **Correctness:** team grading-v2 success is not lower than the same-backend monolith and
  the team passes at least 11 of 12 runs in a three-repeat design, with no unexplained
  position or mirror failure.
- **Historical controls:** every injected rev2-rail and T4-datum defect is rejected by the
  named owner before delivery, and reference-vs-itself verifier calibration passes.
- **Look-first evidence:** every graded team run contains an opened/described same-camera
  composite and, where photos permit, an overlay. Missing visual evidence is a failed run
  regardless of numeric scores.
- **DFM depth:** the team is no worse than the monolith on the DFM/design rubric and does
  not lose the skill's orientation, support-avoidance, chamfer, layer/load, coupon, or
  one-parameter-fix advantages.
- **Cost:** median total tokens per successful graded job are no more than 2.0 times the
  monolith. Report role shares so a costly handoff can be removed without weakening the
  sacred designer/verifier separation.
- **Latency:** median wall time is no more than 1.5 times monolith for CadQuery and 2.0
  times monolith for serialized FreeCAD. Also report critical-path time so parallel
  candidate exploration is not credited with hidden total work.

If correctness or historical-control criteria fail, sunset the split regardless of token
savings. If correctness improves but cost misses the threshold, first reduce optional
parallel candidate count and contract verbosity; do not merge designer and verifier.

## 13. Migration notes

### Stays unchanged

- `skills/3d-modeling/SKILL.md` remains the solo-mode skill.
- `skills/3d-modeling/references/` remains the single shared reference source.
- `skills/3d-modeling/scripts/` remains shared.
- Existing project outputs and experiments remain unchanged.

### Moves into slim slices

Nothing is deleted from the monolith. "Moves" means the pipeline slices restate only the
assigned operational checklist and link back to shared references:

- `skills/3d-orchestrator/SKILL.md`: routing, state machine, contract/revision gates,
  dispatch, serialization, queue/git/delivery.
- `skills/3d-metrologist/SKILL.md`: dimensions contract, provenance/confidence, feature
  inventory, datum positions, blind reference acceptance, overlays.
- `skills/3d-designer/SKILL.md`: REFERENCE/CANDIDATE commissions, selected backend plus
  mandatory FDM reading, parametric outputs, self-check limits.
- `skills/3d-verifier/SKILL.md`: fresh-context rule, upstream/plan audits, seven exported
  STL checks, visual evidence, rejection schema, no fixes.
- `skills/3d-print-engineer/SKILL.md`: pre-design print contract, post-pass coupon/slicing/
  3MF/field test, failed-print forensics.

### Repository wiring

- One Claude Code subagent definition per slice lives under `.claude/agents/`.
- Root `AGENTS.md` contains the routing checklist and exact entry points in
  section 2.4.
- Do not change the existing monolith trigger or content.
- Validate links from every slice to the shared reference files.
- Run a static coverage check against the IDs in section 10 and a paper dispatch smoke
  test. The original T1-T4 evaluation remains proposed; the separately approved Pixel 10
  head-to-head is recorded under `experiments/pixel-10-case/`.

## 14. Design validation checklist

- [x] Five roles only.
- [x] Solo monolith remains unchanged.
- [x] All communication is grounded in project files.
- [x] `dimensions.md`, `print_plan.md`, and `verification_report.md` have exact templates
  and filled examples.
- [x] Orchestrator state has an exact file schema.
- [x] Every monolith obligation is assigned to exactly one owner in section 10.
- [x] Every role's checklist has sufficient shared-reference reading in section 9.
- [x] Designer and verifier are different roles and fresh contexts.
- [x] Visual same-view and photo-overlay inspection is mandatory evidence.
- [x] Verification runs on the exported STL re-imported.
- [x] Print plan precedes candidate design and is audited in the planned orientation.
- [x] FreeCAD is single-instance; CadQuery candidates may parallelize in isolated folders.
- [x] Berlingo v4 dry run identifies the rev2 rail catch and T4 datum catch.
- [x] T1-T4 team-versus-monolith evaluation is proposed but not run.
- [x] Implementation began only after explicit user approval.
