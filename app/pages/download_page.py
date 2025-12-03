"""
Download page
"""

import customtkinter as ctk
from .base_page import BasePage
from ..config import COLORS, SIZES, DOWNLOAD
from ..components.log_widget import LogWidget


class DownloadPage(BasePage):
    """Spotify download page"""
    
    def __init__(self, master, on_download, **kwargs):
        super().__init__(
            master, 
            title="Download from Spotify",
            subtitle="Paste a Spotify URL to download playlists, albums, or tracks",
            **kwargs
        )
        self.on_download = on_download
        self.grid_rowconfigure(2, weight=1)
        
        self._create_card()
        self._create_log()
    
    def _create_card(self):
        """Create main input card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        card.grid_columnconfigure(0, weight=1)
        
        # URL Input
        ctk.CTkLabel(
            card,
            text="Spotify URL",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=25, pady=(25, 8), sticky="w")
        
        self.url_entry = ctk.CTkEntry(
            card,
            placeholder_text="https://open.spotify.com/playlist/...",
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.url_entry.grid(row=1, column=0, padx=25, sticky="ew")
        
        # Output folder
        ctk.CTkLabel(
            card,
            text="Output Folder",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=2, column=0, padx=25, pady=(20, 8), sticky="w")
        
        folder_frame = ctk.CTkFrame(card, fg_color="transparent")
        folder_frame.grid(row=3, column=0, padx=25, sticky="ew")
        folder_frame.grid_columnconfigure(0, weight=1)
        
        self.output_entry = ctk.CTkEntry(
            folder_frame,
            placeholder_text="./downloads",
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.output_entry.grid(row=0, column=0, sticky="ew")
        self.output_entry.insert(0, "./downloads")
        
        ctk.CTkButton(
            folder_frame,
            text="📁",
            width=50,
            height=50,
            corner_radius=10,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            command=lambda: self.browse_folder(self.output_entry)
        ).grid(row=0, column=1, padx=(10, 0))
        
        # Options
        options_frame = ctk.CTkFrame(card, fg_color=COLORS['bg_dark'], corner_radius=10)
        options_frame.grid(row=4, column=0, padx=25, pady=20, sticky="ew")
        
        self.auto_convert_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Auto-convert to 432Hz after download",
            variable=self.auto_convert_var,
            font=ctk.CTkFont(size=13),
            checkbox_height=22,
            checkbox_width=22,
            corner_radius=6
        ).pack(padx=20, pady=15)
        
        # Download button
        self.download_btn = ctk.CTkButton(
            card,
            text="⬇️  Download",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=COLORS['spotify_green'],
            hover_color=COLORS['spotify_green_hover'],
            command=self._start_download
        )
        self.download_btn.grid(row=5, column=0, padx=25, pady=(0, 15), sticky="ew")
        
        # Progress
        self.progress = ctk.CTkProgressBar(
            card, 
            height=6, 
            corner_radius=3,
            progress_color=COLORS['spotify_green']
        )
        self.progress.grid(row=6, column=0, padx=25, pady=(0, 25), sticky="ew")
        self.progress.set(0)
    
    def _create_log(self):
        """Create log widget"""
        self.log_widget = LogWidget(self)
        self.log_widget.grid(row=2, column=0, sticky="nsew")
    
    def _start_download(self):
        """Handle download button click"""
        url = self.url_entry.get().strip()
        output = self.output_entry.get().strip()
        auto_convert = self.auto_convert_var.get()
        
        if self.on_download:
            self.on_download(url, output, auto_convert)
    
    def set_downloading(self, is_downloading):
        """Update UI for download state"""
        if is_downloading:
            self.download_btn.configure(state="disabled", text="Downloading...")
            self.progress.set(0)
        else:
            self.download_btn.configure(state="normal", text="⬇️  Download")
            self.progress.set(1)
    
    def log(self, message):
        """Add message to log"""
        self.log_widget.log(message)

