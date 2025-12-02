"""
Simple Spotify Downloader - Just paste your playlist URL!
"""
import subprocess
import sys
from pathlib import Path

def download(url: str):
    """Download from Spotify URL"""
    output_dir = Path("./downloads")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n🎵 Downloading from: {url}")
    print(f"📁 Output folder: {output_dir.absolute()}\n")
    
    cmd = [
        sys.executable, "-m", "spotdl",
        "--output", str(output_dir),
        "--format", "mp3",
        "--bitrate", "320k",
        url
    ]
    
    subprocess.run(cmd)
    print("\n✅ Done!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download(sys.argv[1])
    else:
        print("🎵 Spotify Playlist Downloader 🎵\n")
        url = input("Paste Spotify URL (playlist/album/track): ").strip()
        if url:
            download(url)
        else:
            print("No URL provided!")

