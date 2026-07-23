"""
Coupon B — the REALITY CHECK: real sculpted sea top, real text underneath.

Coupon A (model.py) is a flat thickness ladder. It gives you the clean law:
how legibility varies with translucent cover, all else equal. What it cannot
tell you is what the base's actual wavy "sea" surface does to the letters --
its sloped facets refract and scatter, and a flat plate has none of that.

This coupon cuts a real chunk straight out of 'jclass wcrew big.stl' -- the
genuine sea sculpt, unmodified -- and recesses the same test word into its
underside. Print it next to coupon A and you can separate the two effects:
any legibility difference between A and B at the same local thickness IS the
waves.

Where the chunk comes from (measured):
  The hull body occupies X ~99..115 of the base's X 86.88..150.55, so it would
  physically block anything read from above in that band. The clear sea strip
  is X 115..150 -- ~35 mm wide, running the full 137.5 mm length -- and that is
  where the final text has to live anyway. The chunk is taken from there, so it
  is representative of the real design, not just of "some waves".

  Sea top in that strip measured z = 1.62 .. 5.49 mm, i.e. the cover over a
  0.6 mm recess varies from ~1.0 to ~4.9 mm naturally. Coupon A's ladder
  (1.0/1.6/2.2/3.0) brackets the useful part of that range.

Print text-face down, same as coupon A.
"""

import os
import numpy as np
import trimesh
import manifold3d as m3d
import cadquery as cq
from cadquery import exporters

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "jclass wcrew big.stl")

# ============================== PARAMETERS ==================================

# --- Chunk to cut out of the real base, in the SOURCE STL's coordinates ------
# Chosen inside the clear-sea strip (X 115..150), away from the hull (X 99..115).
CUT_X0, CUT_X1 = 116.0, 150.0     # mm -> 34 mm wide
CUT_Y0, CUT_Y1 = 60.0, 122.0      # mm -> 62 mm long, matches coupon A's length
CUT_Z_TOP = 6.0                   # mm, above the highest sea point (5.49) and
                                  #     below the rigging that overhangs this strip

# The source STL's underside is flat to within ~1.4 um, but that micro-noise is
# enough to stop any capping/boolean from closing cleanly there. The chunk is
# therefore cut 0.01 mm ABOVE the STL's z-min and then dropped back onto z = 0,
# which buys a genuinely planar underside for the price of 10 um of material --
# 1/20 of a layer, i.e. below anything the printer or the eye can resolve.
CUT_Z_BOT = 0.01                  # mm above the source's z-min

# --- Text, identical to coupon A so the two are directly comparable ---------
TEXT_DEPTH = 0.6                  # mm = 3 layers @ 0.2
FONT = "Arial"
FONT_KIND = "bold"
WORD = "Abba"
WORD_SIZE = 10.0                  # mm, same true final size as coupon A

# Lines run along Y, matching how the final text must be laid out in the
# 35 mm-wide clear strip (3 lines at ~11 mm pitch is the only way it fits).
COL_OFFSET = 7.5                  # mm, column centres at -/+ this in local X
ROW_OFFSET = 15.0                 # mm, two rows per column at -/+ this in local Y

OUT_DIR = D

# ============================== BUILD =======================================


def _to_manifold(mesh):
    return m3d.Manifold(m3d.Mesh(
        vert_properties=np.asarray(mesh.vertices, dtype=np.float32),
        tri_verts=np.asarray(mesh.faces, dtype=np.uint32)))


def _to_trimesh(man):
    me = man.to_mesh()
    return trimesh.Trimesh(
        vertices=np.asarray(me.vert_properties[:, :3], dtype=np.float64),
        faces=np.asarray(me.tri_verts, dtype=np.int64), process=False)


def _unpinch(mesh, eps=2e-3):
    """Nudge coincident-but-distinct vertices apart.

    The sea sculpt touches itself at three points inside this chunk (it looks
    like a marching-cubes surface at a 0.0025 mm grid, and at a saddle the two
    sheets meet exactly). manifold3d is happy with that -- the vertices have
    different indices -- but a binary STL has no indices at all, so on reload
    those vertices merge by position and each contact becomes a non-manifold
    edge with 4 faces. The exported file would then read as NOT watertight.

    Pulling each copy 2 um back along its own vertex normal (i.e. into its own
    side of the solid) separates the sheets without touching the topology. Cost:
    0.0002 mm3 of volume, and a 2 um dimple 1/100 of a layer deep.
    """
    V = mesh.vertices
    order = np.lexsort((V[:, 2], V[:, 1], V[:, 0]))
    Vs = V[order]
    same = np.all(np.isclose(Vs[1:], Vs[:-1], rtol=0, atol=1e-9), axis=1)
    dup = np.zeros(len(V), dtype=bool)
    dup[order[:-1][same]] = True
    dup[order[1:][same]] = True
    if not dup.any():
        return mesh
    V = V.copy()
    V[dup] -= eps * mesh.vertex_normals[dup]
    print(f"  unpinched  : {int(dup.sum())} coincident vertices nudged {eps*1000:.0f} um")
    return trimesh.Trimesh(vertices=V, faces=mesh.faces, process=False)


