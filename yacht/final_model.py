"""
FINAL J-class yacht — the real print, not a coupon.

One physical object, printed dual-nozzle on the Bambu X2D:

  * BASE  (rectangular slab + sculpted "sea") -> TRANSLUCENT PETG on the AUX
    (Bowden) nozzle. Mirrored birthday text is recessed into its DEAD-FLAT
    underside so it reads correctly looking DOWN through the translucent
    material from above, and looks mirrored from directly below (same
    convention as model.py / sea_model.py).
  * BOAT  (hull + mast + rigging + the little crew figure) -> indigo PETG-CF
    on the MAIN (direct-drive, hardened) nozzle. The recessed TEXT is the SAME
    CF material and prints on the SAME MAIN nozzle.

"The flip": CF -> MAIN, translucent -> AUX. Two physical nozzles, no material
switchover, near-zero purge. See the make_bambu_3mf.py block at the bottom of
this file for exactly how to weld the parts into the print-ready 3MF once the
sample settles the open questions.

Everything sample-dependent is a labelled knob in the KNOBS block below. The
geometry of the base (footprint, the hull-blocked X band, the clear "sea" strip
where text can be read from above, and the colour-split plane CUT_Z) is DERIVED
from the scaled mesh at run time, never hard-coded, so it tracks SCALE.

Pipeline:
  1. Load 'jclass wcrew big.stl', split off the detached crew figure, scale the
     yacht uniformly about the origin (keeps the underside on z=0).
  2. Derive the base footprint (flat bottom slab), the hull-blocked X band and
     the clear-sea strip by a downward ray-cast: a column is "readable" from
     above where the translucent sea surface is still visible (not replaced by
     the solid opaque hull). The clear strip is the contiguous readable band on
     the +X (open-water) side.
  3. Lay out the 3 text lines at ABSOLUTE mm size (decoupled from SCALE): each
     line runs along +Y (the long axis), the 3 lines stacked across the strip
     width in X, shrink-to-fit so every line fits the strip length and the
     stack fits the strip width with margin. Text drawn normally in the +Z view.
  4. Cut the text pockets out of the base with manifold3d (the source STL is not
     watertight as supplied; manifold3d ingests it as-is — same technique as
     sea_model.py). If INLAY, also emit the CF text solids that fill the pockets.
  5. Split the whole yacht at CUT_Z into BASE (z 0..CUT_Z, translucent, pocketed)
     and BOAT (z CUT_Z..top, CF, + the crew figure) with manifold3d.
  6. Export final_base.stl, final_boat.stl, final_text_cf.stl (if INLAY),
     a decimated combined final_model.step (see EXPORT_STEP — a preview proxy;
     the STLs are authoritative), and the verification renders.

Run:  python final_model.py
Then: python verify_final.py     (Phase-4 checks on the exported STLs)
"""

import os
import numpy as np
import trimesh
import manifold3d as m3d
import cadquery as cq
from cadquery import exporters

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "jclass wcrew big.stl")

# ============================== KNOBS ======================================
# Sample-dependent choices. The birthday sample print settles the ones marked
# [SAMPLE]; the rest are geometry/typography and are safe as-is.

SCALE = 1.00            # [SAMPLE] Uniform scale of the yacht mesh. Model is
                        #   149.55 mm tall; designer wants >=150 mm, so 1.00 is
                        #   borderline and 1.05 (-> 157 mm) is the safe pick.
                        #   Text is added at ABSOLUTE size AFTER scaling, so its
                        #   legibility is INDEPENDENT of this number.

TEXT_DEPTH = 0.6        # [SAMPLE] Recess depth, mm. Must be a whole number of
                        #   0.2 mm layers. 0.6 = 3 layers reads fully opaque in
                        #   the coupon; the sample may want 0.4 or 0.8.

INLAY = True            # [SAMPLE] True  -> also emit CF solids that FILL the
                        #   recesses (final_text_cf.stl), printed on MAIN.
                        #   False -> recesses left as air gaps (single-material
                        #   engraving in the translucent base). The sample decides.

CUT_Z = None            # [SAMPLE] Colour-split plane, mm. None -> derive it from
                        #   the scaled sea surface (clear-strip sea max + margin,
                        #   lands ~5.5..6.5). Set a number to override.
CUT_Z_MARGIN = 0.30     #   mm added above the derived sea max when CUT_Z is None.

