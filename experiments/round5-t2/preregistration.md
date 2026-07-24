# Round 5 preregistration — model-tiering + build123d pilot (T2 benchmark)

Locked before any candidate is built or graded. No threshold or decision rule below may be
changed after observing results. Token telemetry is not exposed and is never estimated.

## Purpose

Round 3 (team-v3, score 93) and the aborted round-4 Opus attempt showed the five-role
pipeline reaches quality but is **slow and expensive at the candidate stage (D2)** — the round-4
Opus D2 ran ~40 min and persisted nothing. This round isolates and tests the two levers that
matter for "speed *and* quality":

- **H1 (design model).** A fast model (Sonnet 5) can execute a *tightened* D2 candidate
  commission to a state that passes the executable gates **and** an independent Opus
  verification with **zero correction loops**, at materially lower wall-clock than Opus.
- **H2 (backend).** `build123d` (isolated venv) produces gate/grader-compatible B-rep output
  and converges at least as cleanly as the CadQuery incumbent on this part.
- **H3 (process).** The persist-early rule + iteration cap + supplied support-free method +
  the `cad_runner.py` timeout/memory/save-source harness prevent non-converging silent stalls.

## Fixed design (lean sweep)

Everything is held identical across arms except the **D2 designer model**:

| Held constant | Value |
|---|---|
| Backend | `build123d` 0.11.1 in isolated venv `C:\Users\ghsi0\b123dv` (system CadQuery untouched) |
| Frozen upstream inputs | round-4 accepted `dimensions.md` r2, reference (`reference_bar.stl` + manifest + model + views), `print_plan.md` r1, `print_plan_checks.json`, copied verbatim into `experiments/round5-t2/inputs/` |
| Commission | the tightened `commission_d2.md` (persist-early, ≤3 self-repair iterations, supplied support-free method + parametrization skeleton, run every CAD build through `cad_runner.py`) |
| Verifier | a **fresh Opus** V1 for both arms (verification model held strong — downgrading the verifier is a separate, later probe) |
| Common participant inputs | only `experiments/round3-t2/common/{brief.md,common_manifest.json,evidence/fixture_views.svg}` |

| Arm | D2 designer model | Output folder |
|---|---|---|
| **S** | Sonnet 5 (`claude-sonnet-5`) | `experiments/round5-t2/arm-d2-sonnet/` |
| **O** | Opus (`claude-opus-4-8`) | `experiments/round5-t2/arm-d2-opus/` |

The two arms run in parallel (separate folders; permitted for CadQuery/build123d candidates).
Upstream M1/D1/M2/P1 are **reused frozen**, so they are a shared constant, not a confound for
the D2-model comparison. P2 (final prep) and the grader run once on the adopted arm after the
decision, both on Sonnet 5 (P2) / independent Opus (grader).

## Frozen input hashes (working-tree bytes, as the runner/validator read them)

- `inputs/dimensions.md` `e4465a38255ca36c2f322b9cf49f13356528fdb672ff04daa8096b1d7426782d`
- `inputs/print_plan.md` `173dc41c7b812334ef82a27e1be782180d521284209ce41f8a29e6d45bee8e0a`
- `inputs/print_plan_checks.json` `6f146669b2c819d9b013c31d2e54b4c7a27eec8cec645e9614fcb5fcbdff0016`
- `inputs/reference_bar.stl` `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a`

(Text-file hashes are CRLF working-tree bytes; the LF git-blob equals the round-4 ledger hash.
`team_preflight.py` reads working-tree bytes, so per-arm `candidate_preflight.json` will bind
these exact values.)

## Metrics collected per arm (measured; tokens never estimated)

| Metric | How |
|---|---|
| `t_D2` | wall-clock D2 dispatch → READY (or abort), from orchestrator timestamps |
| `t_V1` | wall-clock V1 dispatch → verdict |
| `iterations_D2` | designer self-repair iterations (from readiness/receipt) |
| `persisted_early` | did `candidate_model.py` + a first STL appear within the first iteration? |
| `gates` | `candidate_preflight_validation.json` result + each `S-0X-support-audit.json` result |
| `V1_verdict` | PASS/REJECT + defects + `correction_loops` |
| `footprint` | delivered files / bytes |
| `quality_proxy` | hidden `experiments/scorer.py T2` (slot width 12.1–14.2, depth ≥23, length ≥58) + trimesh watertight/components + coupon integrity, in the installed frame |
| `backend_note` | build123d convergence/ergonomics vs CadQuery incumbent (qualitative) |

## Decision rules (locked)

- **D2 model.** Adopt **Sonnet 5 for D2** iff Arm S: (a) passes all executable gates, (b) its
  Opus V1 returns **PASS with zero correction loops**, (c) its `quality_proxy` passes all three
  T2 criticals, **and** (d) `t_D2(S) < t_D2(O)`. If Arm S fails any of {gates, V1 PASS,
  criticals} while Arm O passes them → **keep Opus for D2**. If both fully pass → adopt Sonnet 5
  for D2 and record the quality delta (if any) and the wall-clock saving.
- **Backend.** Adopt `build123d` iff both arms' exports pass the trimesh/CadQuery/scorer stack
  and neither shows a build123d-specific failure. (Smoke test already positive.)
- **Process.** Confirm the harness prevented stalls: no silent run exceeded the per-build
  timeout without the harness terminating it; `persisted_early` is true for both arms.

## Pre-declared model-tiering estimate (this round tests only the D2 cell)

| Stage | Estimated model | Tested here? |
|---|---|---|
| Orchestrator / O1 / docs | Sonnet 5 | — (orchestrator = main session) |
| M1, D1, M2, P1 | Sonnet 5 | no (reused frozen this round) |
| **D2 candidate** | **Opus (hypothesis: Sonnet 5 suffices)** | **yes** |
| **V1 verifier** | **Opus (strong)** | held constant strong; downgrade is a later probe |
| P2 final prep | Sonnet 5 | later |
| Grader | Sonnet 5 (Opus optional) | later |

## Integrity rules

Each D2/V1 is a fresh scoped context that reads **only** the frozen upstream inputs, its role
slice + slice-required references, and the three common participant inputs. It must not read:
any round-3/4/5 other arm or grading, any scorer/test, Pixel work, historical reports, other
teams' `.omo`, or web content. Designer ≠ verifier context. Both are **blind to the hidden
scorer bounds** (preserves the hidden-fit test). FreeCAD is prohibited (build123d/CadQuery
only; build123d in the isolated venv). Tokens are not exposed and never estimated.
