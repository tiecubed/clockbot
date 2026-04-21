"""Payroll router for payroll management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import verify_token
from app.services.pay_service import PayService
from app.services.time_service import TimeService
from app.schemas import (
    PayrollResponse, PayrollClearResponse,
    ActiveSessionsResponse, ActiveSessionUser,
    ManualAdjustmentRequest, ManualAdjustmentResponse
)

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.get("/unpaid", response_model=PayrollResponse)
async def get_unpaid_payroll(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all users with unpaid time."""
    pay_service = PayService(db)
    payroll = pay_service.get_all_unpaid_payroll()
    
    total_pay = sum(entry['pay_amount'] for entry in payroll)
    
    return PayrollResponse(
        users=[
            {
                "user_id": entry['user_id'],
                "username": entry['username'],
                "hourly_rate": entry['hourly_rate'],
                "session_minutes": entry['session_minutes'],
                "adjustment_minutes": entry['adjustment_minutes'],
                "total_hours": entry['total_hours'],
                "pay_amount": entry['pay_amount']
            }
            for entry in payroll
        ],
        total_pay=total_pay
    )


@router.post("/clear", response_model=PayrollClearResponse)
async def clear_payroll(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Mark all unpaid time as paid."""
    pay_service = PayService(db)
    user_ids = pay_service.mark_all_paid()
    
    return PayrollClearResponse(
        paid_user_ids=user_ids,
        message=f"Payroll cleared for {len(user_ids)} users"
    )


@router.get("/active", response_model=ActiveSessionsResponse)
async def get_active_sessions(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all currently clocked in users."""
    time_service = TimeService(db)
    pay_service = PayService(db)
    
    active_sessions = time_service.get_all_active_sessions()
    
    sessions_list = []
    for session in active_sessions:
        elapsed = time_service.get_session_duration(session)
        sessions_list.append(ActiveSessionUser(
            user_id=session.user_id,
            username=session.user.username if session.user else f"user_{session.user_id}",
            session_id=session.id,
            started_at=session.started_at,
            elapsed_minutes=elapsed
        ))
    
    return ActiveSessionsResponse(
        sessions=sessions_list,
        count=len(sessions_list)
    )


@router.post("/adjustments", response_model=ManualAdjustmentResponse)
async def add_manual_adjustment(
    request: ManualAdjustmentRequest,
    created_by: str,  # Discord ID of admin
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Add manual time adjustment for a user."""
    pay_service = PayService(db)
    
    adj = pay_service.add_manual_time(
        user_id=request.user_id,
        minutes=request.minutes,
        created_by=created_by,
        reason=request.reason
    )
    
    return ManualAdjustmentResponse(
        adjustment_id=adj.id,
        user_id=adj.user_id,
        minutes=adj.minutes,
        reason=adj.reason,
        created_at=adj.created_at
    )
