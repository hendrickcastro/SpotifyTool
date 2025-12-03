# -*- coding: utf-8 -*-
"""
MP3 432Hz Converter - SIMPLE & WORKING VERSION
Uses proven FFmpeg method for pitch shifting
"""

import subprocess
import sys
import os
import io
from pathlib import Path
from functools import partial

# Fix Windows console encoding and disable buffering
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Force unbuffered print
print = partial(print, flush=True)


def find_ffmpeg() -> str:
    """Find FFmpeg executable"""
    locations = [
        os.path.expanduser("~/.spotdl/ffmpeg.exe"),
        os.path.expanduser("~/AppData/Local/spotdl/ffmpeg.exe"),
        os.path.expanduser("~/.spotdl/ffmpeg"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
        r"D:\_FFMPEG\bin\ffmpeg.exe",
        os.path.expanduser("~/scoop/apps/ffmpeg/current/bin/ffmpeg.exe"),
        "ffmpeg",
    ]
    
    for loc in locations:
        if loc == "ffmpeg":
            try:
                result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True, 
                                        shell=True, encoding='utf-8', errors='ignore')
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip().split('\n')[0].strip()
            except:
                pass
        elif os.path.exists(loc):
            return loc
    
    return None


FFMPEG_PATH = find_ffmpeg()


def convert_single_file(input_file: str, output_file: str) -> bool:
    """Convert a single file from 440Hz to 432Hz"""
    
    if not FFMPEG_PATH:
        print("  [X] FFmpeg not found!")
        return False
    
    pitch_ratio = 432 / 440
    
    cmd_rubberband = [
        FFMPEG_PATH, "-y", "-i", input_file,
        "-af", f"rubberband=pitch={pitch_ratio}",
        "-acodec", "libmp3lame", "-q:a", "0",
        output_file
    ]
    
    print(f"  Converting: {Path(input_file).name}")
    
    result = subprocess.run(cmd_rubberband, capture_output=True, text=True,
                           encoding='utf-8', errors='ignore')
    
    if result.returncode == 0:
        print(f"  [OK] Done (rubberband)")
        return True
    
    speed_compensation = 440 / 432
    
    cmd_fallback = [
        FFMPEG_PATH, "-y", "-i", input_file,
        "-af", f"asetrate=44100*{pitch_ratio},aresample=44100,atempo={speed_compensation}",
        "-acodec", "libmp3lame", "-q:a", "0",
        output_file
    ]
    
    result = subprocess.run(cmd_fallback, capture_output=True, text=True,
                           encoding='utf-8', errors='ignore')
    
    if result.returncode == 0:
        print(f"  [OK] Done (asetrate method)")
        return True
    else:
        print(f"  [X] Failed: {result.stderr[:200]}")
        return False


def test_conversion():
    """Test with a single file"""
    print("")
    print("=" * 60)
    print("    432Hz Converter - TEST MODE")
    print("=" * 60)
    print("")
    
    if FFMPEG_PATH:
        print(f"FFmpeg found: {FFMPEG_PATH}")
    else:
        print("[X] FFmpeg NOT FOUND!")
        print("   Install with: winget install FFmpeg")
        return
    
    if len(sys.argv) < 2:
        input_file = input("Input MP3 file: ").strip().strip('"')
    else:
        input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"[X] File not found: {input_file}")
        return
    
    input_path = Path(input_file)
    output_file = str(input_path.parent / f"{input_path.stem}_432hz_v2{input_path.suffix}")
    
    print(f"\nInput:  {input_file}")
    print(f"Output: {output_file}")
    print(f"Ratio:  432/440 = {432/440:.6f}")
    print("")
    
    success = convert_single_file(input_file, output_file)
    
    if success:
        print("\nVerifying conversion...")
        
        def get_duration(filepath):
            ffprobe = FFMPEG_PATH.replace("ffmpeg", "ffprobe") if FFMPEG_PATH else "ffprobe"
            cmd = [ffprobe, "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=noprint_wrappers=1:nokey=1", filepath]
            result = subprocess.run(cmd, capture_output=True, text=True,
                                   encoding='utf-8', errors='ignore')
            try:
                return float(result.stdout.strip())
            except:
                return 0
        
        orig_dur = get_duration(input_file)
        conv_dur = get_duration(output_file)
        
        print(f"\n  Original duration:  {orig_dur:.3f}s")
        print(f"  Converted duration: {conv_dur:.3f}s")
        
        if orig_dur > 0 and conv_dur > 0:
            ratio = conv_dur / orig_dur
            print(f"  Duration ratio:     {ratio:.6f}")
            
            if abs(ratio - 1.0) < 0.02:
                print("\n  [OK] SUCCESS! Durations match (tempo preserved)")
                print("  [OK] Pitch should be lowered to 432Hz")
                print(f"\n  Output file: {output_file}")
            else:
                print(f"\n  [!] Duration ratio is {ratio:.4f}, expected ~1.0")
    else:
        print("\n[X] Conversion failed")


def convert_folder(input_dir: str, output_dir: str = None):
    """Convert all MP3 files in a folder"""
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"[X] Folder not found: {input_dir}")
        return
    
    mp3_files = list(input_path.glob("*.mp3"))
    
    if not mp3_files:
        print(f"[X] No MP3 files found in: {input_dir}")
        return
    
    out_path = Path(output_dir) if output_dir else input_path / "432hz_v2"
    out_path.mkdir(parents=True, exist_ok=True)
    
    print("")
    print("=" * 60)
    print("    432Hz Batch Converter")
    print("=" * 60)
    print("")
    print(f"Input:  {input_path}")
    print(f"Output: {out_path}")
    print(f"Files:  {len(mp3_files)}")
    print(f"Ratio:  432/440 = {432/440:.6f}")
    print("")
    
    success_count = 0
    skipped_count = 0
    
    for mp3_file in mp3_files:
        output_file = out_path / f"{mp3_file.stem}_432hz{mp3_file.suffix}"
        
        if output_file.exists():
            print(f"  [SKIP] Already exists: {mp3_file.name}")
            skipped_count += 1
            continue
        
        if convert_single_file(str(mp3_file), str(output_file)):
            success_count += 1
    
    print("")
    print("=" * 60)
    print(f"Converted: {success_count} files")
    print(f"Skipped:   {skipped_count} files (already exist)")
    print(f"Output:    {out_path}")
    print("=" * 60)
    print("")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            convert_folder(arg, output_dir)
        else:
            test_conversion()
    else:
        print("Usage:")
        print("  Test single file: python convertir_432hz_v2.py file.mp3")
        print("  Convert folder:   python convertir_432hz_v2.py ./folder")
        print("")
        test_conversion()
