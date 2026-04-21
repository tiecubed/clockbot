"""Desktop Agent Entry Point - Phase 7 Core Services"""
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from gui.main_window import MainWindow
from gui.system_tray import SystemTrayManager
from utils.token_manager import TokenManager
from core.api_client import BackendAPIClient
from core.heartbeat import HeartbeatService
from core.screenshot import ScreenshotService


class TimeTrackerApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = None
        self.window = None
        self.tray = None
        self.api_client = None
        self.heartbeat_service = None
        self.screenshot_service = None
        self.user_id = None
        self.session_id = None
    
    def initialize(self):
        """Initialize the application"""
        # Create Qt application
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Time Tracker Agent")
        self.app.setQuitOnLastWindowClosed(False)
        
        # Load token
        token_data = TokenManager.load_token()
        if token_data:
            self.user_id = token_data.get('user_id')
        
        # Create API client
        self.api_client = BackendAPIClient(
            token=token_data.get('token') if token_data else None
        )
        
        # Create main window
        self.window = MainWindow(token_data)
        self.window.closeEvent = lambda event: self.handle_close(event)
        
        # Connect clock status changes
        self.window.clock_status_changed.connect(self.on_clock_status_changed)
        
        # Create services if we have a user
        if self.user_id:
            self.create_services()
        
        # Create system tray
        self.tray = SystemTrayManager(self.window, self.app)
        self.tray.tray_icon.show()
        
        return True
    
    def create_services(self):
        """Create heartbeat and screenshot services"""
        # Heartbeat service
        self.heartbeat_service = HeartbeatService(self.api_client, self.user_id)
        self.heartbeat_service.heartbeat_sent.connect(self.on_heartbeat_sent)
        self.heartbeat_service.error_occurred.connect(self.on_service_error)
        
        # Screenshot service
        self.screenshot_service = ScreenshotService(self.api_client, self.user_id)
        self.screenshot_service.screenshot_taken.connect(self.on_screenshot_taken)
        self.screenshot_service.countdown_updated.connect(self.on_countdown_updated)
        self.screenshot_service.error_occurred.connect(self.on_service_error)
        
        # Start heartbeat immediately (agent should be healthy)
        self.heartbeat_service.start()
    
    def on_clock_status_changed(self, is_clocked_in: bool, session_id: int = None):
        """Handle clock in/out status changes"""
        self.window.is_clocked_in = is_clocked_in
        
        if is_clocked_in:
            # User clocked in - start screenshot service
            self.session_id = session_id
            if self.screenshot_service:
                self.screenshot_service.set_session_id(session_id)
                self.screenshot_service.start()
                self.tray.show_notification(
                    "Time Tracker",
                    f"Clocked in! Screenshots enabled (session {session_id})"
                )
        else:
            # User clocked out - stop screenshot service
            self.session_id = None
            if self.screenshot_service:
                self.screenshot_service.stop()
                self.tray.show_notification(
                    "Time Tracker",
                    "Clocked out! Screenshots stopped"
                )
    
    def on_heartbeat_sent(self, timestamp: str):
        """Update UI when heartbeat sent"""
        self.window.status_widget.update_heartbeat(timestamp)
        self.tray.update_status(connected=True)
    
    def on_screenshot_taken(self, timestamp: str, monitor_count: int):
        """Update UI when screenshot taken"""
        self.window.status_widget.update_screenshot(timestamp, monitor_count)
    
    def on_countdown_updated(self, seconds_remaining: int):
        """Update countdown display"""
        self.window.status_widget.update_countdown(seconds_remaining)
    
    def on_service_error(self, error_message: str):
        """Handle service errors"""
        print(f"Service error: {error_message}")
    
    def handle_close(self, event):
        """Handle window close"""
        from gui.system_tray import ExitConfirmationDialog
        
        is_clocked_in = getattr(self.window, 'is_clocked_in', False)
        
        if ExitConfirmationDialog.confirm(self.window, is_clocked_in):
            # Stop services
            if self.heartbeat_service:
                self.heartbeat_service.stop()
            if self.screenshot_service:
                self.screenshot_service.stop()
            
            self.tray.tray_icon.hide()
            event.accept()
        else:
            event.ignore()
            self.window.hide()
            self.tray.show_notification(
                "Time Tracker Agent",
                "Running in system tray. Double-click to restore."
            )
    
    def run(self):
        """Run the application"""
        self.window.show()
        
        print("=" * 60)
        print("Time Tracker Agent - Phase 7 Core Services")
        print("=" * 60)
        print(f"User: {self.user_id or 'Not connected'}")
        print(f"Heartbeat: Every {30}s (maintains healthy status)")
        print(f"Screenshots: Every {300}s (only while clocked in)")
        print("=" * 60)
        
        return self.app.exec()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.api_client:
            import asyncio
            asyncio.get_event_loop().run_until_complete(self.api_client.close())


def main():
    """Main entry point"""
    from core.config import config
    
    # Check configuration
    if not config.is_configured:
        print("❌ Agent not configured!")
        print("Please set BACKEND_URL and SHARED_TOKEN in .env")
        sys.exit(1)
    
    # Create and run app
    app = TimeTrackerApp()
    if not app.initialize():
        sys.exit(1)
    
    try:
        sys.exit(app.run())
    finally:
        app.cleanup()


if __name__ == '__main__':
    main()
