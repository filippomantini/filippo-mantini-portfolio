"""FIRST display reconstruction: photographed clay texture and raised, beveled
letter geometry. Uses the eight author-supplied PNG references (not a CAD scan).
Dependencies: numpy, pillow, fonttools, shapely, mapbox-earcut.
"""
from pathlib import Path
import numpy as np, math,json,struct,io
from PIL import Image,ImageOps
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon,Point
from shapely.geometry.polygon import orient
from shapely.affinity import scale as shscale,translate
import mapbox_earcut as earcut
R=Path(__file__).resolve().parents[2];O=R/'public/assets/first';O.mkdir(exist_ok=True);refs=sorted((R.parent/'upload').glob('*20_13*png'));assert len(refs)==8
patch=Image.open(refs[1]).convert('RGB').crop((450,220,730,1000));grain=np.array(patch).mean(2)/255
mirror=Image.new('RGB',(560,780));mirror.paste(patch,(0,0));mirror.paste(ImageOps.mirror(patch),(280,0));atlas=Image.new('RGB',(2048,2048));atlas.paste(mirror.resize((1024,2048),Image.Resampling.LANCZOS),(0,0))
region=np.array(Image.open(refs[0]).convert('RGB'))[1140:1290,330:810];best=region[:24,:24];score=-1
for y in range(0,region.shape[0]-24,4):
 for x in range(0,region.shape[1]-24,4):
  p=region[y:y+24,x:x+24];v=((p.max(2)<75)&(p.mean(2)>8)).mean()
  if v>score:score=v;best=p.copy()
black=Image.fromarray(best);bt=Image.new('RGB',(48,48));bt.paste(black,(0,0));bt.paste(ImageOps.mirror(black),(24,0));bt.paste(ImageOps.flip(black),(0,24));bt.paste(ImageOps.mirror(ImageOps.flip(black)),(24,24))
for y in range(0,2048,48):
 for x in range(1024,2048,48):atlas.paste(bt,(x,y))
