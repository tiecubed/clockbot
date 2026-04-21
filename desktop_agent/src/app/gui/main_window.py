"""Main Window for Desktop Agent"""
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

from ..core.config import config
from ..utils.token_manager import TokenManager


class StatusWidget(QWidget):
    """Widget displaying agent status information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self._start_refresh_timer()
    
    def setup_ui(self):
        """Setup the status display UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Connection status
        connection_frame = QFrame()
        connection_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        conn_layout = QHBoxLayout(connection_frame)
        
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: gray; font-size: 24px;")
        
        self.status_text = QLabel("Disconnected")
        self.status_text.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        conn_layout.addWidget(self.status_indicator)
        conn_layout.addWidget(self.status_text)
        conn_layout.addStretch()
        
        layout.addWidget(connection_frame)
        
        # User info
        self.username_label = QLabel("User: Not connected")
        self.username_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(self.username_label)
        
        # Status details frame
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.StyledPanel)
        details_layout = QVBoxLayout(details_frame)
        
        # Last heartbeat
        self.heartbeat_label = QLabel("Last heartbeat: --")
        self.heartbeat_label.setStyleSheet("font-family: monospace; font-size: 12px;")
        details_layout.addWidget(self.heartbeat_label)
        
        # Last screenshot
        self.screenshot_label = QLabel("Last screenshot: --")
        self.screenshot_label.setStyleSheet("font-family: monospace; font-size: 12px;")
        details_layout.addWidget(self.screenshot_label)
        
        # Next screenshot countdown
        self.countdown_label = QLabel("Next screenshot: --")
        self.countdown_label.setStyleSheet("font-family: monospace; font-size: 12px; color: #0066cc;")
        details_layout.addWidget(self.countdown_label)
        
        layout.addWidget(details_frame)
        
        # Info message
        info_label = QLabel("Leave this window open while clocked in")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _start_refresh_timer(self):
        """Start timer for UI refresh"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)  # Update every second
    
    def update_connection(self, connected: bool, username: str = ""):
        """Update connection status display"""
        if connected:
            self.status_indicator.setStyleSheet("color: #00aa00; font-size: 24px;")
            self.status_text.setText("Connected")
            self.status_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #00aa00;")
        else:
            self.status_indicator.setStyleSheet("color: #cc0000; font-size: 24px;")
            self.status_text.setText("Disconnected")
            self.status_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #cc0000;")
        
        if username:
            self.username_label.setText(f"User: {username}")
        else:
            self.username_label.setText("User: Not connected")
    
    def update_heartbeat(self, timestamp: str):
        """Update last heartbeat display"""
        self.heartbeat_label.setText(f"Last heartbeat: {timestamp}")
    
    def update_screenshot(self, timestamp: str, monitor_count: int = 1):
        """Update last screenshot display"""
        self.screenshot_label.setText(f"Last screenshot: {timestamp} ({monitor_count} monitor(s))")
    
    def update_countdown(self, seconds_remaining: int):
        """Update countdown display"""
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        self.countdown_label.setText(f"Next screenshot: {minutes}:{seconds:02d}")
    
    def refresh(self):
        """Called every second - placeholder for countdown updates"""
        pass


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, token_data: dict = None):
        super().__init__()
        self.token_data = token_data or {}
        self.is_clocked_in = False
        
        self.setWindowTitle("Time Tracker Agent")
        self.setMinimumSize(450, 350)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Status widget
        self.status_widget = StatusWidget()
        layout.addWidget(self.status_widget)
        
        # Button area
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Connect to Discord")
        self.login_button.clicked.connect(self.show_login)
        
        self.logout_button = QPushButton("Disconnect")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setEnabled(False)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.logout_button)
        
        layout.addLayout(button_layout)
        
        # Initialize status
        self.update_status_from_token()
    
    def update_status_from_token(self):
        """Update UI based on saved token"""
        if self.token_data:
            username = self.token_data.get('username', 'Unknown')
            self.status_widget.update_connection(True, username)
            self.login_button.setEnabled(False)
            self.logout_button.setEnabled(True)
        else:
            self.status_widget.update_connection(False)
    
    def show_login(self):
        """Show login dialog"""
        from .login_dialog import LoginDialog
        dialog = LoginDialog(self)
        if dialog.exec():
            # Reload token after login
            self.token_data = TokenManager.load_token()
            self.update_status_from_token()
    
    def logout(self):
        """Clear token and reset UI"""
        reply = QMessageBox.question(
            self, "Logout",
            "Are you sure you want to disconnect?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            TokenManager.clear_token()
            self.token_data = {}
            self.update_status_from_token()
            self.login_button.setEnabled(True)
            self.logout_button.setEnabled(False)
    
    def closeEvent(self, event):
        """Handle window close - show confirmation"""
        from .system_tray import ExitConfirmationDialog
        
        if ExitConfirmationDialog.confirm(self, self.is_clocked_in):
            event.accept()
        else:
            event.ignore()
            # Minimize to tray if available
            self.hide()
