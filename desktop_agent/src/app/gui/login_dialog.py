"""Login Dialog for OAuth Authentication"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
import asyncio

from ..core.auth import OAuthHandler
from ..utils.token_manager import TokenManager


class OAuthWorker(QThread):
    """Worker thread for OAuth flow"""
    
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.oauth = OAuthHandler()
    
    def run(self):
        """Run OAuth flow"""
        try:
            # Create new event loop for thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Complete login flow
            result = loop.run_until_complete(self.oauth.complete_login())
            
            if result:
                self.finished.emit(result)
            else:
                self.error.emit("Login timed out or was cancelled")
            
            loop.close()
        except Exception as e:
            self.error.emit(str(e))


class LoginDialog(QDialog):
    """Dialog for Discord OAuth login"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Discord")
        self.setMinimumSize(400, 200)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Time Tracker Agent")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Click 'Connect' to authenticate with Discord.\n"
            "Your browser will open to complete the login."
        )
        desc.setStyleSheet("color: #666;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Progress bar (hidden initially)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.hide()
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel("Ready to connect")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()
        layout.addWidget(self.status_label)
        
        # Connect button
        self.connect_button = QPushButton("Connect to Discord")
        self.connect_button.setStyleSheet(
            "QPushButton { padding: 10px; font-size: 14px; }"
        )
        self.connect_button.clicked.connect(self.start_oauth)
        layout.addWidget(self.connect_button)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)
    
    def start_oauth(self):
        """Start OAuth flow"""
        self.connect_button.setEnabled(False)
        self.connect_button.setText("Connecting...")
        self.progress.show()
        self.status_label.setText("Waiting for browser authentication...")
        self.status_label.show()
        
        # Start OAuth worker thread
        self.worker = OAuthWorker()
        self.worker.finished.connect(self.on_oauth_finished)
        self.worker.error.connect(self.on_oauth_error)
        self.worker.start()
    
    def on_oauth_finished(self, result: dict):
        """Handle successful OAuth"""
        # Save token
        TokenManager.save_token(
            token=result.get('token', ''),
            user_id=result.get('user_id', ''),
            username=result.get('username', '')
        )
        
        QMessageBox.information(
            self,
            "Success",
            f"Connected as {result.get('username', 'user')}!"
        )
        self.accept()
    
    def on_oauth_error(self, error: str):
        """Handle OAuth error"""
        self.progress.hide()
        self.status_label.hide()
        self.connect_button.setEnabled(True)
        self.connect_button.setText("Connect to Discord")
        
        QMessageBox.critical(
            self,
            "Connection Failed",
            f"Failed to connect: {error}"
        )
    
    def closeEvent(self, event):
        """Handle dialog close"""
        # Stop worker if running
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()
