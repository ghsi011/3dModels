---
contract: print-plan
contract_version: 4
job_id: garmin-7x-charging-dock
revision: 1
owner: print-engineer
status: ACCEPTED
dimensions_revision: 1
reference_sha256: adcbff5b80a50107f830f8e4e3310aaa6cb0023639a40bf1e6c60cd7f6cc0c31
printer_profile: Bambu Lab X2D Combo w/ AMS 2 Pro / 0.4mm hardened main nozzle
updated_utc: 2026-07-24T23:00:00Z
---

# Print plan — Garmin Fenix 7X charging dock/cradle (pre-design pass)

Scope of this commission: **step ③, pre-design only.** No CAD has been produced or will be
produced under this document. This plan issues the manufacturing constraints the CAD
designer must build to. It is the DFM input to `CANDIDATE_BUILD`, not a candidate.

## Upstream gate note (process, not geometry)

`tests/eval/garmin-step1-metrology/dimensions.md` (revision 1) carries `status: DRAFT` in
its own frontmatter, and its own "Blind reference round trip" table records
`Round-trip verdict: PENDING` / `Accepted by metrologist: not applicable at this step`.
`tests/eval/garmin-step2-reference/reference_manifest.md` independently confirms the same
thing from the other side: the blind reference build is "PENDING metrologist round-trip."

Per `skills/3d-modeling/references/team-contracts-v4.md` §"Print engineer" inputs, this
role expects an **accepted** `dimensions.md` and reference envelope; per the state machine,
`PRE_DESIGN_PRINT_PLAN` formally follows a completed `REFERENCE_OVERLAY_REVIEW`. That gate
has not been closed as of this revision. This is a **process observation, not a request to
redesign geometry or a rejection of the metrology content** — every dimension in
`dimensions.md` still carries its own per-feature confidence grade (A/B/C/D) and the
reference build's re-measured STL matches its cited sheet values exactly (see
`reference_manifest.md`'s feature re-measurement table), so the numbers are usable on their
own stated confidence terms. I am proceeding on that basis because this commission was
explicitly dispatched now with these two files as the stated accepted inputs. I am not
waiving the gate itself: **flagged as a blocking item for the orchestrator/metrologist to
close** (formally revise `dimensions.md` to `status: ACCEPTED` with a completed round-trip
overlay) before or concurrently with candidate dispatch. See "Plan acceptance" below.

## Process

| Printer/material/nozzle | Layer | Environment/load | Rationale |
|---|---:|---|---|
| Bambu Lab X2D Combo; **PETG** final material; main nozzle only, 0.4mm hardened | 0.20 mm | Indoor nightstand/desk dock; static watch weight (~50 g) resting in the pocket; cyclic hand-insertion/removal load on the retention lip; snug radial fit (0.10–0.30 mm/side per `dimensions.md`) must hold its band over months, not just at first print | PLA creeps and is only ~57–60 °C HDT (`fdm-design.md` §7) — too soft a long-term guarantee for a snug fit that must not loosen with time/heat. ASA/ABS are indoor overkill (no outdoor/car/UV load stated) and add avoidable warp risk for no functional gain. PETG (HDT ~69/80 °C) is tough, easy on the X2D, and is the material `dimensions.md` itself anticipates: its Fit specification section explicitly notes "PETG/ABS printed cradles want +0.05 mm over a PLA-tuned value" — carried through below |

- Effective build volume: single-nozzle job; a bedside cradle is well inside 256×256×260mm
  (no dual-nozzle-envelope shrink applies since only the main nozzle is used).
- Coupon material: **PETG**, not the SKILL's PLA default — see "Coupon" section for why.
- Main/aux nozzle assignment: main only. No stated 2-color/2-material requirement; if the
  user later wants an accent-color base, the small-volume body could move to aux per
  `printers.md`'s near-zero-purge exploit, but that is a future plan revision, not assumed
  here.

## Model-to-printer transform

