"""
MP3 Frequency Converter - 440Hz to 432Hz (HIGH QUALITY)
Converts audio files to 432Hz tuning using professional-grade pitch shifting
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Conversion ratio: 432/440 = 0.981818...
RATIO_432 = 432 / 440


def find_ffmpeg() -> str:
    """Find FFmpeg executable"""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\ffmpeg\bin\ffmpeg.exe"),
        os.path.expanduser(r"~\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"),
        os.path.expanduser(r"~\.spotdl\ffmpeg.exe"),
        os.path.expanduser(r"~\AppData\Local\spotdl\ffmpeg.exe"),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    try:
        result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True, shell=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return "ffmpeg"


def check_rubberband_support(ffmpeg_path: str) -> bool:
    """Check if FFmpeg has rubberband support"""
    try:
        result = subprocess.run(
            [ffmpeg_path, "-filters"],
            capture_output=True,
            text=True,
            shell=True
        )
        return "rubberband" in result.stdout
    except:
        return False


FFMPEG_PATH = find_ffmpeg()
HAS_RUBBERBAND = check_rubberband_support(FFMPEG_PATH)


def convert_to_432hz(input_file: Path, output_dir: Path, keep_original: bool = True) -> tuple[bool, str]:
    """
    Convert audio from 440Hz to 432Hz with HIGH QUALITY
    
    Uses rubberband if available (best quality), otherwise falls back to 
    high-quality resampling method
    """
    try:
        if keep_original:
            output_file = output_dir / f"{input_file.stem}_432hz{input_file.suffix}"
        else:
            output_file = output_dir / input_file.name
        
        if HAS_RUBBERBAND:
            # BEST QUALITY: Rubberband pitch shifting
            # Preserves tempo, minimal artifacts, professional quality
            audio_filter = f"rubberband=pitch={RATIO_432}:formant=preserved"
        else:
            # HIGH QUALITY FALLBACK: 
            # Use high-quality resampling with proper compensation
            # asetrate changes pitch, aresample with high quality settings
            audio_filter = (
                f"asetrate=44100*{RATIO_432},"
                f"aresample=44100:resampler=soxr:precision=28:cutoff=1:dither_method=triangular,"
                f"atempo={1/RATIO_432}"
            )
        
        cmd = [
            FFMPEG_PATH,
            "-i", str(input_file),
            "-af", audio_filter,
            "-acodec", "libmp3lame",
            "-q:a", "0",  # Highest VBR quality
            "-y",
            "-loglevel", "error",
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            return True, f"✓ {input_file.name}"
        else:
            return False, f"✗ {input_file.name}: {result.stderr[:100]}"
            
    except Exception as e:
        return False, f"✗ {input_file.name}: {str(e)}"


def convert_folder(input_dir: str, output_dir: str = None, replace: bool = False, workers: int = 4):
    """Convert all MP3 files in a folder to 432Hz"""
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ Folder not found: {input_dir}")
        return
    
    mp3_files = list(input_path.glob("*.mp3"))
    
    if not mp3_files:
        print(f"❌ No MP3 files found in: {input_dir}")
        return
    
    if replace:
        out_path = input_path
        keep_original = False
    else:
        out_path = Path(output_dir) if output_dir else input_path / "432hz"
        out_path.mkdir(parents=True, exist_ok=True)
        keep_original = True
    
    quality_method = "🎯 Rubberband (BEST)" if HAS_RUBBERBAND else "🎚️ SoXR High-Quality"
    
    print(f"""
╔═══════════════════════════════════════════════════╗
║     🎵 MP3 432Hz Converter - HIGH QUALITY 🎵      ║
║     Converting from 440Hz to 432Hz                ║
╚═══════════════════════════════════════════════════╝

📁 Input:   {input_path}
📁 Output:  {out_path}
🎵 Files:   {len(mp3_files)} MP3s
⚡ Workers: {workers}
🔧 FFmpeg:  {FFMPEG_PATH}
{quality_method}
🎚️ Ratio:   {RATIO_432:.6f} (432/440)
🔊 Output:  VBR Quality 0 (Highest)
""")
    
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(convert_to_432hz, f, out_path, keep_original): f 
            for f in mp3_files
        }
        
        for future in as_completed(futures):
            success, message = future.result()
            print(message)
            if success:
                successful += 1
            else:
                failed += 1
    
    print(f"""
═══════════════════════════════════════════════════
✅ Completed: {successful}/{len(mp3_files)} files converted
❌ Failed: {failed}
📁 Output folder: {out_path}
═══════════════════════════════════════════════════
""")


def main():
    """Main entry point"""
    quality_method = "🎯 Rubberband (Professional)" if HAS_RUBBERBAND else "🎚️ SoXR (High-Quality)"
    
    print(f"""
╔═══════════════════════════════════════════════════╗
║     🎵 MP3 432Hz Converter - HIGH QUALITY 🎵      ║
║     "The Natural Frequency"                       ║
╚═══════════════════════════════════════════════════╝

🔧 FFmpeg: {FFMPEG_PATH}
{quality_method}
""")
    
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_dir = input("📁 Folder with MP3s (Enter for ./downloads): ").strip() or "./downloads"
        output_dir = input("📁 Output folder (Enter for /432hz): ").strip() or None
    
    convert_folder(input_dir, output_dir)


if __name__ == "__main__":
    main()
