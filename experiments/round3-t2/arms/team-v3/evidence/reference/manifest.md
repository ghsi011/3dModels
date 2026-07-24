# Blind reference manifest

Commission: `round3-t2-washer-filter-cap-tool`, dimensions contract revision 1.

This geometry was constructed only from `experiments/round3-t2/arms/team-v3/dimensions.md`. No common brief, SVG, other arm, scorer, test, history, hidden/reference artifact, web source, or FreeCAD input was inspected.

The exported `reference.stl` and `reference.step` contain only the authorized raised-bar envelope: `X=-31.00..+31.00`, `Y=-5.85..+5.85`, `Z=0.00..+24.00` mm. `reference.py` retains the authorized `Ø63.00` cap-face planar keep-out as a non-exported construction datum; cap thickness and rear geometry are not inferred.

Reproduce from this directory:

```powershell
python .\reference.py
python .\render_reference.py
python -c "import trimesh; m=trimesh.load_mesh('reference.stl'); print(m.is_watertight, m.bounds.tolist())"
Get-FileHash reference.py,reference.stl,reference.step,render_reference.py,reference_top.png,reference_side.png -Algorithm SHA256
```

| Artifact | SHA-256 |
|---|---|
| `reference.py` | `3c36bfcd12a253c9412f92fa460e12acf420e733fba69ffbfe898e7e4813fb29` |
| `reference.stl` | `25fac0c2fe277d8cdaf7384d7076019623291a01f4989cc23e908d55839c303a` |
| `reference.step` | `a65aec3a5144a5a8f5b32c04b51d93d4464927b13ea67d2f52ce35d80b75570e` |
| `render_reference.py` | `f7abc787714b55b6ddfbbc4d8f4b150daf80b9216e265ae6e51868586c534c9a` |
| `reference_top.png` | `5b1dcbb45a811da3de6478d59fae51970a899a4bbdae5cf7b8d2ae3de602e81f` |
| `reference_side.png` | `bb7ababc8b981a3b41285748b478c08702f4712543725f701a1156575d04983a` |

Exported-STL re-import observed: watertight; bounds `[-31.0, -5.8499999, 0.0]..[31.0, 5.8499999, 24.0]` mm.
