"""Screenshots router for upload endpoint."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.dependencies import verify_token
from app.services.image_service import ImageService
from app.schemas import ScreenshotUploadResponse, ScreenshotResponse

router = APIRouter(prefix="/screenshots", tags=["screenshots"])


@router.post("/upload", response_model=ScreenshotUploadResponse)
async def upload_screenshot(
    user_id: str = Form(...),
    session_id: int = Form(...),
    monitor_index: int = Form(...),
    image: UploadFile = File(...),
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Upload screenshot from desktop agent."""
    # Validate image type
    if not image.content_type or not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image bytes
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")
    
    # Process and save screenshot
    image_service = ImageService(db)
    
    try:
        screenshot = image_service.save_screenshot(
            user_id=user_id,
            session_id=session_id,
            monitor_index=monitor_index,
            image_bytes=image_bytes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process screenshot: {str(e)}")
    
    return ScreenshotUploadResponse(
        screenshot_id=screenshot.id,
        session_id=screenshot.session_id,
        monitor_index=screenshot.monitor_index,
        uploaded_at=screenshot.uploaded_at,
        message="Screenshot uploaded successfully"
    )


@router.get("/session/{session_id}", response_model=list[ScreenshotResponse])
async def get_session_screenshots(
    session_id: int,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all screenshots for a session."""
    image_service = ImageService(db)
    screenshots = image_service.get_session_screenshots(session_id)
    
    return [
        ScreenshotResponse(
            id=s.id,
            session_id=s.session_id,
            monitor_index=s.monitor_index,
            file_path=s.file_path,
            uploaded_at=s.uploaded_at
        )
        for s in screenshots
    ]