# --- Typography (absolute mm, applied after SCALE) --------------------------
FONT = "Arial"
FONT_KIND = "bold"      # Bold only: PETG-CF fuzzes fine detail; Arial-Bold stem
                        #   ~0.14*size, so ~10 mm size -> ~1.4 mm stem (> 1.2 mm,
                        #   i.e. 3 x 0.4 nozzle).
LINES = [               # (text, default size mm). Sizes are STARTING points;
    ("Oh the places you'll go!", 10.0),   # shrink-to-fit may reduce them so the
    ("Happy birthday Abba!",     11.0),   # stack fits the strip width.
    ("24.07.2026",               12.0),
]
TEXT_ROT = 90.0         # deg about +Z. 90 -> lines run along +Y (the long axis),
                        #   which is the only way 3 lines fit the ~35 mm strip.
LINE_GAP = 2.0          # mm, minimum clear gap between adjacent stacked lines.
EDGE_MARGIN_X = 2.0     # mm, clearance from the text stack to each clear-strip edge.
EDGE_MARGIN_Y = 3.0     # mm, clearance from each line end to the footprint Y ends.
FOOT_MARGIN = 2.0       # mm, required min clearance to the footprint edge (checked).

# --- Clear-strip derivation (ray-cast) --------------------------------------
STRIP_PITCH = 0.5       # mm, XY ray grid for the readability map.
STRIP_READ_FRAC = 0.99  # a column is "clear" if >= this fraction of its Y length
                        #   still sees the sea surface from above.
HULL_READ_FRAC = 0.90   # a column is "hull-blocked" (for reporting) below this.

# --- STEP export (preview proxy; STLs are authoritative) --------------------
EXPORT_STEP = True      # The yacht is a ~275k-triangle art mesh; a full-fidelity
                        #   faceted STEP is ~1 GB. This writes a vertex-clustered
                        #   PROXY so a combined .step deliverable exists and opens.
STEP_BASE_CELL = 1.5    # mm clustering cell for the base in the STEP proxy.
STEP_BOAT_CELL = 0.6    # mm clustering cell for the boat in the STEP proxy.

# --- Constants --------------------------------------------------------------
LAYER = 0.2             # mm, printer layer height (X2D 0.20 Standard).
SLAB_Z = 1.0            # mm, "flat bottom slab" vertex band used to read the footprint.
SEA_BAND = (0.30, 6.5)  # mm (unscaled) z window that counts as "sea surface" in the
                        #   readability ray-cast; scaled by SCALE at run time.

OUT_BASE = os.path.join(D, "final_base.stl")
OUT_BOAT = os.path.join(D, "final_boat.stl")
OUT_TEXT = os.path.join(D, "final_text_cf.stl")
OUT_STEP = os.path.join(D, "final_model.step")


# ======================== mesh <-> manifold helpers =========================
def to_manifold(mesh):
    return m3d.Manifold(m3d.Mesh(
        vert_properties=np.asarray(mesh.vertices, dtype=np.float32),
        tri_verts=np.asarray(mesh.faces, dtype=np.uint32)))


def to_trimesh(man):
    me = man.to_mesh()
    return trimesh.Trimesh(
        vertices=np.asarray(me.vert_properties[:, :3], dtype=np.float64),
        faces=np.asarray(me.tri_verts, dtype=np.int64), process=False)


def unpinch(mesh, eps=2e-3):
    """Nudge coincident-but-distinct vertices apart (verbatim technique from
    sea_model.py). The sea sculpt touches itself at saddle points; manifold3d is
    fine with that (distinct indices) but a binary STL merges them on reload,
    turning each contact into a 4-face non-manifold edge that reads as NOT
    watertight. Pull each copy 2 um back along its own normal to separate the
    sheets without changing topology."""
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


def drop_slivers(mesh, min_vol=0.005):
    """Drop microscopic disconnected components. The source STL carries a few
    degenerate 4-face tets (near-zero volume, sub-micron extent) at its
    non-manifold spots; manifold3d preserves them as tiny closed volumes and they
    end up as junk specks in the boat STL that would confuse a slicer. Keep only
    components with |volume| >= min_vol (the real crew figure is ~7.8 mm3, so it
    survives comfortably). Returns (clean_mesh, n_dropped, n_bodies_kept)."""
    comps = mesh.split(only_watertight=False)
    with np.errstate(invalid="ignore", divide="ignore"):   # zero-vol slivers warn
        keep = [c for c in comps if abs(c.volume) >= min_vol]
    dropped = len(comps) - len(keep)
    if dropped == 0:
        return mesh, 0, len(comps)
    return trimesh.util.concatenate(keep), dropped, len(keep)


