"""Health service for tracking agent online status via heartbeat."""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.config import settings
from app.models.agent_status import AgentStatus
from app.models.user import User


class HealthService:
    """Service for checking agent health status."""
    
    def __init__(self, db: Session):
        self.db = db
        self.threshold_seconds = settings.HEALTH_THRESHOLD_SECONDS
    
    def is_agent_healthy(self, user_id: str) -> bool:
        """Check if agent is healthy (heartbeat within last 90 seconds)."""
        status = self.db.query(AgentStatus).filter(
            AgentStatus.user_id == user_id
        ).first()
        
        if not status:
            return False
        
        if not status.is_online:
            return False
        
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.threshold_seconds)
        return status.last_heartbeat > cutoff_time
    
    def update_heartbeat(self, user_id: str, version: str = "unknown") -> AgentStatus:
        """Update agent heartbeat timestamp."""
        status = self.db.query(AgentStatus).filter(
            AgentStatus.user_id == user_id
        ).first()
        
        now = datetime.utcnow()
        
        if status:
            status.last_heartbeat = now
            status.is_online = True
            status.version = version
            status.updated_at = now
        else:
            user = self.db.query(User).filter(User.discord_id == user_id).first()
            if not user:
                user = User(discord_id=user_id, username=f"user_{user_id}", hourly_rate=0.0)
                self.db.add(user)
                self.db.flush()
            
            status = AgentStatus(
                user_id=user_id,
                last_heartbeat=now,
                is_online=True,
                version=version
            )
            self.db.add(status)
        
        self.db.commit()
        return status
    
    def get_agent_status(self, user_id: str) -> Optional[AgentStatus]:
        """Get raw agent status for a user."""
        return self.db.query(AgentStatus).filter(
            AgentStatus.user_id == user_id
        ).first()
    
    def get_seconds_since_heartbeat(self, user_id: str) -> Optional[int]:
        """Get seconds elapsed since last heartbeat."""
        status = self.get_agent_status(user_id)
        if not status:
            return None
        elapsed = datetime.utcnow() - status.last_heartbeat
        return int(elapsed.total_seconds())
    
    def mark_offline(self, user_id: str) -> None:
        """Mark agent as offline."""
        status = self.db.query(AgentStatus).filter(
            AgentStatus.user_id == user_id
        ).first()
        
        if status:
            status.is_online = False
            self.db.commit()
