# AGENTS.md — 3D printing projects

Guidance for AI agents working in this folder.

## Rules

- **Always use the `3d-freecad` skill** for any modeling or print-prep work here. Follow
  its phases and verification gates — no exporting fit-critical parts without the Phase 4
  checks (interference, insertion sweep, section render, measurement audit).
- **Printer: Bambu Lab X2D Combo** (dual nozzle, AMS 2 Pro, heated chamber). Machine
  profile with quirks and recipes lives in the skill's `references/printers.md` — consult
  it before giving slicing advice. Key: model/TPU/CF on main nozzle, second color/support
  on auxiliary; dual-nozzle jobs shrink build volume to 235.5×256×256.
- **Track every part in the Notion Print Queue** (database under the "3D Printing" page).
  Create the entry when design starts; update Status on every transition
  (To Design / Tweak → Ready to Print → Printing → Done), and keep Material, For, and the
  page body's dimensions current whenever the design changes.
- **One folder per project**, containing: parametric `.FCStd` (with hidden reference model
  of the mating object), per-part STLs, combined STEP, single-file multi-color 3MF,
  renders, and `print_notes.md`.
- **Commit to git** after every meaningful design iteration with a message that says what
  changed physically (e.g. "knob rev2: rail channels added to bore").

## Environment notes

- Parts often live in a car interior (Israeli summer): default to ASA/PETG, never PLA for
  final parts. PLA is for fit-test prints only.
- FreeCAD runs on this machine and is reachable via the FreeCAD MCP; files export directly
  into these folders.
