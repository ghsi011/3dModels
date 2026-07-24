# D2 candidate commission — round-5 (tightened, shared by both model arms)

Both arms (Sonnet 5 and Opus) receive this identical commission; only the designer model and
the arm output folder differ. It exists to make the candidate build **converge fast and
persist as it goes**, so the independent verifier can pass first time.

## Identity and scope
You are a fresh, independent **candidate designer**. Work only in your assigned arm folder
(given at dispatch: `experiments/round5-t2/arm-d2-sonnet/` or `.../arm-d2-opus/`). You never
accept your own work. Read **only** the allowed inputs listed under "Contracts". Do **not**
read any other arm, any grading/scorer/test, prior rounds' arms, Pixel work, reports, other
teams' `.omo`, or the web. **Never touch FreeCAD.**

## Backend and the mandatory harness
- Author geometry with **build123d** using the isolated venv interpreter:
  `C:/Users/ghsi0/b123dv/Scripts/python.exe`.
- Run **every** build/measure script through the harness so nothing can hang:
  `python experiments/round5-t2/cad_runner.py --interp <interp> --script <file> --timeout 120 --mem-mb 4000 --label <name> --workdir <arm-folder>`
  It saves the source hash and kills the process tree on a 120 s / 4 GB breach. If a build
  hits the timeout, **fix the script** — never re-launch the same runaway.
- Measurement and the shared gates run with **system python** (`python`, which has
  trimesh/numpy/matplotlib + `skills/3d-modeling/scripts/team_preflight.py`). build123d exports
  are already confirmed to re-import cleanly in system trimesh/CadQuery.

## Persist-early (mandatory)
In your **first** working iteration, write `candidate_model.py` and export a first
`candidate_tool.stl` + `candidate_tool.step`, even if rough. Never iterate in memory without a
file on disk. If you cannot export within your first few build attempts, **stop and report the
blocker** — do not keep trying silently.

## Iteration cap (mandatory)
At most **3** self-repair iterations against the executable gates. After each change,
regenerate all exports and re-run the **full** edge + support-rule sets (not just the last
failure). If the gates still fail after 3 iterations, **stop** and report `NOT_READY` with the
exact failing predicate plus your best artifacts. Do not wander.

## Supplied method for the hard constraint (support-free channel)
The part prints on its side. The transform `[[1,0,0,0],[0,0,-1,0],[0,1,0,16],[0,0,0,1]]` sends
installed `Y=-16` (`P_BED`) to the bed and makes **installed +Y the build (+printer_Z)
direction**; so installed **-Y-facing** surfaces point **down** while printing. Support-free
means no facet with transformed normal `printer_Z <= -0.70710679` except the bed land. Build it
this way:
- Keep the capture **mouth open toward installed -Z** (→ +printer_Y, horizontal). Never roof it.
- Form **every** downward-facing surface — bar-cavity ceiling, handle-opening roof, relief and
  transition roofs — as a **self-supporting chamfer (≤45° from vertical) or a teardrop**, not a
  flat horizontal roof. Bevel the top of the cavity/openings at ≥45°.
- Any unavoidable flat bridge span ≤ **5.0 mm**.
- After every change run `team_preflight.py support-audit` for S-01..S-04; the out-of-limit
  area must be **0.000 mm²**. Use the audit to **locate** offending faces and re-bevel them —
  do not guess.
- `P_BED` = planar land at installed `Y=-16.000`, ≥ `20×10 mm`, with a `0.30 mm × 45°` chamfer;
  keep all functional geometry ≥ `0.50 mm` off printer `Z=0`.

