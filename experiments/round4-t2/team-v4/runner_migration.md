---
contract: runner-migration-record
contract_version: 4
job_id: round4-t2-team-v4
durable_team: team-44ca6798 / round4-t2-v4-optimization
owner: orchestrator (main session)
created_utc: 2026-07-24T13:31:33Z
---

# Durable runner migration — stale-binding repair

This record repairs the stale active-runner binding for durable team
`team-44ca6798` (`round4-t2-v4-optimization`) and documents the substrate
migration for the D2→P2 resume. It is a **new** durable record; the existing
`.omo/teams/team-44ca6798/{team.json,guide.md}` state files are retained
unchanged (not hand-edited), per the continuation handoff's fallback clause.

## What was stale

- `team.json` member **A** (`V4 team arm`, task `round4_team_v4`, agent
  `/root/round4_team_v4`) is marked `status: active`, and team `status: active`.
- The prior runner bound to `/root/round4_team_v4` was a `gpt-5.6-terra` ("Terra")
  agent that hit a **platform usage limit at the very start of D2**. It reported
  no design and no D2 output; it left member A visually `active` even though the
  agent had terminated on the usage-limit error.
- This is an **infrastructure interruption, not a CAD design-correction loop** and
  not a successful or failed candidate commission. It must not count against the
  v4 adoption threshold of "zero verifier correction loops."

## Why the repair is a migration, not an in-tool rebind

- The installed team tooling is the OMO / LazyCodex CLI (`omo` →
  `oh-my-opencode`, sisyphuslabs/omo 4.17.1). Its team transport is
  `multi_agent_v2` native agents (`spawn_agent`/`send_message`/`followup_task`),
  which drive Codex / OpenCode / GPT models.
- Two facts make an in-tool rebind the wrong action here:
  1. The CLI exposes **no** `team`/`member`/`rebind` subcommand (verified via
     `oh-my-opencode --help`: only install, cleanup, run, doctor, boulder,
     ulw-loop, mcp, version). There is no safe, non-spawning state command to
     re-bind member A; its `run` path spawns model agents.
  2. The user directive for this resume is explicit: **use Claude Opus for every
     new specialist/subagent, not GPT.** Using the omo spawn path would launch a
     GPT/OpenCode agent, violating that directive.
- The handoff anticipated exactly this: "If Claude's agent system does not support
  that continuity, create a new, clearly named durable runner record but retain
  the existing state files and log the migration." That is this record.

## New runner binding (authoritative for the resume)

| Field | Value |
|---|---|
| Substrate | Claude Code Agent-tool subagents (fresh contexts) |
| Leader / thin orchestrator | Claude Code main session (writes no geometry) |
| D2 candidate designer | `3d-designer` subagent, Claude Opus, fresh context |
| O1 receipt validation | main session (orchestrator) re-runs `validate-receipts` |
| V1 independent verifier | `3d-verifier` subagent, Claude Opus, fresh context (no D2 conversation) |
| P2 final print prep | `3d-print-engineer` subagent, Claude Opus |
| Grader (member B) | fresh Claude Opus context, scoped to `experiments/round4-t2/grading`, only after arm freeze |
| Working checkout | `.claude/worktrees/3d-multi-agent-optimization-resume-f8dac6` on branch `claude/3d-multi-agent-optimization-resume-f8dac6` |
| Prior bound cwd (superseded) | `.claude/worktrees/3d-modeling-multi-agent-split-fd66c0` |

Each Claude subagent is an inherently fresh context that sees only its commission
prompt and the files it reads; this preserves the v4 invariants (designer ≠
verifier context, no hidden historical material) by construction, enforced by
scoped commissions and an explicit read-prohibition list.

## Model-continuity disclosure (deviation from preregistration)

- The round-4 preregistration specified `gpt-5.6-terra` for **every** specialist.
  M1/D1/M2/P1 were run under that model and are frozen/accepted (preserved, not
  re-run).
- Per the user's explicit resume directive, the **new** specialists D2, O1, V1, P2
  and the grader run on **Claude Opus** (Claude Code's current Opus, model id
  `claude-opus-4-8`). The requested "Opus 4.6" point release is not separately
  selectable in this environment; 4.8 is the current Opus and supersedes 4.6.
- This makes the frozen v4 arm a **disclosed mixed-model continuation**
  (Terra for M1–P1, Claude Opus 4.8 for D2–P2). It is a user-directed, disclosed
  deviation — not a silent change. The v4 adoption decision is therefore about the
  v4 **pipeline design** (five roles, file-only contracts, executable gates, blind
  overlay round trip, fresh independent verification, real coupon/DFM depth) with
  this model-continuity caveat recorded. No adoption threshold is relaxed.

## Retained state

- `.omo/teams/team-44ca6798/team.json` — retained unchanged.
- `.omo/teams/team-44ca6798/guide.md` — retained unchanged.
- A pointer copy of this record is placed in that team's `artifacts/` shared desk.
- M1/D1/M2/P1 artifacts and their hashes are preserved and re-verified (see
  `run_ledger.md` → Resume verification).
