"""
Nuc bottle feeder — through-roof inverted-bottle syrup feeder for nucleus colonies.

Architecture ("monolithic bulkhead tray"):
  One printed BODY = drinking tray + hollow threaded barrel that rises through the
  roof. The barrel carries an external 2-start clamp thread over its whole length;
  the PCO-1881 female socket is bored INSIDE the barrel top, so nothing on the body
  is wider than the clamp thread and the NUT spins on from above unobstructed.
  Roof+ceiling (8-30 mm) is sandwiched between the body's bearing flange (below the
  ceiling) and the nut (on the roof) -- pure compression, tool-free.
  The syrup outlet (bore mouth standing pool_depth above the tray floor) is integral
  with the tray, so pool depth is INDEPENDENT of roof thickness / clamp position.
  The whole bottle->outlet air path has exactly ONE joint: bottle lip -> TPU gasket
  -> printed seat inside the barrel top. Everything else is monolithic PETG.

Backend: CadQuery. Run:  python model.py          (build + export everything)
         Verification:   python verify.py         (Phase-4 checks on exported STLs)

Coordinate convention: body modeled in PRINT orientation, tray underside on Z=0.
The hive ceiling underside plane is at Z = Z_CEILING (see derived values).
"""

import math
import os

import cadquery as cq

# ============================================================================
# PARAMETERS (mm unless noted; provenance in comments)
# ============================================================================

# ---- Bottle interface: PCO-1881 — verified against ISBT drawing 3784253-17
#      (imajeenyus mirror), KIMEX preform QC sheet, patent WO2016019321A1 ----
PCO_T = 27.40            # thread crest OD ±0.13          [ISBT 3784253-17]
PCO_E = 24.20            # thread ROOT Ø (ØE)             [ISBT 3784253-17]
                         #   (24.94 is ØF, the collar — a common misquote)
PCO_G_COLLAR = 25.07     # ØG MAX, unthreaded collar under the lip: the printed
                         #   female crest ID must clear THIS, not ØE  [ISBT]
PCO_C = 21.74            # neck bore (21.72 ±0.13 at 4 mm depth)  [ISBT]
PCO_PITCH = 2.70         # right-hand, single start       [ISBT]
PCO_WRAP_DEG = 650.0     # thread wrap                    [ISBT]
PCO_LIP_TO_THREAD = 1.70 # S: top of finish -> thread start ±0.08 [ISBT]
PCO_X_LIP_TO_LEDGE = 17.0   # X: lip -> BOTTOM of support ledge ±0.25 [ISBT]
PCO_H_LIP_TO_LEDGE_TOP = 15.24  # H: lip -> top of support ledge [ISBT]
PCO_BEAD_D = 28.00       # TE bead Ø ±0.15                [ISBT]
PCO_BEAD_TOP_FROM_LIP = 9.0    # lip -> bead upper slope start  [ISBT ref]
PCO_BEAD_BOT_FROM_LIP = 12.97  # lip -> bead bottom int pt      [ISBT]
PCO_LEDGE_D = 33.0       # Z: support ledge OD ±0.15      [ISBT]
PCO_LIP_OD = 24.9        # lip outer blends R0.58 into ØF 24.94; usable flat
                         #   seal annulus ≈ Ø22.3-23.8    [ISBT]
# male thread ridge cross-section (ISBT Detail B, trapezoid approximation)
PCO_RIDGE_DEPTH = (PCO_T - PCO_E) / 2.0   # 1.60 radial   [ISBT]
PCO_RIDGE_W_ROOT = 1.66  # axial width at root            [ISBT]
PCO_RIDGE_W_CREST = 0.80 # axial width at crest flat      [ISBT]

# ---- Printed-female PCO thread fit (community-validated recipe: BOSL2
#      pco1881_cap, terahurts, Gazorpa — 0.2-0.3/side = snug, 0.4+ = free) ----
PCO_CLR_RADIAL = 0.32    # grows the groove cutter radially
PCO_CLR_AXIAL = 0.25     # per-flank axial clearance (~0.2-0.25 recipe)
SOCKET_BORE_D = 25.55    # female thread crest ID: clears ØG collar 25.07 max
                         #   AND male root 24.33 max; = BOSL2's 25.5. NOT E+clr!

