"""Round-5 D2 candidate tool (Arm S / Sonnet 5) -- build123d source.

Installed frame (matches dimensions.md / reference_model.py):
  X = D1 (bar long axis, centred);  Y = D2 (bar short axis, centred);
  Z = D3 (cap normal, D0 cap face at Z=0). Bar occupies X +/-31.0, Y +/-5.85, Z 0..24.0.

Print transform (print_plan.md): printer_X=X, printer_Y=-Z, printer_Z=Y+16.
=> installed +Y is the printer build (+printer_Z) direction; P_BED is the installed
   Y=-16.000 end face. A face is a print "roof" (needs <=45deg self-support) only if
   its outward normal has a large *installed +/-Y* component (that is what maps to
   printer +/-Z after the transform's rotation part, printer_normal=(nx,-nz,ny)).
   Faces with normal purely in installed X or Z stay print-vertical walls regardless
   of shape, because those map to printer_X / printer_Y (both horizontal, in-plane
   with the bed, never overhangs). Only installed-Y-varying transitions are overhang
   risk; everything else can be any shape without support.

Design: one continuous outer prism (constant X/Z cross-section) running the whole
installed-Y length from the P_BED land (Y=-16, first print layer) through a hand
grip and into the bar-capture channel body -- a straight extrusion has zero overhang
risk by construction. A single rectangular cavity (open at the -Z mouth, per F05) is
cut for the bar envelope + G-02 clearances. The cavity's near (-Y) side opens
straight into the solid grip (removing material as Y increases needs no support).
Its far (+Y) side is closed by a self-supporting "tent" (gable) wedge: two <=40deg
sloped faces converging to a true zero-width ridge LINE (built by extruding a flat
triangle along X, not by lofting between rectangles -- see NOTE below), never a flat
roof/bridge, so every S-01..S-04 out-of-limit area is exactly 0.0 mm^2.

NOTE on two debugging findings kept here for the record (both confirmed empirically
against team_preflight.py support-audit on the exported/re-imported STL):
  1. build123d `loft()` defaults to a SMOOTH (non-ruled) interpolation between two
     section profiles. Lofting a full 63x24.6 rectangle to a near-zero sliver
     rectangle (as an easy way to approximate a ridge) produced a locally distorted,
     non-planar surface near the wide end -- 80+ mm^2 of faces steeper than 45 deg
     that a flat 40 deg taper should never have had. Fixed by building the wedge as
     a plain `extrude()` of a 2D triangle (Polygon) instead: a straight extrude of
     straight edges is always exactly planar, no loft/spline risk, and gives a true
     zero-width ridge with no residual end-cap face at all.
  2. A geometrically exact 45 deg face (e.g. the G-06 P_BED chamfer) has printer
     normal_z = -0.70710678118654752... (double precision). The audit threshold is
     -0.70710679 -- mathematically just barely on the passing side of that number --
     but the exported STL stores vertices in float32, and trimesh recomputes each
     face normal from those rounded vertices; the recomputed value lands a hair past
     the threshold and gets flagged. Any exactly-45deg flat face is float32-fragile
     this way, so every self-support-relevant angle in this model is kept measurably
     under 45 deg (40 deg taper; ~34 deg P_BED chamfer via asymmetric chamfer legs)
     rather than exactly at the limit.
"""
from __future__ import annotations

import math
from pathlib import Path

from build123d import (
    Align,
    Axis,
    BuildPart,
    BuildSketch,
    Box,
    Plane,
    Polygon,
    Pos,
    extrude,
    fillet,
    chamfer,
)
from build123d import export_stl, export_step

OUT = Path(__file__).parent

# ==== PARAMETERS (mm; provenance = commission_d2.md parametrization skeleton /
#       experiments/round5-t2/inputs/dimensions.md + print_plan.md) ====
BAR_L, BAR_W, BAR_H = 62.0, 11.7, 24.0        # F02 mating bar envelope (M02-M04)
CL_END, CL_SIDE, CL_TOP = 0.50, 0.30, 0.60    # G-02 min clearances (per end/side/top)
WALL = 3.60                                    # G-01 min wall 1.20 (3x0.42 line); sized
                                                # (with margin) so the outer comfort
                                                # fillet and the inner mouth-rim fillet,
                                                # which share this wall thickness from
                                                # opposite faces, both fit -- empirically
                                                # verified (see debug log in commission
                                                # receipt): WALL must exceed
                                                # OUTER_FILLET + MOUTH_R with headroom.