| Item | Exact value |
|---|---|
| Bed-contact landmark | `STAND_BASE_PLANE` — the single dominant flat face of the cradle's own base/foot (the surface that would rest on a nightstand/desk). The designer must build one planar face at the model's lowest installed-pose Z and use it as this landmark; the plan forbids splitting the base across multiple non-coplanar feet. |
| Bed normal (printer +Z) | Same as the stand's installed "up" direction — no flip. |
| Transform/rotation | **Identity relative to the installed/as-used pose**: 0° about printer X, 0° about printer Y, 0° about printer Z, beyond translating `STAND_BASE_PLANE` to printer Z=0 and centering the bbox in X/Y. Model the cradle directly in its as-installed orientation; do not add a print-only flip or lay-down. |
| Insertion/open direction | Along the pocket's central axis, tilted back from vertical by the assumed display angle (see below) — the watch travels down-and-back into the pocket. |
| Forbidden downward faces | Watch-contact seat wall (pocket bore, radial), pocket floor (caseback contact plane — also the future, currently-blocked charge-contact plane), and the retention lip's **inward/contact** face (the surface that presses the bezel). None of these three may ever be classified support-touchable, in this or any later plan revision, without a plan revision that explicitly re-justifies it. |

**Assumed display/tilt angle (flagged ASSUMPTION, not evidenced):** `dimensions.md` OQ-05
states explicitly that no photo shows the watch mounted or propped at any angle, and that
"any angle is a downstream design decision, not a metrology fact." I assume a **bounded
back-tilt range of 20–35° from vertical** (≈55–70° from horizontal) — an ordinary bedside/
desk charging-dock viewing angle — as a design envelope, not a single fabricated number.
The designer may pick any angle in this band; nothing in this plan depends on the exact
value inside it. **Why this choice doesn't need to be "solved before" orientation:** with
`STAND_BASE_PLANE` flat on the bed and the pocket opening up-and-forward at any angle in
this band, the pocket floor and bore wall stay self-supporting regardless of the exact
angle chosen — the only overhang this range produces is the retention lip described next,
which is handled by its own bounded support rule independent of the exact tilt value.

### Why this orientation over the alternatives (support reasoning)

A cradle that captures a round watch necessarily has a **retention lip** — a rim that
curls in over the bezel edge to keep the case seated (without it, the case is only held by
friction against the bore wall, which risks a slop-driven ejection during handling; the
`dimensions.md` fit band already treats over-clearance as a real failure mode, not just
under-clearance). That lip is a true undercut: no orientation of a round pocket with an
inward-curling rim eliminates it — printing pocket-down (upside-down) would remove the
lip's overhang but would put the base/foot, and the entire pocket floor and bore wall
(the actual functional seat), into overhang instead, which is strictly worse: it would
force the functional watch-contact seat itself onto a support-touched face, exactly what
`SKILL.md`'s "support-free is the default, not an absolute" guidance warns against ("never
require SELF_SUPPORT_REQUIRED where meeting it forces a functional surface... into a
distorting gable, steep taper, or over-wide cavity").

So: **installed-pose-on-bed wins.** It keeps the seat wall and pocket floor self-supporting
(their normals face generally up/outward, not down), and it localizes the one unavoidable
overhang — the retention lip — to a small, bounded, mostly-nonfunctional region: only the
lip's **inward-facing** surface actually touches the watch; its **outward/topside** surface
never contacts anything. That outward face is exactly where a bounded `SUPPORT_ALLOWED`
belongs (see "Supports and bridges" below). This is the honest tradeoff the commission
asked about: **the cradle geometry genuinely cannot be made 100% self-supporting without
compromising the functional seat**, so I am planning bounded support on the nonfunctional
side of the one unavoidable undercut rather than either (a) forcing a distorted/oversized
lip to dodge support, or (b) flipping the whole part and support-touching the actual seat.

## Geometry rules and phase scope