# ---- Sealing (the ONE airtight joint) ----
GASKET_T = 2.0           # TPU washer thickness (printed on X2D main nozzle)
GASKET_OD = 25.0         # slips into the socket bore (bore Ø25.55)
GASKET_ID = 17.0         # > bore Ø16 so it never occludes the flow path
GASKET_CRUSH = 0.8       # thread positioned so the lip can compress the gasket
                         #   0.8 mm past first contact before threads bind
SEAT_DEPTH = 10.0        # barrel top face -> gasket seat shoulder
# => lip first touches at depth 8.0, fully crushed at 8.8 below the barrel top.

# ---- Roof clamp ----
ROOF_MIN = 8.0           # clamp range, brief §2
ROOF_MAX = 30.0
ROOF_HOLE_D = 44.0       # drill this through ceiling+roof (Ø44 hole saw; 42-46 ok)
CLAMP_MAJOR_D = 40.0     # barrel clamp-thread major diameter
CLAMP_DEPTH = 1.8        # thread radial depth  -> minor Ø36.4
CLAMP_LEAD = 8.0         # 2-start, pitch 4 -> fast tool-free travel (~3 turns/24mm)
CLAMP_STARTS = 2
CLAMP_W_ROOT = 3.0       # ridge axial width at root (trapezoid)
CLAMP_W_CREST = 1.0      # ridge axial width at crest
CLAMP_CLR_RADIAL = 0.30  # nut fit, per-side  (fdm-design §4 sliding/loose for PETG)
CLAMP_CLR_AXIAL = 0.25   # per-flank

# ---- Tray / bee biology ----
TRAY_OD = 150.0          # drinking tray outer diameter
TRAY_WALL = 2.4          # 3 perimeters at 0.4 nozzle... wall = multiple of 0.8
TRAY_FLOOR_T = 2.4       # floor thickness
POOL_DEPTH = 4.5         # syrup depth = outlet lip above floor. Range 3-6 (brief §3.8)
BOSS_FREEBOARD = 1.2     # boss top above equilibrium syrup level (dry footing)
BOSS_AF = 5.0            # hex boss across-flats
BEE_CHANNEL = 1.8        # drinking channel width between bosses (prior art ~1.6)
WALL_H = 15.0            # tray wall height above floor top: pool 4.5 + flood
                         # reserve ~8.5 + 2 margin. Reserve swallows a worst-case
                         # thermal expulsion (~80-100 ml) — see design_notes.md
RIM_GAP = 9.0            # tray rim to ceiling: bee space (6-9), bees enter here
N_RIBS = 4               # outlet support ribs (windows between = syrup exit)
RIB_W = 3.0
N_RIDGES = 4             # radial rescue ridges (climb-out during a flood event)
RIDGE_W = 1.6
N_WALL_RIBS = 8          # vertical grip ribs on tray outer wall (bee climbing)
WALL_RIB_W = 2.4
WALL_RIB_PROUD = 0.8

# ---- Riser / bore ----
BORE_D = 16.0            # syrup/air path bore (< C=21.74 cap, plenty for glugging)
COLUMN_OD = 22.0         # column around the bore below the cone
FLANGE_OD = 60.0         # ceiling bearing flange (>= hole Ø44 + 2x7 mm shoulder)
FLANGE_LAND_H = 3.0      # cylindrical land under the bearing face
CONE_ANGLE = 45.0        # support-free cone from column to flange (printed upright)

# ---- Nut ----
NUT_H = 16.0
NUT_OD = 80.0            # scalloped grip wheel, gloved-hand friendly
NUT_SCALLOP_D = 22.0
NUT_SCALLOP_N = 6
SKIRT_OD = 96.0          # anti-ant / rain skirt: shields a barrier-grease band
SKIRT_T = 2.0            # and sheds rain away from the roof hole
SKIRT_DROP = 12.0        # skirt lower edge below nut bearing face... see build_nut

