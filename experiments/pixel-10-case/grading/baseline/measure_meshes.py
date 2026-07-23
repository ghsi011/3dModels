from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parents[2]
HIDDEN_REFERENCE = Path(r"C:\Users\ghsi0\AppData\Local\Temp\pixel10-reference.ZNSPlu\Pixel10.stl")
ARMS = {
    "monolith": ROOT / "arms" / "monolith",
    "team": ROOT / "arms" / "team",
}
STLS = {
    "monolith": ARMS["monolith"] / "pixel10_case.stl",
    "team": ARMS["team"] / "pixel10_case_cq_a.stl",
    "hidden_reference": HIDDEN_REFERENCE,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_info(path: Path) -> dict[str, object]:
    mesh = trimesh.load_mesh(path, force="mesh", process=True)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
    extents = mesh.bounds[1] - mesh.bounds[0]
    components = mesh.split(only_watertight=False)
    return {
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "bounds_mm": [[round(float(v), 4) for v in row] for row in mesh.bounds],
        "extents_mm": [round(float(v), 4) for v in extents],
        "faces": int(len(mesh.faces)),
        "vertices": int(len(mesh.vertices)),
        "components": int(len(components)),
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "euler_number": int(mesh.euler_number),
        "volume_mm3": round(float(abs(mesh.volume)), 3),
        "area_mm2": round(float(mesh.area), 3),
    }


def source_info(folder: Path) -> dict[str, object]:
    py = sorted(folder.rglob("*.py"))
    delivered = [p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    return {
        "python_files": len(py),
        "python_bytes": sum(p.stat().st_size for p in py),
        "python_lines": sum(len(p.read_text(encoding="utf-8").splitlines()) for p in py),
        "delivered_file_count": len(delivered),
        "delivered_bytes": sum(p.stat().st_size for p in delivered),
    }


def main() -> None:
    metrics = {
        "command": "python experiments/pixel-10-case/grading/baseline/measure_meshes.py",
        "mesh_reimports": {key: mesh_info(path) for key, path in STLS.items()},
        "artifact_inventory": {key: source_info(path) for key, path in ARMS.items()},
        "official_body_dimensions_mm": [72.0, 152.8, 8.6],
        "hidden_reference_limitations": (
            "Unverified community mesh used only as one grading reference; reconciled against "
            "official overall body dimensions, not treated as absolute truth."
        ),
    }
    out = Path(__file__).with_name("mesh_measurements.json")
    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
