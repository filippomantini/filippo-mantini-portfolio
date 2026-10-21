"""Build web playback copies; keep original masters, dimensions and frame rates."""
from pathlib import Path
import hashlib
import subprocess

PUBLIC = Path('public')
ASSETS = PUBLIC / 'assets'
FILES = [ASSETS / 'vibrazioni-process.mp4', *sorted((ASSETS / 'collapse/ss26').glob('*-1080p.mp4'))]
RECIPE = b'web-video-v1-crf20-vib23-faststart-gop2s'


def build_video_delivery():
    dest_dir = ASSETS / 'video'
    dest_dir.mkdir(exist_ok=True)
    mapping = {}
    for source in FILES:
        if not source.exists():
            raise FileNotFoundError(source)
        silent = source.name == 'vibrazioni-process.mp4'
        key = hashlib.sha256(source.read_bytes() + (b'vib-copy-silent-faststart-v1' if silent else RECIPE)).hexdigest()[:12]
        dest = dest_dir / f'{source.stem}-{key}.mp4'
        if not dest.exists():
            temp = dest.with_suffix('.tmp.mp4')
            command = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(source),
                       '-map', '0:v:0', '-c:v', 'libx264', '-preset', 'slow',
                       '-crf', '23' if silent else '20', '-pix_fmt', 'yuv420p',
                       '-maxrate', '1100k' if silent else '5000k',
                       '-bufsize', '2200k' if silent else '10000k',
                       '-force_key_frames', 'expr:gte(t,n_forced*2)',
                       '-threads', '2', '-movflags', '+faststart', '-map_metadata', '-1']
            command += ['-map', '0:a:0?', '-c:a', 'aac', '-b:a', '128k']
            if silent:
                # Removing audio and moving moov is lossless for the picture.
                command = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(source),
                           '-map', '0:v:0', '-c:v', 'copy', '-an', '-movflags', '+faststart', '-map_metadata', '-1']
            subprocess.run(command + [str(temp)], check=True)
            temp.replace(dest)
        original_url = '/' + source.relative_to(PUBLIC).as_posix()
        output_url = '/' + dest.relative_to(PUBLIC).as_posix()
        mapping[original_url] = output_url
        mapping[output_url] = output_url
    return mapping


if __name__ == '__main__':
    for source, output in build_video_delivery().items():
        if source != output:
            print(source, '->', output)
