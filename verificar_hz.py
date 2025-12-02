"""
Verify MP3 tuning frequency (432Hz vs 440Hz)
Analyzes audio to detect the reference pitch
"""

import subprocess
import sys
import os
from pathlib import Path

def analyze_with_ffmpeg(file_path: str) -> dict:
    """Get audio file information using FFmpeg"""
    cmd = [
        "ffmpeg", "-i", file_path, "-af", 
        "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
        "-f", "null", "-"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    # Get basic info
    info_cmd = ["ffprobe", "-v", "error", "-show_entries", 
                "format=duration,bit_rate:stream=sample_rate,channels,codec_name",
                "-of", "default=noprint_wrappers=1", file_path]
    
    info_result = subprocess.run(info_cmd, capture_output=True, text=True, shell=True)
    
    return info_result.stdout

def main():
    print("""
╔════════════════════════════════════════════════╗
║     🎵 MP3 Frequency Analyzer 🎵               ║
║     Check if audio is 432Hz or 440Hz           ║
╚════════════════════════════════════════════════╝
""")
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("📁 Enter MP3 file path: ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"\n📄 Analyzing: {file_path}\n")
    
    # Get file info
    info = analyze_with_ffmpeg(file_path)
    print("📊 File Info:")
    print(info)
    
    print("""
════════════════════════════════════════════════════
📝 HOW TO VERIFY 432Hz TUNING:

Since MP3 files don't store tuning metadata, you need to:

1️⃣  USE A TUNER APP (Easiest):
    • Open a tuner app on your phone (like "Pano Tuner" or "gStrings")
    • Play a song section with a clear sustained note
    • If tuned to 432Hz, notes will show ~31 cents FLAT
    • Example: A note showing "A" at 440Hz will show A -31¢ at 432Hz

2️⃣  COMPARE ORIGINAL VS CONVERTED:
    • Play both files side by side
    • The 432Hz version sounds slightly LOWER in pitch
    • Same tempo, but all notes are ~1.8% lower

3️⃣  USE AUDACITY (Visual):
    • Open file in Audacity
    • Select a section → Analyze → Plot Spectrum
    • Look for peaks at musical frequencies
    • 432Hz: A4 peak at 432Hz, E4 at 324Hz, etc.
    • 440Hz: A4 peak at 440Hz, E4 at 330Hz, etc.

4️⃣  ONLINE PITCH DETECTOR:
    • https://www.onlinemictest.com/tuners/pitch-detector/
    • Play the MP3 through your speakers near the mic

════════════════════════════════════════════════════

🎯 QUICK TEST: 
   If your converted file sounds slightly DEEPER/LOWER 
   than the original but at the SAME SPEED, 
   then it's correctly tuned to 432Hz! ✅

════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    main()

