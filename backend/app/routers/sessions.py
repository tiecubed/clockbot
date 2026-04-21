"""Session router for clock in/out endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.dependencies import verify_token
from app.services.health_service import HealthService
from app.services.time_service import TimeService
from app.models.session import Session as WorkSession
from app.models.user import User
from app.schemas import (
    SessionStartRequest, SessionStartResponse, 
    SessionEndResponse, SessionResponse
)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/start", response_model=SessionStartResponse)
async def start_session(
    request: SessionStartRequest,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Start a new work session (clock in). Checks agent health first."""
    # Check agent health
    health_service = HealthService(db)
    if not health_service.is_agent_healthy(request.user_id):
        raise HTTPException(
            status_code=400,
            detail="Desktop agent not healthy. Please ensure agent is running and connected."
        )
    
    # Check if user already has active session
    existing = db.query(WorkSession).filter(
        WorkSession.user_id == request.user_id,
        WorkSession.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already has an active session")
    
    # Ensure user exists
    user = db.query(User).filter(User.discord_id == request.user_id).first()
    if not user:
        user = User(discord_id=request.user_id, username=f"user_{request.user_id}", hourly_rate=0.0)
        db.add(user)
        db.flush()
    
    # Create session
    session = WorkSession(
        user_id=request.user_id,
        started_at=datetime.utcnow(),
        is_active=True,
        is_paid=False
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return SessionStartResponse(
        session_id=session.id,
        started_at=session.started_at,
        message="Session started successfully"
    )


@router.post("/{session_id}/end", response_model=SessionEndResponse)
async def end_session(
    session_id: int,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """End a work session (clock out)."""
    session = db.query(WorkSession).filter(
        WorkSession.id == session_id,
        WorkSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Active session not found")
    
    session.ended_at = datetime.utcnow()
    session.is_active = False
    db.commit()
    db.refresh(session)
    
    time_service = TimeService(db)
    
    return SessionEndResponse(
        session_id=session.id,
        started_at=session.started_at,
        ended_at=session.ended_at,
        duration_minutes=session.duration_minutes,
        duration_formatted=time_service.format_duration(session.duration_minutes),
        message="Session ended successfully"
    )


@router.get("/active/{user_id}", response_model=SessionResponse)
async def get_active_session(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's active session."""
    session = db.query(WorkSession).filter(
        WorkSession.user_id == user_id,
        WorkSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="No active session")
    
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        started_at=session.started_at,
        ended_at=session.ended_at,
        is_active=session.is_active,
        is_paid=session.is_paid,
        duration_minutes=None
    )
