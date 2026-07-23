# Ref-2 artifact manifest

Input contract: `experiments/pixel-10-case/arms/team/dimensions.md` revision 3 only.
Commission: `ref-2`. All dimensions are millimetres. This is designer evidence only and
awaits the metrologist's r3 overlay review.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `reference_ref2.py` | 3963 | `5b8226728e963a8ef3675a8034093b53ff7978c24e9e4ad05f286949a0f5330a` |
| `render_ref2_views.py` | 853 | `66463744b62be8be2a41125312b88c0b6fb664f2c698b6e1190f461b1d26d46f` |
| `pixel10_reference_ref2.stl` | 154284 | `c1a250fdd68a54688308732bd4c9637eb4dd512406cdcdad2188fd0dd7e68d91` |
| `pixel10_reference_ref2.step` | 92214 | `6a5e8ae693dc3ce3906b9067e20102c9e6e3311200b4b5706a01dec1da10aa25` |
| `v-rear.png` | 38228 | `515fbfdb00d1c8121250e5eec5c43b6c197df3e4be2c07860d31066c33c342bd` |
| `v-front-right.png` | 5107 | `e4772e9feb16693096288fd117ee45c2c304f7e86efec2b2db4950a1e106201e` |
| `v-bottom.png` | 8654 | `0326ffe1abbb7312102700bd70511658f94c407a3b2322d58489910fa525691b` |
| `v-top.png` | 13224 | `5f19c0bb6ff99ad50923b15db3f8fb0fd04b118a3a975a12eb5a80c9b3eb8fe6` |
| `reference_ref2_technical.png` | 117767 | `0eacce927a8461a8e072efc0536a1dd6e662681171002de02eb9ac76a697ccfc` |

## Reproduction commands

Run from repository root:

```powershell
python experiments/pixel-10-case/arms/team/evidence/reference/ref-2/reference_ref2.py
python experiments/pixel-10-case/arms/team/evidence/reference/ref-2/render_ref2_views.py
python skills/3d-modeling/scripts/preview.py experiments/pixel-10-case/arms/team/evidence/reference/ref-2/pixel10_reference_ref2.stl experiments/pixel-10-case/arms/team/evidence/reference/ref-2/reference_ref2_technical.png --views multi --resolution 360 --title "Pixel 10 Ref-2 blind reference" --subtitle "dimensions.md r3 only" --strict
Get-FileHash experiments/pixel-10-case/arms/team/evidence/reference/ref-2/* -Algorithm SHA256
```

## Designer self-check

The source ran successfully with `valid True`, volume `96468.398 mm3`, and model bounding
box `73.003 x 152.806 x 10.606 mm`. The expected body dimensions remain 72.0 x 152.8 x
8.6 mm; the total exported extent includes the r3 camera-island protrusion and the
continuous right-control proxy. The strict preview reported a watertight STL with 3,084
triangles.