def cluster_decimate(mesh, cell):
    """Fast vertex-clustering decimation (self-contained; fast_simplification is
    not installed). Quantise vertices to a grid, average each cluster, drop
    degenerate faces. Used ONLY for the STEP preview proxy."""
    V = mesh.vertices
    q = np.round(V / cell).astype(np.int64)
    _, inv = np.unique(q, axis=0, return_inverse=True)
    inv = inv.ravel()
    nv = np.zeros((inv.max() + 1, 3))
    cnt = np.zeros(inv.max() + 1)
    np.add.at(nv, inv, V)
    np.add.at(cnt, inv, 1)
    nv /= cnt[:, None]
    F = inv[mesh.faces]
    good = (F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])
    return trimesh.Trimesh(vertices=nv, faces=F[good], process=False)


# =============================== load & scale ===============================
def load_scaled():
    """Return (main, crew) trimeshes, uniformly scaled about the origin so the
    flat underside stays exactly on z=0."""
    src = trimesh.load(SRC)
    comps = src.split(only_watertight=False)
    main = max(comps, key=lambda m: len(m.faces))
    crew = min(comps, key=lambda m: len(m.faces)) if len(comps) > 1 else None
    if SCALE != 1.0:
        for m in (main, crew):
            if m is not None:
                m.apply_scale(SCALE)     # scales vertex coords about origin
    return main, crew


# ============================ derive base footprint =========================
def footprint(main):
    """Rectangular flat-bottom slab, read from the vertices in the bottom band."""
    V = main.vertices
    low = V[V[:, 2] < SLAB_Z * SCALE]
    return (low[:, 0].min(), low[:, 0].max(), low[:, 1].min(), low[:, 1].max())


# ===================== derive hull band + clear sea strip ===================
def readability_map(main, foot):
    """Downward ray-cast readability. For a grid over the footprint, a column is
    readable where the sea surface is still visible from above (a ray hit in the
    scaled SEA_BAND). Where the solid opaque hull replaces the sea, no such hit
    exists -> not readable. Returns (gx, frac_readable_per_x)."""
    X0, X1, Y0, Y1 = foot
    lo, hi = SEA_BAND[0] * SCALE, SEA_BAND[1] * SCALE
    gx = np.arange(X0 + STRIP_PITCH / 2, X1, STRIP_PITCH)
    gy = np.arange(Y0 + STRIP_PITCH / 2, Y1, STRIP_PITCH)
    GX, GY = np.meshgrid(gx, gy)
    origins = np.column_stack([GX.ravel(), GY.ravel(),
                               np.full(GX.size, (Y1 - Y0) + 300.0)])
    dirs = np.tile([0.0, 0.0, -1.0], (len(origins), 1))
    loc, idx_ray, _ = main.ray.intersects_location(origins, dirs, multiple_hits=True)
    sea_vis = np.zeros(len(origins), dtype=bool)
    sea_z = np.full(len(origins), np.nan)   # top sea-surface height per column
    for r in np.unique(idx_ray):
        zs = loc[idx_ray == r][:, 2]
        band = zs[(zs >= lo) & (zs <= hi)]
        if len(band):
            sea_vis[r] = True
            sea_z[r] = band.max()
    sea_visG = sea_vis.reshape(GX.shape)
    frac = sea_visG.mean(axis=0)            # per-X readable fraction
    return gx, frac, sea_z.reshape(GX.shape)


def derive_strip(gx, frac, foot):
    """Clear strip = the contiguous readable (frac >= STRIP_READ_FRAC) band that
    touches the +X footprint edge. Hull band = the low-readability run."""
    X1 = foot[1]
    clear = frac >= STRIP_READ_FRAC
    # walk inward from the +X end while columns stay clear
    j = len(gx) - 1
    while j >= 0 and clear[j]:
        j -= 1
    strip_x0 = gx[j + 1] - STRIP_PITCH / 2 if j + 1 < len(gx) else X1
    strip_x1 = X1
    # hull band: the contiguous run below HULL_READ_FRAC (for the report)
    blocked = np.where(frac < HULL_READ_FRAC)[0]
    if len(blocked):
        hull_x0, hull_x1 = gx[blocked.min()], gx[blocked.max()]
    else:
        hull_x0 = hull_x1 = np.nan
    return strip_x0, strip_x1, hull_x0, hull_x1


