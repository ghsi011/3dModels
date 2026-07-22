"""
Beach Headrest + Sunshade -- parametric printed parts (CadQuery).

Architecture: "node and strut".  Long straight members (legs optional,
crossbeams, shade arms, shade-frame rails) are commodity 16 mm tubes / dowels.
All the clever, load-bearing geometry is printed: the adjustable apex CLUTCH,
the sand ANCHOR FEET, the fabric RAIL, the quick-release CROSSBEAM fittings,
the captive PIN, and the SHADE pivot + corners.

Every printed part fits inside the X2D 256^3 build volume and is oriented for
minimal supports.  Units = mm.  Run:  python parts.py
"""
import math
import os
import cadquery as cq

# ============================================================
# GLOBAL PARAMETERS  -- edit these to re-size the whole product
# ============================================================
# ---- overall stance / ergonomics ----
TRACK_WIDTH      = 360.0   # centreline spacing of the two side frames (= crossbeam span)
FRONT_LEG_LEN    = 250.0   # apex -> front foot   (<=256 so it can be a printed leg too)
REAR_LEG_LEN     = 230.0   # apex -> rear foot
FRONT_LEG_ANGLE  = 30.0    # deg from vertical, leaning toward the body (+X)
# rear angle is derived so both feet sit on the ground (see assembly.py)

# ---- struts (commodity tube/dowel stock) ----
TUBE_OD          = 16.0    # aluminium or fibreglass tube outside diameter
TUBE_ID          = 12.0    # nominal inside diameter (for plug fittings)
PIN_D            = 6.0     # quick-release pin (printed PETG or 6 mm stainless)

# ---- structural print defaults ----
WALL             = 3.4     # structural wall thickness (>= 2.4)
FILLET           = 2.0     # general cosmetic/strength fillet

# ---- tolerances (beach / sand tolerant -> generous) ----
CLR_SLIDE        = 0.30    # sliding printed joints
CLR_SAND         = 0.55    # sand-exposed sliding joints (tube into socket)
CLR_PIN          = 0.40    # pin through hole

# ---- apex CLUTCH (serrated face coupling) ----
CLUTCH_D         = 58.0    # serrated disc outer diameter
CLUTCH_TEETH     = 24      # -> 360/24 = 15 deg adjustment increments
CLUTCH_TOOTH_H   = 3.2     # tooth height (engagement depth)
CLUTCH_BASE_H    = 7.0     # solid disc behind the teeth
CLUTCH_BOLT_D    = 6.4     # M6 clutch bolt clearance
CLUTCH_SPIGOT_D  = 16.0    # centring spigot diameter (male hub)
CLUTCH_HUB_TONGUE_W = 22.0 # width of the flat tongue that joins the leg
CLUTCH_HUB_TONGUE_L = 46.0 # tongue length (overlap into the leg fork)
CLUTCH_HUB_TONGUE_T = 11.0 # tongue thickness

# ---- anchor feet (sand spades) ----
# The spade is COLLINEAR with the leg (runs at the leg angle), so it drives
# deep along the leg line and a full inclined wedge of sand loads its top face.
# Cruciform = broad ballast plate (sand weight) + keel fin (lateral stability),
# both tapering to a shared point.  The part is leg-angle independent.
FOOT_SOCK_DEPTH  = 48.0    # how deep the leg/tube sits in the socket
FOOT_BLADE_T     = 6.0     # plate / keel thickness
FOOT_BLADE_W_F   = 82.0    # FRONT ballast-plate width (broad -> big sand column)
FOOT_BLADE_L_F   = 120.0   # FRONT spade length along the leg axis (drives deep)
FOOT_KEEL_W_F    = 46.0    # FRONT keel-fin span (lateral grip)
FOOT_BLADE_W_R   = 62.0    # REAR ballast-plate width
FOOT_BLADE_L_R   = 130.0   # REAR spade length (deeper, anti-tip)
FOOT_KEEL_W_R    = 60.0    # REAR keel-fin span (bigger -> more anti-wobble)
FOOT_TIP_FRAC    = 0.32    # tip width as fraction of base (taper to a point)

# ---- fabric rail (head cloth C-channel) ----
# Cloth spans the ENTIRE front face of the triangles: the rail runs almost the
# full front-leg length, so the side hems are captured top-to-bottom.
RAIL_LEN         = 215.0   # captured length along the front leg (~full leg)
RAIL_BORE_D      = 9.0     # holds the rod/cord hem of the fabric edge
RAIL_SLOT_W      = 5.0     # mouth the fabric passes through
RAIL_BACK_T      = 4.0     # back wall thickness

