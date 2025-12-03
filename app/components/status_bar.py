"""
Status bar component
"""

import customtkinter as ctk
from ..constants import COLORS, APP_VERSION


class StatusBar(ctk.CTkFrame):
    """Status bar at bottom of window"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, fg_color=COLORS['bg_card'], **kwargs)
        self.grid_columnconfigure(1, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self, 
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted']
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.version_label = ctk.CTkLabel(
            self,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted']
        )
        self.version_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
    
    def set_status(self, text, color=None):
        """Update status text"""
        self.status_label.configure(text=text)
        if color:
            self.status_label.configure(text_color=color)
        else:
            self.status_label.configure(text_color=COLORS['text_muted'])

