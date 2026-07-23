"""Blind Pixel 10 mating reference, built only from dimensions.md r1.

Coordinate frame: X left-to-right on the rear view, Y bottom-to-top, Z rearward.
The handset body spans Z=-8.6..0.0 mm.  This is a pipeline intermediate fixture,
not a printable part or a candidate case.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import cadquery as cq


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence" / "reference"

# dimensions.md r1, all units mm.  Values intentionally stay named and traceable.
BODY_HEIGHT = 152.8  # M-001, D2_BOTTOM -> D4_TOP
BODY_WIDTH = 72.0  # M-002, D1_XMID -> D3_RIGHT
BODY_DEPTH = 8.6  # M-003, front exterior -> D0_REAR
CORNER_RADIUS = 10.0  # M-004 nominal within approved 7..13 bound

ISLAND_WIDTH = 60.5  # M-005 nominal
ISLAND_HEIGHT = 22.0  # M-006 nominal
ISLAND_CENTER_X = 0.0  # M-007
ISLAND_TOP_Y = 138.8  # M-008
ISLAND_PROTRUSION = 2.0  # M-009 nominal
CAMERA_COUNT = 3  # M-010
FLASH_COUNT = 1  # M-011

RIGHT_FACE_X = 36.0  # M-013 / D3_RIGHT
CONTROL_Y_MIN = 42.0  # M-012 approved continuous-relief bound
CONTROL_Y_MAX = 122.0  # M-012 approved continuous-relief bound
USB_CENTER_X = 0.0  # M-014
USB_MIN_WIDTH = 18.0  # M-014 approved lower bound
TOP_MIC_RELIEF_WIDTH = 8.0  # M-017 approved temporary centred relief

# Geometric proxy proportions for features whose individual dimensions are explicitly
# unmeasured in r1.  They derive from the measured island/body envelopes; no photo or
# hidden dimension is used.  The metrologist round-trip decides whether r1 needs detail.
LENS_DIAMETER = ISLAND_HEIGHT / 3.5
LENS_PITCH = ISLAND_WIDTH / 4.0
FLASH_DIAMETER = ISLAND_HEIGHT / 4.0
FRONT_CAMERA_DIAMETER = LENS_DIAMETER / 2.0
FRONT_CAMERA_Y = BODY_HEIGHT - ISLAND_HEIGHT / 2.0
SURFACE_MARK_DEPTH = 0.5


def rounded_rectangle(width: float, height: float, radius: float, z0: float, depth: float) -> cq.Workplane:
    """A planar rounded rectangle extruded from z0, centred in X and bottomed at Y=0."""
    if radius <= 0 or radius > min(width, height) / 2:
        raise ValueError("rounded rectangle radius is invalid")
    shape = cq.Workplane("XY").box(width - 2 * radius, height, depth, centered=(True, False, False)).translate((0, 0, z0))
    if height - 2 * radius > 1e-6:
        shape = shape.union(
            cq.Workplane("XY").box(width, height - 2 * radius, depth, centered=(True, False, False)).translate((0, radius, z0))
        )
    for x in (-width / 2 + radius, width / 2 - radius):
        for y in (radius, height - radius):
            shape = shape.union(cq.Workplane("XY").center(x, y).circle(radius).extrude(depth).translate((0, 0, z0)))
    return shape


def _surface_cut(body: cq.Workplane, x: float, y: float, diameter: float, z0: float, depth: float) -> cq.Workplane:
    return body.cut(cq.Workplane("XY").center(x, y).circle(diameter / 2).extrude(depth).translate((0, 0, z0)))


def build_reference() -> cq.Workplane:
    body = rounded_rectangle(BODY_WIDTH, BODY_HEIGHT, CORNER_RADIUS, -BODY_DEPTH, BODY_DEPTH)

    # F-003: capsule-derived raised island.  Its top edge is exactly M-008.
    island_bottom_y = ISLAND_TOP_Y - ISLAND_HEIGHT
    island = rounded_rectangle(ISLAND_WIDTH, ISLAND_HEIGHT, ISLAND_HEIGHT / 2, 0.0, ISLAND_PROTRUSION)
    island = island.translate((ISLAND_CENTER_X, island_bottom_y, 0))
    body = body.union(island)

    # F-004/F-005: three lens and one +X flash surface apertures in F-003.
    for x in (-LENS_PITCH, 0.0, LENS_PITCH):
        body = _surface_cut(body, x, island_bottom_y + ISLAND_HEIGHT / 2, LENS_DIAMETER, ISLAND_PROTRUSION - SURFACE_MARK_DEPTH, SURFACE_MARK_DEPTH)
    body = _surface_cut(
        body,
        ISLAND_WIDTH / 2 - FLASH_DIAMETER,
        island_bottom_y + ISLAND_HEIGHT / 2,
        FLASH_DIAMETER,
        ISLAND_PROTRUSION - SURFACE_MARK_DEPTH,
        SURFACE_MARK_DEPTH,
    )

    # F-006/F-007: only the continuous 42..122 mm functional envelope is specified.
    control_height = CONTROL_Y_MAX - CONTROL_Y_MIN
    controls = cq.Workplane("XY").box(2.0, control_height, BODY_DEPTH / 2, centered=(False, False, True))
    controls = controls.translate((RIGHT_FACE_X, CONTROL_Y_MIN, -BODY_DEPTH / 2))
    body = body.union(controls)

    # F-009 USB-C bottom-edge envelope (M-014/M-015), plus broad symbolic F-008/F-010
    # regions at either side.  Detailed slot placement is intentionally not invented.
    port = cq.Workplane("XY").box(USB_MIN_WIDTH, 2.0, BODY_DEPTH / 2, centered=(True, True, True))
    body = body.cut(port.translate((USB_CENTER_X, 0, -BODY_DEPTH / 2)))
    for x in (-BODY_WIDTH / 4, BODY_WIDTH / 4):
        opening = cq.Workplane("XY").box(BODY_WIDTH / 6, 2.0, BODY_DEPTH / 3, centered=(True, True, True))
        body = body.cut(opening.translate((x, 0, -BODY_DEPTH / 2)))

    # F-013 top microphone: exact point unknown; r1 authorizes a centred 8 mm relief.
    top_relief = cq.Workplane("XY").box(TOP_MIC_RELIEF_WIDTH, 2.0, BODY_DEPTH / 3, centered=(True, True, True))
    body = body.cut(top_relief.translate((0, BODY_HEIGHT, -BODY_DEPTH / 2)))

    # F-012 front camera identity marker.  Its only r1 location constraint is centred
    # and near the top, so it is derived from the named camera-island height proxy.
    body = _surface_cut(body, 0.0, FRONT_CAMERA_Y, FRONT_CAMERA_DIAMETER, -BODY_DEPTH, SURFACE_MARK_DEPTH)

    if not body.val().isValid():
        raise RuntimeError("reference solid is invalid")
    return body


ref_part = build_reference()


def export_artifacts() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stl = OUT / "pixel10_reference_r1.stl"
    step = OUT / "pixel10_reference_r1.step"
    cq.exporters.export(ref_part, str(stl), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(ref_part, str(step))

    # These exact camera tuples are the deterministic same-view evidence for V-REAR,
    # V-FRONT-RIGHT, V-BOTTOM, and V-TOP requested by dimensions.md r1.
    sys.path.insert(0, str(ROOT.parents[3] / "skills" / "3d-modeling" / "scripts"))
    import trimesh
    from PIL import Image, ImageDraw
    import pyrender
    from preview import _build_scene, _render_frame

    mesh = trimesh.load_mesh(stl, force="mesh")
    views = {
        "V-REAR": (89.0, 0.0, "Rear / Z+"),
        "V-FRONT-RIGHT": (-32.0, 0.0, "Front-right / X+ Z-"),
        "V-BOTTOM": (12.0, -90.0, "Bottom edge / Y-"),
        "V-TOP": (12.0, 90.0, "Top edge / Y+"),
    }
    scene, radius, center, _, _ = _build_scene(mesh, include_ground=False)
    renderer = pyrender.OffscreenRenderer(900, 900)
    for view_id, (elev, azim, label) in views.items():
        image = _render_frame(scene, radius, center, elev, azim, renderer)
        canvas = Image.new("RGB", (900, 940), "white")
        canvas.paste(image, (0, 40))
        ImageDraw.Draw(canvas).text((450, 14), f"Pixel 10 blind reference r1 — {view_id}: {label}", fill="black", anchor="mt")
        canvas.save(OUT / f"reference_{view_id.lower()}.png")
    renderer.delete()

    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("pixel10_reference_r1.*"))}
    manifest = {
        "commission": "ref-1",
        "dimensions_contract": "dimensions.md r1",
        "source": "reference.py",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "exports": hashes,
        "renders": {k: {"file": f"reference_{k.lower()}.png", "camera_elev_deg": v[0], "camera_azim_deg": v[1]} for k, v in views.items()},
        "command": "python reference.py",
        "notes": "Blind fixture built from dimensions.md r1 only; unmeasured individual feature geometry remains explicit envelope/proxy geometry.",
    }
    (OUT / "reference_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bbox": [ref_part.val().BoundingBox().xlen, ref_part.val().BoundingBox().ylen, ref_part.val().BoundingBox().zlen], "exports": hashes}, indent=2))


if __name__ == "__main__":
    export_artifacts()