# ================================ CUT_Z =====================================
def derive_cut_z(sea_zG, gx, strip_x0):
    """CUT_Z = max sea-surface height inside the clear strip + margin. The sea
    merges continuously into the hull, so this is a design plane, not a natural
    gap; keeping it above the strip's sea crest keeps the whole translucent
    window below the split. The innermost ~2 mm of the strip is skipped: the sea
    rears up steeply against the hull there (a narrow lip that would drag CUT_Z
    up by ~1 mm), and that lip carries no text."""
    col = gx >= strip_x0 + 2.0 * SCALE
    zz = sea_zG[:, col]
    sea_max = np.nanmax(zz)
    return sea_max, sea_max + CUT_Z_MARGIN * SCALE


# ============================ shrink-to-fit text ============================
def measure(txt, size):
    """(length_along_the_line, height_across_the_line) of one line after TEXT_ROT,
    in mm. A line of text is always far wider than tall, so length is the larger
    world extent and height the smaller — correct for any TEXT_ROT."""
    s = (cq.Workplane("XY")
         .text(txt, size, TEXT_DEPTH, font=FONT, kind=FONT_KIND,
               halign="center", valign="center")
         .rotate((0, 0, 0), (0, 0, 1), TEXT_ROT))
    bb = s.val().BoundingBox()
    return max(bb.xlen, bb.ylen), min(bb.xlen, bb.ylen)


def fit_text(strip_x0, strip_x1, foot):
    """Return a list of dicts per line: fitted size, X centre, length, height.
    Two constraints, both enforced:
      * length: each line's Y-run <= footprint_Y - 2*EDGE_MARGIN_Y
      * width : sum of line heights + gaps <= strip_width - 2*EDGE_MARGIN_X
    """
    X0, X1, Y0, Y1 = foot
    Yusable = (Y1 - Y0) - 2 * EDGE_MARGIN_Y
    strip_w = strip_x1 - strip_x0
    Xusable = strip_w - 2 * EDGE_MARGIN_X
    n = len(LINES)

    sizes = [d for _, d in LINES]
    # 1) length cap per line
    for i, (txt, _) in enumerate(LINES):
        L, _h = measure(txt, sizes[i])
        if L > Yusable:
            sizes[i] *= Yusable / L
    # 2) width cap on the stack (uniform shrink of all lines)
    heights = [measure(txt, sizes[i])[1] for i, (txt, _) in enumerate(LINES)]
    need = sum(heights) + (n - 1) * LINE_GAP
    if need > Xusable:
        k = (Xusable - (n - 1) * LINE_GAP) / sum(heights)
        sizes = [s * k for s in sizes]

    # final metrics + packing (centre the stack on the strip centre in X,
    # centre every line on the footprint centre in Y)
    dims = [measure(txt, sizes[i]) for i, (txt, _) in enumerate(LINES)]
    heights = [h for _, h in dims]
    total = sum(heights) + (n - 1) * LINE_GAP
    strip_cx = 0.5 * (strip_x0 + strip_x1)
    y_c = 0.5 * (Y0 + Y1)
    start = strip_cx - total / 2.0
    out = []
    for i, (txt, _) in enumerate(LINES):
        L, h = dims[i]
        cx = start + h / 2.0
        out.append({"txt": txt, "size": sizes[i], "x": cx, "y": y_c,
                    "length": L, "height": h})
        start += h + LINE_GAP
    return out, {"Yusable": Yusable, "Xusable": Xusable, "strip_w": strip_w,
                 "stack": total, "x_spare": Xusable - total, "strip_cx": strip_cx}


def build_text_mesh(fitted):
    """Union all fitted lines into one solid at z 0..TEXT_DEPTH; return a trimesh."""
    body = None
    for f in fitted:
        s = (cq.Workplane("XY")
             .text(f["txt"], f["size"], TEXT_DEPTH, font=FONT, kind=FONT_KIND,
                   halign="center", valign="center")
             .rotate((0, 0, 0), (0, 0, 1), TEXT_ROT)
             .translate((f["x"], f["y"], 0)))
        body = s if body is None else body.union(s)
    tmp = os.path.join(D, "_tmp_final_text.stl")
    exporters.export(body, tmp, tolerance=0.01, angularTolerance=0.1)
    m = trimesh.load(tmp, process=True)
    os.remove(tmp)
    return m


