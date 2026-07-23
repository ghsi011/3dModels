# Frozen benchmark run log — monolith arm

- Agent/model: `gpt-5.6-terra`
- UTC start: `2026-07-23T21:51:00Z` (recorded from team commissioning interval)
- UTC end: `2026-07-23T21:59:48Z`
- Elapsed: approximately 8m 48s
- Backend: CadQuery 2.8.0 only. FreeCAD was not queried, opened, connected, or changed.
- Web research: 2 web tool calls covering the two official sources and the two benchmark-listed community-model leads. The supplied official evidence and fixed brief facts were used; no unverified third-party geometry was copied.
- Major known tool/command counts: at least 20 command/tool invocations, 5 visual image inspections, 3 CadQuery model runs (two strict), and 4 verification runs (one expected printability failure followed by corrected final passes).
- Token count: not exposed.

## Produced files

- `model.py`, parametric CadQuery source with centralized parameters and source/confidence data.
- `verify.py`, independent STL re-import verifier and render generator.
- `pixel10_case.stl`, final watertight case mesh.
- `pixel10_case.step`, combined single-solid STEP.
- `phone_reference.stl` and `case_section.stl`, verification fixtures.
- `render_exterior_isometric.png`, `render_phone_case_fit.png`, `render_section.png`, and `render_print_orientation.png`.
- `verification_report.json` and `print_notes.md`.

## Checks executed

1. CadQuery strict model run: success; all emitted STL meshes watertight.
2. Final `verify.py` on exported STL re-imports: overall pass.
3. Exported-STL bounds: 76.2 × 157.0 × 11.25 mm, matching design tolerance.
4. Seated fit and five-position insertion sweep: zero embedded reference vertices at all tested offsets.
5. Exported section STL: watertight.
6. Rendered and personally inspected four required STL-derived views.
7. Exported-STL printability face audit: 0.0 mm² unsupported downward-facing area.
8. STEP re-import: one valid solid.

The first verification attempt correctly detected 201.986 mm² of unsupported down-facing ceiling caused by access-cut ceilings. The model was changed so all access cuts exit the open screen side, then all checks were re-run and passed.
