"""User model for Discord users."""
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    """Discord user with time tracking profile."""
    
    __tablename__ = 'users'
    
    discord_id = Column(String(20), primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    hourly_rate = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    sessions = relationship('Session', back_populates='user', cascade='all, delete-orphan')
    adjustments = relationship('ManualAdjustment', back_populates='user', cascade='all, delete-orphan')
    agent_status = relationship('AgentStatus', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(discord_id={self.discord_id}, username={self.username})>"