# ============================== STEP proxy ==================================
def write_step_proxy(base, boat):
    """Decimated, faceted combined STEP. Clearly a PREVIEW PROXY: a faithful
    faceted STEP of the full mesh is ~1 GB, so the base/boat are vertex-clustered
    first. The per-part STLs remain the authoritative geometry."""
    try:
        from OCP.BRep import BRep_Builder
        from OCP.TopoDS import TopoDS_Shell, TopoDS_Compound
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
        from OCP.gp import gp_Pnt
        from OCP.STEPControl import STEPControl_Writer, STEPControl_StepModelType
    except Exception as e:                      # pragma: no cover
        print(f"  STEP skipped (OCP unavailable): {e}")
        return None

    bld = BRep_Builder()
    comp = TopoDS_Compound()
    bld.MakeCompound(comp)
    total = 0
    for mesh, cell in ((base, STEP_BASE_CELL), (boat, STEP_BOAT_CELL)):
        d = cluster_decimate(mesh, cell)
        shell = TopoDS_Shell()
        bld.MakeShell(shell)
        pts = [gp_Pnt(float(x), float(y), float(z)) for x, y, z in d.vertices]
        for a, b, c in d.faces:
            try:
                w = BRepBuilderAPI_MakePolygon(pts[a], pts[b], pts[c], True).Wire()
                bld.Add(shell, BRepBuilderAPI_MakeFace(w).Face())
                total += 1
            except Exception:
                pass
        bld.Add(comp, shell)
    w = STEPControl_Writer()
    w.Transfer(comp, STEPControl_StepModelType.STEPControl_AsIs)
    w.Write(OUT_STEP)
    return total


# ================================ renders ===================================
def render_readability(base, text_all, foot, fitted, out):
    """Top view (read down through the translucent base -> MUST read correctly)
    and bottom view (as printed -> MUST look mirrored)."""
    X0, X1, Y0, Y1 = foot

    def draw(ax, flip, title):
        hx = [-X1, -X0] if flip else [X0, X1]
        ax.add_patch(plt.Rectangle((hx[0], Y0), hx[1] - hx[0], Y1 - Y0,
                                   facecolor="#dfe8e6", edgecolor="#5a6b68", lw=1.2))
        tri = text_all.triangles[:, :, :2]
        h = tri[:, :, 0] * (-1 if flip else 1)
        polys = np.stack([h, tri[:, :, 1]], axis=-1)
        ax.add_collection(PolyCollection(polys, facecolors="#26315e", edgecolors="none"))
        ax.set_aspect("equal")
        ax.autoscale_view()
        ax.set_title(title, fontsize=10)
        ax.axis("off")

    fig, axes = plt.subplots(1, 2, figsize=(11, 8))
    draw(axes[0], False,
         "TOP view — read down through the translucent base\nMUST READ CORRECTLY")
    draw(axes[1], True,
         "BOTTOM view — the underside as printed\nMUST LOOK MIRRORED")
    plt.tight_layout()
    plt.savefig(out, dpi=140, facecolor="white")
    plt.close(fig)
    print(f"  wrote {out}")


