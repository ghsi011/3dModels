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
