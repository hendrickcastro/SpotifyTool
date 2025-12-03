"""
Configuration manager for storing and retrieving credentials
"""

import json
import os
from pathlib import Path
from base64 import b64encode, b64decode


class ConfigManager:
    """Manages application configuration and credentials"""
    
    CONFIG_FILE = "spotifytool_config.json"
    
    def __init__(self):
        self.config_path = Path.home() / ".spotifytool" / self.CONFIG_FILE
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config = self._load()
    
    def _load(self) -> dict:
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def _encode(self, value: str) -> str:
        """Simple encoding for credentials (not encryption, just obfuscation)"""
        if not value:
            return ""
        return b64encode(value.encode()).decode()
    
    def _decode(self, value: str) -> str:
        """Decode encoded value"""
        if not value:
            return ""
        try:
            return b64decode(value.encode()).decode()
        except:
            return value
    
    def set_credentials(self, client_id: str, client_secret: str):
        """Save Spotify credentials"""
        self._config['spotify_client_id'] = self._encode(client_id)
        self._config['spotify_client_secret'] = self._encode(client_secret)
        self._save()
    
    def get_credentials(self) -> tuple:
        """Get Spotify credentials (decoded)"""
        client_id = self._decode(self._config.get('spotify_client_id', ''))
        client_secret = self._decode(self._config.get('spotify_client_secret', ''))
        return client_id, client_secret
    
    def has_credentials(self) -> bool:
        """Check if credentials are saved"""
        client_id, client_secret = self.get_credentials()
        return bool(client_id and client_secret)
    
    def clear_credentials(self):
        """Remove saved credentials"""
        self._config.pop('spotify_client_id', None)
        self._config.pop('spotify_client_secret', None)
        self._save()
    
    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self._config.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a setting value"""
        self._config[key] = value
        self._save()
    
    @staticmethod
    def obfuscate(value: str, visible_chars: int = 4) -> str:
        """Obfuscate a string showing only last N characters"""
        if not value:
            return ""
        if len(value) <= visible_chars:
            return "*" * len(value)
        return "*" * (len(value) - visible_chars) + value[-visible_chars:]


# Global instance
config_manager = ConfigManager()