# ---- shade ----
# Default orientation is HORIZONTAL (panel parallel to the ground); the pivot
# allows only a limited tilt either way, which also keeps wind leverage low.
SHADE_CLUTCH_D   = 46.0    # shade pivot (friction) disc
SHADE_TILT_RANGE = 30.0    # deg of tilt allowed EACH WAY from horizontal
SHADE_HEIGHT     = 205.0   # frame height above the apex (head clearance)
SHADE_FRAME_W    = 520.0   # shade panel width  (tube, lateral)
SHADE_FRAME_D    = 460.0   # shade panel depth  (tube, fore-aft over the body)

# ---- derived stance geometry (both feet on the ground) ----
APEX_Z = FRONT_LEG_LEN * math.cos(math.radians(FRONT_LEG_ANGLE))
REAR_LEG_ANGLE = math.degrees(math.acos(APEX_Z / REAR_LEG_LEN))  # from vertical

OUT = os.path.join(os.path.dirname(__file__), "stl")
os.makedirs(OUT, exist_ok=True)


# ============================================================
# REUSABLE: serrated face-clutch disc (Hirth-style dog coupling)
# Printed teeth-up: flat top teeth + vertical radial flanks => zero supports.
# ============================================================
def serrated_disc(disc_d, n_teeth, tooth_h, base_h, bore_d,
                  tooth_inner_r=8.0, tooth_frac=0.46):
    R = disc_d / 2.0
    base = cq.Workplane("XY").circle(R).extrude(base_h)
    pitch = 360.0 / n_teeth
    half = pitch * tooth_frac          # angular half-width of one tooth (with backlash)
    teeth = None
    for i in range(n_teeth):
        a = math.radians(half)
        pts = [(tooth_inner_r, 0.0),
               (R, 0.0),
               (R * math.cos(a), R * math.sin(a)),
               (tooth_inner_r * math.cos(a), tooth_inner_r * math.sin(a))]
        t = (cq.Workplane("XY").workplane(offset=base_h)
             .polyline(pts).close().extrude(tooth_h)
             .rotate((0, 0, 0), (0, 0, 1), i * pitch - half / 2.0))
        teeth = t if teeth is None else teeth.union(t)
    disc = base.union(teeth)
    disc = disc.cut(cq.Workplane("XY").circle(bore_d / 2.0).extrude(base_h + tooth_h + 1))
    return disc


# ============================================================
# PART: apex hub  (male = front leg side, female = rear leg side)
# disc + centring spigot/recess + flat tongue to fork into the leg
# ============================================================
def apex_hub(male=True):
    R = CLUTCH_D / 2.0
    hub = serrated_disc(CLUTCH_D, CLUTCH_TEETH, CLUTCH_TOOTH_H,
                        CLUTCH_BASE_H, CLUTCH_BOLT_D)
    top = CLUTCH_BASE_H + CLUTCH_TOOTH_H
    if male:
        # centring spigot rises above the teeth
        spg = (cq.Workplane("XY").workplane(offset=top)
               .circle(CLUTCH_SPIGOT_D / 2.0).extrude(CLUTCH_TOOTH_H + 1.5))
        spg = spg.cut(cq.Workplane("XY").circle(CLUTCH_BOLT_D / 2.0)
                      .extrude(top + CLUTCH_TOOTH_H + 2))
        hub = hub.union(spg)
    else:
        # female recess to receive the spigot
        rec = (cq.Workplane("XY").workplane(offset=top - (CLUTCH_TOOTH_H + 1.8))
               .circle((CLUTCH_SPIGOT_D + 2 * CLR_SLIDE) / 2.0)
               .extrude(CLUTCH_TOOTH_H + 3))
        hub = hub.cut(rec)
        # counterbore on the back for the wing-knob nut capture
        cb = (cq.Workplane("XY").circle(12.0 / 2.0).extrude(4.0))
        hub = hub.cut(cb)

    # flat tongue extending radially (+X) in the base plane -> leg fork
    tw, tl, tt = CLUTCH_HUB_TONGUE_W, CLUTCH_HUB_TONGUE_L, CLUTCH_HUB_TONGUE_T
    tongue = (cq.Workplane("XY")
              .moveTo(R - 6 + tl / 2.0, 0)
              .rect(tl + 12, tw).extrude(tt)
              .edges("|Z").fillet(6.0))
    # pin hole through tongue (vertical in print => lateral pin in use)
    tongue = tongue.faces(">Z").workplane().pushPoints(
        [(R - 6 + tl - 8, 0)]).hole(PIN_D + CLR_PIN)
    hub = hub.union(tongue)
    return hub