| ID | Rule | Numeric limit | Verification predicate | required_now | deferred_owner | final_gate |
|---|---|---:|---|---|---|---|
| G-01 | Watch-pocket radial fit band (bounded band, metrology-sourced + PETG adjustment) | Metrology geometric target: 0.10–0.30 mm/side (diametral 0.20–0.60 mm) around Ø51.75 mm nominal (`dimensions.md` M-001/M-003). **PETG-adjusted manufacturing band: 0.15–0.35 mm/side** (diametral 0.30–0.70 mm) — target band +0.05 mm/side per `fdm-design.md` §4 | Coupon ladder (below) + candidate check 1 (interference) + check 7 (bore diameter measurement on re-imported STL) | Coupon ladder must be printed and measured before candidate CAD is trusted for this rule; candidate STL bore re-measured at verification | none | Verifier must reject any candidate whose re-measured bore clearance falls outside 0.15–0.35 mm/side, regardless of nominal parameter value used in source |
| G-02 | Watch-pocket axial/depth clearance (print-engineer-set process value, **not** a `dimensions.md`-sourced dimension) | Pocket depth ≥ 14.9 mm (M-004, confidence B, OQ-02) + 0.15–0.35 mm axial clearance → target pocket depth 15.05–15.25 mm | Candidate section render + check 7 depth measurement | yes | none | Verifier confirms axial clearance stays in band; this is my own DFM budget, explicitly not a metrology fact — do not attribute it to the metrologist |
| G-03 | Minimum structural wall — pocket bore wall and retention lip cross-section | ≥1.6 mm (4 lines at 0.4 mm nozzle, matches `fdm-design.md` §2 structural default) | Check 7 wall-thickness audit on exported STL | yes | none | none |
| G-04 | Absolute minimum wall floor — non-structural shell elsewhere (base shell, cosmetic surfaces) | ≥0.8 mm (2× nozzle) | Check 7 wall-thickness audit | yes | none | none |
| G-05 | Bed-contact chamfer at `STAND_BASE_PLANE` perimeter | 0.2–0.4 mm at any edge that is itself dimension-critical (none identified yet); ≥1.0 mm elsewhere per `fdm-design.md` §9 production rule | Check 7 face/edge audit; see Edge E-01 | yes | none | none |
| G-06 | Button-axis keep-out relief (conditional) | If the cradle's pocket sidewall height (measured from the pocket floor) reaches the button/pusher Z-band along D2_BUTTON_AXIS, the wall must relieve to ≥Ø56.8 mm **only along that axis** (`dimensions.md` F-002 candidate response, M-002). If the sidewall stays below button height everywhere, no relief is required. | Candidate designer states final pocket wall height vs. button Z-band in `candidate_readiness.md`; verifier checks 5/7 confirm the relief (or its absence) is correct for the height actually built | Designer must self-certify wall-height-vs-button-band at candidate dispatch | none | Verifier rejects a candidate that reaches button height without the Ø56.8 mm relief |
| G-07 | Band/lug-axis keep-out relief (conditional) | Same logic as G-06, for D3_BAND_AXIS: if the pocket sidewall height reaches the band-exit Z (F-004/F-006, 26.0 mm band width, lug collars not independently measured), the wall must relieve enough that the flexible band is not pinched/trapped at the two lugs. A case-only cradle whose wall stays below band-exit height needs no response (`dimensions.md` F-004 candidate response). | Same as G-06 | Designer must self-certify wall-height-vs-band-exit at candidate dispatch | none | Verifier rejects a candidate that pinches the band without relief |
| G-08 | **Watch remains on the band during charging (design assumption, flagged)** | The cradle is sized around the case body only (Ø51.75 mm envelope); the band is assumed to stay on the watch and hang free outside the cradle body rather than being captured in a dedicated channel — ordinary bedside-dock use does not remove the band nightly | Visual/silhouette check at verification (check 4) confirms no band-capture channel was silently added or omitted without being asked for | none — informs G-07's applicability | orchestrator/user | If the user actually wants a band-off, case-only display posture, or a band-capture channel, that changes G-07 and requires a plan revision before candidate build |
| G-09 | **Charge-cable/puck alignment interface — BLOCKED pending OQ-01** | No numeric limit issued. See dedicated section below. | N/A this revision | **none — explicitly BLOCKED, not deferred-with-a-number** | metrologist (new `dimensions.md` revision resolving F-003/M-009), then print engineer (a plan revision that defines the charge-interface geometry rule once that data exists) | No charge-contact, pogo-pin keep-out, puck boss, cable channel, or any other charge-related geometry may enter candidate CAD, `candidate_readiness.md`, or verification under this plan revision. A candidate that adds any such geometry must be rejected as `CANDIDATE_GEOMETRY` scope violation regardless of how plausible it looks. |

## Edges

| Edge ID | Description | Exposure class | Radius/chamfer requirement |
|---|---|---|---|
| E-01 | `STAND_BASE_PLANE` bed-contact perimeter chamfer (elephant-foot immunity) — see G-05 | `BED_CONTACT` | 0.2–0.4 mm |
| E-02 | Pocket rim entry edge — guides the bezel during insertion; protects the watch's own finish from a sharp catch edge | `EXPOSED_FUNCTIONAL` | ≥0.5 mm |
| E-03 | Retention lip outer/topside edge — user-touched during removal, cosmetic/comfort only | `EXPOSED_COMFORT` | ≥1.0 mm, general production rounding per `fdm-design.md` §9 |
| E-04 | Retention lip boundary edge between the lip's inward functional contact face and its `S-01` support-touched topside face — must be clean and unmarked after support removal | `EXPOSED_FUNCTIONAL` | ≥0.3 mm |

## Supports and bridges

