# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery", "numpy", "trimesh"]
# ///
# ─── How to run ───
# uv run experiments/pixel-10-case/optimization/round2/grading/measure_v2.py
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final

import cadquery as cq
import numpy as np
import trimesh


OFFICIAL_BODY_MM: Final[tuple[float, float, float]] = (72.0, 152.8, 8.6)
CANDIDATE: Final[Path] = Path(__file__).resolve().parents[1] / "team-v2"
OUTPUT: Final[Path] = Path(__file__).with_name("mesh_measurements.json")


@dataclass(frozen=True, slots=True)
class MeshMeasurement:
    path: str
    sha256: str
    bytes: int
    bounds_mm: tuple[tuple[float, float, float], tuple[float, float, float]]
    extents_mm: tuple[float, float, float]
    faces: int
    vertices: int
    components: int
    watertight: bool
    winding_consistent: bool
    euler_number: int
    volume_mm3: float
    area_mm2: float


@dataclass(frozen=True, slots=True)
class StepMeasurement:
    path: str
    sha256: str
    bytes: int
    valid: bool
    volume_mm3: float


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rounded(values: np.ndarray) -> tuple[float, float, float]:
    return (round(float(values[0]), 4), round(float(values[1]), 4), round(float(values[2]), 4))


def measure_stl(path: Path) -> MeshMeasurement:
    mesh = trimesh.load_mesh(path, force="mesh", process=True)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
    components = mesh.split(only_watertight=False)
    return MeshMeasurement(
        path=str(path),
        sha256=digest(path),
        bytes=path.stat().st_size,
        bounds_mm=(rounded(mesh.bounds[0]), rounded(mesh.bounds[1])),
        extents_mm=rounded(mesh.bounds[1] - mesh.bounds[0]),
        faces=len(mesh.faces),
        vertices=len(mesh.vertices),
        components=len(components),
        watertight=mesh.is_watertight,
        winding_consistent=mesh.is_winding_consistent,
        euler_number=mesh.euler_number,
        volume_mm3=round(abs(float(mesh.volume)), 3),
        area_mm2=round(float(mesh.area), 3),
    )


def measure_step(path: Path) -> StepMeasurement:
    solid = cq.importers.importStep(str(path)).val()
    return StepMeasurement(
        path=str(path),
        sha256=digest(path),
        bytes=path.stat().st_size,
        valid=solid.isValid(),
        volume_mm3=round(float(solid.Volume()), 3),
    )


def inventory(folder: Path) -> tuple[int, int, int, int, int]:
    files = tuple(path for path in folder.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    python_files = tuple(path for path in files if path.suffix == ".py")
    return (
        len(files),
        sum(path.stat().st_size for path in files),
        len(python_files),
        sum(path.stat().st_size for path in python_files),
        sum(len(path.read_text(encoding="utf-8").splitlines()) for path in python_files),
    )


def main() -> None:
    stl = CANDIDATE / "pixel10_case.stl"
    step = CANDIDATE / "pixel10_case.step"
    delivered_files, delivered_bytes, python_files, python_bytes, python_lines = inventory(CANDIDATE)
    result = {
        "command": "uv run experiments/pixel-10-case/optimization/round2/grading/measure_v2.py",
        "candidate_root": str(CANDIDATE),
        "official_body_dimensions_mm": OFFICIAL_BODY_MM,
        "stl_reimport": asdict(measure_stl(stl)),
        "step_reimport": asdict(measure_step(step)),
        "artifact_inventory_excluding_caches": {
            "delivered_file_count": delivered_files,
            "delivered_bytes": delivered_bytes,
            "python_files": python_files,
            "python_bytes": python_bytes,
            "python_lines": python_lines,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