encoded=io.BytesIO();atlas.save(encoded,'JPEG',quality=88,subsampling=0,optimize=True);texture=encoded.getvalue();atlas.resize((700,700)).save('/tmp/first-v2-texture.jpg')
positions=[];uvs=[];triangles=[];seams=[]
def vert(xyz,uv):positions.append(xyz);uvs.append(uv);return len(positions)-1
def tri(a,b,c):triangles.append((a,b,c))
class Outline(BasePen):
 def __init__(self,gs):super().__init__(gs);self.contours=[];self.points=[]
 def _moveTo(self,p):self.points=[p]
 def _lineTo(self,p):self.points.append(p)
 def _qCurveToOne(self,p1,p2):
  p0=self._getCurrentPoint()
  for t in np.linspace(0,1,9)[1:]:self.points.append(tuple((1-t)**2*np.array(p0)+2*(1-t)*t*np.array(p1)+t*t*np.array(p2)))
 def _curveToOne(self,p1,p2,p3):
  p0=self._getCurrentPoint()
  for t in np.linspace(0,1,11)[1:]:self.points.append(tuple((1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t*t*np.array(p2)+t**3*np.array(p3)))
 def _closePath(self):
  if len(self.points)>2:self.contours.append(self.points)
  self.points=[]
 def _endPath(self):self._closePath()
f=TTFont(next((R/'public/assets/fonts').glob('inter-tight-700-*.woff2')));gs=f.getGlyphSet();cmap=f.getBestCmap();shapes=[]
for c in 'FIRST':
 pen=Outline(gs);gs[cmap[ord(c)]].draw(pen);shape=Polygon()
 for contour in pen.contours:shape=shape.symmetric_difference(Polygon(contour).buffer(0))
 shapes.append(shape)
height=max(p.bounds[3] for p in shapes)-min(p.bounds[1] for p in shapes);scale=.285/height;gap=.024;total=sum((p.bounds[2]-p.bounds[0])*scale for p in shapes)+4*gap;cursor=-total/2;letter_counts={}
def pieces(p):return [p] if p.geom_type=='Polygon' else list(p.geoms)
def letterxyz(x,y,r):a=x/.50;return [r*math.sin(a),y,r*math.cos(a)]
def face(shape,radius,front=True,inset=None):
 for poly in pieces(shape):
  if poly.area<1e-9:continue
  poly=orient(poly,sign=1);rings=[np.array(poly.exterior.coords[:-1])]+[np.array(h.coords[:-1]) for h in poly.interiors];v=np.concatenate(rings);ids=earcut.triangulate_float64(v,np.cumsum([len(r) for r in rings],dtype=np.uint32)).reshape(-1,3);vs=[]
  for x,y in v:
   r=radius if inset is None else .544 if inset.boundary.distance(Point(x,y))<1e-6 else .533
   vs.append(vert(letterxyz(x,y,r),[.515+.47*(x+total/2)/total,.1+.8*(y+1.32)/.3]))
  for a,b,c in ids:
   cross=(v[b,0]-v[a,0])*(v[c,1]-v[a,1])-(v[b,1]-v[a,1])*(v[c,0]-v[a,0]);t=(vs[a],vs[b],vs[c]);tri(*(t if (cross>0)==front else t[::-1]))
for char,shape in zip('FIRST',shapes):
 x0,y0,x1,y1=shape.bounds;shape=translate(shscale(shape,xfact=scale,yfact=scale,origin=(0,0)),xoff=cursor-x0*scale,yoff=-1.318-y0*scale);cursor+=(x1-x0)*scale+gap;before=len(triangles)
 for poly in pieces(shape):
  poly=orient(poly,sign=1);inner=poly.buffer(-.0035,join_style=1)
  if inner.is_empty:inner=poly
  face(inner,.544);face(poly,.501,False);rim=poly.difference(inner)
  if not rim.is_empty:face(rim,.533,inset=inner)
  for ring in [poly.exterior,*poly.interiors]:
   coords=list(ring.coords)
   for (x,y),(xx,yy) in zip(coords,coords[1:]):
    a=vert(letterxyz(x,y,.501),[.75,.5]);b=vert(letterxyz(xx,yy,.501),[.75,.5]);c=vert(letterxyz(x,y,.533),[.75,.5]);d=vert(letterxyz(xx,yy,.533),[.75,.5]);tri(a,b,c);tri(c,b,d)
 letter_counts[char]=len(triangles)-before
letter_vertices=len(positions)
start=len(positions);N=112;M=112
for j in range(M+1):
 t=j/M
 for i in range(N+1):
  a=i/N*math.tau;r=.425+.018*math.sin(a*2+t*3.3)+.012*math.cos(a*3-t*5);angle=math.atan2(math.sin(a-2.25),math.cos(a-2.25));weight=math.exp(-(angle/.66)**2)
  for center,depth,width in [(.13,.115,.065),(.355,.14,.076),(.59,.145,.079),(.835,.16,.083)]:r-=depth*weight*math.exp(-((t-center)/width)**2)
  thumb=math.atan2(math.sin(a-.25),math.cos(a-.25));r-=.045*math.exp(-(thumb/.7)**2-((t-.81)/.18)**2);r+=(grain[int((1-t)*779),int(i/N*279)]-.47)*.018;top=1.30+.045*math.sin(a*2.2)+.035*math.cos(a*3.1);y=-1+t*(top+1);r*=max(.84,min(1,(t+.007)/.022,(1-t+.006)/.024));vert([r*math.cos(a),y,r*math.sin(a)],[.005+.49*i/N,.005+.99*(1-t)])
for j in range(M):
 for i in range(N):
  a=start+j*(N+1)+i;b=a+N+1;tri(a,b,a+1);tri(a+1,b,b+1)
for j in range(M+1):seams.append((start+j*(N+1),start+j*(N+1)+N))
for j,top in [(0,False),(M,True)]:
 ring=[start+j*(N+1)+i for i in range(N)];center=vert([0,float(np.mean([positions[x][1] for x in ring])),0],[.25,.5])
 for i in range(N):
  a,b=ring[i],ring[(i+1)%N];tri(center,b,a) if top else tri(center,a,b)
start=len(positions);N=144;rings=[(-1.35,.452),(-1.343,.477),(-1.327,.493),(-1.30,.499),(-1.015,.499),(-.991,.492),(-.975,.475),(-.967,.444)]
for y,r in rings:
 for i in range(N+1):
  a=i/N*math.tau;vert([r*math.cos(a),y,r*math.sin(a)],[.005+.49*i/N,.93])
for j in range(len(rings)-1):
 seams.append((start+j*(N+1),start+j*(N+1)+N))
 for i in range(N):
  a=start+j*(N+1)+i;b=a+N+1;tri(a,b,a+1);tri(a+1,b,b+1)
for j,top in [(0,False),(len(rings)-1,True)]:
 center=vert([0,rings[j][0],0],[.25,.93])
 for i in range(N):
  a=start+j*(N+1)+i;b=a+1;tri(center,b,a) if top else tri(center,a,b)
pos=np.array(positions,dtype='<f4');indices=np.array(triangles,dtype='<u2');assert len(pos)<65536;normal=np.zeros_like(pos)
for t in indices:
 n=np.cross(pos[t[1]]-pos[t[0]],pos[t[2]]-pos[t[0]])
 for i in t:normal[i]+=n
for a,b in seams:normal[a]=normal[b]=(normal[a]+normal[b])/2
length=np.linalg.norm(normal,axis=1);normal[length>0]/=length[length>0,None];normal[length==0]=[0,1,0]
views=[];accessors=[];binary=bytearray()
for a,component,typ in [(pos,5126,'VEC3'),(normal,5126,'VEC3'),(np.ones_like(pos),5126,'VEC3'),(indices.flatten(),5123,'SCALAR'),(np.array(uvs,dtype='<f4'),5126,'VEC2')]:
 while len(binary)%4:binary.append(0)
 offset=len(binary);binary.extend(a.tobytes());views.append({'buffer':0,'byteOffset':offset,'byteLength':a.nbytes});v={'bufferView':len(views)-1,'componentType':component,'count':len(a),'type':typ}
 if a is pos:v.update(min=pos.min(0).tolist(),max=pos.max(0).tolist())
 accessors.append(v)
while len(binary)%4:binary.append(0)
offset=len(binary);binary.extend(texture);views.append({'buffer':0,'byteOffset':offset,'byteLength':len(texture)})
while len(binary)%4:binary.append(0)
g={'asset':{'version':'2.0','generator':'FIRST visual reconstruction v2'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'COLOR_0':2,'TEXCOORD_0':4},'indices':3,'material':0}]}],'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'baseColorTexture':{'index':0},'roughnessFactor':.92,'metallicFactor':0},'doubleSided':True}],'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors,'images':[{'bufferView':5,'mimeType':'image/jpeg'}],'textures':[{'source':0,'sampler':0}],'samplers':[{'magFilter':9729,'minFilter':9729,'wrapS':33071,'wrapT':33071}],'extras':{'classification':'interpretative visual reconstruction','photoTexture':True,'raisedLetters':list('FIRST'),'letterTriangleCounts':letter_counts,'letterVertexCount':letter_vertices,'textureSource':'Surface and letter-material crops from author-supplied reference PNGs','textureResolution':[2048,2048],'letterDepth':.043}}
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4);glb=struct.pack('<III',0x46546c67,2,28+len(j)+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary;(O/'first-sculpt-v2.glb').write_bytes(glb)
assert np.isfinite(pos).all() and np.isfinite(normal).all();print('V2:',len(pos),'vertices',len(indices),'triangles',len(glb),'bytes; letters:',letter_counts)
