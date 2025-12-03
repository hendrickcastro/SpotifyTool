"""
Application constants and color scheme
"""

# Color palette
COLORS = {
    # Spotify brand
    "spotify_green": "#1DB954",
    "spotify_green_hover": "#1ed760",
    "spotify_dark": "#191414",
    
    # Purple accent
    "purple": "#8B5CF6",
    "purple_hover": "#7C3AED",
    
    # Status colors
    "success": "#10B981",
    "success_hover": "#059669",
    "warning": "#F59E0B",
    "error": "#EF4444",
    
    # Backgrounds
    "bg_dark": "#0f0f0f",
    "bg_card": "#1a1a1a",
    "bg_card_hover": "#252525",
    
    # Text
    "text_primary": "#ffffff",
    "text_muted": "#6b7280",
    
    # Borders
    "border": "#2d2d2d",
}

# App info
APP_NAME = "SpotifyTool"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Download from Spotify + Convert to 432Hz"

# Window settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 700

# 432Hz conversion
PITCH_RATIO = 432 / 440  # = 0.981818...

