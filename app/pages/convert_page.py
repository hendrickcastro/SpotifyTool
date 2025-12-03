"""
Convert to 432Hz page
"""

import customtkinter as ctk
from .base_page import BasePage
from ..constants import COLORS
from ..components.log_widget import LogWidget


class ConvertPage(BasePage):
    """432Hz conversion page"""
    
    def __init__(self, master, on_convert, **kwargs):
        super().__init__(
            master, 
            title="Convert to 432Hz",
            subtitle="Transform your music to the natural frequency",
            **kwargs
        )
        self.on_convert = on_convert
        self.grid_rowconfigure(2, weight=1)
        
        self._create_card()
        self._create_log()
    
    def _create_card(self):
        """Create main card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        card.grid_columnconfigure(0, weight=1)
        
        # Mode selection
        mode_frame = ctk.CTkFrame(card, fg_color="transparent")
        mode_frame.grid(row=0, column=0, padx=25, pady=25, sticky="ew")
        
        ctk.CTkLabel(
            mode_frame,
            text="Conversion Mode",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 12))
        
        self.convert_mode = ctk.StringVar(value="folder")
        
        modes_container = ctk.CTkFrame(mode_frame, fg_color="transparent")
        modes_container.pack(fill="x")
        
        for value, text, icon in [("file", "Single File", "📄"), ("folder", "Entire Folder", "📁")]:
            ctk.CTkRadioButton(
                modes_container,
                text=f"{icon}  {text}",
                variable=self.convert_mode,
                value=value,
                font=ctk.CTkFont(size=13),
                command=self._update_mode
            ).pack(side="left", padx=(0, 30))
        
        # Input
        ctk.CTkLabel(
            card,
            text="Input",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=1, column=0, padx=25, pady=(0, 8), sticky="w")
        
        input_frame = ctk.CTkFrame(card, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=25, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Select folder with MP3 files...",
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.input_entry.grid(row=0, column=0, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            input_frame,
            text="📁",
            width=50,
            height=50,
            corner_radius=10,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            command=self._browse_input
        )
        self.browse_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Info box
        info_frame = ctk.CTkFrame(card, fg_color=COLORS['bg_dark'], corner_radius=12)
        info_frame.grid(row=3, column=0, padx=25, pady=20, sticky="ew")
        
        info_text = """🎚️  432Hz is known as the "natural frequency"
✨  High-quality Rubberband pitch shifting
⏱️  Same tempo, lower pitch (~31 cents)
🎵  Output: VBR highest quality MP3"""
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            text_color=COLORS['text_muted']
        ).pack(padx=20, pady=15, anchor="w")
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            card,
            text="🎚️  Convert to 432Hz",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=COLORS['purple'],
            hover_color=COLORS['purple_hover'],
            command=self._start_convert
        )
        self.convert_btn.grid(row=4, column=0, padx=25, pady=(0, 15), sticky="ew")
        
        # Progress
        self.progress = ctk.CTkProgressBar(
            card, 
            height=6, 
            corner_radius=3,
            progress_color=COLORS['purple']
        )
        self.progress.grid(row=5, column=0, padx=25, pady=(0, 25), sticky="ew")
        self.progress.set(0)
    
    def _create_log(self):
        """Create log widget"""
        self.log_widget = LogWidget(self)
        self.log_widget.grid(row=2, column=0, sticky="nsew")
    
    def _update_mode(self):
        """Update UI based on mode selection"""
        if self.convert_mode.get() == "file":
            self.input_entry.configure(placeholder_text="Select MP3 file...")
        else:
            self.input_entry.configure(placeholder_text="Select folder with MP3 files...")
    
    def _browse_input(self):
        """Browse for input based on mode"""
        if self.convert_mode.get() == "file":
            self.browse_file(self.input_entry)
        else:
            self.browse_folder(self.input_entry)
    
    def _start_convert(self):
        """Handle convert button click"""
        input_path = self.input_entry.get().strip()
        mode = self.convert_mode.get()
        
        if self.on_convert:
            self.on_convert(input_path, mode)
    
    def set_converting(self, is_converting):
        """Update UI for convert state"""
        if is_converting:
            self.convert_btn.configure(state="disabled", text="Converting...")
            self.progress.set(0)
        else:
            self.convert_btn.configure(state="normal", text="🎚️  Convert to 432Hz")
            self.progress.set(1)
    
    def log(self, message):
        """Add message to log"""
        self.log_widget.log(message)

