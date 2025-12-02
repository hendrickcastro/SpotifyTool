"""
Configuration module for Spotify Downloader
Loads settings from environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Spotify API credentials
    SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    
    # Download settings
    DOWNLOAD_PATH: Path = Path(os.getenv("DOWNLOAD_PATH", "./downloads"))
    AUDIO_FORMAT: str = os.getenv("AUDIO_FORMAT", "mp3")
    AUDIO_QUALITY: int = int(os.getenv("AUDIO_QUALITY", "320"))
    
    # Spotify API scopes needed
    SPOTIFY_SCOPE: str = "playlist-read-private playlist-read-collaborative user-library-read"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.SPOTIFY_CLIENT_ID or not cls.SPOTIFY_CLIENT_SECRET:
            return False
        return True
    
    @classmethod
    def ensure_download_dir(cls) -> Path:
        """Ensure download directory exists"""
        cls.DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
        return cls.DOWNLOAD_PATH


config = Config()

