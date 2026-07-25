"""
edge_samples.py -- DESIGNER SELF-CHECK, NON-ACCEPTANCE.

Samples every plan-named Edge ID (E-01..E-04) on the re-imported, exported cradle.stl and
writes the numeric samples this design uses in candidate_readiness.md / candidate_preflight.json.
Not part of the shared team_preflight.py gate (which validates edge coverage/bands given these
numbers, but does not itself measure geometry) -- this script IS the measurement step.
"""
import json
import math

import numpy as np
import trimesh

TILT_DEG = 27.5
WEDGE_HEIGHT = 18.0
POCKET_BORE_R = 26.125
POCKET_DEPTH = 15.15
LIP_RADIAL_REACH = 1.0
LIP_HEIGHT = 2.0
WALL_OD_R = 27.725
LIP_TOP_FILLET_APPROX = 1.2  # nominal E-03 fillet radius, used only to size the scan window


def circle_fit_radius(xs, ys):
    A = np.column_stack([xs, ys, np.ones_like(xs)])
    b = xs**2 + ys**2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    x0 = sol[0] / 2
    y0 = sol[1] / 2
    return math.sqrt(sol[2] + x0**2 + y0**2)


def e01_samples(m):
    """Base bed-contact fillet: local-outward-normal radial samples around the actual
    (ellipse-like) STAND_BASE_PLANE rim curve, not a naive world-Z-axis radial ray (which
    misattributes samples once the rim departs from a true circle -- see cradle_model.py's
    KEEL_R comment)."""
    sec = m.section(plane_origin=[0, 0, 0.001], plane_normal=[0, 0, 1])
    loop = max(sec.discrete, key=lambda l: len(l))
    coords = loop[:, :2]
    n = len(coords)
    idxs = np.linspace(0, n - 2, 12, dtype=int)
    vals = []
    for idx in idxs:
        p0 = coords[idx]
        p_prev = coords[idx - 2]
        p_next = coords[(idx + 2) % (n - 1)]
        tangent = p_next - p_prev
        tangent /= np.linalg.norm(tangent)
        normal2d = np.array([tangent[1], -tangent[0]])
        if np.dot(normal2d, p0) < 0:
            normal2d = -normal2d
        d = np.array([normal2d[0], normal2d[1], 0.0])
        p03 = np.array([p0[0], p0[1], 0.0])
        zs, rs = [], []
        for z in np.arange(0.0, 0.45, 0.015):
            origin = (p03 + d * 30 + np.array([0, 0, z])).reshape(1, 3)
            direction = (-d).reshape(1, 3)
            loc, ridx, tidx = m.ray.intersects_location(
                ray_origins=origin, ray_directions=direction, multiple_hits=False
            )
            if len(loc):
                proj = np.dot(loc[0][:2] - p0, normal2d)
                zs.append(z)
                rs.append(proj)
        zs, rs = np.array(zs), np.array(rs)
        if len(zs) >= 5:
            R = circle_fit_radius(rs, zs)
            if 0.05 < R < 2.0:  # drop rare grazing-ray outliers (see print_notes.md)
                vals.append(round(float(R), 4))
    return vals


def e02_samples(m):
    """Pocket rim entry fillet: sampled at MULTIPLE points within each of the 2 clear-wall
    arcs that survive with NO lip finger in them (138.5 deg and 318.5 deg -- see
    cradle_model.py CLEAR_ARC_CENTERS_DEG; the other two, 41.5/221.5 deg, are the lip-finger
    centers themselves and no longer carry this edge at all, replaced by the finger geometry)."""
    theta = math.radians(TILT_DEG)
    Rx = np.array(
        [[1, 0, 0], [0, math.cos(theta), -math.sin(theta)], [0, math.sin(theta), math.cos(theta)]]
    )
    Rinv = Rx.T
    vals = []
    for center in (138.5, 318.5):
        for ang in (center - 8, center, center + 8):
            a = math.radians(ang)
            d_local = np.array([math.cos(a), math.sin(a), 0.0])
            zs, rs = [], []
            for zprime in np.arange(POCKET_DEPTH - 0.8, POCKET_DEPTH + 0.02, 0.01):
                pt_local = d_local * 0.5 + np.array([0, 0, zprime])
                origin_world = (Rx @ pt_local) + np.array([0, 0, WEDGE_HEIGHT])
                dir_world = Rx @ d_local
                loc, ridx, tidx = m.ray.intersects_location(
                    ray_origins=origin_world.reshape(1, 3), ray_directions=dir_world.reshape(1, 3),
                    multiple_hits=False,
                )
                if len(loc):
                    hit_local = Rinv @ (loc[0] - np.array([0, 0, WEDGE_HEIGHT]))
                    r = math.hypot(hit_local[0], hit_local[1])
                    if r < 27.0:
                        zs.append(hit_local[2])
                        rs.append(r)
            zs, rs = np.array(zs), np.array(rs)
            if len(zs) >= 5:
                R = circle_fit_radius(rs, zs)
                if 0.05 < R < 5.0:
                    vals.append(round(float(R), 4))
    return vals


