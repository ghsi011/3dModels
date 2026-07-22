# FreeCAD macro — regenerates the sprayer handle + clamp fastener (wing bolt & wing nut).
# Edit the numbers in P, run in FreeCAD (Macro > Macros... > Execute), then re-export STLs
# (select each object -> File > Export), or just re-run: it saves the FCStd automatically.

import FreeCAD as App
import Part, os, math
from FreeCAD import Vector

P = dict(
    tube_od     = 58.9,   # OD of tube/coupling the collar clamps
    fit_clr     = 0.6,    # bore clearance for print fit
    wall        = 6.0,    # collar wall thickness
    collar_w    = 32.0,   # collar width along the tube
    grip_d      = 29.4,   # grip diameter
    grip_len    = 143.6,  # straight grip section
    grip_angle  = 70.0,   # grip angle from the tube axis (deg)
    flare_d     = 40.0,   # base flare diameter where grip meets collar
    flare_len   = 45.0,   # flare (cone) length
    slit_w      = 4.0,    # clamp slit gap
    ear_w       = 12.0,   # each bolt ear width
    ear_drop    = 32.0,   # ears extend below collar (deep enough for wing clearance)
    bolt_hole_d = 11.4,   # ear through-hole (clears the 10.6 thread OD; metal M6+washers also fits)
    thr_core_d  = 8.0,    # fastener thread core diameter
    thr_depth   = 1.3,    # thread depth (OD ~10.6)
    thr_pitch   = 3.0,    # coarse printable pitch
    thr_clr     = 0.3,    # radial clearance for the nut thread
    nut_h       = 12.0,   # wing nut thickness
    wing_span   = 34.0,   # wing span on both bolt head and nut
)
OUTDIR = 'C:/github/3D/Sprayer handle'

bore_r = (P['tube_od'] + P['fit_clr']) / 2.0
out_r  = bore_r + P['wall']
grip_r = P['grip_d'] / 2.0
rc     = P['thr_core_d'] / 2.0

DOC = "SprayerHandle"
if DOC in App.listDocuments():
    App.closeDocument(DOC)
doc = App.newDocument(DOC)

# ---------- handle ----------
ring = Part.makeCylinder(out_r, P['collar_w'], Vector(-P['collar_w']/2, 0, 0), Vector(1, 0, 0))
ear_h = P['ear_drop'] + 8.0
ear1 = Part.makeBox(P['collar_w'], P['ear_w'], ear_h,
                    Vector(-P['collar_w']/2,  P['slit_w']/2, -(out_r + P['ear_drop'])))
ear2 = Part.makeBox(P['collar_w'], P['ear_w'], ear_h,
                    Vector(-P['collar_w']/2, -P['slit_w']/2 - P['ear_w'], -(out_r + P['ear_drop'])))
ang = math.radians(P['grip_angle'])
dirv = Vector(math.cos(ang), 0, math.sin(ang))
anchor = Vector(0, 0, 5.0)
flare = Part.makeCone(P['flare_d']/2, grip_r, P['flare_len'], anchor, dirv)
gstart = anchor.add(Vector(dirv).multiply(P['flare_len']))
grip = Part.makeCylinder(grip_r, P['grip_len'], gstart, dirv)
tip  = Part.makeSphere(grip_r, gstart.add(Vector(dirv).multiply(P['grip_len'])))
solid = ring.fuse(ear1).fuse(ear2).fuse(flare).fuse(grip).fuse(tip)
bore = Part.makeCylinder(bore_r, 300, Vector(-150, 0, 0), Vector(1, 0, 0))
slit = Part.makeBox(P['collar_w'] + 4, P['slit_w'], out_r + P['ear_drop'] + 6 - (bore_r - 1),
                    Vector(-P['collar_w']/2 - 2, -P['slit_w']/2, -(out_r + P['ear_drop'] + 6)))
bolt_hole = Part.makeCylinder(P['bolt_hole_d']/2, 60, Vector(0, -30, -(out_r + P['ear_drop']/2)), Vector(0, 1, 0))
handle_shape = solid.cut(bore).cut(slit).cut(bolt_hole).removeSplitter()

# ---------- thread helper (trimmed helical sweep) ----------
def thread_solid(r_core, depth, pitch, length):
    helix = Part.makeHelix(pitch, length + 2*pitch, r_core)
    prof = Part.makePolygon([
        Vector(r_core - 0.5, 0, -pitch * 0.3),
        Vector(r_core - 0.5, 0,  pitch * 0.3),
        Vector(r_core + depth, 0, 0),
        Vector(r_core - 0.5, 0, -pitch * 0.3)])
    sweep = Part.Wire(helix).makePipeShell([Part.Wire(prof)], True, True)
    trim = Part.makeCylinder(r_core + depth + 1, length, Vector(0, 0, pitch))
    thr = sweep.common(trim)
    thr.translate(Vector(0, 0, -pitch))
    return thr.fuse(Part.makeCylinder(r_core, length))

# ---------- wing bolt (fully threaded so it passes the ear holes) ----------
wr = P['wing_span'] / 2.0
thr_len = 44.0
head = Part.makeCylinder(8.0, 8.0, Vector(0, 0, -8))
wing = Part.makeBox(5.0, P['wing_span'], 8.0, Vector(-2.5, -wr, -8))
thr = thread_solid(rc, P['thr_depth'], P['thr_pitch'], thr_len)
tipc = Part.makeCone(rc, rc - 1.5, 2.0, Vector(0, 0, thr_len))
bolt_shape = head.fuse(wing).fuse(thr).fuse(tipc)
if not bolt_shape.isValid():
    bolt_shape.fix(0.1, 0.1, 0.1)
bolt_shape = bolt_shape.removeSplitter()

# ---------- wing nut ----------
hub = Part.makeCylinder(9.0, P['nut_h'])
nwing = Part.makeBox(5.0, P['wing_span'], P['nut_h'], Vector(-2.5, -wr, 0))
cutter = thread_solid(rc + P['thr_clr'], P['thr_depth'], P['thr_pitch'], P['nut_h'] + 2*P['thr_pitch'])
cutter.translate(Vector(0, 0, -P['thr_pitch']))
nut_shape = hub.fuse(nwing).cut(cutter)
if not nut_shape.isValid():
    nut_shape.fix(0.1, 0.1, 0.1)
nut_shape = nut_shape.removeSplitter()

# display placement beside the handle
bolt_shape.rotate(Vector(0,0,0), Vector(1,0,0), -90)
bolt_shape.translate(Vector(0, -55, -(out_r + P['ear_drop']/2)))
nut_shape.rotate(Vector(0,0,0), Vector(1,0,0), 90)
nut_shape.translate(Vector(0, 55, -(out_r + P['ear_drop']/2)))

oh = doc.addObject('Part::Feature', 'Handle');   oh.Shape = handle_shape
ob = doc.addObject('Part::Feature', 'WingBolt'); ob.Shape = bolt_shape
on = doc.addObject('Part::Feature', 'WingNut');  on.Shape = nut_shape
doc.recompute()
doc.saveAs(os.path.join(OUTDIR, 'sprayer_handle.FCStd'))

import MeshPart
for o, fn in ((oh, 'sprayer_handle.stl'), (ob, 'clamp_wing_bolt.stl'), (on, 'clamp_wing_nut.stl')):
    m = MeshPart.meshFromShape(Shape=o.Shape, LinearDeflection=0.05, AngularDeflection=0.35, Relative=False)
    m.write(os.path.join(OUTDIR, fn))
Part.export([oh, ob, on], os.path.join(OUTDIR, 'sprayer_handle.step'))
print('done')
