# Sprint 1 + Sprint 1A — independent adversarial verification

Fresh reviewer, no prior context. Verdicts formed from the code, the diffs, and my own
adversarial repro (temp dirs, real round4 fixture, the example project). Nothing under
`experiments/` or the running experiment was modified; only this file was written.

## Verdict

| Scope | Verdict |
|---|---|
| Sprint 1 (gate hardening + doc normativity) | **PASS** |
| Sprint 1A (`team_tools` contract automation) | **PASS** |

**Real issues found: 0 correctness defects.** 3 non-blocking notes (scope hygiene, one
forward-looking gap for H-03, one "trust boundary" observation). No false-pass, no crash,
no doc contradiction survives.

## Command runs (all green)
- `python -m ruff check skills/3d-modeling/scripts` -> **All checks passed!**
- `python skills/3d-modeling/scripts/test_team_preflight.py` -> **33 tests OK**
- `(cd skills/3d-modeling/scripts && python -m team_tools.test_contracts)` -> **68 tests OK**

---

## Sprint 1 — findings

### R-01 NaN/non-finite false-pass — CLOSED (independently reproduced closed)
Built my own `validate-receipts` inputs over the **real** round4 STL+plan and tried to sneak a
PASS through `samples_mm`. Every garbage form FAILs (none sneaked a PASS):
NaN, +Inf, -Inf, `true` (bool), `null`, numeric string `"1.7"`, empty list, negative,
below-min, nested list, dict. The fix is `team_preflight._finite()` (rejects bool via the
`bool`-is-`int` subclass trap, rejects non-numeric, then `math.isfinite`), applied to every
sample and every numeric threshold. Root cause is correctly identified in the docstring:
`json.loads` turns the non-standard `NaN`/`Infinity` tokens into real floats, so a naive
`isinstance(x, float)` check was the hole.

### S-03 `float(None)` crash — FIXED, clean field-named error
`support_rules` with `max_out_of_limit_area_mm2: null` now yields a collected error
`"<rule>: max_out_of_limit_area_mm2 must be a finite number for SELF_SUPPORT_REQUIRED"`
(FAIL, no exception), and `support_audit` raises a `ValueError` naming both the rule id and
the field. The null-cap is only demanded for `SELF_SUPPORT_REQUIRED`; `SUPPORT_ALLOWED` may
legitimately leave it null (verified: that path PASSes). The `float()` call is correctly
guarded behind the disposition branch + `_finite` check.

### Transform validation (`is_finite_rigid`) — rejects everything it should
Verified directly and through `support_audit` + `validate_receipts`: identity accepted;
singular (det 0), reflected (det -1), scaled (R·Rᵀ≠I), sheared, NaN-entry, wrong-shape, and
non-matrix (`None`/string) all rejected with a field-named message. Checks are: 4x4, all
finite, last row `[0,0,0,1]`, orthonormal rotation (atol 1e-6), det ≈ +1.

### Path containment (`resolve_contained_path`) — rejects escapes
`../` traversal, absolute path, and missing file all FAIL with field-named errors. Uses
`os.path.realpath` (follows symlinks/junctions before the containment test) + `commonpath`,
with a cross-drive `ValueError` treated as an escape. Non-string / empty rejected.

### support-audit relabel — honest
Output `kind` is now `downward-facing-surface-screen` with an embedded `note` that it "does
NOT prove slicer supportability, bridgeability, or print success." The v4 contract
(§ lines ~284-290) repeats this and frames it as "evidence for the agent's supportability
judgment, never as that judgment itself." The CLI subcommand name `support-audit` is retained
only for backward compatibility (documented in `--help`). No output or doc still claims it
proves supportability.

### Regression — valid data still passes
- Geometry math (`transform_points` → cross → normals → out-of-limit area) is **byte-for-byte
  unchanged** by the Sprint 1 diff (confirmed via `git diff HEAD`). Sprint 1 only *added*
  validation guards + the relabel, so no geometric result can have shifted.