def render_section(base, boat, foot, fitted, cut_z, out):
    """XZ section at the text Y-centre: base profile (translucent) with the text
    notches in the underside, boat profile (CF) above, and the CUT_Z line."""
    y_c = fitted[0]["y"]
    fig, ax = plt.subplots(figsize=(9, 5))
    # Cut plane normal is +Y, so both sections live at the same Y: plot world
    # (X, Z) directly. (to_2D() would re-base each section in its own frame and
    # the two parts would not line up.)
    for mesh, color, label in ((base, "#3fb59e", "base (translucent)"),
                               (boat, "#26315e", "boat (CF)")):
        sec = mesh.section(plane_origin=[0, y_c, 0], plane_normal=[0, 1, 0])
        if sec is None:
            continue
        for ent in sec.entities:
            pts = sec.vertices[ent.points]
            ax.plot(pts[:, 0], pts[:, 2], color=color, lw=1.0)
        ax.plot([], [], color=color, lw=2, label=label)
    ax.axhline(cut_z, color="#c0392b", lw=0.8, ls="--", label=f"CUT_Z = {cut_z:.2f}")
    ax.axhline(TEXT_DEPTH, color="#888", lw=0.6, ls=":", label=f"recess {TEXT_DEPTH}")
    ax.axhline(0, color="#333", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Z (mm)")
    ax.set_title(f"Section at Y = {y_c:.1f} mm (through the text)\n"
                 "translucent base below CUT_Z, CF boat above, text recess in the underside",
                 fontsize=10)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(foot[0] - 4, foot[1] + 4)
    ax.set_ylim(-2, 36)
    plt.tight_layout()
    plt.savefig(out, dpi=140, facecolor="white")
    plt.close(fig)
    print(f"  wrote {out}")


def render_iso(parts, out, size=820):
    """Flat-shaded software z-buffer iso of the whole yacht, coloured by part.
    Runs on the decimated proxy meshes so it is fast and dependency-free."""
    az, el = np.radians(-52.0), np.radians(26.0)
    d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), -np.sin(el)])
    d /= np.linalg.norm(d)
    up = np.array([0.0, 0.0, 1.0])
    r = np.cross(d, up); r /= np.linalg.norm(r)
    tu = np.cross(r, d)
    light = np.array([0.35, 0.35, 0.87]); light /= np.linalg.norm(light)

    allv = np.vstack([m.vertices for m, _ in parts])
    sx = allv @ r; sy = allv @ tu
    pad = 0.06 * max(np.ptp(sx), np.ptp(sy))
    x0, x1 = sx.min() - pad, sx.max() + pad
    y0, y1 = sy.min() - pad, sy.max() + pad
    sc = min((size - 2) / (x1 - x0), (size - 2) / (y1 - y0))

    img = np.ones((size, size, 3), dtype=np.float32)
    zbuf = np.full((size, size), -1e9, dtype=np.float32)
    for mesh, col in parts:
        V = mesh.vertices
        px = ((V @ r - x0) * sc).astype(np.float64)
        py = (size - 1 - (V @ tu - y0) * sc).astype(np.float64)
        depth = V @ d
        col = np.array(col, dtype=np.float32)
        fn = mesh.face_normals
        shade = np.clip(np.abs(fn @ light), 0, 1) * 0.75 + 0.25
        for f in range(len(mesh.faces)):
            a, b, c = mesh.faces[f]
            xs = np.array([px[a], px[b], px[c]]); ys = np.array([py[a], py[b], py[c]])
            minx, maxx = int(np.floor(xs.min())), int(np.ceil(xs.max()))
            miny, maxy = int(np.floor(ys.min())), int(np.ceil(ys.max()))
            if maxx < 0 or minx >= size or maxy < 0 or miny >= size:
                continue
            minx, maxx = max(minx, 0), min(maxx, size - 1)
            miny, maxy = max(miny, 0), min(maxy, size - 1)
            if maxx < minx or maxy < miny:
                continue
            yy, xx = np.mgrid[miny:maxy + 1, minx:maxx + 1]
            x1x2 = xs[1] - xs[0]; x1x3 = xs[2] - xs[0]
            y1y2 = ys[1] - ys[0]; y1y3 = ys[2] - ys[0]
            det = x1x2 * y1y3 - x1x3 * y1y2
            if abs(det) < 1e-9:
                continue
            wx = xx - xs[0]; wy = yy - ys[0]
            u = (wx * y1y3 - x1x3 * wy) / det
            v = (x1x2 * wy - wx * y1y2) / det
            inside = (u >= -1e-4) & (v >= -1e-4) & (u + v <= 1 + 1e-4)
            if not inside.any():
                continue
            zf = depth[a] + u * (depth[b] - depth[a]) + v * (depth[c] - depth[a])
            reg = zbuf[yy[inside], xx[inside]]
            zi = zf[inside]
            take = zi > reg
            if not take.any():
                continue
            iy = yy[inside][take]; ix = xx[inside][take]
            zbuf[iy, ix] = zi[take]
            img[iy, ix] = col * shade[f]

    fig, ax = plt.subplots(figsize=(7.6, 7.6))
    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Whole yacht — iso  (indigo = CF boat + text, pale = translucent base)",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(out, dpi=140, facecolor="white")
    plt.close(fig)
    print(f"  wrote {out}")