# ---- Plug (bee-tight when the bottle is off) ----
PLUG_COMP = 0.15         # radial print compensation on the plug's male PCO thread
PLUG_DISC_D = 44.0
PLUG_DISC_T = 4.0

# ---- Derived vertical stack (print Z, tray underside = 0) ----
Z_FLOOR_TOP = TRAY_FLOOR_T                    # 2.4
Z_MOUTH = Z_FLOOR_TOP + POOL_DEPTH            # 6.9  outlet lip
Z_RIM_TOP = Z_FLOOR_TOP + WALL_H              # 17.4
Z_CEILING = Z_RIM_TOP + RIM_GAP               # 26.4 ceiling underside / flange face
Z_BARREL_TOP = Z_CEILING + ROOF_MAX + NUT_H   # 72.4 barrel top face
Z_SEAT = Z_BARREL_TOP - SEAT_DEPTH            # 62.4 gasket seat shoulder
Z_LIP_SEATED = Z_SEAT + GASKET_T - GASKET_CRUSH  # 63.6 lip plane, gasket crushed
HANG_DEPTH = Z_CEILING                        # ceiling to tray underside = 26.4+2.4
# HEADSPACE ASSUMPTION (brief §2, UNMEASURED): >= 35 mm. With 35, the gap under
# the tray to the frame top bars = 35 - 28.8 = 6.2 mm -> inside bee space. Idan:
# measure and, if headspace < 33, reduce WALL_H / RIM_GAP.

CONE_R0 = COLUMN_OD / 2.0                     # 11
Z_CONE_BASE = Z_MOUTH + 1.1                   # 8.0 cone starts above outlet mouth
CONE_R1 = CONE_R0 + (Z_CEILING - Z_CONE_BASE) * math.tan(math.radians(90 - CONE_ANGLE))
                                              # 29.4 at ceiling for 45°

OUT = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
# HELPERS
# ============================================================================

def helical_ridge(r_root, depth, w_root, w_crest, lead, wrap_deg,
                  z0=0.0, phase_deg=0.0, embed=0.25):
    """A single helical thread ridge solid (right-hand), axis +Z.
    Profile is a symmetric trapezoid, embedded `embed` below r_root so booleans
    fuse cleanly. Ridge centerline starts at angle phase_deg, height z0."""
    height = lead * wrap_deg / 360.0
    helix = cq.Wire.makeHelix(lead, height, r_root)
    pts = [(r_root - embed, -w_root / 2.0),
           (r_root + depth, -w_crest / 2.0),
           (r_root + depth, w_crest / 2.0),
           (r_root - embed, w_root / 2.0)]
    ridge = (cq.Workplane("XZ")
             .polyline(pts).close()
             .sweep(cq.Workplane(obj=helix), isFrenet=True))
    if phase_deg:
        ridge = ridge.rotate((0, 0, 0), (0, 0, 1), phase_deg)
    if z0:
        ridge = ridge.translate((0, 0, z0))
    return ridge


def tube(od, id_, h, z0=0.0):
    s = cq.Workplane("XY", origin=(0, 0, z0)).circle(od / 2.0)
    if id_ > 0:
        s = s.circle(id_ / 2.0)
    return s.extrude(h)


def cone_cut(d_top, d_bot, z_bot, h):
    """Frustum solid (for chamfer lead-in cuts)."""
    return (cq.Workplane("XZ")
            .polyline([(0, z_bot), (d_bot / 2.0, z_bot),
                       (d_top / 2.0, z_bot + h), (0, z_bot + h)])
            .close().revolve(360, (0, 0, 0), (0, 0, 1)))


# ============================================================================
# PCO-1881 male thread (used by: ref bottle, plug, and — dilated — the female
# socket groove cut). Local frame: neck axis +Z, support ledge at z=0, LIP AT
# z = PCO_X_LIP_TO_LEDGE (17.0). Thread descends from near the lip.
# ============================================================================

