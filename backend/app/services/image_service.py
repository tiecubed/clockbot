"""Image service for processing and storing screenshots."""
import os
import io
from datetime import datetime
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session

from app.config import settings
from app.models.screenshot import Screenshot


class ImageService:
    """Service for processing and storing screenshot images."""
    
    def __init__(self, db: Session):
        self.db = db
        self.max_width = settings.SCREENSHOT_MAX_WIDTH
        self.quality = settings.SCREENSHOT_QUALITY
        self.storage_dir = settings.SCREENSHOT_DIR
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def process_image(self, image_bytes: bytes) -> bytes:
        """Process image: convert to RGB, resize if >1920px, compress to JPEG quality 70."""
        img = Image.open(io.BytesIO(image_bytes))
        
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        if img.width > self.max_width:
            ratio = self.max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((self.max_width, new_height), Image.LANCZOS)
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=self.quality, optimize=True)
        return output.getvalue()
    
    def save_screenshot(self, user_id: str, session_id: int, monitor_index: int, image_bytes: bytes) -> Screenshot:
        """Process and save screenshot to filesystem and database."""
        processed_bytes = self.process_image(image_bytes)
        
        user_dir = os.path.join(self.storage_dir, str(user_id))
        session_dir = os.path.join(user_dir, str(session_id))
        os.makedirs(session_dir, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_monitor{monitor_index}.jpg"
        filepath = os.path.join(session_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(processed_bytes)
        
        screenshot = Screenshot(session_id=session_id, monitor_index=monitor_index, file_path=filepath)
        self.db.add(screenshot)
        self.db.commit()
        
        return screenshot
    
    def get_screenshot(self, screenshot_id: int) -> Optional[Screenshot]:
        return self.db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()
    
    def get_session_screenshots(self, session_id: int) -> list:
        return self.db.query(Screenshot).filter(Screenshot.session_id == session_id).order_by(Screenshot.uploaded_at).all()
    
    def delete_screenshot(self, screenshot_id: int) -> bool:
        screenshot = self.get_screenshot(screenshot_id)
        if not screenshot:
            return False
        if os.path.exists(screenshot.file_path):
            os.remove(screenshot.file_path)
        self.db.delete(screenshot)
        self.db.commit()
        return True
    
    def get_image_bytes(self, screenshot: Screenshot) -> Optional[bytes]:
        if not os.path.exists(screenshot.file_path):
            return None
        with open(screenshot.file_path, 'rb') as f:
            return f.read()