# ================================= main =====================================
def main():
    print(f"=== FINAL J-class yacht  (SCALE={SCALE}) ===")
    main_m, crew = load_scaled()
    print(f"loaded: main {len(main_m.faces)} faces, "
          f"crew {'None' if crew is None else str(len(crew.faces)) + ' faces'}")
    zmax = main_m.bounds[1][2]
    print(f"height after scale: {zmax:.2f} mm")

    # --- derive footprint / strip / CUT_Z ---
    foot = footprint(main_m)
    X0, X1, Y0, Y1 = foot
    print(f"footprint: X {X0:.2f}..{X1:.2f} ({X1-X0:.2f})  "
          f"Y {Y0:.2f}..{Y1:.2f} ({Y1-Y0:.2f})")

    gx, frac, sea_zG = readability_map(main_m, foot)
    strip_x0, strip_x1, hull_x0, hull_x1 = derive_strip(gx, frac, foot)
    print(f"hull-blocked band  : X {hull_x0:.2f}..{hull_x1:.2f}  "
          f"(readability < {HULL_READ_FRAC:.0%})")
    print(f"clear sea strip    : X {strip_x0:.2f}..{strip_x1:.2f}  "
          f"({strip_x1-strip_x0:.2f} mm wide, full {Y1-Y0:.1f} mm length)")

    sea_max, cut_z = (None, CUT_Z)
    if CUT_Z is None:
        sea_max, cut_z = derive_cut_z(sea_zG, gx, strip_x0)
        print(f"CUT_Z derived      : {cut_z:.2f} mm "
              f"(clear-strip sea max {sea_max:.2f} + {CUT_Z_MARGIN*SCALE:.2f})")
    else:
        print(f"CUT_Z (override)   : {cut_z:.2f} mm")

    # --- text layout ---
    fitted, meta = fit_text(strip_x0, strip_x1, foot)
    print("text layout (absolute mm, running along Y, stacked in X):")
    for i, f in enumerate(fitted):
        xr = (f["x"] - f["height"] / 2, f["x"] + f["height"] / 2)
        yr = (f["y"] - f["length"] / 2, f["y"] + f["length"] / 2)
        print(f"  line {i+1}: size {f['size']:5.2f}  height(X) {f['height']:5.2f}  "
              f"length(Y) {f['length']:6.2f}  X {xr[0]:.2f}..{xr[1]:.2f}  "
              f"Y {yr[0]:.2f}..{yr[1]:.2f}")
    tight = meta["x_spare"] < 1.0
    print(f"  stack width {meta['stack']:.2f} in Xusable {meta['Xusable']:.2f} "
          f"(spare {meta['x_spare']:.2f} mm){'  <-- TIGHT' if tight else ''}")

    # --- text mesh + booleans (manifold3d) ---
    text_all = build_text_mesh(fitted)
    tb = text_all.bounds
    print(f"text mesh: {len(text_all.faces)} faces, z {tb[0][2]:.3f}..{tb[1][2]:.3f}, "
          f"X {tb[0][0]:.2f}..{tb[1][0]:.2f}  Y {tb[0][1]:.2f}..{tb[1][1]:.2f}")

    man_main = to_manifold(main_m)
    W, Ly = (X1 - X0 + 4), (Y1 - Y0 + 4)
    lower = m3d.Manifold.cube([W, Ly, cut_z + 2]).translate([X0 - 2, Y0 - 2, -2])
    upper = m3d.Manifold.cube([W, Ly, zmax - cut_z + 4]).translate([X0 - 2, Y0 - 2, cut_z])

    base_full = man_main ^ lower
    base_man = base_full - to_manifold(text_all)
    boat_man = man_main ^ upper
    if crew is not None:
        boat_man = boat_man + to_manifold(crew)

    base = unpinch(to_trimesh(base_man))
    boat = unpinch(to_trimesh(boat_man))
    base, nd_b, _ = drop_slivers(base)
    boat, nd_o, nb_o = drop_slivers(boat)
    if nd_b or nd_o:
        print(f"  dropped degenerate slivers: base {nd_b}, boat {nd_o} "
              f"(boat now {nb_o} real bodies: hull-assembly + crew figure)")

    # --- export STLs ---
    base.export(OUT_BASE)
    boat.export(OUT_BOAT)
    print(f"  wrote {OUT_BASE}  ({len(base.faces)} faces, watertight {base.is_watertight})")
    print(f"  wrote {OUT_BOAT}  ({len(boat.faces)} faces, watertight {boat.is_watertight}, "
          f"bodies {boat.body_count})")
    if INLAY:
        text_all.export(OUT_TEXT)
        print(f"  wrote {OUT_TEXT}  ({len(text_all.faces)} faces) -- CF inlay")
    else:
        if os.path.exists(OUT_TEXT):
            os.remove(OUT_TEXT)
        print("  INLAY=False -> recesses left as air gaps, no final_text_cf.stl")

    # --- volumes / masses (translucent & CF both 1.27 g/cm3) ---
    vb, vo = base.volume / 1000, boat.volume / 1000
    vt = (text_all.volume / 1000) if INLAY else 0.0
    print("masses (PETG translucent 1.27, PETG-CF 1.27 g/cm3):")
    print(f"  BASE translucent (AUX) : {vb:7.2f} cm3  ~{vb*1.27:6.1f} g")
    print(f"  BOAT CF (MAIN)         : {vo:7.2f} cm3  ~{vo*1.27:6.1f} g")
    if INLAY:
        print(f"  TEXT CF inlay (MAIN)   : {vt:7.3f} cm3  ~{vt*1.27:6.2f} g")
    tot = vb + vo + vt
    print(f"  TOTAL                  : {tot:7.2f} cm3  ~{tot*1.27:6.1f} g")

    # --- STEP proxy ---
    if EXPORT_STEP:
        n = write_step_proxy(base, boat)
        if n is not None:
            print(f"  wrote {OUT_STEP}  (PROXY, {n} decimated faces; STLs are authoritative)")

    # --- renders ---
    print("renders:")
    render_readability(base, text_all, foot, fitted,
                       os.path.join(D, "final_readability.png"))
    render_section(base, boat, foot, fitted, cut_z,
                   os.path.join(D, "final_section.png"))
    render_iso([(cluster_decimate(base, STEP_BASE_CELL), (0.82, 0.88, 0.86)),
                (cluster_decimate(boat, STEP_BOAT_CELL), (0.15, 0.19, 0.37))],
               os.path.join(D, "final_iso.png"))

    print("\nDONE. Now run:  python verify_final.py")


