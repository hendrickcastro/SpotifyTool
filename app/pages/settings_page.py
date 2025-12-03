"""
Settings page
"""

import customtkinter as ctk
from tkinter import messagebox
from .base_page import BasePage
from ..constants import COLORS, APP_VERSION
from ..utils.config_manager import config_manager


class SettingsPage(BasePage):
    """Settings page"""
    
    def __init__(self, master, on_check_deps, on_theme_change, **kwargs):
        super().__init__(
            master, 
            title="Settings",
            subtitle="Configure application preferences",
            **kwargs
        )
        self.on_check_deps = on_check_deps
        self.on_theme_change = on_theme_change
        
        self._create_credentials_card()
        self._create_appearance_card()
        self._create_deps_card()
        self._create_about_card()
        
        # Load saved credentials
        self._load_credentials()
    
    def _create_credentials_card(self):
        """Create Spotify credentials card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        card.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="🔑  Spotify API Credentials",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right")
        
        # Help text
        ctk.CTkLabel(
            card,
            text="Get your credentials from: developer.spotify.com/dashboard",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted']
        ).grid(row=1, column=0, padx=25, pady=(0, 15), sticky="w")
        
        # Client ID
        ctk.CTkLabel(
            card,
            text="Client ID",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=2, column=0, padx=25, pady=(0, 5), sticky="w")
        
        id_frame = ctk.CTkFrame(card, fg_color="transparent")
        id_frame.grid(row=3, column=0, padx=25, sticky="ew")
        id_frame.grid_columnconfigure(0, weight=1)
        
        self.client_id_entry = ctk.CTkEntry(
            id_frame,
            placeholder_text="Enter your Spotify Client ID",
            height=40,
            corner_radius=8
        )
        self.client_id_entry.grid(row=0, column=0, sticky="ew")
        
        self.show_id_btn = ctk.CTkButton(
            id_frame,
            text="👁",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            command=lambda: self._toggle_visibility("id")
        )
        self.show_id_btn.grid(row=0, column=1, padx=(8, 0))
        
        # Client Secret
        ctk.CTkLabel(
            card,
            text="Client Secret",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=4, column=0, padx=25, pady=(15, 5), sticky="w")
        
        secret_frame = ctk.CTkFrame(card, fg_color="transparent")
        secret_frame.grid(row=5, column=0, padx=25, sticky="ew")
        secret_frame.grid_columnconfigure(0, weight=1)
        
        self.client_secret_entry = ctk.CTkEntry(
            secret_frame,
            placeholder_text="Enter your Spotify Client Secret",
            height=40,
            corner_radius=8,
            show="•"
        )
        self.client_secret_entry.grid(row=0, column=0, sticky="ew")
        
        self.show_secret_btn = ctk.CTkButton(
            secret_frame,
            text="👁",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            command=lambda: self._toggle_visibility("secret")
        )
        self.show_secret_btn.grid(row=0, column=1, padx=(8, 0))
        
        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=6, column=0, padx=25, pady=20, sticky="ew")
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾  Save Credentials",
            height=40,
            corner_radius=8,
            fg_color=COLORS['spotify_green'],
            hover_color=COLORS['spotify_green_hover'],
            command=self._save_credentials
        )
        self.save_btn.pack(side="left", padx=(0, 10))
        
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️  Clear",
            height=40,
            corner_radius=8,
            fg_color=COLORS['error'],
            hover_color="#dc2626",
            command=self._clear_credentials
        )
        self.clear_btn.pack(side="left")
        
        # Track visibility state
        self.id_visible = False
        self.secret_visible = False
        self.id_real_value = ""
        self.secret_real_value = ""
    
    def _create_appearance_card(self):
        """Create appearance settings card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(
            card,
            text="🎨  Appearance",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=25, pady=(20, 15), anchor="w")
        
        theme_row = ctk.CTkFrame(card, fg_color="transparent")
        theme_row.pack(fill="x", padx=25, pady=(0, 20))
        
        ctk.CTkLabel(theme_row, text="Theme:", font=ctk.CTkFont(size=13)).pack(side="left")
        
        theme_menu = ctk.CTkOptionMenu(
            theme_row,
            values=["Dark", "Light", "System"],
            command=self._handle_theme_change,
            width=150,
            height=35,
            corner_radius=8
        )
        theme_menu.pack(side="right")
        
        # Load saved theme
        saved_theme = config_manager.get_setting("theme", "Dark")
        theme_menu.set(saved_theme)
    
    def _create_deps_card(self):
        """Create dependencies card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(
            card,
            text="🔧  Dependencies",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=25, pady=(20, 15), anchor="w")
        
        ctk.CTkButton(
            card,
            text="Check Dependencies",
            height=40,
            corner_radius=8,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['bg_card_hover'],
            command=self._handle_check_deps
        ).pack(padx=25, pady=(0, 20), anchor="w")
    
    def _create_about_card(self):
        """Create about card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=4, column=0, sticky="ew")
        
        ctk.CTkLabel(
            card,
            text="ℹ️  About",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=25, pady=(20, 10), anchor="w")
        
        about_text = f"""SpotifyTool v{APP_VERSION}

A powerful tool to download music from Spotify and convert it to 432Hz.

• Download playlists, albums, and tracks
• High-quality 432Hz pitch conversion
• Cross-platform (Windows, Mac, Linux)

Built with Python, CustomTkinter, spotdl, and FFmpeg"""
        
        ctk.CTkLabel(
            card,
            text=about_text,
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_muted'],
            justify="left"
        ).pack(padx=25, pady=(0, 20), anchor="w")
    
    def _load_credentials(self):
        """Load saved credentials and display obfuscated"""
        client_id, client_secret = config_manager.get_credentials()
        
        if client_id:
            self.id_real_value = client_id
            self.client_id_entry.delete(0, "end")
            self.client_id_entry.insert(0, config_manager.obfuscate(client_id))
            self.client_id_entry.configure(state="disabled")
        
        if client_secret:
            self.secret_real_value = client_secret
            self.client_secret_entry.delete(0, "end")
            self.client_secret_entry.insert(0, config_manager.obfuscate(client_secret))
            self.client_secret_entry.configure(state="disabled", show="")
        
        self._update_status()
    
    def _update_status(self):
        """Update credential status indicator"""
        if config_manager.has_credentials():
            self.status_label.configure(text="✅ Configured", text_color=COLORS['success'])
        else:
            self.status_label.configure(text="⚠️ Not configured", text_color=COLORS['warning'])
    
    def _toggle_visibility(self, field: str):
        """Toggle visibility of a credential field"""
        if field == "id":
            if self.id_real_value:
                if self.id_visible:
                    # Hide
                    self.client_id_entry.configure(state="normal")
                    self.client_id_entry.delete(0, "end")
                    self.client_id_entry.insert(0, config_manager.obfuscate(self.id_real_value))
                    self.client_id_entry.configure(state="disabled")
                    self.show_id_btn.configure(text="👁")
                else:
                    # Show
                    self.client_id_entry.configure(state="normal")
                    self.client_id_entry.delete(0, "end")
                    self.client_id_entry.insert(0, self.id_real_value)
                    self.client_id_entry.configure(state="disabled")
                    self.show_id_btn.configure(text="🙈")
                self.id_visible = not self.id_visible
        
        elif field == "secret":
            if self.secret_real_value:
                if self.secret_visible:
                    # Hide
                    self.client_secret_entry.configure(state="normal")
                    self.client_secret_entry.delete(0, "end")
                    self.client_secret_entry.insert(0, config_manager.obfuscate(self.secret_real_value))
                    self.client_secret_entry.configure(state="disabled", show="")
                    self.show_secret_btn.configure(text="👁")
                else:
                    # Show
                    self.client_secret_entry.configure(state="normal")
                    self.client_secret_entry.delete(0, "end")
                    self.client_secret_entry.insert(0, self.secret_real_value)
                    self.client_secret_entry.configure(state="disabled", show="")
                    self.show_secret_btn.configure(text="🙈")
                self.secret_visible = not self.secret_visible
    
    def _save_credentials(self):
        """Save credentials"""
        # If fields are disabled, we're editing existing
        if str(self.client_id_entry.cget("state")) == "disabled":
            # Enable editing mode
            self.client_id_entry.configure(state="normal")
            self.client_id_entry.delete(0, "end")
            self.client_secret_entry.configure(state="normal", show="•")
            self.client_secret_entry.delete(0, "end")
            self.save_btn.configure(text="💾  Save Credentials")
            self.id_real_value = ""
            self.secret_real_value = ""
            return
        
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        
        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter both Client ID and Client Secret")
            return
        
        # Save
        config_manager.set_credentials(client_id, client_secret)
        
        # Update UI
        self.id_real_value = client_id
        self.secret_real_value = client_secret
        
        self.client_id_entry.delete(0, "end")
        self.client_id_entry.insert(0, config_manager.obfuscate(client_id))
        self.client_id_entry.configure(state="disabled")
        
        self.client_secret_entry.delete(0, "end")
        self.client_secret_entry.insert(0, config_manager.obfuscate(client_secret))
        self.client_secret_entry.configure(state="disabled", show="")
        
        self._update_status()
        messagebox.showinfo("Success", "Credentials saved successfully!")
    
    def _clear_credentials(self):
        """Clear saved credentials"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear saved credentials?"):
            config_manager.clear_credentials()
            
            self.client_id_entry.configure(state="normal")
            self.client_id_entry.delete(0, "end")
            
            self.client_secret_entry.configure(state="normal", show="•")
            self.client_secret_entry.delete(0, "end")
            
            self.id_real_value = ""
            self.secret_real_value = ""
            self.id_visible = False
            self.secret_visible = False
            
            self._update_status()
            messagebox.showinfo("Success", "Credentials cleared!")
    
    def _handle_theme_change(self, theme):
        """Handle theme change"""
        config_manager.set_setting("theme", theme)
        if self.on_theme_change:
            self.on_theme_change(theme)
    
    def _handle_check_deps(self):
        """Handle check dependencies"""
        if self.on_check_deps:
            self.on_check_deps()
