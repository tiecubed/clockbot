"""Pay service for calculating payroll amounts."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.session import Session as WorkSession
from app.models.manual_adjustment import ManualAdjustment
from app.services.time_service import TimeService


class PayService:
    """Service for calculating pay amounts."""
    
    def __init__(self, db: Session):
        self.db = db
        self.time_service = TimeService(db)
    
    def get_unpaid_session_minutes(self, user_id: str) -> int:
        """Get total unpaid session minutes for user."""
        sessions = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id,
            WorkSession.is_active == False,
            WorkSession.is_paid == False
        ).all()
        return sum(s.duration_minutes for s in sessions)
    
    def get_unpaid_adjustment_minutes(self, user_id: str) -> int:
        """Get total unpaid manual adjustment minutes for user."""
        adjustments = self.db.query(ManualAdjustment).filter(
            ManualAdjustment.user_id == user_id,
            ManualAdjustment.is_paid == False
        ).all()
        return sum(a.minutes for a in adjustments)
    
    def get_unpaid_summary(self, user_id: str) -> Dict:
        """Get complete unpaid summary for user."""
        user = self.db.query(User).filter(User.discord_id == user_id).first()
        if not user:
            return {'session_minutes': 0, 'adjustment_minutes': 0, 'total_minutes': 0, 'total_hours': 0, 'hourly_rate': 0, 'pay_amount': 0}
        
        session_minutes = self.get_unpaid_session_minutes(user_id)
        adjustment_minutes = self.get_unpaid_adjustment_minutes(user_id)
        total_minutes = session_minutes + adjustment_minutes
        total_hours = total_minutes / 60
        pay_amount = total_hours * user.hourly_rate
        
        return {
            'session_minutes': session_minutes,
            'adjustment_minutes': adjustment_minutes,
            'total_minutes': total_minutes,
            'total_hours': round(total_hours, 2),
            'hourly_rate': user.hourly_rate,
            'pay_amount': round(pay_amount, 2)
        }
    
    def get_all_unpaid_payroll(self) -> List[Dict]:
        """Get all users with unpaid time for payroll processing."""
        users_with_sessions = self.db.query(WorkSession.user_id).filter(
            WorkSession.is_paid == False, WorkSession.is_active == False
        ).distinct().all()
        
        users_with_adjustments = self.db.query(ManualAdjustment.user_id).filter(
            ManualAdjustment.is_paid == False
        ).distinct().all()
        
        user_ids = set([u[0] for u in users_with_sessions] + [u[0] for u in users_with_adjustments])
        
        payroll = []
        for user_id in user_ids:
            user = self.db.query(User).filter(User.discord_id == user_id).first()
            if not user:
                continue
            summary = self.get_unpaid_summary(user_id)
            if summary['total_minutes'] > 0:
                payroll.append({
                    'user_id': user_id,
                    'username': user.username,
                    'hourly_rate': user.hourly_rate,
                    'session_minutes': summary['session_minutes'],
                    'adjustment_minutes': summary['adjustment_minutes'],
                    'total_hours': summary['total_hours'],
                    'pay_amount': summary['pay_amount']
                })
        
        payroll.sort(key=lambda x: x['username'].lower())
        return payroll
    
    def mark_user_paid(self, user_id: str) -> bool:
        """Mark all unpaid sessions and adjustments as paid for a user."""
        changed = False
        
        sessions = self.db.query(WorkSession).filter(
            WorkSession.user_id == user_id, WorkSession.is_paid == False, WorkSession.is_active == False
        ).all()
        for session in sessions:
            session.is_paid = True
            changed = True
        
        adjustments = self.db.query(ManualAdjustment).filter(
            ManualAdjustment.user_id == user_id, ManualAdjustment.is_paid == False
        ).all()
        for adj in adjustments:
            adj.is_paid = True
            changed = True
        
        if changed:
            self.db.commit()
        return changed
    
    def mark_all_paid(self) -> List[str]:
        """Mark all unpaid time as paid."""
        payroll = self.get_all_unpaid_payroll()
        user_ids = []
        for entry in payroll:
            if self.mark_user_paid(entry['user_id']):
                user_ids.append(entry['user_id'])
        return user_ids
    
    def add_manual_time(self, user_id: str, minutes: int, created_by: str, reason: Optional[str] = None) -> ManualAdjustment:
        """Add manual time adjustment."""
        adj = ManualAdjustment(user_id=user_id, minutes=minutes, reason=reason or "Manual adjustment", created_by=created_by)
        self.db.add(adj)
        self.db.commit()
        return adj
