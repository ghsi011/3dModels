#!/usr/bin/env python3
"""Score a candidate STL (or dir of STLs) against a test's functional spec.
Usage: python3 scorer.py T1|T2|T3|T4 <stl-or-dir> [--json]
Checks marked CRIT are required for functional success."""
import sys, os, glob, json
import numpy as np
import trimesh
import shapely.geometry as sg


def load(path):
    files = sorted(glob.glob(os.path.join(path, '**/*.stl'), recursive=True)) \
        if os.path.isdir(path) else [path]
    skip = ('_check', 'section', 'preview', 'ref_', 'fixture')
    files = [f for f in files if not any(s in os.path.basename(f).lower() for s in skip)] or files
    meshes = []
    for f in files:
        m = trimesh.load(f)
        if hasattr(m, 'geometry'):
            meshes += list(m.geometry.values())
        else:
            meshes.append(m)
    return files, meshes


def slice_polys(m, z):
    """model-frame XY sections — bare to_2D() re-origins on a path-dependent frame"""
    try:
        sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None: return []
        p, _ = sec.to_2D(trimesh.geometry.plane_transform([0, 0, z], [0, 0, 1]))
        return list(p.polygons_full)
    except Exception:
        return []


def overhang_frac(m, up=True):
    mm = m.copy()
    if not up:
        mm.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    mm.apply_translation(-mm.bounds[0])
    down = mm.face_normals[:, 2] < -np.cos(np.radians(30))  # steeper than 60 deg
    above = mm.triangles_center[:, 2] > 2.5
    a = mm.area_faces
    return float(a[down & above].sum() / max(a.sum(), 1e-9))


def holes_at(m, z):
    out = []
    for poly in slice_polys(m, z):
        for h in poly.interiors:
            c = np.array(h.coords); mn, mx = c.min(0), c.max(0)
            out.append(dict(w=float(mx[0]-mn[0]), h=float(mx[1]-mn[1]),
                            cx=float((mn[0]+mx[0])/2), cy=float((mn[1]+mx[1])/2),
                            area=float(sg.Polygon(h).area)))
    return out


def free_regions(m, z):
    """free (non-solid) regions inside the convex hull at height z"""
    polys = slice_polys(m, z)
    if not polys: return []
    u = sg.MultiPolygon(polys).buffer(0)
    free = u.convex_hull.difference(u)
    out = []
    for g in getattr(free, 'geoms', [free]):
        if g.is_empty or g.area < 4: continue
        b = g.bounds
        out.append(dict(w=float(b[2]-b[0]), h=float(b[3]-b[1]), area=float(g.area),
                        cx=float((b[0]+b[2])/2), cy=float((b[1]+b[3])/2)))
    return out


def span_profile(m, z, axis=0):
    """free-span along `axis` per row of the perpendicular axis, at height z"""
    polys = slice_polys(m, z)
    if not polys: return []
    u = sg.MultiPolygon(polys).buffer(0)
    b = u.bounds
    rows = []
    lo, hi = (b[1], b[3]) if axis == 0 else (b[0], b[2])
    for t in np.arange(lo + 1, hi - 1, 1.0):
        line = sg.LineString([(-1000, t), (1000, t)]) if axis == 0 else                sg.LineString([(t, -1000), (t, 1000)])
        seg = line.intersection(u.convex_hull).difference(u)
        L = 0
        for gg in getattr(seg, 'geoms', [seg]):
            if not gg.is_empty: L = max(L, gg.length)
        rows.append((float(t), float(L)))
    return rows


def round_through_hole(m, dmin=3, dmax=7):
    """detect small round through-hole along any principal axis"""
    for ax_n, rot in ((2, None), (1, [1, 0, 0]), (0, [0, 1, 0])):
        mm = m.copy()
        if rot is not None:
            mm.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, rot))
        mm.apply_translation(-mm.bounds[0])
        h = mm.bounds[1][2]
        for z in np.arange(1.5, max(h - 1, 2), 2.0):
            for hl in holes_at(mm, z):
                if dmin <= hl['w'] <= dmax and dmin <= hl['h'] <= dmax:
                    return True
    return False


def check(res, name, ok, crit=False, detail=""):
    res['checks'].append(dict(name=name, ok=bool(ok), crit=crit, detail=str(detail)))


def common(meshes):
    big = max(meshes, key=lambda m: m.volume if m.is_volume else 0)
    big = big.copy(); big.apply_translation(-big.bounds[0])
    return big


