# Printer profiles

One profile per machine the user owns. If the user's printer isn't here: research specs,
strengths, and community-reported quirks (official wiki + reviews + forums), use the
findings, then persist them: append the profile to this file in a writable copy of the
skill folder, zip that folder as `<name>.skill` (zip archive, folder at root), and
SendUserFile it so the user can click Save skill — edits to the installed copy alone do
not survive the session.

## Bambu Lab X2D (Combo w/ AMS 2 Pro) — researched 2026-07

**Specs**: 256×256×260 mm — shrinks to **235.5×256×256 in dual-nozzle jobs** (check wide
parts fit!). Enclosed; active chamber heat to 65 °C (Heat Mode) or Cool Mode for PLA/PETG.
2× hardened 0.4 nozzles (0.2/0.6/0.8 available), 300 °C max, bed 120 °C. Main nozzle:
direct drive, 40 mm³/s, flow-calibrated. **Auxiliary nozzle: Bowden-fed, ≤200 mm/s — no
TPU, no CF/abrasives, slightly waivier finish.** AMS 2 Pro: 4 slots, RFID, dries to 65 °C
(not while printing); no soft TPU through AMS. Ships with textured PEI only. No LiDAR.

**Exploit**: near-zero purge for 2-color/2-material — model/TPU/CF on **main**, second
color/support material on **auxiliary**. Chamber+bed+300 °C = reliable ABS/ASA/PA-CF/PC.
Tested support-interface winners per model material: materials.md §2 (short version:
Support-for-ABS for most nylons/ASA/ABS/PC-ABS, but ASA for PA6-CF; PETG for TPU).
Auto flow/motion/nozzle-offset calibration — trust it, but run offset cal with dry filament.

**Quirks**: dual-nozzle filament→nozzle assignment in Bambu Studio is buried — use
grouping mode "Custom" and verify the assignment preview before slicing (can't reassign
after; rearrange AMS slots instead). Ooze smearing the calibration pad = wet filament.
AI spaghetti detection hypersensitive (may pause on wisps). Early units: PTFE tube rubbing
lid, right-path buffer spring failures (fixed ~2026-06), AMS hub lever grinding — Bambu
replaces. Textured PEI adhesion weaker than smooth for some materials — brim tall ASA.

**Recipes**: ASA 240–255 °C / bed 90–100 / Heat Mode 60–65 / fan 0 / dry 4–6 h @80.
PA6-CF: main only, 260–270 / bed 95–110 / chamber 65 / dry 8–12 h @80 mandatory.
TPU: main nozzle, external spool, 40–60 mm/s.

Sources: store.bblcdn.com X2D spec PDF, wiki.bambulab.com dual-nozzles-slicing-filament-grouping,
techradar.com X2D review, notebookcheck.net X2D review, forum.bambulab.com X2D threads.
