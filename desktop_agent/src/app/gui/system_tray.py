"""System Tray Integration for Desktop Agent"""
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Signal


class SystemTrayManager:
    """Manage system tray icon and menu"""
    
    def __init__(self, parent_window, app):
        self.parent = parent_window
        self.app = app
        
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(parent_window)
        
        # Create menu
        self.create_menu()
        
        # Connect activation signal
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def create_menu(self):
        """Create context menu for system tray"""
        menu = QMenu()
        
        # Show action
        show_action = QAction("Show", self.parent)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)
        
        menu.addSeparator()
        
        # Status indicator (disabled)
        self.status_action = QAction("Status: Disconnected", self.parent)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)
        
        menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self.parent)
        exit_action.triggered.connect(self.on_exit_clicked)
        menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def update_status(self, connected: bool):
        """Update status in tray menu"""
        status = "Connected" if connected else "Disconnected"
        self.status_action.setText(f"Status: {status}")
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def show_window(self):
        """Show and raise the main window"""
        self.parent.showNormal()
        self.parent.raise_()
        self.parent.activateWindow()
    
    def on_exit_clicked(self):
        """Handle exit from tray menu"""
        is_clocked_in = getattr(self.parent, 'is_clocked_in', False)
        if ExitConfirmationDialog.confirm(self.parent, is_clocked_in):
            self.tray_icon.hide()
            QApplication.quit()
    
    def show_notification(self, title: str, message: str):
        """Show system tray notification"""
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            3000  # 3 seconds
        )
    
    def hide(self):
        """Hide tray icon"""
        self.tray_icon.hide()


class ExitConfirmationDialog:
    """Dialog to confirm exit and prevent accidental close"""
    
    @staticmethod
    def confirm(parent, is_clocked_in: bool = False) -> bool:
        """
        Show exit confirmation dialog
        Returns: True if user confirmed exit, False otherwise
        """
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Exit Agent?")
        
        if is_clocked_in:
            msg.setText("Warning: You are currently clocked in!")
            msg.setInformativeText(
                "Exiting will stop screenshot capture and heartbeat.\n"
                "Your session will remain active on the server.\n\n"
                "Are you sure you want to exit?"
            )
        else:
            msg.setText("Exit Time Tracker Agent?")
            msg.setInformativeText(
                "The agent will stop sending heartbeats.\n\n"
                "Are you sure you want to exit?"
            )
        
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        return msg.exec() == QMessageBox.Yes