## Parametrization skeleton (fill geometry, not scaffolding)
```python
# --- contract-derived named parameters (mm) ---
BAR_L, BAR_W, BAR_H = 62.0, 11.7, 24.0     # F02 mating bar envelope
CL_END, CL_SIDE, CL_TOP = 0.50, 0.30, 0.60 # G-02 min clearances (may increase, never reduce)
WALL = 1.20                                 # G-01 min wall (3 x 0.42 line)
CAP_CLEAR = 0.60                            # G-03 clearance to cap face (D0) outside F02
LEADIN_CH = 0.50                            # G-04 lead-in chamfer (<=45 deg)
GRIP_R, ROOT_R, MOUTH_R = 1.50, 0.80, 0.80 # E-01 comfort / E-02 root / E-03,E-04 functional
PBED_Y, PBED_CH = -16.000, 0.30            # P_BED plane + G-06 chamfer
# channel inner: X = BAR_L + 2*CL_END ; Y = BAR_W + 2*CL_SIDE ; Z engage >= BAR_H + CL_TOP
# tool outer = channel inner + 2*WALL, plus an exterior hand grip; mouth opens toward -Z
```
Compose: a capture body around the bar cavity (open bottom, -Z), a protective relief plane
≥ `CAP_CLEAR` above D0 outside F02, an exterior hand grip (comfort radius `GRIP_R`), the
`P_BED` land + chamfer, and self-supporting roofs per the method above.

## Contracts to obey (the only files you read for geometry)
- `experiments/round5-t2/inputs/dimensions.md` (M01–M07, F01–F05, datums D0–D3)
- `experiments/round5-t2/inputs/print_plan.md` (G-01..G-07, S-01..S-04, E-01..E-05, transform, coupon)
- `experiments/round5-t2/inputs/print_plan_checks.json` (exact edge/support ID sets — echo them exactly)
- `experiments/round5-t2/inputs/reference_manifest.md` + `reference_bar.stl`/`.step`/`reference_model.py` (accepted mating envelope) + `reference_*` views for the overlay
- Role + refs: `skills/3d-designer/SKILL.md`; `skills/3d-modeling/references/cadquery-patterns.md`
  (concepts — re-import, section, overlay, datum measurement — translate to build123d; author in
  build123d idioms), `skills/3d-modeling/references/fdm-design.md`,
  `skills/3d-modeling/references/team-contracts-v4.md` (`candidate_readiness.md`/`candidate_preflight.json`
  sections), `skills/3d-modeling/scripts/team_preflight.py`
- Allowed common inputs: `experiments/round3-t2/common/{brief.md,common_manifest.json,evidence/fixture_views.svg}`

## Required outputs (into your arm folder)
`candidate_model.py`; `candidate_tool.stl`; `candidate_tool.step`; `candidate_coupon.py` +
`candidate_coupon.stl` (the real functional engagement coupon per `print_plan.md` "Coupon" —
full 62 mm F02 X span, production Y width/clearance, ≥20 mm Z engagement, rigid hand tab; not a
peg/hole surrogate); matplotlib PNG renders (exterior, installed-coordinate mating **section**
proving the open architecture + clearances, **print-orientation** view showing `P_BED` as sole
plate face, candidate **overlay** vs the reference/fixture); `print_notes.md`;
`candidate_readiness.md` (marked `DESIGNER SELF-CHECK — NON-ACCEPTANCE`); `candidate_preflight.json`
(schema_version 4; `candidate_stl_sha256` of your STL; `print_plan_checks_sha256` of
`inputs/print_plan_checks.json`; `edges` = exactly E-01..E-05 with numeric `samples_mm` +
`method` + `evidence`; `support_rules` = exactly S-01..S-04 with `audit_path`);
`S-01..S-04-support-audit.json` (from `team_preflight.py support-audit`); and
`candidate_preflight_validation.json` (from `team_preflight.py validate-receipts`) which **must**
exit 0 / `PASS` before readiness may say `READY`.

Do not edit any `inputs/` contract. Only create files in your arm folder.

## Structured receipt (your return value — raw data, not chat)
1. **Scope proof** — every file you read (confirm no FreeCAD/web/forbidden reads).
2. **Result** — READY/NOT_READY; `candidate_preflight_validation.json` result; each support-audit result + out-of-limit area.
3. **Files** — each with sha256 + bytes.
4. **Key measurements** (re-imported STL) — bounds; cavity X/Y/Z clearances vs 62/11.7/24; cap-face clearance outside F02; `P_BED` plane (= Y −16.000) + area; min wall; E-01..E-05 sampled radii; supports-off.
5. **Iterations** — how many (≤3) and what each fixed; confirm `persisted_early`.
6. **Harness receipts** — the `*.run.json` elapsed/peak for your builds.
7. **Failures/limits** — honest; no unverified pass claims.
