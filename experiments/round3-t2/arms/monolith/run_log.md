# Round 3 T2 monolith run ledger

- UTC start: `2026-07-24T01:04:48.7719937Z`
- Monotonic start tick: `142868536047` at `10,000,000` ticks/second
- Contexts / commissions: `1` (`gpt-5.6-terra`)
- Backend: CadQuery 2.8.0; FreeCAD and web access were not used.
- Inputs consulted: the assigned common brief, fixture SVG, common manifest, unchanged solo skill, and its CadQuery/FDM/material/printer references.
- Token telemetry: `not exposed` (not estimated).
- Validation command: `python model.py; python verify.py`
- Re-imported STL validation: watertight tool and coupon; 62.70 x 12.40 x 24.50 mm engagement slot; 62.0 mm engagement length; zero seated and insertion-sweep bar intersection; 303.80 mm² of designed downward bridge surface, spanning 24.5 mm and requiring no supports.
- UTC finish: `2026-07-24T01:10:49.2461464Z`
- Monotonic finish tick: `146472506108`; elapsed `360.3970061` seconds.
- Final file footprint excluding caches: `12` files, `451351` bytes.

## SHA-256 output manifest

| File | SHA-256 |
|---|---|
| `model.py` | `8638352b1c16b8dbd14ce69d1f2b0bd8e218f33e5401f3d05e6d41c27db8088d` |
| `verify.py` | `75160f9b73c9b2b2e4350065212876b84021d039e6bcdf5fc2543fb336a2e922` |
| `filter_cap_tool.stl` | `cbdc85ee1ee848f7c0683bc002f260f83e33f0fdf3b7b56c96b995ec0d44098b` |
| `filter_cap_tool.step` | `b9354aa901057c66ecf2de3d795d023d87ae0bf21ea812d9f5106eb30bd1455a` |
| `bar_engagement_coupon.stl` | `06b5b2e2d950516215c8f089b58c1243352ed0b41abf88a975de2202f12ac853` |
| `verification.json` | `eed6e1d910f0c64a005d88208e1f4ce1dd068f1d11c8cda3ef2bcf72dd8956c4` |
| `print_notes.md` | `e51fc1d0dd4bdaa658af97a3f4da88d90198c30a2c19dc0376a157c18a923347` |
| `renders/exterior_isometric.png` | `aa865e3b191ed1ff28f11d49901ee3ed263902147e206dd34a3f4e0151c9c746` |
| `renders/installed_engagement.png` | `b50025cfd2b2741aa2e93190c36aff371434c197f74806c58637e7cee63003b4` |
| `renders/section.png` | `1b71564b75fc475491aac5fd509867d90479c870c488e73043e4ba4859be5004` |
| `renders/print_orientation.png` | `a685c07ba2b06abaa73e9c91b6f7e0b5355a79e5b91a403a219fe5840227d209` |
