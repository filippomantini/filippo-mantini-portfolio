"""Refine original FIRST photogrammetry scan: continuous bottom, cleaner clay, unchanged relief."""
from pathlib import Path
import cv2
import numpy as np
import trimesh
from PIL import Image
from scipy import sparse
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import ConvexHull

root=Path(__file__).resolve().parents[2]/'public/assets/first'
src=root/'FIRST_THINGS_FIRST_DA_SCANSIONE_RESTAURO_WEB.glb'
dst=root/'FIRST_THINGS_FIRST_SCANSIONE_LISCIA_V2.glb'
scene=trimesh.load(src,force='scene',process=False)
sculpt=scene.geometry['FIRST_THINGS_FIRST_scultura']
original=sculpt.vertices.copy()
unique,idx=np.unique(np.round(original,6),axis=0,return_inverse=True)
n=len(unique)
cnt=np.bincount(idx,minlength=n).astype('float64')
v=np.zeros((n,3),dtype='float64')
np.add.at(v,idx,original)
v/=cnt[:,None]
face=idx[sculpt.faces]
edges=np.vstack([face[:,[0,1]],face[:,[1,2]],face[:,[2,0]]])
edges=edges[edges[:,0]!=edges[:,1]]
edges=np.vstack([edges,edges[:,::-1]])
adj=sparse.coo_matrix((np.ones(len(edges),dtype='float32'),(edges[:,0],edges[:,1])),shape=(n,n)).tocsr()
adj.data[:]=1
degree=np.array(adj.sum(axis=1)).ravel()
degree[degree==0]=1
adj=sparse.diags(1.0/degree)@adj
# Keep letter edges and the ergonomic thumb/finger recesses, attenuate grain on clay.
weight=.12+.88*np.clip((v[:,1]+.068)/.024,0,1)
for _ in range(45):
    v+=weight[:,None]*(.34*(adj@v-v))
    v+=weight[:,None]*(-.345*(adj@v-v))
sculpt.vertices=v[idx]

# Remove oversharpened photogrammetry normal map; refine noisy baked photo lighting.
material=sculpt.visual.material
albedo=np.asarray(material.baseColorTexture.convert('RGB'))
smooth=cv2.bilateralFilter(albedo,9,30,25)
smooth=cv2.bilateralFilter(smooth,7,26,18).astype('float32')
r,g,b=smooth[:,:,0],smooth[:,:,1],smooth[:,:,2]
chrom=r-(g+b)/2
black=np.clip((45-chrom)/33,0,1)*np.clip((150-r)/95,0,1)
black=cv2.GaussianBlur(black,(0,0),sigmaX=.8)
red=np.stack([np.clip(223+.47*(r-197),154,250),
              np.clip(71+.30*(g-78),48,125),
              np.clip(75+.29*(b-80),48,130)],axis=-1)
dark=np.stack([np.clip(26+.58*(r-30),17,85),
               np.clip(25+.57*(g-30),17,85),
               np.clip(26+.57*(b-30),17,85)],axis=-1)
new=np.clip(red*(1-black[:,:,None])+dark*black[:,:,None],0,255).astype('uint8')
material.baseColorTexture=Image.fromarray(new)
material.normalTexture=None
material.roughnessFactor=.76
material.metallicFactor=0.0
material.doubleSided=True

# The previous disc omitted one entire sector of the actual footprint.
# Infer a perimeter from the scan's lowest original contour, with a narrow bevel.
min_y=float(original[:,1].min())
footprint=sculpt.vertices[sculpt.vertices[:,1]<min_y+.001][:,[0,2]]
hull=ConvexHull(footprint)
shape=footprint[hull.vertices]
center=np.mean(shape,axis=0)
closed=np.vstack([shape,shape[0]])
steps=np.linalg.norm(np.diff(closed,axis=0),axis=1)
arclen=np.r_[0,np.cumsum(steps)]
N=192
position=np.linspace(0,arclen[-1],N,endpoint=False)
loop=np.stack([np.interp(position,arclen,closed[:,k]) for k in range(2)],axis=1)
loop=np.stack([gaussian_filter1d(loop[:,k],2,mode='wrap') for k in range(2)],axis=1)
rings=[]
for scale,y in [(1.006,min_y+.00025),(1.006,min_y-.00040),(.990,min_y-.00155),
                (.966,min_y-.00215),(.80,min_y-.00215),(.56,min_y-.00215),(.28,min_y-.00215)]:
    xy=center+(loop-center)*scale
    rings.append(np.c_[xy[:,0],np.full(N,y),xy[:,1]])
vertices=np.vstack(rings+[np.array([[center[0],min_y-.00215,center[1]]])])
faces=[]
for j in range(len(rings)-1):
    for k in range(N):
        a,b=j*N+k,j*N+(k+1)%N
        c,d=(j+1)*N+k,(j+1)*N+(k+1)%N
        faces.extend([[a,c,b],[b,c,d]])
for k in range(N):
    faces.append([(len(rings)-1)*N+k,len(rings)*N,(len(rings)-1)*N+(k+1)%N])
cap=trimesh.Trimesh(vertices=vertices,faces=np.array(faces),process=False)
if np.mean(cap.face_normals[-N:,1])>0:
    cap.invert()
base_mat=scene.geometry['FIRST_THINGS_FIRST_fondo'].visual.material
base_mat.normalTexture=None
base_mat.roughnessFactor=.82
base_mat.metallicFactor=0.
base_mat.doubleSided=True
rad=max(np.ptp(loop[:,0]),np.ptp(loop[:,1]))*.56
uv=np.stack([.5+(vertices[:,0]-center[0])/(rad*2),
             .5+(vertices[:,2]-center[1])/(rad*2)],axis=1)
cap.visual=trimesh.visual.TextureVisuals(uv=np.clip(uv,0,1),material=base_mat)
scene.delete_geometry('FIRST_THINGS_FIRST_fondo')
scene.add_geometry(cap,geom_name='FIRST_THINGS_FIRST_fondo_pieno',node_name='FIRST_THINGS_FIRST_fondo_pieno')
scene.export(dst)
checked=trimesh.load(dst,force='scene',process=False)
assert len(checked.geometry)==2
assert checked.bounds[0,1] < min_y-.001
assert not checked.geometry['FIRST_THINGS_FIRST_scultura'].visual.material.normalTexture
assert dst.stat().st_size<8000000
print('READY',dst,'bytes',dst.stat().st_size,'underface',checked.bounds[0,1])