def pco_male_ridge(radial_comp=0.0, axial_grow=0.0, wrap_extra_deg=0.0):
    """Male PCO ridge in neck-local coords. radial_comp shrinks (plug) or grows
    (>0 with axial_grow -> female groove cutter). wrap_extra extends the helix
    DOWNWARD in local z (= past the socket entry once inverted)."""
    z_lip = PCO_X_LIP_TO_LEDGE
    z_hi = z_lip - PCO_LIP_TO_THREAD                       # 15.3 upper ridge end
    wrap = PCO_WRAP_DEG + wrap_extra_deg
    height = PCO_PITCH * wrap / 360.0
    z_lo = z_hi - height
    r_root = PCO_E / 2.0 + radial_comp
    depth = PCO_RIDGE_DEPTH + max(0.0, radial_comp) * 0.0  # depth kept nominal
    # for the female cutter we want the OUTER radius grown too:
    return helical_ridge(r_root, depth + (radial_comp if radial_comp > 0 else 0),
                         PCO_RIDGE_W_ROOT + 2 * axial_grow,
                         PCO_RIDGE_W_CREST + 2 * axial_grow,
                         PCO_PITCH, wrap, z0=z_lo)


def build_ref_bottle(with_body=True):
    """Reference bottle neck (+ simplified body) in neck-local coords
    (ledge at z=0, lip at z=17, axis +Z = toward the lip)."""
    z_lip = PCO_X_LIP_TO_LEDGE
    neck = tube(PCO_E, PCO_C, z_lip)                       # neck wall at root Ø
    neck = neck.union(pco_male_ridge(radial_comp=-0.0))
    # ØF/ØG collar between thread start and lip (this is what jams bad caps)
    neck = neck.union(tube(PCO_G_COLLAR, PCO_C, PCO_LIP_TO_THREAD + 0.6,
                           z0=z_lip - PCO_LIP_TO_THREAD - 0.6))
    # TE bead (modeled as full-Ø cylinder over its whole slope zone: conservative)
    bead_z0 = z_lip - PCO_BEAD_BOT_FROM_LIP
    neck = neck.union(tube(PCO_BEAD_D, PCO_C,
                           PCO_BEAD_BOT_FROM_LIP - PCO_BEAD_TOP_FROM_LIP,
                           z0=bead_z0))
    # support ledge (bottom edge at z=0 per X; top at 17-15.24)
    neck = neck.union(tube(PCO_LEDGE_D, PCO_C,
                           PCO_X_LIP_TO_LEDGE - PCO_H_LIP_TO_LEDGE_TOP, z0=0.0))
    if with_body:
        # shoulder + body cylinder, enough for envelope/render purposes
        shoulder = (cq.Workplane("XZ")
                    .polyline([(PCO_LEDGE_D / 2.0, 0), (45.0, -25.0),
                               (45.0, -245.0), (0, -245.0), (0, 0)])
                    .close().revolve(360, (0, 0, 0), (0, 0, 1)))
        neck = neck.union(shoulder)
    return neck


def bottle_world_transform(wp):
    """Neck-local -> body/world coords at the SEATED position:
    invert (rotate 180 about X) then lift so the lip lands on the gasket."""
    return (wp.rotate((0, 0, 0), (1, 0, 0), 180)
              .translate((0, 0, Z_LIP_SEATED + PCO_X_LIP_TO_LEDGE)))


# ============================================================================
# BODY
# ============================================================================

