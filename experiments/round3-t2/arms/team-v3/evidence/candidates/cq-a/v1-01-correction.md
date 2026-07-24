# V1-01 correction receipt

DESIGNER SELF-CHECK — NON-ACCEPTANCE

The grip extrusion was translated from its negative-normal source range to the same `Y=-8.000..+8.000 mm` native interval as the designated P_BED side land. This removes the prior unintended `Y=-24.000 mm` lower grip face.

Re-imported final STL `b2b13f8a953a7e11d00d0d503f830715843f2e8463da9c173099188e505059ca` has native bounds `[-42.000,-8.000,0.600]..[42.000,8.000,64.994]` mm. The verifier script asserts that native minimum Y equals `P_BED=-8.000 mm` before measuring all transformed downfaces. It records zero forbidden/non-P_BED downface area; the sole below-limit boundary is the plan-required 0.30-mm P_BED perimeter chamfer.

Reproduce:

```powershell
python .\model.py
python .\verify.py
```
