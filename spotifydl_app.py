"""
SpotifyDL - Desktop Application
Download from Spotify + Convert to 432Hz
Cross-platform GUI using CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import subprocess
import sys
import os
from pathlib import Path
import queue

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SpotifyDLApp(ctk.CTk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("🎵 SpotifyDL - Music Downloader & 432Hz Converter")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Queue for thread communication
        self.log_queue = queue.Queue()
        
        # Create UI
        self.create_ui()
        
        # Start log checker
        self.check_log_queue()
    
    def create_ui(self):
        """Create the main UI"""
        
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        
        # Add tabs
        self.tab_download = self.tabview.add("📥 Download")
        self.tab_convert = self.tabview.add("🎚️ Convert 432Hz")
        self.tab_verify = self.tabview.add("✓ Verify")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        # Create tab contents
        self.create_download_tab()
        self.create_convert_tab()
        self.create_verify_tab()
        self.create_settings_tab()
        
        # Log area
        self.create_log_area()
    
    def create_header(self):
        """Create header with title"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title = ctk.CTkLabel(
            header_frame,
            text="🎵 SpotifyDL",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Download from Spotify & Convert to 432Hz",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(side="left", padx=(20, 0))
    
    def create_download_tab(self):
        """Create download tab content"""
        tab = self.tab_download
        tab.grid_columnconfigure(0, weight=1)
        
        # URL Input
        url_frame = ctk.CTkFrame(tab)
        url_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        url_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(url_frame, text="Spotify URL:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://open.spotify.com/playlist/... or album/track URL",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Output folder
        output_frame = ctk.CTkFrame(tab)
        output_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(output_frame, text="Output Folder:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.download_output_entry = ctk.CTkEntry(
            output_frame,
            placeholder_text="./downloads",
            height=40
        )
        self.download_output_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.download_output_entry.insert(0, "./downloads")
        
        browse_btn = ctk.CTkButton(
            output_frame,
            text="Browse",
            width=100,
            command=lambda: self.browse_folder(self.download_output_entry)
        )
        browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Options
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.auto_convert_var = ctk.BooleanVar(value=False)
        auto_convert_cb = ctk.CTkCheckBox(
            options_frame,
            text="Auto-convert to 432Hz after download",
            variable=self.auto_convert_var
        )
        auto_convert_cb.pack(padx=20, pady=15)
        
        # Download button
        self.download_btn = ctk.CTkButton(
            tab,
            text="⬇️ Download",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_download
        )
        self.download_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Progress
        self.download_progress = ctk.CTkProgressBar(tab)
        self.download_progress.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.download_progress.set(0)
    
    def create_convert_tab(self):
        """Create convert tab content"""
        tab = self.tab_convert
        tab.grid_columnconfigure(0, weight=1)
        
        # Mode selection
        mode_frame = ctk.CTkFrame(tab)
        mode_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(
            mode_frame,
            text="Conversion Mode:",
            font=ctk.CTkFont(size=14)
        ).pack(padx=20, pady=(15, 5), anchor="w")
        
        self.convert_mode = ctk.StringVar(value="file")
        
        mode_container = ctk.CTkFrame(mode_frame, fg_color="transparent")
        mode_container.pack(padx=20, pady=(0, 15), fill="x")
        
        ctk.CTkRadioButton(
            mode_container,
            text="Single File",
            variable=self.convert_mode,
            value="file",
            command=self.update_convert_ui
        ).pack(side="left", padx=(0, 30))
        
        ctk.CTkRadioButton(
            mode_container,
            text="Entire Folder",
            variable=self.convert_mode,
            value="folder",
            command=self.update_convert_ui
        ).pack(side="left")
        
        # Input selection
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        self.convert_input_label = ctk.CTkLabel(
            input_frame,
            text="Input File:",
            font=ctk.CTkFont(size=14)
        )
        self.convert_input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.convert_input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Select MP3 file...",
            height=40
        )
        self.convert_input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.convert_browse_btn = ctk.CTkButton(
            input_frame,
            text="Browse",
            width=100,
            command=self.browse_convert_input
        )
        self.convert_browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Output folder
        output_frame = ctk.CTkFrame(tab)
        output_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(output_frame, text="Output Folder:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.convert_output_entry = ctk.CTkEntry(
            output_frame,
            placeholder_text="Leave empty for auto (creates /432hz subfolder)",
            height=40
        )
        self.convert_output_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        browse_out_btn = ctk.CTkButton(
            output_frame,
            text="Browse",
            width=100,
            command=lambda: self.browse_folder(self.convert_output_entry)
        )
        browse_out_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Info
        info_frame = ctk.CTkFrame(tab, fg_color=("gray90", "gray20"))
        info_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        info_text = """🎚️ 432Hz Conversion Info:
        
• Converts music from standard 440Hz tuning to 432Hz
• Uses high-quality Rubberband pitch shifting
• Preserves tempo (same speed, lower pitch)
• Output quality: VBR highest quality MP3"""
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            justify="left",
            font=ctk.CTkFont(size=12)
        ).pack(padx=20, pady=15, anchor="w")
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            tab,
            text="🎚️ Convert to 432Hz",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.start_conversion
        )
        self.convert_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        # Progress
        self.convert_progress = ctk.CTkProgressBar(tab, progress_color="#8B5CF6")
        self.convert_progress.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.convert_progress.set(0)
    
    def create_verify_tab(self):
        """Create verify tab content"""
        tab = self.tab_verify
        tab.grid_columnconfigure(0, weight=1)
        
        # Original file
        orig_frame = ctk.CTkFrame(tab)
        orig_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        orig_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            orig_frame,
            text="Original (440Hz):",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.verify_orig_entry = ctk.CTkEntry(orig_frame, height=40)
        self.verify_orig_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            orig_frame,
            text="Browse",
            width=100,
            command=lambda: self.browse_file(self.verify_orig_entry)
        ).grid(row=0, column=2, padx=10, pady=10)
        
        # Converted file
        conv_frame = ctk.CTkFrame(tab)
        conv_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        conv_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            conv_frame,
            text="Converted (432Hz):",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.verify_conv_entry = ctk.CTkEntry(conv_frame, height=40)
        self.verify_conv_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            conv_frame,
            text="Browse",
            width=100,
            command=lambda: self.browse_file(self.verify_conv_entry)
        ).grid(row=0, column=2, padx=10, pady=10)
        
        # Verify button
        ctk.CTkButton(
            tab,
            text="✓ Verify Conversion",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#10B981",
            hover_color="#059669",
            command=self.verify_files
        ).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Results
        self.verify_results = ctk.CTkTextbox(tab, height=200, font=ctk.CTkFont(size=12))
        self.verify_results.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        tab.grid_rowconfigure(3, weight=1)
    
    def create_settings_tab(self):
        """Create settings tab content"""
        tab = self.tab_settings
        tab.grid_columnconfigure(0, weight=1)
        
        # Appearance
        appear_frame = ctk.CTkFrame(tab)
        appear_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(
            appear_frame,
            text="Appearance",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        theme_container = ctk.CTkFrame(appear_frame, fg_color="transparent")
        theme_container.pack(padx=20, pady=(0, 15), fill="x")
        
        ctk.CTkLabel(theme_container, text="Theme:").pack(side="left")
        
        theme_menu = ctk.CTkOptionMenu(
            theme_container,
            values=["Dark", "Light", "System"],
            command=self.change_theme
        )
        theme_menu.pack(side="left", padx=(10, 0))
        theme_menu.set("Dark")
        
        # Dependencies
        deps_frame = ctk.CTkFrame(tab)
        deps_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(
            deps_frame,
            text="Dependencies",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(15, 10), anchor="w")
        
        ctk.CTkButton(
            deps_frame,
            text="Check Dependencies",
            command=self.check_dependencies
        ).pack(padx=20, pady=(0, 15))
        
        # About
        about_frame = ctk.CTkFrame(tab)
        about_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        about_text = """SpotifyDL - Music Downloader & 432Hz Converter

Features:
• Download playlists, albums, and tracks from Spotify
• Convert music to 432Hz tuning
• High-quality audio processing
• Cross-platform (Windows, Mac, Linux)

Built with Python, CustomTkinter, spotdl, and FFmpeg"""
        
        ctk.CTkLabel(
            about_frame,
            text=about_text,
            justify="left",
            font=ctk.CTkFont(size=12)
        ).pack(padx=20, pady=20, anchor="w")
    
    def create_log_area(self):
        """Create log output area"""
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        log_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            log_frame,
            text="📋 Log",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        clear_btn = ctk.CTkButton(
            log_frame,
            text="Clear",
            width=60,
            height=25,
            command=self.clear_log
        )
        clear_btn.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        
        self.log_text = ctk.CTkTextbox(log_frame, height=120, font=ctk.CTkFont(size=11))
        self.log_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
    # Helper methods
    def browse_folder(self, entry):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, "end")
            entry.insert(0, folder)
    
    def browse_file(self, entry):
        """Open file browser dialog"""
        file = filedialog.askopenfilename(
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if file:
            entry.delete(0, "end")
            entry.insert(0, file)
    
    def browse_convert_input(self):
        """Browse for convert input based on mode"""
        if self.convert_mode.get() == "file":
            self.browse_file(self.convert_input_entry)
        else:
            self.browse_folder(self.convert_input_entry)
    
    def update_convert_ui(self):
        """Update convert UI based on mode"""
        if self.convert_mode.get() == "file":
            self.convert_input_label.configure(text="Input File:")
            self.convert_input_entry.configure(placeholder_text="Select MP3 file...")
        else:
            self.convert_input_label.configure(text="Input Folder:")
            self.convert_input_entry.configure(placeholder_text="Select folder with MP3s...")
    
    def log(self, message):
        """Add message to log"""
        self.log_queue.put(message)
    
    def check_log_queue(self):
        """Check for log messages from threads"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert("end", message + "\n")
                self.log_text.see("end")
        except queue.Empty:
            pass
        self.after(100, self.check_log_queue)
    
    def clear_log(self):
        """Clear log text"""
        self.log_text.delete("1.0", "end")
    
    def change_theme(self, theme):
        """Change app theme"""
        ctk.set_appearance_mode(theme.lower())
    
    # Action methods
    def start_download(self):
        """Start Spotify download"""
        url = self.url_entry.get().strip()
        output = self.download_output_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a Spotify URL")
            return
        
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.download_progress.set(0)
        self.log(f"Starting download: {url}")
        
        def download_thread():
            try:
                cmd = [sys.executable, "-m", "spotdl", url, "--output", output]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log(line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log("✓ Download complete!")
                    if self.auto_convert_var.get():
                        self.log("Starting auto-conversion to 432Hz...")
                        self.convert_folder_sync(output)
                else:
                    self.log("✗ Download failed")
                    
            except Exception as e:
                self.log(f"Error: {str(e)}")
            finally:
                self.after(0, lambda: self.download_btn.configure(
                    state="normal", text="⬇️ Download"
                ))
                self.after(0, lambda: self.download_progress.set(1))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def start_conversion(self):
        """Start 432Hz conversion"""
        input_path = self.convert_input_entry.get().strip()
        output_path = self.convert_output_entry.get().strip() or None
        
        if not input_path:
            messagebox.showerror("Error", "Please select input file or folder")
            return
        
        self.convert_btn.configure(state="disabled", text="Converting...")
        self.convert_progress.set(0)
        
        def convert_thread():
            try:
                if self.convert_mode.get() == "file":
                    self.log(f"Converting: {Path(input_path).name}")
                    cmd = [sys.executable, "convertir_432hz_v2.py", input_path]
                else:
                    self.log(f"Converting folder: {input_path}")
                    cmd = [sys.executable, "convertir_432hz_v2.py", input_path]
                    if output_path:
                        cmd.append(output_path)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log(line.strip())
                
                process.wait()
                self.log("✓ Conversion complete!")
                
            except Exception as e:
                self.log(f"Error: {str(e)}")
            finally:
                self.after(0, lambda: self.convert_btn.configure(
                    state="normal", text="🎚️ Convert to 432Hz"
                ))
                self.after(0, lambda: self.convert_progress.set(1))
        
        threading.Thread(target=convert_thread, daemon=True).start()
    
    def convert_folder_sync(self, folder):
        """Convert folder (called from download thread)"""
        try:
            cmd = [sys.executable, "convertir_432hz_v2.py", folder]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in process.stdout:
                self.log(line.strip())
            process.wait()
            self.log("✓ Auto-conversion complete!")
        except Exception as e:
            self.log(f"Conversion error: {str(e)}")
    
    def verify_files(self):
        """Verify conversion by comparing files"""
        orig = self.verify_orig_entry.get().strip()
        conv = self.verify_conv_entry.get().strip()
        
        if not orig or not conv:
            messagebox.showerror("Error", "Please select both files")
            return
        
        self.verify_results.delete("1.0", "end")
        
        def verify_thread():
            try:
                # Get durations
                def get_duration(filepath):
                    cmd = [
                        "ffprobe", "-v", "error",
                        "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1",
                        filepath
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    try:
                        return float(result.stdout.strip())
                    except:
                        return 0
                
                orig_dur = get_duration(orig)
                conv_dur = get_duration(conv)
                
                results = f"""📊 VERIFICATION RESULTS
{'='*50}

📄 Original (440Hz):
   {Path(orig).name}
   Duration: {orig_dur:.3f}s

📄 Converted (432Hz):
   {Path(conv).name}
   Duration: {conv_dur:.3f}s

"""
                
                if orig_dur > 0 and conv_dur > 0:
                    ratio = conv_dur / orig_dur
                    results += f"""Duration Ratio: {ratio:.6f}
Expected: ~1.000000 (same duration)

"""
                    if abs(ratio - 1.0) < 0.02:
                        results += """✅ SUCCESS!
• Durations match (tempo preserved)
• Pitch should be shifted to 432Hz

👂 To verify aurally:
1. Play both files back-to-back
2. The 432Hz version sounds LOWER in pitch
3. But plays at the SAME SPEED

📱 Use a phone tuner app:
• 440Hz: notes show normal (A=A)
• 432Hz: notes show ~31 cents flat (A=-31¢)
"""
                    else:
                        results += f"⚠️ Duration ratio differs from 1.0"
                else:
                    results += "❌ Could not read file durations"
                
                self.after(0, lambda: self.verify_results.insert("1.0", results))
                
            except Exception as e:
                self.after(0, lambda: self.verify_results.insert("1.0", f"Error: {str(e)}"))
        
        threading.Thread(target=verify_thread, daemon=True).start()
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        self.log("Checking dependencies...")
        
        # Python
        self.log(f"✓ Python {sys.version.split()[0]}")
        
        # FFmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.log(f"✓ {version}")
            else:
                self.log("✗ FFmpeg not found")
        except:
            self.log("✗ FFmpeg not found - Install with: winget install FFmpeg")
        
        # spotdl
        try:
            result = subprocess.run(
                [sys.executable, "-m", "spotdl", "--version"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.log(f"✓ spotdl {result.stdout.strip()}")
            else:
                self.log("✗ spotdl not found")
        except:
            self.log("✗ spotdl not found - Install with: pip install spotdl")


def main():
    """Main entry point"""
    app = SpotifyDLApp()
    app.mainloop()


if __name__ == "__main__":
    main()