- **Support budget:** bounded, not zero. Zero-support is not achievable here without
  compromising the functional seat (see orientation reasoning above); the budget is
  deliberately small and confined to one nonfunctional region.
- **Allowed support regions:**
  - `S-01` — the retention lip's **outward/topside** face only (never its inward contact
    face). Classification: `SUPPORT_ALLOWED`. Bounded footprint budget for candidate
    geometry: **≤180° of pocket-rim arc, ≤3.5 mm radial extent beyond the bore, ≤250 mm²
    total area.** A candidate that needs a larger lip than this budget must return to this
    plan for a revision, not silently exceed it.
  - Allowed contact class: `PERMITTED_SUPPORT_CONTACT` on the lip's nonfunctional topside
    only.
- **Forbidden support regions:** watch-contact seat wall (pocket bore), pocket floor
  (caseback/future-charge-contact plane), retention lip's inward contact face, and — per
  G-09 — the entire, currently unbuilt, charge-interface region.
- **Maximum unsupported bridge:** 5 mm pristine per `fdm-design.md` §1; the pocket floor
  itself, once designed, is expected to be a supported/solid disc printed near the bed
  plane at this orientation, not a bridge, so this limit is a backstop, not an expected
  condition.
- **Designed-support requirement:** the lip's overhang must not be met by widening the
  lip's radial reach or flattening the tilt angle to dodge support — per the orientation
  reasoning above, that would be exactly the "distort the seat/stand angle to avoid
  support" tradeoff the skill instructs against. `SUPPORT_ALLOWED` on the topside is the
  correct response, not a geometry compromise.
- No other region may be added as `SUPPORT_ALLOWED` after the fact if it fails
  verification; an unplanned overhang the designer discovers requires a plan revision
  before candidate dispatch proceeds with it.

## Charge-cable/puck alignment interface — BLOCKED (OQ-01)

`dimensions.md` F-003/M-009 states plainly: the caseback charge-contact pad's location,
pin pattern/spacing, and the OEM charging cable's clip engagement geometry are **UNKNOWN**
— no caseback photo exists in the 11-photo evidence set, and the only supporting source
(S-14) is generic Garmin-family "4 gold-plated pins" knowledge with no geometry. The
`reference_manifest.md` blind build correspondingly builds a **plain flat caseback**,
deliberately not modeling any contact geometry, and calls this "the single most important
limitation of this file."

