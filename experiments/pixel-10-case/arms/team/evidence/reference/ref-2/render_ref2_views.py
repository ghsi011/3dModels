from pathlib import Path
import sys

from PIL import Image, ImageDraw
import trimesh


OUTPUT_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = OUTPUT_DIR.parents[6]
sys.path.insert(0, str(REPOSITORY_ROOT / "skills" / "3d-modeling" / "scripts"))

from preview import render_view


VIEWS = (
    ("V-REAR", 89, -90),
    ("V-FRONT-RIGHT", -20, 0),
    ("V-BOTTOM", 0, -90),
    ("V-TOP", 0, 90),
)


def main() -> None:
    mesh = trimesh.load(OUTPUT_DIR / "pixel10_reference_ref2.stl")
    for name, elevation, azimuth in VIEWS:
        image = render_view(mesh, elevation, azimuth, 720, 720)
        canvas = Image.new("RGB", (720, 760), "white")
        canvas.paste(image, (0, 40))
        ImageDraw.Draw(canvas).text((24, 12), name, fill="black")
        canvas.save(OUTPUT_DIR / f"{name.lower()}.png")


if __name__ == "__main__":
    main()
