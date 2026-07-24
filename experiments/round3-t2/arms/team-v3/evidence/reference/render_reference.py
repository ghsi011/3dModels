from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh


OUT = Path(__file__).resolve().parent
MESH = trimesh.load_mesh(OUT / "reference.stl")


def render(name: str, elev: float, azim: float) -> None:
    fig = plt.figure(figsize=(7, 7), dpi=160, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    tri = Poly3DCollection(MESH.triangles, facecolor="#8aa4b8", edgecolor="none")
    ax.add_collection3d(tri)
    bounds = MESH.bounds
    center = bounds.mean(axis=0)
    half = max((bounds[1] - bounds[0]).max() / 2, 1.0) * 1.12
    ax.set_xlim(center[0] - half, center[0] + half)
    ax.set_ylim(center[1] - half, center[1] + half)
    ax.set_zlim(center[2] - half, center[2] + half)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


if __name__ == "__main__":
    render("reference_top.png", elev=90, azim=-90)
    render("reference_side.png", elev=0, azim=-90)
