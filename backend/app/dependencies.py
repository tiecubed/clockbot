"""FastAPI dependencies for authentication and database."""
from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.config import settings


def verify_token(token: Optional[str] = Header(None)) -> str:
    """Verify the shared secret token."""
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")
    
    if token != settings.SHARED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return token


def get_db_session():
    """Get database session dependency."""
    return get_db