def build_body(fast=False):
    # ---- tray dish ----
    body = cq.Workplane("XY").circle(TRAY_OD / 2.0).extrude(Z_RIM_TOP)
    body = body.cut(tube(TRAY_OD - 2 * TRAY_WALL, 0,
                         Z_RIM_TOP - Z_FLOOR_TOP + 1, z0=Z_FLOOR_TOP))
    # bed-edge chamfer (elephant-foot immunity, fdm-design §9)
    body = body.edges("<Z").chamfer(1.0)

    # ---- hex boss field (anti-drowning footing) ----
    if not fast:
        s = BOSS_AF + BEE_CHANNEL                # hex grid pitch between centers
        r_in = CONE_R0 + 4.0                     # clear of cone base + bubble path
        r_out = TRAY_OD / 2.0 - TRAY_WALL - BOSS_AF / 2.0 - 1.0
        pts = []
        ny = int(TRAY_OD / (s * 0.866)) + 2
        nx = int(TRAY_OD / s) + 2
        for j in range(-ny, ny + 1):
            for i in range(-nx, nx + 1):
                x = (i + (0.5 if j % 2 else 0.0)) * s
                y = j * s * 0.866
                r = math.hypot(x, y)
                if r_in + BOSS_AF / 2.0 <= r <= r_out:
                    pts.append((x, y))
        boss_h = POOL_DEPTH + BOSS_FREEBOARD
        bosses = (cq.Workplane("XY", origin=(0, 0, Z_FLOOR_TOP))
                  .pushPoints(pts)
                  .polygon(6, BOSS_AF / math.cos(math.radians(30)))
                  .extrude(boss_h))
        body = body.union(bosses)

    # ---- rescue ridges (radial, full wall height, climb-out during floods) ----
    for k in range(N_RIDGES):
        ang = 45.0 + k * 360.0 / N_RIDGES
        ridge = (cq.Workplane("XY", origin=(0, 0, Z_FLOOR_TOP))
                 .box(TRAY_OD / 2.0 - CONE_R0, RIDGE_W, WALL_H,
                      centered=(False, True, False))
                 .translate((CONE_R0 - 1.0, 0, 0))
                 .rotate((0, 0, 0), (0, 0, 1), ang))
        body = body.union(ridge)

    # ---- outer-wall climbing ribs ----
    for k in range(N_WALL_RIBS):
        ang = k * 360.0 / N_WALL_RIBS
        rib = (cq.Workplane("XY")
               .box(WALL_RIB_PROUD + 1.0, WALL_RIB_W, Z_RIM_TOP - 1.0,
                    centered=(False, True, False))
               .translate((TRAY_OD / 2.0 - 1.0, 0, 0))
               .rotate((0, 0, 0), (0, 0, 1), ang))
        body = body.union(rib)

    # ---- outlet ribs + column + cone + flange + barrel ----
    for k in range(N_RIBS):
        ang = k * 360.0 / N_RIBS
        rib = (cq.Workplane("XY", origin=(0, 0, Z_FLOOR_TOP))
               .box(COLUMN_OD / 2.0 + 3.5, RIB_W, (Z_MOUTH - Z_FLOOR_TOP) + 3.0,
                    centered=(False, True, False))
               .rotate((0, 0, 0), (0, 0, 1), ang))
        body = body.union(rib)
    body = body.union(tube(COLUMN_OD, 0, Z_CEILING - Z_MOUTH, z0=Z_MOUTH))
    cone = (cq.Workplane("XZ")
            .polyline([(0, Z_CONE_BASE), (CONE_R0, Z_CONE_BASE),
                       (CONE_R1, Z_CEILING), (0, Z_CEILING)])
            .close().revolve(360, (0, 0, 0), (0, 0, 1)))
    body = body.union(cone)
    body = body.union(tube(FLANGE_OD, 0, FLANGE_LAND_H, z0=Z_CEILING - FLANGE_LAND_H))
    # barrel core
    body = body.union(tube(CLAMP_MAJOR_D - 2 * CLAMP_DEPTH, 0,
                           Z_BARREL_TOP - Z_CEILING, z0=Z_CEILING))

    # ---- clamp thread (2 starts, full barrel length) ----
    r_minor = CLAMP_MAJOR_D / 2.0 - CLAMP_DEPTH
    wrap = (Z_BARREL_TOP - 1.5 - (Z_CEILING + 0.5)) / CLAMP_LEAD * 360.0
    for k in range(CLAMP_STARTS):
        ridge = helical_ridge(r_minor, CLAMP_DEPTH, CLAMP_W_ROOT, CLAMP_W_CREST,
                              CLAMP_LEAD, wrap, z0=Z_CEILING + 0.5,
                              phase_deg=k * 360.0 / CLAMP_STARTS)
        body = body.union(ridge)
    # thread lead-in: chamfer the barrel top region by cutting a cone ring
    body = body.cut(
        (cq.Workplane("XZ")
         .polyline([(r_minor + 0.2, Z_BARREL_TOP + 0.01),
                    (CLAMP_MAJOR_D / 2.0 + 1.0, Z_BARREL_TOP + 0.01),
                    (CLAMP_MAJOR_D / 2.0 + 1.0, Z_BARREL_TOP - 3.0)])
         .close().revolve(360, (0, 0, 0), (0, 0, 1))))

    # ---- bore ----
    body = body.cut(tube(BORE_D, 0, Z_BARREL_TOP - Z_MOUTH + 2, z0=Z_MOUTH))

    # ---- socket: entry relief, bore, seat, female PCO groove ----
    body = body.cut(tube(SOCKET_BORE_D, 0, SEAT_DEPTH, z0=Z_SEAT))
    # TE-bead relief + lead-in at the entry (bead reaches the barrel top plane
    # at full crush: lip at 8.8 deep, bead slope starts 9.0 below lip)
    body = body.cut(tube(PCO_BEAD_D + 1.2, 0, 2.0, z0=Z_BARREL_TOP - 2.0))
    body = body.cut(cone_cut(SOCKET_BORE_D + 3.0, SOCKET_BORE_D,
                             Z_BARREL_TOP - 2.6, 2.6))
    # female groove = dilated male ridge, seated transform, wrap extended past entry
    groove = pco_male_ridge(radial_comp=PCO_CLR_RADIAL,
                            axial_grow=PCO_CLR_AXIAL,
                            wrap_extra_deg=540.0)
    groove = bottle_world_transform(groove)
    body = body.cut(groove)

    return body


