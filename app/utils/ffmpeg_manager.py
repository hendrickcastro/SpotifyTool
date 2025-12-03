# -*- coding: utf-8 -*-
"""
FFmpeg Manager - Auto-downloads FFmpeg for the current OS
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import shutil
from pathlib import Path

# FFmpeg binary folder in project root
FFMPEG_DIR = Path(__file__).parent.parent.parent / "bin"

# FFmpeg download URLs by platform
FFMPEG_URLS = {
    "Windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
    "Darwin": "https://evermeet.cx/ffmpeg/getrelease/zip",  # macOS
    "Linux": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz",
}


def get_ffmpeg_path() -> str:
    """Get path to ffmpeg executable"""
    system = platform.system()
    
    if system == "Windows":
        return str(FFMPEG_DIR / "ffmpeg.exe")
    else:
        return str(FFMPEG_DIR / "ffmpeg")


def get_ffprobe_path() -> str:
    """Get path to ffprobe executable"""
    system = platform.system()
    
    if system == "Windows":
        return str(FFMPEG_DIR / "ffprobe.exe")
    else:
        return str(FFMPEG_DIR / "ffprobe")


def is_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed locally"""
    ffmpeg = get_ffmpeg_path()
    ffprobe = get_ffprobe_path()
    return os.path.exists(ffmpeg) and os.path.exists(ffprobe)


def download_ffmpeg(progress_callback=None) -> bool:
    """
    Download and extract FFmpeg for the current OS
    
    Args:
        progress_callback: Optional function(message: str) to report progress
    
    Returns:
        True if successful, False otherwise
    """
    system = platform.system()
    
    if system not in FFMPEG_URLS:
        if progress_callback:
            progress_callback(f"[ERROR] Unsupported OS: {system}")
        return False
    
    url = FFMPEG_URLS[system]
    
    # Create bin directory
    FFMPEG_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        if progress_callback:
            progress_callback("[INFO] Downloading FFmpeg... (this may take a minute)")
        
        # Determine file extension
        if system == "Windows" or system == "Darwin":
            temp_file = FFMPEG_DIR / "ffmpeg_temp.zip"
        else:
            temp_file = FFMPEG_DIR / "ffmpeg_temp.tar.xz"
        
        # Download
        urllib.request.urlretrieve(url, temp_file)
        
        if progress_callback:
            progress_callback("[INFO] Extracting FFmpeg...")
        
        # Extract based on OS
        if system == "Windows":
            _extract_windows(temp_file)
        elif system == "Darwin":
            _extract_macos(temp_file)
        else:
            _extract_linux(temp_file)
        
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()
        
        if progress_callback:
            progress_callback("[OK] FFmpeg installed successfully!")
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"[ERROR] Failed to download FFmpeg: {str(e)}")
        return False


def _extract_windows(zip_path: Path):
    """Extract FFmpeg for Windows"""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Find the bin folder inside the zip
        for name in zf.namelist():
            if name.endswith('/bin/ffmpeg.exe'):
                base_path = name.rsplit('/bin/ffmpeg.exe', 1)[0]
                break
        else:
            raise Exception("ffmpeg.exe not found in archive")
        
        # Extract only ffmpeg.exe and ffprobe.exe
        for filename in ['ffmpeg.exe', 'ffprobe.exe']:
            source = f"{base_path}/bin/{filename}"
            target = FFMPEG_DIR / filename
            
            with zf.open(source) as src, open(target, 'wb') as dst:
                dst.write(src.read())


def _extract_macos(zip_path: Path):
    """Extract FFmpeg for macOS"""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(FFMPEG_DIR)
    
    # Make executable
    ffmpeg = FFMPEG_DIR / "ffmpeg"
    if ffmpeg.exists():
        os.chmod(ffmpeg, 0o755)
    
    # For ffprobe, we need to download separately on macOS
    ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
    ffprobe_zip = FFMPEG_DIR / "ffprobe_temp.zip"
    
    urllib.request.urlretrieve(ffprobe_url, ffprobe_zip)
    
    with zipfile.ZipFile(ffprobe_zip, 'r') as zf:
        zf.extractall(FFMPEG_DIR)
    
    ffprobe_zip.unlink()
    
    ffprobe = FFMPEG_DIR / "ffprobe"
    if ffprobe.exists():
        os.chmod(ffprobe, 0o755)


def _extract_linux(tar_path: Path):
    """Extract FFmpeg for Linux"""
    with tarfile.open(tar_path, 'r:xz') as tf:
        # Find the bin folder
        for member in tf.getmembers():
            if member.name.endswith('/bin/ffmpeg'):
                base_path = member.name.rsplit('/bin/ffmpeg', 1)[0]
                break
        else:
            raise Exception("ffmpeg not found in archive")
        
        # Extract only ffmpeg and ffprobe
        for filename in ['ffmpeg', 'ffprobe']:
            source = f"{base_path}/bin/{filename}"
            member = tf.getmember(source)
            member.name = filename  # Rename to just the filename
            tf.extract(member, FFMPEG_DIR)
            
            # Make executable
            target = FFMPEG_DIR / filename
            os.chmod(target, 0o755)


def ensure_ffmpeg(progress_callback=None) -> bool:
    """
    Ensure FFmpeg is available, download if needed
    
    Args:
        progress_callback: Optional function(message: str) to report progress
    
    Returns:
        True if FFmpeg is available, False otherwise
    """
    if is_ffmpeg_installed():
        if progress_callback:
            progress_callback("[OK] FFmpeg already installed")
        return True
    
    return download_ffmpeg(progress_callback)


# Test if run directly
if __name__ == "__main__":
    def print_progress(msg):
        print(msg)
    
    print(f"FFmpeg dir: {FFMPEG_DIR}")
    print(f"FFmpeg path: {get_ffmpeg_path()}")
    print(f"FFprobe path: {get_ffprobe_path()}")
    print(f"Installed: {is_ffmpeg_installed()}")
    
    if not is_ffmpeg_installed():
        print("\nDownloading FFmpeg...")
        ensure_ffmpeg(print_progress)