def score(test, path):
    files, meshes = load(path)
    res = dict(test=test, files=files, n_parts=len(meshes), checks=[])
    if not meshes:
        res['error'] = 'no meshes'; return res
    wt = all(m.is_watertight for m in meshes)
    res['watertight'] = wt
    m = common(meshes)
    bb = m.bounds[1] - m.bounds[0]
    res['bbox'] = [round(float(x), 1) for x in bb]
    res['volume_cm3'] = round(float(sum(abs(x.volume) for x in meshes)) / 1000, 1)
    of_up, of_dn = overhang_frac(m, True), overhang_frac(m, False)
    res['overhang_frac'] = round(min(of_up, of_dn), 3)

    if test == 'T1':
        # scan free span along X per y-row at mid height; try both axes, pick the one w/ a clip profile
        best = None
        for axis in (0, 1):
            rows = [r for r in span_profile(m, bb[2] * 0.5, axis) if r[1] > 1]
            if not rows: continue
            spans = [L for _, L in rows]
            for sp in (spans, spans[::-1]):
                entry = sp[0]
                run = []
                for L in sp:
                    if L > 28: break
                    run.append(L)
                pocket = max(run) if run else 0
                if 10 <= entry <= 28 and 16 <= pocket <= 30 and pocket >= entry - 0.5:
                    if best is None or pocket > best[0]:
                        best = (pocket, entry)
        pocket, entry = best if best else (0, 0)
        check(res, 'grip pocket 20-26.5 for d25 handle', 20 <= pocket <= 26.5, True, f'{pocket:.1f}')
        check(res, 'entry gap 15-24 (retention+insertion)', 15 <= entry <= 24, True, f'{entry:.1f}')
        check(res, 'screw hole d3-7 present', round_through_hole(m), True)
        check(res, 'envelope <= 55x50x20', bb[0] <= 55 and bb[1] <= 55 and bb[2] <= 20, False, res['bbox'])
        check(res, 'prints flat (overhang<8%)', res['overhang_frac'] < 0.08, False, res['overhang_frac'])

    elif test == 'T2':
        # slot: scan top-down for a through gap ~13mm wide
        slots = []   # (z, width, length) of slot-like free regions
        for z in np.linspace(1, bb[2] - 1, 34):
            for fr in free_regions(m, z):
                wmin, wmax = sorted((fr['w'], fr['h']))
                if 10 <= wmin <= 18 and wmax >= 40:
                    slots.append((float(z), wmin, wmax))
        slotw = float(np.median([s[1] for s in slots])) if slots else 0
        depth = (max(s[0] for s in slots) - min(s[0] for s in slots) + 2) if slots else 0
        length = max((s[2] for s in slots), default=0)
        # open-ended slot: at a slot z, region length ~= full solid extent along slot axis
        open_ended = False
        if slots:
            zmid = float(np.median([s[0] for s in slots]))
            polys = slice_polys(m, zmid)
            if polys:
                u = sg.MultiPolygon(polys).buffer(0)
                ext = max(u.bounds[2] - u.bounds[0], u.bounds[3] - u.bounds[1])
                open_ended = length >= 0.93 * ext
        check(res, 'slot width 12.1-14.2 (bar 11.7)', 12.1 <= slotw <= 14.2, True, f'{slotw:.1f}')
        check(res, 'slot depth >= 23 (bar 24)', depth >= 23, True, f'{depth:.1f}')
        check(res, 'slot engages bar (>=58, or open-ended >=40)',
              length >= 58 or (open_ended and length >= 40), True,
              f'{length:.1f} open={open_ended}')
        check(res, 'grip 58-95 across, h 45-95', 58 <= max(bb[0], bb[1]) <= 95 and 45 <= bb[2] <= 95, False, res['bbox'])
        check(res, 'supportless in some orientation (<8%)', res['overhang_frac'] < 0.08, False, res['overhang_frac'])

    elif test == 'T3':
        check(res, 'footprint fits 101x165.5 (96-101.2 x 158-165.7)',
              96 <= bb[0] <= 101.2 and 158 <= bb[1] <= 165.7 or
              96 <= bb[1] <= 101.2 and 158 <= bb[0] <= 165.7, True, res['bbox'])
        check(res, 'height 15-25.7', 15 <= bb[2] <= 25.7, True, f'{bb[2]:.1f}')
        hl = holes_at(m, bb[2]*0.5)
        big = [h for h in hl if h['area'] > 150]
        check(res, 'pockets >= 10', len(big) >= 10, True, len(big))
        sizes = sorted(h['area'] for h in big)
        classes = 1
        for a, b2 in zip(sizes, sizes[1:]):
            if b2 > a * 1.25: classes += 1
        check(res, '>=3 pocket size classes', classes >= 3, False, classes)
        small = [h for h in hl if 6 <= h['area'] <= 25]
        check(res, 'hex-bit holes >= 2', len(small) >= 2, False, len(small))
        check(res, 'prints flat (overhang<8%)', res['overhang_frac'] < 0.08, False, res['overhang_frac'])

    elif test == 'T4':
        # cavity at mid height
        cav = None
        for z in np.linspace(bb[2]*0.25, bb[2]*0.95, 12):
            for poly in slice_polys(m, z):
                for h in poly.interiors:
                    c = np.array(h.coords); d = sorted(c.max(0)-c.min(0))
                    if d[1] > 140 and (cav is None or d[0] > cav[0]):
                        cav = [float(d[0]), float(d[1])]
        ok = cav and 73.2 <= cav[0] <= 74.6 and 154.6 <= cav[1] <= 156.0
        check(res, 'cavity 154.6-156 x 73.2-74.6', bool(ok), True, cav)
        # camera cutout in back face (z near 0): hole >= 44x22
        cam = [h for z in (0.5, 1.0, 1.5) for h in holes_at(m, z)
               if max(h['w'], h['h']) >= 42 and min(h['w'], h['h']) >= 20 and h['area'] < 2500]
        check(res, 'camera cutout >=44x22', len(cam) > 0, True,
              f"{[(round(h['w'],1), round(h['h'],1)) for h in cam[:2]]}")
        # retention lip: top slice interior narrower than cavity
        lip = False
        if cav:
            top = slice_polys(m, bb[2]-0.6)
            for poly in top:
                for h in poly.interiors:
                    c = np.array(h.coords); d = sorted(c.max(0)-c.min(0))
                    if d[0] < cav[0] - 1.0: lip = True
            if not top: lip = False
        check(res, 'retention lip at rim', lip, True)
        # usb: opening in bottom edge — detect via slice in wall plane is hard; approximate:
        # look for a gap in the outer boundary of a mid-z slice at the bottom (y min) side
        usb = False
        for z in np.linspace(bb[2]*0.3, bb[2]*0.8, 4):
            polys = slice_polys(m, z)
            if not polys: continue
            u = sg.MultiPolygon(polys).buffer(0)
            hull = u.convex_hull
            free = hull.difference(u)
            for g in getattr(free, 'geoms', [free]):
                if g.is_empty: continue
                gb = g.bounds
                if gb[3] - gb[1] < 30 and 6 <= gb[2]-gb[0] <= 30 and gb[1] < u.bounds[1] + 6:
                    usb = True
        check(res, 'USB opening bottom', usb, False)
        check(res, 'walls 1.6-3.5 (outer minus cavity)',
              cav and 1.6 <= (bb[0]-cav[0])/2 <= 3.5, False,
              cav and round((bb[0]-cav[0])/2, 2))

    crit = [c for c in res['checks'] if c['crit']]
    res['crit_pass'] = sum(c['ok'] for c in crit)
    res['crit_total'] = len(crit)
    res['success'] = bool(wt and all(c['ok'] for c in crit))
    w = sum(2 if c['crit'] else 1 for c in res['checks'])
    res['fit_score'] = round(100 * sum((2 if c['crit'] else 1) * c['ok'] for c in res['checks']) / max(w, 1))
    res['printability'] = round(max(0, 100 - res['overhang_frac'] * 300 - (0 if wt else 40)))
    return res


if __name__ == '__main__':
    r = score(sys.argv[1], sys.argv[2])
    if '--json' in sys.argv:
        print(json.dumps(r))
    else:
        print(f"== {r['test']} parts={r['n_parts']} wt={r.get('watertight')} bbox={r.get('bbox')} vol={r.get('volume_cm3')}cm3 overhang={r.get('overhang_frac')}")
        for c in r['checks']:
            print(f"  [{'X' if c['ok'] else ' '}]{'*' if c['crit'] else ' '} {c['name']}  ({c['detail']})")
        print(f"SUCCESS={r['success']}  fit={r['fit_score']}  printability={r['printability']}")
