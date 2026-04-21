"""AgentStatus model for tracking desktop agent health."""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class AgentStatus(Base):
    """Tracks desktop agent online status via heartbeat."""
    
    __tablename__ = 'agent_status'
    
    user_id = Column(String(20), ForeignKey('users.discord_id'), primary_key=True, index=True)
    last_heartbeat = Column(DateTime, nullable=False)
    is_online = Column(Boolean, default=True, nullable=False)
    version = Column(String(20), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    user = relationship('User', back_populates='agent_status')
    
    def __repr__(self):
        return f"<AgentStatus(user_id={self.user_id}, online={self.is_online}, last_heartbeat={self.last_heartbeat})>"
