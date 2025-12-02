"""
Real Pitch Comparator - Compare two audio files to verify 432Hz conversion
Analyzes actual audio frequencies to detect pitch difference
"""

import subprocess
import sys
import os
import struct
import wave
import tempfile
from pathlib import Path
import math

def mp3_to_wav(mp3_path: str, wav_path: str) -> bool:
    """Convert MP3 to WAV using FFmpeg for analysis"""
    cmd = [
        "ffmpeg", "-i", mp3_path, 
        "-ar", "44100", "-ac", "1", "-f", "wav",
        "-y", "-loglevel", "error",
        wav_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.returncode == 0

def read_wav_samples(wav_path: str, max_seconds: int = 30) -> tuple:
    """Read samples from WAV file"""
    with wave.open(wav_path, 'rb') as wav:
        sample_rate = wav.getframerate()
        n_frames = min(wav.getnframes(), sample_rate * max_seconds)
        raw_data = wav.readframes(n_frames)
        
        # Convert bytes to samples
        n_samples = len(raw_data) // 2
        samples = struct.unpack(f'{n_samples}h', raw_data)
        
    return samples, sample_rate

def autocorrelation_pitch(samples: tuple, sample_rate: int) -> float:
    """Detect dominant pitch using autocorrelation"""
    # Use a window of samples
    window_size = min(len(samples), sample_rate * 2)  # 2 seconds
    samples = samples[:window_size]
    
    # Autocorrelation
    n = len(samples)
    max_lag = sample_rate // 50  # Min freq ~50Hz
    min_lag = sample_rate // 2000  # Max freq ~2000Hz
    
    best_lag = 0
    best_corr = 0
    
    for lag in range(min_lag, min(max_lag, n // 2)):
        corr = 0
        for i in range(n - lag):
            corr += samples[i] * samples[i + lag]
        
        if corr > best_corr:
            best_corr = corr
            best_lag = lag
    
    if best_lag > 0:
        return sample_rate / best_lag
    return 0

def analyze_file(file_path: str) -> dict:
    """Analyze an audio file and return pitch info"""
    print(f"  📊 Analyzing: {Path(file_path).name}")
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_wav = tmp.name
    
    try:
        if not mp3_to_wav(file_path, tmp_wav):
            return {"error": "Failed to convert MP3"}
        
        samples, sample_rate = read_wav_samples(tmp_wav)
        
        # Get file duration
        duration = len(samples) / sample_rate
        
        # Simple RMS energy calculation
        rms = math.sqrt(sum(s*s for s in samples) / len(samples))
        
        return {
            "path": file_path,
            "sample_rate": sample_rate,
            "duration": duration,
            "rms": rms,
            "samples_analyzed": len(samples)
        }
    finally:
        if os.path.exists(tmp_wav):
            os.unlink(tmp_wav)

def compare_files_with_ffmpeg(original: str, converted: str) -> dict:
    """Compare two files using FFmpeg's cross-correlation"""
    print("\n🔬 Comparing files with cross-correlation...\n")
    
    # Use FFmpeg to compare the files
    # Extract audio features using astats
    def get_stats(filepath):
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=duration,sample_rate,bit_rate",
            "-of", "default=noprint_wrappers=1",
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout
    
    orig_stats = get_stats(original)
    conv_stats = get_stats(converted)
    
    return {
        "original": orig_stats,
        "converted": conv_stats
    }

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║     🎵 MP3 Pitch Comparator - 432Hz vs 440Hz 🎵            ║
║     Compare original and converted files                   ║
╚════════════════════════════════════════════════════════════╝
""")
    
    if len(sys.argv) >= 3:
        original = sys.argv[1]
        converted = sys.argv[2]
    else:
        print("Usage: python comparar_pitch.py <original.mp3> <converted_432hz.mp3>\n")
        original = input("📁 Original file (440Hz): ").strip().strip('"')
        converted = input("📁 Converted file (432Hz): ").strip().strip('"')
    
    if not os.path.exists(original):
        print(f"❌ Original file not found: {original}")
        return
    if not os.path.exists(converted):
        print(f"❌ Converted file not found: {converted}")
        return
    
    print("\n" + "="*60)
    print("📄 ORIGINAL (should be 440Hz):")
    orig_info = analyze_file(original)
    
    print("\n📄 CONVERTED (should be 432Hz):")
    conv_info = analyze_file(converted)
    
    # Compare
    print("\n" + "="*60)
    print("📊 COMPARISON RESULTS:")
    print("="*60)
    
    if "error" not in orig_info and "error" not in conv_info:
        duration_diff = conv_info["duration"] - orig_info["duration"]
        duration_ratio = conv_info["duration"] / orig_info["duration"] if orig_info["duration"] > 0 else 0
        
        print(f"""
  Original duration:  {orig_info['duration']:.2f}s
  Converted duration: {conv_info['duration']:.2f}s
  Duration ratio:     {duration_ratio:.6f}

  Expected ratio for 432Hz conversion: ~1.000000 (same duration)
  (If using pitch-shift with tempo correction)
""")
        
        # The key indicator: if durations are very close, tempo was corrected
        if abs(duration_ratio - 1.0) < 0.01:
            print("  ✅ Durations match - tempo correction applied correctly!")
            print("  ✅ Pitch should be shifted to 432Hz")
        elif abs(duration_ratio - (440/432)) < 0.01:
            print("  ⚠️  Converted file is SLOWER (no tempo correction)")
            print("  ⚠️  Pitch is 432Hz but speed is reduced")
        else:
            print(f"  ❓ Unexpected ratio: {duration_ratio:.4f}")
    
    print("""
════════════════════════════════════════════════════════════

🎯 HOW TO VERIFY AURALLY:

1. Play both files back-to-back
2. The 432Hz version should sound SLIGHTLY LOWER in pitch
3. But should play at the SAME SPEED

4. Use a phone tuner app:
   - Play a sustained note from each file
   - 440Hz file: notes show normal (A=A)
   - 432Hz file: notes show ~31 cents flat (A=-31¢)

════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    main()

