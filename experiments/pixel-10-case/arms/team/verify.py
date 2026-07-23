# /// script
# dependencies = ["trimesh>=4.7"]
# ///
# ─── How to run ───
# python experiments/pixel-10-case/arms/team/verify.py

from __future__ import annotations

from pathlib import Path

import trimesh


CASE_STL = Path(__file__).with_name("pixel10_case_cq_a.stl")


def main() -> None:
    mesh = trimesh.load_mesh(CASE_STL)
    bounds = mesh.bounds
    print("DESIGNER SELF-CHECK - NON-AUTHORITATIVE; cq-a-r3; NOT AN ACCEPTANCE REPORT")
    print("stl", CASE_STL.name)
    print("watertight", mesh.is_watertight)
    print("volume_mm3", round(float(mesh.volume), 3))
    print("print_bounds_mm", [[round(float(value), 3) for value in row] for row in bounds])
    print("triangles", len(mesh.faces))


if __name__ == "__main__":
    main()
