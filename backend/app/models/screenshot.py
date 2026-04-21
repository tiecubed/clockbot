"""Screenshot model for storing captured screenshots."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Screenshot(Base):
    """Screenshot captured by desktop agent."""
    
    __tablename__ = 'screenshots'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False, index=True)
    monitor_index = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    session = relationship('Session', back_populates='screenshots')
    
    def __repr__(self):
        return f"<Screenshot(id={self.id}, session_id={self.session_id}, monitor={self.monitor_index})>"
