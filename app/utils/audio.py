"""
Audio utility functions
"""

import subprocess
import os
import shutil


def find_ffmpeg() -> str:
    """Find FFmpeg executable"""
    # Check if in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Common locations
    locations = [
        os.path.expanduser("~/.spotdl/ffmpeg.exe"),
        os.path.expanduser("~/AppData/Local/spotdl/ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
        r"D:\_FFMPEG\bin\ffmpeg.exe",
    ]
    
    for loc in locations:
        if os.path.exists(loc):
            return loc
    
    return None


def get_duration(filepath: str) -> float:
    """Get audio file duration in seconds"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filepath
        ]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return float(result.stdout.strip())
    except:
        return 0.0

