from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw

RUN = Path(__file__).resolve().parent
TEAM = RUN.parents[3]
CAND_PATH = TEAM / "pixel10_case_cq_a.stl"
REF_PATH = TEAM / "evidence/reference/ref-2/pixel10_reference_ref2.stl"


def installed_candidate() -> trimesh.Trimesh:
    m = trimesh.load_mesh(CAND_PATH, process=True)
    m.apply_translation([0, 0, -4.8])
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    return m


def section_bounds(mesh: trimesh.Trimesh, z: float):
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    path, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1]))
    rings = []
    for poly in path.polygons_full:
        rings.append(np.asarray(poly.exterior.coords))
        rings.extend(np.asarray(h.coords) for h in poly.interiors)
    return rings


def render_xy(meshes, out: Path, title: str, z=None):
    W, H, pad = 900, 1800, 80
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((30, 20), title, fill="black")
    allb = np.vstack([m.bounds for m, _, _ in meshes])
    xmin, ymin = allb[:, 0].min() - 4, allb[:, 1].min() - 4
    xmax, ymax = allb[:, 0].max() + 4, allb[:, 1].max() + 4
    scale = min((W - 2*pad)/(xmax-xmin), (H - 2*pad)/(ymax-ymin))
    def pt(p): return (pad + (p[0]-xmin)*scale, H-pad-(p[1]-ymin)*scale)
    for mesh, color, label in meshes:
        if z is None:
            zz = min(max(mesh.bounds[0,2]+0.6, 0.0), mesh.bounds[1,2]-0.6)
        else: zz = z
        rings = section_bounds(mesh, zz) or []
        for ring in rings:
            if len(ring) > 2: d.line([pt(p) for p in ring], fill=color, width=3, joint="curve")
        d.text((30, 50 + meshes.index((mesh,color,label))*22), label, fill=color)
    im.save(out)


def main():
    cand_raw = trimesh.load_mesh(CAND_PATH, process=True)
    cand = installed_candidate()
    ref = trimesh.load_mesh(REF_PATH, process=True)
    data = {
        "candidate_raw_bounds": cand_raw.bounds.tolist(),
        "candidate_installed_bounds": cand.bounds.tolist(),
        "reference_bounds": ref.bounds.tolist(),
        "candidate_watertight": bool(cand_raw.is_watertight),
        "candidate_volume_mm3": float(cand_raw.volume),
        "candidate_triangles": int(len(cand_raw.faces)),
        "reference_watertight": bool(ref.is_watertight),
    }
    try:
        inter = trimesh.boolean.intersection([cand, ref], engine="manifold")
        data["seated_intersection_mm3"] = float(abs(inter.volume)) if inter is not None else 0.0
    except Exception as exc:
        data["seated_intersection_mm3"] = None; data["intersection_error"] = repr(exc)
    rows=[]
    for travel in range(18, -1, -1):
        rr=ref.copy(); rr.apply_translation([0,0,travel])
        try:
            ii=trimesh.boolean.intersection([cand,rr],engine="manifold")
            vol=float(abs(ii.volume)) if ii is not None else 0.0
        except Exception:
            vol=float('nan')
        rows.append((travel,vol))
    with (RUN/"check-2-insertion-sweep.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["screenward_offset_mm","intersection_mm3"]);w.writerows(rows)
    data["sweep"] = rows
    normals=cand_raw.face_normals; centers=cand_raw.triangles_center
    down=(normals[:,2] < -0.70710678) & (centers[:,2] > 0.3)
    data["unsupported_downward_area_mm2"] = float(cand_raw.area_faces[down].sum())
    data["raw_bbox_mm"]=(cand_raw.bounds[1]-cand_raw.bounds[0]).tolist()
    render_xy([(ref,"#b22222","reference ref-2"),(cand,"#1f4eaa","candidate re-import")], RUN/"check-3-section-plan.png", "Re-imported STL section at rear-plane Z=0", z=0.0)
    render_xy([(ref,"#b22222","reference ref-2"),(cand,"#1f4eaa","candidate re-import")], RUN/"check-4-datum-overlay.png", "Same-datum rear-plan overlay (red reference, blue candidate)", z=0.0)
    (RUN/"reimport_metrics.json").write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))

if __name__ == "__main__": main()