# ============================================================================
# NUT (modeled in assembly orientation: bearing face DOWN at z=0; printed
# upside-down — the export flips it so the skirt prints support-free)
# ============================================================================

def build_nut():
    r_bore = CLAMP_MAJOR_D / 2.0 - CLAMP_DEPTH + CLAMP_CLR_RADIAL   # 18.5... 18.4+
    nut = cq.Workplane("XY").circle(NUT_OD / 2.0).extrude(NUT_H)
    # grip scallops
    for k in range(NUT_SCALLOP_N):
        ang = math.radians(k * 360.0 / NUT_SCALLOP_N)
        r_c = NUT_OD / 2.0 + NUT_SCALLOP_D / 2.0 - 4.0
        nut = nut.cut(tube(NUT_SCALLOP_D, 0, NUT_H + 2, z0=-1)
                      .translate((r_c * math.cos(ang), r_c * math.sin(ang), 0)))
    # anti-ant / rain skirt: 45° flare, lower edge stops 3 mm above bearing plane
    skirt = (cq.Workplane("XZ")
             .polyline([(NUT_OD / 2.0 - 1.0, NUT_H),
                        (SKIRT_OD / 2.0, NUT_H - SKIRT_DROP),
                        (SKIRT_OD / 2.0, NUT_H - SKIRT_DROP + SKIRT_T * 1.6),
                        (NUT_OD / 2.0 - 1.0, NUT_H + SKIRT_T * 1.6)])
             .close().revolve(360, (0, 0, 0), (0, 0, 1)))
    # keep skirt from poking below bearing plane
    skirt = skirt.cut(cq.Workplane("XY").box(300, 300, 40, centered=(True, True, False))
                      .translate((0, 0, -40 + 3.0)))
    nut = nut.union(skirt)
    # bore + female clamp thread
    nut = nut.cut(tube(2 * r_bore, 0, NUT_H + SKIRT_T * 1.6 + 2, z0=-1))
    wrap = (NUT_H + 4 * CLAMP_LEAD) / CLAMP_LEAD * 360.0
    for k in range(CLAMP_STARTS):
        groove = helical_ridge(r_bore - 0.2, CLAMP_DEPTH + CLAMP_CLR_RADIAL + 0.2,
                               CLAMP_W_ROOT + 2 * CLAMP_CLR_AXIAL,
                               CLAMP_W_CREST + 2 * CLAMP_CLR_AXIAL,
                               CLAMP_LEAD, wrap, z0=-2 * CLAMP_LEAD,
                               phase_deg=k * 360.0 / CLAMP_STARTS)
        nut = nut.cut(groove)
    # lead-in chamfer cones both ends
    nut = nut.cut(cone_cut(2 * r_bore + 3.0, 2 * r_bore, NUT_H - 1.6, 1.7)
                  .translate((0, 0, 0)))
    nut = nut.cut(cone_cut(2 * r_bore, 2 * r_bore + 3.0, -0.1, 1.7))
    return nut


