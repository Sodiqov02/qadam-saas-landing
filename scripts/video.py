"""Prepare real footage only, with FFmpeg; no placeholder video generation."""
import argparse
from pathlib import Path
import shutil
import subprocess

def command(source,output,vertical=False):
    width,height=(1080,1920) if vertical else (1920,1080)
    # Preserve readable interfaces: pad rather than crop the original footage.
    return ['ffmpeg','-n','-i',str(source),'-t','30','-vf',f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x102d22','-c:v','libx264','-crf','23','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-c:a','aac','-b:a','128k',str(output)]

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--dry-run',action='store_true');args=parser.parse_args()
    if not args.source.is_file():parser.error('Provide actual approved source footage')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for vertical in [False,True]:
        cmd=command(args.source,args.output_dir/('qadamup-9x16.mp4' if vertical else 'qadamup-16x9.mp4'),vertical)
        if args.dry_run: print(subprocess.list2cmdline(cmd))
        else:
            if not shutil.which('ffmpeg'):parser.error('FFmpeg is not installed; install it before rendering')
            subprocess.run(cmd,check=True)