I am carrying that same discipline into this print plan: **I will not invent a pad
location, pin spacing, pocket, boss, or cable channel.** Doing so would produce a plan that
*looks* complete but silently commits the candidate designer to a fabricated charging
interface — worse than an honest gap, because a wrong guess here is a guaranteed field
failure (the watch simply won't charge) dressed up as a pass.

**What this plan authorizes instead:**
- The watch-capture cradle (pocket, seat, retention lip, base/stand) is planned fully per
  the geometry rules above and is authorized for candidate CAD this revision.
- The pocket floor may be built as a plain, flat, uncommitted surface (matching the
  reference model's plain caseback) — a legitimate placeholder for "we don't know what
  goes here yet," not a claim that no contacts exist.
- No feature anywhere in the candidate may be shaped, bossed, drilled, or channeled in a
  way that presumes where the contacts or a cable will sit. In particular, do not center a
  "cable pass-through" on the case center by default — that is itself an unapproved
  assumption about geometry that a real OEM puck/clip would need to clear.
- G-09 (above) freezes this as the exact required_now / deferred_owner / final_gate
  triple: not ready now, owned next by the metrologist (new caseback evidence or an
  explicit user-approved bounded placeholder per `dimensions.md` OQ-01's own approved-bound
  options), then by this role again for a plan revision.
- **This means the dock this plan authorizes is a watch-capture cradle, not yet a
  functioning charger.** That is the correct honest state per the commission brief, not a
  planning failure: a dock that reliably holds the watch, with the charging function
  explicitly and traceably unresolved, is more useful and more honest than one that
  invents contact geometry and fails silently on the shelf.

## Coupon

| Interfaces represented | Clearance lanes | Material | Pass/fail measurements |
|---|---|---|---|
| Watch-pocket radial bore fit (G-01) against the accepted reference case cylinder (Ø51.75 mm, `watch_reference.stl`) | 0.15 / 0.20 / 0.25 / 0.30 / 0.35 mm/side → target bore Ø52.05 / 52.15 / 52.25 / 52.35 / 52.45 mm | PETG (matches final material — see rationale below) | Each lane: gauge enters and seats by hand with light-to-moderate, tool-free force (snug–sliding class per `fdm-design.md` §4); holds position without falling out when inverted; caliper-measured actual clearance falls within 0.15–0.35 mm/side. Reject lanes outside that band even if they "feel" fine by hand. |

**Scope of this pre-design coupon (per `SKILL.md`'s pre-design checklist item 6, "define
the fit coupon region and pass/fail measurements before the designer begins"):** this
coupon is a **standalone fixture**, buildable now because the case geometry (Ø51.75 ×
14.9 mm, `watch_reference.stl`) is already accepted, independent of the not-yet-designed
cradle shape. It is a five-lane arc ladder (≈90° arc segments, each at G-03's planned
1.6 mm wall thickness and G-02's planned pocket depth) plus a printed **Ø51.75 mm gauge
cylinder** (sliced directly from the accepted reference model) to stand in for the
physical watch when it is not on hand for testing — the real watch is the primary go/no-go
article whenever available; the printed gauge is the documented fallback, not a
replacement of choice.

**Why PETG, not the skill's PLA default:** the post-verification checklist's PLA-coupon
default is explicitly conditioned on "when it does not invalidate shrink/thermal
behavior." Here it would: the entire accepted fit band (0.10–0.30 mm/side geometric,
0.15–0.35 mm/side manufacturing) is narrow enough that PETG's own noted +0.05 mm/side
material offset is 25–33% of the band width. A PLA coupon would validate a different
material's shrink/friction behavior at exactly the tolerance scale where that difference
matters most. PETG coupon lanes test the real production condition.

**What this coupon does not cover (deferred to post-verification, once real candidate
geometry exists):** the retention lip's `S-01` support-contact quality (clean release,
no witness marks on the inward contact face) and the axial/depth fit (G-02) both require
actual candidate geometry to test meaningfully and belong to the post-verification pass's
"actual mating-region coupon extracted from the accepted candidate" per `SKILL.md`'s
post-verification checklist items 2 and 4 (native slicer support-contact evidence for every
`SUPPORT_ALLOWED` footprint). This plan defines that requirement now so the post-verification
commission does not have to invent it, but does not attempt to execute it against geometry
that does not yet exist.

## Final-prep placeholders

- Slicer profile: 0.20 mm standard PETG profile on X2D main nozzle; finalize exact
  temperature/fan/flow after the coupon print, not guessed here.
- Walls/top-bottom/infill: 4 walls minimum around the pocket/seat/lip region (satisfies
  G-03's 1.6 mm via wall count, not a thin single-perimeter shell), 5 top/bottom, 30–40%
  gyroid elsewhere per `fdm-design.md` §2 structural default — perimeters, not infill,
  carry the load here.
- Drying/preparation: PETG 4–6 h @ 65–70 °C before printing; AMS/dry-box storage between
  prints given PETG's moisture sensitivity.
- Print order: PETG fit-band coupon (this plan) → measure/select the winning lane → full
  candidate print, once accepted, in PETG at the same settings.
- Field-test protocol: to be written by the post-verification pass against the actual
  accepted candidate; must include a documented number of insert/remove cycles and a
  recheck of the bore clearance afterward (creep/wear check), since PETG's long-term
  behavior under repeated snug insertion is exactly what motivated the material choice.
- Bambu after-import checks: orientation matches `STAND_BASE_PLANE` at Z=0 with the
  assumed tilt band intact, main-nozzle-only assignment, no supports auto-generated on the
  seat/floor/lip-inward faces, only the bounded `S-01` lip-topside region shows planned
  support.

## Plan acceptance

- **Blocking items for candidate CAD of the watch-capture cradle:** none. G-01 through
  G-08 and the support disposition are fully specified and authorize candidate dispatch.
- **Blocking items for the charge-interface feature specifically:** G-09 blocks all
  charge-contact/puck/cable geometry until OQ-01 resolves (new caseback evidence or an
  explicit user-approved bounded placeholder) and this plan is revised.
- **Process flag for the orchestrator (not a geometry blocker):** `dimensions.md` revision
  1 is `status: DRAFT` with `Round-trip verdict: PENDING`. I am proceeding on its stated
  values as explicitly dispatched, but recommend the metrologist close the
  `REFERENCE_OVERLAY_REVIEW` gate (photo-overlay the accepted `watch_reference.stl` and
  revise `dimensions.md` to `ACCEPTED`) before this plan's candidate is treated as final —
  or that the orchestrator explicitly records accepting that risk if it chooses to proceed
  regardless.
- Accepted by print engineer: print-plan-garmin-7x-charging-dock-1
