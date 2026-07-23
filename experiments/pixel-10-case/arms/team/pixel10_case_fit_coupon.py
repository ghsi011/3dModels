#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery==2.8.0"]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run pixel10_case_fit_coupon.py
# 3. Or make executable and run:
#      chmod +x pixel10_case_fit_coupon.py && ./pixel10_case_fit_coupon.py
# ──────────────────

from __future__ import annotations

from pathlib import Path

import cadquery as cq


MODEL_FILENAME = "model.py"
CLEARANCE_TOKEN = "CAVITY_CLEARANCE_MM = 0.35"
CLEARANCES_MM = (0.25, 0.35, 0.45)
LOWER_BAND_Y_MIN_MM = 0.0
LOWER_BAND_Y_MAX_MM = 30.0
RIGHT_CONTROL_Y_MIN_MM = 42.0
RIGHT_CONTROL_Y_MAX_MM = 122.0
RIGHT_STRIP_X_MIN_MM = 18.0
RIGHT_STRIP_X_MAX_MM = 44.0
FIXTURE_DEPTH_MM = 30.0
FIXTURE_Z_CENTER_MM = -4.0


class CouponGenerationError(RuntimeError):
    pass


def load_case_for_clearance(model_path: Path, clearance_mm: float) -> cq.Workplane:
    source = model_path.read_text(encoding="utf-8")
    replacement = f"CAVITY_CLEARANCE_MM = {clearance_mm:.2f}"
    if source.count(CLEARANCE_TOKEN) != 1:
        raise CouponGenerationError("Accepted model clearance parameter is not uniquely addressable")
    namespace = {"__file__": str(model_path), "__name__": "coupon_model"}
    exec(compile(source.replace(CLEARANCE_TOKEN, replacement), str(model_path), "exec"), namespace)
    candidate = namespace.get("case")
    if not isinstance(candidate, cq.Workplane):
        raise CouponGenerationError("Accepted model did not expose a CadQuery case workplane")
    return candidate


def crop_case(case: cq.Workplane, x_min_mm: float, x_max_mm: float, y_min_mm: float, y_max_mm: float) -> cq.Workplane:
    width_mm = x_max_mm - x_min_mm
    height_mm = y_max_mm - y_min_mm
    cutter = (
        cq.Workplane("XY")
        .box(width_mm, height_mm, FIXTURE_DEPTH_MM, centered=(True, True, True))
        .translate(((x_min_mm + x_max_mm) / 2.0, (y_min_mm + y_max_mm) / 2.0, FIXTURE_Z_CENTER_MM))
    )
    coupon = case.intersect(cutter)
    if not coupon.val().isValid():
        raise CouponGenerationError("Coupon crop is not a valid solid")
    return coupon


def export_coupon(case: cq.Workplane, label: str, output_path: Path) -> None:
    printed = case.rotate((0, 0, 0), (1, 0, 0), 180.0)
    printed = printed.translate((0.0, 0.0, -printed.val().BoundingBox().zmin))
    cq.exporters.export(printed, str(output_path), tolerance=0.01, angularTolerance=0.1)
    bbox = printed.val().BoundingBox()
    print(f"{label}: valid={printed.val().isValid()} bbox={bbox.xlen:.3f}x{bbox.ylen:.3f}x{bbox.zlen:.3f}")


def main() -> None:
    directory = Path(__file__).resolve().parent
    model_path = directory / MODEL_FILENAME
    for clearance_mm in CLEARANCES_MM:
        case = load_case_for_clearance(model_path, clearance_mm)
        lower = crop_case(case, -50.0, 50.0, LOWER_BAND_Y_MIN_MM, LOWER_BAND_Y_MAX_MM)
        right_control = crop_case(case, RIGHT_STRIP_X_MIN_MM, RIGHT_STRIP_X_MAX_MM, RIGHT_CONTROL_Y_MIN_MM, RIGHT_CONTROL_Y_MAX_MM)
        suffix = f"{clearance_mm:.2f}".replace(".", "p")
        export_coupon(lower, f"lower-{suffix}", directory / f"pixel10_case_fit_coupon_lower_{suffix}.stl")
        export_coupon(right_control, f"right-control-{suffix}", directory / f"pixel10_case_fit_coupon_right_control_{suffix}.stl")


if __name__ == "__main__":
    main()
