# 3D-Modeling Skill — TEAM VERSION — full bundle for external review

Generated from git `75211b2` (2026-07-24).

This is the **five-role, file-contract team pipeline** version of the `3d-modeling` skill: a thin no-geometry orchestrator routes fit-critical jobs through **metrologist → designer (blind reference, then candidate) → print-engineer → independent verifier**, communicating only through contract files (never chat). It includes the architecture, the five role slices, all shared reference material the roles read, and the scripts (including the executable preflight gate `team_preflight.py`). The solo-mode monolith is appended at the end only as context. Each file is delimited by a `FILE:` header with its repo path.

## Table of contents

- **TEAM PIPELINE — ENTRY POINT & ARCHITECTURE**
  - [`AGENTS.md`](#AGENTS_md)
  - [`skills/team-design.md`](#skills__team-design_md)
- **TEAM PIPELINE — THE FIVE ROLE SLICES**
  - [`skills/3d-orchestrator/SKILL.md`](#skills__3d-orchestrator__SKILL_md)
  - [`skills/3d-metrologist/SKILL.md`](#skills__3d-metrologist__SKILL_md)
  - [`skills/3d-designer/SKILL.md`](#skills__3d-designer__SKILL_md)
  - [`skills/3d-verifier/SKILL.md`](#skills__3d-verifier__SKILL_md)
  - [`skills/3d-print-engineer/SKILL.md`](#skills__3d-print-engineer__SKILL_md)
- **SHARED REFERENCE MATERIAL (read by the roles)**
  - [`skills/3d-modeling/references/team-contracts-v4.md`](#skills__3d-modeling__references__team-contracts-v4_md)
  - [`skills/3d-modeling/references/fdm-design.md`](#skills__3d-modeling__references__fdm-design_md)
  - [`skills/3d-modeling/references/cadquery-patterns.md`](#skills__3d-modeling__references__cadquery-patterns_md)
  - [`skills/3d-modeling/references/freecad-mcp-patterns.md`](#skills__3d-modeling__references__freecad-mcp-patterns_md)
  - [`skills/3d-modeling/references/printers.md`](#skills__3d-modeling__references__printers_md)
  - [`skills/3d-modeling/references/materials.md`](#skills__3d-modeling__references__materials_md)
  - [`skills/3d-modeling/references/mechanisms.md`](#skills__3d-modeling__references__mechanisms_md)
  - [`skills/3d-modeling/references/troubleshooting.md`](#skills__3d-modeling__references__troubleshooting_md)
  - [`skills/3d-modeling/references/preflight-checklist.md`](#skills__3d-modeling__references__preflight-checklist_md)
  - [`skills/3d-modeling/references/bambu-3mf-authoring.md`](#skills__3d-modeling__references__bambu-3mf-authoring_md)
- **SCRIPTS (executable preflight gate + shared tooling)**
  - [`skills/3d-modeling/scripts/team_preflight.py`](#skills__3d-modeling__scripts__team_preflight_py)
  - [`skills/3d-modeling/scripts/test_team_preflight.py`](#skills__3d-modeling__scripts__test_team_preflight_py)
  - [`skills/3d-modeling/scripts/run_cadquery_model.py`](#skills__3d-modeling__scripts__run_cadquery_model_py)
  - [`skills/3d-modeling/scripts/mesh_io.py`](#skills__3d-modeling__scripts__mesh_io_py)
  - [`skills/3d-modeling/scripts/preview.py`](#skills__3d-modeling__scripts__preview_py)
  - [`skills/3d-modeling/scripts/make_3mf.py`](#skills__3d-modeling__scripts__make_3mf_py)
  - [`skills/3d-modeling/scripts/make_bambu_3mf.py`](#skills__3d-modeling__scripts__make_bambu_3mf_py)
- **APPENDIX — SOLO-MODE MONOLITH (for context; the team pipeline decomposes this)**
  - [`skills/3d-modeling/SKILL.md`](#skills__3d-modeling__SKILL_md)



==========================================================================================
# TEAM PIPELINE — ENTRY POINT & ARCHITECTURE
==========================================================================================


<a id="AGENTS_md"></a>

------------------------------------------------------------------------------------------
### FILE: `AGENTS.md`  (103 lines)
------------------------------------------------------------------------------------------

# AGENTS.md — 3D printing projects

Guidance for AI agents working in this folder. (`CLAUDE.md` points here; this file is the
single source of truth.)

## Modeling entry points

- Start every modeling or print-prep request by loading **`3d-orchestrator`**. It owns the
  route and records the decision in `job_state.md`.
- **Solo mode** runs the existing [`skills/3d-modeling/`](skills/3d-modeling/) monolith
  unchanged. Use it only for a simple, single-part, non-fit-critical job with no recreated
  mating geometry, no moving/multi-part interfaces, and no high-consequence DFM question.
- **Team mode** uses the five slices in `skills/3d-orchestrator/`,
  `skills/3d-metrologist/`, `skills/3d-designer/`, `skills/3d-verifier/`, and
  `skills/3d-print-engineer/`. Use it when fit or named-datum accuracy matters, geometry is
  reconstructed from photos, parts mate or move, the job is multi-part/multi-colour, DFM is
  difficult, failure has safety/thermal/load consequences, or the user asks for independent
  verification.
- Invoke solo explicitly with `/3d-modeling`. Invoke the team with `/3d-orchestrator` or
  “use the 3D team.” For normal new jobs, let the orchestrator decide.
- Team agents communicate only through project contract files and source evidence, never
  chat summaries. The required flow and templates are in
  [`skills/team-design.md`](skills/team-design.md).
- In Claude Code, keep orchestration in the main session or launch
  `claude --agent 3d-orchestrator`; nested Claude subagents cannot spawn specialists. In
  Codex, the root agent may dispatch the five slices directly. Runtime model selection is a
  launcher concern; it does not change the file contracts.

## The solo skill

- **Use the `3d-modeling` skill** for any modeling or print-prep work here. A copy lives in
  this repo at [`skills/3d-modeling/`](skills/3d-modeling/) (browsable) and
  [`skills/3d-modeling.skill`](skills/3d-modeling.skill) (installable bundle). It supersedes
  the older single-backend `3d-freecad` / `3d-cadquery` skills.
- It supports **two backends** — pick per part in the skill's Phase 0:
  - **FreeCAD** (via the FreeCAD MCP on this machine): parametric `.FCStd` you can open and
    edit; best design-quality; needs the desktop + FreeCAD + MCP addon running.
  - **CadQuery** (code-first, runs in the cloud container): a parametric `model.py`; no
    desktop dependency; cheap fast iteration. Use when the bridge/FreeCAD is offline.
- **Never export a fit-critical part without the skill's Phase 4 checks** (all seven):
  interference, insertion sweep over full travel, section render, **visual side-by-side vs
  the photos/reference**, **feature positions measured from named datums**, measurement
  audit, printability + face audit — all run on the **exported STL re-imported**, not the
  in-memory model.
- **Before finalizing STL and before slicing, run the pre-print validation checklist**
  (`skills/3d-modeling/references/preflight-checklist.md`): DFAM/adhesion/overhang geometry,
  material calibration, and the exact final-3MF settings. It exists because CAD-clean parts
  still fail on the plate — see the PETG-CF knock-off case in
  `skills/3d-modeling/references/troubleshooting.md`.
- **Recreating a part from photos**: use the render-over-photo overlay loop
  (`skills/3d-modeling/references/cadquery-patterns.md`) — draw the model's boundaries on the
  photo and iterate. Overlays catch millimetre errors that side-by-side viewing misses.
- **Known products** (phone, battery, SBC, appliance part): web-search the official specs and
  look for existing 3D models before measuring — then still confirm with photos + calipers.

## Team invariants

- The metrologist owns all numbers and named datums in `dimensions.md`. The designer never
  silently repairs or replaces ground truth.
- The mating reference is built blind from `dimensions.md`; the metrologist then overlays it
  on the photos. If it misses, revise the sheet and rebuild.
- The print engineer issues `print_plan.md` before candidate design and returns after an
  independent pass for coupon, slicing, print order, and field testing.
- The designer and verifier must be different fresh contexts. The verifier must look at
  renders/overlays and must run all seven Phase-4 checks on the exported STL re-imported.
- Never run two FreeCAD designers concurrently. CadQuery candidate instances may run in
  separate folders in parallel.

## Printer

- **Bambu Lab X2D Combo** (dual nozzle, AMS 2 Pro, heated chamber). Full profile with quirks
  and recipes: `skills/3d-modeling/references/printers.md`. Key: model/TPU/CF on main nozzle,
  second colour/support on auxiliary; dual-nozzle jobs shrink build volume to 235.5×256×256.

## Workflow rules

- **Track every part in the Notion Print Queue** (database under the "3D Printing" page).
  Create the entry when design starts; update Status on every transition
  (To Design / Tweak → Ready to Print → Printing → Done); keep Material, For, and the page
  body's dimensions current whenever the design changes.
- **One folder per project**, containing the parametric source (FreeCAD `.FCStd` with the
  hidden reference model of the mating object, **or** CadQuery `model.py` + `verify.py`),
  per-part STLs, combined STEP, single-file multi-colour 3MF if applicable, renders, and
  `print_notes.md`.
- **Fit parts get a printed test coupon first** (PLA, ~15 min) before the full part in the
  final material. The coupon slices the actual bore/mating region.
- **Commit to git after every meaningful design iteration** with a message that says what
  changed physically (e.g. "knob v4: added button escape channels to bore").

## Environment notes

- Parts often live in a car interior (Israeli summer): default to **ASA/PETG, never PLA** for
  final parts. PLA is for fit-test coupons only.
- FreeCAD runs on this machine and is reachable via the FreeCAD MCP when the desktop bridge is
  connected; files export directly into these folders. When it's offline, use the CadQuery
  backend in the cloud and deliver the files back here.

## Learning / experiments

The `experiments/` folder holds a benchmarked comparison of the two backends vs an unassisted
control, plus the verification methodology (`verification_postmortem.md`, `verify_visual.py`,
`overlay_photo.py`) that the skill's Phase 4 is built on. Read `experiments/experiment_report.md`
for why the checks exist — most were added after a real miss.

<a id="skills__team-design_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/team-design.md`  (1671 lines)
------------------------------------------------------------------------------------------

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
  candidate_readiness.md
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

## 15. Runtime optimization v2

The first live Pixel 10 comparison preserved quality but exposed excessive serial cost:
team `91/100` versus monolith `62/100`, at `71m22s` versus `8m48s`. The team caught three
real defects: an incomplete camera datum sheet, a closed installation face, and a wrong
model-to-printer orientation. The controls remain correct; the preventable work before
those controls is optimized.

The compact runtime schemas introduced for v2 now live, with the evidence-driven v3
amendments, in
[`3d-modeling/references/team-contracts-v4.md`](3d-modeling/references/team-contracts-v4.md).
They retain the exact semantic fields in section 6 and all 53 ownership assignments while
removing repeated prose from runtime contexts.

The v2 changes are:

1. **Blind-build completeness gate.** Before reference CAD, each visible feature has
   count/function, relative layout/handedness, and a datum/bounded envelope or documented
   shared-envelope response. This prevents spending a reference build to discover a missing
   visible feature. It does not replace the blind build or visual overlay.
2. **Designer readiness receipt.** Candidate CAD stays inside its own non-authoritative
   loop until `candidate_readiness.md` proves, on the re-imported exported STL, integrity,
   full insertion/travel, the intended section/open-face architecture, exact bed transform,
   unsupported-roof limits, and required hashes/artifacts. It never grants acceptance.
3. **Fresh verifier remains sacred.** Only after readiness does a new context independently
   rerun all seven checks, inspect the images, and audit upstream contracts. Every changed
   STL hash still requires a new fresh verifier.
4. **File receipt drives progress.** The orchestrator advances when the required hash-bound
   file exists and validates; chat completion prose is not a gate.
5. **Compact evidence.** Use decisive crops/overlays and one multi-lane coupon by default.
   Preserve source, exports, hashes, reports, and decisive failed visuals; avoid duplicate
   previews and whole-image overlays.
6. **Exact print transform.** `print_plan.md` names the model-to-printer transform, bed
   landmark, bed normal, open direction, and forbidden downward faces so orientation is
   testable before verifier dispatch.

Pre-registered v2 Pixel targets are: final independent score at least `88/100`; one fresh
verifier when the readiness gate works; no avoidable reference or candidate rejection;
at most eight logged commissions; at most 35 minutes critical path; and at least 50% fewer
contract/evidence files or bytes. Per-agent tokens remain reported only when the runtime
exposes them; file bytes and commission count are proxies, never token estimates.

## 16. Runtime optimization v3

### Round-2 result and reason for another revision

The preregistered Pixel v2 rerun did reduce artifact fan-out, but it failed the adoption
thresholds:

| Metric | Target | Round 2 |
|---|---:|---:|
| Independent score | at least 88 | 80 |
| Critical path | at most 35 min | 1h 15m 35s |
| Logged commissions | at most 8 | 17 |
| Fresh verifier contexts | 1 unless corrected | 5 |
| Delivered footprint | at most 43 files / 2,068,316 bytes | 30 files / 1,519,980 bytes |

The smaller footprint is retained. The score/time loss came from four concrete loops:

1. readiness did not inventory or measure every exposed comfort/functional edge;
2. adding the missing round exposed a print-orientation support conflict that readiness had
   not quantified;
3. a print-plan revision confused current candidate evidence with later slicer evidence; and
4. post-verification print prep documented native support proof as pending while the job was
   marked delivered.

Fresh verification correctly found all four. V3 therefore strengthens deterministic
pre-dispatch evidence and phase ordering; it does not reduce verifier independence, visual
inspection, or any of the seven checks.

### V3 contract and state-machine amendment

The current templates, including the later executable v4 amendment, are in
[`3d-modeling/references/team-contracts-v4.md`](3d-modeling/references/team-contracts-v4.md).
They add:

- `required_now`, `deferred_owner`, and `final_gate` to each print-plan geometry rule;
- an Edge ID inventory with re-imported-STL endpoint/interior sampling;
- a support-sensitivity table that classifies and quantifies every out-of-limit region;
- `final_print_prep.md` for actual coupon/slicer/field-test evidence; and
- conditional `final_prep_review.md` only when the accepted plan depends on visual
  support-contact or toolpath evidence.

The orchestrator state tail is:

```text
CANDIDATE_BUILD
  -> INDEPENDENT_VERIFICATION
  -> PRINT_PREP
  -> [FINAL_PREP_REVIEW only for slicer-dependent visual predicates]
  -> DELIVERY
```

A support-free part with zero out-of-limit regions stays on the compact path and does not
create a native slicer project solely for ceremony. A design that relies on selected supports
must provide the bound contact/toolpath evidence and independent final-prep review. If a
plan-required native slicer is unavailable, the state is `BLOCKED_NATIVE_SLICER`, never
Ready to Print.

### Revision and rejection rules

- A failed `required_now` rule cannot be moved downstream for the same candidate.
- A plan revision that changes any candidate predicate requires a new readiness receipt and
  a new fresh full seven-check verifier, even if STL bytes did not change.
- Adding only post-verification artifacts under the unchanged accepted plan requires the
  applicable final-prep review, not another seven-check run.
- Every changed STL hash still requires a new fresh designer-distinct verifier context.
- The designer's edge/support preflight remains non-acceptance; the verifier independently
  repeats applicable edge sections and all printability predicates.

### Ownership and migration

No sixth role was added. The metrologist still owns truth and blind acceptance; the designer
owns source and non-acceptance readiness; the verifier owns fresh candidate acceptance and,
when required, independent final-prep inspection; the print engineer owns print rules and P2
evidence; the orchestrator owns file gates and delivery state. The 53-rule coverage table in
section 10 is unchanged and still gives each monolith obligation exactly one owner.

The shared runtime reference moved from `team-contracts-v2.md` through v3 to the current
`team-contracts-v4.md`; all five slices point to that one shared copy. The monolith
`3d-modeling/SKILL.md`, its solo workflow, backend patterns, and all original shared
references remain unchanged.

### V3 adoption hypotheses

- no verifier rejection for an uninventoried exposed edge, source-only radius claim,
  unclassified support footprint, or contract-order error;
- one fresh candidate verifier on the normal one-candidate path, at most two after one real
  geometry correction;
- at most eight specialist commissions and 30 minutes on the compact T2 regression;
- hard functional/export pass, total score at least 85 and not below the monolith arm;
- visual plus DFM score at least 22/30 and within two points of the monolith arm;
- at most 35 delivered files and 1 MB for the smaller T2 job; and
- token counts reported only if runtime telemetry exposes them, with commissions/files/bytes
  kept as explicitly non-token proxies.

## 17. Runtime optimization v4

### Round-3 result

The T2-style regression proved the architecture's quality and the prose-only readiness
limit:

| Metric | Monolith | Team v3 |
|---|---:|---:|
| Independent score | 86 | 93 |
| Functional/export hard gate | pass | pass |
| Critical path | 6m00s | 74m18s |
| Specialist commissions | 1 | 13 |
| Fresh verifier contexts / correction loops | 0 / 0 | 4 / 3 |
| Footprint excluding caches | 12 files / 451,351 bytes | 61 files / 3,660,471 bytes |

Fresh verifiers caught a 1,112.5 mm² print-orientation face error and then two separately
missed exposed-edge defects. Each was real and the final v3 artifact scored higher than the
monolith, so acceptance remains correct. The failure was that the designer and verifier
implemented the same written predicates differently, and the readiness gate could omit Edge
IDs while still saying `READY`.

### Executable shared gate

V4 adds
[`3d-modeling/scripts/team_preflight.py`](3d-modeling/scripts/team_preflight.py) and the
machine-readable `print_plan_checks.json` / `candidate_preflight.json` contracts in
[`team-contracts-v4.md`](3d-modeling/references/team-contracts-v4.md).

- The print engineer owns the complete Edge ID and support-rule sets.
- The shared `support-audit` command transforms the canonical STL into printer coordinates
  and measures non-bed downward area with the exact plan threshold.
- The shared `validate-receipts` command recomputes file hashes, rejects missing/extra Edge
  IDs or support rules, checks every numeric radius sample, and validates support-audit
  provenance and thresholds.
- The designer must obtain an executable `PASS`, then the orchestrator reruns that command
  before verifier dispatch.
- The fresh verifier independently executes the same repository-owned geometric predicate
  into verifier-owned output and still reruns all seven checks and actual visual inspection.

Shared code aligns the question being measured; it does not share context, designer results,
or acceptance authority. The designer's result remains `NON-ACCEPTANCE`.

### Evidence compaction

Verifiers re-import the canonical STL in place and bind its hash; they never copy it into
their evidence folder. Rejections preserve a report, numeric metrics, hashes, and the
defect-specific visual, not another STL or unchanged full render set. A later correction
reruns the full Edge ID/support set inside the existing designer commission so defects are
not fixed one at a time.

### V4 adoption hypothesis

On the same frozen T2-style common package, a clean v4 team-only rerun must:

- preserve a score of at least 90, the hard functional gate, all five role gates, the blind
  overlay, one real coupon, and one fresh all-seven visual verifier;
- complete in exactly seven normal-path specialist commissions with zero verifier
  rejections;
- finish in at most 35 minutes, recognizing that seven mandatory file-grounded commissions
  cannot match a one-context six-minute solo run;
- deliver at most 35 non-cache files and 1,000,000 bytes;
- have both designer and verifier shared support audits report zero out-of-limit area and
  cover the identical complete Edge ID set; and
- keep token telemetry honest: report it only when exposed and use operational proxies only
  as non-token evidence.


==========================================================================================
# TEAM PIPELINE — THE FIVE ROLE SLICES
==========================================================================================


<a id="skills__3d-orchestrator__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-orchestrator/SKILL.md`  (89 lines)
------------------------------------------------------------------------------------------

---
name: 3d-orchestrator
description: Route and govern 3D-printable modeling jobs. Use for new modeling or print-prep requests to choose solo monolith versus the five-role file-contract pipeline, enforce phase gates, dispatch specialists, maintain job state, and deliver verified artifacts without authoring geometry.
---

# 3D Orchestrator

## Charter

Own routing, job state, phase gates, user questions, specialist dispatch, project/queue
housekeeping, and delivery. Never write or edit geometric source, STL, STEP, or 3MF content.
Specialists communicate through project files and source photos only, never chat summaries.

## Inputs and outputs

- Inputs: the user request, photos and measurements, repository state, printer constraints,
  and every current contract artifact in the project folder.
- Write: `job_state.md` using the exact schema in
  [`../team-design.md`](../team-design.md#job-statemd).
- Read and gate: `dimensions.md`, `print_plan.md`, `candidate_readiness.md`,
  `verification_report.md`, designer outputs, `final_print_prep.md`, and conditional
  `final_prep_review.md`.
- Housekeeping: the Notion Print Queue entry and physical-change git commits required by
  repository policy.
- Never substitute a chat summary for a contract. Before every dispatch, tell the agent to
  read the named files from disk.

## Required reading

1. [`../3d-modeling/references/team-contracts-v4.md`](../3d-modeling/references/team-contracts-v4.md).
2. For a solo job only, read and run [`../3d-modeling/SKILL.md`](../3d-modeling/SKILL.md)
   unchanged.

## Checklist

1. Create the project folder and compact `job_state.md`; create/update the Print Queue
   entry. Use `COMPACT` unless multi-part/moving/high-consequence work requires `FULL`.
2. Route to **solo** only when the part is simple, single-part, non-fit-critical, has no
   recreated mating geometry, and does not merit independent visual verification.
3. Route to **pipeline** when any condition holds: fit or datum criticality, recreated
   geometry from photos, multiple parts, mating or moving interfaces, safety/thermal/load
   consequences, multi-colour alignment, difficult DFM, or user-requested team/fresh review.
4. In pipeline mode, advance only through:
   `INTAKE -> METROLOGY -> REFERENCE_BUILD -> REFERENCE_ACCEPTANCE -> PRINT_PLAN ->
   CANDIDATE_BUILD -> INDEPENDENT_VERIFICATION -> PRINT_PREP ->
   [FINAL_PREP_REVIEW when required] -> DELIVERY`.
5. Dispatch the metrologist to create `dimensions.md`; gate on complete datum/provenance,
   confidence grades, resolved blockers, and one blind-build-completeness row for every
   visible feature before spending a reference build.
6. Dispatch one designer with the **reference** commission. Then dispatch the metrologist
   again to overlay-accept it. A failure returns to `METROLOGY`: fix the sheet, not the
   reference model.
7. Dispatch the print engineer for the pre-design `print_plan.md`; gate on orientation,
   material, nozzle-linked limits, support budget, chamfers, colour constraints, and a
   frozen `required_now` / `deferred_owner` / `final_gate` scope for every geometry rule.
8. Dispatch candidate designer(s) against the sheet, accepted reference, and print plan.
   Require a hash-bound `candidate_readiness.md` with `status: READY` from the exported STL
   before verifier dispatch, including complete edge/comfort and support-sensitivity
   preflight tables. Independently rerun the v4 `validate-receipts` command and gate on its
   zero exit plus `PASS`; matching Markdown prose is insufficient. `NOT_READY` remains inside
   the same designer commission. Only CadQuery candidates may run in parallel. Serialize all
   FreeCAD work through one instance.
9. Dispatch a fresh verifier that was never a designer and has no candidate-author history.
   Treat designer readiness as untrusted and require all seven checks. A `REJECT` returns to
   `CANDIDATE_BUILD` with the concrete defect list; never ask the verifier to fix it.
10. After candidate `PASS`, dispatch the print engineer for coupon, slicing, print order,
    and field-test details in `final_print_prep.md`. A support-free plan with no deferred
    visual predicate may finish `COMPLETE`. When the plan relies on support contacts,
    toolpaths, or another slicer-dependent visual predicate, require `READY_FOR_REVIEW` and
    dispatch the verifier to write `final_prep_review.md` before delivery.
11. Enforce the plan-revision rule in the shared v3 contract. Any changed candidate
    predicate requires a new readiness receipt and a new fresh full seven-check verifier;
    adding only bound P2 evidence does not.
12. If plan-required native slicer evidence cannot be produced, stop at
    `BLOCKED_NATIVE_SLICER` with hashes and the missing capability. Never label it Ready to
    Print. A non-native exception requires explicit user approval.
13. Deliver only when the exported/re-imported artifacts pass all gates, final print prep is
    `COMPLETE` or has `FINAL_PRINT_PASS`, the queue is current, and the meaningful physical
    iteration is committed.
14. Advance from a commission as soon as its required file receipt is complete and valid;
    do not wait for a chat summary. Record a realistic minute budget per dispatch and ask
    for an exact blocker when it expires.
15. Keep evidence differential. Never copy a canonical STL into a verifier folder. Preserve
    hashes, reports, metrics, and the decisive defect visual; do not fan out unchanged exports
    or full render sets per rejection.

If this skill is loaded inside an agent runtime that cannot spawn nested subagents, keep the
orchestrator in the main session (or launch it as a top-level agent) and dispatch specialists
from there.

<a id="skills__3d-metrologist__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-metrologist/SKILL.md`  (67 lines)
------------------------------------------------------------------------------------------

---
name: 3d-metrologist
description: Establish geometric ground truth for fit-critical 3D jobs. Use to turn photos, caliper readings, official specifications, and existing reference models into a datum-based dimensions.md, and to overlay-accept a blind reference reconstruction before candidate design.
---

# 3D Metrologist

## Charter

Own geometric ground truth for the whole job. Name every feature, attach provenance and a
confidence grade to every number, express positions from named datums, and surface open
questions. Specify the mating object but never model it. Own photo zoom, annotations, and
render-over-photo overlays.

## Inputs and outputs

- Inputs: original-resolution photos, caliper readings, user answers, official product
  specifications, existing-model research, and later the blind reference renders.
- Write: `dimensions.md` using the exact template in
  [`../team-design.md`](../team-design.md#dimensionsmd).
- Write/update: annotated and overlay images with reproducible alignment notes.
- In the reference-acceptance pass, write only the round-trip verdict and sheet corrections.
  Never repair the CAD model.

## Required reading

1. [`../3d-modeling/references/team-contracts-v4.md`](../3d-modeling/references/team-contracts-v4.md):
   `dimensions.md` only.
2. [`../3d-modeling/references/cadquery-patterns.md`](../3d-modeling/references/cadquery-patterns.md):
   datum discipline, render/overlay, inspection, and image-alignment patterns only.
3. Use the shared overlay tools at
   [`../../experiments/overlay_photo.py`](../../experiments/overlay_photo.py) and
   [`../../experiments/verify_visual.py`](../../experiments/verify_visual.py);
   do not copy them.

## Checklist

1. Preserve original images and inspect them at useful zoom; annotate which visible edge
   corresponds to which feature. Note **where the caliper jaws sit**: an overall-envelope
   dimension must be read at a flat, representative region — a read taken across or beside a
   raised feature (button, camera bar, corner radius, lip) is biased and is evidence for that
   local feature, not the envelope. Prefer the flat-region read as nominal and flag near-feature
   reads; corroborate against an official spec when the product is known.
2. For a known product, search official specifications and existing 3D models first, then
   reconcile them with the supplied photos and calipers.
3. Define axis directions, named primary/secondary/tertiary datums, and the zero origin.
4. Inventory every functional, mating, clearance, cosmetic, and uncertain feature. Before
   reference dispatch, complete the blind-build table with count, relative layout/handedness,
   and a datum/bounded envelope or explicit shared-envelope response for every visible
   feature.
5. Record each design-driving dimension with value/range, units, provenance, method, confidence
   (`A measured`, `B official/corroborated`, `C image-derived`, `D assumed`), and datum.
   For a **fit-driving clearance, specify a bounded fit BAND** — a fit class from
   `fdm-design.md` §4 (press/snug/sliding/loose/free) with an explicit min **and** max per side
   — never an open-ended floor. Over-clearance (slop, wobble, a captured part that slips or
   rattles) is a failure mode exactly like interference; do not write "designer may increase"
   without an upper bound. A snug non-moving capture around a known feature targets snug–sliding
   (≈0.1–0.3 mm/side), not "≥0.3 and whatever is convenient."
6. Never silently average conflicts or convert an assumed visual proportion into a measured
   fact. Put unresolved conflicts in open questions with their downstream effect.
7. Mark the minimum set of blocking unknowns that prevents reference construction.
8. After the designer builds the mating reference blind from the sheet, render matching
   photo viewpoints, make one decisive crop/overlay per fit-critical view, and inspect each
   composite by eye. Do not fan out duplicate whole-image overlays.
9. `ACCEPT` only when the reference hugs all fit-critical features within the stated
   tolerance. Otherwise revise `dimensions.md`, increase ambiguity explicitly, and require
   a fresh blind rebuild. The round trip tests the sheet, not the designer.

<a id="skills__3d-designer__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-designer/SKILL.md`  (78 lines)
------------------------------------------------------------------------------------------

---
name: 3d-designer
description: Build parametric FDM-aware CAD from file contracts. Use with either a reference commission, reconstructing the mating object blind from dimensions.md, or a candidate commission, designing printable parts against dimensions.md, the accepted reference, and print_plan.md.
---

# 3D CAD Designer

## Charter

Write geometric source and exported design artifacts for exactly one explicit commission.
For a **reference** commission, reconstruct the mating object from `dimensions.md` alone and
do not inspect the source photos. For a **candidate** commission, design against the sheet,
accepted reference, and print plan. Never verify your own work for acceptance and never edit
the contracts.

## Inputs and outputs

- Reference commission inputs: `dimensions.md` only.
- Candidate commission inputs: accepted `dimensions.md`, reference source/export/renders,
  `print_plan.md`, and prior `verification_report.md` when iterating.
- CadQuery outputs: `model.py`, `verify.py`, per-part STL, combined STEP, renders, and
  `print_notes.md`.
- FreeCAD outputs: `.FCStd` with organized parameters and hidden mating reference, `verify.py`
  or verification macro, per-part STL, combined STEP, renders, and `print_notes.md`.
- Multi-colour jobs also output the required single-file multi-body 3MF.
- Candidate commissions also output `candidate_readiness.md` from the re-imported exported
  STL. It is explicitly non-acceptance evidence.

## Required reading

Read exactly one backend pattern file plus mandatory FDM guidance:

1. CadQuery: [`../3d-modeling/references/cadquery-patterns.md`](../3d-modeling/references/cadquery-patterns.md).
2. FreeCAD: [`../3d-modeling/references/freecad-mcp-patterns.md`](../3d-modeling/references/freecad-mcp-patterns.md).
3. Always: [`../3d-modeling/references/fdm-design.md`](../3d-modeling/references/fdm-design.md).
4. Only when the part uses a standard mechanism:
   [`../3d-modeling/references/mechanisms.md`](../3d-modeling/references/mechanisms.md).
5. [`../3d-modeling/references/team-contracts-v4.md`](../3d-modeling/references/team-contracts-v4.md):
   `candidate_readiness.md` only.
6. Shared deterministic gate:
   [`../3d-modeling/scripts/team_preflight.py`](../3d-modeling/scripts/team_preflight.py).

## Checklist

1. Confirm commission, backend, output folder, units, named datums, tolerances, and contract
   versions before modeling.
2. Keep all design-driving values as named parameters derived from contracts; no unexplained
   magic numbers or scattered coordinate arithmetic.
3. Reference commission: use no photos or hidden dimensions. Model all specified mating
   features so ambiguity becomes visible during the metrologist round trip.
4. Candidate commission: make orientation, layer-vs-load direction, nozzle/wall limits,
   overhangs, support access, shrink/clearance, elephant-foot chamfers, and multi-colour
   constraints geometric inputs from `print_plan.md`.
5. Organize boolean operations robustly; preserve editable source; label bodies and exports.
6. Generate deterministic exports from the source and render useful exterior, mating,
   section, and print-orientation views.
7. Before handoff, re-import the exported STL and keep iterating inside this commission
   until the readiness receipt passes: intended body/integrity and bounds; seated
   interference; full insertion/travel sweep; installed-coordinate section proving the
   open/closed architecture; exact print-plan transform with named bed face at Z=0;
   unsupported-roof and critical-wall floors; required source/STEP/renders and hashes.
8. Before declaring `READY`, execute the v4 edge/comfort preflight for every plan-named
   exposed boundary and the support-sensitivity preflight for every transformed downface,
   roof, bridge, and layer-transition rule. Measure the re-imported STL, record every
   nonzero footprint/interval, and correct failures inside this commission. These are
   deterministic self-checks, never acceptance.
9. Write the machine-readable files required by the v4 contract. Run shared
   `team_preflight.py support-audit` for every support rule and `validate-receipts` for the
   complete Edge ID/support-rule sets. Markdown readiness may say `READY` only when the
   shared validator exits zero and reports `PASS`. After a correction, rerun every row.
10. Provide `verify.py` and `candidate_readiness.md` as useful designer evidence, but mark
   both `DESIGNER SELF-CHECK — NON-ACCEPTANCE`. Never claim the Phase-4 gate passed.
11. Record source parameters, orientation, material assumptions, supports, weak directions,
   and coupon region in `print_notes.md`.
12. When a verifier rejects, change only the owned geometry, regenerate every derived
    artifact, and cite each resolved defect in the next handoff.
13. Never run two FreeCAD designer instances concurrently. Separate CadQuery candidate
    folders may run in parallel and must not overwrite shared contracts.

<a id="skills__3d-verifier__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-verifier/SKILL.md`  (82 lines)
------------------------------------------------------------------------------------------

---
name: 3d-verifier
description: Independently accept or reject fit-critical 3D designs. Use only in a fresh context that did not author the geometry, to audit dimensions.md against photos and to run all seven Phase-4 checks on re-imported exported STL plus visual renders, overlays, and print_plan.md constraints.
---

# 3D Verifier

## Charter

Be fresh eyes. Never reuse a designer context, trust designer self-checks, or repair rejected
geometry. Audit both upstream truth and downstream geometry, look at the renders and
overlays, and issue a concrete file-contract verdict.

## Inputs and outputs

- Inputs: original photos and measurements, `dimensions.md`, accepted reference artifacts,
  `print_plan.md`, candidate source only for traceability, exported STL/STEP/3MF, renders,
  overlays, `candidate_readiness.md`, `verify.py` output, and `print_notes.md`. A conditional
  final-prep review also reads `final_print_prep.md` and its actual contact/toolpath evidence.
- Write: `verification_report.md` using the exact template in
  [`../team-design.md`](../team-design.md#verification_reportmd), plus verifier-owned
  measurements and evidence images.
- Output is `PASS` or `REJECT`; never modified model artifacts.
- For a conditional final-prep review, write `final_prep_review.md`; do not edit the print
  engineer's receipt.

## Required reading

1. [`../3d-modeling/references/team-contracts-v4.md`](../3d-modeling/references/team-contracts-v4.md):
   `verification_report.md` and `final_prep_review.md` only.
2. [`../3d-modeling/references/cadquery-patterns.md`](../3d-modeling/references/cadquery-patterns.md):
   re-import, interference, insertion-sweep, section, render, overlay, and datum-measurement
   patterns.
3. [`../3d-modeling/references/fdm-design.md`](../3d-modeling/references/fdm-design.md).
4. For a FreeCAD candidate, also read
   [`../3d-modeling/references/freecad-mcp-patterns.md`](../3d-modeling/references/freecad-mcp-patterns.md).
5. Shared tools:
   [`../../experiments/overlay_photo.py`](../../experiments/overlay_photo.py) and
   [`../../experiments/verify_visual.py`](../../experiments/verify_visual.py).
6. Shared deterministic support predicate:
   [`../3d-modeling/scripts/team_preflight.py`](../3d-modeling/scripts/team_preflight.py).

## Checklist

1. Confirm you did not author or edit the candidate and re-ground from files and photos.
2. Recompute candidate hashes and treat `candidate_readiness.md` as untrusted completeness
   evidence only. It never passes a check on the verifier's behalf.
3. Audit upstream: independently compare `dimensions.md` values, named datums, provenance,
   and feature inventory against the original evidence. Reject corrupted ground truth.
4. Re-import the exported STL and use it, not the in-memory source, for all geometric checks.
5. Run all seven checks: interference; full-travel insertion sweep; section render; visual
   side-by-side; feature positions from named datums; measurement audit; printability and
   face audit.
6. Actually inspect renders and overlay composites. Do not replace visual evidence with
   bounding-box or scalar checks; note occluded or misleading views.
7. Audit against `print_plan.md`: planned orientation, overhangs/support budget,
   wall/feature sizes versus the planned nozzle, bed chamfers, material/load direction, and
   colour/process constraints. Independently repeat declared edge sections in check 6. In
   check 7, recompute every `SELF_SUPPORT_REQUIRED` predicate and each
   `SUPPORT_ALLOWED` footprint/classification. Rerun shared `team_preflight.py
   support-audit` into verifier-owned JSON for every support rule; never trust the designer's
   JSON or infer contacts from an isometric view.
8. Verify export completeness and consistency: STL/STEP/3MF identities, closed solids,
   intended bodies, units, and no missing or stray components.
9. A `PASS` requires every applicable check to pass with evidence and no open critical
   upstream question.
10. A `REJECT` must identify defect, evidence path, expected versus observed value/appearance,
   named datum or print-plan rule, severity, and owning loop (`METROLOGY`, `PRINT_PLAN`, or
    `CANDIDATE_BUILD`). Never prescribe an unverified geometry fix as acceptance. Every
    changed STL hash requires a new fresh verifier context and a full seven-check rerun.
11. Enforce the shared plan-revision rule. A changed candidate predicate needs a new
    readiness receipt and fresh full seven-check verification even when STL bytes are
    unchanged. Bound P2 evidence added under an unchanged plan does not.
12. When `final_print_prep.md` is `READY_FOR_REVIEW`, inspect actual support contacts,
    toolpaths, sections, and layer maps against the unchanged plan and write
    `final_prep_review.md`. Missing coverage, forbidden/exposed-edge contact, or an unmapped
    footprint rejects or blocks final prep. This review never waives candidate verification.
13. If required native slicer evidence is unavailable, return `FINAL_PRINT_BLOCKED`; do not
    convert notes or a render into native proof.
14. Re-import the canonical STL in place and record its hash; never copy it into the verifier
    folder. For a rejection, retain only the report, metrics, hashes, and defect-specific
    visual in addition to canonical artifacts.

<a id="skills__3d-print-engineer__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-print-engineer/SKILL.md`  (91 lines)
------------------------------------------------------------------------------------------

---
name: 3d-print-engineer
description: "Own manufacturing constraints and physical validation for 3D jobs. Use twice in the team pipeline: before CAD to issue print_plan.md, then after independent verification to define coupons, slicing, print order, and field-test or failed-print procedures."
---

# 3D Print Engineer

## Charter

Own the printer, material, orientation, slicing process, coupons, and failed-print forensics.
Engage before design so DFM is a design input, and after verification so accepted geometry
has an executable physical test plan. Do not redesign geometry or waive verification.

## Inputs and outputs

- Pre-design inputs: `dimensions.md`, functional/load/environment requirements, available
  machines/nozzles/materials, and reference acceptance.
- Pre-design output: `print_plan.md` using the exact template in
  [`../team-design.md`](../team-design.md#print_planmd).
- Post-verification inputs: passing `verification_report.md`, final exports, and
  `print_notes.md`.
- Post-verification outputs: finalized `print_notes.md`, coupon source/export when
  fit-critical, slicing notes/profile, print order, inspection and field-test protocol, and
  failed-print evidence when applicable. Summarize the gate in `final_print_prep.md`.

## Required reading

1. [`../3d-modeling/references/team-contracts-v4.md`](../3d-modeling/references/team-contracts-v4.md):
   `print_plan.md` and `final_print_prep.md` only.
2. [`../3d-modeling/references/fdm-design.md`](../3d-modeling/references/fdm-design.md).
3. [`../3d-modeling/references/printers.md`](../3d-modeling/references/printers.md).
4. [`../3d-modeling/references/materials.md`](../3d-modeling/references/materials.md).
5. For Bambu slicing or multi-colour:
   [`../3d-modeling/references/bambu-3mf-authoring.md`](../3d-modeling/references/bambu-3mf-authoring.md).
6. For failures:
   [`../3d-modeling/references/troubleshooting.md`](../3d-modeling/references/troubleshooting.md).

## Checklist

### Pre-design

1. Select printer, material, nozzle(s), layer height range, and single/dual-nozzle envelope.
2. Set the planned orientation from loads, mating surfaces, visible faces, bridges,
   overhangs, supports, and anisotropy. Record an exact model-to-printer transform, named
   bed-contact landmark at Z=0, bed normal, insertion/open direction, and forbidden
   downward faces.
3. State minimum walls, pins, holes, gaps, embossed/debossed features, tolerance/shrink
   allowances, and load-path rules tied to the planned nozzle/material/profile. Carry the
   metrologist's fit through as a **bounded band (min AND max)**, never a floor; do not widen a
   functional clearance to simplify the plan.
4. Set the support budget and forbidden support-contact faces; require bed-facing
   elephant-foot chamfers where fit geometry approaches the plate. Classify each printability
   rule as `SELF_SUPPORT_REQUIRED` or `SUPPORT_ALLOWED`, and freeze its `required_now`,
   `deferred_owner`, and `final_gate` fields before candidate design.
   **Support-free is the default, not an absolute.** Never require `SELF_SUPPORT_REQUIRED`
   where meeting it forces a *functional* surface — a mating wall, a fit face, a bearing/grip
   face — into a distorting gable, steep taper, or over-wide cavity. When self-supporting would
   compromise function or fit, plan a **bounded `SUPPORT_ALLOWED`** on a *nonfunctional* region
   instead: function and fit win over support-purity. Reserve zero-support absolutism for parts
   where a support-free orientation costs nothing functional.
5. Define multi-colour/body/nozzle constraints and purge/contamination risks.
6. Define the fit coupon region and pass/fail measurements before the designer begins.
   Default to one multi-lane coupon STL; add files only for physically disjoint interfaces.
7. Record assumptions and approval state in `print_plan.md`; unresolved manufacturing
   blockers stop candidate design.
8. Write `print_plan_checks.json` as the exact machine-readable projection of every plan
   Edge ID and support rule. The Markdown and JSON ID sets, transforms, thresholds, and
   dispositions must agree before candidate dispatch.

### Post-verification

1. Confirm the verification report passes the same `print_plan.md` version and final exports.
2. Produce the actual mating-region coupon first for fit-critical parts; default coupon
   material is PLA only when it does not invalidate shrink/thermal behavior.
3. Give slicer/profile, orientation, supports, brims, seam, wall/top/bottom, infill,
   temperature/drying, colour/nozzle assignment, and export/import notes.
4. For every `SUPPORT_ALLOWED` footprint, produce the plan-required native slicer project,
   underside contact-selection view, section/toolpath view per failing interval, and
   footprint-to-contact/layer map. Confirm transform, material, nozzle, layer, line width,
   gap, and interface settings. Support-free plans with zero out-of-limit regions do not
   need a native project solely for ceremony.
5. Write `final_print_prep.md`: use `COMPLETE` only when no deferred visual review remains,
   or `READY_FOR_REVIEW` when support/contact/toolpath evidence needs verifier review.
6. If plan-required native slicer evidence cannot be produced, write
   `BLOCKED_NATIVE_SLICER` with command/version, candidate and plan hashes, missing
   capability, and required action. A `NON_NATIVE` fallback stays blocked without explicit
   user approval.
7. State print order and dimensional/visual inspection after the coupon and final print.
8. Define field-test procedure, acceptance thresholds, safety limits, and rollback.
9. For failure forensics, preserve photos/settings/measurements, identify whether truth,
   geometry, material, slicing, or machine owns the failure, and route to that contract.


==========================================================================================
# SHARED REFERENCE MATERIAL (read by the roles)
==========================================================================================


<a id="skills__3d-modeling__references__team-contracts-v4_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/team-contracts-v4.md`  (432 lines)
------------------------------------------------------------------------------------------

# Team pipeline runtime contracts v4

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
contract_version: 4
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
contract_version: 4
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

A fit-driving clearance is a **bounded band, not a floor.** State a fit class (`fdm-design.md`
§4) with an explicit per-side min **and** max; over-clearance (slop, wobble, a captured part
that slips) fails the fit exactly as interference does. Do not carry a one-sided "≥X, designer
may increase" into the sheet — that is what produces loose, rattly parts that pass every gate.

## `print_plan.md`

```markdown
---
contract: print-plan
contract_version: 4
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

Support-free is the **default, not a hard constraint.** Do not classify a face
`SELF_SUPPORT_REQUIRED` when meeting it forces a *functional* surface (a mating wall, fit
face, bearing/grip surface, or the snug cavity itself) into a distorting gable, steep taper,
or over-wide cavity — that trades a real functional defect for support-purity. Where a
support-free orientation would compromise function or fit, the print engineer plans a bounded
`SUPPORT_ALLOWED` on a *nonfunctional* region instead. Zero-support absolutism is reserved for
parts where it costs nothing functional.

The print engineer also writes `print_plan_checks.json` with every Edge ID and support rule.
This file is the machine-readable projection of the accepted Markdown plan, not a second
source of requirements:

```json
{
  "schema_version": 4,
  "candidate_predicate_revision": 1,
  "edges": [
    {
      "id": "E-01",
      "min_radius_mm": 0.4,
      "max_radius_mm": null,
      "samples_required": 3
    }
  ],
  "support_rules": [
    {
      "id": "S-01",
      "disposition": "SELF_SUPPORT_REQUIRED",
      "model_to_printer_matrix": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
      "bed_z_mm": 0,
      "bed_tolerance_mm": 0.05,
      "downward_normal_z_max": -0.70710678,
      "max_out_of_limit_area_mm2": 0
    }
  ]
}
```

Use `allowed_sharp: true` only with `allowed_sharp_reason`. A `SUPPORT_ALLOWED` row also
names `allowed_contact_class` and forbidden faces in the Markdown plan. The print engineer
must make the Edge ID and support-rule ID sets complete before candidate CAD.

## `candidate_readiness.md`

This is designer-owned dispatch evidence. It is never acceptance and never substitutes for
fresh verification.

```markdown
---
contract: candidate-readiness
contract_version: 4
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

The designer also writes `candidate_preflight.json`, one shared support-audit JSON per
support rule, and `candidate_preflight_validation.json`. It must run:

```text
python skills/3d-modeling/scripts/team_preflight.py support-audit \
  --stl <candidate.stl> --plan print_plan_checks.json --rule-id <S-ID> \
  --output <S-ID>-support-audit.json

python skills/3d-modeling/scripts/team_preflight.py validate-receipts \
  --stl <candidate.stl> --plan print_plan_checks.json \
  --readiness candidate_preflight.json \
  --output candidate_preflight_validation.json
```

`candidate_preflight.json` binds the STL and plan-check hashes, contains exactly every plan
Edge ID with numeric `samples_mm`, method, and evidence, and exactly every support-rule ID
with its shared audit path. The validator must exit zero and report `PASS` before Markdown
readiness may say `READY`. After any correction, rerun the full Edge ID and support-rule
sets, not only the last reported defect.

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
contract_version: 4
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

The verifier reruns `team_preflight.py support-audit` into verifier-owned JSON for every
support rule and independently checks that its edge evidence covers the exact plan Edge ID
set. Shared code standardizes the geometric predicate; a fresh context, fresh execution,
fresh visual inspection, and independent measurements preserve verifier independence.

Do not copy the canonical candidate STL into verifier folders. Re-import it in place and
record its hash. A rejected run retains its report, metrics, the defect-specific visual, and
source/output hashes; it does not duplicate unchanged full render sets or exports. A passing
run retains the canonical full report and only verifier-owned visuals that add evidence.

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
contract_version: 4
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
contract_version: 4
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

<a id="skills__3d-modeling__references__fdm-design_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/fdm-design.md`  (235 lines)
------------------------------------------------------------------------------------------

# FDM design reference — numbers and tactics

Values assume a tuned 0.4 mm nozzle, 0.2 mm layers. Sources at end.
§1 printability · §2 orientation/strength · §3 no-supports · §4 fits · §5 print-in-place
· §6 multi-color · §7 materials by environment · §8 finishing · §9 production rules
· §10 domes, curves & rotors.
Deeper dives: [mechanisms.md](mechanisms.md) (hinges/springs/magnets),
[materials.md](materials.md) (filament picks, support pairings),
[troubleshooting.md](troubleshooting.md) (symptom→fix).

## 1. Printability rules

- Overhangs ≤ 45° from vertical always print clean; well-cooled modern machines manage
  50–60° in PLA. Design to 45, accept 50 when unavoidable.
- Bridges (one rule, cited elsewhere): ≤5 mm pristine · 5–25 mm fine on modern machines
  · 25–50 mm sags — hidden undersides only · >50 mm add internal ribs or supports.
  Long shallow custom curves/fillets under a surface: keep ≤30° from horizontal or they
  need support.
- Walls: ≥ 2× nozzle (0.8 mm); make wall thickness a multiple of line width (0.8/1.2/1.6)
  to avoid gap-fill. Vertical pins ≥ Ø5 mm or they snap — use steel dowels below that.
- Text/detail (single-color engrave/emboss): stroke 0.5–1 mm wide; engraved 0.5–1 mm
  deep; embossed 0.5–0.75 mm tall, never >1 mm (sags). Multi-color inlay strokes need
  ≥0.8 mm (§6). Surface textures ≥0.4 mm wide (nozzle width); knurling 0.5 mm wide /
  0.5 mm spacing.
- Slicer manipulation: a 0.2–2 mm wide slot or disc cut through a region forces the
  slicer to build solid perimeter walls there — free local reinforcement around holes,
  bosses, and rods without touching infill settings.
- Vertical holes: 1 mm fillet on the top edge = screw funnel + stops top-layer pull-out.
- Vents: 45° slats as thin as 0.5 mm; overlap + stair-step the slats to block water
  splash while passing air.
- Holes print undersized: +0.3–0.5 mm on Ø2–3, +0.2–0.4 on Ø3–8, +0.2–0.3 on Ø8–12.
  Oversize in CAD or use slicer X-Y hole compensation (0.05 PLA / 0.1 PETG-ABS);
  drill/ream critical bores. §4 fit clearances are ON TOP of this correction for mating
  bores — apply hole compensation first, then the fit clearance; don't confuse the two.
- Bed-contact edges: 45° chamfer 0.2–0.4 mm (beats slicer elephant-foot compensation).
  Chamfer horizontal/overhanging edges; fillet only vertical edges. Never fillet into the
  bed plane (creates a near-0° overhang).
- Horizontal holes: teardrop (to ~Ø4) or flat-roof/diamond with +0.4 mm above nominal.
- Vase mode: one continuous contour per Z, no islands/holes; line width 150–200% of nozzle.

## 2. Orientation & strength

- Across-layer (Z) strength ≈ 55–67% of in-plane; design as if half. Never load a
  cantilever root, screw boss, or snap arm across layers.
- Orientation decision order: (1) big flat face on bed, (2) overhangs minimized/designed
  out, (3) layers aligned with load, (4) cosmetic faces up/outward — never on supports,
  (5) seam on a hidden or sharp edge, (6) multi-color layers as low as possible.
  Conflicts? Split the part (dovetails or pins + glue), each half in its ideal orientation.
- One-piece boxes/enclosures: print **diagonally on an edge at 45°** (lids/trays ~35°)
  — box+lid pairs instead get a diagonal parting line, §9. Diagonal printing kills
  supports, layer lines loop through every wall (no single splitting plane — flat-printed
  parts are up to 3× stronger along layers), uniform finish on all faces. Flatten a
  small land on the down edge for bed adhesion.
- Strength budget: perimeters >> infill. Structural default: 4 walls, 5 top/bottom,
  30–40% gyroid (near-isotropic). >50% infill is wasted; add walls instead.
- FDM cost ≈ surface area, not volume: thick voluminous parts beat thin-walled/ribbed
  ones (weight-saving cutouts often ADD time and material). Don't model internal
  cavities — let honeycomb infill lightweight it; modeled thin shells put layer seams
  at stress concentrations.

## 3. Designing out supports

- Put 45° chamfers under every boss, counterbore, and side protrusion.
- Sacrificial bridge: roof a counterbore with one bridged layer, drill/punch after; leave
  0.4 mm droop clearance under any bridged roof that matters.
- Model break-away tabs with a 0.2 mm (1-layer) gap where a slicer support would scar.
- Designed bed helpers, exact numbers: raft 1 mm thick; brim 0.2 mm (one layer);
  tie-down struts 1 mm wide; one-layer "velcro" connection points 0.4–0.5 mm. Large flat
  first layers: warp-relief checkerboard cuts 1 mm deep spaced ~25 mm apart.
- Internal steps: widening-upward needs nothing; narrowing-upward creates internal bridges
  — flip the part or chamfer the transition.
- Prefer a designed bridge (or a 1-layer sacrificial floor punched out after) over any
  support — span limits per §1.
- When support is unavoidable, **model it in CAD** so every print is identical: triangular
  fins parallel to the overhang, body 0.5–1 mm off the part, connected by 0.5 mm snap
  prongs; ~0.2 mm top gap, 0.2–0.3 bottom; 45° the fins themselves; wide base; chamfer
  so they break away by hand. "Thumbtack" pin supports stabilize tall diagonal parts.
  Cut holes through sacrificial blocks (crush to remove) and emboss "SUPPORT" on them.
  Trick: generate tree supports in a slicer's SLA mode, export STL, place in CAD.

## 4. Fits & tolerances (per-side clearance — store per-side values in Params cells / PARAMETERS variables)

- Press: 0.0–0.1 mm · snug: 0.1–0.2 · sliding: 0.15–0.3 · loose: 0.3–0.5 ·
  free rotation: 0.4–0.7. PETG/ABS want +0.05 over PLA. Mating parts from another
  printer: 0.5. (Diametral = 2× these.)
- Press-fit insurance: 3–4 crush ribs 0.2 mm proud inside a +0.4 mm bore — ribs deform
  plastically, bore doesn't crack — but **single assembly only** (refit force collapses).
  For repeated assembly use **grip fins** (thin elastic fins that flex, not crush):
  fin ID 1 mm under the rod diameter (11 mm ID grips a 12 mm rod), 0.3 mm clearance gap
  behind each fin — constant grip that also absorbs shrinkage.
  Hex/square bores tolerate interference better than round.
- Alignment: **diamond pins** — square pins rotated 45° in diamond holes — self-center
  and print sideways with zero overhang sag (round pins print oval on their side).
  Panel edge-joins: curved **spring T-slots** that compress on insertion.
- Compliance beats precision: a fit tuned on one printer/material won't transfer. Build
  in flex — slot behind a wall so it springs (gap 0.3–0.5 mm), chamfer mating lid edges
  so parts wedge over a range, cut away box corners (least accurate region, where fits
  bind). Assume ±0.1 mm per surface; single-layer features run undersized.
- Tight or unknown fit → print a coupon first: ladder of holes/pegs stepped
  0 / 0.1 / 0.15 / 0.2 / 0.3 / 0.4 mm. Ten minutes of printing saves the real part.
- Snap fits: taper the arm toward the tip, base fillet ≥ 0.5× thickness, deflect only
  during assembly, print the arm lying in the layer plane. PETG/ABS/PA — PLA arms shatter.
- Threads: model ≥ M8 (≥1/8") vertical with 0.15–0.3 mm radial clearance, trapezoidal
  profile, thread features 2–4 mm; horizontal threaded holes: cut away the top and
  bottom arcs of the thread (sag zones) — the sidewall threads alone grip the screw.
  Below M8 use heat-set inserts — M6–M8 either works, inserts win for repeated assembly
  — (hole Ø4.1–4.3 for M3, blind hole +1 mm, 1–2 mm solid
  plastic around the hole, iron ~10–20°C above print temp) or captive nuts (pocket
  +0.1–0.2 mm, pause-and-insert, bridge over) — a flanged nut dropped in mid-print with
  plastic grown over it is pull-out-proof.

## 5. Print-in-place & moving parts

- Gaps: 0.3 mm minimum between PIP features; 0.4–0.6 for free-spinning axles/hinges;
  vertical gaps ≥ 2 layers (0.4 mm). First motion "cracks" the joint free — keep contact
  area small.
- Living hinges (materials canon: mechanisms.md §1): PP/TPU for real cycle life;
  PETG/PA survive a few gentle cycles; PLA never.
  Web 0.2–0.5 mm × 3–6 mm span, filleted, printed flat on the bed — never bridged.
- Compliant mechanisms: keep flexure strain low and add hard stops limiting travel.
- Full catalog — 9 hinge types, printed springs, magnet retention, pin strengthening:
  [mechanisms.md](mechanisms.md).

## 6. Multi-color / multi-material

- **Waste economics**: single-nozzle AMS purges on every swap (dark→light ≈ 3× light→dark;
  a 12 g model can make 70 g waste). Prime tower height = last color-change layer, so
  concentrate color in few, contiguous, **low** layers. Dual-nozzle (X2D/H2D): ~zero purge
  between two materials; >2 colors still purge within a nozzle group.
- **Face-down graphics**: mirror text/logo into the bottom face, colors in layers 1–3 —
  minimal purge, razor-sharp boundaries, uniform plate finish. Guard with elephant-foot
  compensation ≥ 0.15 so thin strokes don't bleed. This also shrinks the prime tower.
- **Flush inlays**: cut the recess and the inlay from the same sketch, zero clearance
  (same-layer extrusions fuse); 0.4–0.6 mm deep (2–3 layers) hides the base color; stroke
  width ≥ 0.8–1.0 mm, bold sans fonts. Export as one 3MF via scripts/make_3mf.py.
- **Free color tricks**: color-change-at-Z (pause/M600) gives per-band color with zero
  purge and no AMS; engrave-and-paint-fill or a sticker recess when only one filament.
- **Bonding matrix**: same polymer = welds. Welds well: ABS↔ASA, PETG↔TPU, ABS/ASA↔TPU,
  PETG↔ABS. Separates cleanly (use as support interface or avoid as structure):
  PLA↔PETG, PLA↔ASA/ABS, TPU↔PLA, PA↔almost everything. Co-printed colors must share a
  polymer family or be mechanically interlocked (dovetails, through-holes, captive geometry).
- Mixed-material jobs share one bed/chamber: don't pair PLA with ABS/ASA (bed 60 vs 95 °C,
  chamber heat-creeps PLA); PLA+PETG at ~60–65 °C is the workable odd couple.

## 7. Material by environment

| Material | HDT/Tg | Notes |
|---|---|---|
| PLA/PLA+ | ~57/60 °C | Creeps under load at room temp; fades in UV. Prototypes, fit tests |
| PETG | ~69/80 °C | Easy, tough, decent UV; top-rack dishwasher risky |
| ABS | ~87/105 °C | Yellows in UV; acetone-weldable/smoothable |
| ASA | ~100 °C | Outdoor + car-interior default; acetone-weldable |
| PC | ~117/147 °C | Boiling-water capable; hygroscopic |
| PA/PA-CF | HDT 190–205 °C | Strongest; absorbs water, bonds to nothing |
| TPU | flex, −30…+80 °C | Grips/gaskets/feet; soft grades need external spool |

Parked car in sun (cabin 60–80 °C, dash to 105 °C): ASA/ABS/PC only — PLA fails, PETG
marginal. Outdoors year-round: ASA. Always propose the PLA fit-test before printing the
final in engineering material.

## 8. Finishing tricks

- Fuzzy skin hides layer lines and adds grip; ironing smooths top faces (~10–15% flow).
  Better: model texture in CAD (knurl, crosshatch, noise) — travels with the file,
  free in FDM (vs tooling cost in molding). Avoid raised details thinner than the nozzle.
- Seams distort round walls up to 0.4 mm and protrude into holes — give the slicer a
  sharp concave corner (≥120°) to hide the seam in, or align to a hidden edge. Vertical
  holes: a 120° teardrop corner does the same job.
- Warping: CAD-modeled mouse-ear tabs (0.2–0.4 mm discs) release cleaner than brim;
  rounded outer contours warp less than sharp corners.
- Shrinkage scaling: ABS ~0.4–0.8%, ASA ~0.6%, PLA ~0.2–0.3% — or measure a test cube.
- Annealing PLA (100 °C/45 min): heat resistance jumps, strength barely, dimensions shift
  up to 10% — rarely worth it vs printing ASA.
- Gluing: CA for PLA/PETG/ABS; epoxy for gaps/dissimilar; acetone welds ABS/ASA
  near-monolithic; PP/TPU need roughening + specialty adhesives.

## 9. Production rules (print-farm wisdom — cheap insurance on any print)

- **Design slicer-agnostic**: every functional feature lives in CAD, never in slicer
  settings — the part must print right at any layer height, infill, or machine.
- First layer: as close to a circle as possible — no sharp corners, no text, minimal
  area on the bed face; sharp first-layer corners are the #1 warp/curl failure. Slightly
  recess (bow) large bottom faces to cut contact area.
- Chamfer the bottom perimeter ≥1 mm on production parts (machine-independent
  elephant-foot immunity); 0.2–0.4 mm where the dimension is critical.
- Round/fillet every vertical edge ≥1 mm: the nozzle never decelerates into corners →
  faster, stronger, more accurate, less ringing. Inner corners: chamfers stair-step
  predictably. Replace thin flat mounting tabs with chunky monolithic tabs grown from
  the body, chamfered underneath.
- Enclosures: cut the box/lid parting line diagonally so both halves print belly-down
  supportless; square lids with cut-out corners wedge tight on the flat walls; grip fins
  hold lids at constant pressure; quarter-turn lids = nub + channel <2 mm deep (or
  chamfered); sliding latches = print-in-place spring with ~2 mm travel. Hide any box
  inside an organic shell by boolean-cutting the cavity + standoffs into it; integrate
  DIN-rail / extrusion / strap mounts directly into the body.
- Batch tricks: group parts on a 1 mm raft (whole batch ejects as one), connect
  multi-part assemblies with snip-sprues so they ship assembled, stand large panels on
  edge held by thin fins.
- Invisible extras: text/logo/barcode embedded 0.5–1 mm under the surface reads only
  when backlit. Internal glue channels: assemble dry, inject glue at one port, channels
  route it everywhere — doubles as internal rebar.
- Fillet every feature-to-body transition — sharp inside corners are where FDM cracks.
- Text: ≥3 mm tall (stroke/depth floors in §1); deboss beats raised; cleanest on
  vertical faces; never on the bed layer.
- Zip-tie channels: ~4.8 OD / 3.2 ID tube sections, perpendicular to layers.
- Shadow lines: deliberate 0.5–1.5 mm gaps between mating shells hide fit imperfections.
- Zero post-processing target: no supports, no bed-face cleanup, textures hiding layer
  lines — every human touch multiplies cost at volume.

## 10. Domes, curves & rotors

- Domes: make them egg-shaped/oblong (steeper overhang) or keep the outside spherical
  and cut the inside to a cone — the sag is always internal. If support is needed, a
  designed internal "mushroom" 0.5 mm below the arch apex, or flatten the interior apex
  so slicer supports get a clean pop-off target.
- Spheres: cut a flat base at 60° tangent; or lift on a disc + fat 1 mm pin; star-pattern
  fin supports offset 0.2 mm beat solid cylinders (airflow → no thermal shrink lines).
- Shallow top curves stair-step: drop to 0.1 mm layers, or facet the curve deliberately,
  or pixelate it in 1 mm steps as an aesthetic, or hide it under noise/knurl/concentric
  rings; a domed lid with a flat edge chamfer can print on its side instead.
- Vase mode: prismatic folds/creases for rigidity; never a flat roof — slot the ceiling
  so the path stays one continuous outline.
- Propellers/fans: hub flat on bed, blade pitch >45° (shallower → designed vertical
  supports 0.3 mm off, twist away); a thin ring joining blade tips = permanent support;
  serrated/micro-blade leading edges are free in FDM.
- Rings with clips: best printed on their side on an octagonal outer flat; clips at 45°
  to the bed so they don't align with the weak layer plane; bottom clips moved to touch
  the bed need no support.

Sources: hubs.com/knowledge-base (FDM design, snap fits), blog.rahix.de/design-for-3d-printing,
cnckitchen.com (layer adhesion, inserts, annealing), wiki.bambulab.com (shrinkage, flush,
TPU), help.prusa3d.com (purging volumes), toms3d.org (material combination tests),
bambulab.com/en/filament-guide, orcaslicer.com/wiki (flush options), Slant3D channel
(production DFAM, supports, tolerances, mechanisms), The Next Layer (filaments,
troubleshooting), Planet 3DP (X2D support-interface tests).

<a id="skills__3d-modeling__references__cadquery-patterns_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/cadquery-patterns.md`  (195 lines)
------------------------------------------------------------------------------------------

# CadQuery — tested code patterns

**When to pick CadQuery** (vs FreeCAD): runs anywhere Python does — no desktop, no GUI
dependency; iteration is cheap and fast; verification is scriptable; previews render
headless. Best cost/quality ratio in our benchmark. **Costs**: the user edits a .py, not
a GUI document (also ship STEP so any CAD can open it); OCC kernel pitfalls below
(fillet corruption on scalloped solids, volume misreport on periodic splines); every
output must be delivered explicitly — nothing lands on the user's disk by itself.

Run everything through the bundled runner — it executes the script, finds the STL,
renders a multi-view preview, and returns JSON (`success`, `stderr`, `stl`, `preview`,
`watertight`):

```bash
python3 scripts/run_cadquery_model.py model.py --preview --strict   # strict: non-watertight = fail
python3 scripts/preview.py model.stl preview.png --views multi      # render-only
```

`success: false` → read `stderr`, fix the script, re-run. Always LOOK at the preview.

## Script skeleton (one file, parameters first)

```python
import cadquery as cq

# ==== PARAMETERS (mm; provenance in comments) ====
shaft_d       = 12.9   # measured, caliper photo 1
fit_clr_side  = 0.15   # per-side, sliding fit — fdm-design §4
bore_depth    = 74.0   # rod exposed 72.1 + 1.9 seat offset
# ==== MODEL ====
body = (cq.Workplane("XY")
        .circle(46/2).extrude(95)                      # never centered in Z: bed at Z=0
        .faces("<Z").workplane()
        .hole(shaft_d + 2*fit_clr_side, bore_depth))
# ==== REFERENCE (mating object, NOT exported) ====
ref_part = (cq.Workplane("XY").circle(shaft_d/2).extrude(72.1)
            .translate((0, 0, 1.9)))                   # seated position
# ==== EXPORT ====
cq.exporters.export(body, "body.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "body.step")
print("volume", body.val().Volume(), "bbox", body.val().BoundingBox().xlen)
```

- Bottom of the part at Z=0 in print orientation (`centered=(True, True, False)`).
- Booleans: `.cut()`, `.union()`, `.intersect()`. Chain fillets AFTER shell/booleans,
  largest radius first; a failing fillet usually means the radius ≥ local wall.
- OCC pitfalls (observed): fillet/chamfer on scalloped/periodic-spline edges can silently
  corrupt the solid — assert `isValid()` AND a sane volume delta after every
  fillet/chamfer/boolean; if one corrupts, replace it with a revolved or wedge cut.
  `.val().Volume()` can misreport on periodic-spline solids — trust the exported mesh
  (trimesh volume), which is also what Phase 4 must measure.
- Selectors: `faces(">Z")`, `edges("|Z")`, `edges("<Z")` (bed chamfer: `.chamfer(0.5)`).

## Phase-4 verification patterns

```python
# 1. seated interference (must be ~0)
inter = body.intersect(ref_part)
print("interference", inter.val().Volume() if inter.val().Solids() else 0.0)

# 2. insertion sweep — ref less deep by t, still no interference
for t in (5, 15, 25, 35, 45, 55, 65):
    r = ref_part.translate((0, 0, -t))
    s = body.intersect(r)
    v = s.val().Volume() if s.val().Solids() else 0.0
    assert v < 1e-6, f"insertion blocked at travel {t}: {v}"

# 3. section render: cut half, export, preview
half = body.cut(cq.Workplane("XY").box(500, 500, 500, centered=(False, True, True)))
cq.exporters.export(half, "section.stl", tolerance=0.01, angularTolerance=0.1)

# 4. visual side-by-side vs reference model / photos — SAME cameras, one image
import sys; sys.path.insert(0, '<skill>/scripts'); from preview import render_view
from PIL import Image
import trimesh
ref_mesh = trimesh.load('ref.stl')                  # render_view takes trimesh meshes,
cand_mesh = trimesh.load('body.stl')                # not CadQuery Workplanes
views = [(89, -90), (5, -90), (25, -60)]            # top, front, iso
row_r = [render_view(ref_mesh, e, a, 420, 420) for e, a in views]
row_c = [render_view(cand_mesh, e, a, 420, 420) for e, a in views]
canvas = Image.new('RGB', (3*420, 2*420), 'white')
for i, im in enumerate(row_r + row_c):
    canvas.paste(im, ((i % 3)*420, (i // 3)*420))
canvas.save('side_by_side.png')                      # then LOOK at it and compare
# feature-by-feature: silhouette, shapes, counts, positions — before any export

# 5. feature positions from named datums — on the EXPORTED STL
import trimesh, numpy as np
m = trimesh.load('body.stl')
sec = m.section(plane_origin=[0, 0, 1.0], plane_normal=[0, 0, 1])
# ALWAYS pass plane_transform: bare to_2D() re-origins on a path-dependent frame,
# so hole centers silently stop matching model-coordinate datums
p, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, 1.0], [0, 0, 1]))
for poly in p.polygons_full:
    for hole in poly.interiors:
        c = np.array(hole.coords)
        ctr, size = (c.min(0) + c.max(0)) / 2, c.max(0) - c.min(0)
        print('hole', np.round(size, 1), 'center', np.round(ctr, 1))
# compare each center to the Phase-2 datum values (e.g. camera window: +5.5 from
# centerline, 36.7 from top edge). Size alone never passes a placement check.
# Handedness: also compare with x negated — mirrored layouts fit the numbers too.

# 7. face audit half of check 7 — cylindrical radii present in the part
#    (check 6, measurement audit, is a manual diff of prompt numbers vs geometry;
#     printability half of check 7: next section)
import re
radii = sorted({round(f.radius(), 2) for f in body.val().Faces()
                if f.geomType() == "CYLINDER"})
print("cyl radii", radii, "bbox", body.val().BoundingBox())
```

## Render-over-photo overlay loop (recreating a part from photos)

Side-by-side comparison catches gross mismatch; an OVERLAY catches millimeters. When a
near-orthographic photo exists (top/front view), draw the model's slice boundaries ON
the photo and iterate parameters until they hug the features:

```python
# 1. segment the part's bbox in the photo (non-white profile rows/cols, or threshold)
# 2. map model mm -> photo px: fit model slice bbox to photo bbox, y flipped
# 3. slice the exported STL (plane_transform! see item 5) at feature depths,
#    draw every exterior+interior ring on the photo in red, save, LOOK
# 4. adjust the named parameters the misfit points at; re-export; repeat
```

Rules learned running this: iterate against the PHOTO only (never against a scoring
reference — that's tuning to the answer key); a mean-distance-to-nearest-edge residual
is a useful trend number but too forgiving to decide with (any line lands near SOME
edge in a busy photo) — the overlay image decides; apply the same trick to iso/side
photos to catch vertical architecture (raised rims, ramps, dips) that top views hide —
render your model from the photo's viewpoint and compare silhouettes. Measured result:
one overlay iteration took a photo recreation from layout-IoU 0.59 to 0.70 vs ground
truth; the loop also exposed pocket-mouth chamfers and a raised-end architecture that
side-by-side viewing had missed.

## Printability audit helpers (trimesh, on the exported STL)

```python
import trimesh, numpy as np
m = trimesh.load("body.stl")
print("watertight", m.is_watertight, "volume", m.volume)
down = m.face_normals[:, 2] < -0.7071                # faces steeper than 45° down
overhang_area = m.area_faces[down & (m.triangles_center[:, 2] > 0.3)].sum()
print("unsupported overhang area mm2", overhang_area)  # ~0 for a support-free print
```

## Extracting a chunk from a NON-watertight source mesh (scans, marching cubes)

Do **not** chain `trimesh.slice_plane(cap=True)` to whittle a region out of a dirty mesh:
capping a face with sub-micron float noise on nominally-flat faces, or with sliver
triangles, leaves thousands of unshared edges — the result isn't a volume and the next
boolean dies with `Not all meshes are volumes!`. Instead feed the raw face soup straight to
`manifold3d` and take the region as ONE boolean intersection against a box:

```python
import trimesh
src = trimesh.load("scan.stl", process=False)          # keep the raw faces as-is
box = trimesh.creation.box(extents=(bx, by, bz))
box.apply_translation((cx, cy, cz))                    # the chunk you want to keep
chunk = trimesh.boolean.intersection([src, box], engine="manifold")
```

- **Dodge a noisy flat face**: cut a hair (~0.01 mm) ABOVE it, then translate the chunk back
  down to z=0 — you get a genuinely planar face instead of inheriting the float noise.
- **Self-touching marching-cubes surfaces**: fine in memory (the two sheets have distinct
  vertex indices), but go non-manifold the instant a binary STL merges coincident vertices
  on export. Nudge such vertices ~2 µm apart before writing the STL.

## Common shapes

```python
# revolve a profile (knobs, bulbs)
profile = cq.Workplane("XZ").polyline([(0,0),(15,0),(23,40),(8,95),(0,95)]).close()
solid = profile.revolve(360, (0,0,0), (0,0,1))
# polar pattern (bolt circles, fins)
r = 20  # bolt-circle radius
wp = (cq.Workplane("XY").pushPoints(
      [(r*__import__('math').cos(a), r*__import__('math').sin(a))
       for a in [i*2*3.14159/6 for i in range(6)]]).circle(1.6).cutThruAll())
# text (engrave 0.6 deep)
body = body.faces(">Z").workplane().text("R", 8, -0.6, font="DejaVu Sans", kind="bold")
# shell an enclosure (open top)
box = cq.Workplane("XY").box(60, 40, 25, centered=(True, True, False)).faces(">Z").shell(-2)
```

## Multi-color

Export each color as its own STL from the same script (shared coordinates), then:
`python3 scripts/make_3mf.py out.3mf "Body=body.stl" "Inlay=inlay.stl"` — one 3MF,
one build object, one component per part; Bambu/Orca import it as a single object with
parts individually assignable to filaments. Inlay geometry rules (flush recess, zero
clearance, stroke ≥0.8 mm): fdm-design §6.

Slicer-facing design decisions (orientation, prime tower, materials, clearances) live in
`fdm-design.md` — consult it, not memory.

<a id="skills__3d-modeling__references__freecad-mcp-patterns_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/freecad-mcp-patterns.md`  (135 lines)
------------------------------------------------------------------------------------------

# FreeCAD MCP — tested code patterns

**When to pick FreeCAD** (vs CadQuery): the user gets a parametric FCStd they can open
and edit; Params spreadsheet makes every fit fix a one-cell change; renders come from the
real GUI; outputs save directly to the user's disk. Benchmark winner on design quality.
**Costs**: needs the desktop + FreeCAD + MCP addon running; every execute_code returns a
~10k-token screenshot, making it the most expensive backend (plan ≤8 chunks per job);
single instance — parallel jobs serialize. No desktop connected → use CadQuery.

These patterns were proven working on the user's machine through the FreeCAD MCP
(`mcp__remote-devices__freecad__*` tools). Every `execute_code` call returns stdout plus a
viewport screenshot — always print check values and look at the screenshot.
Screenshots make each call expensive (~10k tokens): plan the job into FEW large
execute_code chunks (aim ≤8 per job), print all check numbers in each, and never make
a call just to peek.

## Session setup

- First call `list_documents`. If the freecad tools are missing or error, the user's
  desktop/FreeCAD isn't connected — ask them to open FreeCAD with the MCP addon; never
  fall back to guessing geometry offline.
- `list_documents` → `create_document` with a project name (snake_case).
- Files save directly to the user's disk from inside FreeCAD (`doc.saveAs`, `Mesh`/`Part`
  export, `saveImage`) — no staging round-trip for outputs FreeCAD itself writes.
  Files built in the cloud container (the 3MF, print_notes.md) must be sent back
  explicitly: SendUserFile → `device_commit_files` into the project folder.
- Keep each `execute_code` chunk small enough to verify: build → print `Shape.isValid()`,
  `Volume`, `BoundBox` → next chunk.
- Hide the reference part before final renders/exports:
  `doc.RefPart.ViewObject.Visibility = False`.

## Params spreadsheet driving geometry

All clearance cells store **per-side** values (the convention of fdm-design §4).

```python
sheet = doc.addObject('Spreadsheet::Sheet', 'Params')
rows = [('shaft_d', 12.9,      'measured rod shaft diameter'),
        ('fit_clr_side', 0.15, 'per-side clearance — pick from fdm-design §4')]
for i, (name, val, note) in enumerate(rows, start=1):
    sheet.set(f'A{i}', name); sheet.set(f'B{i}', str(val)); sheet.set(f'C{i}', note)
    sheet.setAlias(f'B{i}', name)
doc.recompute()

bore = doc.addObject('Part::Cylinder', 'MainBore')
bore.setExpression('Radius', 'Params.shaft_d / 2 + Params.fit_clr_side')
bore.setExpression('Height', 'Params.bore_depth')
```

Read back with `sheet.get('alias')`. Update with `sheet.set('B6', '74')` + `recompute()`.

## Sculpted solids (revolves) + parametric cut chain

```python
import Part
from FreeCAD import Vector as V
bs = Part.BSplineCurve(); bs.interpolate([V(r,0,z) for r,z in profile_pts])
wire = Part.Wire([Part.makeLine(V(0,0,0), V(r0,0,0)), bs.toShape(), ...])
solid = Part.Face(wire).revolve(V(0,0,0), V(0,0,1), 360)
fo = doc.addObject('Part::Feature', 'OuterBody'); fo.Shape = solid   # static sculpt
cut1 = doc.addObject('Part::Cut', 'Cut1'); cut1.Base = fo; cut1.Tool = bore  # parametric
```

Static base + parametric cutters keeps recompute working when Params change.

## Text / logos (two-color inlays)

```python
import Draft, os
CANDIDATES = ['C:/Windows/Fonts/arialbd.ttf',                       # Windows
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
              '/System/Library/Fonts/Supplemental/Arial Bold.ttf']  # macOS
FONT = next((f for f in CANDIDATES if os.path.exists(f)), None)  # none → ask user for a .ttf
ss = Draft.make_shapestring(String='5', FontFile=FONT, Size=5.0)
doc.recompute(); sh = ss.Shape.copy(); doc.removeObject(ss.Name)
if not sh.Faces: sh = Part.makeFace(sh.Wires, 'Part::FaceMakerBullseye')  # holes in R, 4...
# center via sh.BoundBox, translate, extrude 0.6, fuse with gate bars
```

Make the inlay a separate solid that exactly fills a recess cut from the body: export both,
they print flush. Keep inlay strokes ≥ 0.8 mm wide (multi-color floor; single-color
engrave/emboss floors are lower — fdm-design §1).

## Fit verification (Phase 4)

```python
inter = part.Shape.common(rod.Shape)           # rod at final inserted Placement
print('interference volume:', inter.Volume)     # must be ~0
halfbox = Part.makeBox(200,100,300, V(-100,0,-50))
section = doc.KnobBody.Shape.cut(halfbox)       # half-section for render
radii = sorted({round(f.Surface.Radius,2) for f in part.Shape.Faces
                if isinstance(f.Surface, Part.Cylinder)})
print('cylindrical radii:', radii, 'bbox:', part.Shape.BoundBox)
```

Visual side-by-side (Phase 4 check): render the part and RefPart from the SAME saved
camera views as the user's photos (set the view, `saveImage`, repeat per model with the
other hidden), stage the PNGs back, compose one side-by-side image, and look at it
feature-by-feature before export. Feature positions: verify on the **exported STL** in
the cloud container — `device_stage_files` the STL back first — (trimesh slice → hole
centers vs named datums — snippet in cadquery-patterns.md §Phase-4 item 5); the in-memory shape is not the artifact, and
check handedness — a mirrored layout fits the numbers too.

## Renders

```python
import FreeCADGui as Gui
doc.KnobBody.ViewObject.ShapeColor = (0.13,0.13,0.13)
Gui.runCommand('Std_ViewIsometric'); Gui.SendMsgToActiveView('ViewFit')
Gui.activeDocument().activeView().saveImage(path, 1200, 900, 'White')
```

Note: a section cut parallel to the view plane renders as the intact silhouette — cut the
half that faces the camera away, or orbit so the section face is visible before saving.
Stage the saved PNGs back with `device_stage_files` and SendUserFile them so the user sees
them in chat.

## Exports

```python
import MeshPart, Part
m = MeshPart.meshFromShape(Shape=doc.KnobBody.Shape,
                           LinearDeflection=0.05, AngularDeflection=0.3, Relative=False)
m.write(out_stl)
Part.export([doc.KnobBody, doc.PatternInlay], out_step)   # multi-solid STEP
```

For the single-file multi-color 3MF, run `scripts/make_3mf.py` in the cloud container on
the staged STLs (trimesh welds vertices; output is a core-spec 3MF with one build object
containing one component per part — Bambu Studio imports it as one object, parts
individually assignable to filaments). The 3MF is a container-built file — commit it back
to the project folder (see Session setup).

Slicer-facing design decisions (orientation, prime tower, materials, clearances) live in
`fdm-design.md` — consult it, not memory.

<a id="skills__3d-modeling__references__printers_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/printers.md`  (57 lines)
------------------------------------------------------------------------------------------

# Printer profiles

One profile per machine the user owns. If the user's printer isn't here: research specs,
strengths, and community-reported quirks (official wiki + reviews + forums), use the
findings, then persist them: append the profile to this file in a writable copy of the
skill folder, zip that folder as `<name>.skill` (zip archive, folder at root), and
SendUserFile it so the user can click Save skill — edits to the installed copy alone do
not survive the session.

## Bambu Lab X2D (Combo w/ AMS 2 Pro) — researched 2026-07

**Specs**: 256×256×260 mm — shrinks to **235.5×256×256 in dual-nozzle jobs** (check wide
parts fit!). Enclosed; active chamber heat to 65 °C (Heat Mode) or Cool Mode for PLA/PETG.
2× hardened 0.4 nozzles (0.2/0.6/0.8 available), 300 °C max, bed 120 °C. Main nozzle:
direct drive, 40 mm³/s, flow-calibrated. **Auxiliary nozzle: Bowden-fed, ≤200 mm/s and
≤1000 mm/s² — no TPU (main only); CF/GF rated "print with caution" (permitted, not the
primary recommendation: higher clog risk; both extruders' gears and the aux nozzle are
hardened steel, HRA ~74 vs carbide ~90, so abrasives wear it gradually, not instantly);
plain PETG allowed after a firmware update with a "quality will be reduced" warning;
wavier finish.** AMS 2 Pro: 4 slots, RFID, dries to 65 °C (not while printing); no soft
TPU through AMS. Ships with textured PEI only. No LiDAR.

**Exploit**: near-zero purge for 2-color/2-material — put the material that dominates
volume and visible surface quality on **main** (TPU always), the small-volume second
color/support material on **auxiliary** — CF/GF is acceptable there too as long as its
volume stays small. Chamber+bed+300 °C = reliable ABS/ASA/PA-CF/PC.
Tested support-interface winners per model material: materials.md §2 (short version:
Support-for-ABS for most nylons/ASA/ABS/PC-ABS, but ASA for PA6-CF; PETG for TPU).
Auto flow/motion/nozzle-offset calibration — trust it, but run offset cal with dry filament.

**Material-by-region (dual-nozzle)**: when the 2-material boundary is a REGION (translucent
base below, opaque body above), assign by cutting the mesh at the boundary plane into parts
and giving each part a nozzle (scripts/make_bambu_3mf.py). Two physical nozzles = near-zero
purge AND no cross-contamination — separate melt paths, unlike single-nozzle switching which
purges and can bleed pigment into a clear material. Rule of thumb: showpiece + any
abrasive/CF material on **main** (direct-drive, hardened), the less finish-critical material
on **aux** (Bowden) — the optically-critical face is usually plate-formed anyway, so the
aux's wavier finish lands where it doesn't cost you. Single-nozzle switching contaminates a
clear material only if it shares a nozzle with an opaque and RETURNS to clear: make any such
transition one-way, and expect a large purge into the clear direction.

**Quirks**: dual-nozzle filament→nozzle assignment in Bambu Studio is buried — use
grouping mode "Custom" and verify the assignment preview before slicing (can't reassign
after; rearrange AMS slots instead). Ooze smearing the calibration pad = wet filament.
AI spaghetti detection hypersensitive (may pause on wisps). Early units: PTFE tube rubbing
lid, right-path buffer spring failures (fixed ~2026-06), AMS hub lever grinding — Bambu
replaces. Textured PEI adhesion weaker than smooth for some materials — brim tall ASA.

**Recipes**: ASA 240–255 °C / bed 90–100 / Heat Mode 60–65 / fan 0 / dry 4–6 h @80.
PA6-CF: main only, 260–270 / bed 95–110 / chamber 65 / dry 8–12 h @80 mandatory.
TPU: main nozzle, external spool, 40–60 mm/s.

Sources: store.bblcdn.com X2D spec PDF, wiki.bambulab.com dual-nozzles-slicing-filament-grouping,
techradar.com X2D review, notebookcheck.net X2D review, forum.bambulab.com X2D threads,
wiki.bambulab.com/en/x2d/manual/filament-compatibility,
wiki.bambulab.com/en/x2d/manual/auxiliary-extruder-intro,
forum.bambulab.com/t/confused-on-using-petg-in-x2d-on-aux-nozzle/250170.

<a id="skills__3d-modeling__references__materials_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/materials.md`  (37 lines)
------------------------------------------------------------------------------------------

# Materials — extended picks, drying, support pairings

Environment table (which polymer survives where) lives in fdm-design.md §7. This file:
underrated filaments worth choosing, moisture handling, and support-interface pairings.

## 1. Picks beyond the basics

| Filament | Why | Numbers / caveats |
|---|---|---|
| PA (nylon) | most rugged FDM material; repeated-impact parts | Dry at **80–100 °C** (50–60 °C dryers insufficient). Bed heat suffices, no chamber needed; Magigoo PA or PA plate for adhesion. Easy variants for open printers: Sunlu Easy PA, Polymaker CoPA. Ventilate. Bonds to almost nothing |
| PA12-CF vs PA6 | PA12 absorbs less water, holds shape better | CF/GF nylons print easier than neat PA |
| TPU-GF/CF | TPU layer adhesion + partial rigidity (between TPU and PA) | Semi-matte; spools often 500–750 g |
| PC-CF | HDT ~130 °C at fraction of PPA-CF price; prints easier than neat PC | Excels at load-bearing printed threads; satin finish |
| Foamed "Air" TPU/PEBA | ~40 % air: light, skin-friendly, EVA-like compression recovery → gaskets/seals/wearables | Standard TPU stays squished — bad gaskets. Foaming needs flow/PA re-tuning |
| PETG-CF | fixes PETG: no nozzle boogers, stiffer, matte, far less moisture-bubbling | ~$20–30/kg. CF weakens PLA but not PETG |

- Any CF/GF filament → hardened steel nozzle; on X2D never through the auxiliary nozzle.
- Wet-filament tells: popping/bubbling while extruding; ooze smearing calibration pads;
  stringing that temperature tuning doesn't fix. PETG, TPU, PA worst offenders.

## 2. Support-interface pairings (tested on X2D dual-nozzle)

Model → best interface material (aux nozzle prints ONLY the thin interface layers):

| Model | Winner | Loser / trade-off |
|---|---|---|
| PA (Easy PA, PA12-CF, PA6-GF) | Support-for-ABS | ASA grooves or welds |
| **PA6-CF** | **ASA** | Support-for-ABS welds solid — filled nylons differ; always coupon-test |
| ASA / ABS-GF / PC-ABS | Support-for-ABS | same-material support sags/lines |
| PC | ASA (releases, small grooves) | Support-for-ABS: perfect surface but needs a chisel |
| TPU | cheap PETG (or Support-for-PLA) | never zero XY-spacing; 3 interface layers |
| PLA | Support-for-PLA / PVA (dried) | — |

- Dedicated dissimilar interface prints at **zero Z-gap** → no sag lines. Don't manually
  zero spacings the slicer sets for interface materials.
- Dual nozzle = ~zero purge; AMS single-nozzle purges every swap (dark→light ≈ 3×).
- Run a small support coupon before committing any large print with a new pairing.

<a id="skills__3d-modeling__references__mechanisms_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/mechanisms.md`  (54 lines)
------------------------------------------------------------------------------------------

# Print-in-place mechanisms — hinges, springs, flexures, magnets

Catalog of mechanisms that print reliably. Universal rules: forces stay **in the layer
plane**; overhang-free or chamfered joints; chunky beats tuned (a good design prints at
any layer height/infill/material — never rely on slicer settings for function).
Gaps: ≥0.3 mm between PIP surfaces; 0.4–0.6 free-spinning; vertical ≥2 layers.

## 1. Hinges (pick by life + load)

| Type | How | Notes |
|---|---|---|
| Living (flap) | thin flexing web | Print on its side, flex in-plane. PP/TPU for real cycle life; PETG/PA a few gentle cycles; PLA never. Can't bend far. Never bridge it |
| Circular (arc) | arc spreads bending | Less wear + built-in spring-return (self-closing lid); less range; arc protrudes |
| Toothed circular | grooves cut into arc | More flex + life, less protrusion; tune via groove depth & count |
| Spring (distributed) | many small flexures | Long articulated columns; no single point flexes far |
| Slat (kerf) | slats twist in torsion | Woodworking-style; design around target bend radius |
| Axle, vertical print | axle axis vertical | Smooth precise rotation; **chamfer inner axle ends** or droop welds them; weak in torsion → make chunky |
| Axle, horizontal | layers through axis | Strong but bore sags oval → rough rotation; cheap parts |
| Cone | splayed cone in socket | Self-captive, rotates, no side travel; weak in twist → oversize |
| Double-cone | cones top+bottom, ~2 mm engage | Leverage-free, strong; overhang can fuse → hybrid profile (cone-step-cone), alternate cones per link, or print on side |

## 2. Printed springs (all flat, in-plane)
- Extension: coil profile printed flat as slot pattern. **Round every corner** — square
  corners are the crack sites. Member ≥1 mm (thicker = stiffer).
- Spiral/torsion: wind-up and self-closing lids; thicker feed = stronger, more coils +
  height = more energy.
- Leaf / parallel-leaf flexure stage: compress + shear; pair keeps orientation constant.
  Strength ≈ band thickness only.
- Stabilizer ring: extension springs around a perimeter = trampoline mount for buttons
  and vibration isolation.
- Any spring printed at an angle loses most return force. FDM can't do helical coils —
  use flat styles (or steel springs).
- Flat springs can be fully encased mid-print → assembled mechanism with zero assembly.
  Use-case: embedded leaf springs inside a knob bore grip any shaft shape/size.
- Compliant spring latches: design ~2 mm of travel; print-in-place vertical springs make
  sliding latches integral to an enclosure printed on its long edge.
- Flexures: thinnest possible for range; stack several thin instead of one thick for
  stiffness; ALWAYS add hard end-stops against plastic deformation.

## 3. Magnets (7 retention methods, best first)
- Press-fit cylinder (not disc — side-wall friction) into bore, arbor press it.
- Snap-lip pocket: press magnet past a small modeled lip; works for spheres too
  (self-orienting).
- Pause-and-insert mid-print: fully captive, invisible.
- Side slot after print: easy but leaves a wall that weakens pull.
- Latches: magnet + **steel ball/washer** on the other side — cheaper, and two magnets
  chip each other.

## 4. Pins & bosses
- Short and thick; length multiplies leverage stress. Fillet the base (root is where
  they snap). Vertical pins ≥ Ø5 or use steel dowel.
- Gear-tooth micro-cutouts around a pin cross-section = more perimeter per layer =
  stronger, slicer-independent. Slots plunged through pin into parent body anchor it
  like local dense infill.

<a id="skills__3d-modeling__references__troubleshooting_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/troubleshooting.md`  (64 lines)
------------------------------------------------------------------------------------------

# Print troubleshooting — symptom → cause → fix

Rule out mechanical causes before touching slicer settings.

## Calibration order for every new filament
Temperature tower → pressure advance (PA depends on temp) → flow rate → retraction →
shrinkage cube (measure, store compensation) → save custom profile.
Shrinkage: scale per fdm-design §8's per-material table, or measure a test cube.

## First layer & adhesion
- Wash plate with degreasing dish soap — no aloe/moisturizer soaps.
- Z-offset 0.1 mm too high already ruins adhesion; too low → elephant foot, shifts.
  Enable a brim and babystep live at print start.
- Stubborn: Magigoo (material-specific), 3DLAC, Nano Polymer; brim/mouse-ears vs warp.
- Elephant foot: compensation setting + check bed temp against spool range.

## Extrusion
- Clogs: acupuncture needle or cold pull (~100 °C). Recurring clogs = heat creep →
  clean heatsink fan; open the door for PLA/PETG in enclosures.
- Under-extrusion, ranked: too fast > partial clog > slipping extruder gear > temp low.
  Fix flow with slicer's flow test; push temp toward manufacturer max.
- Pressure advance: corners gap = PA too high; corners round/mushy = PA too low.
- Stringing: temp too high, retraction wrong, or wet filament (popping sounds = wet).
  Last resorts: faster travel, avoid crossing perimeters.
- CF/GF wear: nozzle orifice no longer round → replace.

## Surfaces
- Poor top: over-extrusion on top layer → narrower top width, slower, +top layers,
  ironing. Pillowing over infill = cooling → +1–2 top layers cheapest fix.
- Weak layer bond: too fast / too cold / cold room / overcooled — lower fan but keep
  100 % on bridges & overhangs. Rotate part toward directional cooling ducts.
- Support scars: +Z-distance a notch, add interface layers (see materials.md §2).

## Motion artifacts
- Layer shifts: nozzle collisions (over-extrusion, curled edges, low/slow Z-hop),
  loose belts, debris in idlers, dry rails. Power off, move head by hand, feel for it.
- Ghosting/ringing: belt tension (check quarterly) + input shaping.
- Z-banding: bent lead screw, binding nut, temp fluctuation → clean/lube, PID tune.

## Field failure: PETG-CF parts knocked off mid-print (nuc feeder, 2026-07)

**Symptom:** part detached from textured PEI a few mm up, spaghetti; happened twice
identically, at the same layer band. Filament was dried (12 h @65 °C, AMS at 21% RH) —
so NOT moisture. The failure height matched the part's first heavy bridging layers.

**Root causes (compound):**
1. **Flat bridges + CF filament = nozzle strikes.** CF-filled PETG curls at bridge and
   overhang edges; the nozzle clips the curled strands every pass and eventually shears
   the part off. Repeatable failure at the bridge band is the signature.
2. **PETG-CF grips textured PEI worse than plain PETG**, and Bambu Studio's `auto_brim`
   frequently decides on NO brim — a tall part on a small/segmented footprint (spokes,
   arms, narrow rings) then has no adhesion margin at all.
3. **Long flat arms warp**: tips lift, nozzle taps them with big leverage at the ends.

**Fixes that must travel together (design + slice):**
- Design: never leave >8–10 mm flat down-facing bridges in CF materials. Corbel them —
  45° fillets (fuse a 45°-rotated square prism along each supporting edge) shrink the
  span without support material. Keep corbels clipped to where solid wall exists above.
- Slice: force `brim_type: outer_only` (do not trust auto_brim), and halve
  `bridge_speed` (X2D preset ships ["50","50","50","200"] per extruder variant — the
  override must match that array shape).
- Bed prep: wipe plate with IPA; glue stick adds margin for CF on textured PEI.
- When several parts share a plate, one knock-off wrecks all of them — consider
  printing the risky tall part alone first.

<a id="skills__3d-modeling__references__preflight-checklist_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/preflight-checklist.md`  (135 lines)
------------------------------------------------------------------------------------------

# Pre-print validation checklist (FDM functional parts)

Run this as a **gate before exporting final STL and before slicing** any design meant to be
manufactured — especially multi-part functional assemblies, threaded/sealed parts, and stiff
carbon-filled filaments (PETG-CF, PA-CF) on the Bambu X2D. It exists because a design can pass
watertight/interference checks in CAD and still fail on the plate: e.g. the nuc-feeder drip
barrel was knocked off the bed twice at its bridge layers even with dried filament (see
[troubleshooting.md](troubleshooting.md) → "PETG-CF parts knocked off").

Sources: the **3D Design NotebookLM** corpus (DFAM lectures, print-troubleshooting + filament-
calibration videos, DfAM papers), cross-checked against Bambu Lab's PETG-CF TDS/wiki and
community reports. Numbers are starting points — a calibrated printer + material beats any table.

How to read it: each item is **PASS / FIX / N/A**. Any FIX with no mitigation = do not print yet.

---

## A. Geometry / DFAM (fix in CAD, before STL)

### A1. Bed adhesion & knock-off (the #1 mid-print killer)
- [ ] **Footprint vs height sanity.** Tall part on a small or *segmented* footprint (spokes,
  arms, rings, a cylinder on legs) is the classic knock-off. If height ÷ min-footprint-width is
  large, add a brim (slicer) AND/OR widen the base contact.
- [ ] **First-layer chamfer.** 0.5–1 mm chamfer on every bottom edge — kills side-extrusion
  "elephant lip" and gives a clean transition. (Also enable slicer elephant-foot compensation.)
- [ ] **Round vertical corners** on the first layer so the nozzle never makes a sharp 90° turn
  it can drag the part up by. Sharp bottom corners are where peel starts.
- [ ] **No text / logos / tiny cosmetic holes on the first layer** — small tool moves warp and
  drag; move them up a few layers or emboss instead of engrave on layer 1.
- [ ] **Tall thin risky feature?** Design a **sacrificial support fin** (0.5–1 mm wall, parallel,
  0.5–1 mm gap, joined by horizontal 0.5–1 mm breakaway prongs) rather than trusting auto-supports.
- [ ] **Custom brim / mouse-ears** (if used) modeled at exactly one layer (0.2 mm) thick.

### A2. Warping of thin/flat features
- [ ] **Large flat base** → checkerboard the underside: ~1 mm-deep cuts, ~25 mm (1") apart, to
  break the continuous shrink lines. (Do not breach the outer wall.)
- [ ] **Long flat sidewalls** → add ~1 mm wrinkle/ripple/slight curve so shrinkage straightens
  the ripple instead of lifting the corners.
- [ ] **Interrupt internal tension** → small circular cavities / narrow slits inside the model
  break long diagonal infill runs that pull corners off the bed.

### A3. Overhangs & bridges (tightened for carbon-filled/stiff filaments)
- [ ] **Overhang angle:** self-supporting surfaces should rise ≥ 45° from horizontal (≤ 45° from
  vertical). **30° from horizontal is the absolute floor** before you need support/redesign.
- [ ] **Bridge span:** general max reliable unsupported bridge ≈ 25–50 mm (1–2"); add an internal
  rib every 25–50 mm to break longer spans. **For PETG-CF/PA-CF, be far more conservative** —
  fibers make edges *curl up* proud of the layer, the nozzle then clips them and shears the part
  off. Keep flat bridges short (target < 8–10 mm) or eliminate them with corbels.
- [ ] **90° overhang → 45–60° CHAMFER, never a fillet.** A fillet is tangent to horizontal at
  the top → an infinite 0° overhang that droops. Chamfers give a self-supporting stair-step.
  (Corbel technique: fuse a 45°-rotated square prism along each supporting edge to shrink a flat
  bridge span without support material; clip it to where solid wall exists above.)

### A4. Mating parts, threads & seals
- [ ] **Moving/snug fit:** start at **0.2 mm** gap between parts. Pin-in-hole: hole **0.25–0.5 mm**
  larger than the pin.
- [ ] **Horizontal (side-printed) holes** shrink more from overhang sag → give them extra clearance,
  or print undersize and ream.
- [ ] **Airtight/precise hole:** model **0.5 mm undersize** and ream/tap to final size post-print.
- [ ] **Printed threads:** none below ~1/8" (≈3 mm) major diameter — nozzles can't resolve them.
  Model thread crests/roots as **45° triangular cuts** (no horizontal overhang). A **horizontally**
  printed threaded hole should have its top+bottom thread arcs deleted in CAD, leaving only the
  clean vertical sidewalls to grip.
- [ ] **Pressure/gasket faces:** force solid material by embedding thin (0.1–2 mm) slots/cuts in
  CAD so the slicer lays dense perimeters exactly there, rather than hoping infill fills it.

---

## B. Material & calibration preflight (do once per filament/printer)

- [ ] **Filament dried.** PETG/PETG-CF are hygroscopic. Bambu PETG-CF: **65 °C / 8 h** (dryer) or
  heatbed **75–85 °C / 12 h**. Note: drying alone does **not** cure adhesion/bridge failures.
- [ ] **Hardened steel nozzle** installed for any carbon/glass-filled filament (abrasive).
- [ ] **Calibrated, in this order** (each has a "correct value" tell):
  1. **Temperature tower** → pick the *highest* temp that still bridges/overhangs cleanly with
     minimal stringing (higher = better layer adhesion + higher max flow). Bambu PETG-CF nozzle
     range **240–270 °C**.
  2. **Max volumetric speed** → find Z of first defect/sheen change, read flow at that height,
     subtract 10–20%. This hard-caps your real print speed.
  3. **Pressure / linear advance** → run the PA pattern **at your actual outer-wall speed/accel**;
     correct = sharpest corner with no gaps.
  4. **Flow ratio / extrusion multiplier** → correct = top surface with no gaps between lines.
     (For airtight parts, bias slightly high — e.g. ×1.02 — for wall fusion.)
  5. **Retraction** (optional) → lowest value with no stringing; too high pokes holes in walls.

---

## C. Final 3MF settings to verify before you hit slice

Confirm these are actually in the project, not just "probably inherited." Right column = the
values baked into the nuc-feeder PETG-CF X2D project as a worked example.

| Setting | Target for a sealed PETG-CF part | Nuc-feeder 3MF |
|---|---|---|
| Filament / nozzle map | correct material on the intended nozzle | PETG-CF, MAIN (direct-drive) |
| Walls / perimeters | **≥ 4** for any pressure/airtight wall (perimeters > infill for strength) | 4 |
| Top / bottom layers | +1–2 extra tops to avoid pillowing | 5 / 3 |
| Infill | 15–30% functional; gyroid for isotropic sealing | 30% gyroid |
| **Brim** | **outer, ≥ 5 mm — set explicitly; do NOT trust `auto_brim`** (it gave our part none) | outer_only, 5 mm |
| **Bridge speed** | **halved** vs default for CF (curl control) | 25 mm/s |
| Flow ratio | calibrated; ~×1.02 bias for airtight walls | 0.969 (×1.02) |
| Nozzle temp | in material range (PETG-CF 240–270) | 255 °C |
| Plate temp / type | PETG-CF 60–80 °C; the plate you actually own | 70 °C, Textured PEI |
| Part-cooling fan | **PETG-CF 0–40% general**; full fan only on overhangs/bridges | 40% max / 100% overhang |
| Elephant-foot comp | ~0.15 mm (with the CAD chamfer, not instead of it) | 0.15 mm |
| Seam position | hide inside/rear away from threads & sealing faces | aligned* |
| Max volumetric speed | your calibrated cap | 11.5 mm³/s |

\* For threaded sockets, prefer a rear/hidden seam so a seam blob doesn't tighten the thread fit.

**Slicer sanity preview:** confirm **0 support material** (unless intended), brim actually renders
around **every** part, and the bridge/overhang regions are the only blue "overhang" faces.

---

## D. Bed prep & first-layer watch (at the machine)

- [ ] **Degrease the plate** with dish soap (no aloe/moisturizer) or IPA; don't touch it after.
- [ ] **PETG-CF ↔ textured PEI is a known weak combo on big/tall parts** — corners lift / parts
  come loose in a narrow Z-window. A thin **glue-stick** layer both evens adhesion *and* acts as a
  release layer (PETG can also bond *too* hard to smooth PEI and tear it). Prefer glue stick here.
- [ ] **Z-offset dialed:** too high → separation; too low → elephant foot / nozzle collision →
  layer shift → knock-off. Enable **Z-hop** so travel moves clear curled edges.
- [ ] **Watch layer 1** and the first bridge layers live. Abort early if a corner lifts or a bridge
  strand stands proud — that is the exact moment a knock-off begins.
- [ ] **Multi-part plate risk:** one knocked-off part spaghettis the rest. Print the tallest/
  riskiest part **alone first**; add the others once it's proven.
- [ ] **Release:** let the plate fully cool (or chill it) before removing — don't pry hot.

---

### One-line gate
Chamfered base + rounded first-layer corners + no long flat CF bridges (corbel/chamfer them) +
explicit outer brim + slowed bridges + degreased plate/glue stick + calibrated flow/temp +
≥4 walls on sealed faces + risky part printed first. If any of those is missing, fix before slicing.

<a id="skills__3d-modeling__references__bambu-3mf-authoring_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/references/bambu-3mf-authoring.md`  (61 lines)
------------------------------------------------------------------------------------------

# Authoring a print-ready Bambu Studio project 3MF

A plain core-spec 3MF ([scripts/make_3mf.py](../scripts/make_3mf.py)) carries geometry only —
Bambu Studio imports it as one object, every part on filament 1, process = whatever was last
used. A print-ready Bambu *project* 3MF carries the **settings** too, so import is
"eyeball → slice". Two files do the work:

- `Metadata/project_settings.config` — JSON: layer height, infill, brim, bed type, and the
  per-filament / per-extruder-variant **arrays** (nozzle temps, flush volumes, retraction…).
- `Metadata/model_settings.config` — XML: per-object and per-part assignment via
  `<metadata key="extruder" value="N"/>`, where **N is a 1-based filament slot** (not a
  physical nozzle — the slot→nozzle mapping is `filament_map` in project_settings).

## Never guess keys — round-trip the real slicer

Machine/process/filament key NAMES and VALUES differ per machine and change between Studio
builds; a new machine's keys aren't documented. Get them from the slicer itself:

1. In Bambu Studio, configure ONE plate correctly for the exact machine (printer preset,
   process, filaments, per-object filament, bed type).
2. **File → Save Project As**, unzip the result, read `project_settings.config` and
   `model_settings.config`. Those are ground truth for names, shapes, and values.
3. **Save twice** — once before your changes, once after — and **diff** the two
   `project_settings.config` files. The diff is exactly the keys your settings touched;
   everything else you should leave inheriting.

Keep the saved project as the reference fixture and diff your generated file against it
(same members, same array lengths, same values except your deliberate overrides).

## Three traps (all cost a wasted print if missed)

1. **G-code hides in sidecar template profiles.** Machine start/end/layer-change/
   change-filament/timelapse G-code may not be in the machine profile — it can live in
   sibling `<machine> template <key>.json` profiles with `instantiation:false`. A naive
   `inherits` walk silently falls back to generic (X1/P1) G-code: wrong toolhead-offset
   calibration, wrong dual-nozzle filament change. **Verify the emitted G-code actually
   names the target machine** (e.g. grep the five blocks for the machine name).
2. **Generic-ancestor values carry the wrong unit form.** e.g. `fdm_process_dual_common`
   ships `monotonic_travel_into_wall` as `"45.0"`, which Studio parses as 45 **mm**, not
   45 **%**. Pin such keys to the value a real save contains, not the ancestor profile's.
3. **Bambu Studio may DISCARD your part names on import** — parts have come in renamed to
   "assembly" / "assembly_2". So key per-part filament assignment on the explicit
   `extruder` metadata you write into `model_settings.config`, **never** on part names
   surviving import.

## Honesty rule — you cannot confirm acceptance without launching the slicer

Structural verification proves the file is internally consistent, NOT that Studio likes it.
So: re-open the zip, parse every config, confirm each part's `extruder` slot and the
filament/nozzle map, check array shapes (n_filaments × block), confirm G-code names the
machine. State confidence **per setting**, and ship a short **"verify these after import"**
checklist (filament assignment preview, bed type, infill density, brim) rather than
claiming the print will succeed.

## Reusable tool

[scripts/make_bambu_3mf.py](../scripts/make_bambu_3mf.py) emits the whole project 3MF with
settings baked in and per-part filament assignment from part names, then self-verifies. It
is currently **X2D-specific** (built from that machine's installed profiles); to target
another machine, re-run the round-trip above to get that machine's profile ids and key
values, then update the presets/rules at the top of the script.


==========================================================================================
# SCRIPTS (executable preflight gate + shared tooling)
==========================================================================================


<a id="skills__3d-modeling__scripts__team_preflight_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/team_preflight.py`  (311 lines)
------------------------------------------------------------------------------------------

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import trimesh

SCHEMA_VERSION = 4
TOOL_VERSION = "1.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_single_mesh(path: Path) -> trimesh.Trimesh:
    loaded = trimesh.load(path, force="mesh", process=True)
    if not isinstance(loaded, trimesh.Trimesh):
        raise ValueError(f"{path}: did not load as one mesh")
    return loaded


def indexed_rows(
    rows: Any,
    *,
    label: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{label}: expected a list")
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError(f"{label}: every row needs a string id")
        row_id = row["id"]
        if row_id in indexed:
            raise ValueError(f"{label}: duplicate id {row_id}")
        indexed[row_id] = row
    return indexed


def support_audit(
    *,
    stl_path: Path,
    plan_path: Path,
    rule_id: str,
) -> tuple[dict[str, Any], float]:
    plan = load_json(plan_path)
    rules = indexed_rows(plan.get("support_rules"), label="support_rules")
    if rule_id not in rules:
        raise ValueError(f"support_rules: missing id {rule_id}")
    rule = rules[rule_id]

    matrix = np.asarray(rule.get("model_to_printer_matrix"), dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError(f"{rule_id}: model_to_printer_matrix must be 4x4")
    bed_z = float(rule.get("bed_z_mm"))
    bed_tolerance = float(rule.get("bed_tolerance_mm"))
    downward_normal_z_max = float(rule.get("downward_normal_z_max"))
    maximum_area = float(rule.get("max_out_of_limit_area_mm2"))

    mesh = load_single_mesh(stl_path)
    vertices = trimesh.transform_points(mesh.vertices, matrix)
    triangles = vertices[mesh.faces]
    edges_a = triangles[:, 1] - triangles[:, 0]
    edges_b = triangles[:, 2] - triangles[:, 0]
    crosses = np.cross(edges_a, edges_b)
    double_areas = np.linalg.norm(crosses, axis=1)
    valid = double_areas > 1e-12
    normals = np.zeros_like(crosses)
    normals[valid] = crosses[valid] / double_areas[valid, None]
    areas = double_areas * 0.5

    bed_contact = (
        np.max(np.abs(triangles[:, :, 2] - bed_z), axis=1) <= bed_tolerance
    )
    downward = normals[:, 2] <= downward_normal_z_max
    out_of_limit = valid & downward & ~bed_contact
    out_of_limit_area = float(areas[out_of_limit].sum())

    result = {
        "schema_version": SCHEMA_VERSION,
        "tool": "team_preflight.py",
        "tool_version": TOOL_VERSION,
        "kind": "support-audit",
        "stl_path": stl_path.name,
        "stl_sha256": sha256_file(stl_path),
        "plan_checks_sha256": sha256_file(plan_path),
        "rule_id": rule_id,
        "matrix_sha256": canonical_sha256(rule["model_to_printer_matrix"]),
        "disposition": rule.get("disposition"),
        "bed_z_mm": bed_z,
        "bed_tolerance_mm": bed_tolerance,
        "downward_normal_z_max": downward_normal_z_max,
        "bed_contact_area_mm2": float(areas[valid & bed_contact].sum()),
        "out_of_limit_faces": int(np.count_nonzero(out_of_limit)),
        "out_of_limit_area_mm2": out_of_limit_area,
        "max_out_of_limit_area_mm2": maximum_area,
        "result": "PASS" if out_of_limit_area <= maximum_area + 1e-9 else "FAIL",
    }
    return result, maximum_area


def validate_receipts(
    *,
    stl_path: Path,
    plan_path: Path,
    readiness_path: Path,
) -> dict[str, Any]:
    plan = load_json(plan_path)
    readiness = load_json(readiness_path)
    errors: list[str] = []

    if plan.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"plan schema_version must be {SCHEMA_VERSION}")
    if readiness.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"readiness schema_version must be {SCHEMA_VERSION}")

    stl_sha = sha256_file(stl_path)
    plan_sha = sha256_file(plan_path)
    if readiness.get("candidate_stl_sha256") != stl_sha:
        errors.append("candidate_stl_sha256 does not match the exported STL")
    if readiness.get("print_plan_checks_sha256") != plan_sha:
        errors.append("print_plan_checks_sha256 does not match the plan checks file")

    plan_edges = indexed_rows(plan.get("edges"), label="plan edges")
    ready_edges = indexed_rows(readiness.get("edges"), label="readiness edges")
    if set(plan_edges) != set(ready_edges):
        errors.append(
            "edge ID set mismatch: "
            f"missing={sorted(set(plan_edges) - set(ready_edges))}, "
            f"extra={sorted(set(ready_edges) - set(plan_edges))}"
        )
    for edge_id in sorted(set(plan_edges) & set(ready_edges)):
        expected = plan_edges[edge_id]
        observed = ready_edges[edge_id]
        samples = observed.get("samples_mm")
        if not isinstance(samples, list) or not all(
            isinstance(value, (int, float)) for value in samples
        ):
            errors.append(f"{edge_id}: samples_mm must be a numeric list")
            continue
        required_samples = int(expected.get("samples_required", 3))
        if len(samples) < required_samples:
            errors.append(
                f"{edge_id}: needs {required_samples} samples, found {len(samples)}"
            )
            continue
        if expected.get("allowed_sharp") is True:
            if not expected.get("allowed_sharp_reason"):
                errors.append(f"{edge_id}: allowed sharp edge needs a plan reason")
            continue
        minimum = float(expected.get("min_radius_mm"))
        maximum_value = expected.get("max_radius_mm")
        observed_min = min(float(value) for value in samples)
        observed_max = max(float(value) for value in samples)
        if observed_min + 1e-9 < minimum:
            errors.append(
                f"{edge_id}: radius {observed_min:.6f} below {minimum:.6f} mm"
            )
        if maximum_value is not None and observed_max - 1e-9 > float(maximum_value):
            errors.append(
                f"{edge_id}: radius {observed_max:.6f} above "
                f"{float(maximum_value):.6f} mm"
            )
        if not observed.get("method") or not observed.get("evidence"):
            errors.append(f"{edge_id}: method and evidence are required")

    plan_support = indexed_rows(plan.get("support_rules"), label="plan support_rules")
    ready_support = indexed_rows(
        readiness.get("support_rules"), label="readiness support_rules"
    )
    if set(plan_support) != set(ready_support):
        errors.append(
            "support-rule ID set mismatch: "
            f"missing={sorted(set(plan_support) - set(ready_support))}, "
            f"extra={sorted(set(ready_support) - set(plan_support))}"
        )
    for rule_id in sorted(set(plan_support) & set(ready_support)):
        expected = plan_support[rule_id]
        observed = ready_support[rule_id]
        audit_value = observed.get("audit_path")
        if not isinstance(audit_value, str):
            errors.append(f"{rule_id}: audit_path is required")
            continue
        audit_path = (readiness_path.parent / audit_value).resolve()
        if not audit_path.is_file():
            errors.append(f"{rule_id}: missing audit file {audit_value}")
            continue
        audit = load_json(audit_path)
        if audit.get("tool") != "team_preflight.py":
            errors.append(f"{rule_id}: audit must come from team_preflight.py")
        if audit.get("stl_sha256") != stl_sha:
            errors.append(f"{rule_id}: audit STL hash mismatch")
        if audit.get("plan_checks_sha256") != plan_sha:
            errors.append(f"{rule_id}: audit plan hash mismatch")
        if audit.get("rule_id") != rule_id:
            errors.append(f"{rule_id}: audit rule ID mismatch")
        if audit.get("matrix_sha256") != canonical_sha256(
            expected.get("model_to_printer_matrix")
        ):
            errors.append(f"{rule_id}: transform hash mismatch")
        observed_area = float(audit.get("out_of_limit_area_mm2", float("inf")))
        maximum_area = float(expected.get("max_out_of_limit_area_mm2"))
        if expected.get("disposition") == "SELF_SUPPORT_REQUIRED":
            if observed_area > maximum_area + 1e-9:
                errors.append(
                    f"{rule_id}: {observed_area:.6f} mm2 exceeds "
                    f"{maximum_area:.6f} mm2"
                )
        elif expected.get("disposition") == "SUPPORT_ALLOWED":
            if not expected.get("allowed_contact_class"):
                errors.append(f"{rule_id}: SUPPORT_ALLOWED needs allowed_contact_class")
            if observed.get("forbidden_faces_checked") is not True:
                errors.append(f"{rule_id}: forbidden faces were not checked")
        else:
            errors.append(f"{rule_id}: unknown disposition")

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": "team_preflight.py",
        "tool_version": TOOL_VERSION,
        "kind": "receipt-validation",
        "candidate_stl_sha256": stl_sha,
        "print_plan_checks_sha256": plan_sha,
        "edge_ids": sorted(plan_edges),
        "support_rule_ids": sorted(plan_support),
        "errors": errors,
        "result": "PASS" if not errors else "FAIL",
    }


def write_result(result: dict[str, Any], output: Path | None) -> None:
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is None:
        sys.stdout.write(payload)
    else:
        output.write_text(payload, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic team-pipeline non-acceptance gates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    support = subparsers.add_parser(
        "support-audit",
        help="Measure transformed non-bed downward area on a re-imported STL.",
    )
    support.add_argument("--stl", required=True, type=Path)
    support.add_argument("--plan", required=True, type=Path)
    support.add_argument("--rule-id", required=True)
    support.add_argument("--output", type=Path)

    validate = subparsers.add_parser(
        "validate-receipts",
        help="Validate hashes and complete edge/support ID coverage.",
    )
    validate.add_argument("--stl", required=True, type=Path)
    validate.add_argument("--plan", required=True, type=Path)
    validate.add_argument("--readiness", required=True, type=Path)
    validate.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "support-audit":
            result, _ = support_audit(
                stl_path=args.stl.resolve(),
                plan_path=args.plan.resolve(),
                rule_id=args.rule_id,
            )
        else:
            result = validate_receipts(
                stl_path=args.stl.resolve(),
                plan_path=args.plan.resolve(),
                readiness_path=args.readiness.resolve(),
            )
        write_result(result, args.output.resolve() if args.output else None)
        return 0 if result["result"] == "PASS" else 1
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        sys.stderr.write(f"team_preflight: {error}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

<a id="skills__3d-modeling__scripts__test_team_preflight_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/test_team_preflight.py`  (210 lines)
------------------------------------------------------------------------------------------

```python
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import trimesh

import team_preflight


class TeamPreflightTest(unittest.TestCase):
    def write_plan(self, directory: Path) -> Path:
        plan = {
            "schema_version": 4,
            "candidate_predicate_revision": 1,
            "edges": [
                {
                    "id": "E-01",
                    "min_radius_mm": 0.4,
                    "max_radius_mm": 0.8,
                    "samples_required": 3,
                },
                {
                    "id": "E-02",
                    "allowed_sharp": True,
                    "allowed_sharp_reason": "hidden datum edge",
                    "samples_required": 3,
                },
            ],
            "support_rules": [
                {
                    "id": "S-01",
                    "disposition": "SELF_SUPPORT_REQUIRED",
                    "model_to_printer_matrix": [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1],
                    ],
                    "bed_z_mm": 0,
                    "bed_tolerance_mm": 0.001,
                    "downward_normal_z_max": -0.7,
                    "max_out_of_limit_area_mm2": 0.0,
                }
            ],
        }
        path = directory / "print_plan_checks.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return path

    def test_box_on_bed_has_zero_out_of_limit_area(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)

            result, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            self.assertEqual(result["result"], "PASS")
            self.assertAlmostEqual(result["out_of_limit_area_mm2"], 0.0, places=6)

    def test_elevated_plate_fails_support_audit(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "overhang.stl"
            base = trimesh.creation.box(extents=(1, 1, 2))
            plate = trimesh.creation.box(extents=(4, 4, 0.2))
            plate.apply_translation((0, 0, 2))
            trimesh.util.concatenate((base, plate)).export(stl_path)
            plan_path = self.write_plan(directory)

            result, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            self.assertEqual(result["result"], "FAIL")
            self.assertGreater(result["out_of_limit_area_mm2"], 10.0)

    def test_receipt_validator_rejects_missing_edge(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            audit, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            audit_path = directory / "support_audit.json"
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            readiness = {
                "schema_version": 4,
                "candidate_stl_sha256": team_preflight.sha256_file(stl_path),
                "print_plan_checks_sha256": team_preflight.sha256_file(plan_path),
                "edges": [
                    {
                        "id": "E-01",
                        "samples_mm": [0.5, 0.5, 0.5],
                        "method": "section fit",
                        "evidence": "edge.png",
                    }
                ],
                "support_rules": [
                    {
                        "id": "S-01",
                        "audit_path": audit_path.name,
                        "forbidden_faces_checked": True,
                    }
                ],
            }
            readiness_path = directory / "candidate_preflight.json"
            readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

            result = team_preflight.validate_receipts(
                stl_path=stl_path,
                plan_path=plan_path,
                readiness_path=readiness_path,
            )
            self.assertEqual(result["result"], "FAIL")
            self.assertTrue(
                any("edge ID set mismatch" in error for error in result["errors"])
            )

    def test_receipt_validator_accepts_complete_rows(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            audit, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            audit_path = directory / "support_audit.json"
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            readiness = {
                "schema_version": 4,
                "candidate_stl_sha256": team_preflight.sha256_file(stl_path),
                "print_plan_checks_sha256": team_preflight.sha256_file(plan_path),
                "edges": [
                    {
                        "id": "E-01",
                        "samples_mm": [0.5, 0.6, 0.7],
                        "method": "section fit",
                        "evidence": "edge.png",
                    },
                    {
                        "id": "E-02",
                        "samples_mm": [0.0, 0.0, 0.0],
                        "method": "declared sharp",
                        "evidence": "hidden edge",
                    },
                ],
                "support_rules": [
                    {
                        "id": "S-01",
                        "audit_path": audit_path.name,
                        "forbidden_faces_checked": True,
                    }
                ],
            }
            readiness_path = directory / "candidate_preflight.json"
            readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

            result = team_preflight.validate_receipts(
                stl_path=stl_path,
                plan_path=plan_path,
                readiness_path=readiness_path,
            )
            self.assertEqual(result["result"], "PASS", result["errors"])

    def test_support_audit_cli(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(team_preflight.__file__)),
                    "support-audit",
                    "--stl",
                    str(stl_path),
                    "--plan",
                    str(plan_path),
                    "--rule-id",
                    "S-01",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
```

<a id="skills__3d-modeling__scripts__run_cadquery_model_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/run_cadquery_model.py`  (236 lines)
------------------------------------------------------------------------------------------

```python
#!/usr/bin/env python3
"""
Run a generated CadQuery model script in a subprocess and emit a structured
JSON result so Claude can parse success/failure without the user copy-pasting
tracebacks.

Usage:
    python3 run_cadquery_model.py path/to/model.py
    python3 run_cadquery_model.py path/to/model.py --preview            # also render
    python3 run_cadquery_model.py path/to/model.py --preview --strict   # fail on non-watertight

3MF and STEP files produced by the script (via cq.exporters.export(result,
"name.3mf") / cq.exporters.export(result, "name.step")) are discovered
automatically and reported alongside the STLs.

Emits a single JSON object to stdout (key order matches the emitted JSON):
    {
      "success": true/false,
      "script": "model.py",
      "stls": ["a.stl", "b.stl"],          # every .stl written during this run
      "stl": "a.stl",                       # newest, for single-file convenience
      "previews": ["a_preview.png", ...],   # one per STL when --preview is set
      "preview": "a_preview.png",           # newest, for single-file convenience
      "threemfs": ["a.3mf", "b.3mf"],       # every .3mf produced by the script
      "threemf": "a.3mf",                   # newest, for single-file convenience
      "steps": ["a.step", "b.step"],        # every .step produced by the script
      "step": "a.step",                     # newest, for single-file convenience
      "watertight": true/false/null,        # true only if ALL meshes are watertight
      "stdout": "...",
      "stderr": "...",
      "returncode": 0,                      # -1 on timeout / spawn failure
    }

Exit codes:
    0  success
    1  CadQuery script failed, preview failed, or --strict rejected output
    2  interpreter / script path could not be launched
    3  subprocess timed out
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time


def _sibling(path, suffix):
    return os.path.splitext(path)[0] + suffix


def _append_stderr(result, msg):
    result["stderr"] = (result["stderr"] or "") + msg + "\n"


def _new_files_by_ext(script_dir, after_mtime, exts):
    """Return {ext: [paths]} in script_dir matching each *.{ext}
    (case-insensitive) strictly newer than after_mtime, newest first.
    Dedupes case-variant hits that macOS's case-insensitive filesystem
    returns from both glob patterns.

    The threshold is strict (>=) rather than with a slack window because
    a backward slack would pull in stale files from a previous run started
    less than a second ago, silently reporting them as this run's output.
    Modern filesystems (APFS, ext4, NTFS) have sub-second mtimes, so a
    file written at exactly `after_mtime` is a valid hit.
    """
    buckets = {ext: {} for ext in exts}
    for ext in exts:
        for case in (ext.lower(), ext.upper()):
            for path in glob.glob(os.path.join(script_dir, f"*.{case}")):
                real = os.path.realpath(path)
                if real in buckets[ext]:
                    continue
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    continue
                if mtime >= after_mtime:
                    buckets[ext][real] = (mtime, path)
    return {
        ext: [p for _, p in sorted(entries.values(), reverse=True)]
        for ext, entries in buckets.items()
    }


def _process_stls(stls, views, strict, want_preview):
    """Load each STL once and optionally render a preview + check watertightness.

    Single pass so an STL is never loaded twice when both outputs are
    requested, and so --strict's watertight check runs on every mesh.

    `mesh_io` is imported lazily because the wrapper's common case (bare
    run, no --preview, no --strict) doesn't touch meshes at all. `preview`
    is imported only inside the rendering branch so that --strict by itself
    stays headless-safe (no pyrender / PyOpenGL required).

    Returns a dict with previews, watertights (lists), and error (str or None).
    The caller surfaces the error into result["stderr"].
    """
    import mesh_io  # trimesh + numpy only

    out = {"previews": [], "watertights": [], "error": None}

    for stl in stls:
        try:
            tm = mesh_io.load_mesh(stl)
        except ValueError as e:
            out["error"] = f"Mesh load failed ({stl}): {e}"
            return out

        watertight = bool(tm.is_watertight)
        out["watertights"].append(watertight)

        if strict and not watertight:
            out["error"] = f"Mesh {stl} is not watertight (--strict set)."
            return out

        if want_preview:
            import preview  # heavy: trimesh + pyrender, only here
            preview_path = _sibling(stl, "_preview.png")
            try:
                if views == "multi":
                    preview.render_multi_view(tm, preview_path)
                else:
                    preview.render_single(tm, preview_path)
            except Exception as e:
                out["error"] = f"Preview render failed ({stl}): {e}"
                return out
            out["previews"].append(preview_path)

    return out


def main():
    parser = argparse.ArgumentParser(
        description="Run a CadQuery model script and report a JSON result",
        epilog="Exit codes: 0 success, 1 script/preview/--strict failure, "
               "2 interpreter not launchable, 3 timeout.",
    )
    parser.add_argument("script", help="Path to the CadQuery .py file")
    parser.add_argument("--preview", action="store_true",
                        help="Render a multi-view preview PNG for every STL the script wrote")
    parser.add_argument("--strict", action="store_true",
                        help="Fail with exit code 1 if any STL is not watertight, "
                             "or if the script produced no STL at all")
    parser.add_argument("--views", choices=["iso", "multi"], default="multi",
                        help="Preview layout: 'iso' (single isometric) or 'multi' (6-view) (default: multi)")
    parser.add_argument("--timeout", type=int, default=180,
                        help="Seconds before killing the model script (default: 180)")
    args = parser.parse_args()

    script_path = os.path.abspath(args.script)
    script_dir = os.path.dirname(script_path) or "."

    result = {
        "success": False,
        "script": args.script,
        "stls": [],
        "stl": None,
        "previews": [],
        "preview": None,
        "threemfs": [],
        "threemf": None,
        "steps": [],
        "step": None,
        "watertight": None,
        "stdout": "",
        "stderr": "",
        "returncode": -1,
    }

    started = time.time()

    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=args.timeout,
            cwd=script_dir,
        )
    except subprocess.TimeoutExpired as e:
        _append_stderr(result, f"Timeout after {args.timeout}s: {e}")
        print(json.dumps(result, indent=2))
        sys.exit(3)
    except FileNotFoundError as e:
        _append_stderr(result, f"Cannot launch interpreter: {e}")
        print(json.dumps(result, indent=2))
        sys.exit(2)

    result["stdout"] = proc.stdout
    result["stderr"] = proc.stderr
    result["returncode"] = proc.returncode
    result["success"] = proc.returncode == 0

    if result["success"]:
        found = _new_files_by_ext(script_dir, started, ("stl", "3mf", "step", "stp"))
        result["stls"] = found["stl"]
        result["threemfs"] = found["3mf"]
        # CadQuery writes .step by convention; .stp is accepted too. Both
        # are merged into one list (newest-first within each extension).
        result["steps"] = found["step"] + found["stp"]

    # --strict implies the run must produce at least one STL. A script that
    # exits 0 but forgot to call cq.exporters.export() would otherwise slip
    # through with an empty stls list and a null watertight claim.
    if args.strict and result["success"] and not result["stls"]:
        _append_stderr(result, "No STL files produced by the script (--strict set).")
        result["success"] = False

    needs_mesh_pass = args.preview or args.strict
    if needs_mesh_pass and result["success"] and result["stls"]:
        processed = _process_stls(
            result["stls"], args.views, args.strict,
            want_preview=args.preview,
        )
        result["previews"] = processed["previews"]
        if processed["watertights"]:
            result["watertight"] = all(processed["watertights"])
        if processed["error"]:
            _append_stderr(result, processed["error"])
            result["success"] = False

    result["stl"] = result["stls"][0] if result["stls"] else None
    result["preview"] = result["previews"][0] if result["previews"] else None
    result["threemf"] = result["threemfs"][0] if result["threemfs"] else None
    result["step"] = result["steps"][0] if result["steps"] else None

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
```

<a id="skills__3d-modeling__scripts__mesh_io_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/mesh_io.py`  (35 lines)
------------------------------------------------------------------------------------------

```python
"""Pure trimesh STL loading with validation guards.

Kept separate from preview.py so consumers that only need mesh loading
(run_cadquery_model.py's --strict watertight check) don't
pay the pyrender + PyOpenGL import cost. Only depends on trimesh + numpy.
"""
import numpy as np
import trimesh


def load_mesh(path):
    """Load an STL file via trimesh.

    Raises ValueError if the file cannot be parsed, contains no geometry,
    has zero faces, or has non-finite vertex coordinates. Callers handle
    the failure in-process instead of being killed by sys.exit, and silent
    garbage (zero-face or NaN meshes) is stopped before it reaches pyrender.
    """
    try:
        tm = trimesh.load(path, force="mesh")
    except Exception as e:
        raise ValueError(f"Failed to load STL: {e}") from e
    if not hasattr(tm, "vertices") or len(tm.vertices) == 0:
        raise ValueError("STL file contains no vertices")
    if not hasattr(tm, "faces") or len(tm.faces) == 0:
        raise ValueError("STL file contains no triangles")
    if not np.isfinite(tm.vertices).all():
        raise ValueError("STL file has non-finite vertex coordinates (NaN or inf)")
    # OCC's tessellator emits zero-area triangles at the poles of
    # spherical faces (and similar degenerate spots). They carry no
    # surface, but their zero-length open edges make an otherwise
    # closed mesh read as non-watertight. Drop them before any checks.
    tm.update_faces(tm.nondegenerate_faces())
    tm.merge_vertices()
    return tm
```

<a id="skills__3d-modeling__scripts__preview_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/preview.py`  (488 lines)
------------------------------------------------------------------------------------------

```python
#!/usr/bin/env python3
"""
Render preview images of a CadQuery model for visual inspection.

Usage:
    python3 preview.py model.stl [output.png]
    python3 preview.py model.stl --views multi       # 6-view technical sheet
    python3 preview.py model.stl --views iso          # single isometric
    python3 preview.py model.stl --resolution 800     # higher-res per view

Dependencies:
    pip install trimesh pyrender Pillow
"""
import sys
import os
import argparse
import math
import numpy as np

# Pyrender needs an OpenGL context for offscreen rendering.
# On Linux set PYOPENGL_PLATFORM=egl (GPU) or osmesa (CPU) before import.
# On macOS the default CGL/pyglet backend works — do NOT set egl/osmesa.
import platform as _plat
if _plat.system() == "Linux" and "PYOPENGL_PLATFORM" not in os.environ:
    os.environ["PYOPENGL_PLATFORM"] = "egl"

import trimesh
import pyrender
from PIL import Image, ImageDraw, ImageFont

from mesh_io import load_mesh  # re-exported: preview's public surface for mesh loading


# ---------------------------------------------------------------------------
# Scene + camera helpers
# ---------------------------------------------------------------------------

def _rotation_matrix(elev_deg, azim_deg):
    """Build a camera-pose matrix from elevation and azimuth (degrees).

    Convention:
        azim  = rotation around Z (world up)
        elev  = rotation above the XY plane
    Returns a 4x4 camera pose (OpenGL: -Z forward, +Y up).
    """
    elev = math.radians(elev_deg)
    azim = math.radians(azim_deg)

    # Camera position on a unit sphere
    cx = math.cos(elev) * math.cos(azim)
    cy = math.cos(elev) * math.sin(azim)
    cz = math.sin(elev)
    eye = np.array([cx, cy, cz])

    # Look-at
    target = np.array([0.0, 0.0, 0.0])
    up = np.array([0.0, 0.0, 1.0])

    forward = target - eye
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, up)
    if np.linalg.norm(right) < 1e-6:
        # Degenerate case (looking straight down/up)
        up = np.array([0.0, 1.0, 0.0])
        right = np.cross(forward, up)
    right /= np.linalg.norm(right)
    cam_up = np.cross(right, forward)

    # Build OpenGL camera matrix (-Z forward)
    pose = np.eye(4)
    pose[0:3, 0] = right
    pose[0:3, 1] = cam_up
    pose[0:3, 2] = -forward
    pose[0:3, 3] = eye
    return pose


def _nice_spacing(extent):
    """Pick a human-friendly grid spacing that gives ~8-12 lines."""
    target = extent / 10
    for s in [1, 2, 5, 10, 20, 50, 100, 200]:
        if s >= target:
            return s
    return 200


def _build_grid(tm):
    """Create a ground-plane grid mesh at the bottom of the object.

    Returns (ground_plane_trimesh, grid_lines_trimesh).
    """
    bounds = tm.bounds  # shape (2, 3): [[min_x,y,z], [max_x,y,z]]
    z_floor = bounds[0][2]
    cx, cy = tm.bounding_box.centroid[:2]

    extent = max(bounds[1][0] - bounds[0][0], bounds[1][1] - bounds[0][1])
    spacing = _nice_spacing(extent)
    pad = extent * 0.5

    # Snap grid bounds to spacing multiples
    x0 = math.floor((cx - extent / 2 - pad) / spacing) * spacing
    x1 = math.ceil((cx + extent / 2 + pad) / spacing) * spacing
    y0 = math.floor((cy - extent / 2 - pad) / spacing) * spacing
    y1 = math.ceil((cy + extent / 2 + pad) / spacing) * spacing

    lw = max(0.4, spacing * 0.02)  # line half-width

    # --- Ground plane (slightly below grid lines to avoid z-fighting) ---
    ground = trimesh.creation.box(
        extents=[x1 - x0, y1 - y0, 0.01],
        transform=trimesh.transformations.translation_matrix(
            [(x0 + x1) / 2, (y0 + y1) / 2, z_floor - 0.02]
        ),
    )

    # --- Grid lines as thin quads at z_floor ---
    verts = []
    faces = []

    def _add_quad(v0, v1, v2, v3):
        n = len(verts)
        verts.extend([v0, v1, v2, v3])
        faces.extend([[n, n + 1, n + 2], [n, n + 2, n + 3]])

    # Lines parallel to X axis (one per Y tick)
    y = y0
    while y <= y1 + 0.001:
        _add_quad(
            [x0, y - lw, z_floor], [x1, y - lw, z_floor],
            [x1, y + lw, z_floor], [x0, y + lw, z_floor],
        )
        y += spacing

    # Lines parallel to Y axis (one per X tick)
    x = x0
    while x <= x1 + 0.001:
        _add_quad(
            [x - lw, y0, z_floor], [x + lw, y0, z_floor],
            [x + lw, y1, z_floor], [x - lw, y1, z_floor],
        )
        x += spacing

    grid_lines = trimesh.Trimesh(
        vertices=np.array(verts), faces=np.array(faces)
    )
    return ground, grid_lines


def _build_scene(tm, include_ground=True):
    """Create a pyrender scene containing the mesh, lights, and optionally ground.

    Returns (scene, bounding_sphere_radius, center, ground_node, grid_node).
    ground_node/grid_node are None if include_ground is False.
    """
    # Compute smooth vertex normals so Phong shading looks good
    tm.fix_normals()

    mesh = pyrender.Mesh.from_trimesh(
        tm,
        smooth=True,
        material=pyrender.MetallicRoughnessMaterial(
            baseColorFactor=[0.42, 0.62, 0.92, 1.0],  # medium blue
            metallicFactor=0.1,
            roughnessFactor=0.6,
            doubleSided=True,
        ),
    )

    scene = pyrender.Scene(
        bg_color=[0.90, 0.90, 0.92, 1.0],  # neutral light gray
        ambient_light=[0.3, 0.3, 0.3],
    )
    scene.add(mesh)

    # Ground grid (skipped for below-horizon views to avoid occluding the model)
    ground_node = None
    grid_node = None
    if include_ground:
        ground, grid_lines = _build_grid(tm)
        ground_mat = pyrender.MetallicRoughnessMaterial(
            baseColorFactor=[0.82, 0.82, 0.84, 1.0],
            metallicFactor=0.0,
            roughnessFactor=0.9,
        )
        grid_mat = pyrender.MetallicRoughnessMaterial(
            baseColorFactor=[0.68, 0.68, 0.72, 1.0],
            metallicFactor=0.0,
            roughnessFactor=0.9,
        )
        ground_node = scene.add(pyrender.Mesh.from_trimesh(ground, material=ground_mat, smooth=False))
        grid_node = scene.add(pyrender.Mesh.from_trimesh(grid_lines, material=grid_mat, smooth=False))

    # Four-point lighting: three from above + one from below so the
    # bottom view (Z-) isn't in total shadow.
    for direction in ([1, 1, 1], [-1, 0.5, 0.5], [0, -1, 1], [0, 0.5, -1]):
        light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=2.5)
        d = np.array(direction, dtype=float)
        d /= np.linalg.norm(d)
        pose = np.eye(4)
        pose[0:3, 2] = -d  # pyrender light shines along -Z of its frame
        scene.add(light, pose=pose)

    # Bounding sphere for camera framing
    center = tm.bounding_box.centroid
    radius = np.linalg.norm(tm.bounding_box.extents) / 2.0

    return scene, radius, center, ground_node, grid_node


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

DEFAULT_VIEW_SIZE = 600  # width/height of each sub-view (multi-view)
_SINGLE_WIDTH = 900      # single isometric view defaults
_SINGLE_HEIGHT = 750


def _add_edges(color, depth, strength=0.6):
    """Overlay edge lines detected from the depth buffer onto the color image."""
    valid = depth > 0
    if not valid.any():
        return color

    # Normalise depth into 0-1 range for gradient detection
    d = np.zeros_like(depth)
    d_min, d_max = depth[valid].min(), depth[valid].max()
    if d_max - d_min > 0:
        d[valid] = (depth[valid] - d_min) / (d_max - d_min)

    # Sobel-style gradient magnitude
    dy = np.zeros_like(d)
    dx = np.zeros_like(d)
    dy[1:, :] = np.abs(d[1:, :] - d[:-1, :])
    dx[:, 1:] = np.abs(d[:, 1:] - d[:, :-1])
    edges = np.sqrt(dx ** 2 + dy ** 2)

    # Object-boundary edges (depth jumps from 0 to non-zero)
    boundary = np.zeros_like(valid)
    boundary[1:, :] |= (valid[1:, :] != valid[:-1, :])
    boundary[:, 1:] |= (valid[:, 1:] != valid[:, :-1])

    # Normalise to 0-1 and apply threshold
    p = np.percentile(edges[valid], 97) if valid.sum() > 100 else 1.0
    if p > 0:
        edges = np.clip(edges / p, 0, 1)
    edge_alpha = np.clip(edges * strength, 0, strength)
    edge_alpha[boundary] = np.maximum(edge_alpha[boundary], strength * 0.8)

    # Darken colour at edge pixels
    result = color.astype(np.float32)
    result *= (1 - edge_alpha[:, :, np.newaxis])
    return np.clip(result, 0, 255).astype(np.uint8)


def _render_frame(scene, radius, center, elev, azim, renderer):
    """Render one frame from an existing scene.

    Adds a camera, renders, then removes the camera so the scene can be
    reused for additional views without rebuilding.
    """
    yfov = math.radians(35)
    cam = pyrender.PerspectiveCamera(yfov=yfov)
    distance = radius / math.sin(yfov / 2) * 1.15  # slight padding

    cam_pose = _rotation_matrix(elev, azim)
    cam_pose[0:3, 3] = center + cam_pose[0:3, 2] * distance

    cam_node = scene.add(cam, pose=cam_pose)
    try:
        color, depth = renderer.render(scene)
    except Exception as e:
        scene.remove_node(cam_node)
        raise RuntimeError(
            f"Rendering failed: {e}\n"
            "On Linux without GPU, try: PYOPENGL_PLATFORM=osmesa python3 preview.py ..."
        ) from e
    scene.remove_node(cam_node)

    color = _add_edges(color, depth)
    return Image.fromarray(color)


def render_view(tm, elev, azim, width=DEFAULT_VIEW_SIZE, height=DEFAULT_VIEW_SIZE):
    """Render the mesh from a specific angle. Returns a PIL Image."""
    scene, radius, center, _, _ = _build_scene(tm)
    renderer = None
    try:
        renderer = pyrender.OffscreenRenderer(width, height)
        img = _render_frame(scene, radius, center, elev, azim, renderer)
    finally:
        if renderer is not None:
            renderer.delete()
    return img


def _get_font(size=14):
    """Try to load a nice sans-serif font, falling back to PIL default."""
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _info_lines(tm):
    """Two-line footer with dimensions, volume, triangle count, and status."""
    extents = tm.bounding_box.extents
    line1 = f"Bounding box: {extents[0]:.1f} x {extents[1]:.1f} x {extents[2]:.1f} mm"
    try:
        vol = abs(tm.volume)
        line1 += f"  |  Volume: {vol/1000:.1f} cm\u00b3"
    except Exception:
        pass

    line2 = f"Triangles: {len(tm.faces):,}"
    line2 += f"  |  {'Watertight' if tm.is_watertight else 'NOT watertight'}"
    try:
        vol = abs(tm.volume)
        weight_g = vol / 1000 * 1.24  # PLA density ~1.24 g/cm3
        line2 += f"  |  PLA estimate: ~{weight_g:.0f} g"
    except Exception:
        pass
    return line1, line2


def render_single(tm, output_path, title="Model Preview", width=_SINGLE_WIDTH, height=_SINGLE_HEIGHT):
    """Render a single isometric view with title and footer."""
    img = render_view(tm, elev=25, azim=-60, width=width, height=height)

    # Add title + footer
    canvas = Image.new("RGB", (img.width, img.height + 100), "white")
    canvas.paste(img, (0, 40))
    draw = ImageDraw.Draw(canvas)

    title_font = _get_font(20)
    info_font = _get_font(13)
    line1, line2 = _info_lines(tm)

    draw.text((canvas.width // 2, 10), title, fill="black", font=title_font, anchor="mt")
    draw.text((canvas.width // 2, canvas.height - 30), line1,
              fill="gray", font=info_font, anchor="mb")
    draw.text((canvas.width // 2, canvas.height - 10), line2,
              fill="gray", font=info_font, anchor="mb")

    canvas.save(output_path)
    return output_path


def render_multi_view(tm, output_path, title="Model Preview", subtitle=None, view_size=DEFAULT_VIEW_SIZE):
    """Render 6-view technical preview in a 3x2 grid.

    Views: isometric, front, right (top row), back-iso, top, bottom (bottom row).
    Builds the scene once and reuses a single renderer for all views.
    """
    views = [
        (25,  -60, "Isometric"),
        (5,   -90, "Front (Y-)"),
        (5,     0, "Right (X+)"),
        (25,  120, "Back Isometric"),
        (90,  -90, "Top (Z+)"),
        (-90, -90, "Bottom (Z-)"),
    ]

    scene, radius, center, _, _ = _build_scene(tm, include_ground=True)
    scene_bottom, _, _, _, _ = _build_scene(tm, include_ground=False)
    renderer = None
    try:
        renderer = pyrender.OffscreenRenderer(view_size, view_size)
        images = []
        for elev, azim, label in views:
            s = scene_bottom if elev < 0 else scene
            img = _render_frame(s, radius, center, elev, azim, renderer)
            images.append((img, label))
    finally:
        if renderer is not None:
            renderer.delete()

    # Compose 3x2 grid
    cols = 3
    rows = 2
    gap = 4
    header_h = 40 + (20 if subtitle else 0)
    footer_h = 55
    label_h = 24
    w = view_size * cols + gap * (cols - 1)
    h = view_size * rows + gap * (rows - 1) + header_h + footer_h + label_h * rows

    canvas = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(canvas)

    title_font = _get_font(20)
    subtitle_font = _get_font(14)
    label_font = _get_font(14)
    info_font = _get_font(13)

    # Title + optional subtitle
    draw.text((w // 2, 12), title, fill="black", font=title_font, anchor="mt")
    if subtitle:
        draw.text((w // 2, 34), subtitle, fill="#666666", font=subtitle_font, anchor="mt")

    for idx, (img, label) in enumerate(images):
        col = idx % cols
        row = idx // cols
        px = col * (view_size + gap)
        py = header_h + label_h + row * (view_size + gap + label_h)
        canvas.paste(img, (px, py))
        draw.text((px + view_size // 2, py - 4), label,
                  fill="#444444", font=label_font, anchor="mb")

    # Footer (two lines)
    line1, line2 = _info_lines(tm)
    draw.text((w // 2, h - 30), line1, fill="gray", font=info_font, anchor="mb")
    draw.text((w // 2, h - 10), line2, fill="gray", font=info_font, anchor="mb")

    canvas.save(output_path)
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Preview a 3D model STL file")
    parser.add_argument("stl_file", help="Path to STL file")
    parser.add_argument("output", nargs="?", default=None,
                        help="Output PNG path (default: <stl_name>_preview.png)")
    parser.add_argument("--views", choices=["iso", "multi"], default="multi",
                        help="View mode: iso (single) or multi (6-view)")
    parser.add_argument("--title", default=None, help="Title for the preview")
    parser.add_argument("--resolution", type=int, default=DEFAULT_VIEW_SIZE,
                        help=f"Pixels per view (default: {DEFAULT_VIEW_SIZE})")
    parser.add_argument("--subtitle", default=None,
                        help="Subtitle shown below the title (e.g. model description or usage)")
    parser.add_argument("--strict", action="store_true",
                        help="Fail with exit code 2 if the mesh is not watertight")
    args = parser.parse_args()

    if args.output is None:
        base = os.path.splitext(args.stl_file)[0]
        args.output = f"{base}_preview.png"

    if args.title is None:
        args.title = os.path.splitext(os.path.basename(args.stl_file))[0].replace("_", " ").title()

    try:
        tm = load_mesh(args.stl_file)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    extents = tm.bounding_box.extents
    print(f"Model: {args.stl_file}")
    print(f"Bounding box: {extents[0]:.1f} x {extents[1]:.1f} x {extents[2]:.1f} mm")
    print(f"Triangles: {len(tm.faces)}")

    if tm.is_watertight:
        print("Mesh: watertight (good)")
    else:
        print("WARNING: Mesh is NOT watertight. May cause slicing issues.",
              file=sys.stderr)
        if args.strict:
            print("ERROR: --strict set, aborting before render.",
                  file=sys.stderr)
            sys.exit(2)

    if args.views == "multi":
        render_multi_view(tm, args.output, args.title, subtitle=args.subtitle,
                          view_size=args.resolution)
    else:
        scale = args.resolution / DEFAULT_VIEW_SIZE
        render_single(tm, args.output, args.title,
                      width=int(_SINGLE_WIDTH * scale), height=int(_SINGLE_HEIGHT * scale))

    print(f"Preview saved: {args.output} ({os.path.getsize(args.output)} bytes)")


if __name__ == "__main__":
    main()
```

<a id="skills__3d-modeling__scripts__make_3mf_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/make_3mf.py`  (78 lines)
------------------------------------------------------------------------------------------

```python
#!/usr/bin/env python3
"""Weld multiple STL parts into ONE 3MF whose build object contains one component
per part. Bambu Studio / OrcaSlicer import the result as a single object with
individually selectable parts (assign a filament per part for multi-color).

Usage:
    python3 make_3mf.py out.3mf "KnobBody (black)=body.stl" "Pattern (white)=pattern.stl"

Parts must already share one coordinate system (exported from the same CAD doc).
Requires: pip install trimesh numpy
"""
import sys, io, zipfile, os
import trimesh


def mesh_xml(obj_id, name, mesh):
    buf = io.StringIO()
    buf.write(f'<object id="{obj_id}" type="model" name="{name}"><mesh><vertices>')
    for x, y, z in mesh.vertices:
        buf.write(f'<vertex x="{x:.6g}" y="{y:.6g}" z="{z:.6g}"/>')
    buf.write('</vertices><triangles>')
    for a, b, c in mesh.faces:
        buf.write(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>')
    buf.write('</triangles></mesh></object>')
    return buf.getvalue()


def main():
    if len(sys.argv) < 3 or any('=' not in s for s in sys.argv[2:]):
        sys.exit(__doc__)
    out, specs = sys.argv[1], sys.argv[2:]
    objects, comp = [], []
    for i, spec in enumerate(specs, start=1):
        name, path = spec.split('=', 1)
        m = trimesh.load(path, process=True)  # welds duplicate STL vertices
        m.remove_unreferenced_vertices()
        print(f'{name}: {len(m.vertices)} verts, {len(m.faces)} tris, '
              f'watertight={m.is_watertight}')
        if not m.is_watertight:
            print(f'  WARNING: {name} is not watertight — check the source mesh')
        objects.append(mesh_xml(i, name, m))
        comp.append(f'<component objectid="{i}"/>')
    asm_id = len(specs) + 1
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
        '<resources>' + ''.join(objects)
        + f'<object id="{asm_id}" type="model" name="assembly">'
          f'<components>{"".join(comp)}</components></object>'
        '</resources>'
        f'<build><item objectid="{asm_id}"/></build>\n</model>'
    )
    ct = ('<?xml version="1.0" encoding="UTF-8"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel-1" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
            '</Relationships>')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('3D/3dmodel.model', model)
    print('wrote', out, os.path.getsize(out), 'bytes')
    try:  # round-trip check — file is already written; failure here is verification only
        check = trimesh.load(out)
        geoms = getattr(check, 'geometry', {})
        print('re-loaded:', {k: (len(g.vertices), len(g.faces)) for k, g in geoms.items()})
    except Exception as e:
        print(f'wrote OK; round-trip verification skipped: {e}')


if __name__ == '__main__':
    main()
```

<a id="skills__3d-modeling__scripts__make_bambu_3mf_py"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/scripts/make_bambu_3mf.py`  (760 lines)
------------------------------------------------------------------------------------------

```python
#!/usr/bin/env python3
"""
Weld STL parts into ONE **Bambu Studio project 3MF** with print settings and
per-part filament assignment already baked in, so opening it in Bambu Studio is
"import -> eyeball -> slice" with nothing to configure by hand.

    python make_bambu_3mf.py out.3mf "Base (translucent)=base.stl" "Text (CF)=text.stl"

Part-name -> filament rule (the whole point of this script; see PART_RULES):
    name contains "Base"  ->  filament 1, Bambu PETG Translucent, MAIN nozzle
    name contains "Text"  ->  filament 2, Bambu PETG-CF,          AUX  nozzle

Why this exists at all: the plain 3MF core spec (what skills/3d-modeling/scripts/
make_3mf.py writes) carries geometry and nothing else. Bambu Studio imports it as
one object with N selectable parts, but every part lands on filament 1 and the
process preset is whatever was last used. On a dual-nozzle X2D with a translucent
part that must be 100% infill, that is four separate hand-edits, each easy to get
wrong and invisible until the print fails. See references/bambu-3mf-authoring.md
for the concepts (project_settings.config vs model_settings.config, the slicer
round-trip, the three traps, and the honesty rule) this script implements.

ADAPTING TO ANOTHER MACHINE/PRINTER: every preset name, profile id, extruder
map, and pinned value below is X2D-specific and was read out of THIS machine's
*installed* Bambu Studio profile tree (BBL system bundle) - names from a newer
machine like the X2D do NOT transfer from H2D/older machines. To retarget:
re-run the round-trip in references/bambu-3mf-authoring.md (configure a plate for
the new machine in Bambu Studio, Save Project As, unzip, diff two saves) to learn
that machine's profile ids and key names/values, then update PRINTER_PRESET /
PROCESS_PRESET / FILAMENT_PRESETS / PART_RULES / the per-variant + fixup tables
here. Never guess keys; verify() proves internal consistency only, not that the
slicer accepts the file.

Requires: trimesh, numpy (mesh load), lxml (verification). Reads - never writes -
the installed Bambu Studio profile tree.
"""

import io
import json
import os
import sys
import uuid
import zipfile

import trimesh
from lxml import etree

# ============================ WHERE THE FACTS COME FROM =====================
# Everything below was read out of the *installed* Bambu Studio, not guessed.
# The user runs BambuStudio 02.07.01.62 (bambu-studio.exe FileVersion, and
# BambuStudio.conf app.version) with vendor profile bundle BBL 02.07.00.08.
# X2D support is new, so profile names from H2D/older machines do NOT transfer -
# every name below is copied verbatim from a file on this disk.
#
# Ground truth for the file layout and for every value below is
# yacht/reference_x2d.3mf: a project the user actually saved from Bambu Studio
# 02.07.01.62 for this X2D. Everything this script emits was diffed against it -
# same members, same XML shape, same array lengths, and identical values except
# for the settings we deliberately override and two filament swatch colours.

BBL_ROOT = os.path.join(os.environ.get("APPDATA", ""), "BambuStudio")
BBL_VENDOR_JSON = os.path.join(BBL_ROOT, "system", "BBL.json")   # profile index
BBL_SYSTEM_DIR = os.path.join(BBL_ROOT, "system", "BBL")
BBL_CONF = os.path.join(BBL_ROOT, "BambuStudio.conf")            # app version

# --- Presets. Names are the exact `name` field of the system profile JSONs, ---
# --- which is also the string Bambu Studio shows in its preset combo boxes. ---
PRINTER_PRESET = "Bambu Lab X2D 0.4 nozzle"
#   system/BBL/machine/Bambu Lab X2D 0.4 nozzle.json  setting_id GM045
#   -> nozzle_diameter ["0.4","0.4"], extruder_type ["Direct Drive","Bowden"]

PROCESS_PRESET = "0.20mm Standard @BBL X2D"
#   system/BBL/process/0.20mm Standard @BBL X2D.json  setting_id GP151
#   Already layer_height 0.2 / initial_layer_print_height 0.2; it is also the
#   machine's own `default_print_profile`, so it is the least surprising base.

FILAMENT_PRESETS = [
    "Bambu PETG Translucent @BBL X2D 0.4 nozzle",   # setting_id GFSG01_19, filament_id GFG01
    "Bambu PETG-CF @BBL X2D 0.4 nozzle",            # setting_id GFSG50_17, filament_id GFG50
]
# Both are `instantiation: true` with compatible_printers ["Bambu Lab X2D 0.4
# nozzle"], i.e. they are exactly the two entries the X2D 0.4 filament dropdown
# offers for these materials. PETG-CF carries required_nozzle_HRC 40 - fine, both
# X2D nozzles are hardened steel.

# Filament swatch colours. Cosmetic (3D-view tint + flush estimate) but the
# indigo is real: it is the PETG-CF spool already in this user's Bambu filament
# inventory - AppData/Roaming/BambuStudio/filament_inventory/spools.json,
# setting_id GFG50, tray "G50-B6", color_code "#324585FF".
FILAMENT_COLOURS = ["#E8E8E8", "#324585"]

# --- MAIN vs AUX -> extruder index. Three independent confirmations: ---------
#   1. machine/Bambu Lab X2D 0.4 nozzle.json:
#        extruder_type            = ["Direct Drive", "Bowden"]
#        printer_extruder_variant = ["Direct Drive Standard","Direct Drive High
#                                    Flow","Bowden Standard","Bowden High Flow"]
#   2. process/0.20mm Standard @BBL X2D (inherited) pairs those four variants
#        with print_extruder_id   = ["1","1","2","2"]
#   3. a real X2D project saved by this Studio build (Downloads/Poop-Bucket-
#        Logo-X2D.3mf) carries printer_extruder_id = ["1","1","2","2"] against
#        the same variant list.
#   => extruder 1 == Direct Drive == MAIN;  extruder 2 == Bowden == AUX.
EXTRUDER_MAIN = 1
EXTRUDER_AUX = 2

# --- Part-name -> (filament slot, physical extruder) ------------------------
# `filament slot` is what goes in model_settings.config as the per-part
# `extruder` metadata: a 1-based index into the project's filament list.
# `physical extruder` is a separate concept, expressed by filament_map below.
# Note the rule is applied HERE, at build time, and the result is written out as
# a literal per-part `extruder` value. Nothing at import time re-derives it from
# the name, which matters: a bare core-spec 3MF (no model_settings.config) loses
# its part names entirely - importing the old sample_coupon.3mf gave Bambu Studio
# parts called "assembly" and "assembly_2" (see yacht/reference_x2d.3mf). Names
# survive only because we write them as <metadata key="name"> ourselves, and the
# assignment does not depend on that surviving anyway.
PART_RULES = [
    ("Base", 1, EXTRUDER_MAIN),   # translucent PETG, direct drive, ~98% of volume
    ("Text", 2, EXTRUDER_AUX),    # PETG-CF, Bowden; ~0.5 g in the bottom 3 layers
]
DEFAULT_SLOT = 1                  # unmatched part names fall back to filament 1

# --- Process overrides we bake in on top of PROCESS_PRESET ------------------
PROCESS_OVERRIDES = {
    # The coupon's step heights are chosen so every zone is a whole number of
    # 0.2 mm layers. Both are already 0.2 in GP151; pinned here so a future
    # preset change can never silently re-round the geometry.
    "layer_height": "0.2",
    "initial_layer_print_height": "0.2",

    # Sparse infill inside a translucent plate prints a lattice straight through
    # the viewing path. 100% removes it. Preset default is 15%.
    "sparse_infill_density": "100%",
    # At 100% the pattern still matters optically: `grid` (the preset default)
    # crosses over itself and leaves a faint waffle. `monotonic` lays a
    # unidirectional solid, same as a top surface. Enum verified against the
    # pattern list in BambuStudio.dll.
    "sparse_infill_pattern": "monotonic",

    # Brim would run over the engraved zone labels, which sit ~1.9 mm from the
    # part edge. Enum values in BambuStudio.dll: no_brim / outer_only /
    # inner_only / outer_and_inner / auto_brim / brim_ears. Studio's default is
    # auto_brim, so this override is doing real work.
    "brim_type": "no_brim",
    "brim_width": "0",

    # The only plate this user owns. Enum from BambuStudio.dll: Cool Plate /
    # Engineering Plate / High Temp Plate / Textured PEI Plate / Supertack
    # Plate. It selects which of the filament profiles' *_plate_temp pairs is
    # used - both PETG profiles say textured_plate_temp 70 / first layer 70.
    # (The X2D machine model also declares default_bed_type "Textured PEI
    # Plate" and not_support_bed_type "Cool Plate".)
    "curr_bed_type": "Textured PEI Plate",
}

# Chamber / cooling is deliberately NOT overridden. The X2D advertises
# support_chamber_temp_control 1, but both PETG profiles ship
# chamber_temperatures ["0"] - no active chamber heating, i.e. the cool-running
# configuration PETG wants - together with during_print_exhaust_fan_speed 70 and
# activate_air_filtration 0. Those inherited values are the correct "PETG on an
# X2D in Cool Mode" answer; inventing our own would only make it worse.

# ============================ PROFILE RESOLUTION ============================
# Bambu profiles are a single-inheritance chain via the `inherits` key, resolved
# against the vendor index in system/BBL.json. Flattening it here reproduces what
# Studio itself computes when you pick the preset, and guarantees the numbers we
# emit match the *installed* bundle rather than some remembered version.

# Keys that are profile bookkeeping, not print settings. Confirmed absent from a
# real project_settings.config written by this Studio build.
_META_KEYS = {
    "type", "name", "from", "inherits", "setting_id", "instantiation",
    "description", "include", "filament_id", "version",
    "compatible_printers", "compatible_printers_condition",
    "filament_ingredients_safe", "filament_emission_safe", "filament_contact_safe",
}

# Legacy keys that still sit in the shipped profile JSONs but are not options in
# this Studio build - none of these strings occurs anywhere in BambuStudio.dll,
# and none appears in a real project_settings.config written by it. Studio's
# loader would skip them with a warning; cleaner not to emit them at all.
_LEGACY_KEYS = {
    "deretract_speed_extruder_change", "extruder_clearance_radius",
    "extruder_height_gap", "filament_long_retractions_when_ec",
    "filament_retraction_distances_when_ec",
    "layer_time_smoothing", "layer_time_smoothing_threshold",
}
_META_KEYS |= _LEGACY_KEYS

# Filament options that Bambu Studio stores per *extruder variant* (4 of them on
# the X2D) even though the shipped filament JSONs carry only a single value for
# them. Derived by comparing a real 4-filament X2D project_settings.config
# (Downloads/Poop-Bucket-Logo-X2D.3mf, written by 02.07.01.62) against the
# installed filament profiles: these are exactly the keys whose project array is
# 4x the filament count while the profile holds one value. Everything else
# follows the profile's own block size, so no table is needed for it.
# Emitting them at block 1 is not fatal - Preset::normalize() resizes filament
# vectors by padding - but the padded entries land at the wrong offsets as soon
# as two filaments disagree, so get the shape right instead.
_PER_VARIANT_FILAMENT_KEYS = {
    "filament_adaptive_volumetric_speed", "filament_bridge_speed",
    "filament_deretraction_speed", "filament_enable_overhang_speed",
    "filament_flush_temp", "filament_flush_volumetric_speed",
    "filament_long_retractions_when_cut", "filament_overhang_1_4_speed",
    "filament_overhang_2_4_speed", "filament_overhang_3_4_speed",
    "filament_overhang_4_4_speed", "filament_overhang_totally_speed",
    "filament_pre_cooling_temperature", "filament_pre_cooling_temperature_nc",
    "filament_preheat_temperature_delta", "filament_ramming_travel_time_nc",
    "filament_ramming_volumetric_speed", "filament_ramming_volumetric_speed_nc",
    "filament_retract_before_wipe", "filament_retract_length_nc",
    "filament_retract_restart_extra", "filament_retract_when_changing_layer",
    "filament_retraction_minimum_travel", "filament_retraction_speed",
    "filament_z_hop", "long_retractions_when_ec",
    "override_process_overhang_speed", "slow_down_min_speed",
    "volumetric_speed_coefficients",
}
# Per-filament option that lives in the machine/process profile as a single
# value; same source, same reasoning.
_PER_FILAMENT_FROM_MACHINE = {"pre_start_fan_time"}

# Handful of keys where the value shipped in the *generic ancestor* profiles
# (fdm_process_common / fdm_process_dual_common / fdm_filament_common /
# fdm_bbl_3dp_002_common) is stale: a project actually saved by this Studio for
# an X2D (yacht/reference_x2d.3mf) contains something else, i.e. Studio's own
# default wins over those ancestors. Two of them matter semantically -
# monotonic_travel_into_wall "45.0" would be read as 45 *mm* instead of 45%, and
# long_retractions_when_ec flips 0 -> 1 - so pin all of them to what the real
# save contains. Values that are per-variant are given as a single element and
# replicated below.
_REFERENCE_FIXUPS = {
    "monotonic_travel_into_wall": "45%",       # profile says "45.0"
    "bottom_surface_density": "100%",          # profile says "100"
    "top_surface_density": "100%",             # profile says "100"
    "best_object_pos": "0.3,0.5",              # profile says "0.3x0.5"
}
_REFERENCE_FIXUPS_PER_VARIANT = {
    "long_retractions_when_ec": "1",           # fdm_filament_common says "0"
    "filament_preheat_temperature_delta": "10",  # fdm_filament_common says "0"
}


def profile_index():
    """name -> absolute path, for every machine/filament/process system profile."""
    with open(BBL_VENDOR_JSON, encoding="utf-8") as f:
        vendor = json.load(f)
    idx = {}
    for key in ("machine_list", "filament_list", "process_list"):
        for entry in vendor[key]:
            idx[entry["name"]] = os.path.join(
                BBL_SYSTEM_DIR, entry["sub_path"].replace("/", os.sep))
    return idx, vendor["version"]


def apply_gcode_templates(idx, name, cfg):
    """Overlay the machine's `<preset> template <key>.json` sidecars.

    The X2D's start/end/layer-change/filament-change/timelapse G-code is NOT in
    Bambu Lab X2D 0.4 nozzle.json - those keys are absent there and live in five
    sibling profiles named "<preset> template <key>" with instantiation:false.
    Miss this and the inheritance chain silently hands back the generic
    fdm_bbl_3dp_002_common G-code, which is X1/P1 flavour: no X2D toolhead-offset
    calibration, wrong dual-nozzle filament change. A real X2D project saved by
    Studio contains the X2D flavour (";======== X2D start gcode ========"), which
    is how this was caught.
    """
    prefix = name + " template "
    for key in [k for k in idx if k.startswith(prefix)]:
        for k, v in flatten(idx, key).items():
            if k not in _META_KEYS:
                cfg[k] = v
    return cfg


def flatten(idx, name):
    """Resolve `name` through its `inherits` chain, child overriding parent."""
    chain = []
    while name:
        path = idx.get(name)
        if path is None:
            raise SystemExit(f"profile not found in installed BBL bundle: {name!r}")
        with open(path, encoding="utf-8") as f:
            node = json.load(f)
        chain.append(node)
        name = node.get("inherits")
    out = {}
    for node in reversed(chain):          # root ancestor first
        out.update(node)
    return out


def studio_version():
    """App version string, e.g. '02.07.01.62'. Stamped into the config files so
    they agree with the Studio that will open them. BambuStudio.conf is JSON
    followed by trailing bytes, hence raw_decode."""
    try:
        with open(BBL_CONF, encoding="utf-8") as f:
            conf, _ = json.JSONDecoder().raw_decode(f.read())
        return conf["app"]["version"]
    except Exception:
        return "02.07.01.62"          # observed on this machine; last resort


# ======================== Metadata/project_settings.config ==================
# The JSON blob holding print + filament + printer settings for the whole
# project. Studio starts from its compiled-in defaults, applies this on top, then
# tries to match each section back to a named preset. Keys we omit therefore fall
# back to Studio's own default - which, for anything the system profiles do not
# override, is the same value the preset would have given.

def build_project_settings(idx, bundle_version):
    machine = apply_gcode_templates(idx, PRINTER_PRESET, flatten(idx, PRINTER_PRESET))
    machine["printable_area"] = [s.strip() for s in machine["printable_area"]]
    process = flatten(idx, PROCESS_PRESET)
    filaments = [flatten(idx, n) for n in FILAMENT_PRESETS]
    n = len(filaments)

    cfg = {}
    # Machine and process values are already shaped correctly: scalars, or lists
    # of 2 (per physical extruder), 4 (per extruder *variant*) or 8 (2 x 4).
    for src in (machine, process):
        for k, v in src.items():
            if k not in _META_KEYS:
                cfg[k] = v

    # Filament values are per-preset and must be concatenated in slot order.
    # Shape rule, read off a real project file: a filament option stored as a
    # 1-element list is per-filament (final length n), a 4-element list is
    # per-extruder-variant (final length 4n, e.g. nozzle_temperature), a
    # 2-element list stays 2-per-filament. So: concatenate the raw blocks.
    n_var = len(machine["printer_extruder_variant"])
    fil_keys = set()
    for f in filaments:
        fil_keys |= {k for k, v in f.items() if k not in _META_KEYS and isinstance(v, list)}
    blocks = {}
    for k in sorted(fil_keys):
        if not all(k in f and len(f[k]) == len(filaments[0].get(k, [])) for f in filaments):
            continue          # inconsistent across presets -> let Studio default it
        rep = n_var if (k in _PER_VARIANT_FILAMENT_KEYS and len(filaments[0][k]) == 1) else 1
        blocks[k] = len(filaments[0][k]) * rep
        cfg[k] = [str(x) for f in filaments for x in f[k] for _ in range(rep)]

    # Same treatment for the handful that arrive from the machine/process side
    # but are per-filament in a project file.
    for k in _PER_FILAMENT_FROM_MACHINE:
        if isinstance(cfg.get(k), list) and len(cfg[k]) == 1:
            cfg[k] = [str(cfg[k][0])] * n
            blocks[k] = 1

    # ---- identity / preset matching -----------------------------------------
    cfg["from"] = "project"
    cfg["name"] = "project_settings"
    cfg["version"] = studio_version()          # must agree with the app reading it
    cfg["printer_settings_id"] = PRINTER_PRESET
    cfg["print_settings_id"] = PROCESS_PRESET
    cfg["filament_settings_id"] = list(FILAMENT_PRESETS)
    cfg["print_compatible_printers"] = [PRINTER_PRESET]
    cfg["default_print_profile"] = PROCESS_PRESET
    cfg["filament_ids"] = [flatten(idx, nme).get("filament_id", "") for nme in FILAMENT_PRESETS]

    # ---- THE per-part colour plumbing ---------------------------------------
    # Two distinct concepts, easy to conflate:
    #   * filament slot  - which spool a part is printed with. Lives per part in
    #     model_settings.config as `extruder` (1-based into these lists).
    #   * filament_map   - which physical nozzle each *slot* is loaded on.
    # filament_map_mode enum from BambuStudio.dll: Auto For Flush / Auto For
    # Match / Manual / Nozzle Manual / Auto For Quality. "Manual" is what stops
    # Studio re-deciding the mapping for us; the auto modes optimise flush volume
    # and would happily put both PETGs on the same nozzle.
    cfg["filament_map_mode"] = "Manual"
    cfg["filament_map"] = [str(e) for _, _, e in sorted(PART_RULES, key=lambda r: r[1])][:n]
    cfg["filament_colour"] = FILAMENT_COLOURS[:n]
    cfg["filament_multi_colour"] = FILAMENT_COLOURS[:n]
    cfg["default_filament_colour"] = [""] * n
    # These two are stored in the *filament* profile as a 1-element stub, but a
    # real project file expands them to one entry per extruder variant per
    # filament (16 for a 4-filament X2D project). Expand them the same way, and
    # drop them from `blocks` so the shape check below uses the real shape.
    cfg["filament_self_index"] = [str(i + 1) for i in range(n) for _ in range(n_var)]
    cfg["filament_extruder_variant"] = [v for _ in range(n)
                                        for v in machine["printer_extruder_variant"]]
    for k in ("filament_self_index", "filament_extruder_variant"):
        blocks[k] = n_var
    # Redundant with the machine profile, but a real project file states them
    # explicitly and they are the record of which variant belongs to which
    # nozzle - the evidence for EXTRUDER_MAIN/EXTRUDER_AUX above.
    cfg["printer_extruder_id"] = ["1", "1", "2", "2"]
    cfg["printer_extruder_variant"] = list(machine["printer_extruder_variant"])
    cfg["nozzle_volume_type"] = list(machine.get("default_nozzle_volume_type",
                                                 ["Standard", "Standard"]))

    # Flush volumes must be sized n*n per extruder (2n^2) and n per extruder
    # (2n), or Studio has to resize them itself. Values barely matter here: on a
    # dual-nozzle machine each nozzle keeps its own filament, so a "colour
    # change" is a nozzle change, not a purge of one material through the other.
    cfg["flush_volumes_matrix"] = ["0" if i == j else "140"
                                   for _ in range(2) for i in range(n) for j in range(n)]
    cfg["flush_volumes_vector"] = ["140"] * (2 * n)
    cfg["flush_multiplier"] = ["1", "1"]

    # Record which overrides genuinely deviate from the stock process preset
    # *before* applying them, so Studio's "modified" markers point at the real
    # deltas. layer_height/initial_layer_print_height are already 0.2 in GP151
    # and so should not show up here; curr_bed_type is a plater setting and is
    # not part of the process preset at all.
    cfg.update(_REFERENCE_FIXUPS)
    for k, v in _REFERENCE_FIXUPS_PER_VARIANT.items():
        cfg[k] = [v] * (n * n_var)
        blocks[k] = n_var

    deltas = sorted(k for k, v in PROCESS_OVERRIDES.items()
                    if k in process and str(process[k]) != v)
    cfg.update(PROCESS_OVERRIDES)
    # Layout is [process, filament_1 .. filament_n, printer].
    cfg["different_settings_to_system"] = [";".join(deltas)] + [""] * n + [""]

    return cfg, blocks, bundle_version


# ========================= Metadata/model_settings.config ==================
# The XML that actually carries the per-part assignment. Structure copied from
# real Bambu projects (Downloads/Toolbox_X2D_logo.3mf is the same shape as ours:
# one object, several parts, differing `extruder`):
#   <object id=C>        C = the *container* object id in 3D/3dmodel.model
#     <metadata key="extruder" value="1"/>          object-level default
#     <part id=K>        K = objectid of the component, i.e. the sub-mesh id
#       <metadata key="extruder" value="2"/>        per-part override <- the point
# Plus a <plate> block; its filament_maps mirrors project_settings' filament_map
# because the mapping is stored per plate as well as per project.

def build_model_settings(parts, container_id, tvec):
    def esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))

    o = io.StringIO()
    o.write('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n')
    o.write(f'  <object id="{container_id}">\n')
    o.write(f'    <metadata key="name" value="{esc(parts[0]["name"])}"/>\n')
    o.write(f'    <metadata key="extruder" value="{parts[0]["slot"]}"/>\n')
    o.write(f'    <metadata face_count="{sum(p["faces"] for p in parts)}"/>\n')
    for p in parts:
        o.write(f'    <part id="{p["id"]}" subtype="normal_part">\n')
        o.write(f'      <metadata key="name" value="{esc(p["name"])}"/>\n')
        # Identity: the sub-meshes are already in a common coordinate system
        # (same CAD doc), and the plate placement lives on the build item.
        o.write('      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n')
        o.write(f'      <metadata key="source_file" value="{esc(os.path.basename(p["src"]))}"/>\n')
        o.write('      <metadata key="source_object_id" value="0"/>\n')
        o.write('      <metadata key="source_volume_id" value="0"/>\n')
        for axis in "xyz":     # zero: the parts are already in shared coords
            o.write(f'      <metadata key="source_offset_{axis}" value="0"/>\n')
        o.write(f'      <metadata key="extruder" value="{p["slot"]}"/>\n')
        o.write(f'      <mesh_stat face_count="{p["faces"]}" edges_fixed="0" '
                'degenerate_facets="0" facets_removed="0" facets_reversed="0" '
                'backwards_edges="0"/>\n')
        o.write('    </part>\n')
    o.write('  </object>\n')

    slots = sorted({p["slot"] for p in parts})
    fmap = {slot: ext for _, slot, ext in PART_RULES}
    o.write('  <plate>\n')
    o.write('    <metadata key="plater_id" value="1"/>\n')
    o.write('    <metadata key="plater_name" value=""/>\n')
    o.write('    <metadata key="locked" value="false"/>\n')
    o.write('    <metadata key="filament_map_mode" value="Manual"/>\n')
    o.write('    <metadata key="filament_maps" value="%s"/>\n'
            % " ".join(str(fmap.get(s, EXTRUDER_MAIN)) for s in slots))
    o.write('    <metadata key="filament_volume_maps" value="%s"/>\n'
            % " ".join("0" for _ in slots))
    o.write('    <model_instance>\n')
    o.write(f'      <metadata key="object_id" value="{container_id}"/>\n')
    o.write('      <metadata key="instance_id" value="0"/>\n')
    o.write('    </model_instance>\n')
    o.write('  </plate>\n')
    # The assemble_item transform mirrors the build item's plate placement -
    # reference_x2d.3mf carries "1 0 0 0 1 0 0 0 1 128 128 0" in both places.
    o.write(f'  <assemble>\n   <assemble_item object_id="{container_id}" '
            'instance_id="0" transform="1 0 0 0 1 0 0 0 1 '
            f'{tvec[0]:g} {tvec[1]:g} {tvec[2]:g}" offset="0 0 0" />\n'
            '  </assemble>\n')
    o.write('</config>\n')
    return o.getvalue()


# ================================ GEOMETRY =================================
# Layout copied from real Bambu projects: the sub-meshes live in
# 3D/Objects/object_1.model and 3D/3dmodel.model holds one container object whose
# <component>s reference them by p:path (the 3MF "production" extension). This is
# the shape Studio writes itself, so it is the shape best tested on import.

MODEL_HDR = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<model unit="millimeter" xml:lang="en-US" '
    'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
    'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
    'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
    'requiredextensions="p">\n'
)
OBJECTS_PATH = "3D/Objects/object_1.model"


def mesh_xml(obj_id, mesh):
    o = io.StringIO()
    o.write(f'  <object id="{obj_id}" p:UUID="{uuid.uuid4()}" type="model">\n'
            '   <mesh>\n    <vertices>\n')
    for x, y, z in mesh.vertices:
        o.write(f'     <vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>\n')
    o.write('    </vertices>\n    <triangles>\n')
    for a, b, c in mesh.faces:
        o.write(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>\n')
    o.write('    </triangles>\n   </mesh>\n  </object>\n')
    return o.getvalue()


def build_geometry(parts, bed_centre, app_ver):
    """Return (objects_model_xml, root_model_xml, container_id)."""
    container_id = len(parts) + 1

    objs = io.StringIO()
    objs.write(MODEL_HDR)
    objs.write(' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n')
    for p in parts:
        objs.write(mesh_xml(p["id"], p["mesh"]))
    objs.write(' </resources>\n <build/>\n</model>\n')

    # Place the assembly: centre the combined footprint on the bed and drop it
    # to z=0. Doing it on the build item (not by moving vertices) keeps the parts
    # in their shared CAD coordinate system, which is what makes them line up.
    lo = [min(p["mesh"].bounds[0][i] for p in parts) for i in range(3)]
    hi = [max(p["mesh"].bounds[1][i] for p in parts) for i in range(3)]
    tx = bed_centre[0] - (lo[0] + hi[0]) / 2
    ty = bed_centre[1] - (lo[1] + hi[1]) / 2
    tz = -lo[2] + 0.0               # + 0.0 normalises a -0.0 away

    root = io.StringIO()
    root.write(MODEL_HDR)
    root.write(f' <metadata name="Application">BambuStudio-{app_ver}</metadata>\n')
    root.write(' <metadata name="BambuStudio:3mfVersion">1</metadata>\n')
    today = __import__("datetime").date.today().isoformat()
    root.write(f' <metadata name="CreationDate">{today}</metadata>\n')
    root.write(f' <metadata name="ModificationDate">{today}</metadata>\n')
    root.write(' <metadata name="Title"></metadata>\n')
    root.write(' <resources>\n')
    root.write(f'  <object id="{container_id}" p:UUID="{uuid.uuid4()}" type="model">\n'
               '   <components>\n')
    for p in parts:
        root.write(f'    <component p:path="/{OBJECTS_PATH}" objectid="{p["id"]}" '
                   f'p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>\n')
    root.write('   </components>\n  </object>\n </resources>\n')
    root.write(f' <build p:UUID="{uuid.uuid4()}">\n')
    root.write(f'  <item objectid="{container_id}" p:UUID="{uuid.uuid4()}" '
               f'transform="1 0 0 0 1 0 0 0 1 {tx:.6f} {ty:.6f} {tz:.6f}" printable="1"/>\n')
    root.write(' </build>\n</model>\n')
    return objs.getvalue(), root.getvalue(), container_id, (tx, ty, tz)


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
    ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
    ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
    ' <Default Extension="png" ContentType="image/png"/>\n'
    ' <Default Extension="gcode" ContentType="text/x.gcode"/>\n'
    '</Types>\n'
)
ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
    ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" '
    'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
    '</Relationships>\n'
)
# Every sub-model file must be declared here or Studio will not open it.
MODEL_RELS = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
    f' <Relationship Target="/{OBJECTS_PATH}" Id="rel-1" '
    'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
    '</Relationships>\n'
)


def slice_info(app_ver):
    """Bambu writes this in every project; it only records who produced it."""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n  <header>\n'
            '    <header_item key="X-BBL-Client-Type" value="slicer"/>\n'
            f'    <header_item key="X-BBL-Client-Version" value="{app_ver}"/>\n'
            '  </header>\n</config>\n')


# ================================ VERIFY ===================================

def verify(path, parts, cfg, blocks, container_id):
    """Re-open our own output and prove it says what we meant. Nothing here can
    prove Bambu Studio *likes* the file - only that it is internally consistent."""
    print("\n--- verification " + "-" * 58)
    ok = True

    def chk(label, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print(f"  [{'ok ' if cond else 'FAIL'}] {label}{(' : ' + detail) if detail else ''}")

    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        expected = {"[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model",
                    "3D/_rels/3dmodel.model.rels", OBJECTS_PATH,
                    "Metadata/project_settings.config",
                    "Metadata/model_settings.config", "Metadata/slice_info.config"}
        chk("zip members", names == expected,
            "missing " + str(sorted(expected - names)) if expected - names else
            f"{len(names)} entries")

        # -- project_settings.config parses and says what we set ---------------
        got = json.loads(z.read("Metadata/project_settings.config"))
        chk("project_settings.config parses as JSON", True, f"{len(got)} keys")
        for k in ("layer_height", "initial_layer_print_height", "sparse_infill_density",
                  "sparse_infill_pattern", "brim_type", "brim_width", "curr_bed_type"):
            chk(f"  {k}", got.get(k) == cfg[k], repr(got.get(k)))
        chk("  printer / process preset",
            got["printer_settings_id"] == PRINTER_PRESET
            and got["print_settings_id"] == PROCESS_PRESET,
            f"{got['printer_settings_id']} / {got['print_settings_id']}")
        chk("  filament presets", got["filament_settings_id"] == FILAMENT_PRESETS,
            str(got["filament_settings_id"]))
        chk("  filament_map_mode / filament_map",
            got["filament_map_mode"] == "Manual" and got["filament_map"] == cfg["filament_map"],
            f"{got['filament_map_mode']} {got['filament_map']} "
            f"(1=Direct Drive/MAIN, 2=Bowden/AUX)")

        n = len(FILAMENT_PRESETS)
        bad = [k for k, b in blocks.items() if len(got.get(k, [])) != b * n]
        chk("  filament arrays all sized n_filaments x block", not bad, str(bad[:5]))
        chk("  chamber_temperatures (PETG wants no chamber heating)",
            set(got.get("chamber_temperatures", [])) == {"0"},
            str(got.get("chamber_temperatures")))
        chk("  textured plate temps", True,
            f"bed {got.get('textured_plate_temp')} / first layer "
            f"{got.get('textured_plate_temp_initial_layer')}")
        chk("  nozzle temps per filament x variant", True,
            str(got.get("nozzle_temperature")))
        # Guards the sidecar-template trap described in apply_gcode_templates().
        chk("  machine G-code is the X2D flavour, not generic BBL",
            all("X2D" in got.get(k, "") for k in
                ("machine_start_gcode", "machine_end_gcode", "layer_change_gcode",
                 "change_filament_gcode", "time_lapse_gcode")),
            "all 5 machine G-code blocks mention X2D")

        # -- model_settings.config: the per-part assignment --------------------
        ms = etree.fromstring(z.read("Metadata/model_settings.config"))
        obj = ms.find("object")
        chk("model_settings.config parses as XML",
            obj is not None and obj.get("id") == str(container_id),
            f'object id={obj.get("id") if obj is not None else None}')
        seen = {}
        for part in obj.findall("part"):
            name = part.find('metadata[@key="name"]').get("value")
            ext = part.find('metadata[@key="extruder"]').get("value")
            seen[name] = int(ext)
        for p in parts:
            want = p["slot"]
            nozzle = "MAIN/direct-drive" if p["extruder"] == EXTRUDER_MAIN else "AUX/Bowden"
            chk(f'  part "{p["name"]}" -> filament {want}',
                seen.get(p["name"]) == want,
                f'got {seen.get(p["name"])}; nozzle {p["extruder"]} ({nozzle}), '
                f'{FILAMENT_PRESETS[want - 1]}')

        # -- geometry ----------------------------------------------------------
        NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        sub = etree.fromstring(z.read(OBJECTS_PATH))
        counts = {o.get("id"): (len(o.findall(".//m:vertex", NS)),
                                len(o.findall(".//m:triangle", NS)))
                  for o in sub.findall(".//m:object", NS)}
        for p in parts:
            v, t = counts.get(str(p["id"]), (0, 0))
            chk(f'  mesh {p["id"]} "{p["name"]}"',
                v == len(p["mesh"].vertices) and t == p["faces"],
                f"{v} verts / {t} tris")

        root = etree.fromstring(z.read("3D/3dmodel.model"))
        comps = root.findall(".//m:component", NS)
        chk("  root object references every sub-mesh", len(comps) == len(parts),
            f"{len(comps)} components")
        item = root.find(".//m:item", NS)
        chk("  build item present", item is not None,
            f'transform {item.get("transform") if item is not None else None}')

    print("  " + "-" * 60)
    print("  VERIFICATION " + ("PASSED" if ok else "FAILED"))
    return ok


# ================================= MAIN ====================================

def main():
    if len(sys.argv) < 3 or any("=" not in s for s in sys.argv[2:]):
        sys.exit(__doc__)
    out, specs = sys.argv[1], sys.argv[2:]

    idx, bundle_version = profile_index()
    app_ver = studio_version()
    print(f"Bambu Studio {app_ver}, BBL profile bundle {bundle_version}")
    print(f"printer  : {PRINTER_PRESET}")
    print(f"process  : {PROCESS_PRESET}")
    for i, f in enumerate(FILAMENT_PRESETS, 1):
        nozzle = [e for _, s, e in PART_RULES if s == i]
        tag = ("MAIN/direct-drive" if nozzle and nozzle[0] == EXTRUDER_MAIN
               else "AUX/Bowden") if nozzle else "?"
        print(f"filament {i}: {f}   -> extruder {nozzle[0] if nozzle else '?'} ({tag})")

    parts = []
    for i, spec in enumerate(specs, start=1):
        name, src = spec.split("=", 1)
        mesh = trimesh.load(src, process=True)     # welds duplicate STL vertices
        mesh.remove_unreferenced_vertices()
        slot, ext = DEFAULT_SLOT, EXTRUDER_MAIN
        for token, s, e in PART_RULES:
            if token.lower() in name.lower():
                slot, ext = s, e
                break
        else:
            print(f"  WARNING: '{name}' matches no rule in PART_RULES; "
                  f"defaulting to filament {DEFAULT_SLOT}")
        if not mesh.is_watertight:
            print(f"  WARNING: {name} is not watertight - check the source mesh")
        parts.append({"id": i, "name": name, "src": src, "mesh": mesh,
                      "faces": len(mesh.faces), "slot": slot, "extruder": ext})
        print(f"  {name}: {len(mesh.vertices)} verts, {len(mesh.faces)} tris, "
              f"watertight={mesh.is_watertight} -> filament {slot}, extruder {ext}")

    cfg, blocks, _ = build_project_settings(idx, bundle_version)

    # Bed centre from the machine profile's printable_area corners ("0x0",
    # "256x0", ...), so this follows the printer rather than a hard-coded 256.
    corners = [tuple(float(v) for v in c.strip().split("x"))
               for c in flatten(idx, PRINTER_PRESET)["printable_area"]]
    bed_centre = (sum(c[0] for c in corners) / len(corners),
                  sum(c[1] for c in corners) / len(corners))

    objs_xml, root_xml, container_id, tvec = build_geometry(parts, bed_centre, app_ver)
    model_settings = build_model_settings(parts, container_id, tvec)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("3D/3dmodel.model", root_xml)
        z.writestr("3D/_rels/3dmodel.model.rels", MODEL_RELS)
        z.writestr(OBJECTS_PATH, objs_xml)
        z.writestr("Metadata/project_settings.config",
                   json.dumps(cfg, indent=4, ensure_ascii=False))
        z.writestr("Metadata/model_settings.config", model_settings)
        z.writestr("Metadata/slice_info.config", slice_info(app_ver))

    print(f"\nwrote {out}  ({os.path.getsize(out)} bytes)")
    print(f"placed at bed centre {bed_centre[0]:.1f},{bed_centre[1]:.1f} "
          f"(build item translate {tvec[0]:.2f} {tvec[1]:.2f} {tvec[2]:.2f})")
    sys.exit(0 if verify(out, parts, cfg, blocks, container_id) else 1)


if __name__ == "__main__":
    main()
```


==========================================================================================
# APPENDIX — SOLO-MODE MONOLITH (for context; the team pipeline decomposes this)
==========================================================================================


<a id="skills__3d-modeling__SKILL_md"></a>

------------------------------------------------------------------------------------------
### FILE: `skills/3d-modeling/SKILL.md`  (144 lines)
------------------------------------------------------------------------------------------

---
name: 3d-modeling
description: Design 3D-printable parts with an FDM-aware workflow, using FreeCAD (via the FreeCAD MCP, on the user's machine) or CadQuery (code-first, runs anywhere Python does) — new designs, replacement parts, adapters, enclosures, brackets, knobs, print-in-place mechanisms, multi-color prints. Use whenever the user wants to design or modify anything for 3D printing, fit a part to an existing object or commercial product (phone, battery, SBC, appliance), fix a print that failed or doesn't fit, pick materials or orientation, or export STL/STEP/3MF — even if they only say "model this" or "make me a replacement". Printing mistakes cost hours and filament; this workflow front-loads the checks that prevent them.
---

# 3D modeling for FDM printing

Printed parts fail for two reasons: real-world geometry you never noticed, and designs that
ignore how FDM deposits plastic. The phases below close both. Track the phases with your
task/todo tool so the user sees progress.

Read before acting (only what the task needs):
- [references/freecad-mcp-patterns.md](references/freecad-mcp-patterns.md) — FreeCAD backend: when to pick it + tested code patterns
- [references/cadquery-patterns.md](references/cadquery-patterns.md) — CadQuery backend: when to pick it + tested code patterns
- [references/fdm-design.md](references/fdm-design.md) — before design decisions (indexed: printability, orientation, supports, fits, colors, materials, production rules)
- [references/mechanisms.md](references/mechanisms.md) — hinges, printed springs, flexures, magnets, pins
- [references/materials.md](references/materials.md) — filament picks, drying temps, support-interface pairings
- [references/troubleshooting.md](references/troubleshooting.md) — print-quality symptom → cause → fix, calibration order
- [references/printers.md](references/printers.md) — the user's machine, before slicing advice
- [references/bambu-3mf-authoring.md](references/bambu-3mf-authoring.md) — Phase 5 only: authoring a print-ready Bambu *project* 3MF (settings baked in, per-part filament), not bare geometry

## Phase 0 — Choose the backend

Two backends, one workflow. Pick once per part; never mix mid-part.

| | **FreeCAD** (MCP, user's desktop) | **CadQuery** (pip, this environment) |
|---|---|---|
| Pros | Parametric FCStd the user can open and edit; Params spreadsheet = one-cell fit fixes; GUI renders; outputs save directly to the user's disk | Runs anywhere Python does — no desktop dependency; cheap fast iteration; scriptable verification; headless previews |
| Cons | Needs desktop + FreeCAD + MCP addon running; every execute_code returns a ~10k-token screenshot (plan ≤8 chunks/job); one instance — jobs serialize | User edits a .py, not a GUI document; OCC pitfalls (fillet corruption, volume misreport — see patterns); every output must be delivered explicitly |
| Pick when | User wants an editable document, works in FreeCAD, or the job is an iterate-on-physical-fit project on their machine | No desktop connected, batch/cloud work, quick parts, or cost matters |

Availability check first: FreeCAD → `list_documents` succeeds (else ask the user to open
FreeCAD with the MCP addon). CadQuery → `python3 -c "import cadquery"` (else
`pip install cadquery trimesh pyrender Pillow`). Neither available → say so; never guess
geometry offline.

## Phase 1 — Understand the job

Ask what's missing, in one round of pointed questions:

- **Function & loads**: what it does, forces and their directions.
- **Environment**: heat (car? dishwasher? outdoors?), UV, moisture → dictates material.
- **Fit**: mates with a real object? Then Phase 2 is mandatory.
- **Known product?** If the mating object is a commercial product (phone, battery,
  Raspberry Pi/SBC, power tool, appliance part — anything with a model number):
  **web-search its official specs/drawings now**, cross-check two sources, record every
  dimension with its source next to the parameter. Also search MakerWorld / Printables /
  GrabCAD for existing 3D models of the product or of parts that mate with it — a
  published model is documentation AND a candidate reference fixture (import as ref).
  Specs cover the product family; photos + calipers still confirm the user's actual unit
  and variant.
- **Printer**: exact model. If it's not in printers.md, research its specs, strengths, and
  quirks now and persist a profile (procedure in printers.md). Nozzle count and chamber
  change the design strategy, not just the slicing.
- **Filaments on hand; visible faces; text/logos; color count.**
- **Project folder on their disk? Print queue to update?** (needed in Phase 5 — ask now,
  or reuse what they've already mentioned).

Gate: every fit-critical dimension is measured, sourced, or an assumption the user approved.

## Phase 2 — Master the mating object (fit jobs)

- Photos arrive as chat uploads or in a connected folder; inspect by re-reading cropped
  regions. No photos of the mating object → ask before proceeding.
- Inventory **every** feature from photos at max zoom: steps, collars, rails, ribs, clips,
  buttons, windows, tapers, D-flats, threads. Molded parts are never bare cylinders.
- Pin each measurement to a named feature; calipers read a solid collar and two rails
  identically. Ambiguous number → ask, citing the photo. Request missing dims concretely:
  what to clamp, from where to where.
- **Every cutout and pocket needs a position, not just a size** — record each feature's
  center from a named datum (e.g. "camera window: 5.5 right of centerline, 36.7 below top
  edge"). A correctly-sized window in the wrong place is a failed part.
- Commercial counterparts are documentation — every window/slot/tab mates with something.
- **Model the mating object first** (ref part, same document/script). Render beside the
  photos, compare silhouettes, get user confirmation before designing. It becomes the
  Phase 4 test fixture.
- **Recreating a part from photos?** Use the render-over-photo overlay loop
  (cadquery-patterns.md §overlay): draw the model's boundaries on the photo and iterate
  until they hug the features — overlays resolve millimeters where side-by-side viewing
  only catches gross mismatch. Do the same against iso/side photos for heights and ramps.

## Phase 3 — Design and build

- Choose **print orientation before modeling** (checklist in fdm-design.md); it drives
  chamfers, support avoidance, layer-vs-load direction, and where color layers land.
- **Design slicer-agnostic**: function lives in CAD, never in slicer settings. Prefer
  compliant fits (flex walls, grip fins, chamfered mates) over precision fits.
- Every measured dimension and clearance is a named parameter with unit + provenance
  (FreeCAD: aliased Params spreadsheet cells; CadQuery: PARAMETERS section) — a failed
  fit must be a one-line fix. Clearances from fdm-design.md §4 (per-side); tight fits get
  a printed test coupon before the full part.
- Build in small verified steps; after each boolean print validity, volume, bbox, and
  look at a render/preview.

## Phase 4 — Verify before export (all seven)

Any check fails → fix the model (parameter first), then re-run all seven.
Run the dimensional checks on the **exported STL re-imported** (trimesh), not only the CAD
solid — export paths and late chamfer/repair steps can silently change geometry (a slot
once grew 3 mm between model and export).

1. **Interference**: part ∩ ref-part volume ≈ 0 at seated position.
2. **Insertion path**: seated-clear ≠ insertable — intersect at stepped travel offsets.
3. **Section render**: cut the assembly in half, render, show the user.
4. **Visual side-by-side**: render the part from the SAME viewpoints as the user's photos
   (or reference model) and compose them into one image — then actually look: same
   silhouette? same feature shapes? same counts? Numbers pass parts that look nothing
   like the target; this check exists because that happened. (Patterns files have
   same-camera render + side-by-side compose snippets.)
5. **Feature positions**: every cutout/pocket center re-measured from its named datum on
   the exported STL and compared to Phase 2's recorded value. Size alone never passes a
   placement check — and check handedness: a mirrored layout fits the numbers too.
6. **Measurement audit**: every measured number appears in geometry; unused number =
   erased feature — stop and ask.
7. **Printability + face audit**: overhangs, bridges, thin walls, missing chamfers —
   against the chosen orientation; cylindrical radii + bbox vs expected.

## Phase 5 — Deliver

**Where files live**: FreeCAD writes to the user's disk directly (confirm the project
folder in Phase 1). Anything built in this environment — CadQuery outputs, the 3MF,
notes — must be delivered explicitly: SendUserFile every output, and if the user has a
connected project folder, also commit there (`device_commit_files`). A file left here
never reaches the user.

Deliverables: parametric source (FCStd with RefPart hidden / model.py with ref_part not
exported), per-part STLs (CadQuery: tolerance=0.01, angularTolerance=0.1), combined STEP,
renders/previews, `print_notes.md` (geometry summary, which parameter fixes which fit,
orientation + why, material + why, slicer settings, honest risks). Multi-color: run
[scripts/make_3mf.py](scripts/make_3mf.py) → one 3MF, per-part filament assignment.
For a **print-ready Bambu project 3MF** (settings baked in, not just geometry), use
[scripts/make_bambu_3mf.py](scripts/make_bambu_3mf.py) and follow
[references/bambu-3mf-authoring.md](references/bambu-3mf-authoring.md): round-trip the slicer
for the machine's keys, verify structurally, ship an after-import checklist (you can't
confirm the slicer accepts it without launching it).
If the user keeps a print queue (ask once in Phase 1, or reuse what they've mentioned),
update it now and on every design change; otherwise skip.

Propose a cheap PLA fit test before the final material — an hour vs an evening.

**Failed print = data**: photo where it stopped, measure the travel, diff against the
model — the stopping point names the missed feature. Fix the ref part first, re-verify,
re-export, record the lesson in print_notes.md. Quality defects (adhesion, stringing,
shifts, banding) → diagnose with troubleshooting.md, not guesswork.