- Positive path confirmed: a bed-aligned box under identity transform → `support-audit` PASS
  (area 0.0); a well-formed readiness with in-range samples + matching hashes →
  `validate-receipts` PASS, errors `[]`.
- **Note (not a regression):** running `support-audit` on `round4-t2/team-v4/reference_bar.stl`
  under the plan's own declared matrix yields `out_of_limit_area = 1488 mm²` (FAIL for the
  `max=0` rules). This is because `reference_bar.stl` is the **reference** geometry, not a
  bed-aligned candidate, and the matrix translates model-Y→printer-Z+16 (bottom lands at
  z≈8, not the bed). Pre-existing behavior, unrelated to Sprint 1. Flag for the team only as
  a *data* question (does the round4 transform actually seat the candidate on the bed?), not a
  code finding — I did not touch the experiment.

### Doc consistency — no surviving contradiction
Two "source of truth" statements exist but at **different layers**, so they don't conflict:
- `AGENTS.md` line 4 "this file is the single source of truth" is about the *agent-guidance*
  hierarchy (CLAUDE.md → AGENTS.md).
- Runtime-contract authority is uniform: `AGENTS.md` (lines 23-26), `team-design.md` (top
  Normative-status notice), and `team-contracts-v4.md` (line 3) all name
  **`team-contracts-v4.md` as the sole normative runtime contract and gate schema**, with
  "where they disagree, v4 governs." `team-design.md` is explicitly marked historical/
  non-normative and its "Exact template" sections marked as an earlier revision.
- `AGENTS.md` adds a clean "Agent judgment vs software enforcement" section matching the plan's
  Core principle ("necessary evidence, not proof").

### Adversarial test suite
`test_team_preflight.py` grew 5 → 33 tests covering NaN/±Inf/empty/string/bool/negative/
min>max, null-cap (both dispositions), singular/reflected/scaled/sheared/NaN transforms,
`../`/absolute/missing evidence paths, wrong schema_version, stale STL hash, duplicate
edge/support ids. Independent of the impl; they pin the fixes as regressions.

---

## Sprint 1A — findings (`skills/3d-modeling/scripts/team_tools/`)

Package: CLI `contracts.py` (validate/hash/status/render/agent-summary) + `validators.py`
(5 contract validators) + `manifest_checks.py` + `common.py`/`schemas.py`/`project.py`/
`receipts.py`/`render.py`/`status.py`/`summary.py` + `examples/project_ok` + 68 tests.

### Adversarial `validate` probes — every one rejected (CLI, real receipts)
Mutated the passing example project one field at a time and ran `python -m team_tools.contracts
validate`:

| Attack | Result |
|---|---|
| NaN injected into a `print_plan` number | rc=1, overall FAIL, `NON_FINITE` |
| raw `Infinity` token in `dimensions` JSON | rc=1, FAIL, `NON_FINITE` |
| duplicate edge id | rc=1, FAIL, `DUPLICATE_ID` |
| broken FK `dimension.feature_id → F-NOPE` | rc=1, FAIL, `FK_MISSING` |
| escaped artifact `path: ../secret.stl` | rc=1, FAIL, `BAD_PATH` |
| wrong `contract_version` (3) | rc=1, FAIL, `UNSUPPORTED_CONTRACT_VERSION` |
| declared `sha256` ≠ computed | rc=1, FAIL, `HASH_MISMATCH` |

Finite validation is real and **recursive**: `project._load_one` runs `common.check_finite`
over the whole decoded structure at load, so a non-finite value is caught even where the
per-field type check would accept a `float`. (The naive-type-check gap I looked for is covered
by this second layer.)

### `status` — stale + invalidated both fire
- Bumped `dimensions.revision` → `status` reports `PRINT_PLAN STALE`, `VERIFICATION_REPORT
  STALE`, and two `ARTIFACT_MANIFEST STALE` rows (source_revisions binding), rc=1.
