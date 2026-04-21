"""Desktop Agent Entry Point"""
import sys
import os
import asyncio

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from core.config import config
from utils.token_manager import TokenManager


def check_configuration():
    """Check if agent is configured"""
    if not config.is_configured:
        print("❌ Agent not configured!")
        print("Please set BACKEND_URL and SHARED_TOKEN in .env")
        return False
    return True


def check_saved_token():
    """Check for saved authentication token"""
    token_data = TokenManager.load_token()
    if token_data:
        print(f"✅ Found saved token for user: {token_data.get('username', 'unknown')}")
        return token_data
    return None


def main():
    """Main entry point"""
    print("=" * 60)
    print("Time Tracker Desktop Agent")
    print("=" * 60)
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    print(f"✅ Configuration loaded")
    print(f"   Backend: {config.BACKEND_URL}")
    print(f"   Heartbeat: {config.HEARTBEAT_INTERVAL}s")
    print(f"   Screenshot: {config.SCREENSHOT_INTERVAL}s")
    
    # Check for saved token
    token_data = check_saved_token()
    if token_data:
        print(f"✅ User authenticated: {token_data.get('username')}")
        print("\nTODO: Start GUI with system tray and heartbeat")
    else:
        print("⚠️  No saved token found")
        print("\nTODO: Show login dialog for OAuth")
    
    print("\n" + "=" * 60)
    print("Phase 5 Foundation Complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
