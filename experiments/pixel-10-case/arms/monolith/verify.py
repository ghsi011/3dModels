from pathlib import Path
import json, sys
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[3] / "skills" / "3d-modeling" / "scripts"))
from preview import render_single, render_multi_view

P = {
    "phone_w": 72.0, "phone_h": 152.8, "phone_d": 8.6,
    "case_w": 76.2, "case_h": 157.0, "case_d": 11.25,
    "camera_y": 50.0, "camera_h": 24.0, "camera_w": 64.0,
    "back": 1.60, "screen_lip": 1.05, "clearance_side": 0.30,
}

def load(name):
    mesh = trimesh.load_mesh(ROOT / name, force="mesh")
    if isinstance(mesh, trimesh.Scene): mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
    return mesh

def extent(mesh): return np.asarray(mesh.bounds[1] - mesh.bounds[0], dtype=float)

case, ref, section = load("pixel10_case.stl"), load("phone_reference.stl"), load("case_section.stl")
checks = {}
checks["watertight"] = bool(case.is_watertight)
checks["positive_mesh_volume"] = bool(abs(case.volume) > 1000)
checks["case_bbox_exported_stl"] = np.round(extent(case), 3).tolist()
checks["bbox_matches_design"] = bool(np.allclose(extent(case), [P["case_w"], P["case_h"], P["case_d"]], atol=0.08))
checks["phone_ref_bbox_exported_stl"] = np.round(extent(ref), 3).tolist()

inside = case.contains(ref.vertices)
checks["seated_interference_vertices"] = int(inside.sum())
checks["seated_interference_pass"] = bool(inside.sum() == 0)

sweep = []
for dz in (45, 30, 15, 5, 0):
    moved = ref.copy(); moved.apply_translation((0, 0, dz))
    hits = int(case.contains(moved.vertices).sum())
    sweep.append({"lift_mm": dz, "embedded_reference_vertices": hits})
checks["insertion_sweep"] = sweep
checks["insertion_sweep_pass"] = bool(all(s["embedded_reference_vertices"] == 0 for s in sweep))

checks["section_mesh_watertight"] = bool(section.is_watertight)

render_single(case, str(ROOT / "render_exterior_isometric.png"), "Pixel 10 TPU case — exterior")
render_multi_view(case, str(ROOT / "render_print_orientation.png"), "Planned TPU print orientation", "Rear face down; open screen side up", view_size=300)
render_single(section, str(ROOT / "render_section.png"), "Exported STL section — cavity and lips")

fit_ref = ref.copy(); fit_ref.apply_translation((0, 0, 0.15))
fit = trimesh.util.concatenate((case, fit_ref))
render_single(fit, str(ROOT / "render_phone_case_fit.png"), "Exported STL fit fixture — phone plus case")
checks["renders_from_exported_stls"] = ["render_exterior_isometric.png", "render_phone_case_fit.png", "render_section.png", "render_print_orientation.png"]

verts = case.vertices
camera_band = verts[(verts[:, 2] < P["back"] + .03) & (np.abs(verts[:, 0]) < 33.0) &
                    (verts[:, 1] > 30.0) & (verts[:, 1] < 70.0)]
measured_cam = {"x_span": [float(camera_band[:,0].min()), float(camera_band[:,0].max())],
                "y_span": [float(camera_band[:,1].min()), float(camera_band[:,1].max())]}
checks["camera_window_mesh_datum_measurement"] = measured_cam
camera_center = [(measured_cam["x_span"][0] + measured_cam["x_span"][1]) / 2,
                 (measured_cam["y_span"][0] + measured_cam["y_span"][1]) / 2]
camera_size = [measured_cam["x_span"][1] - measured_cam["x_span"][0],
               measured_cam["y_span"][1] - measured_cam["y_span"][0]]
checks["camera_window_mesh_center_from_phone_centerline"] = camera_center
checks["camera_window_mesh_size"] = camera_size
checks["camera_window_position_pass"] = bool(np.allclose(camera_center, [0, P["camera_y"]], atol=.35) and
                                             np.allclose(camera_size, [P["camera_w"], P["camera_h"]], atol=.75))
checks["named_datums"] = {"phone_centerline": [0,0], "camera_center_y": 50.0,
                            "bottom_edge_y": -78.5, "top_edge_y": 78.5,
                            "right_edge_x": 38.1}

checks["measurement_audit"] = {"official_phone_body": [72.0,152.8,8.6],
    "case_wall_mm": 1.8, "back_mm": 1.6, "side_clearance_mm": 0.3,
    "screen_lip_mm": 1.05, "camera_aperture_mm": [64.0,24.0],
    "bottom_relief": "USB-C/speaker/mic", "top_relief": "mic/speaker", "right_relief": "power/volume"}

down = case.face_normals[:, 2] < -0.7071
unsupported = float(case.area_faces[down & (case.triangles_center[:,2] > .35)].sum())
checks["unsupported_downfacing_area_mm2"] = round(unsupported, 3)
checks["printability_pass"] = bool(unsupported < 30.0)
checks["mesh_face_count"] = int(len(case.faces))

checks["overall_pass"] = bool(all([checks["watertight"], checks["positive_mesh_volume"],
    checks["bbox_matches_design"], checks["seated_interference_pass"],
    checks["insertion_sweep_pass"], checks["section_mesh_watertight"],
    checks["camera_window_position_pass"], checks["printability_pass"]]))
(ROOT / "verification_report.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
if not checks["overall_pass"]: raise SystemExit("Verification failed")