- Flipped one byte of `reference_bar.stl` → `PRINT_PLAN INVALIDATED` and
  `VERIFICATION_REPORT INVALIDATED` (`reference_sha256` bound-vs-current), rc=1.
- Read-only: it reports, never rewrites a binding (verified in code). Good.

### 25.4× unit-scale check — real
Declared an artifact bbox exactly 25.4× the re-imported STL's true extent (and fixed the
sha256 so `HASH_MISMATCH` wouldn't mask it): `validate` → overall FAIL with
`UNIT_SCALE_MISMATCH` (hard error, within 0.5% of an exact inch/mm ratio). A looser ratio
downgrades to a `POSSIBLE_UNIT_SCALE_MISMATCH` warning. Not a stub.

### Render determinism — byte-identical
Rendered all five contracts twice each: output is byte-for-byte identical, carries the
`<!-- GENERATED -- do not edit ... -->` banner, and field order is fixed by contract type
(not JSON key order), so upstream reordering can't create diff noise. `_cell` sorts dict keys.

### Receipts — honest + reproducible
`build_validate_receipt` carries tool+schema version, job id, validated paths, observed
revisions, recomputed sha256s, per-file + overall result, sorted warning/error ids, injected
timestamp (`resolve_timestamp`, env `TEAM_TOOLS_TIMESTAMP`, never wall-clock), invocation, and
an explicit **DISCLAIMER** that it "does NOT prove geometric or manufacturing correctness."
Hashes are always recomputed from bytes; declared hashes never trusted. Matches the plan's
receipt spec item-for-item. (`project_dir`/`argv` are absolute in the receipt — deterministic
for a fixed invocation but path-dependent across machines; fine, and separate from the
git-stable render output.)

### Other checks confirmed present and correct
- `mating_reference` artifact cannot be marked `printable_deliverable` (`MATING_REFERENCE_NOT_
  PRINTABLE`).
- bbox must be finite + positive extent per axis; component count vs `expected_components`;
  paired STL/STEP bbox compare (STEP load opportunistic — skipped, never failed, when no OCC
  backend). unknown-field policy = warn, never crash. verification_report enforces the seven
  checks on PASS and defects on REJECT; `fresh_context:false` flagged.

---

## Non-blocking notes (0 are correctness bugs)

1. **Scope hygiene — the working tree is not cleanly scoped to Sprint 1 + 1A.** Beyond the
   declared file list, uncommitted edits also touch:
   - `skills/3d-modeling/scripts/make_3mf.py` — cosmetic import split only (ruff E401 fix). It
     does **not** fix R-02 (that's Sprint 3, out of scope) — don't mistake its presence for an
     R-02 fix.
   - `skills/3d-metrologist/SKILL.md` and `skills/3d-print-engineer/SKILL.md` — fit-band
     ("bounded band, min AND max") and "support-free is default, not absolute" guidance. These
     are recent fit-optimization edits, and notably the **metrologist SKILL currently prescribes
     fit BANDS/classes** — a state that H-03 is explicitly meant to reverse. Recommend
     committing/segregating these before starting H-03 so the ownership move is a clean diff and
     the metrologist's fit-class authority is removed in one place.

2. **Forward-looking gap for H-03:** the per-interface fit declaration H-03 adds to the print
   plan has **no structured validator yet**. If H-03 lands as Markdown prose only, the new fit
   fields (fit_type, contact_state, interference/clearance min/max, coupon requirement,
   acceptance method) are unenforced. Recommend extending `validators.validate_print_plan` with
   an `interfaces` row validator (enum fit_type/contact_state, finite min≤max, required coupon
   flag) in the **same** change — otherwise the whole point of H-03 (declared, checkable fit
   intent) is lost.

3. **Trust-boundary observation (by design, now honestly labeled):** `validate-receipts`
   validates *contract consistency*, not ground-truth geometry — it trusts the agent-entered
   `samples_mm` edge radii and the agent-declared bbox. A truthfully-formatted but wrong
   measurement will PASS. This is exactly the "necessary evidence, not proof" principle and is
   now correctly documented, but reviewers/agents must not read a PASS as geometric proof.

---

## Decisions for the next sprint

### H-03 (fit ownership metrologist → print engineer) — SOUND, do it next, but pair with schema
- **Architecturally correct.** Fit strategy (clearance/interference/crush-rib/snap/press/
  thread/seal band) is a *manufacturing/process* decision bound to material, printer, and
  process — not a measurement. Metrologist = as-observed nominal geometry + uncertainty;
  print-engineer = fit class/band + intended contact state; designer implements; verifier
  checks the *declared* acceptance. Cleaner than today's split (metrologist currently owns the
  band — see note 1).
