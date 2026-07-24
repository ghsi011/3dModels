import json, sys
import numpy as np, trimesh

M = np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,16.0],[0,0,0,1]])
THR = -0.70710679
BED_TOL = 0.05
m = trimesh.load("candidate_tool.stl", force="mesh", process=True)
v = trimesh.transform_points(m.vertices, M)
tri = v[m.faces]
ea = tri[:,1]-tri[:,0]; eb = tri[:,2]-tri[:,0]
cr = np.cross(ea,eb); da = np.linalg.norm(cr,axis=1)
valid = da>1e-12
n = np.zeros_like(cr); n[valid]=cr[valid]/da[valid,None]
areas = da*0.5
bed = np.max(np.abs(tri[:,:,2]-0.0),axis=1) <= BED_TOL
down = n[:,2] <= THR
oob = valid & down & ~bed
cent = tri.mean(axis=1)  # printer-space centroids
idx = np.where(oob)[0]
print("oob faces", len(idx), "area", round(areas[oob].sum(),4))
# cluster by rounded (installed) location + normal signature
inst = m.triangles.mean(axis=1)  # installed centroids
rows=[]
for i in idx:
    rows.append((round(float(n[i,2]),3), round(float(inst[i,0]),1), round(float(inst[i,1]),2),
                 round(float(inst[i,2]),2), round(float(areas[i]),4)))
# group by normal_z bucket and installed Y,Z region
from collections import defaultdict
g=defaultdict(lambda:[0,0.0])
for nz,ix,iy,iz,a in rows:
    key=(nz, round(iy,1), round(iz,0))
    g[key][0]+=1; g[key][1]+=a
print("group (normal_z, instY, instZ) -> count, area")
for k in sorted(g, key=lambda k:-g[k][1]):
    print(" ", k, g[k][0], round(g[k][1],4))
# bounds of offending installed centroids
ic = inst[idx]
print("inst X", round(ic[:,0].min(),2), round(ic[:,0].max(),2),
      "Y", round(ic[:,1].min(),2), round(ic[:,1].max(),2),
      "Z", round(ic[:,2].min(),2), round(ic[:,2].max(),2))
print("normal_z range", round(n[idx,2].min(),5), round(n[idx,2].max(),5))
