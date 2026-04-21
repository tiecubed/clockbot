"""Agent router for heartbeat and health endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.dependencies import verify_token
from app.services.health_service import HealthService
from app.schemas import HeartbeatRequest, HeartbeatResponse, AgentHealthResponse

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/heartbeat", response_model=HeartbeatResponse)
async def agent_heartbeat(
    request: HeartbeatRequest,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Receive heartbeat from desktop agent."""
    health_service = HealthService(db)
    health_service.update_heartbeat(request.user_id, request.version)
    
    return HeartbeatResponse(
        status="ok",
        timestamp=datetime.utcnow()
    )


@router.get("/{user_id}/health", response_model=AgentHealthResponse)
async def check_agent_health(
    user_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Check if agent is healthy (heartbeat within last 90 seconds)."""
    health_service = HealthService(db)
    
    is_healthy = health_service.is_agent_healthy(user_id)
    status = health_service.get_agent_status(user_id)
    seconds_since = health_service.get_seconds_since_heartbeat(user_id)
    
    return AgentHealthResponse(
        user_id=user_id,
        healthy=is_healthy,
        last_heartbeat=status.last_heartbeat if status else None,
        seconds_since_heartbeat=seconds_since,
        threshold_seconds=health_service.threshold_seconds
    )
