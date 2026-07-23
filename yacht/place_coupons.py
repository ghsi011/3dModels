"""Place coupon A and coupon B side by side for ONE print job.

The two coupons only mean something compared with each other, so they have to
come off the same plate, in the same session, with the same filament, the same
first layer and the same lighting when you hold them up. This script drops
coupon B to the right of coupon A with a 6 mm gap, both undersides on z = 0 and
both centred in Y, and writes *_placed.stl copies -- the originals are never
touched, so re-running model.py / sea_model.py stays authoritative.
"""

import os
import numpy as np
import trimesh

D = os.path.dirname(os.path.abspath(__file__))
GAP = 6.0     # mm of clear plate between the two coupons

A_BASE = trimesh.load(os.path.join(D, "sample_base.stl"))
A_TEXT = trimesh.load(os.path.join(D, "sample_text_cf.stl"))
B_BASE = trimesh.load(os.path.join(D, "sea_base.stl"))
B_TEXT = trimesh.load(os.path.join(D, "sea_text_cf.stl"))

a = A_BASE.bounds
b = B_BASE.bounds
dx = (a[1][0] + GAP) - b[0][0]                       # B's left edge lands GAP right of A's right edge
dy = ((a[0][1] + a[1][1]) / 2) - ((b[0][1] + b[1][1]) / 2)   # keep both centred in Y
dz = -b[0][2]                                        # keep the underside on z = 0
T = np.array([dx, dy, dz])

for mesh, name in ((B_BASE, "sea_base_placed.stl"), (B_TEXT, "sea_text_cf_placed.stl")):
    m = mesh.copy()
    m.apply_translation(T)
    m.export(os.path.join(D, name))
    print(f"wrote {name}: bounds "
          f"X {m.bounds[0][0]:.2f}..{m.bounds[1][0]:.2f}  "
          f"Y {m.bounds[0][1]:.2f}..{m.bounds[1][1]:.2f}  "
          f"Z {m.bounds[0][2]:.2f}..{m.bounds[1][2]:.2f}")

print(f"\ntranslation applied to coupon B: {np.round(T, 3).tolist()} mm")
print(f"coupon A X {a[0][0]:.2f}..{a[1][0]:.2f}   "
      f"coupon B X {b[0][0]+dx:.2f}..{b[1][0]+dx:.2f}   "
      f"gap {(b[0][0]+dx) - a[1][0]:.2f} mm")

# --------------------------------------------------------------- job checks
FAIL = []


def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{('  -- ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(label)


print("\nCOMBINED JOB")
Bb = trimesh.load(os.path.join(D, "sea_base_placed.stl"))
Bt = trimesh.load(os.path.join(D, "sea_text_cf_placed.stl"))
parts = [A_BASE, A_TEXT, Bb, Bt]

check((b[0][0] + dx) - a[1][0] >= GAP - 1e-6,
      f"coupons do not overlap in X, >= {GAP} mm apart",
      f"A ends {a[1][0]:.2f}, B starts {b[0][0]+dx:.2f}, gap {(b[0][0]+dx)-a[1][0]:.3f} mm")
check(abs(Bb.bounds[0][2]) < 1e-9 and abs(A_BASE.bounds[0][2]) < 1e-9,
      "both undersides on z = 0",
      f"A {A_BASE.bounds[0][2]:.6f}, B {Bb.bounds[0][2]:.6f}")
ay = (a[0][1] + a[1][1]) / 2
by = (Bb.bounds[0][1] + Bb.bounds[1][1]) / 2
check(abs(ay - by) < 1e-6, "both centred on the same Y", f"A {ay:.4f}, B {by:.4f}")
check(Bt.bounds[0][0] > Bb.bounds[0][0] and Bt.bounds[1][0] < Bb.bounds[1][0],
      "coupon B's CF text moved with its base")

lo = np.min([p.bounds[0] for p in parts], axis=0)
hi = np.max([p.bounds[1] for p in parts], axis=0)
print(f"  combined bbox  X {lo[0]:.2f}..{hi[0]:.2f}  "
      f"Y {lo[1]:.2f}..{hi[1]:.2f}  Z {lo[2]:.2f}..{hi[2]:.2f}")
print(f"  combined size  {hi[0]-lo[0]:.2f} x {hi[1]-lo[1]:.2f} x {hi[2]-lo[2]:.2f} mm")

RHO = 1.27  # g/cm3, PETG and PETG-CF are close enough to share one figure
main = (A_BASE.volume + Bb.volume) / 1000
aux = (A_TEXT.volume + Bt.volume) / 1000
print(f"  translucent PETG (MAIN) {main:.3f} cm3  ~{main*RHO:.2f} g")
print(f"  indigo PETG-CF   (AUX)  {aux:.3f} cm3  ~{aux*RHO:.2f} g")
print(f"  TOTAL                   {main+aux:.3f} cm3  ~{(main+aux)*RHO:.2f} g")

mf = os.path.join(D, "both_coupons.3mf")
if os.path.exists(mf):
    scene = trimesh.load(mf)
    g = getattr(scene, "geometry", {})
    check(len(g) == 4, "3MF re-loads with all 4 parts", f"{len(g)} parts")
    want = {"A Base flat ladder (translucent PETG - MAIN)": len(A_BASE.faces),
            "A Text (indigo PETG-CF - AUX)": len(A_TEXT.faces),
            "B Base real sea (translucent PETG - MAIN)": len(Bb.faces),
            "B Text (indigo PETG-CF - AUX)": len(Bt.faces)}
    for k, nfaces in want.items():
        got = g.get(k)
        check(got is not None and len(got.faces) == nfaces,
              f"3MF part '{k}' triangle count",
              f"{len(got.faces) if got is not None else 'MISSING'} vs {nfaces}")
    sb = scene.bounds
    check(np.allclose(sb[0], lo, atol=1e-3) and np.allclose(sb[1], hi, atol=1e-3),
          "3MF bounding box matches the STLs",
          f"X {sb[0][0]:.2f}..{sb[1][0]:.2f} Y {sb[0][1]:.2f}..{sb[1][1]:.2f} "
          f"Z {sb[0][2]:.2f}..{sb[1][2]:.2f}")
else:
    print(f"  (no {os.path.basename(mf)} yet -- run make_3mf.py, then re-run this script)")

print("\n" + ("JOB OK" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"))
