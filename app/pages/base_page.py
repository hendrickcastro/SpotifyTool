"""
Base page class
"""

import customtkinter as ctk
from tkinter import filedialog
from ..constants import COLORS


class BasePage(ctk.CTkFrame):
    """Base class for all pages"""
    
    def __init__(self, master, title, subtitle, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header(title, subtitle)
    
    def _create_header(self, title, subtitle):
        """Create page header"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_muted']
        ).pack(anchor="w", pady=(5, 0))
    
    def browse_folder(self, entry):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, "end")
            entry.insert(0, folder)
    
    def browse_file(self, entry, filetypes=None):
        """Open file browser dialog"""
        if filetypes is None:
            filetypes = [("MP3 files", "*.mp3"), ("All files", "*.*")]
        file = filedialog.askopenfilename(filetypes=filetypes)
        if file:
            entry.delete(0, "end")
            entry.insert(0, file)

