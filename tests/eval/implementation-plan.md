# Green-lit implementation plan (revised)

Executes the approved subset of the external-review backlog (`external-review-backlog.md`).
Authoritative for what is being built now. Full triage/patch mapping stays in the backlog.

## Green-lit scope (approved)
1. **Sprint 1** in full (protect the experiment; remove confirmed false confidence).
2. **Sprint 1A** — a deliberately small deterministic *contract automation* layer (new).
3. **H-03** fit-ownership move, immediately after Sprint 1 + 1A pass.
4. Only the **cheapest, dependency-light** Sprint 2 slices after those pass.

**Not yet:** full motion/contact solver, native slicer integration, generalized workflow engine,
coupon generator, broad printer-profile system, autonomous dispatch/approval, visual grading,
photo feature-extraction, safety-critical auto-acceptance, auto-calibration from one print.

## Core principle (documented in the architecture)
> Agents own engineering decisions. Deterministic tools enforce contract structure, provenance,
> artifact identity, dependency freshness, resource limits, and repeatable measurements. Passing
> a software gate is necessary evidence, not proof of functional correctness.
Automate only tasks with defined inputs, objective pass/fail, low risk, frequent repetition, and
no visual/mechanical/design judgment.

## Pixel ④ sequencing constraint (hard)
Pixel ④ is running and uses `team_preflight.py` + reads the v4 contract. Per the directive,
experiment-touching edits are **experiment-protecting** and apply **only after Pixel ④ finishes**.
Therefore execution order is adapted:
- **Now (safe, net-new):** this plan revision + build **Sprint 1A** under `skills/3d-modeling/scripts/team_tools/` (touches no existing experiment file).
- **After Pixel ④ completes:** apply **Sprint 1** edits (gate fix + doc normativity) and their tests; then **H-03**; then re-test on ≥2 parts.
No files or runtime state used by the active run are modified until it finishes.

## Sprint 1 — files expected to change (applied AFTER Pixel ④)
| File | Change |
|---|---|
| `skills/3d-modeling/scripts/team_preflight.py` | reject non-finite/negative/malformed samples & thresholds (P-10); validate transforms are finite rigid (det≈+1, no shear/scale/reflection) (P-11); contain evidence paths (no `..`/abs/symlink; hash the file) (P-11); rename `support-audit` output/claim to a **downward-facing-surface / orientation screen** — never "supportability" (P-12). Backward-compatible for valid inputs. |
| `skills/3d-modeling/scripts/test_team_preflight.py` | add adversarial tests (list below); keep the 5 existing. |
| `skills/3d-modeling/references/team-contracts-v4.md` | header: **sole normative runtime contract**; the `support-audit` naming/claim update (P-01/P-12). |
| `skills/team-design.md` | top **normative-status notice** (non-normative/historical; v4 governs); mark v1 "Exact template" as historical (P-01). |
| `AGENTS.md` | point normative schema to `team-contracts-v4.md`; add **team v4 = guarded pilot** note (P-01/P-02); add the "agent judgment vs software enforcement" split. |

Adversarial tests (≥): NaN; +Inf; -Inf; empty samples; malformed numeric strings; singular
transform; non-rigid transform where rigidity required; `../` path traversal; absolute evidence
path; missing evidence file; unsupported contract version; stale upstream hash; duplicate
feature/datum/dimension/constraint IDs. General validation, **re-tested on ≥2 structurally
different parts**, not the known fixture.

## Sprint 1A — minimal contract automation (new, built NOW)
New package `skills/3d-modeling/scripts/team_tools/` with one CLI:
`python -m team_tools.contracts <validate|hash|status|render> <project>`
(run from `skills/3d-modeling/scripts/`, or via a thin wrapper).

1. **Canonical representation:** structured JSON is machine-authoritative for the 5 contracts
   (`job_state`, `dimensions`, `print_plan`, `verification_report`, `artifact_manifest`);
   Markdown is generated (with a "GENERATED — do not edit; regenerate with …" banner). Do not
   convert existing docs wholesale; provide the schema + generator so new/migrated contracts use it.
   Per contract: one schema, explicit `contract_version`, finite-number validation, enum
   validation, ID uniqueness, foreign-key validation across feature/datum/dimension/constraint/
   artifact/defect IDs, project-relative normalized paths, required-vs-optional, explicit
   unknown-field behavior, deterministic output ordering, git-stable Markdown.
2. **Hashes/binding:** compute SHA-256 (never trust agent-entered); record in a deterministic
   receipt; verify downstream inputs match bound revisions/hashes; report STALE/INVALIDATED;
   never silently update a stale binding.
3. **Receipt:** machine-readable; tool+schema version, job ID, validated paths, observed revisions,
   computed hashes, results, warning/error IDs, timestamp (injected, not `Date.now`), invocation.
   Must **not** claim geometric/manufacturing correctness.
4. **Minimal `artifact_manifest`:** job/candidate ID, declared units, per-artifact id/role/path/
   type/sha256/expected-components/bbox/source-revisions/optional-transform. Checks: exists;
   hash matches; finite values/transforms; units declared; bbox finite/positive; project-relative
   path; duplicate-ID reject; obvious 25.4× scale warn/block by confidence; STL/STEP bbox compare
   when both present; never mistake the mating reference for a printable deliverable. (No deep STEP
   topology compare yet.)
5. **Agent-facing summary:** compact status text (mode, contract revisions, artifact counts, stale
   deps, blocking errors, warnings), informational only, pointing to authoritative structured
   contracts + receipts — to cut re-reading/token use without adding an authority layer.

Dependencies: stdlib + already-present `trimesh`/`numpy` only (no new heavy deps). Property-based
tests where they add value (non-finite, transforms, paths, dup IDs, enums, hashes/mutation).

## H-03 — fit ownership → print engineer (after Sprint 1 + 1A)
Ownership: print engineer owns **fit strategy**; designer implements it geometrically; metrologist
owns measured mating geometry + uncertainty; verifier checks implementation + declared acceptance;
orchestrator routes failures only. "Fit strategy" explicitly spans clearance / transition /
interference / elastic contact / crush ribs / snap / retention / seals / threads / compliant
mechanisms / coupon-or-calibration. **No universal zero-interference rule.** Print plan declares
per interface: interface ID, fit type, intended contact state, allowed interference/clearance
range, motion path, material assumptions, coupon/calibration requirement, numeric/physical
acceptance method. Re-test on ≥2 parts: (1) a rigid sliding/seated fit; (2) intended-contact/
compliance/retention/interference.

## Then (cheap Sprint 2 slices only): complete manifest · unit/25.4× · raw-vs-normalized mesh
report · `cad_runner` resource governor (wall/mem/proc-tree/output/triangle/render/log caps,
temp dir, output allowlist, cleanup, failure receipt; **never silently reduce quality**) ·
risk-classification schema+gate. **Stop and report before the motion/contact engine.**

## Documentation change (with Sprint 1)
Architecture docs split **agent judgment** (photos, datums, geometry, fit/manufacturing strategy,
visual/physical evidence, accepting high-risk designs) from **software enforcement** (schema,
finite-number, hashes, revision binding, stale-state, path safety, manifest consistency, resource
limits, repeatable measurements/receipts), using the Core-principle wording above.

## Work procedure & stop point
Plan revised → show breakdown+files → Sprint 1 (post-Pixel④) → Sprint 1A (now) → full tests +
receipts → H-03 → re-test ≥2 parts → **STOP + completion report** before Sprint 2 motion work.
Re-ask only if a change would touch live Pixel ④, migrate/delete data, add a heavy dep, break
backward-compat intentionally, or broaden scope.
