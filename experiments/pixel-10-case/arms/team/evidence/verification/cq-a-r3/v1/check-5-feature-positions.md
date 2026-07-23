# Re-imported STL feature-position audit

Candidate was inverse-transformed from its supplied printer pose by translating printer
Z -1.75 mm, then rotating 180 degrees about X.  Measurements below are from section
rings of the re-imported STL with an explicit model-coordinate plane transform.

| Feature | Expected named datum | Observed on re-imported STL | Result |
|---|---|---|---|
| F-003 shared camera opening | D1_XMID: X=0; D4_TOP: top >=141.8; P-005 oversized shared opening | X=-0.000; X span -33.246..+33.246 (66.492); Y span 114.300..142.300 (28.000); top=142.300 | pass |
| F-004 A/B/C and F-005 flash | M-019/M-021/M-023/M-025 bounded points must lie inside shared opening | all four accepted datum points lie inside X=-33.246..33.246, Y=114.300..142.300; flash stays at +X | pass |
| F-006/F-007 control relief | D3_RIGHT/+X; Y=42..122 | +X-side gap is continuous through the required Y=42..122 band; no matching -X control gap | pass |
| F-009 bottom opening | D1_XMID; >=18 mm wide; open at D2_BOTTOM | re-imported lower edge has material only outside X=-29.000..+29.000, hence 58.000 mm centred opening | pass |
| F-013 top relief | D1_XMID; 8 mm centred top relief | re-imported rear-plane ring has X=-4.000..+4.000, Y=150.300..155.300 | pass |

Handedness was checked against the official rear view: the control relief is on +X/rear-view right and the flash datum is on +X. Mirroring would move the control relief to -X and contradict both the fixture and IMG-01.

At three central rear-panel probes (X=0, Y=30/80/110), the re-imported STL ray
intersections were Z=0.350 and Z=1.750 mm, giving a 1.400 mm rear wall. This also
records the useful section evidence for the open screen face and P-002 wall response.
