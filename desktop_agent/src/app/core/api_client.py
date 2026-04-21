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
        """
        Upload screenshot to backend.
        Uses multipart/form-data encoding for file upload.
        """
        # Build multipart form data manually for async compatibility
        boundary = '----FormBoundary' + str(hash(str(image_data)))[:16]
        
        # Build multipart body
        body = bytearray()
        
        # Add user_id field
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(b'Content-Disposition: form-data; name="user_id"\r\n\r\n')
        body.extend(f'{user_id}\r\n'.encode())
        
        # Add session_id field
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(b'Content-Disposition: form-data; name="session_id"\r\n\r\n')
        body.extend(f'{session_id}\r\n'.encode())
        
        # Add monitor_index field
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(b'Content-Disposition: form-data; name="monitor_index"\r\n\r\n')
        body.extend(f'{monitor_index}\r\n'.encode())
        
        # Add image file
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(b'Content-Disposition: form-data; name="image"; filename="screenshot.jpg"\r\n')
        body.extend(b'Content-Type: image/jpeg\r\n\r\n')
        body.extend(image_data)
        body.extend(b'\r\n')
        
        # End boundary
        body.extend(f'--{boundary}--\r\n'.encode())
        
        # Send request with custom content type
        response = await self.client.post(
            '/api/v1/screenshots/upload',
            content=bytes(body),
            headers={
                'Authorization': f'Bearer {self.token}',
                'Content-Type': f'multipart/form-data; boundary={boundary}'
            },
            timeout=60.0
        )
        response.raise_for_status()
        return response.json()
    
    async def get_user_status(self, user_id: str) -> Dict[str, Any]:
        """Get user clock status"""
        response = await self.client.get(f'/api/v1/users/{user_id}/status')
        response.raise_for_status()
        return response.json()
