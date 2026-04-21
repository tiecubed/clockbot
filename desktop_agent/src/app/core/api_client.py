"""Backend API Client for Desktop Agent"""
import httpx
from typing import Optional, Dict, Any
from .config import config


class BackendAPIClient:
    """HTTP client for backend API communication"""
    
    def __init__(self, token: str = None):
        self.base_url = config.BACKEND_URL.rstrip('/')
        self.token = token or config.SHARED_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30.0
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def send_heartbeat(self, user_id: str, version: str = "1.0.0") -> Dict[str, Any]:
        """Send heartbeat to backend (30s interval)"""
        response = await self.client.post(
            '/api/v1/agents/heartbeat',
            json={'user_id': user_id, 'version': version}
        )
        response.raise_for_status()
        return response.json()
    
    async def check_health(self, user_id: str) -> Dict[str, Any]:
        """Check agent health status"""
        response = await self.client.get(
            f'/api/v1/agents/{user_id}/health'
        )
        response.raise_for_status()
        return response.json()
    
    async def upload_screenshot(self, user_id: str, session_id: int, 
                                 monitor_index: int, image_data: bytes) -> Dict[str, Any]:
        """Upload screenshot to backend"""
        files = {'image': ('screenshot.jpg', image_data, 'image/jpeg')}
        data = {
            'user_id': user_id,
            'session_id': session_id,
            'monitor_index': monitor_index
        }
        
        # Use sync client for multipart upload
        import httpx
        response = httpx.post(
            f'{self.base_url}/api/v1/screenshots/upload',
            headers={'Authorization': f'Bearer {self.token}'},
            data=data,
            files=files,
            timeout=60.0
        )
        response.raise_for_status()
        return response.json()
    
    async def get_user_status(self, user_id: str) -> Dict[str, Any]:
        """Get user clock status"""
        response = await self.client.get(f'/api/v1/users/{user_id}/status')
        response.raise_for_status()
        return response.json()
