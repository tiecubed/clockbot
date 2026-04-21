"""Desktop Agent Entry Point - Phase 6 GUI"""
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from gui.main_window import MainWindow
from gui.system_tray import SystemTrayManager
from utils.token_manager import TokenManager


def main():
    """Main entry point for Desktop Agent"""
    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Time Tracker Agent")
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    
    # Check for saved token
    token_data = TokenManager.load_token()
    
    # Create main window
    window = MainWindow(token_data)
    
    # Create system tray
    tray = SystemTrayManager(window, app)
    tray.tray_icon.show()
    
    # Connect window close to minimize to tray
    window.closeEvent = lambda event: handle_close(event, window, tray)
    
    # Show window initially
    window.show()
    
    print("=" * 60)
    print("Time Tracker Agent - Phase 6 GUI")
    print("=" * 60)
    print(f"Token status: {'Connected' if token_data else 'Not connected'}")
    print("Minimize to system tray to keep running")
    print("=" * 60)
    
    # Run application
    sys.exit(app.exec())


def handle_close(event, window, tray):
    """Handle window close - minimize to tray instead of exit"""
    from gui.system_tray import ExitConfirmationDialog
    
    is_clocked_in = getattr(window, 'is_clocked_in', False)
    
    # Show confirmation dialog
    if ExitConfirmationDialog.confirm(window, is_clocked_in):
        # User wants to exit completely
        tray.tray_icon.hide()
        event.accept()
    else:
        # User wants to minimize to tray
        event.ignore()
        window.hide()
        tray.show_notification(
            "Time Tracker Agent",
            "Running in system tray. Double-click to restore."
        )


if __name__ == '__main__':
    main()