CAP_CLEAR = 0.60                               # G-03 clearance to D0 outside F02 (M05)
LEADIN_CH = 0.50                               # G-04 lead-in chamfer reference (<=45 deg);
                                                # realised here as the MOUTH_R fillet.
GRIP_R, ROOT_R, MOUTH_R = 1.50, 0.80, 0.80    # E-01 comfort / E-02 root / E-03,E-04 mins
PBED_Y = -16.000                               # P_BED plane (G-06)
PBED_CH1, PBED_CH2 = 0.30, 0.20                # G-06 chamfer legs: 0.30 mm (spec value)
                                                # x an asymmetric 0.20 mm second leg =
                                                # ~33.7 deg from the side wall, safely
                                                # under the 45 deg float32-fragile limit
                                                # (see module docstring, finding 2).
OUTER_FILLET = 2.00                            # actual uniform long-edge fillet used,
                                                # >= GRIP_R and >= ROOT_R with margin

# ---- derived channel geometry ----
CAV_X_HALF = BAR_L / 2 + CL_END               # 31.50  (X span 63.00 total, >=63.00 req)
CAV_Y_HALF = BAR_W / 2 + CL_SIDE              # 6.15   (Y span 12.30 total, >=12.30 req)
Z_FLOOR = CAP_CLEAR                            # 0.60   cavity mouth plane (open, no floor)
Z_CEIL = CAP_CLEAR + BAR_H + CL_TOP           # 25.20  cavity ceiling (>= BAR_H+CL_TOP=24.60 req)
Z_CAV_MID = (Z_FLOOR + Z_CEIL) / 2            # 12.90
CAV_Z_HALF = (Z_CEIL - Z_FLOOR) / 2           # 12.30

BODY_X_HALF = CAV_X_HALF + WALL               # 35.10  outer half-width (X)
Z_TOP = Z_CEIL + WALL                          # 28.80  outer top (Z)

Y_GRIP_LO = PBED_Y                             # -16.00 P_BED land (first print layer)
Y_ROOT = -CAV_Y_HALF                           # -6.15  nominal grip/body root boundary
                                                #        (functional label; geometry is
                                                #        one continuous prism through here)

TAPER_DEG = 40.0                               # < 45 deg design margin (method: <=45 deg)
TAPER_DEPTH = CAV_Z_HALF / math.tan(math.radians(TAPER_DEG))  # ~14.659
TAPER_RUNWAY = 3.0                             # extra straight cavity/mouth length kept
                                                # before the taper begins (more capture
                                                # depth; also where the far mouth-rim
                                                # edge would sit -- see below, that edge
                                                # is deliberately left unfilleted).
Y_TAPER_START = CAV_Y_HALF + TAPER_RUNWAY      # 9.15
Y_TAPER_END = Y_TAPER_START + TAPER_DEPTH      # ~23.81 (ridge line, cavity fully closed)
Y_END = Y_TAPER_END + 2.0                      # small structural margin past the ridge

print("derived: CAV_X_HALF", CAV_X_HALF, "CAV_Y_HALF", CAV_Y_HALF)
print("derived: Z_FLOOR", Z_FLOOR, "Z_CEIL", Z_CEIL, "Z_TOP", Z_TOP)
print("derived: BODY_X_HALF", BODY_X_HALF, "TAPER_DEPTH", TAPER_DEPTH, "Y_TAPER_END", Y_TAPER_END)


