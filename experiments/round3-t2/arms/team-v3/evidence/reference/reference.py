from pathlib import Path

import cadquery as cq


CAP_DIAMETER = 63.00
BAR_LENGTH = 62.00
BAR_WIDTH = 11.70
BAR_HEIGHT = 24.00
CAP_FACE_Z = 0.00

OUT = Path(__file__).resolve().parent
STL_PATH = OUT / "reference.stl"
STEP_PATH = OUT / "reference.step"


def make_reference() -> tuple[cq.Workplane, cq.Workplane]:
    bar = cq.Workplane("XY").box(BAR_LENGTH, BAR_WIDTH, BAR_HEIGHT,
                                  centered=(True, True, False))
    cap_face_keepout = cq.Workplane("XY", origin=(0, 0, CAP_FACE_Z)).circle(CAP_DIAMETER / 2)
    assert bar.val().isValid(), "raised-bar envelope must be a valid solid"
    return bar, cap_face_keepout


def export_reference(bar: cq.Workplane) -> None:
    cq.exporters.export(bar, str(STL_PATH), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(bar, str(STEP_PATH))


if __name__ == "__main__":
    reference_bar, cap_face_keepout = make_reference()
    export_reference(reference_bar)
    bb = reference_bar.val().BoundingBox()
    print("reference_bar_bbox_mm", (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("reference_bar_volume_mm3", reference_bar.val().Volume())
    print("cap_keepout_diameter_mm", CAP_DIAMETER)
