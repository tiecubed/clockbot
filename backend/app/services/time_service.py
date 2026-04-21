"""Time service for calculating work time."""
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from app.models.session import Session as WorkSession


class TimeService:
    """Service for calculating work time and session data."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_today_minutes(self, user_id: str) -> Tuple[int, float]:
        """Get total minutes worked today. Returns (minutes, hours)."""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        sessions = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == False,
            WorkSession.ended_at >= today_start,
            WorkSession.ended_at < today_end
        ).all()
        
        total_minutes = sum(s.duration_minutes for s in sessions)
        
        active = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == True
        ).first()
        
        if active:
            elapsed = datetime.utcnow() - active.started_at
            active_minutes = int(elapsed.total_seconds()) // 60
            total_minutes += active_minutes
        
        return total_minutes, total_minutes / 60
    
    def get_week_minutes(self, user_id: str) -> Tuple[int, float]:
        """Get total minutes worked in last 7 days (rolling). Returns (minutes, hours)."""
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        sessions = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == False,
            WorkSession.ended_at >= week_ago
        ).all()
        
        total_minutes = sum(s.duration_minutes for s in sessions)
        
        active = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == True
        ).first()
        
        if active:
            elapsed = datetime.utcnow() - active.started_at
            active_minutes = int(elapsed.total_seconds()) // 60
            total_minutes += active_minutes
        
        return total_minutes, total_minutes / 60
    
    def get_session_duration(self, session: WorkSession) -> int:
        """Get session duration in minutes."""
        if session.ended_at:
            return session.duration_minutes
        elapsed = datetime.utcnow() - session.started_at
        return int(elapsed.total_seconds()) // 60
    
    def format_duration(self, minutes: int) -> str:
        """Format minutes as 'X hours Y minutes'."""
        hours = minutes // 60
        mins = minutes % 60
        if hours == 0:
            return f"{mins} minutes"
        elif mins == 0:
            return f"{hours} hours"
        else:
            return f"{hours} hours {mins} minutes"
    
    def get_active_session(self, user_id: str) -> Optional[WorkSession]:
        """Get user's active session if any."""
        return self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == True
        ).first()
    
    def get_all_active_sessions(self) -> List[WorkSession]:
        """Get all currently active sessions."""
        return self.db.query(WorkSession).filter(
            WorkSession.is_active == True
        ).all()
