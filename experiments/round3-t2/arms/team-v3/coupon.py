#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery==2.8.0", "trimesh"]
# ///

# ─── How to run ───
# 1. Run: uv run coupon.py
# ──────────────────

from __future__ import annotations

from pathlib import Path

import cadquery as cq

import model as candidate


OUT = Path(__file__).resolve().parent
COUPON_STL = OUT / "cq-a-real-bar-engagement-coupon.stl"

INTERFACE_SPAN_NOMINAL = candidate.BAR_LENGTH
RETAINED_ENGAGEMENT_DEPTH = candidate.BAR_HEIGHT
FIT_CLEAR_XY = candidate.FIT_CLEAR_XY
FIT_CLEAR_Z_TOP = candidate.FIT_CLEAR_Z_TOP
CAVITY_X = candidate.CAVITY_X
CAVITY_Y = candidate.CAVITY_Y
CAVITY_Z = candidate.CAVITY_Z
CONTACT_RADIUS = candidate.CONTACT_RADIUS
END_WALL = candidate.END_WALL
P_BED_Y = candidate.BASE_Y_MIN

CORE_X = CAVITY_X + 2.0 * END_WALL
CORE_Y = candidate.RETAINING_Y - candidate.BASE_Y_MIN
CORE_Z_MIN = 0.0
CORE_Z_MAX = candidate.CAVITY_TOP_Z + candidate.MIN_WALL + CONTACT_RADIUS
CORE_Z = CORE_Z_MAX - CORE_Z_MIN

TAB_X = 50.0
TAB_Y = 6.0
TAB_Z = 8.0
TAB_Y_MIN = candidate.RETAINING_Y - 0.50
TAB_Z_MIN = candidate.CAVITY_TOP_Z - 0.50


def make_coupon() -> cq.Workplane:
    production_tool = candidate.make_tool()
    retained_core = production_tool.intersect(
        candidate.box(CORE_X, CORE_Y, CORE_Z, 0.0,
                      (candidate.BASE_Y_MIN + candidate.RETAINING_Y) / 2.0,
                      CORE_Z_MIN + CORE_Z / 2.0)
    )
    hand_tab = candidate.box(TAB_X, TAB_Y, TAB_Z, 0.0,
                             TAB_Y_MIN + TAB_Y / 2.0,
                             TAB_Z_MIN + TAB_Z / 2.0)
    coupon = retained_core.union(hand_tab)
    if not coupon.val().isValid():
        raise RuntimeError("CadQuery produced an invalid coupon solid")
    return coupon


def main() -> None:
    RESULT = make_coupon()
    cq.exporters.export(RESULT, str(COUPON_STL), tolerance=0.01, angularTolerance=0.1)
    print(f"coupon_volume_mm3={RESULT.val().Volume():.3f}")
    print(f"nominal_span_mm={INTERFACE_SPAN_NOMINAL:.2f}")
    print(f"retained_depth_mm={RETAINED_ENGAGEMENT_DEPTH:.2f}")
    print(f"production_cavity_mm={CAVITY_X:.2f} x {CAVITY_Y:.2f} x {CAVITY_Z:.2f}")


if __name__ == "__main__":
    main()
