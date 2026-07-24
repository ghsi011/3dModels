# cq-a reproducibility manifest

DESIGNER SELF-CHECK — NON-ACCEPTANCE

| Artifact | SHA-256 |
|---|---|
| `cq-a-washer-filter-tool.stl` | `39b305ae74ab71d95fcad4160b86d3202c5880dbc7741981a045fac9e5d889df` |
| `cq-a-washer-filter-tool.step` | `ecafce833ab955e8f945b0c644388615806b6a9deda24d68f24b43b238accf21` |
| `model.py` | `b35f3917821b29f143db5ef3ba4d83e2b2d43de8a40cbdd3ca970e031cc86a81` |
| `verify.py` | `4cf47b5e4024121aa9330ce8ab4ef6b286806668994eea8f964e45e350d10a2e` |
| `cq-a-exterior-isometric.png` | `611bf72e3c28fec6fbbc9587dbebcc96f2528973fd74c1a642dc7b9507b30ae0` |
| `cq-a-installed-engagement.png` | `09f2c86fe8625efd897de8ffab7407b2994420681825a51336ddb3114f102213` |
| `cq-a-section.png` | `7ba6076eb07fca4b790c4b375d12511b5c8b2679e7f544c2a1e85e860dd943aa` |
| `cq-a-print-orientation.png` | `432678e787d3151d8f44fe48bb1e37d00248d0aabb36b1fe6b1148d580d2d3ac` |

Reproduce from `arms/team-v3`:

```powershell
python .\model.py
python .\verify.py
```

The current STL hash is the binding candidate hash; render/source hashes should be recomputed with `Get-FileHash` after any change.
