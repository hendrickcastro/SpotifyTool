"""
Audio utility functions - Uses embedded FFmpeg
"""

import subprocess
from .ffmpeg_manager import get_ffmpeg_path, get_ffprobe_path


def find_ffmpeg() -> str:
    """Find FFmpeg executable - uses embedded version"""
    return get_ffmpeg_path()


def find_ffprobe() -> str:
    """Find FFprobe executable - uses embedded version"""
    return get_ffprobe_path()


def get_duration(filepath: str) -> float:
    """Get audio file duration in seconds"""
    try:
        ffprobe = get_ffprobe_path()
        cmd = [
            ffprobe, "-v", "error",
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

