"""Screenshot Service for Desktop Agent"""
from PySide6.QtCore import QTimer, QObject, Signal
from datetime import datetime
import asyncio
import mss
from PIL import Image

from .config import config
from ..utils.image_processor import ImageProcessor


class ScreenshotService(QObject):
    """Service to capture and upload screenshots periodically"""
    
    screenshot_taken = Signal(str, int)  # Emits (timestamp, monitor_count)
    error_occurred = Signal(str)  # Emits error message
    countdown_updated = Signal(int)  # Emits seconds remaining
    
    def __init__(self, api_client, user_id: str, session_id: int = None):
        super().__init__()
        self.api_client = api_client
        self.user_id = user_id
        self.session_id = session_id
        self.timer = QTimer()
        self.timer.timeout.connect(self.take_screenshot)
        self.is_running = False
        self.image_processor = ImageProcessor(
            max_width=config.MAX_WIDTH,
            quality=config.JPEG_QUALITY
        )
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.seconds_remaining = config.SCREENSHOT_INTERVAL
    
    def start(self):
        """Start taking screenshots at configured interval"""
        if not self.is_running and self.session_id:
            self.timer.start(config.SCREENSHOT_INTERVAL * 1000)  # Convert to ms
            self.countdown_timer.start(1000)  # Update every second
            self.is_running = True
            self.seconds_remaining = config.SCREENSHOT_INTERVAL
            # Take first screenshot immediately
            self.take_screenshot()
    
    def stop(self):
        """Stop taking screenshots"""
        if self.is_running:
            self.timer.stop()
            self.countdown_timer.stop()
            self.is_running = False
    
    def set_session_id(self, session_id: int):
        """Update session ID when user clocks in"""
        self.session_id = session_id
    
    def update_countdown(self):
        """Update countdown timer"""
        self.seconds_remaining -= 1
        if self.seconds_remaining <= 0:
            self.seconds_remaining = config.SCREENSHOT_INTERVAL
        self.countdown_updated.emit(self.seconds_remaining)
    
    def take_screenshot(self):
        """Capture and upload screenshots"""
        if not self.session_id:
            self.error_occurred.emit("No active session - skipping screenshot")
            return
        
        try:
            # Run async screenshot in event loop
            asyncio.create_task(self._async_take_screenshot())
        except Exception as e:
            self.error_occurred.emit(f"Failed to queue screenshot: {str(e)}")
    
    async def _async_take_screenshot(self):
        """Async screenshot capture and upload"""
        try:
            # Capture all monitors using mss
            with mss.mss() as sct:
                monitor_count = len(sct.monitors) - 1  # Exclude "all" monitor
                
                for monitor_num in range(1, len(sct.monitors)):
                    # Capture specific monitor
                    screenshot = sct.grab(sct.monitors[monitor_num])
                    
                    # Convert to PIL Image
                    img = Image.frombytes(
                        "RGB",
                        screenshot.size,
                        screenshot.bgra,
                        "raw",
                        "BGRX"
                    )
                    
                    # Process image (resize, compress)
                    image_data = self.image_processor.process(img)
                    
                    # Upload to backend
                    await self.api_client.upload_screenshot(
                        user_id=self.user_id,
                        session_id=self.session_id,
                        monitor_index=monitor_num,
                        image_data=image_data
                    )
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.screenshot_taken.emit(timestamp, monitor_count)
                
        except Exception as e:
            self.error_occurred.emit(f"Screenshot failed: {str(e)}")