def make_tent_wedge() -> "Part":
    """Self-supporting gable wedge that closes the cavity's far (+Y) side: extrude a
    flat 2D triangle (Y,Z) along X. A straight extrude of straight edges is always
    exactly planar (no loft/spline distortion risk -- see module docstring)."""
    # Plane normal = +X (z_dir), local x_dir = +Y, so local in-plane (x,y) = (Y,Z).
    plane = Plane(origin=(-CAV_X_HALF, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    with BuildPart() as tent:
        with BuildSketch(plane):
            Polygon(
                (Y_TAPER_START, Z_FLOOR),
                (Y_TAPER_START, Z_CEIL),
                (Y_TAPER_END, Z_CAV_MID),
            )
        extrude(amount=2 * CAV_X_HALF)
    return tent.part


def _select_mouth_rim_edges(part: "Part") -> list:
    """Cavity mouth-rim edges to round for G-04/E-03/E-04: the inner rectangle
    boundary at Z == Z_FLOOR (the open -Z mouth) on the CONST cavity segment only
    (Y_ROOT .. Y_TAPER_START) -- the near (Y_ROOT) edge and the two X-side edges.
    The far (Y_TAPER_START) edge, immediately adjacent to the tent wedge's sloped
    face, is deliberately left UNFILLETED: rounding it swept the blend locally past
    45 deg (measured out-of-limit area ~38 mm^2 with it filleted, ~0 mm^2 without --
    see support-audit log) because a fillet sweeps continuously through every angle
    between its two bounding faces, and immediately past the mouth the taper's own
    face is already close to that limit. length>5mm excludes tiny corner slivers."""

    def _near(a: float, b: float, tol: float = 0.05) -> bool:
        return abs(a - b) < tol

    edges = []
    for e in part.edges():
        c = e.center()
        if not _near(c.Z, Z_FLOOR, 1e-2):
            continue
        on_x_side = _near(abs(c.X), CAV_X_HALF) and Y_ROOT - 0.05 <= c.Y <= Y_TAPER_START + 0.05
        on_near_y = _near(c.Y, Y_ROOT) and -CAV_X_HALF - 0.05 <= c.X <= CAV_X_HALF + 0.05
        if (on_x_side or on_near_y) and e.length > 5.0:
            edges.append(e)
    return edges


def build() -> "Part":
    # One continuous outer prism, Y_GRIP_LO (P_BED) .. Y_END (past the taper ridge),
    # constant X/Z cross-section -- a straight extrusion, zero overhang risk.
    outer = Box(
        2 * BODY_X_HALF, Y_END - Y_GRIP_LO, Z_TOP - Z_FLOOR,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    outer = Pos(0, Y_GRIP_LO, Z_FLOOR) * outer
    long_edges = outer.edges().filter_by(Axis.Y)
    outer = fillet(long_edges, radius=OUTER_FILLET)

    # Cut the constant-cross-section cavity box first (Y_ROOT..Y_TAPER_START), fillet
    # its mouth rim, THEN cut the tent wedge -- resolving the fillet before the wedge
    # cut keeps the fillet operation local to flat geometry only (see selection notes
    # above; also matches the empirically-working construction order).
    cav_const = Box(
        2 * CAV_X_HALF, Y_TAPER_START - Y_ROOT, Z_CEIL - Z_FLOOR,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    cav_const = Pos(0, Y_ROOT, Z_FLOOR) * cav_const
    part = outer - cav_const
    assert part.is_valid, "boolean result invalid after const-cavity cut"

    mouth_edges = _select_mouth_rim_edges(part)
    print("mouth_edges found:", len(mouth_edges), [round(e.length, 2) for e in mouth_edges])
    assert len(mouth_edges) == 3, f"expected 3 mouth-rim edges (near Y_ROOT + 2 X-sides), found {len(mouth_edges)}"
    part = fillet(mouth_edges, radius=MOUTH_R)

    tent = make_tent_wedge()
    part = part - tent
    assert part.is_valid, "boolean result invalid after tent-wedge cut"

    # ---- P_BED chamfer (G-06 / E-05): sharp-allowed nonfunctional bed land ----
    pbed_edges = [e for e in part.edges() if abs(e.center().Y - Y_GRIP_LO) < 1e-3]
    print("pbed_edges found:", len(pbed_edges))
    if pbed_edges:
        part = chamfer(pbed_edges, length=PBED_CH1, length2=PBED_CH2)

    return part


if __name__ == "__main__":
    part = build()
    print("is_valid", part.is_valid)
    print("volume_mm3", part.volume)
    bb = part.bounding_box()
    print("bbox_min", bb.min, "bbox_max", bb.max)

    export_stl(part, str(OUT / "candidate_tool.stl"), tolerance=0.01, angular_tolerance=0.1)
    export_step(part, str(OUT / "candidate_tool.step"))
    print("exported candidate_tool.stl / candidate_tool.step")