def extract_chunk():
    """Cut a rectangular block of the real base out of the source STL.

    The obvious route -- repeated trimesh.slice_plane(cap=True) -- does NOT work
    here. The source is reported non-watertight (276,010 faces), but the real
    problem is subtler than that: as a face soup it is actually closed (every
    edge has exactly 2 faces bar two non-manifold edges away from this strip).
    What breaks is the CAPPING. The underside carries ~1.4 um of float noise and
    the sea sculpt has a few sliver triangles, and the cap triangulator leaves
    thousands of unshared edges along the bottom plus ~34 along the +X cap. The
    result is a chunk that no CSG engine will accept as a volume, which is why
    the text boolean died with "Not all meshes are volumes!".

    manifold3d, on the other hand, ingests the raw source as-is (status NoError,
    volume 45,850 mm3), so the whole cut is done as ONE boolean intersection
    against a box. That gives a watertight chunk with a 2-triangle planar
    underside of exactly (CUT_X1-CUT_X0) x (CUT_Y1-CUT_Y0) mm.
    """
    src = trimesh.load(SRC)
    z0 = src.bounds[0][2] + CUT_Z_BOT
    box = (m3d.Manifold.cube([CUT_X1 - CUT_X0, CUT_Y1 - CUT_Y0, CUT_Z_TOP - z0])
           .translate([CUT_X0, CUT_Y0, z0]))
    m = _to_trimesh(_to_manifold(src) ^ box)
    # Move to a local frame: centred in XY, underside on z = 0.
    m.apply_translation([-(CUT_X0 + CUT_X1) / 2.0,
                         -(CUT_Y0 + CUT_Y1) / 2.0,
                         -m.bounds[0][2]])
    return _unpinch(m)


def text_solids():
    """Same word, same size, same recess depth as coupon A.

    Returns (all_text, cf_text) as trimesh meshes in the chunk's local frame.
    Left column -> PETG-CF inlay. Right column -> bare recess.
    """
    def word(rot=90):
        return (cq.Workplane("XY")
                .text(WORD, WORD_SIZE, TEXT_DEPTH, font=FONT, kind=FONT_KIND,
                      halign="center", valign="center")
                .rotate((0, 0, 0), (0, 0, 1), rot))

    cf, bare = None, None
    for row in (-ROW_OFFSET, ROW_OFFSET):
        left = word().translate((-COL_OFFSET, row, 0))
        right = word().translate((COL_OFFSET, row, 0))
        cf = left if cf is None else cf.union(left)
        bare = right if bare is None else bare.union(right)

    tmp_cf = os.path.join(OUT_DIR, "_tmp_cf.stl")
    tmp_all = os.path.join(OUT_DIR, "_tmp_all.stl")
    exporters.export(cf, tmp_cf, tolerance=0.01, angularTolerance=0.1)
    exporters.export(cf.union(bare), tmp_all, tolerance=0.01, angularTolerance=0.1)
    a, c = trimesh.load(tmp_all), trimesh.load(tmp_cf)
    os.remove(tmp_cf)
    os.remove(tmp_all)
    return a, c


if __name__ == "__main__":
    chunk = extract_chunk()
    print(f"chunk        : {chunk.extents[0]:.2f} x {chunk.extents[1]:.2f} x "
          f"{chunk.extents[2]:.2f} mm")
    print(f"  watertight : {chunk.is_watertight}   faces {len(chunk.faces)}")
    print(f"  sea top    : z {chunk.bounds[0][2]:.2f} .. {chunk.bounds[1][2]:.2f}")

    all_text, cf_text = text_solids()
    base = trimesh.boolean.difference([chunk, all_text])

    print(f"  after cut  : watertight {base.is_watertight}  "
          f"vol {base.volume/1000:.2f} cm3  faces {len(base.faces)}")
    print(f"  underside  : z_min {base.bounds[0][2]:.4f}")

    base.export(os.path.join(OUT_DIR, "sea_base.stl"))
    cf_text.export(os.path.join(OUT_DIR, "sea_text_cf.stl"))
    all_text.export(os.path.join(OUT_DIR, "sea_text_all.stl"))

    vb, vt = base.volume / 1000, cf_text.volume / 1000
    print(f"translucent PETG : {vb:.2f} cm3 (~{vb*1.27:.1f} g)   MAIN nozzle")
    print(f"PETG-CF text     : {vt:.3f} cm3 (~{vt*1.27:.2f} g)   AUX nozzle")
