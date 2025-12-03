# -*- coding: utf-8 -*-
"""
Musicalar - Central Configuration
All components should import from here
"""

from pathlib import Path

# =============================================================================
# APP INFO
# =============================================================================
APP_NAME = "Musicalar"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Download from Spotify + Tools to modify the pitch of the music and more"
APP_AUTHOR = "Algoritxia"

# =============================================================================
# PATHS
# =============================================================================
APP_DIR = Path(__file__).parent
ROOT_DIR = APP_DIR.parent
BIN_DIR = ROOT_DIR / "bin"
LOG_FILE = ROOT_DIR / "musicalar.log"
CONFIG_FILE = ROOT_DIR / "musicalar_config.json"
DEFAULT_DOWNLOAD_DIR = ROOT_DIR / "downloads"

# =============================================================================
# WINDOW SETTINGS
# =============================================================================
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 700

# =============================================================================
# COLOR PALETTE
# =============================================================================
COLORS = {
    # Brand colors
    "primary": "#1DB954",           # Spotify green
    "primary_hover": "#1ed760",
    "secondary": "#8B5CF6",         # Purple
    "secondary_hover": "#7C3AED",
    
    # Semantic colors
    "success": "#10B981",
    "success_hover": "#059669",
    "warning": "#F59E0B",
    "warning_hover": "#D97706",
    "error": "#EF4444",
    "error_hover": "#DC2626",
    "info": "#3B82F6",
    "info_hover": "#2563EB",
    
    # Backgrounds
    "bg_dark": "#0f0f0f",
    "bg_main": "#121212",
    "bg_card": "#1a1a1a",
    "bg_card_hover": "#252525",
    "bg_input": "#2a2a2a",
    
    # Text
    "text_primary": "#ffffff",
    "text_secondary": "#b3b3b3",
    "text_muted": "#6b7280",
    "text_disabled": "#4b5563",
    
    # Borders
    "border": "#2d2d2d",
    "border_focus": "#1DB954",
    
    # Legacy aliases (for backward compatibility)
    "spotify_green": "#1DB954",
    "spotify_green_hover": "#1ed760",
    "spotify_dark": "#191414",
    "purple": "#8B5CF6",
    "purple_hover": "#7C3AED",
}

# =============================================================================
# FONTS
# =============================================================================
FONTS = {
    "family": "Segoe UI",
    "family_mono": "Consolas",
    "size_xs": 10,
    "size_sm": 12,
    "size_md": 14,
    "size_lg": 16,
    "size_xl": 20,
    "size_2xl": 24,
    "size_3xl": 32,
}

# =============================================================================
# UI SIZES
# =============================================================================
SIZES = {
    # Buttons
    "btn_height_sm": 32,
    "btn_height_md": 40,
    "btn_height_lg": 50,
    "btn_height_xl": 55,
    
    # Inputs
    "input_height": 45,
    "input_corner_radius": 10,
    
    # Cards
    "card_corner_radius": 16,
    "card_padding": 25,
    
    # Sidebar
    "sidebar_width": 220,
    
    # General
    "corner_radius_sm": 8,
    "corner_radius_md": 12,
    "corner_radius_lg": 16,
}

# =============================================================================
# 432Hz CONVERSION
# =============================================================================
AUDIO = {
    "pitch_ratio": 432 / 440,       # = 0.981818...
    "target_frequency": 432,
    "source_frequency": 440,
    "default_bitrate": "320k",
    "default_format": "mp3",
    "supported_formats": ["mp3", "flac", "ogg", "opus", "m4a", "wav"],
}

# =============================================================================
# DOWNLOAD SETTINGS
# =============================================================================
DOWNLOAD = {
    "default_output": str(DEFAULT_DOWNLOAD_DIR),
    "default_bitrate": "320k",
    "default_format": "mp3",
}

# =============================================================================
# NAVIGATION
# =============================================================================
NAV_ITEMS = [
    {"id": "download", "label": "📥  Download", "color": COLORS["primary"]},
    {"id": "convert", "label": "🎚️  Convert 432Hz", "color": COLORS["secondary"]},
    {"id": "verify", "label": "✓  Verify", "color": COLORS["success"]},
    {"id": "settings", "label": "⚙️  Settings", "color": COLORS["text_muted"]},
]

# =============================================================================
# MESSAGES
# =============================================================================
MESSAGES = {
    "ready": "Ready",
    "downloading": "Downloading...",
    "converting": "Converting to 432Hz...",
    "verifying": "Verifying...",
    "complete": "Complete!",
    "error": "An error occurred",
    "ffmpeg_downloading": "Downloading FFmpeg...",
    "ffmpeg_ready": "FFmpeg ready!",
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_color(name: str, fallback: str = "#ffffff") -> str:
    """Get color by name with fallback"""
    return COLORS.get(name, fallback)


def get_font_size(name: str, fallback: int = 14) -> int:
    """Get font size by name with fallback"""
    key = f"size_{name}"
    return FONTS.get(key, fallback)

