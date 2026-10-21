"""Interpretative FIRST display mesh, not a scan or manufacturing model.
Nominal proportions: 105 mm tall, 50 mm diameter, from the original project PDF.
Recess positions are visually estimated from the author's photographs.
"""
from pathlib import Path
import json,struct,math,io
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[2];out=root/'public/assets/first';out.mkdir(exist_ok=True)
f=TTFont(next((root/'public/assets/fonts').glob('inter-tight-700-*.woff2')));f.flavor=None;f.save('/tmp/first-label-font.ttf')
mask=Image.new('RGB',(1024,1024),'white');d=ImageDraw.Draw(mask);font=ImageFont.truetype('/tmp/first-label-font.ttf',145)
# A complete FIRST label represents the design concept; current prototype photos retain the lost letter.
for i,c in enumerate('FIRST'):d.text((i*202+40,840),c,font=font,fill=(16,16,16))
N=96;M=80;positions=[];colors=[];uvs=[]
for j in range(M+1):
 t=j/M;y=(t-.5)*2.1
 for i in range(N+1):
  a=i/N*math.tau
  radius=.463+.012*math.sin(a*3+t*6)+.009*math.sin(a*5-t*9)
  if t<.18:radius=.49
  if .18<t<.225:radius-=.045*math.exp(-((t-.203)/.012)**2)
  if t>.23:
   angular=math.exp(-(math.atan2(math.sin(a),math.cos(a))/.65)**2)
   for center,depth,width in [(.32,.12,.052),(.49,.145,.065),(.68,.15,.065),(.87,.15,.072)]:radius-=depth*angular*math.exp(-((t-center)/width)**2)
   thumb=math.atan2(math.sin(a-2.5),math.cos(a-2.5));radius-=.08*math.exp(-(thumb/.7)**2-((t-.78)/.16)**2)
  radius*=min(1,t/.018,(1-t)/.018)
  positions.append([radius*math.cos(a),y,radius*math.sin(a)])
  shade=.97+.03*math.sin(a*29+t*95)*math.sin(a*17-t*80);c=[.86*shade,.17*shade,.12*shade]
  uvs.append([1-i/N,1-t])
  colors.append(c)
pos=np.array(positions,dtype='<f4');idx=[]
for j in range(M):
 for i in range(N):
  a=j*(N+1)+i;b=a+N+1
  for tri in [(a,b,a+1),(a+1,b,b+1)]:
   if np.linalg.norm(np.cross(pos[tri[1]]-pos[tri[0]],pos[tri[2]]-pos[tri[0]]))>1e-9:idx.extend(tri)
indices=np.array(idx,dtype='<u2');norm=np.zeros_like(pos)
for tri in indices.reshape(-1,3):
 v=np.cross(pos[tri[1]]-pos[tri[0]],pos[tri[2]]-pos[tri[0]])
 for vtx in tri:norm[vtx]+=v
for j in range(M+1):
 a=j*(N+1);b=a+N;norm[a]=norm[b]=(norm[a]+norm[b])/2
lens=np.linalg.norm(norm,axis=1);norm[lens>0]/=lens[lens>0,None];norm[lens==0]=[0,1,0]
col=np.array(colors,dtype='<f4');views=[];accessors=[];binary=bytearray()
for array,component,typ in [(pos,5126,'VEC3'),(norm,5126,'VEC3'),(col,5126,'VEC3'),(indices,5123,'SCALAR'),(np.array(uvs,dtype='<f4'),5126,'VEC2')]:
 while len(binary)%4:binary.append(0)
 offset=len(binary);raw=array.tobytes();binary.extend(raw);views.append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)})
 acc={'bufferView':len(views)-1,'componentType':component,'count':len(array),'type':typ}
 if array is pos:acc.update(min=pos.min(axis=0).tolist(),max=pos.max(axis=0).tolist())
 accessors.append(acc)
texture=io.BytesIO();mask.save(texture,'PNG',optimize=True);texture=texture.getvalue();texture_offset=len(binary);binary.extend(texture);views.append({'buffer':0,'byteOffset':texture_offset,'byteLength':len(texture)})
while len(binary)%4:binary.append(0)
gltf={'asset':{'version':'2.0','generator':'FIRST interpretative portfolio model'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'COLOR_0':2,'TEXCOORD_0':4},'indices':3,'material':0}]}],'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'baseColorTexture':{'index':0},'metallicFactor':0,'roughnessFactor':.95},'doubleSided':True}],'images':[{'bufferView':5,'mimeType':'image/png'}],'textures':[{'source':0,'sampler':0}],'samplers':[{'magFilter':9729,'minFilter':9729,'wrapS':33071,'wrapT':33071}],'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors,'extras':{'classification':'interpretative reconstruction, not photogrammetry','author':'Filippo Mantini','nominalDimensionsMm':[50,105,50],'note':'Grip shape and surface estimated from reference photographs. Complete FIRST label represents original concept.'}}
js=json.dumps(gltf,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
glb=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary
(out/'first-study-v1.glb').write_bytes(glb)
assert np.isfinite(pos).all() and np.isfinite(norm).all();assert indices.max()<len(pos)
mask.save(out/'model-label.png')
print(len(pos),'vertices',len(indices)//3,'triangles',len(glb),'bytes')
