"""Render the same GLB mesh used by the interactive viewer into portfolio plates."""
from pathlib import Path
import json,struct,math,io
import numpy as np
from PIL import Image,ImageFilter
root=Path(__file__).resolve().parents[2];out=root/'public/assets/first';raw=(out/'first-study-v1.glb').read_bytes();jl=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+jl]);start=28+jl
arrays=[]
for a in g['accessors']:
 v=g['bufferViews'][a['bufferView']];n={'VEC3':3,'VEC2':2,'SCALAR':1}[a['type']];arr=np.frombuffer(raw,dtype='<f4' if a['componentType']==5126 else '<u2',count=a['count']*n,offset=start+v.get('byteOffset',0)+a.get('byteOffset',0));arrays.append(arr.reshape(-1,n))
pos,norm,col,indices,uv=arrays;indices=indices.flatten().reshape(-1,3);bv=g['bufferViews'][g['images'][0]['bufferView']];tex=np.array(Image.open(io.BytesIO(raw[start+bv['byteOffset']:start+bv['byteOffset']+bv['byteLength']])).convert('RGB'))/255

def render(name,yaw,pitch,width=850,height=1000):
 scale=1.5;W=int(width*scale);H=int(height*scale);cy,sy=math.cos(yaw),math.sin(yaw);cx,sx=math.cos(pitch),math.sin(pitch);rot=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])@np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
 p=pos@rot.T;n=norm@rot.T;factor=H*.38;screen=np.stack([p[:,0]*factor+W/2,-p[:,1]*factor+H*.49],1);depth=np.full((H,W),-np.inf,dtype='f4');image=np.zeros((H,W,4),dtype='uint8');light=np.array([-.6,.8,1]);light/=np.linalg.norm(light)
 for tri in indices:
  xy=screen[tri];x0,y0=np.maximum(np.floor(xy.min(0)).astype(int),0);x1,y1=np.minimum(np.ceil(xy.max(0)).astype(int),[W-1,H-1])
  if x1<x0 or y1<y0:continue
  a,b,c=xy;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
  if abs(den)<1e-9:continue
  yy,xx=np.mgrid[y0:y1+1,x0:x1+1];w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1;weights=np.stack([w0,w1,w2],-1);z=weights@p[tri,2];hit=(weights.min(-1)>=-1e-5)&(z>depth[y0:y1+1,x0:x1+1]);
  if not hit.any():continue
  ns=weights@n[tri];ns/=np.maximum(np.linalg.norm(ns,axis=-1,keepdims=True),1e-8);illum=.42+.58*np.maximum(0,ns@light);coords=weights@uv[tri];tx=np.clip((coords[...,0]*1023).astype(int),0,1023);ty=np.clip((coords[...,1]*1023).astype(int),0,1023);rgb=(weights@col[tri])*tex[ty,tx]*illum[...,None];rgba=np.concatenate([np.clip(rgb*255,0,255).astype('uint8'),np.full((*rgb.shape[:2],1),255,dtype='uint8')],-1);image[y0:y1+1,x0:x1+1][hit]=rgba[hit];depth[y0:y1+1,x0:x1+1][hit]=z[hit]
 im=Image.fromarray(image).resize((width,height),Image.Resampling.LANCZOS);im.save(out/(name+'.webp'),'WEBP',lossless=True,method=6)
 
 if name=='render-front':
  bg=Image.new('RGBA',im.size,'#ece9e3');bg.alpha_composite(im);bg.convert('RGB').save('/tmp/first-render.jpg')
 print(name,(out/(name+'.webp')).stat().st_size)
for args in [('render-front',-1.05,-.07),('render-back',1.65,.08),('render-three-quarter',-.45,.12),('render-top',-.7,.75)]:render(*args)
