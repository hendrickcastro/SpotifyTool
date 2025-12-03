"""
Verify conversion page
"""

import customtkinter as ctk
from .base_page import BasePage
from ..config import COLORS, SIZES


class VerifyPage(BasePage):
    """Verification page"""
    
    def __init__(self, master, on_verify, **kwargs):
        super().__init__(
            master, 
            title="Verify Conversion",
            subtitle="Compare original and converted files",
            **kwargs
        )
        self.on_verify = on_verify
        self.grid_rowconfigure(2, weight=1)
        
        self._create_card()
        self._create_results()
        self._create_copy_button()
    
    def _create_card(self):
        """Create input card"""
        card = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=16)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        card.grid_columnconfigure(0, weight=1)
        
        # Original file
        ctk.CTkLabel(
            card,
            text="Original File (440Hz)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=25, pady=(25, 8), sticky="w")
        
        orig_frame = ctk.CTkFrame(card, fg_color="transparent")
        orig_frame.grid(row=1, column=0, padx=25, sticky="ew")
        orig_frame.grid_columnconfigure(0, weight=1)
        
        self.orig_entry = ctk.CTkEntry(orig_frame, height=50, corner_radius=10)
        self.orig_entry.grid(row=0, column=0, sticky="ew")
        
        ctk.CTkButton(
            orig_frame, text="📁", width=50, height=50, corner_radius=10,
            fg_color=COLORS['bg_dark'], hover_color=COLORS['bg_card_hover'],
            command=lambda: self.browse_file(self.orig_entry)
        ).grid(row=0, column=1, padx=(10, 0))
        
        # Converted file
        ctk.CTkLabel(
            card,
            text="Converted File (432Hz)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=2, column=0, padx=25, pady=(20, 8), sticky="w")
        
        conv_frame = ctk.CTkFrame(card, fg_color="transparent")
        conv_frame.grid(row=3, column=0, padx=25, sticky="ew")
        conv_frame.grid_columnconfigure(0, weight=1)
        
        self.conv_entry = ctk.CTkEntry(conv_frame, height=50, corner_radius=10)
        self.conv_entry.grid(row=0, column=0, sticky="ew")
        
        ctk.CTkButton(
            conv_frame, text="📁", width=50, height=50, corner_radius=10,
            fg_color=COLORS['bg_dark'], hover_color=COLORS['bg_card_hover'],
            command=lambda: self.browse_file(self.conv_entry)
        ).grid(row=0, column=1, padx=(10, 0))
        
        # Verify button
        ctk.CTkButton(
            card,
            text="✓  Verify Conversion",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            command=self._start_verify
        ).grid(row=4, column=0, padx=25, pady=25, sticky="ew")
    
    def _create_results(self):
        """Create results textbox"""
        self.results = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=12,
            fg_color=COLORS['bg_card']
        )
        self.results.grid(row=2, column=0, sticky="nsew")
    
    def _create_copy_button(self):
        """Create copy to clipboard button"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="e", pady=(10, 0))
        
        self.copy_btn = ctk.CTkButton(
            btn_frame,
            text="📋 Copy to Clipboard",
            font=ctk.CTkFont(size=13),
            height=35,
            corner_radius=8,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['bg_card_hover'],
            command=self._copy_to_clipboard
        )
        self.copy_btn.pack(side="right")
    
    def _copy_to_clipboard(self):
        """Copy results to clipboard"""
        content = self.results.get("1.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            
            # Show feedback
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="✓ Copied!", fg_color=COLORS['success'])
            self.after(2000, lambda: self.copy_btn.configure(
                text=original_text, fg_color=COLORS['bg_card']))
    
    def _start_verify(self):
        """Handle verify button click"""
        orig = self.orig_entry.get().strip()
        conv = self.conv_entry.get().strip()
        
        if self.on_verify:
            self.on_verify(orig, conv)
    
    def show_results(self, text):
        """Display verification results"""
        self.results.delete("1.0", "end")
        self.results.insert("1.0", text)

