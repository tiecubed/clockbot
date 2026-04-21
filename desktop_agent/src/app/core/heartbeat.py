"""Heartbeat Service for Desktop Agent"""
from PySide6.QtCore import QTimer, QObject, Signal
from datetime import datetime
import asyncio

from .config import config


class HeartbeatService(QObject):
    """Service to send periodic heartbeats to backend"""
    
    heartbeat_sent = Signal(str)  # Emits timestamp string
    error_occurred = Signal(str)  # Emits error message
    
    def __init__(self, api_client, user_id: str):
        super().__init__()
        self.api_client = api_client
        self.user_id = user_id
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_heartbeat)
        self.is_running = False
        self.version = "1.0.0"
    
    def start(self):
        """Start sending heartbeats at configured interval"""
        if not self.is_running:
            self.timer.start(config.HEARTBEAT_INTERVAL * 1000)  # Convert to ms
            self.is_running = True
            # Send first heartbeat immediately
            self.send_heartbeat()
    
    def stop(self):
        """Stop sending heartbeats"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
    
    def send_heartbeat(self):
        """Send heartbeat to backend"""
        try:
            # Run async heartbeat in event loop
            asyncio.create_task(self._async_send_heartbeat())
        except Exception as e:
            self.error_occurred.emit(f"Failed to queue heartbeat: {str(e)}")
    
    async def _async_send_heartbeat(self):
        """Async heartbeat sender"""
        try:
            result = await self.api_client.send_heartbeat(self.user_id, self.version)
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.heartbeat_sent.emit(timestamp)
        except Exception as e:
            self.error_occurred.emit(f"Heartbeat failed: {str(e)}")