# ============================================================
# PART: sand anchor foot  -- collinear cruciform spade
# Socket and spade share ONE axis (the leg axis), so the spade drives deep
# along the leg and a full inclined wedge of sand loads its top face.
# Built in PRINT pose: socket flat on the bed (z=0..D), spade tapering UP to a
# point -> every layer is narrower than the one below = zero supports, wide
# stable base.  (In use it is simply inverted: socket up, spade down in sand.)
# ============================================================
def _tapered_plate(thick, base_w, tip_w, length, z0):
    """flat plate, thickness in X, width in Y, tapering width over +Z length."""
    return (cq.Workplane("XY").workplane(offset=z0).rect(thick, base_w)
            .workplane(offset=length).rect(thick, tip_w)
            .loft(combine=True))


def anchor_foot(front=True):
    blade_w = FOOT_BLADE_W_F if front else FOOT_BLADE_W_R
    blade_l = FOOT_BLADE_L_F if front else FOOT_BLADE_L_R
    keel_w  = FOOT_KEEL_W_F if front else FOOT_KEEL_W_R
    t = FOOT_BLADE_T
    sock_od = TUBE_OD + 2 * WALL
    D = FOOT_SOCK_DEPTH

    # socket (bed face at z=0); bore opens downward, 6 mm floor under the spade
    foot = cq.Workplane("XY").circle(sock_od / 2.0).extrude(D)
    foot = foot.faces("<Z").workplane().hole(TUBE_OD + 2 * CLR_SAND, D - 6)
    # transverse drain / clean-out so wet sand washes out of the socket
    foot = foot.cut(cq.Workplane("YZ").workplane(offset=-sock_od)
                    .center(D - 3, 0).circle(2.5).extrude(2 * sock_od))

    # cruciform spade rising from z=D, tapering to a point at z=D+blade_l
    tipw_b = blade_w * FOOT_TIP_FRAC
    tipw_k = keel_w * FOOT_TIP_FRAC
    ballast = _tapered_plate(t, blade_w, tipw_b, blade_l, D)          # broad: sand ballast
    keel = (_tapered_plate(t, keel_w, tipw_k, blade_l, D)
            .rotate((0, 0, 0), (0, 0, 1), 90))                       # crossed: lateral grip
    foot = foot.union(ballast).union(keel)

    # sand-grip / drainage perforations through the ballast plate (X-axis holes)
    for f in (0.34, 0.60):
        z = D + blade_l * f
        foot = foot.cut(cq.Workplane("YZ").workplane(offset=-t)
                        .center(0, z).circle(4.0).extrude(2 * t))
    return foot


# ============================================================
# PART: fabric rail  (keyhole C-channel; rod-hem of the sling slides in)
# Constant cross-section extruded in Z -> perfect vertical print, no supports.
# ============================================================
def fabric_rail():
    br = RAIL_BORE_D / 2.0
    outer_w = RAIL_BORE_D + 2 * RAIL_BACK_T
    # cross-section: a back slab + a round bore tube with a slot mouth
    sec = (cq.Workplane("XY")
           .moveTo(0, 0).rect(RAIL_BACK_T, outer_w)            # back slab
           .extrude(RAIL_LEN))
    tube = (cq.Workplane("XY").center(RAIL_BACK_T / 2 + br, 0)
            .circle(br + RAIL_BACK_T).extrude(RAIL_LEN))
    rail = sec.union(tube)
    # bore + slot mouth (open toward +X)
    rail = rail.cut(cq.Workplane("XY").center(RAIL_BACK_T / 2 + br, 0)
                    .circle(br).extrude(RAIL_LEN))
    rail = rail.cut(cq.Workplane("XY")
                    .center(RAIL_BACK_T / 2 + br + br, 0)
                    .rect(2 * br, RAIL_SLOT_W).extrude(RAIL_LEN))
    # two snap tabs on the back to clip onto the front leg (printed in line)
    return rail


# ============================================================
# PART: crossbeam end fitting (tube plug + flat tongue + pins)
# ============================================================
def crossbeam_fitting():
    plug_d = TUBE_ID - CLR_SLIDE
    plug = (cq.Workplane("XY").circle(plug_d / 2.0).extrude(34)
            .faces(">Z").workplane().hole(PIN_D + CLR_PIN))  # cross-pin into tube
    collar = (cq.Workplane("XY").workplane(offset=34)
              .circle((TUBE_OD + 2 * WALL) / 2.0).extrude(6)
              .edges(">Z").chamfer(1.5))
    tongue = (cq.Workplane("XY").workplane(offset=34 + 6)
              .rect(CLUTCH_HUB_TONGUE_W, 12).extrude(40)
              .edges("|X").fillet(4.0))
    tongue = tongue.faces(">Z").workplane().hole(PIN_D + CLR_PIN)
    return plug.union(collar).union(tongue)


