"""
Main Window UI for Enhanced Folder Copier
"""

import os
import logging
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QGridLayout, QProgressBar,
                             QMessageBox, QDialog, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPainter, QPen, QIcon, QPixmap

from ui.settings_dialog import SettingsDialog
from ui.password_dialog import PasswordDialog
from core.copy_worker import CopyWorker
from core.settings_manager import SettingsManager
from utils.network_checker import NetworkChecker
from utils.styles import ModernStyles


class StatusIndicator(QWidget):
    """Custom widget for network status indicator"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self._status = "offline"  # "online", "offline", "checking"

    def set_status(self, status):
        """Set the status: 'online', 'offline', or 'checking'"""
        self._status = status
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set color based on status
        if self._status == "online":
            color = Qt.GlobalColor.green
        elif self._status == "offline":
            color = Qt.GlobalColor.red
        else:  # checking
            color = Qt.GlobalColor.yellow

        painter.setBrush(color)
        painter.setPen(QPen(Qt.GlobalColor.darkGray, 1))
        painter.drawEllipse(2, 2, 12, 12)


class FolderCopierApp(QMainWindow):
    """Main application window with modern design"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Folder Copier")
        self.setFixedSize(650, 450)

        # Initialize components
        self.settings_manager = SettingsManager()
        self.network_checker = NetworkChecker()
        self.copy_worker = None
        self.is_authenticated = False

        # Load settings
        self.settings = self.settings_manager.load_settings()

        self.setup_ui()
        self.setup_network_timer()
        self.set_custom_icon()

        # Initial network check
        self.check_network_status()

    def set_custom_icon(self):
        """Set custom folder emoji icon for the window"""
        try:
            # Create a pixmap with the folder emoji
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Set font for emoji
            font = QFont("Segoe UI Emoji", 24)
            painter.setFont(font)

            # Draw the folder emoji
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "📁")
            painter.end()

            # Set the icon
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        except Exception as e:
            logging.warning(f"Could not set custom icon: {str(e)}")
            # Fallback - no icon is better than Windows default
            pass

    def setup_ui(self):
        """Setup the modern user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Apply modern styles
        self.setStyleSheet(ModernStyles.get_main_window_style())

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(main_layout)

        # Header
        self.create_header(main_layout)

        # Main content area
        self.create_content_area(main_layout)

        # Progress section
        self.create_progress_section(main_layout)

        # Action buttons
        self.create_action_buttons(main_layout)

        # Update UI with current settings
        self.update_ui_display()

    def create_header(self, parent_layout):
        """Create the header section"""
        header_layout = QHBoxLayout()

        # Title with folder icon
        title_label = QLabel("📁 Enhanced Folder Copier")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1f2937; margin-bottom: 10px;")

        # Logout button (shown only when authenticated)
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setStyleSheet(ModernStyles.get_logout_button_style())
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setVisible(False)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)

        parent_layout.addLayout(header_layout)

    def create_content_area(self, parent_layout):
        """Create the main content area"""
        content_frame = QFrame()
        content_frame.setStyleSheet(ModernStyles.get_content_frame_style())
        content_layout = QGridLayout()
        content_layout.setSpacing(15)
        content_frame.setLayout(content_layout)

        # Source folder info
        source_icon_label = QLabel("📂")
        source_icon_label.setFont(QFont("Segoe UI", 14))
        source_text_label = QLabel("Source Folder:")
        source_text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        content_layout.addWidget(source_icon_label, 0, 0)
        content_layout.addWidget(source_text_label, 0, 1)

        self.source_label = QLabel("Not configured")
        self.source_label.setStyleSheet(ModernStyles.get_path_label_style())
        content_layout.addWidget(self.source_label, 0, 2, 1, 2)

        # Destination folder info
        dest_icon_label = QLabel("📋")
        dest_icon_label.setFont(QFont("Segoe UI", 14))
        dest_text_label = QLabel("Destination Folder:")
        dest_text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        content_layout.addWidget(dest_icon_label, 1, 0)
        content_layout.addWidget(dest_text_label, 1, 1)

        self.destination_label = QLabel("Not configured")
        self.destination_label.setStyleSheet(ModernStyles.get_path_label_style())
        content_layout.addWidget(self.destination_label, 1, 2, 1, 2)

        # Folder type display
        type_icon_label = QLabel("📍")
        type_icon_label.setFont(QFont("Segoe UI", 14))
        type_text_label = QLabel("Copy Type:")
        type_text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        content_layout.addWidget(type_icon_label, 2, 0)
        content_layout.addWidget(type_text_label, 2, 1)

        self.type_label = QLabel("Local")
        self.type_label.setStyleSheet(ModernStyles.get_info_label_style())
        content_layout.addWidget(self.type_label, 2, 2, 1, 2)

        # Network status (only shown for network type)
        self.network_icon_label = QLabel("🌐")
        self.network_icon_label.setFont(QFont("Segoe UI", 14))
        self.network_text_label = QLabel("Network Status:")
        self.network_text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        self.network_status_widget = QWidget()
        network_layout = QHBoxLayout()
        network_layout.setContentsMargins(0, 0, 0, 0)

        self.status_indicator = StatusIndicator()
        self.network_status_text = QLabel("Checking...")
        self.network_status_text.setStyleSheet("color: #6b7280; font-weight: 500;")

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(30, 30)
        self.refresh_btn.setStyleSheet(ModernStyles.get_refresh_button_style())
        self.refresh_btn.clicked.connect(self.check_network_status)

        network_layout.addWidget(self.status_indicator)
        network_layout.addWidget(self.network_status_text)
        network_layout.addStretch()
        network_layout.addWidget(self.refresh_btn)
        self.network_status_widget.setLayout(network_layout)

        content_layout.addWidget(self.network_icon_label, 3, 0)
        content_layout.addWidget(self.network_text_label, 3, 1)
        content_layout.addWidget(self.network_status_widget, 3, 2, 1, 2)

        # Auto-close option
        auto_icon_label = QLabel("🔄")
        auto_icon_label.setFont(QFont("Segoe UI", 14))
        auto_text_label = QLabel("Auto Close:")
        auto_text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        content_layout.addWidget(auto_icon_label, 4, 0)
        content_layout.addWidget(auto_text_label, 4, 1)

        self.auto_close_label = QLabel("Disabled")
        self.auto_close_label.setStyleSheet(ModernStyles.get_info_label_style())
        content_layout.addWidget(self.auto_close_label, 4, 2, 1, 2)

        parent_layout.addWidget(content_frame)

    def create_progress_section(self, parent_layout):
        """Create the progress section"""
        progress_frame = QFrame()
        progress_frame.setStyleSheet(ModernStyles.get_progress_frame_style())
        progress_layout = QVBoxLayout()
        progress_frame.setLayout(progress_layout)

        # Status label
        self.status_label = QLabel("Ready to copy")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #374151; font-weight: 500; margin-bottom: 10px;")
        progress_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(ModernStyles.get_progress_bar_style())
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        progress_layout.addWidget(self.progress_bar)

        parent_layout.addWidget(progress_frame)

    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Copy button
        self.copy_button = QPushButton("🚀 Start Copy")
        self.copy_button.setStyleSheet(ModernStyles.get_primary_button_style())
        self.copy_button.clicked.connect(self.copy_folder)

        # Settings button
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setStyleSheet(ModernStyles.get_secondary_button_style())
        self.settings_button.clicked.connect(self.open_settings)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.settings_button)

        parent_layout.addLayout(button_layout)

    def setup_network_timer(self):
        """Setup timer for periodic network checks"""
        self.network_timer = QTimer()
        self.network_timer.timeout.connect(self.check_network_status)
        self.network_timer.start(30000)  # Check every 30 seconds

    def update_ui_display(self):
        """Update UI elements with current settings"""
        settings = self.settings

        # Update path labels
        source_path = settings.get('source_path', '')
        dest_path = settings.get('destination_path', '')

        self.source_label.setText(source_path if source_path else 'Not configured')
        self.destination_label.setText(dest_path if dest_path else 'Not configured')

        # Update type label
        folder_type = settings.get('folder_type', 'local')
        self.type_label.setText("Network Folder" if folder_type == 'network' else "Local Folder")

        # Show/hide network status based on type
        is_network = folder_type == 'network'
        self.network_icon_label.setVisible(is_network)
        self.network_text_label.setVisible(is_network)
        self.network_status_widget.setVisible(is_network)

        # Update auto-close label
        auto_close = settings.get('auto_close', False)
        self.auto_close_label.setText("Enabled" if auto_close else "Disabled")
        self.auto_close_label.setStyleSheet(
            ModernStyles.get_success_label_style() if auto_close
            else ModernStyles.get_info_label_style()
        )

    def check_network_status(self):
        """Check network connectivity status"""
        if self.settings.get('folder_type') != 'network':
            return

        self.status_indicator.set_status("checking")
        self.network_status_text.setText("Checking...")

        # Check connectivity
        network_ip = self.settings.get('network_ip', '127.0.0.1')

        try:
            is_connected = self.network_checker.ping_host(network_ip, timeout=3)

            if is_connected:
                self.status_indicator.set_status("online")
                self.network_status_text.setText("Connected")
                self.network_status_text.setStyleSheet("color: #10b981; font-weight: 500;")
            else:
                self.status_indicator.set_status("offline")
                self.network_status_text.setText("Disconnected")
                self.network_status_text.setStyleSheet("color: #ef4444; font-weight: 500;")

        except Exception as e:
            logging.error(f"Network check failed: {str(e)}")
            self.status_indicator.set_status("offline")
            self.network_status_text.setText("Error")
            self.network_status_text.setStyleSheet("color: #ef4444; font-weight: 500;")

    def copy_folder(self):
        """Start the folder copying process"""
        # Validate settings
        source_path = self.settings.get('source_path', '')
        destination_path = self.settings.get('destination_path', '')

        if not source_path or not destination_path:
            QMessageBox.warning(self, "Configuration Required",
                                "Please configure source and destination folders in settings.")
            return

        # Validate paths
        if not os.path.exists(source_path):
            QMessageBox.critical(self, "Error", f"Source folder does not exist:\n{source_path}")
            return

        if os.path.abspath(source_path) == os.path.abspath(destination_path):
            QMessageBox.critical(self, "Error", "Source and destination cannot be the same folder.")
            return

        # Network check for network folders
        if self.settings.get('folder_type') == 'network':
            network_ip = self.settings.get('network_ip', '127.0.0.1')
            try:
                if not self.network_checker.ping_host(network_ip, timeout=5):
                    QMessageBox.critical(self, "Network Error",
                                         f"Cannot connect to network location: {network_ip}")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Network Error",
                                     f"Network check failed: {str(e)}")
                return

        # Start copying
        self.start_copy_operation(source_path, destination_path)

    def start_copy_operation(self, source_path, destination_path):
        """Start the copy operation in a worker thread"""
        self.copy_worker = CopyWorker(source_path, destination_path)
        self.copy_worker.finished.connect(self.on_copy_finished)
        self.copy_worker.progress_update.connect(self.on_progress_update)

        # Update UI for copying state
        self.copy_button.setEnabled(False)
        self.settings_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Preparing to copy...")

        self.copy_worker.start()

    def on_copy_finished(self, success, message):
        """Handle copy operation completion"""
        self.copy_button.setEnabled(True)
        self.settings_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            self.status_label.setText("✅ Copy completed successfully!")
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.exec()

            # Auto-close if enabled
            if self.settings.get('auto_close', False):
                logging.info("Auto-closing application after successful copy")
                self.close()
        else:
            self.status_label.setText("❌ Copy failed")
            QMessageBox.critical(self, "Copy Error", message)

    def on_progress_update(self, message):
        """Update progress status"""
        self.status_label.setText(message)

    def open_settings(self):
        """Open settings dialog with authentication if needed"""
        if not self.is_authenticated:
            if not self.authenticate_user():
                return

        settings_dialog = SettingsDialog(self.settings_manager, self)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload settings and update UI
            self.settings = self.settings_manager.load_settings()
            self.update_ui_display()
            logging.info("Settings updated successfully")

    def authenticate_user(self):
        """Authenticate user with password"""
        password_dialog = PasswordDialog(self)

        if password_dialog.exec() == QDialog.DialogCode.Accepted:
            entered_password = password_dialog.get_password()
            stored_password = self.settings.get('password', 'password123')

            if entered_password == stored_password:
                self.is_authenticated = True
                self.logout_btn.setVisible(True)
                logging.info("User authenticated successfully")
                return True
            else:
                QMessageBox.critical(self, "Authentication Failed", "Incorrect password.")
                logging.warning("Authentication failed - incorrect password")
                return False
        return False

    def logout(self):
        """Logout user"""
        self.is_authenticated = False
        self.logout_btn.setVisible(False)
        logging.info("User logged out")

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Stop worker thread if running
            if self.copy_worker and self.copy_worker.isRunning():
                self.copy_worker.terminate_safely()

            # Stop network timer
            if hasattr(self, 'network_timer'):
                self.network_timer.stop()

            logging.info("Application closing gracefully")
            event.accept()

        except Exception as e:
            logging.error(f"Error during application close: {str(e)}")
            event.accept()