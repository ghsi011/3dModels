# Pixel 10 case head-to-head

This is a quick, single-job comparison of:

- `arms/monolith`: one fresh Codex agent using the unchanged `3d-modeling` skill.
- `arms/team`: the new five-role file-contract pipeline, coordinated by one fresh Codex
  agent that dispatches dedicated role contexts.

Both arms use CadQuery because FreeCAD was occupied by another session. Both receive the
same brief and evidence, use `gpt-5.6-terra`, may research the same public sources, and may
not read the other arm. A fresh independent grader evaluates both after their output folders
are frozen.

This one case is directional, not a replacement for the proposed T1-T4 evaluation.
