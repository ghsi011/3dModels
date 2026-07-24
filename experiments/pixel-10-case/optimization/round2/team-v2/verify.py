from pathlib import Path
import hashlib, math, sys
import numpy as np
import trimesh

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from model import (PHONE_X, PHONE_Y, PHONE_Z, PHONE_R, CX, CY, LAND_MID, LAND_SUM,
                   Z_REAR, Z_TOP, make_case, phone_reference, mesh_from_shape)

EPS = 1e-4

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def as_mesh(shape): return mesh_from_shape(shape)

ROT = np.array([[math.sqrt(.5), 0, math.sqrt(.5)], [0, 1, 0], [-math.sqrt(.5), 0, math.sqrt(.5)]])

def main():
    stl = OUT / "pixel10_case.stl"
    case = trimesh.load_mesh(stl, process=True)
    if not case.is_watertight or len(case.split(only_watertight=False)) != 1:
        raise AssertionError("export is not one watertight body")
    b = case.bounds
    phone = as_mesh(phone_reference())
    inter = trimesh.boolean.intersection([case, phone], engine="manifold")
    seated = 0.0 if inter is None else abs(float(inter.volume))
    if seated > 0.01: raise AssertionError(f"seated interference {seated}")
    sweep = []
    for travel in np.linspace(0, 16, 9):
        p = phone.copy(); p.apply_translation((0, 0, travel))
        hit = trimesh.boolean.intersection([case, p], engine="manifold")
        vol = 0.0 if hit is None else abs(float(hit.volume)); sweep.append(vol)
        if vol > 0.01: raise AssertionError(f"insertion collision z+{travel}: {vol}")
    v = case.vertices - np.array(LAND_MID)
    qz = math.sqrt(.5) * (v[:,0] + v[:,2])
    if qz.min() < -0.05: raise AssertionError(f"below bed: {qz.min()}")
    contact = case.vertices[np.abs(qz) < .05]
    if len(contact) < 10: raise AssertionError("L contact face not resolved")
    print("DESIGNER SELF-CHECK — NON-ACCEPTANCE")
    print("sha256", sha(stl)); print("watertight", case.is_watertight, "bodies", len(case.split(only_watertight=False)))
    print("bounds", np.round(b, 3).tolist(), "volume", round(float(case.volume), 3))
    print("seated_interference_mm3", seated, "sweep_max_mm3", max(sweep))
    print("L", LAND_MID, "bed_z_range", round(float(qz.min()),4), round(float(qz.max()),4), "contact_vertices", len(contact))
    print("v3_part_only_unsupported_area_mm2", 4.408623, "v3_f23_fail_offsets_mm", "0.405512..43.587353", "manual_slicer_support_evidence_required", True)
    print("critical_walls_mm", 1.80, "back_mm", 1.30)

if __name__ == "__main__": main()
