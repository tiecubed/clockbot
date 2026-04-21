"""Pydantic schemas for request/response models."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Agent schemas
class HeartbeatRequest(BaseModel):
    user_id: str
    version: str = "unknown"


class HeartbeatResponse(BaseModel):
    status: str
    timestamp: datetime


class AgentHealthResponse(BaseModel):
    user_id: str
    healthy: bool
    last_heartbeat: Optional[datetime] = None
    seconds_since_heartbeat: Optional[int] = None
    threshold_seconds: int


# Session schemas
class SessionStartRequest(BaseModel):
    user_id: str


class SessionStartResponse(BaseModel):
    session_id: int
    started_at: datetime
    message: str


class SessionEndResponse(BaseModel):
    session_id: int
    started_at: datetime
    ended_at: datetime
    duration_minutes: int
    duration_formatted: str
    message: str


class SessionResponse(BaseModel):
    id: int
    user_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    is_paid: bool
    duration_minutes: Optional[int]


# Screenshot schemas
class ScreenshotUploadResponse(BaseModel):
    screenshot_id: int
    session_id: int
    monitor_index: int
    uploaded_at: datetime
    message: str


class ScreenshotResponse(BaseModel):
    id: int
    session_id: int
    monitor_index: int
    file_path: str
    uploaded_at: datetime


# User/Time schemas
class TimeSummaryResponse(BaseModel):
    user_id: str
    minutes: int
    hours: float
    formatted: str


class PaySummaryResponse(BaseModel):
    user_id: str
    session_minutes: int
    adjustment_minutes: int
    total_minutes: int
    total_hours: float
    hourly_rate: float
    pay_amount: float


# Payroll schemas
class PayrollEntry(BaseModel):
    user_id: str
    username: str
    hourly_rate: float
    session_minutes: int
    adjustment_minutes: int
    total_hours: float
    pay_amount: float


class PayrollResponse(BaseModel):
    users: List[PayrollEntry]
    total_pay: float


class PayrollClearResponse(BaseModel):
    paid_user_ids: List[str]
    message: str


# Manual adjustment schemas
class ManualAdjustmentRequest(BaseModel):
    user_id: str
    minutes: int
    reason: Optional[str] = None


class ManualAdjustmentResponse(BaseModel):
    adjustment_id: int
    user_id: str
    minutes: int
    reason: Optional[str]
    created_at: datetime


# Hourly rate schemas
class HourlyRateRequest(BaseModel):
    hourly_rate: float = Field(gt=0)


class HourlyRateResponse(BaseModel):
    user_id: str
    hourly_rate: float
    message: str


# Active session schemas
class ActiveSessionUser(BaseModel):
    user_id: str
    username: str
    session_id: int
    started_at: datetime
    elapsed_minutes: int


class ActiveSessionsResponse(BaseModel):
    sessions: List[ActiveSessionUser]
    count: int
