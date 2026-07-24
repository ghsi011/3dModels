---
artifact: p2-tpu-multilane-coupon
revision: 1
owner: print-engineer
candidate_stl_sha256: 255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960
print_plan_revision: 4
material: dry TPU 95A
coupon_stl_sha256: ee4c43a818eb2b12d77517d8668e5c9c249c90fe4ff4aea8f08f58bbb7ea931c
---

# One joined multi-lane TPU coupon

`tpu_multilane_coupon.py` exports exactly one joined STL,
`tpu_multilane_coupon.stl`. It represents the actual cq-v2 **straight left
sidewall + rear wall + capture/lip** cross-section: 1.80 mm side rail, 1.30 mm
rear wall, and 1.10 mm proud capture height above the 8.60 mm phone thickness.
The lanes are 35.00 mm long in the straight phone-Y direction.

| Lane | Coupon X centre from datum (mm) | Per-side clearance (mm) | Rear clearance (mm) | CAD rear depth, exterior rear to seating plane (mm) | Result record |
|---|---:|---:|---:|---:|---|
| L20 | 0 | 0.20 | 0.20 | 1.50 | pending physical test |
| L25 | 12 | 0.25 | 0.25 | 1.55 | pending physical test |
| L30 | 24 | 0.30 | 0.30 | 1.60 | pending physical test |
| L35 | 36 | 0.35 | 0.35 | 1.65 | pending physical test |
| L40 | 48 | 0.40 | 0.40 | 1.70 | pending physical test |

Each lane has an 8.00 mm inboard rear-contact pad from the actual left-side
cavity datum. Its cavity-facing wall is at `X = -side clearance` relative to
the device left-side datum; its seating plane is at `Z = rear clearance`
relative to rear datum A. The five lanes share only a 1.00 mm-thick base below
their exterior rear faces and 2.00 mm-wide, 1.00 mm-thick bridges across the
inter-lane gaps. Those sacrificial joins do not touch a device and must not be
used for fit measurements.

## Export and structural evidence

```text
cd experiments/pixel-10-case/optimization/round2/team-v2
python tpu_multilane_coupon.py
python -c "import trimesh; m=trimesh.load_mesh('tpu_multilane_coupon.stl', process=True); print(m.is_watertight, len(m.split(only_watertight=False)), m.bounds.tolist())"
```

The source is CadQuery-only. The exported STL is the only coupon mesh in this
revision; no separate lane mesh is supplied. Re-import evidence: SHA-256
`ee4c43a818eb2b12d77517d8668e5c9c249c90fe4ff4aea8f08f58bbb7ea931c`,
one watertight winding-consistent component, bounds
`[0.000,-17.500,-2.100]..[55.600,17.500,9.700] mm`, and volume
`1462.456250 mm3`.
