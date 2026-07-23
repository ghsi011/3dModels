"""Blind Pixel 10 base reference phone — CadQuery only.

This is a mating reference, not a recreation of unmeasured industrial design.
All dimensional geometry comes from team-v2/dimensions.md revision 1.  The
official diagram is used solely to make the single rear relative-layout overlay.
"""
from pathlib import Path
import hashlib

import cadquery as cq
from PIL import Image, ImageDraw


# ---- Contract-bound parameters (millimetres) --------------------------------
# D01--D03 / S1: exact nominal exterior body envelope.
BODY_X = 72.0
BODY_Y = 152.8
BODY_Z = 8.6
# D04: blind-only bounded assumption; no exact corner-fit claim.
CORNER_R = 12.0
# D05 / F14: conservative shared rear functional envelope.  It is render-only:
# camera-bar thickness/protrusion and component coordinates are explicitly unknown.
REAR_FIELD_X0 = 2.0
REAR_FIELD_X1 = 70.0
REAR_FIELD_Y0 = 107.0
REAR_FIELD_Y1 = 150.0
REAR_FIELD_R = 3.0


def rounded_body(width: float, height: float, depth: float, radius: float) -> cq.Workplane:
    """Body occupying contract frame X=0..width, Y=0..height, Z=0..depth."""
    core_x = cq.Workplane("XY").box(width - 2 * radius, height, depth,
                                      centered=(False, False, False)).translate((radius, 0, 0))
    core_y = cq.Workplane("XY").box(width, height - 2 * radius, depth,
                                      centered=(False, False, False)).translate((0, radius, 0))
    body = core_x.union(core_y)
    for x in (radius, width - radius):
        for y in (radius, height - radius):
            body = body.union(cq.Workplane("XY").center(x, y).circle(radius).extrude(depth))
    return body


PHONE = rounded_body(BODY_X, BODY_Y, BODY_Z, CORNER_R)
assert PHONE.val().isValid(), "Reference body must be a valid solid"


def mm_to_pixel(x_mm: float, y_mm: float, bbox: tuple[int, int, int, int]) -> tuple[float, float]:
    """Map contract coordinates to the diagram body rectangle for relative-only overlay."""
    left, top, right, bottom = bbox
    return (
        left + x_mm / BODY_X * (right - left),
        bottom - y_mm / BODY_Y * (bottom - top),
    )


def draw_rear_overlay(output: Path) -> None:
    """One rear same-view evidence image; never derives millimetres from pixels."""
    source = Path(__file__).resolve().parents[3] / "evidence" / "input" / "pixel10_official_hardware_diagram.png"
    expected = "9d00dd0789cdebbc788199b02c2b633b1ea1f423c78727179540f44b136e27e0"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == expected, "Bound diagram hash changed"
    image = Image.open(source).convert("RGBA")

    # Pixel bounds trace the visible rear handset in this supplied diagram only.
    # They normalize the overlay visually; they are not a dimensional measurement.
    rear_bbox = (1384, 307, 1800, 1187)
    crop = image.crop((1320, 250, 1910, 1245))
    draw = ImageDraw.Draw(crop, "RGBA")
    offset_x, offset_y = 1320, 250
    def p(x, y):
        px, py = mm_to_pixel(x, y, rear_bbox)
        return px - offset_x, py - offset_y

    # Red = contract-bound body silhouette; amber = F14/D05 conservative field.
    body_box = (p(0, BODY_Y), p(BODY_X, 0))
    draw.rounded_rectangle(body_box, radius=CORNER_R / BODY_X * (rear_bbox[2] - rear_bbox[0]),
                           outline=(230, 35, 35, 255), width=5)
    field_box = (p(REAR_FIELD_X0, REAR_FIELD_Y1), p(REAR_FIELD_X1, REAR_FIELD_Y0))
    draw.rounded_rectangle(field_box, radius=REAR_FIELD_R / BODY_X * (rear_bbox[2] - rear_bbox[0]),
                           outline=(245, 155, 0, 255), width=5)
    draw.rectangle((15, 15, 570, 74), fill=(255, 255, 255, 220))
    draw.text((25, 24), "red: D01-D04 blind body | amber: D05/F14 conservative field", fill=(0, 0, 0, 255))
    crop.save(output)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    stl = root / "reference_phone.stl"
    cq.exporters.export(PHONE, str(stl), tolerance=0.01, angularTolerance=0.1)
    draw_rear_overlay(root / "reference_rear_overlay.png")
    bb = PHONE.val().BoundingBox()
    print(f"reference_phone.stl SHA-256 {hashlib.sha256(stl.read_bytes()).hexdigest()}")
    print(f"bounds X={bb.xlen:.3f} Y={bb.ylen:.3f} Z={bb.zlen:.3f}; valid={PHONE.val().isValid()}")
