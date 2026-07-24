# V2-01 correction receipt

DESIGNER SELF-CHECK — NON-ACCEPTANCE

The base is now an XZ sketch with 1.80-mm endpoint rounds. Its continuous exposed upper-side boundary is cut and rebuilt with 1.60-mm cylindrical rails. Both are source geometry, not a source-only assertion.

On re-imported STL `bafb6b7e19a35c602ae105e3c79338db92c0e5a91cc7f2ce4563d8d1e4e0d112`, `verify.py` samples the left E-02 boundary directly from triangle rings. The lower endpoint reads `1.799517..1.799519 mm`, the interior `1.599570..1.599573 mm`, and the upper endpoint `1.799517..1.799519 mm`; each exceeds G-05's 1.50-mm floor.

The same re-import pass records native `Y=-8.000` at P_BED and `0.000000 mm2` forbidden/non-P_BED downface area under the frozen Rx(+90°) transform.