def e03_e04_samples(m):
    """Lip finger top-outer (E-03) and inner-boundary (E-04) edges, both lip fingers."""
    theta = math.radians(TILT_DEG)
    Rx = np.array(
        [[1, 0, 0], [0, math.cos(theta), -math.sin(theta)], [0, math.sin(theta), math.cos(theta)]]
    )
    Rinv = Rx.T
    lip_z0 = POCKET_DEPTH - LIP_HEIGHT
    lip_z1 = POCKET_DEPTH
    lip_r_inner = POCKET_BORE_R - LIP_RADIAL_REACH
    e03_vals, e04_vals = [], []
    # sample near BOTH ends of each finger's arc (not just its center) -- gives >= 3 E-04
    # samples total (contract requires samples_required=3) from only 2 physical fingers
    for ang in (41.5 - 8, 41.5 + 8, 221.5 - 8, 221.5 + 8):
        a = math.radians(ang)
        d_local = np.array([math.cos(a), math.sin(a), 0.0])
        # E-03: top-outer edge (top face z'=lip_z1 meets outer wall r=WALL_OD_R) -- same
        # horizontal-ray-varying-Z method as E-01/E-02 (a downward ray varying only r, tried
        # first, does not reliably track this fillet's own curved profile).
        zs, rs = [], []
        for zprime in np.arange(lip_z1 - LIP_TOP_FILLET_APPROX - 0.1, lip_z1 + 0.02, 0.01):
            pt_local = d_local * 40 + np.array([0, 0, zprime])
            origin_world = (Rx @ pt_local) + np.array([0, 0, WEDGE_HEIGHT])
            dir_world = Rx @ (-d_local)
            loc, ridx, tidx = m.ray.intersects_location(
                ray_origins=origin_world.reshape(1, 3), ray_directions=dir_world.reshape(1, 3),
                multiple_hits=False,
            )
            if len(loc):
                hit_local = Rinv @ (loc[0] - np.array([0, 0, WEDGE_HEIGHT]))
                r = math.hypot(hit_local[0], hit_local[1])
                if WALL_OD_R - LIP_TOP_FILLET_APPROX - 0.2 < r < WALL_OD_R + 0.2:
                    zs.append(hit_local[2])
                    rs.append(r)
        zs, rs = np.array(zs), np.array(rs)
        if len(zs) >= 5:
            R = circle_fit_radius(rs, zs)
            if 0.05 < R < 5.0:
                e03_vals.append(round(float(R), 4))
        # E-04: inner boundary edge (r=lip_r_inner, z'=lip_z0)
        zs2, rs2 = [], []
        for zprime in np.arange(lip_z0 - 0.05, lip_z0 + 0.6, 0.01):
            pt_local = d_local * 0.5 + np.array([0, 0, zprime])
            origin_world = (Rx @ pt_local) + np.array([0, 0, WEDGE_HEIGHT])
            dir_world = Rx @ d_local
            loc, ridx, tidx = m.ray.intersects_location(
                ray_origins=origin_world.reshape(1, 3), ray_directions=dir_world.reshape(1, 3),
                multiple_hits=False,
            )
            if len(loc):
                hit_local = Rinv @ (loc[0] - np.array([0, 0, WEDGE_HEIGHT]))
                r = math.hypot(hit_local[0], hit_local[1])
                if r < lip_r_inner + 0.9:
                    zs2.append(hit_local[2])
                    rs2.append(r)
        zs2, rs2 = np.array(zs2), np.array(rs2)
        if len(zs2) >= 5:
            R2 = circle_fit_radius(rs2, zs2)
            e04_vals.append(round(float(R2), 4))
    return e03_vals, e04_vals


def main():
    m = trimesh.load("cradle.stl")
    e01 = e01_samples(m)
    e02 = e02_samples(m)
    e03, e04 = e03_e04_samples(m)
    result = {"E-01": e01, "E-02": e02, "E-03": e03, "E-04": e04}
    print(json.dumps(result, indent=2))
    with open("edge_samples.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
