"""Desktop Agent Configuration"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env from project root or current directory
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()


@dataclass
class AgentConfig:
    """Agent configuration from environment"""
    
    # Backend API
    BACKEND_URL: str = os.getenv('BACKEND_URL', 'http://localhost:8000')
    SHARED_TOKEN: str = os.getenv('SHARED_TOKEN', '')
    
    # OAuth (Discord)
    OAUTH_REDIRECT_PORT: int = int(os.getenv('OAUTH_REDIRECT_PORT', '53134'))
    DISCORD_CLIENT_ID: str = os.getenv('DISCORD_CLIENT_ID', '')
    
    # Agent Settings
    HEARTBEAT_INTERVAL: int = int(os.getenv('HEARTBEAT_INTERVAL', '30'))
    SCREENSHOT_INTERVAL: int = int(os.getenv('SCREENSHOT_INTERVAL', '300'))
    
    # Image Processing
    MAX_WIDTH: int = int(os.getenv('MAX_WIDTH', '1920'))
    JPEG_QUALITY: int = int(os.getenv('JPEG_QUALITY', '70'))
    
    @property
    def is_configured(self) -> bool:
        """Check if required tokens are set"""
        return bool(self.SHARED_TOKEN and self.BACKEND_URL)
    
    @property
    def can_oauth(self) -> bool:
        """Check if OAuth is configured"""
        return bool(self.DISCORD_CLIENT_ID)


config = AgentConfig()