# ============================================================
# PART: captive quick-release pin (head + shaft + tether eye)
# ============================================================
def captive_pin():
    shaft = cq.Workplane("XY").circle(PIN_D / 2.0).extrude(34)
    head = (cq.Workplane("XY").workplane(offset=34)
            .circle(PIN_D).extrude(5).edges(">Z").fillet(2.0))
    eye = (cq.Workplane("XZ").workplane(offset=0)
           .center(0, 34 + 9).circle(4).extrude(3, both=True))
    eye = eye.cut(cq.Workplane("XZ").center(0, 34 + 9).circle(2).extrude(4, both=True))
    return shaft.union(head).union(eye)


# ============================================================
# PART: shade frame corner  (two 90 deg tube sockets + clip ear)
# ============================================================
def shade_corner():
    sock_od = TUBE_OD + 2 * (WALL - 0.6)
    a = (cq.Workplane("XY").circle(sock_od / 2.0).extrude(40)
         .faces(">Z").workplane().hole(TUBE_OD + CLR_SAND, 34))
    b = (cq.Workplane("YZ").circle(sock_od / 2.0).extrude(-40)
         .faces("<X").workplane().hole(TUBE_OD + CLR_SAND, 34))
    corner = a.union(b)
    return corner


# ============================================================
# PART: shade pivot  -- FRICTION disc + limited-travel arc-slot stop
# Light load, fine adjustment, default HORIZONTAL.  A fixed pin from the apex
# boss rides the arc slot; the slot ends are hard stops at +/- SHADE_TILT_RANGE.
# Prints flat (disc on bed): bolt bore, arc slot and tongue pin are all vertical.
# ============================================================
def shade_clutch():
    R = SHADE_CLUTCH_D / 2.0
    base_h = 7.0
    d = cq.Workplane("XY").circle(R).extrude(base_h)
    # concentric friction grooves on the clamp face (some grip, no hard detents)
    for rr in (R - 5, R - 11):
        d = d.cut(cq.Workplane("XY").workplane(offset=base_h - 0.8)
                  .circle(rr + 0.6).circle(rr - 0.6).extrude(1.0))
    d = d.cut(cq.Workplane("XY").circle(CLUTCH_BOLT_D / 2.0).extrude(base_h + 1))
    # limited-tilt arc slot (rounded ends): fixed pin from the mount rides here
    r_slot = R - 9
    slot_w = PIN_D + CLR_PIN + 0.4
    cutter = None
    n = 18
    for i in range(n + 1):
        ang = math.radians(-SHADE_TILT_RANGE + 2 * SHADE_TILT_RANGE * i / n)
        c = (cq.Workplane("XY")
             .center(r_slot * math.cos(ang), r_slot * math.sin(ang))
             .circle(slot_w / 2.0).extrude(base_h + 1))
        cutter = c if cutter is None else cutter.union(c)
    d = d.cut(cutter)
    # arm tongue (the shade arm end-fitting forks onto this and pins) -- same
    # quick-release motif as everywhere else
    tongue = (cq.Workplane("XY").moveTo(R + 14, 0)
              .rect(44, 16).extrude(10).edges("|Z").fillet(5.0))
    tongue = tongue.faces(">Z").workplane().hole(PIN_D + CLR_PIN)
    return d.union(tongue)


# ============================================================
# EXPORT ALL
# ============================================================
PARTS = {
    "apex_hub_front":   lambda: apex_hub(male=True),
    "apex_hub_rear":    lambda: apex_hub(male=False),
    "foot_front":       lambda: anchor_foot(front=True),
    "foot_rear":        lambda: anchor_foot(front=False),
    "fabric_rail":      fabric_rail,
    "crossbeam_fitting": crossbeam_fitting,
    "captive_pin":      captive_pin,
    "shade_corner":     shade_corner,
    "shade_clutch":     shade_clutch,
}

if __name__ == "__main__":
    for name, fn in PARTS.items():
        try:
            solid = fn()
            path = os.path.join(OUT, name + ".stl")
            cq.exporters.export(solid, path, tolerance=0.01, angularTolerance=0.1)
            step_dir = os.path.join(os.path.dirname(__file__), "step")
            os.makedirs(step_dir, exist_ok=True)
            cq.exporters.export(solid, os.path.join(step_dir, name + ".step"))
            bb = solid.val().BoundingBox()
            print(f"OK  {name:18s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm"
                  f"  -> {path}")
        except Exception as e:
            print(f"ERR {name:18s} {type(e).__name__}: {e}")