def clamp_nut_phase_deg(z_nut_bottom):
    """Rotation (about +Z, degrees) that phase-aligns the nut's female thread
    with the barrel's male thread when the nut bearing face is at z_nut_bottom.
    Barrel ridge phase 0 starts at Z_CEILING+0.5; nut groove phase 0 at local
    z=-2*CLAMP_LEAD."""
    dz = (z_nut_bottom - 2 * CLAMP_LEAD) - (Z_CEILING + 0.5)
    return (dz / CLAMP_LEAD) * 360.0


# ============================================================================
# GASKET / PLUG / COUPONS / REF ROOF
# ============================================================================

def build_gasket():
    return tube(GASKET_OD, GASKET_ID, GASKET_T)


def build_plug():
    """Bee-tight transport plug: printed male PCO neck stub + grip disc.
    Screws into the socket when the bottle is off; presses the same gasket."""
    plug = cq.Workplane("XY").circle(PLUG_DISC_D / 2.0).extrude(PLUG_DISC_T)
    for k in range(12):
        ang = math.radians(k * 30.0)
        r_c = PLUG_DISC_D / 2.0 + 2.4
        plug = plug.cut(tube(6.0, 0, PLUG_DISC_T + 2, z0=-1)
                        .translate((r_c * math.cos(ang), r_c * math.sin(ang), 0)))
    stub_h = SEAT_DEPTH - GASKET_T + 1.0     # reaches the gasket like the lip does
    plug = plug.union(tube(PCO_E - 2 * PLUG_COMP, 0, stub_h, z0=PLUG_DISC_T))
    # male thread positioned like the bottle's: lip-equivalent = stub top face
    z_lip_eq = PLUG_DISC_T + stub_h
    ridge = pco_male_ridge(radial_comp=-PLUG_COMP)
    # neck-local lip is at PCO_X_LIP_TO_LEDGE; shift so lip lands on z_lip_eq
    ridge = ridge.translate((0, 0, z_lip_eq - PCO_X_LIP_TO_LEDGE))
    plug = plug.union(ridge)
    # entry chamfer on the stub tip (tip is the top face as printed)
    tip_cham = (cq.Workplane("XZ")
                .polyline([(PCO_E / 2.0 - 1.7, z_lip_eq + 0.01),
                           (PCO_E / 2.0 + 1.0, z_lip_eq + 0.01),
                           (PCO_E / 2.0 + 1.0, z_lip_eq - 1.6)])
                .close().revolve(360, (0, 0, 0), (0, 0, 1)))
    plug = plug.cut(tip_cham)
    return plug


def build_roof(thickness, size=140.0):
    slab = (cq.Workplane("XY").box(size, size, thickness,
                                   centered=(True, True, False)))
    slab = slab.cut(tube(ROOF_HOLE_D, 0, thickness + 2, z0=-1))
    return slab


