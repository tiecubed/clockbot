"""Users router for time tracking and pay queries."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import verify_token
from app.services.time_service import TimeService
from app.services.pay_service import PayService
from app.models.user import User
from app.schemas import (
    TimeSummaryResponse, PaySummaryResponse,
    HourlyRateRequest, HourlyRateResponse
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/time/today", response_model=TimeSummaryResponse)
async def get_today_time(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's total time worked today."""
    time_service = TimeService(db)
    minutes, hours = time_service.get_today_minutes(user_id)
    
    return TimeSummaryResponse(
        user_id=user_id,
        minutes=minutes,
        hours=hours,
        formatted=time_service.format_duration(minutes)
    )


@router.get("/{user_id}/time/week", response_model=TimeSummaryResponse)
async def get_week_time(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's total time worked in last 7 days."""
    time_service = TimeService(db)
    minutes, hours = time_service.get_week_minutes(user_id)
    
    return TimeSummaryResponse(
        user_id=user_id,
        minutes=minutes,
        hours=hours,
        formatted=time_service.format_duration(minutes)
    )


@router.get("/{user_id}/pay/unpaid", response_model=PaySummaryResponse)
async def get_unpaid_pay(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's unpaid time and pay amount."""
    pay_service = PayService(db)
    summary = pay_service.get_unpaid_summary(user_id)
    
    return PaySummaryResponse(
        user_id=user_id,
        session_minutes=summary['session_minutes'],
        adjustment_minutes=summary['adjustment_minutes'],
        total_minutes=summary['total_minutes'],
        total_hours=summary['total_hours'],
        hourly_rate=summary['hourly_rate'],
        pay_amount=summary['pay_amount']
    )


@router.post("/{user_id}/hourlyrate", response_model=HourlyRateResponse)
async def set_hourly_rate(
    user_id: str,
    request: HourlyRateRequest,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Set user's hourly rate."""
    user = db.query(User).filter(User.discord_id == user_id).first()
    if not user:
        user = User(discord_id=user_id, username=f"user_{user_id}", hourly_rate=request.hourly_rate)
        db.add(user)
    else:
        user.hourly_rate = request.hourly_rate
    
    db.commit()
    db.refresh(user)
    
    return HourlyRateResponse(
        user_id=user_id,
        hourly_rate=user.hourly_rate,
        message=f"Hourly rate set to ${user.hourly_rate}/hour"
    )


@router.get("/{user_id}/status")
async def get_user_status(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's clock in/out status and active session info."""
    time_service = TimeService(db)
    active_session = time_service.get_active_session(user_id)
    
    if active_session:
        elapsed = time_service.get_session_duration(active_session)
        return {
            "user_id": user_id,
            "status": "clocked_in",
            "session_id": active_session.id,
            "started_at": active_session.started_at.isoformat(),
            "elapsed_minutes": elapsed
        }
    else:
        return {
            "user_id": user_id,
            "status": "clocked_out"
        }
