"""
Log output widget component
"""

import customtkinter as ctk
from ..config import COLORS, SIZES, FONTS


class LogWidget(ctk.CTkFrame):
    """Log output widget with clear button"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS['bg_card'], corner_radius=12, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._create_header()
        self._create_textbox()
    
    def _create_header(self):
        """Create header with title and clear button"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            header,
            text="📋 Output Log",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_muted']
        ).pack(side="left")
        
        ctk.CTkButton(
            header,
            text="Clear",
            width=60,
            height=25,
            corner_radius=6,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            font=ctk.CTkFont(size=11),
            command=self.clear
        ).pack(side="right")
    
    def _create_textbox(self):
        """Create log textbox"""
        self.textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=COLORS['bg_dark'],
            corner_radius=8
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
    
    def log(self, message):
        """Add message to log"""
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")
    
    def clear(self):
        """Clear log contents"""
        self.textbox.delete("1.0", "end")

