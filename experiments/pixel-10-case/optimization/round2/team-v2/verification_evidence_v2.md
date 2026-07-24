# V2 fresh verifier evidence

All mesh-derived values below were recomputed from the changed, re-imported `pixel10_case.stl`; no candidate source geometry was used for checks 1--7.

| Item | Independent result |
|---|---|
| Candidate SHA-256 | `e90a7bce24efec848e01dcb8f9e06f76470c14ba0a73c00600211383a5feb2d1` |
| Reference SHA-256 | `81aafa0f715f84efc19cf6767152bb4b1f1412b9f219a504aa45e3ad23157a48` |
| STEP SHA-256 | `2ef37665c3722d6736136a939d1214100b27e01d6ec871ebd1cb6b510e380ddb` |
| Export integrity | One watertight STL component; Euler 2; bounds `[-2.100000,-1.545817,-1.300000]..[74.099998,154.899994,9.700000]` mm; volume `15870.198766 mm3`. Independently imported STEP is valid, one solid, re-exported watertight mesh with identical bounds and `15870.201174 mm3` volume. |
| Check 1 — seated interference | Manifold boolean of re-imported case and accepted re-imported reference: `0.000000000 mm3`. |
| Check 2 — insertion sweep | Manifold booleans at every `+Z` 1-mm increment from 0 through 16 mm: maximum forbidden intersection `0.000000000 mm3`. |
| Check 3 — section | Re-imported STL section at `Y=76.4`: 191 vertices; X `-2.100000..74.099998`, Z `-1.300000..9.700000` mm. `render_section.png` visibly shows the 1.30-mm rear wall, 0.30-mm rear gap, open +Z front, and rounded front lip/root. |
| Check 4 — same-view inspection | `render_exterior.png` was visually inspected. Its right panel is an S2 rear same-view composite: cyan candidate exterior and amber F14 aperture are aligned to the official diagram and explicitly limits the claim to relative layout. The left candidate rendering and other three supplied views were also inspected. No calibrated feature-position claim is made. |
| Check 5 — datum feature response/handedness | Re-imported mesh booleans give `0.000000000 mm3` material in each contract inner response zone: F14, F21, F05/F06, and F07/F08. Their locations remain rear, bottom, top, and right respectively; the layout is not mirrored. |
| Check 6 — F23 edge-radius audit | At the changed STL's F14 rear-aperture back edge (`z=-1.30`, straight portions near `y=107/150`), 3 directly sampled mesh adjacencies are exactly `90.0°`. This is a sharp exposed aperture/rim edge, not the G04-required `>=0.40 mm` rounded edge. |
| Check 7 — planned-orientation audit | Exact `R_y(-45°)` about L gives printer Z `-0.000000047..60.828321224` mm, 16 vertices within 0.05 mm of the bed, and `0.000000000 mm2` non-contact downward unsupported area. The print orientation is otherwise support-free, but the F23 sharp edge remains a G04 face-audit failure. |

Visual files inspected: `render_exterior.png`, `render_fit.png`, `render_section.png`, `render_print_orientation.png`, and `reference_rear_overlay.png`.
