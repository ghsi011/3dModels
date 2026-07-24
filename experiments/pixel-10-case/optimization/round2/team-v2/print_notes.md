---
artifact: p2-final-print-prep
revision: 1
owner: print-engineer
status: PHYSICAL_PRINT_PENDING
candidate_stl_sha256: 255945baa7ab980fb6d43a092cb1a36307e09dd20a53b9c26e971f82f7905960
print_plan_revision: 4
verification_report_revision: 5
---

# P2 final TPU print-prep

## Coupon first

Print `tpu_multilane_coupon.stl` before the case: dry TPU 95A, X2D main 0.4 mm
nozzle, external spool only, textured PEI, cool/normal chamber, 0.20 mm layer,
0.45 mm line width, 40--60 mm/s. Use the same temperature, flow calibration,
line width, and TPU spool intended for the case. Do not substitute PLA: this is
a compliance/shrink-sensitive clearance test.

Measure each lane at both ends: (1) exterior-rear to seating-plane depth against
the manifest's 1.50/1.55/1.60/1.65/1.70 mm CAD targets, and (2) the printed
side-wall position from the left-side datum using a caliper or depth gauge;
accept CAD dimensions within +/-0.10 mm before interpreting fit. With the real
phone, record seating against rear datum A, insertion/removal force class,
inverted retention for 60 s, camera/control/port access, bowing, and every
lip/edge witness mark. Select the tightest lane that fully seats, has no
permanent TPU whitening/tear, retains inverted for 60 s, removes by hand with
no tool/pry force, and does not obstruct a phone function. Any non-seat,
tool/pry removal, uncontrolled drop, permanent deformation, or witness mark is
a failure; if no lane passes, return to `print_plan.md` rather than modify the
candidate by slicing settings.

## Case orientation and fixed profile

Use print-plan rev4's exact transform: rotate cq-v2 by `R_y(-45 degrees)`
about the named exterior rear-left land `L`, putting `L` at printer
`(128,128,0)`. Do not mirror. Printer +Z is bed normal; the phone insertion
vector in printer coordinates is `(-0.70710678,0,0.70710678)`. Only the 1 mm
wide exterior L land contacts the plate. Keep F23 through its full printer-Z
extent at 0.16 mm layers and 0.45 mm perimeter width; use 4 perimeter-equivalent
walls where thickness permits. Use a seam on the nonfunctional exterior near L,
never inside the cavity, capture lip, F14 rim, or a functional opening.

## Mandatory manual exterior-only supports

The re-imported V3/V5 part-only facts remain: 4.408623 mm2 out of self-support
limit and four F23 contour-transition offsets spanning 0.405512..43.587353 mm.
They are **not** proof of a support-free print. In Bambu Studio, use manual
support enforcers only on the unexposed exterior underside of the F23 surround
that lies under those failing layer intervals. No automatic/blanket support.

Forbidden support-contact faces: the whole cavity and capture lip; F05/D09 top
opening; F07/F08/D06 right-control response; F14 opening and its exposed
G04 0.40 mm radius; F21/D07/D08 bottom opening; and the visible exterior face
opposite L. Supports must approach from the exterior only and must leave the
front/open insertion vector unobstructed.

Support settings are fixed by rev4: TPU support material on the main nozzle;
0.20 mm Z gap; two 0.45 mm interface layers; no support elsewhere. A 3--5 mm
brim is allowed only where it reaches L or a nonfunctional support foot. The
support interface must not cross onto an exposed F23 radius or any forbidden
face. Use neither AMS nor the auxiliary/Bowden nozzle for TPU.

| V3 printer-Z layer transition | Required manual support zone | Permitted contact class | Status |
|---|---|---|---|
| 32.16 from 32.00 mm; 43.587353 mm contour offset | F23 unexposed exterior underside directly below the affected contour | exterior nonfunctional underside only | pending slicer selection/preview |
| 50.40 from 50.24 mm; 0.405512 mm contour offset | F23 unexposed exterior underside directly below the affected contour | exterior nonfunctional underside only | pending slicer selection/preview |
| 50.56 from 50.40 mm; 0.588098 mm contour offset | F23 unexposed exterior underside directly below the affected contour | exterior nonfunctional underside only | pending slicer selection/preview |
| 50.72 from 50.56 mm; 14.581540 mm contour offset | F23 unexposed exterior underside directly below the affected contour | exterior nonfunctional underside only | pending slicer selection/preview |
| Outside-F23 4.408623 mm2 | No contact is authorized unless its exact selected footprint is independently classified exterior/nonfunctional and disjoint from every forbidden face | exterior nonfunctional underside only | pending slicer selection/preview |

## Required slicer evidence — pending native slicer execution

No Bambu Studio project, G-code, support-contact preview, or toolpath image is
claimed in this workspace. Consequently the final case is **not accepted for
printing yet**. Before release, save the native Bambu Studio project and record
these P2 artifacts for fresh review:

1. One underside preview with support contacts/highlighted interface footprints.
2. One F23 cross-section/toolpath preview showing prior-layer support beneath
   every V3 failing interval.
3. A layer table mapping each V3 failing interval/area to its support footprint,
   contact face classification, Z gap, and two interface layers.
4. Slicer preview confirmation: main nozzle/external TPU, transform/L land,
   0.16 mm F23 extent, 0.45 mm perimeter/interface line width, no supports on
   every forbidden face, and unobstructed insertion direction.

Native slicer acceptance cannot be inferred from the STL or these notes; a
fresh verifier must assess the actual P2 project and evidence before final-print
acceptance.

## Print, inspection, and field test

After coupon selection, print one case in the selected TPU clearance. Inspect
the 1 mm land, support removal scars (exterior-only), F23 exposed edge, cavity
and capture lip, F14 rim/opening, F05/F21 openings, and right controls before
inserting the phone. Reject for any support mark on a forbidden face, torn lip,
blocked opening, visible sink/void at a rail/root, or deformed F23 edge.

Field test: insert by hand along the specified open direction; confirm full rear
seating with no bow; operate camera/flash, every right control/fingerprint
response, USB-C/bottom functions, and top functions; invert for 60 s over a
soft surface; then remove by hand without a tool. Stop immediately if force
causes permanent deformation, a witness mark, a blocked function, loss of
retention, or a support scar on a forbidden/exposed face. Preserve photos,
native project/profile, actual filament/dryness, caliper readings, and failure
location. Route fit/datum failures to metrology/print plan, geometry interference
to CAD, support/contact failure to P2 slicing, and material/machine defects to
print setup.