- **Risk of re-opening the just-validated fit-band change:** real but bounded. It edits four
  slices (metrologist loses band authority, print-engineer gains fit-strategy + per-interface
  declaration, designer, verifier) plus the contract schema. The danger is a part that passed
  under the metrologist-owned band behaving differently once the band is re-derived by the
  print-engineer. The plan's controls (≥2 re-test parts, scorer/editor separation, general
  edits not fixture-specific) are the right mitigations. **Add:** the structured validator from
  note 2, or the new fit contract is unchecked prose.
- **The ≥2 re-test parts should span the fit spectrum** (that's what "no universal
  zero-interference rule" is for), and be structurally different from the round4 bar so it's
  general, not overfit:
  1. a **rigid clearance fit** with a *moving/seated* interface (slip/sliding — e.g. lid-in-
     box or shaft-in-bore) — exercises the clearance-band + motion-path side;
  2. an **intended-contact fit** (interference/retention/compliance — e.g. snap-fit clip,
     press-fit boss, or crush-rib) — exercises the non-zero-interference + coupon side.
  Ensure ≥1 has a moving interface and ≥1 a compliant/retention interface.

### Cheap Sprint 2 slices — genuinely cheap vs hidden cost, and order
- **Unit / 25.4× check — already built in Sprint 1A** (`manifest_checks` fires
  `UNIT_SCALE_MISMATCH`, verified). Remaining work is only *wiring/adoption* as a hard gate in
  the live flow. Cheapest, effectively done. **Do first.**
- **Artifact-manifest completion — mostly built** (validator + fs/mesh checks + paired
  STL/STEP + unit-scale all present). "Completion" = adopt in the live contract set + generate
  for real jobs. **Hidden cost:** deeper STEP topology needs an OCC/cascadio backend (currently
  opportunistic-skip). Keep STEP shallow. **Second.**
- **Risk-classification gate (R0-R3)** — cheap in the `team_tools` sense: a validated enum +
  an orchestrator rule that blocks autonomous acceptance for high-consequence classes. Cost is
  mostly policy/wording; high safety value; independent of the fit work. **Third (or fold into
  H-03's orchestrator edits).**
- **Raw-vs-normalized mesh reporting + mutation log** — real correctness (makes the verifier's
  "exact exported STL" claim true). **Hidden cost:** every load site currently uses
  `process=True` (a normalization: vertex welding). Making raw-vs-normalized explicit means
  auditing `team_preflight.load_single_mesh` + `manifest_checks._load_mesh_bounds` together.
  **Fourth.**
- **`cad_runner` resource governor — NOT genuinely cheap** (backlog itself rates M-L). Proc-
  tree kill, memory caps, and "never silently reduce quality" are OS-specific (Windows here)
  and easy to get subtly wrong (orphaned children, false timeouts). **Do last, and split:**
  wall-time + mem + temp-dir + cleanup + failure-receipt first; proc-tree/triangle/render caps
  later. **Stop before the motion/contact engine (S2-3)** per the plan.

**Order:** H-03 (+ its print_plan validator) → unit-scale adoption → manifest adoption →
risk-classification gate → raw/normalized mesh + mutation log → resource governor (split).
