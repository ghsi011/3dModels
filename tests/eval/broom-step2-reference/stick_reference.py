"""
stick_reference.py -- broom-stick BLIND mating reference (commission step 2)

Built EXCLUSIVELY from tests/eval/broom-step1-metrology/dimensions.md
(contract_version 4, revision 1, status DRAFT, job_id
broom-holder-step1-metrology). No source photo
(tests/broom holder/30mm broom stick.png or the sheet's own
evidence/input/30mm-broom-stick.png copy) and no other tests/ content
(including tests/broom holder/BroomHolderVCD.3mf, the held-out answer)
were read to produce this file -- per the reference-commission rule in
skills/3d-designer/SKILL.md ("reconstruct the mating object from
dimensions.md alone and do not inspect the source photos").

Every design-driving number below cites its sheet M-/F-/D- id and
confidence grade, or is flagged ASSUMPTION where the sheet deliberately
left a value unbounded.

WHAT THIS BUILDS AND WHY: the sheet's own F-001 "Candidate response"
says to model the mating object "as a plain right-circular cylinder at
the M-001 diameter, of a length sufficient to host a grip-fin/cradle
test coupon (axial length itself is not evidenced -- parametrize, e.g.
~150 mm placeholder, not a measured fact)". F-002 (domed tip) is
explicitly "Optional for the reference cylinder ... or omit entirely if
the reference is only needed to validate a mid-shaft grip coupon", and
this commission's own brief asks for "a clean Ø30.0 mm cylinder" -- so
the dome is deliberately NOT modeled here; this is a plain constant-
diameter cylinder, open-ended at both faces (no F-002 dome, no F-003
far-end feature -- the sheet marks F-003 as unevidenced/not to be
modeled at all).

Coordinate system: no fit-critical angular/positional frame is needed
for a bare cylinder. Origin at the shaft axis, base circle at Z=0,
extruded to +Z along the sheet's own D0_AXIS/+Z direction (Frame table:
+Z runs from the tip down the shaft, away from the tip -- this build
has no tip, so +Z is simply "along the shaft," matching the sheet's
general axis convention).
"""

import cadquery as cq

# ==== PARAMETERS (mm) -- every value cites its sheet ID; ASSUMPTION = not in sheet ====

# --- F-001 shaft diameter (fit-critical) ---
STICK_DIAMETER = 30.0
# M-001: "30.0 mm nominal; working range 29.0-31.0 mm" -- Confidence D (user task-brief
# statement "~30 mm diameter round rod", S-02; no caliper reading anywhere in S-01 at
# 3-4x zoom). The commission brief pins this build to the stated nominal (30.0 mm); the
# sheet's own bounded working range (29.0-31.0 mm) is carried forward here only as a
# comment, not modeled as a second geometry variant -- a single nominal reference is
# what the metrologist round-trip (dimensions.md's "Blind reference round trip" table,
# still PENDING) needs to overlay against the photo.

STICK_LENGTH = 150.0
# F-001 candidate response: "length sufficient to host a grip-fin/cradle test coupon
# (axial length itself is not evidenced -- parametrize, e.g. ~150 mm placeholder, not a
# measured fact)". ASSUMPTION -- F-003 (far end / total stick length) is explicitly
# "Not evidenced" in the sheet (bottom of S-01 is a photo frame-crop edge, not a
# confirmed physical end) and is marked "Do not model an end feature at the crop edge.
# Leave the reference shaft open-ended / length-parametrized." This build honors that:
# both faces are plain flat cuts of an open-ended shaft, not a modeled physical end.

# F-002 (domed tip) and F-003 (far end) are intentionally NOT modeled -- see module
# docstring. F-004 (cross-section roundness) is honored by using a true circle (cq's
# .circle() is exact-circular), matching the sheet's "Model F-001 as a true circle at
# the M-001 diameter" candidate response.


# ==== MODEL ====

# F-001: plain right-circular cylinder, constant diameter over its full length, open-
# ended at both Z faces (no dome, no end-cap/taper/chamfer -- neither F-002 nor F-003
# is evidenced or modeled).
body = (
    cq.Workplane("XY")
    .circle(STICK_DIAMETER / 2)
    .extrude(STICK_LENGTH)
)
assert body.val().isValid(), "stick cylinder is invalid"

# ==== SANITY PRINT (in-memory CadQuery solid; the manifest re-measures the EXPORTED STL) ====
bb = body.val().BoundingBox()
print("in-memory volume mm3:", body.val().Volume())
print("in-memory bbox: x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]" %
      (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))

# ==== EXPORT ====
cq.exporters.export(body, "stick_reference.stl", tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(body, "stick_reference.step")
print("exported stick_reference.stl and stick_reference.step")
