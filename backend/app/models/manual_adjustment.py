"""ManualAdjustment model for admin time corrections."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class ManualAdjustment(Base):
    """Manual time adjustments added by admins (+/- minutes)."""
    
    __tablename__ = 'manual_adjustments'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20), ForeignKey('users.discord_id'), nullable=False, index=True)
    minutes = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    created_by = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False, index=True)
    
    user = relationship('User', back_populates='adjustments')
    
    @property
    def hours(self) -> float:
        """Convert minutes to hours."""
        return self.minutes / 60
    
    def __repr__(self):
        return f"<ManualAdjustment(id={self.id}, user_id={self.user_id}, minutes={self.minutes})>"
