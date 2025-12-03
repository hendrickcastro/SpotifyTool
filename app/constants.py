# -*- coding: utf-8 -*-
"""
Application constants - Re-exports from config.py for backward compatibility
All new code should import from app.config directly
"""

from .config import (
    # App info
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    
    # Paths
    APP_DIR,
    ROOT_DIR,
    BIN_DIR,
    LOG_FILE,
    CONFIG_FILE,
    DEFAULT_DOWNLOAD_DIR,
    
    # Window
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    
    # Colors
    COLORS,
    
    # Fonts
    FONTS,
    
    # Sizes
    SIZES,
    
    # Audio
    AUDIO,
    
    # Download
    DOWNLOAD,
    
    # Navigation
    NAV_ITEMS,
    
    # Messages
    MESSAGES,
    
    # Helpers
    get_color,
    get_font_size,
)

# Legacy constant for backward compatibility
PITCH_RATIO = AUDIO["pitch_ratio"]
