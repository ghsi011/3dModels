"""
Thin "just below the waterline" experiment.

The first sample failed: dark CF letters under 1.0-3.0 mm of translucent PETG
were barely visible -- translucent PETG is too cloudy to read through at that
thickness. This tests the opposite extreme: text sitting JUST under the wavy sea
surface with only a thin translucent skin over it, and left as an AIR-GAP recess
(no CF), single material, so it prints in minutes with no nozzle swap.

Method: take a small patch of the real wavy sea from the clear strip, squash it
in Z so the whole thing is a thin wavy chip, and recess the word into the flat
underside. Because the piece is thin, the cover over the letters is small and
VARIES with the waves -- one small print shows the whole legibility gradient from
~0.24 mm (troughs) to ~1.2 mm (crests). Read from above through the thin skin;
mirrored, so it reads correctly from the top.

Prints as ONE translucent part: drag into Studio, translucent PETG, 0.2 mm layer,
100% infill (so no lattice shows through), no brim needed. ~1.6 mm tall, tiny.
"""

import os
import numpy as np
import trimesh
import manifold3d as m3d
import cadquery as cq
from cadquery import exporters

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "jclass wcrew big.stl")

# --- patch of real wavy sea (clear strip) -----------------------------------
CUT_X0, CUT_X1 = 118.0, 150.0     # 32 mm
CUT_Y0, CUT_Y1 = 86.0, 114.0      # 28 mm
CUT_Z_TOP = 7.0
CUT_Z_BOT = 0.01                  # cut just above the noisy underside, drop to 0

# --- thinning + text --------------------------------------------------------
TARGET_MAX_H = 1.6                # mm, squash the wavy sea to this max height
TEXT_DEPTH = 0.4                  # mm = 2 layers @0.2, air-gap recess
FONT, FONT_KIND = "Arial", "bold"
WORD = "Abba"
WORD_SIZE = 9.0                   # mm, big-ish -> best case for legibility


def _to_manifold(mesh):
    return m3d.Manifold(m3d.Mesh(
        vert_properties=np.asarray(mesh.vertices, dtype=np.float32),
        tri_verts=np.asarray(mesh.faces, dtype=np.uint32)))


def _to_trimesh(man):
    me = man.to_mesh()
    return trimesh.Trimesh(
        vertices=np.asarray(me.vert_properties[:, :3], dtype=np.float64),
        faces=np.asarray(me.tri_verts, dtype=np.int64), process=False)


# ---- cut the patch out of the source (manifold3d; source isn't watertight) --
src = trimesh.load(SRC)
z0 = src.bounds[0][2] + CUT_Z_BOT
box = (m3d.Manifold.cube([CUT_X1 - CUT_X0, CUT_Y1 - CUT_Y0, CUT_Z_TOP - z0])
       .translate([CUT_X0, CUT_Y0, z0]))
patch = _to_trimesh(_to_manifold(src) ^ box)
patch.apply_translation([-(CUT_X0 + CUT_X1) / 2, -(CUT_Y0 + CUT_Y1) / 2, -patch.bounds[0][2]])

# ---- squash in Z (flat bottom stays at 0) ----------------------------------
h0 = patch.bounds[1][2]
kz = TARGET_MAX_H / h0
patch.vertices[:, 2] *= kz
sea_lo, sea_hi = patch.bounds[0][2], patch.bounds[1][2]
# sea_lo is the lowest point of the TOP surface (troughs); cover = sea - TEXT_DEPTH
print(f"patch {CUT_X1-CUT_X0:.0f}x{CUT_Y1-CUT_Y0:.0f} mm, squashed z x{kz:.3f}")
print(f"sea skin height : {sea_lo:.2f} .. {sea_hi:.2f} mm")
print(f"cover over text : {sea_lo-TEXT_DEPTH:.2f} .. {sea_hi-TEXT_DEPTH:.2f} mm  "
      f"(text depth {TEXT_DEPTH})")

# ---- text recess in the flat underside, mirrored ---------------------------
# Drawn normally in +Z view, cut into z=0..TEXT_DEPTH -> reads correct from above.
txt = cq.Workplane("XY").text(WORD, WORD_SIZE, TEXT_DEPTH * 3, font=FONT,
                              kind=FONT_KIND, halign="center", valign="center")
tmp = os.path.join(D, "_thin_txt.stl")
exporters.export(txt, tmp, tolerance=0.01, angularTolerance=0.1)
tmesh = trimesh.load(tmp)
os.remove(tmp)
# place at z=0..TEXT_DEPTH (its box is centred on z=0, so shift up by 1.5*depth top)
tmesh.apply_translation([0, 0, -tmesh.bounds[0][2]])          # base at 0
tmesh = _to_trimesh(_to_manifold(tmesh) ^ m3d.Manifold.cube(
    [100, 100, TEXT_DEPTH]).translate([-50, -50, 0]))         # keep only 0..DEPTH

base = _to_trimesh(_to_manifold(patch) - _to_manifold(tmesh))
base.export(os.path.join(D, "thin_base.stl"))

vol = base.volume / 1000
print(f"watertight {base.is_watertight}  vol {vol:.2f} cm3 (~{vol*1.27:.1f} g)  "
      f"faces {len(base.faces)}")

# ---- renders: mirror check + cover heatmap ---------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

tri = tmesh.triangles[:, :, :2]
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for a, flip, ttl in ((ax[0], False, "TOP - read through the thin skin (must read)"),
                     (ax[1], True, "BOTTOM - as printed (must mirror)")):
    pb = base.bounds
    hx = [-pb[1][0], -pb[0][0]] if flip else [pb[0][0], pb[1][0]]
    a.add_patch(plt.Rectangle((hx[0], pb[0][1]), hx[1]-hx[0], pb[1][1]-pb[0][1],
                              facecolor="#dfe8e6", edgecolor="#5a6b68"))
    h = tri[:, :, 0] * (-1 if flip else 1)
    a.add_collection(PolyCollection(np.stack([h, tri[:, :, 1]], -1),
                                    facecolors="#26315e", edgecolors="none"))
    a.set_aspect("equal"); a.autoscale_view(); a.set_title(ttl, fontsize=10); a.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(D, "thin_readability.png"), dpi=140, facecolor="white")
print("wrote thin_readability.png")