if __name__ == "__main__":
    main()


# ===========================================================================
# READY-TO-RUN 3MF COMMAND (the flip) — DO NOT run until the sample is settled.
# ===========================================================================
#
# The parts, once the sample fixes TEXT_DEPTH / SCALE / INLAY:
#
#   python make_bambu_3mf.py yacht_final.3mf \
#       "Base (translucent)=final_base.stl" \
#       "Boat (CF)=final_boat.stl" \
#       "Text (CF)=final_text_cf.stl"          # omit this arg if INLAY=False
#
# BUT make_bambu_3mf.py as written implements the OLD (un-flipped) assignment:
#
#     FILAMENT_PRESETS = [PETG Translucent (slot 1), PETG-CF (slot 2)]
#     PART_RULES = [("Base", 1, EXTRUDER_MAIN),   # translucent -> MAIN
#                   ("Text", 2, EXTRUDER_AUX)]    # CF          -> AUX
#
# i.e. it puts the TRANSLUCENT part on MAIN and CF on AUX — the exact opposite
# of the decided flip (CF -> MAIN, translucent -> AUX). The filament->nozzle map
# is DERIVED from the `extruder` column of PART_RULES (project_settings
# `filament_map` = [extruder of slot 1, extruder of slot 2], and the plate
# `filament_maps` likewise), so inverting that column inverts the map. The
# material<->slot pairing and the swatch colours stay put, so nothing else needs
# touching.
#
# THE MINIMAL, EXACT EDIT to make in make_bambu_3mf.py (do NOT change anything
# else — leave FILAMENT_PRESETS and FILAMENT_COLOURS as they are; slot 1 stays
# translucent, slot 2 stays CF, so the colours remain correct):
#
#     PART_RULES = [
#         ("Base", 1, EXTRUDER_AUX),    # translucent PETG -> AUX/Bowden
#         ("Boat", 2, EXTRUDER_MAIN),   # PETG-CF boat      -> MAIN/direct drive
#         ("Text", 2, EXTRUDER_MAIN),   # PETG-CF text      -> MAIN/direct drive
#     ]
#
# What that produces (verify in make_bambu_3mf.py's own output):
#   * project_settings filament_map = ["2","1"]  (slot1 translucent -> extruder 2
#     = Bowden/AUX ; slot2 CF -> extruder 1 = Direct Drive/MAIN)   <- the flip.
#   * plate filament_maps           = "2 1"      (same).
#   * "Base (translucent)"  -> filament 1, extruder 2 (AUX).
#   * "Boat (CF)" / "Text (CF)" -> filament 2, extruder 1 (MAIN).
#
# Note the added ("Boat", ...) token: the CF part is now the hull, whose name
# contains "Boat" not "Text", so it needs its own rule (first matching token
# wins). If INLAY=False there is no Text part and that rule is simply unused.
#
# Two X2D print settings worth a look before slicing (both are set for the
# coupon and remain correct here): sparse_infill_density 100% (no lattice in the
# translucent light path) and curr_bed_type "Textured PEI Plate". The tall thin
# mast will want supports — enable them in Studio for the BOAT only.
# ===========================================================================
