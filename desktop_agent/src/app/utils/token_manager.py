"""Token Manager for Desktop Agent"""
import os
import json
from pathlib import Path


class TokenManager:
    """Manage agent authentication tokens"""
    
    TOKEN_FILE = 'agent_token.json'
    
    @classmethod
    def get_token_path(cls) -> Path:
        """Get path to token file (in app data directory)"""
        # Store in user's home directory for portability
        token_dir = Path.home() / '.clock_agent'
        token_dir.mkdir(exist_ok=True)
        return token_dir / cls.TOKEN_FILE
    
    @classmethod
    def save_token(cls, token: str, user_id: str = None, username: str = None):
        """Save token to file"""
        token_path = cls.get_token_path()
        data = {
            'token': token,
            'user_id': user_id,
            'username': username
        }
        with open(token_path, 'w') as f:
            json.dump(data, f)
        return token_path
    
    @classmethod
    def load_token(cls) -> dict:
        """Load token from file"""
        token_path = cls.get_token_path()
        if not token_path.exists():
            return None
        try:
            with open(token_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @classmethod
    def clear_token(cls):
        """Clear saved token"""
        token_path = cls.get_token_path()
        if token_path.exists():
            token_path.unlink()
    
    @classmethod
    def has_token(cls) -> bool:
        """Check if token exists"""
        return cls.get_token_path().exists()
