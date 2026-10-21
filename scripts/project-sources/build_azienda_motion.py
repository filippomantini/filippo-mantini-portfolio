from pathlib import Path
import subprocess,hashlib,json,concurrent.futures
root=Path(__file__).resolve().parents[2];paths=sorted((Path(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else root.parent/'upload').glob('*.mov'));order=['12.59.03','12.59.32','1.00.01'];manifest=[]
def build(item):
 i,token=item;p=next(p for p in paths if token in p.name);result={'index':i,'source':p.name,'original_bytes':p.stat().st_size,'duration':float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))};result['variants']={}
 for label,width in [('desktop',1920),('mobile',960)]:
  temp=root/f'public/assets/video/azienda-piu-motion-{i:02d}-{label}.mp4'
  subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(p),'-map','0:v:0','-vf',f'scale={width}:-2:flags=lanczos','-c:v','libx264','-preset','slow','-crf','18' if label=='desktop' else '19','-pix_fmt','yuv420p','-an','-movflags','+faststart','-map_metadata','-1','-g','120','-threads','2',str(temp)],check=True)
  dest=temp.with_name(temp.stem+'-'+hashlib.sha256(temp.read_bytes()).hexdigest()[:12]+'.mp4');temp.rename(dest);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(dest)]))['streams'][0];result['variants'][label]={'url':'/'+str(dest.relative_to(root/'public')),'bytes':dest.stat().st_size,'width':probe['width'],'height':probe['height'],'fps':probe['r_frame_rate']}
 poster=root/f'public/assets/responsive/azienda-piu-motion-{i:02d}-poster.webp';subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss','1','-i',str(p),'-frames:v','1','-vf','scale=960:-2','-quality','90',str(poster)],check=True);dest=poster.with_name(poster.stem+'-'+hashlib.sha256(poster.read_bytes()).hexdigest()[:12]+'.webp');poster.rename(dest);result['poster']='/'+str(dest.relative_to(root/'public'));return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(build,enumerate(order,1)):
  manifest.append(result);print(json.dumps(result),flush=True)
(root/'scripts/project-sources/azienda-motion-manifest.json').write_text(json.dumps(manifest,indent=2))
