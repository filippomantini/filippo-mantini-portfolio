"""Native paper-support geometry; source artwork and ticket pixels are never redrawn."""
from pathlib import Path
from PIL import Image
import base64,hashlib,math,json,argparse
parser=argparse.ArgumentParser();parser.add_argument("--artwork",required=True);parser.add_argument("--ticket-render",required=True);args=parser.parse_args()
R=Path(__file__).resolve().parents[2];A=R/'public/assets/rebuild-admission';A.mkdir(parents=True,exist_ok=True)
art=Image.open(args.artwork).convert('RGB')
# Format conversion only: no retouching, redrawing or replacement of the artwork.
art.save(A/'wristband-original.webp',quality=98,method=6)
uri='data:image/webp;base64,'+base64.b64encode((A/'wristband-original.webp').read_bytes()).decode()
w,h=art.size
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 100 1200 800"><defs><image id="art" width="{w}" height="{h}" xlink:href="{uri}"/><linearGradient id="paper" x1="0" y1="0" x2=".1" y2="1"><stop stop-color="#d7d5cf"/><stop offset=".38" stop-color="#faf9f5"/><stop offset="1" stop-color="#eeede8"/></linearGradient><linearGradient id="light" x1="0" x2="1"><stop stop-color="#57564e" stop-opacity=".12"/><stop offset=".32" stop-color="#fff" stop-opacity="0"/><stop offset=".76" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#49483f" stop-opacity=".12"/></linearGradient><filter id="shadow" x="-.3" y="-1" width="1.6" height="3"><feGaussianBlur stdDeviation="14"/></filter><filter id="edge" x="-.2" y="-.5" width="1.4" height="2"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#24201b" flood-opacity=".14"/></filter>']
N=40
for i in range(N):parts.append(f'<clipPath id="slice{i}"><rect x="{w*i/N:.5f}" y="0" width="{w/N+.85:.5f}" height="{h}"/></clipPath>')
parts.append('</defs><ellipse cx="610" cy="555" rx="465" ry="27" fill="#34302b" opacity=".18" filter="url(#shadow)"/><path d="M100 428 C183 220 914 179 1100 348 L1098 446 C914 287 185 320 101 523Z" fill="url(#paper)" stroke="#cecac2" stroke-width="1.3"/><path d="M100 428 C183 220 914 179 1100 348" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/><path d="M105 528 C390 556 837 475 1100 446" fill="none" stroke="#4b463c" stroke-opacity=".12" stroke-width="2"/>')
def top(t):return 428-80*t+24*math.sin(math.pi*t)
def height(t):return 99-2*math.cos(math.pi*t)
parts.append('<g filter="url(#edge)">')
for i in range(N):
 t0=i/N;t1=(i+1)/N;u=w*t0
 x0=100+1000*t0;x1=100+1000*t1;y0=top(t0);y1=top(t1)
 a=(x1-x0)/(w/N);b=(y1-y0)/(w/N);d=height((t0+t1)/2)/h
 parts.append(f'<g transform="matrix({a:.8f} {b:.8f} 0 {d:.8f} {x0-a*u:.7f} {y0-b*u:.7f})" clip-path="url(#slice{i})"><use xlink:href="#art"/></g>')
parts.append('</g>')
points=' '.join(f'{100+1000*t:.3f},{top(t):.3f}' for t in [i/N for i in range(N+1)])+' '+' '.join(f'{100+1000*t:.3f},{top(t)+height(t):.3f}' for t in [i/N for i in reversed(range(N+1))])
parts.append(f'<polygon points="{points}" fill="url(#light)"/><path d="M100 428 C427 435 751 381 1100 348" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1"/></svg>')
svg=''.join(parts);digest=hashlib.sha256(svg.encode()).hexdigest()[:12];bracelet='paper-wristband-'+digest+'.svg';(A/bracelet).write_text(svg)
ticket=Image.open(args.ticket_render).convert('RGB');sizes=[]
for width in [540,800,ticket.width]:
 im=ticket if width==ticket.width else ticket.resize((width,round(ticket.height*width/ticket.width)),Image.Resampling.LANCZOS)
 data_path=A/('ticket-'+str(width)+'.webp');im.save(data_path,quality=96,method=6);digest=hashlib.sha256(data_path.read_bytes()).hexdigest()[:12];name='ticket-'+str(width)+'-'+digest+'.webp';data_path.rename(A/name);sizes.append({'width':width,'height':im.height,'file':name})
manifest={'bracelet':bracelet,'ticket':sizes,'artwork_size':list(art.size)};(R/'admission-manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
