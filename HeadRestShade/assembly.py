"""
Schematic assembly of the beach headrest + sunshade.
Struts shown as primitives so the overall stance / form reads clearly.
Coordinates:  +X = toward the user's body/feet,  +Z = up,  Y = lateral.
Exports stl/assembly.stl  (for a single overview render only -- not for print).
"""
import math
import cadquery as cq
import parts as P

th_f = math.radians(P.FRONT_LEG_ANGLE)
apex_z = P.FRONT_LEG_LEN * math.cos(th_f)
front_x = P.FRONT_LEG_LEN * math.sin(th_f)
cos_r = apex_z / P.REAR_LEG_LEN
th_r = math.acos(cos_r)
rear_x = -P.REAR_LEG_LEN * math.sin(th_r)
half = P.TRACK_WIDTH / 2.0
r_leg = 8.0

print(f"apex_z={apex_z:.1f}  front_x={front_x:.1f}  rear_x={rear_x:.1f}  "
      f"apex_angle={math.degrees(th_f+th_r):.1f} deg")


def rod(p0, p1, r=8.0):
    """solid cylinder between two 3D points"""
    v = cq.Vector(*[b - a for a, b in zip(p0, p1)])
    L = v.Length
    d = v.normalized()
    base = cq.Workplane("XY").circle(r).extrude(L)
    ax = cq.Vector(0, 0, 1).cross(d)
    ang = math.degrees(math.acos(max(-1, min(1, d.z))))
    if ax.Length > 1e-6:
        base = base.rotate((0, 0, 0), (ax.x, ax.y, ax.z), ang)
    return base.translate(p0)


_solids = []


def add(s):
    # schematic only: collect solids, do NOT boolean-fuse (thin coplanar
    # panels make fusing fail).  Exported as one compound for rendering.
    _solids.extend(s.solids().vals())


apex = (0, 0, apex_z)
for s in (+1, -1):
    y = s * half
    A = (0, y, apex_z)
    Ff = (front_x, y, 0)
    Fr = (rear_x, y, 0)
    add(rod(A, Ff, r_leg))                       # front leg
    add(rod(A, Fr, r_leg))                        # rear leg
    # apex hub disc
    add(cq.Workplane("XY").circle(P.CLUTCH_D / 2).extrude(12)
        .rotate((0, 0, 0), (1, 0, 0), 90).translate((0, y - 6 * s, apex_z)))
    # feet (simple wedge spades)
    for fx, fwd in ((front_x, 1), (rear_x, -1)):
        add(cq.Workplane("XY").box(70 * 1.0, 70, P.FOOT_BLADE_T)
            .translate((fx + fwd * 25, y, -3)))
        add(cq.Workplane("XY").circle(11).extrude(40).translate((fx, y, 0)))

# crossbeams (apex / front-foot / rear-foot)
add(rod((0, -half, apex_z), (0, half, apex_z), P.TUBE_OD / 2))
add(rod((front_x, -half, 0), (front_x, half, 0), P.TUBE_OD / 2))
add(rod((rear_x, -half, 0), (rear_x, half, 0), P.TUBE_OD / 2))

# head cloth: spans the ENTIRE front face of the triangles (apex -> front feet,
# full width), forming a sloped head+neck+upper-back support surface.
t1, t2 = 0.08, 0.93   # fraction of the front leg covered by cloth (near full)
pa = (front_x * t1, apex_z * (1 - t1))
pb = (front_x * t2, apex_z * (1 - t2))
# build the cloth as a thin slab in the plane of the two front legs
clothL = (cq.Workplane("XY")
          .polyline([(pa[0], -half + 12), (pb[0], -half + 12),
                     (pb[0], half - 12), (pa[0], half - 12)]).close()
          .extrude(3))
# rotate the flat panel into the front-leg plane (lean it back by the leg angle)
clothL = (clothL.rotate((0, 0, 0), (0, 1, 0), math.degrees(th_f))
          .translate((0, 0, 0)))
# position so its top edge sits near the apex, bottom near the front feet
clothL = clothL.translate((pa[0], 0, pa[1] - 6))
add(clothL)

# shade arms + frame  -- DEFAULT HORIZONTAL, mounted at the apex clutch
sh_z = apex_z + P.SHADE_HEIGHT          # frame height above ground
fd = P.SHADE_FRAME_D                    # fore-aft (over the body, +X)
fw = P.SHADE_FRAME_W / 2                # half lateral width
x_near = -20.0                          # rear rail just behind the apex
x_far = x_near + fd                     # front rail out over the chest
for s in (+1, -1):
    y = s * half
    add(rod((0, y, apex_z), (x_near, y, sh_z), 7))   # short arm up to rear rail
# horizontal frame rails
add(rod((x_near, -fw, sh_z), (x_near, fw, sh_z), P.TUBE_OD / 2))   # rear rail
add(rod((x_far, -fw, sh_z), (x_far, fw, sh_z), P.TUBE_OD / 2))     # front rail
add(rod((x_near, -fw, sh_z), (x_far, -fw, sh_z), P.TUBE_OD / 2))   # side rail L
add(rod((x_near, fw, sh_z), (x_far, fw, sh_z), P.TUBE_OD / 2))     # side rail R
# horizontal shade panel
panel = (cq.Workplane("XY").box(fd, P.SHADE_FRAME_W, 2)
         .translate(((x_near + x_far) / 2, 0, sh_z)))
add(panel)

asm = cq.Compound.makeCompound(_solids)
cq.exporters.export(asm, "stl/assembly.stl", tolerance=0.02, angularTolerance=0.2)
bb = asm.BoundingBox()
print(f"assembly: {len(_solids)} solids  bbox  "
      f"{bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f} mm  "
      f"(packed size is far smaller -- this is the deployed stance)")
