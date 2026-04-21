"""Discord Bot Configuration"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


@dataclass
class BotConfig:
    """Bot configuration from environment"""
    # Discord
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '')
    COMMAND_PREFIX: str = os.getenv('COMMAND_PREFIX', '!clock')
    
    # Backend API
    API_BASE_URL: str = os.getenv('API_BASE_URL', 'http://localhost:8000')
    SHARED_TOKEN: str = os.getenv('SHARED_TOKEN', '')
    
    # Guild Settings (defaults, can be overridden via commands)
    DEFAULT_GUILD_ID: str = os.getenv('DEFAULT_GUILD_ID', '1298218073941217331')
    CLOCK_ROLE_ID: str = os.getenv('CLOCK_ROLE_ID', '1324268726819754055')
    ADMIN_ROLE_ID: str = os.getenv('ADMIN_ROLE_ID', '1298219350817505354')
    SCREENSHOT_CHANNEL_ID: str = os.getenv('SCREENSHOT_CHANNEL_ID', '1407132078121816156')
    INOUT_CHANNEL_ID: str = os.getenv('INOUT_CHANNEL_ID', '1495997857180684410')
    
    @property
    def is_configured(self) -> bool:
        """Check if required tokens are set"""
        return bool(self.DISCORD_TOKEN and self.SHARED_TOKEN)


config = BotConfig()
