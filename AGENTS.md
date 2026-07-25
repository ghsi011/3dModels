# AGENTS.md — 3D printing projects

Guidance for AI agents working in this folder. (`CLAUDE.md` points here; this file is the
single source of truth.)

This repo tracks **my own 3D models and prints** — one folder per project. It is not where the
modeling skill is developed.

## Modeling skill

The `3d-modeling` skill (solo + the five-role team pipeline, the deterministic gates, and the
CAD tooling) lives in its own repository: **https://github.com/ghsi011/3d-modeling-skill**.
Install it from there; it is no longer vendored in this repo.

Use it for modeling and print-prep work here, and do not skip its verification checks:

- **Never export a fit-critical part without the skill's Phase 4 checks** (all seven:
  interference, insertion sweep over full travel, section render, visual side-by-side vs the
  photos/reference, feature positions measured from named datums, measurement audit,
  printability + face audit) — all run on the **exported STL re-imported**, not the in-memory
  model.
- **Before finalizing STL and before slicing, run the pre-print validation checklist**
  (DFAM/adhesion/overhang geometry, material calibration, exact final-3MF settings). It exists
  because CAD-clean parts still fail on the plate.
- **Recreating a part from photos**: use the render-over-photo overlay loop — draw the model's
  boundaries on the photo and iterate. Overlays catch millimetre errors that side-by-side
  viewing misses.
- **Known products** (phone, battery, SBC, appliance part): web-search the official specs and
  look for existing 3D models before measuring — then still confirm with photos + calipers.

Passing a software gate is necessary evidence, not proof of functional correctness. A gate can
tell you a contract is well-formed and a measured predicate holds under a stated transform; it
cannot tell you a part will fit, print, or survive its load.

## Printer

- **Bambu Lab X2D Combo** (dual nozzle, AMS 2 Pro, heated chamber). Key: model/TPU/CF on main
  nozzle, second colour/support on auxiliary; dual-nozzle jobs shrink the build volume to
  235.5×256×256. Full profile with quirks and recipes lives in the skill repo
  (`references/printers.md`).

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
  connected; files export directly into these folders. When it's offline, use a code-first
  backend (CadQuery/build123d) and deliver the files back here.
