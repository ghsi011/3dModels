# Real-part step-at-a-time skill optimization — log

Method: run one pipeline step (Sonnet, short) on a real part; score its output against real
ground truth (the user's final 3MF / a downloaded reference model); fix the skill as a **general
principle**; regression-check on other parts; move on. The skill never sees the 3MF answer —
only the evaluator (orchestrator) compares to it. Anti-overfit: every edit is a general
CAD/DFM/metrology principle, never a part-specific number.

## Spec fixes (pre-loop, from round-5 findings) — applied
- **Fit is a bounded band, not a floor** (metrologist + print-engineer slices, team contract).
- **Support-free is the default, not an absolute** (print-engineer slice, team contract).
Monolith untouched; team_preflight tests 5/5.

## Step ① — Metrology (Pixel 7 case, Sonnet)
Cost: ~18.7 min, 222,530 tokens, 82 tools (vs ~69 min for a full pipeline attempt).

Scored vs the phone reference model (155.61 × 73.56 × 11.46 mm), held out from the metrologist:

| Dimension | Metrology | Ground truth | Δ |
|---|---|---|---|
| Length | 155.6 | 155.61 | 0.0 |
| Width | 73.2 (flagged caliper under-read 71.9) | 73.56 | −0.36 |
| Total thickness | 8.7 body + 2.74 camera = 11.44 | 11.46 | 0.02 |

Findings:
- **Fit-band fix validated**: specified body walls snug–sliding **0.10–0.30 mm/side** (bounded
  class, min+max), windows loose 0.30–0.50 — not an open floor. The round-5 over-clearance
  failure is fixed at the source.
- Envelope accurate to <0.5 mm; flagged thickness conflict was benign (envelope matches to
  0.02 mm). High honesty: 8 open questions, excluded 2 bad caliper photos, marked DRAFT.
- **Skill edit (general):** added a measurement-placement principle to the metrologist slice —
  read envelope dims at flat regions; near-feature caliper reads (button/camera/corner) are
  biased and are evidence for the local feature, not the envelope. (Prevents the width/thickness
  near-feature confusion; general, not part-specific.)

## Experiment firewall (corrected — do not repeat the leak)
The user's `pixel7_high_detail_reference_model.stl` and `PixelCaseV4.3mf` are the **held-out
scoring ORACLE**, never agent inputs. The whole point of using already-solved parts is to check
each blind step against known truth. Agents get **photos + calipers + public specs only**; every
step runs blind and is scored by the orchestrator against the oracle. (An earlier attempt to
"use the downloaded model as the reference and skip blind-build" was a leak — discarded.)

## Step ② — Blind reference build (Pixel 7 phone, from metrology only) — DONE, PASS
Cost ~15 min, 167,916 tokens, 45 tools. Designer reconstructed the phone from `dimensions.md`
alone (verified: no photos/model/oracle read). Watertight solid, realistically stepped
(8.7 mm body + 2.74 mm camera bump).

Scored vs held-out oracle (footprint only — see caveat): length Δ0.01, width Δ0.24 (buttons
protrude 73.8 vs 73.56), thickness-envelope Δ0.02 mm. **Reconstruction chain validated.**

**Oracle-quality finding:** the downloaded `pixel7_high_detail_reference_model.stl` is
non-watertight with a **uniform 0→11.46 mm Z** at every slice (a coarse 2.5D shell), while the
blind build models the real stepped phone. Cross-check: the real case (3MF) is only 10.7 mm
thick externally, so the true body is ~8.7–9 mm — the blind reconstruction is *more* accurate
than the oracle. Consequence: score **footprint** against the reference model, but use the
**3MF (real case) cavity** as the fit/thickness oracle for the case steps.

**Open fit question (carried):** body 8.7 (spec) vs 9.5–9.8 (caliper) — matters for case fit;
honestly flagged by metrology, resolve at design.

No skill edit needed at step ② — the blind build performed well (realistic, assumption-flagged,
no invented numbers).

## Step ③ — Print plan (Pixel 7 case), blind — DONE, both fixes validated
Cost ~14 min, 166,622 tokens, 19 tools. Blind (metrology + own blind phone; oracle/3MF held out).
- **Fit-band fix validated at plan level:** all clearances carried as explicit per-side
  min-AND-max bands (snug 0.10–0.30, loose 0.30–0.50), never floors.
- **Support fix validated:** case naturally support-free in the chosen orientation; the single
  feature that forced a tradeoff (a ~38 mm button-window bridge > the 25 mm self-support limit)
  was resolved by an internal rib / a bounded SUPPORT_ALLOWED confined to the *nonfunctional*
  window opening — never distorting the fit or the exterior. Function-over-support-purity, applied.
- Sensible DFM: TPU 95A (impact), open-rim-down orientation so the camera boss self-supports,
  thickness kept at 8.7 nominal with OQ-01 open + a TPU coupon confirmation lane.

## Method upgrades (from external audit vs fastxyz/skill-optimizer) — adopted
1. **Provisional-until-cross-part-confirmed (overfitting gate).** A skill edit is PROVISIONAL
   until re-run, unchanged, on ≥1 *different* real part with no regression, then promoted. Our
   n=1 metrology edit (flat-region principle) and even the spec fixes are **provisional** until
   confirmed on the Garmin dock or broom holder.
2. **Per-step numeric accept criteria** (extend the round5-t2 locked-rule style to every step):
   improvement or neutrality on the scored metric + no regression on any exercised part.
3. **Coverage matrix** (below) — track slice × part × backend; fill empty cells before re-running
   the easiest part again.
4. **Blindness verification.** Transcript-grep is unavailable here (0-byte `.output` files);
   substitute = result-divergence from the oracle (documented per step) + strict input scoping in
   the commission. Flagged as weaker than a programmatic file-open check.

5. **Scorer/editor separation (adopted).** Grading a step produces numbers/defects ONLY (no
   fix). Any skill fix is proposed in a SEPARATE pass/context, so the grader can't rationalize a
   fix that just explains the one observed miss.
6. **Repeated trials on contested comparative calls (adopted).** Before locking a comparative
   decision (e.g. model A vs B), rerun the closer arm ≥1 more time and report the spread, not a
   single point (round-5 Opus attempt1-vs-2 proved real run-to-run variance).

Next per the provisional gate: **cross-part validation on the Garmin 7X dock** (steps ①–③,
scored vs its real 3MF + public Fenix 7X specs) to confirm the fit-band + support fixes hold and
nothing regresses, before promoting them or going deeper on Pixel.

### Coverage matrix (× = scored, ~ = running, · = pending)
| Step \ Part | Pixel 7 case | Garmin dock | Broom holder |
|---|---|---|---|
| ① metrology | × | × | × |
| ② blind reference | × | × | · |
| ③ print plan | × | × | · |
| ④ design | ~ | · | · |
| ⑤ verify / ⑥ prep | · | · | · |

Backend: CadQuery exercised (real-part loop); build123d validated (round-5); FreeCAD untested.

## Pixel ④ — Case design — DONE, NOT_READY (honest). Cost ~73 min, 398,972 tok, 130 tools.
- **Fit-band fix propagated to geometry ✅** — cavity clearance **0.20 mm/side on all 8 zones**
  (snug-band midpoint, in-band). Round-5's over-clearance failure fixed at the design level.
- Self-repaired a 9,200 mm² unsupported back → open bumper; relieved the camera; found+fixed a
  false-floor air gap and corner-fillet undercuts. Bulkier than real (14.6 vs 10.7 mm) due to a
  camera-protection boss (a valid but heavier choice than the real thin cut-out case).
- **Gate FAIL is largely a TOOL limitation (corroborates C-03):** support-audit sums the whole
  mesh (not per-rule); a legit **45° chamfer trips the −0.70710679 threshold** (~181 of 399 mm²).
  **New bug found: S-03 `float(None)` crash** on a JSON-`null` `max_out_of_limit_area_mm2`.
  Plus stale audit-STL hashes (STL changed after audits) → corroborates C-06 (Sprint 1A auto-hash).
- Design step ④ remains the hardest; the *fit* is now right, but support handling + tool fidelity
  need the Sprint 1 fixes (finiteness incl. `float(None)`, per-rule honesty, 45° threshold).

## Garmin ④ — Dock design (post-Sprint/H-03) — NOT_READY, but design logic strong
Cost ~89 min, 628k tokens, 290 tools. Blind (dock 3MF held out).
- **Support-fix + H-03 both worked at the geometry level:** bounded support confined to the lip's
  nonfunctional face (43.88/250 mm², PASS); seat fit **in-band** (52.0–52.4 for Ø51.75); and the
  retention lip correctly modeled as an **intended interference** (37.9 mm³ at-lip vs 0 mm³ general)
  — collision-vs-intended-contact distinguished, the exact review-C-05 capability. team_tools
  manifest validate PASS.
- **Only defect (NOT_READY): E-03** — an OCC fillet that would not compute at any radius; shipped
  sharp. Same class as Pixel ④'s corner-fillet conflicts.
- Scored vs real 3MF: fit/support/retention correct, but **over-sized** (100×99.5 / 163 cm³ vs
  74.7×65.4 / 98 cm³) — partly because it enlarged the base to route around the failing fillet.

## Design-step optimization #1 — fillet/OCC robustness (evidence: Garmin E-03 + Pixel corners)
Recurring design-step failure = a fillet OCC won't compute at any radius (lip/thin/post-boolean
edges). Added a **general fallback ladder** to `cadquery-patterns.md`: fillet-before-boolean →
one-edge-at-a-time + smaller radius → **substitute a chamfer** (OCC-robust, equal hand-feel) →
last resort **declare `allowed_sharp` with a reason** (never an undeclared sharp edge). This also
attacks the bulk (don't distort the part to dodge a fillet). Multi-part evidenced, general
principle; **validate on the next design run.** Broom ② = clean Ø30 reference (trivial).

## Garmin ① — Metrology (cross-part validation) — DONE, PASS + fixes PROMOTED
Cost ~13.6 min, 201,234 tokens, 46 tools. Blind (photos+calipers+specs; dock 3MF held out —
result-divergence confirms: it produced 51.75 mm, not the dock's seat number).
- **Fit-band fix held on a 2nd part:** case fit specified snug–sliding **0.10–0.30 mm/side**
  (explicit min–max, not a floor).
- **Flat-region fix held:** rejected a 56.8 mm over-the-buttons read, kept it as button
  protrusion, took the flat-bezel 51.7/51.8 → **51.75 mm** case as nominal.
- **Evidence discipline:** correctly overrode the orchestrator's wrong "~47 mm" hint by evidence
  rank (didn't average), logged as OQ-06. My hint was corrected mid-run via SendMessage.
- Honest: flagged the missing caseback charge-contact photo (OQ-01, blocking for the dock's
  charging interface) and no seating-angle evidence.

**Anti-overfit gate satisfied → the fit-band and flat-region metrology fixes are PROMOTED from
provisional to permanent** (validated on Pixel + Garmin, two different part types, no regression).
Broom ① (grip fit) will add a 3rd datapoint.

**Oracle-validity check (user request):** the user's watch measures **51.75 mm → Fenix 7X**,
matching the ~51 mm "7X" dock (ring seat ≈50.8 mm, outer 59.6 mm). Confirmed valid oracle.

## Broom ① — Metrology (3rd-part cross-validation, different fit TYPE) — DONE, PASS
Cost ~8.7 min, 117,645 tokens, 27 tools. Blind (single stick photo only).
- Correctly identified **Ø30 mm dowel** but honestly flagged **no caliper/scale in the photo**
  → 30 mm is D-confidence (from the brief), not a fabricated measurement.
- **Fit-band fix generalized to an INTERFERENCE/grip fit:** chose spring/grip fins (fin ID
  *under* the rod, per `fdm-design.md` grip-fin rule), expressed as a bounded band
  (0.6/1.0/1.4 mm diametral interference; fin-tip ID 28.6–29.4 mm) — not a floor.
- So "bounded band, not a floor" now holds across clearance fits (phone, watch) **and** an
  interference grip fit — genuine generalization, no part-specific tuning. No skill fix needed.

**Fit-band + flat-region fixes confirmed on 3 parts / 3 fit contexts, zero regressions.**

## Garmin ③ — Dock plan (the SUPPORT fix's hardest test) — DONE, PASS
Cost ~10.7 min, 140,777 tokens, 19 tools. Blind (metrology + blind watch; dock 3MF held out).
The dock has a **round-case retention lip = a genuine undercut in every orientation** — the real
test the naturally-support-free phone case couldn't provide.
- **Support fix validated:** refused pocket-down (would overhang the *functional* seat), printed
  install-pose (seat self-supporting), and confined a bounded `SUPPORT_ALLOWED` to the lip's
  **outward, nonfunctional** face only (≤180° arc, ≤250 mm²) — never the watch-contact face.
  Exact opposite of round-5's fit-distorting gable. "Support-free = default, not absolute;
  function wins" holds on a part that genuinely needs support.
- **Fit-band fix:** seat carried as a band (0.10–0.30 geometric + 0.05 PETG → 0.15–0.35 mm/side),
  both numbers + provenance.
- **Honest blocking:** charge/puck/contact geometry marked BLOCKED (G-09), no invented pads;
  deferred to metrology (OQ-01) → new plan revision. Also flagged that dimensions.md is still
  DRAFT (round-trip PENDING) as a process item rather than silently treating it as accepted.

**Deployment note (from this run):** the agent reported that invoking the `Skill` tool loaded the
globally-installed `anthropic-skills:3d-modeling` instead of this repo's role slice — it correctly
ignored that and used `skills/3d-print-engineer/SKILL.md` directly. So agents must **read the repo
slice files**, not `Skill`-invoke by name (name collision with the installed skill). Commissions
already point to repo paths; keep it that way.
**Resolved 2026-07 (verified):** the user uninstalled `anthropic-skills:3d-modeling`. Confirmed
absent from `installed_plugins.json`, the plugin cache, `~/.claude/skills/`, settings, and no
`3d-modeling` SKILL.md remains under `~/.claude` — contamination path closed. (Residual: a
separate `parametric-3d-printing` user skill remains, different name/purpose.) Still open for real
deployment: the *optimized repo skill* is not itself registered/invocable — `/3d-modeling` has no
target now; the repo version must be installed as the registered skill when optimization is done.
