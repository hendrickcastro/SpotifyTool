"""
Sidebar navigation component
"""

import customtkinter as ctk
from ..config import COLORS, APP_NAME, NAV_ITEMS, SIZES, FONTS


class Sidebar(ctk.CTkFrame):
    """Sidebar with navigation and stats"""
    
    def __init__(self, master, on_navigate, **kwargs):
        super().__init__(master, width=220, corner_radius=0, fg_color=COLORS['bg_card'], **kwargs)
        self.grid_propagate(False)
        
        self.on_navigate = on_navigate
        self.nav_buttons = {}
        self.stat_labels = {}
        self.stats = {"downloaded": 0, "converted": 0, "errors": 0}
        
        self._create_logo()
        self._create_separator()
        self._create_navigation()
        self._create_stats()
    
    def _create_logo(self):
        """Create logo section"""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(30, 10))
        
        ctk.CTkLabel(
            logo_frame,
            text="🎵",
            font=ctk.CTkFont(size=40)
        ).pack(side="left")
        
        title_container = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_container.pack(side="left", padx=(10, 0))
        
        ctk.CTkLabel(
            title_container,
            text=APP_NAME,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['spotify_green']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_container,
            text="Music Downloader",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted']
        ).pack(anchor="w")
    
    def _create_separator(self):
        """Create separator line"""
        ctk.CTkFrame(self, height=1, fg_color=COLORS['border']).pack(fill="x", padx=20, pady=20)
    
    def _create_navigation(self):
        """Create navigation buttons"""
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)
        
        nav_items = [
            ("download", "📥  Download", COLORS['spotify_green']),
            ("convert", "🎚️  Convert 432Hz", COLORS['purple']),
            ("verify", "✓  Verify", COLORS['success']),
            ("settings", "⚙️  Settings", COLORS['text_muted']),
        ]
        
        for page_id, text, color in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                font=ctk.CTkFont(size=14),
                height=45,
                anchor="w",
                fg_color="transparent",
                text_color="white",
                hover_color=COLORS['bg_card_hover'],
                command=lambda p=page_id: self._handle_nav(p)
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[page_id] = btn
    
    def _create_stats(self):
        """Create stats section at bottom"""
        stats_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'], corner_radius=12)
        stats_frame.pack(fill="x", padx=15, pady=20, side="bottom")
        
        ctk.CTkLabel(
            stats_frame,
            text="Session Stats",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_muted']
        ).pack(padx=15, pady=(15, 10), anchor="w")
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        for key, icon, label in [
            ("downloaded", "📥", "Downloaded"),
            ("converted", "🎚️", "Converted"),
            ("errors", "❌", "Errors")
        ]:
            row = ctk.CTkFrame(stats_grid, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row, 
                text=f"{icon} {label}:", 
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_muted']
            ).pack(side="left")
            
            self.stat_labels[key] = ctk.CTkLabel(
                row, 
                text="0", 
                font=ctk.CTkFont(size=11, weight="bold")
            )
            self.stat_labels[key].pack(side="right")
    
    def _handle_nav(self, page_id):
        """Handle navigation click"""
        self.set_active(page_id)
        if self.on_navigate:
            self.on_navigate(page_id)
    
    def set_active(self, page_id):
        """Set active navigation button"""
        for pid, btn in self.nav_buttons.items():
            if pid == page_id:
                btn.configure(fg_color=COLORS['bg_card_hover'])
            else:
                btn.configure(fg_color="transparent")
    
    def update_stat(self, key, increment=1):
        """Update a stat value"""
        self.stats[key] += increment
        self.stat_labels[key].configure(text=str(self.stats[key]))

