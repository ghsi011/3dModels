# Round 3 common brief — washer filter-cap tool

Design a one-piece hand tool that grips the raised cross-bar on the washer fluff-filter cap
shown in `evidence/fixture_views.svg`.

Participant-visible facts:

- the cap is approximately 63.0 mm diameter;
- the raised bar is 62.0 mm long, 11.7 mm wide, and 24.0 mm high above the cap face;
- the appliance-facing cap and bar must not be damaged;
- the tool must be comfortable to turn by hand and must not slip off during normal use;
- use Bambu Lab X2D constraints with a 0.4 mm nozzle;
- final material is PETG; a PLA fit coupon is allowed;
- the chosen print orientation must be support-free.

Use CadQuery only. Keep fit-driving values and clearance as named parameters.

Deliver:

- `model.py` and `verify.py`;
- one final tool STL and STEP;
- one fit-coupon STL generated from the real bar-engagement geometry;
- exterior/isometric, installed-engagement, section, and print-orientation renders;
- `print_notes.md`;
- a run ledger with start/end timestamps, contexts/commissions, output hashes, and explicit
  token telemetry status.

All dimensional, fit, and printability claims must be made on the exported STL re-imported,
not only on source or in-memory geometry.

Use only this common package, the skill assigned to your arm, CadQuery/Python, and your own
empty output directory. Do not read prior experiment outputs, the other arm, hidden scorers,
reference STLs/renders, tests, optimization grading, or historical reports. Do not use the
web. Do not access FreeCAD.