def build_coupons(body, nut):
    """Coupons sliced from the REAL geometry so they test the real fit."""
    big = 400.0
    slab = (cq.Workplane("XY").box(big, big, Z_BARREL_TOP - 56.4,
                                   centered=(True, True, False))
            .translate((0, 0, 56.4)))
    coupon_socket = body.intersect(slab).translate((0, 0, -56.4))
    slab2 = (cq.Workplane("XY").box(big, big, 8.0, centered=(True, True, False))
             .translate((0, 0, 4.0)))
    ring = nut.intersect(slab2)
    # shave the scalloped wheel down to a Ø52 ring so it prints in minutes
    ring = ring.intersect(tube(52.0, 0, 20, z0=0)).translate((0, 0, -4.0))
    return coupon_socket, ring


# ============================================================================
# BUILD + EXPORT
# ============================================================================

def build_all(fast=False):
    parts = {}
    parts["body"] = build_body(fast=fast)
    parts["clamp_nut"] = build_nut()
    parts["gasket_tpu"] = build_gasket()
    parts["plug"] = build_plug()
    parts["ref_bottle"] = bottle_world_transform(build_ref_bottle())
    parts["ref_roof_8"] = build_roof(ROOF_MIN).translate((0, 0, Z_CEILING))
    parts["ref_roof_30"] = build_roof(ROOF_MAX).translate((0, 0, Z_CEILING))
    parts["coupon_socket"], parts["coupon_nut_ring"] = build_coupons(
        parts["body"], parts["clamp_nut"])
    return parts


def export_all(parts):
    tol = dict(tolerance=0.01, angularTolerance=0.1)
    stl_dir = os.path.join(OUT, "stl")
    os.makedirs(stl_dir, exist_ok=True)
    printable = {
        "body": parts["body"],
        # nut prints upside-down (skirt flares upward): flip for the STL
        "clamp_nut": parts["clamp_nut"]
        .rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, NUT_H + SKIRT_T * 1.6)),
        "gasket_tpu": parts["gasket_tpu"],
        "plug": parts["plug"],
        "coupon_socket": parts["coupon_socket"],
        "coupon_nut_ring": parts["coupon_nut_ring"]
        .rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, 8.0)),
    }
    for name, wp in printable.items():
        path = os.path.join(stl_dir, f"{name}.stl")
        cq.exporters.export(wp, path, **tol)
        v = wp.val()
        print(f"exported {name:16s} vol={v.Volume()/1000.0:8.1f} cm3 "
              f"bbox z {v.BoundingBox().zmin:.1f}..{v.BoundingBox().zmax:.1f}")

    # assembly STEP (authoritative), parts at ASSEMBLED positions, roof=20 nominal
    nut_z = Z_CEILING + 20.0
    asm = cq.Assembly(name="nuc_bottle_feeder")
    asm.add(parts["body"], name="body", color=cq.Color("gray"))
    asm.add(parts["clamp_nut"]
            .rotate((0, 0, 0), (0, 0, 1), clamp_nut_phase_deg(nut_z))
            .translate((0, 0, nut_z)), name="clamp_nut", color=cq.Color("orange"))
    asm.add(parts["gasket_tpu"].translate((0, 0, Z_SEAT)),
            name="gasket", color=cq.Color("red"))
    asm.add(parts["plug"].translate((90, 0, 0)), name="plug",
            color=cq.Color("green"))
    asm.save(os.path.join(OUT, "feeder.step"))
    print("exported feeder.step (assembly, roof=20 nominal)")


if __name__ == "__main__":
    import sys
    fast = "--fast" in sys.argv
    parts = build_all(fast=fast)
    export_all(parts)
    print("Z stack: floor", Z_FLOOR_TOP, "mouth", Z_MOUTH, "rim", Z_RIM_TOP,
          "ceiling", Z_CEILING, "seat", Z_SEAT, "lip", Z_LIP_SEATED,
          "barrel_top", Z_BARREL_TOP)
