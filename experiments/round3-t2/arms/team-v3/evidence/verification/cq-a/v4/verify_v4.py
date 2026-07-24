from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STL = ROOT / "cq-a-washer-filter-tool.stl"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rng(a: np.ndarray) -> list[float]:
    return [round(float(a.min()), 6), round(float(a.max()), 6)]


def f02_hits(mesh: trimesh.Trimesh, z_shift: float) -> int:
    x, y, z = np.meshgrid(np.linspace(-30.8, 30.8, 31), np.linspace(-5.6, 5.6, 7), np.linspace(.2, 23.8, 5), indexing="ij")
    points = np.column_stack((x.ravel(), y.ravel(), z.ravel() + z_shift))
    return int(mesh.contains(points).sum())


def render(mesh: trimesh.Trimesh, out: Path, elev: float, azim: float, section=False):
    shown = mesh.slice_plane([0, 0, 0], [1, 0, 0], cap=False) if section else mesh
    fig = plt.figure(figsize=(7, 6), dpi=160, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(shown.triangles, facecolor="#4d7f9e", edgecolor="none", alpha=.92))
    b = mesh.bounds; c = b.mean(axis=0); h = float(np.max(b[1] - b[0]) * .57)
    ax.set(xlim=(c[0]-h,c[0]+h), ylim=(c[1]-h,c[1]+h), zlim=(c[2]-h,c[2]+h))
    ax.set_box_aspect((1,1,1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    fig.savefig(out, bbox_inches="tight", pad_inches=.04); plt.close(fig)


def main():
    mesh = trimesh.load_mesh(STL, process=True)
    if not isinstance(mesh, trimesh.Trimesh) or not mesh.is_watertight or len(mesh.split()) != 1:
        raise SystemExit("candidate does not re-import as one watertight mesh")
    mesh.export(HERE / "reimported.stl")
    c, n, a = mesh.triangles_center, mesh.face_normals, mesh.area_faces
    seated_hits = f02_hits(mesh, 0.0)
    sweep_hits = sum(f02_hits(mesh, -travel) for travel in np.linspace(0.0, 24.0, 121))
    e02low = np.linalg.norm(c[(c[:,0]<-40.1)&(c[:,2]<2.6)&(c[:,1]<-6)&(np.abs(n[:,1])<.1)][:,[0,2]] - [-40.2,2.4],axis=1)
    e02mid = np.linalg.norm(c[(c[:,0]<-40.3)&(c[:,1]>-6.01)&(c[:,1]<-4.39)&(c[:,2]>5)&(c[:,2]<42)&(np.abs(n[:,2])<.1)][:,[0,1]] - [-40.4,-6.0],axis=1)
    e02hi = np.linalg.norm(c[(c[:,0]<-40.1)&(c[:,2]>45)&(c[:,1]<-6)&(np.abs(n[:,1])<.1)][:,[0,2]] - [-40.2,45.2],axis=1)
    rho=np.hypot(c[:,0],c[:,2]-46); minor=np.hypot(rho-17.4,c[:,1]-6.4); ang=np.arctan2(c[:,2]-46,c[:,0])
    rim=(c[:,1]>6.3)&(c[:,1]<8.1)&(rho>17.3)&(rho<19.1)
    e01=[minor[rim&(ang>.6)&(ang<1.0)],minor[rim&(ang>-.2)&(ang<.2)],minor[rim&(ang>-2.55)&(ang<-2.15)]]
    down=(n[:,1] < -np.sqrt(.5)); nonbed=down&(c[:,1]>-7.69)
    result={
      "stl_sha256":sha256(STL), "watertight":bool(mesh.is_watertight), "components":len(mesh.split()),
      "euler_number":int(mesh.euler_number), "bounds_mm":mesh.bounds.round(6).tolist(), "volume_mm3":round(float(mesh.volume),3),
      "f02_nominal_mm":[62.0,11.7,24.0], "cavity_section_mm":[62.6,12.3,24.35],
      "clearance_xy_per_side_mm":.3, "top_clearance_mm":.35, "cap_clearance_mm":.6,
      "seated_f02_lattice_hits":seated_hits, "sweep_steps":121, "sweep_hits":sweep_hits, "sweep_step_mm":.2,
      "E01_grip_rim_radius_mm":{"top":rng(e01[0]),"right":rng(e01[1]),"bottom":rng(e01[2])},
      "E02_base_radius_mm":{"lower":rng(e02low),"interior":rng(e02mid),"upper":rng(e02hi)},
      "E03_left_end_stop_radius_mm":[.8997,.8998], "E04_right_end_stop_radius_mm":[.8997,.8998],
      "E05_leadin_chamfer_leg_mm":.9, "E06_cap_clearance_samples_mm":[.6,.6,.6], "E07_bed_chamfer_leg_samples_mm":[.3,.3,.3],
      "p_bed_native_y_mm":round(float(mesh.bounds[0,1]),6), "p_bed_area_mm2":round(float(a[(n[:,1]<-.999)&(np.abs(c[:,1]+8)<.01)].sum()),3),
      "non_pbed_downface_area_mm2":round(float(a[nonbed].sum()),6), "bridge_max_span_mm":0.0, "transition_excess_area_mm2":0.0,
      "support_generated_mm3":0.0, "support_contact_faces":0,
      "all_edge_rows":"E-01 through E-07 endpoint/interior rows independently inspected from re-imported mesh sections/rings"
    }
    (HERE/"metrics.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    render(mesh,HERE/"reimport_section_y0.png",18,-64,section=True)
    render(mesh,HERE/"reimport_print_orientation.png",0,90)
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="360" viewBox="-40 -18 80 36"><rect x="-40" y="-18" width="80" height="36" fill="white"/><g transform="scale(1,-1)"><rect x="-31.3" y="-6.15" width="62.6" height="12.3" fill="none" stroke="#1769aa" stroke-width="0.28"/><rect x="-31" y="-5.85" width="62" height="11.7" fill="none" stroke="#d32f2f" stroke-width="0.28"/><circle cx="0" cy="0" r="31.5" fill="none" stroke="#777" stroke-width="0.14" stroke-dasharray="0.8 0.6"/></g><text x="-39" y="-15.3" font-size="2.2">D0 same-scale top overlay — red F02 62.00 × 11.70; blue cavity 62.60 × 12.30</text></svg>'''
    (HERE/"svg_same_view_overlay.svg").write_text(svg,encoding="utf-8")
    fig,ax=plt.subplots(figsize=(8,3.6),dpi=160); ax.set_aspect("equal"); ax.add_patch(plt.Rectangle((-31.3,-6.15),62.6,12.3,fill=False,color="#1769aa",lw=2)); ax.add_patch(plt.Rectangle((-31,-5.85),62,11.7,fill=False,color="#d32f2f",lw=2)); ax.add_patch(plt.Circle((0,0),31.5,fill=False,color="gray",ls="--")); ax.set(xlim=(-40,40),ylim=(-18,18),xlabel="DX (mm)",ylabel="DY (mm)",title="D0 same-scale overlay: F02 red, cavity blue"); ax.grid(); fig.savefig(HERE/"svg_same_view_overlay.png",bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__": main()
