"""Session model for work time tracking."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Session(Base):
    """Work session for time tracking."""
    
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20), ForeignKey('users.discord_id'), nullable=False, index=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_paid = Column(Boolean, default=False, nullable=False, index=True)
    
    user = relationship('User', back_populates='sessions')
    screenshots = relationship('Screenshot', back_populates='session', cascade='all, delete-orphan')
    
    @property
    def duration_minutes(self) -> int:
        """Calculate session duration in minutes (rounded up)."""
        if not self.ended_at:
            return 0
        duration = self.ended_at - self.started_at
        total_seconds = duration.total_seconds()
        return (int(total_seconds) + 59) // 60
    
    @property
    def duration_hours(self) -> float:
        """Calculate session duration in hours."""
        return self.duration_minutes / 60
    
    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id}, active={self.is_active})>"
