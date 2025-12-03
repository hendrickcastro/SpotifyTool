"""
SpotifyTool - Main Application
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

from .constants import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from .components import Sidebar, StatusBar
from .pages import DownloadPage, ConvertPage, VerifyPage, SettingsPage
from .utils import get_ffmpeg_path, get_ffprobe_path, is_ffmpeg_installed, ensure_ffmpeg

# Log file path
LOG_FILE = Path(__file__).parent.parent / "spotifytool.log"

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SpotifyDLApp(ctk.CTk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("SpotifyTool")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI
        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()
        self._create_pages()
        
        # Show default page
        self.show_page("download")
        
        # Check FFmpeg on startup
        self.after(500, self._check_ffmpeg)
    
    def _check_ffmpeg(self):
        """Check and download FFmpeg if needed"""
        if not is_ffmpeg_installed():
            self.status_bar.set_status("Downloading FFmpeg...", COLORS['warning'])
            self.log("download", "[INFO] FFmpeg not found, downloading...")
            
            def download_thread():
                def progress(msg):
                    self.after(0, lambda m=msg: self.log("download", m))
                
                success = ensure_ffmpeg(progress)
                
                if success:
                    self.after(0, lambda: self.status_bar.set_status("FFmpeg ready!", COLORS['success']))
                else:
                    self.after(0, lambda: self.status_bar.set_status("FFmpeg download failed", COLORS['error']))
                    self.after(0, lambda: messagebox.showerror("Error", 
                        "Failed to download FFmpeg. Please install it manually."))
            
            threading.Thread(target=download_thread, daemon=True).start()
        else:
            self.status_bar.set_status("Ready", COLORS['text_muted'])
    
    def _create_sidebar(self):
        """Create sidebar"""
        self.sidebar = Sidebar(self, on_navigate=self.show_page)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
    
    def _create_main_area(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=(0, 10))
    
    def _create_pages(self):
        """Create all pages"""
        self.pages = {}
        
        # Download page
        self.pages["download"] = DownloadPage(
            self.main_frame,
            on_download=self.handle_download
        )
        
        # Convert page
        self.pages["convert"] = ConvertPage(
            self.main_frame,
            on_convert=self.handle_convert
        )
        
        # Verify page
        self.pages["verify"] = VerifyPage(
            self.main_frame,
            on_verify=self.handle_verify
        )
        
        # Settings page
        self.pages["settings"] = SettingsPage(
            self.main_frame,
            on_check_deps=self.check_dependencies,
            on_theme_change=self.change_theme
        )
    
    def show_page(self, page_id):
        """Show a specific page"""
        # Hide all pages
        for page in self.pages.values():
            page.grid_forget()
        
        # Show selected page
        if page_id in self.pages:
            self.pages[page_id].grid(row=0, column=0, sticky="nsew")
        
        # Update sidebar
        self.sidebar.set_active(page_id)
        
        # Update status
        self.status_bar.set_status(f"Page: {page_id.capitalize()}")
    
    def log(self, page_id, message):
        """Log message to a page and file"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}"
        
        # Log to UI
        if page_id in self.pages and hasattr(self.pages[page_id], 'log'):
            self.pages[page_id].log(full_message)
        
        # Log to file
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d')} {full_message}\n")
        except:
            pass
    
    # Helper methods for thread-safe updates
    def _update_downloaded_stat(self):
        try:
            self.sidebar.stats["downloaded"] += 1
            self.sidebar.stat_labels["downloaded"].configure(text=str(self.sidebar.stats["downloaded"]))
        except Exception as e:
            print(f"Error updating downloaded: {e}")
    
    def _update_converted_stat(self):
        try:
            self.sidebar.stats["converted"] += 1
            self.sidebar.stat_labels["converted"].configure(text=str(self.sidebar.stats["converted"]))
        except Exception as e:
            print(f"Error updating converted: {e}")
    
    def _update_error_stat(self):
        try:
            self.sidebar.stats["errors"] += 1
            self.sidebar.stat_labels["errors"].configure(text=str(self.sidebar.stats["errors"]))
        except Exception as e:
            print(f"Error updating errors: {e}")
    
    # Handlers
    def handle_download(self, url, output, auto_convert):
        """Handle download request"""
        if not url:
            messagebox.showerror("Error", "Please enter a Spotify URL")
            return
        
        page = self.pages["download"]
        page.set_downloading(True)
        self.status_bar.set_status("Downloading...", COLORS['spotify_green'])
        self.log("download", f"Starting download: {url}")
        
        def download_thread():
            try:
                cmd = [sys.executable, "-m", "spotdl", url, "--output", output]
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, encoding='utf-8', errors='ignore'
                )
                
                total_songs = 0
                downloaded_songs = 0
                
                for line in process.stdout:
                    line_stripped = line.strip()
                    self.after(0, lambda l=line_stripped: self.log("download", l))
                    
                    # Detect total songs (e.g., "Found 12 songs in playlist")
                    if "Found" in line and "songs" in line.lower():
                        try:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "Found" and i + 1 < len(parts):
                                    total_songs = int(parts[i + 1])
                                    self.after(0, lambda t=total_songs: self.status_bar.set_status(
                                        f"Downloading 0/{t} songs...", COLORS['spotify_green']))
                                    break
                        except:
                            pass
                    
                    # Detect downloaded/skipped song (spotdl uses "Downloaded" and "Skipping")
                    if "Downloaded" in line_stripped or "Skipping" in line_stripped:
                        downloaded_songs += 1
                        self.after(0, self._update_downloaded_stat)
                        
                        if total_songs > 0:
                            progress = downloaded_songs / total_songs
                            self.after(0, lambda p=progress: page.progress.set(p))
                            self.after(0, lambda d=downloaded_songs, t=total_songs: 
                                self.status_bar.set_status(f"Downloading {d}/{t} songs...", COLORS['spotify_green']))
                    
                    # Detect errors
                    if "error" in line.lower() or "failed" in line.lower():
                        self.after(0, self._update_error_stat)
                
                process.wait()
                
                if process.returncode == 0:
                    self.after(0, lambda: self.log("download", "[OK] Download complete!"))
                    self.after(0, lambda: page.progress.set(1))
                    self.after(0, lambda d=downloaded_songs: self.status_bar.set_status(
                        f"Download complete! ({d} songs)", COLORS['success']))
                    
                    if auto_convert:
                        self.after(0, lambda: self.log("download", "Starting auto-conversion..."))
                        self._convert_folder_sync(output)
                else:
                    self.after(0, lambda: self.log("download", "[X] Download failed"))
                    self.after(0, self._update_error_stat)
                    
            except Exception as e:
                self.after(0, lambda: self.log("download", f"Error: {str(e)}"))
                self.after(0, lambda: self.sidebar.update_stat("errors"))
            finally:
                self.after(0, lambda: page.set_downloading(False))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def handle_convert(self, input_path, mode):
        """Handle convert request"""
        if not input_path:
            messagebox.showerror("Error", "Please select input file or folder")
            return
        
        page = self.pages["convert"]
        page.set_converting(True)
        self.status_bar.set_status("Converting to 432Hz...", COLORS['purple'])
        
        def convert_thread():
            try:
                # Use -u for unbuffered output
                cmd = [sys.executable, "-u", "convertir_432hz_v2.py", input_path]
                
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, encoding='utf-8', errors='ignore'
                )
                
                total_files = 0
                converted_files = 0
                skipped_files = 0
                
                for line in process.stdout:
                    line_stripped = line.strip()
                    self.after(0, lambda l=line_stripped: self.log("convert", l))
                    
                    # Detect total files
                    if "Files:" in line:
                        try:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "Files:":
                                    total_files = int(parts[i + 1])
                                    break
                        except:
                            pass
                    
                    # Detect converted file
                    if "[OK]" in line:
                        converted_files += 1
                        self.after(0, self._update_converted_stat)
                        
                        if total_files > 0:
                            progress = (converted_files + skipped_files) / total_files
                            msg = f"Converting {converted_files}/{total_files}..."
                            self.after(0, lambda p=progress: page.progress.set(p))
                            self.after(0, lambda m=msg: self.status_bar.set_status(m, COLORS['purple']))
                    
                    # Detect skipped file
                    if "[SKIP]" in line:
                        skipped_files += 1
                        if total_files > 0:
                            progress = (converted_files + skipped_files) / total_files
                            self.after(0, lambda p=progress: page.progress.set(p))
                    
                    # Detect errors
                    if "[X]" in line or "error" in line.lower():
                        self.after(0, self._update_error_stat)
                
                process.wait()
                final_msg = f"Conversion complete! ({converted_files} converted, {skipped_files} skipped)"
                self.after(0, lambda: self.log("convert", "[OK] Conversion complete!"))
                self.after(0, lambda: page.progress.set(1))
                self.after(0, lambda m=final_msg: self.status_bar.set_status(m, COLORS['success']))
                
            except Exception as e:
                self.after(0, lambda e=e: self.log("convert", f"Error: {str(e)}"))
                self.after(0, self._update_error_stat)
            finally:
                self.after(0, lambda: page.set_converting(False))
        
        threading.Thread(target=convert_thread, daemon=True).start()
    
    def _convert_folder_sync(self, folder):
        """Convert folder (sync, for auto-convert)"""
        try:
            self.after(0, lambda: self.log("download", f"[AUTO] Starting conversion of: {folder}"))
            
            # Use -u for unbuffered output
            cmd = [sys.executable, "-u", "convertir_432hz_v2.py", folder]
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding='utf-8', errors='replace', bufsize=1
            )
            
            total_files = 0
            converted_files = 0
            skipped_files = 0
            page = self.pages["download"]
            
            def update_progress(p):
                page.progress.set(p)
            
            def update_status(msg, color):
                self.status_bar.set_status(msg, color)
            
            # Read stdout
            for line in process.stdout:
                line_stripped = line.strip()
                if line_stripped:
                    self.after(0, lambda l=line_stripped: self.log("download", l))
                
                # Detect total files
                if "Files:" in line:
                    try:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "Files:":
                                total_files = int(parts[i + 1])
                                msg = f"Auto-converting 0/{total_files} files..."
                                self.after(0, lambda m=msg: update_status(m, COLORS['purple']))
                                break
                    except:
                        pass
                
                # Detect converted file (check for [OK])
                if "[OK]" in line:
                    converted_files += 1
                    self.after(0, self._update_converted_stat)
                    
                    if total_files > 0:
                        progress = (converted_files + skipped_files) / total_files
                        msg = f"Auto-converting {converted_files}/{total_files}..."
                        self.after(0, lambda p=progress: update_progress(p))
                        self.after(0, lambda m=msg: update_status(m, COLORS['purple']))
                
                # Detect skipped file
                if "[SKIP]" in line:
                    skipped_files += 1
                    if total_files > 0:
                        progress = (converted_files + skipped_files) / total_files
                        self.after(0, lambda p=progress: update_progress(p))
            
            # Read any stderr
            stderr_output = process.stderr.read()
            if stderr_output.strip():
                self.after(0, lambda e=stderr_output: self.log("download", f"[STDERR] {e}"))
            
            process.wait()
            
            if process.returncode != 0:
                self.after(0, lambda r=process.returncode: self.log("download", f"[ERROR] Conversion exited with code: {r}"))
            
            # Final updates
            final_msg = f"Complete! Downloaded + {converted_files} converted, {skipped_files} skipped"
            self.after(0, lambda: update_progress(1))
            self.after(0, lambda c=converted_files, s=skipped_files: self.log("download", f"[OK] Auto-conversion complete! ({c} converted, {s} skipped)"))
            self.after(0, lambda m=final_msg: update_status(m, COLORS['success']))
                
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.after(0, lambda: self.log("download", f"[ERROR] Conversion exception: {str(e)}"))
            self.after(0, lambda t=tb: self.log("download", f"[TRACEBACK] {t}"))
    
    def handle_verify(self, orig, conv):
        """Handle verify request"""
        if not orig or not conv:
            messagebox.showerror("Error", "Please select both files")
            return
        
        self.status_bar.set_status("Verifying...", COLORS['success'])
        ffprobe_path = get_ffprobe_path()
        
        def verify_thread():
            try:
                def get_duration(filepath):
                    cmd = [ffprobe_path, "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", filepath]
                    result = subprocess.run(cmd, capture_output=True, text=True,
                                          encoding='utf-8', errors='ignore', shell=True)
                    try:
                        return float(result.stdout.strip())
                    except:
                        return 0
                
                orig_dur = get_duration(orig)
                conv_dur = get_duration(conv)
                
                results = f"""
  📊 VERIFICATION RESULTS
  {'═'*50}

  📄 Original (440Hz):
     {Path(orig).name}
     Duration: {orig_dur:.3f}s

  📄 Converted (432Hz):
     {Path(conv).name}
     Duration: {conv_dur:.3f}s

"""
                if orig_dur > 0 and conv_dur > 0:
                    ratio = conv_dur / orig_dur
                    results += f"""  Duration Ratio: {ratio:.6f}
  Expected: ~1.000000

"""
                    if abs(ratio - 1.0) < 0.02:
                        results += """  ✅ SUCCESS!
  • Durations match (tempo preserved)
  • Pitch should be shifted to 432Hz

  👂 To verify aurally:
  1. Play both files back-to-back
  2. The 432Hz version sounds LOWER in pitch
  3. But plays at the SAME SPEED
"""
                        self.after(0, lambda: self.status_bar.set_status("Verification: SUCCESS!", COLORS['success']))
                    else:
                        results += f"  ⚠️ Duration ratio differs from 1.0"
                        self.after(0, lambda: self.status_bar.set_status("Verification: Warning", COLORS['warning']))
                
                self.after(0, lambda: self.pages["verify"].show_results(results))
                
            except Exception as e:
                self.after(0, lambda: self.pages["verify"].show_results(f"Error: {str(e)}"))
        
        threading.Thread(target=verify_thread, daemon=True).start()
    
    def check_dependencies(self):
        """Check installed dependencies"""
        self.log("download", "Checking dependencies...")
        self.log("download", f"✓ Python {sys.version.split()[0]}")
        
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, 
                                   text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                self.log("download", "✓ FFmpeg installed")
            else:
                self.log("download", "✗ FFmpeg not found")
        except:
            self.log("download", "✗ FFmpeg not found - Install with: winget install FFmpeg")
        
        try:
            result = subprocess.run([sys.executable, "-m", "spotdl", "--version"],
                                   capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                self.log("download", f"✓ spotdl {result.stdout.strip()}")
            else:
                self.log("download", "✗ spotdl not found")
        except:
            self.log("download", "✗ spotdl not found - Install with: pip install spotdl")
    
    def change_theme(self, theme):
        """Change application theme"""
        ctk.set_appearance_mode(theme.lower())


def run():
    """Run the application"""
    app = SpotifyDLApp()
    app.mainloop()


if __name__ == "__main__":
    run()

