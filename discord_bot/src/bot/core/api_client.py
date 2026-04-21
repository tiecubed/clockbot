"""Backend API Client for Discord Bot"""
import httpx
from typing import Optional, Dict, Any
from ..config import config


class BackendAPIClient:
    """HTTP client for backend API communication"""
    
    def __init__(self):
        self.base_url = config.API_BASE_URL.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {config.SHARED_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30.0
        )
    
    async def close(self):
        await self.client.aclose()
    
    # Agents
    async def check_agent_health(self, user_id: str) -> Dict[str, Any]:
        """Check if agent is healthy (90s heartbeat rule)"""
        response = await self.client.get(f'/api/v1/agents/{user_id}/health')
        response.raise_for_status()
        return response.json()
    
    # Sessions
    async def start_session(self, user_id: str) -> Dict[str, Any]:
        """Clock in - creates new session"""
        response = await self.client.post(
            '/api/v1/sessions/start',
            json={'user_id': user_id}
        )
        response.raise_for_status()
        return response.json()
    
    async def end_session(self, session_id: int, user_id: str) -> Dict[str, Any]:
        """Clock out - ends session"""
        response = await self.client.post(
            f'/api/v1/sessions/{session_id}/end',
            json={'user_id': user_id}
        )
        response.raise_for_status()
        return response.json()
    
    async def get_active_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active session if any"""
        response = await self.client.get(f'/api/v1/sessions/active/{user_id}')
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
    # Users
    async def get_today_time(self, user_id: str) -> Dict[str, Any]:
        response = await self.client.get(f'/api/v1/users/{user_id}/time/today')
        response.raise_for_status()
        return response.json()
    
    async def get_week_time(self, user_id: str) -> Dict[str, Any]:
        response = await self.client.get(f'/api/v1/users/{user_id}/time/week')
        response.raise_for_status()
        return response.json()
    
    async def get_pay_summary(self, user_id: str) -> Dict[str, Any]:
        response = await self.client.get(f'/api/v1/users/{user_id}/pay/unpaid')
        response.raise_for_status()
        return response.json()
    
    async def get_user_status(self, user_id: str) -> Dict[str, Any]:
        response = await self.client.get(f'/api/v1/users/{user_id}/status')
        response.raise_for_status()
        return response.json()
    
    async def set_hourly_rate(self, user_id: str, hourly_rate: float) -> Dict[str, Any]:
        response = await self.client.post(
            f'/api/v1/users/{user_id}/hourlyrate',
            json={'hourly_rate': hourly_rate}
        )
        response.raise_for_status()
        return response.json()
    
    # Payroll (admin)
    async def get_all_unpaid(self) -> Dict[str, Any]:
        response = await self.client.get('/api/v1/payroll/unpaid')
        response.raise_for_status()
        return response.json()
    
    async def get_active_users(self) -> Dict[str, Any]:
        response = await self.client.get('/api/v1/payroll/active')
        response.raise_for_status()
        return response.json()
    
    async def clear_payroll(self) -> Dict[str, Any]:
        response = await self.client.post('/api/v1/payroll/clear')
        response.raise_for_status()
        return response.json()
    
    async def add_manual_time(self, user_id: str, minutes: int, reason: str, created_by: str) -> Dict[str, Any]:
        response = await self.client.post(
            '/api/v1/payroll/adjustments',
            json={
                'user_id': user_id,
                'minutes': minutes,
                'reason': reason,
                'created_by': created_by
            }
        )
        response.raise_for_status()
        return response.json()
