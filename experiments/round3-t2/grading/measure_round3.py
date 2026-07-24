#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parents[3]
ARMS = ROOT / "experiments" / "round3-t2" / "arms"
OUT = Path(__file__).resolve().parent / "mesh_measurements.json"

SPECS = {
    "monolith": {
        "tool": ARMS / "monolith" / "filter_cap_tool.stl",
        "step": ARMS / "monolith" / "filter_cap_tool.step",
        "coupon": ARMS / "monolith" / "bar_engagement_coupon.stl",
        "print_to_installed": True,
    },
    "team_v3": {
        "tool": ARMS / "team-v3" / "cq-a-washer-filter-tool.stl",
        "step": ARMS / "team-v3" / "cq-a-washer-filter-tool.step",
        "coupon": ARMS / "team-v3" / "cq-a-real-bar-engagement-coupon.stl",
        "print_to_installed": False,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh(path: Path) -> trimesh.Trimesh:
    result = trimesh.load_mesh(path, process=True)
    if not isinstance(result, trimesh.Trimesh):
        raise TypeError(f"{path} did not import as a single mesh")
    return result


def installed_frame(value: trimesh.Trimesh, monolith_print_frame: bool) -> trimesh.Trimesh:
    result = value.copy()
    if monolith_print_frame:
        v = result.vertices
        result.vertices = np.column_stack((58.0 - v[:, 2], v[:, 1], v[:, 0]))
    return result


def step_import(path: Path) -> dict:
    import cadquery as cq
    solid = cq.importers.importStep(str(path))
    value = solid.val()
    with tempfile.TemporaryDirectory(prefix="round3_step_") as temp:
        tess = Path(temp) / "step_reimport.stl"
        cq.exporters.export(solid, str(tess), tolerance=0.01, angularTolerance=0.1)
        reimported = mesh(tess)
        return {
            "cadquery_valid": bool(value.isValid()),
            "cadquery_volume_mm3": float(value.Volume()),
            "cadquery_bbox_mm": [float(x) for x in (value.BoundingBox().xlen, value.BoundingBox().ylen, value.BoundingBox().zlen)],
            "tessellation_reimport_watertight": bool(reimported.is_watertight),
            "tessellation_components": len(reimported.split(only_watertight=False)),
            "tessellation_volume_mm3": float(abs(reimported.volume)),
        }


def historical(path: Path) -> dict:
    command = [sys.executable, str(ROOT / "experiments" / "scorer.py"), "T2", str(path), "--json"]
    output = subprocess.check_output(command, text=True, cwd=ROOT)
    return json.loads(output)


def historical_installed_frame(value: trimesh.Trimesh) -> dict:
    with tempfile.TemporaryDirectory(prefix="round3_installed_") as temp:
        path = Path(temp) / "installed_frame.stl"
        value.export(path)
        result = historical(path)
    result["coordinate_frame"] = "installed D0/DX/DY/DZ; cap face DZ=0"
    return result


def one_arm(name: str, spec: dict) -> dict:
    tool = mesh(spec["tool"])
    coupon = mesh(spec["coupon"])
    installed = installed_frame(tool, spec["print_to_installed"])
    return {
        "files": {key: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
                  for key, path in (("tool_stl", spec["tool"]), ("tool_step", spec["step"]), ("coupon_stl", spec["coupon"]))},
        "tool_stl_reimport": {
            "watertight": bool(tool.is_watertight),
            "components": len(tool.split(only_watertight=False)),
            "bbox_native_mm": [float(x) for x in tool.extents],
            "volume_mm3": float(abs(tool.volume)),
        },
        "tool_step_fresh_import": step_import(spec["step"]),
        "coupon_stl_reimport": {
            "watertight": bool(coupon.is_watertight),
            "components": len(coupon.split(only_watertight=False)),
            "bbox_mm": [float(x) for x in coupon.extents],
            "volume_mm3": float(abs(coupon.volume)),
        },
        "historical_scorer_raw_export": historical(spec["tool"]),
        "historical_scorer_controlled_installed_frame": historical_installed_frame(installed),
    }


def main() -> None:
    report = {"method": "fresh trimesh STL re-import; fresh CadQuery/OCCT STEP import and tessellation re-import", "arms": {}}
    for name, spec in SPECS.items():
        report["arms"][name] = one_arm(name, spec)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
