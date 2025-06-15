"""
Main Window Class - Enhanced Folder Copier
Modern GUI with pastel colors and enhanced functionality
"""

import os
import logging
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QFrame, QGridLayout,
                            QProgressBar, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

from settings_dialog import SettingsDialog
from password_dialog import PasswordDialog
from copy_worker import CopyWorker
from settings_manager import SettingsManager
from network_checker import NetworkChecker


class FolderCopierApp(QMainWindow):
    """Main application window with modern design"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Folder Copier")
        self.setFixedSize(700, 400)

        # Initialize managers
        self.settings_manager = SettingsManager()
        self.network_checker = NetworkChecker()

        # Initialize variables
        self.is_authenticated = False
        self.copy_worker = None
        self.network_status_timer = QTimer()

        # Load settings
        self.settings = self.settings_manager.load_settings()

        self.setup_ui()
        self.load_initial_data()
        self.setup_network_monitoring()

    def setup_ui(self):
        """Setup the modern user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(main_layout)

        # Header section
        self.create_header_section(main_layout)

        # Path information section
        self.create_path_section(main_layout)

        # Status section
        self.create_status_section(main_layout)

        # Progress section
        self.create_progress_section(main_layout)

        # Action buttons section
        self.create_action_section(main_layout)

        # Footer section
        self.create_footer_section(main_layout)

    def create_header_section(self, main_layout):
        """Create header with title and auth status"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout()
        header_frame.setLayout(header_layout)

        # Title
        title_label = QLabel("Enhanced Folder Copier")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Auth status
        auth_layout = QVBoxLayout()
        self.auth_status_label = QLabel("🔒 Not Authenticated")
        self.auth_status_label.setObjectName("authLabel")
        self.auth_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.setVisible(False)
        self.logout_button.clicked.connect(self.logout)

        auth_layout.addWidget(self.auth_status_label)
        auth_layout.addWidget(self.logout_button)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(auth_layout)

        main_layout.addWidget(header_frame)

    def create_path_section(self, main_layout):
        """Create path information section"""
        path_frame = QFrame()
        path_frame.setObjectName("pathFrame")
        path_layout = QGridLayout()
        path_layout.setSpacing(15)
        path_frame.setLayout(path_layout)

        # Source path
        source_icon = QLabel("📁")
        source_icon.setObjectName("iconLabel")
        path_layout.addWidget(source_icon, 0, 0)
        path_layout.addWidget(QLabel("Source Folder:"), 0, 1)

        self.source_label = QLabel("Not selected")
        self.source_label.setObjectName("pathLabel")
        path_layout.addWidget(self.source_label, 0, 2)

        # Destination path
        dest_icon = QLabel("📤")
        dest_icon.setObjectName("iconLabel")
        path_layout.addWidget(dest_icon, 1, 0)
        path_layout.addWidget(QLabel("Destination:"), 1, 1)

        self.destination_label = QLabel("Not selected")
        self.destination_label.setObjectName("pathLabel")
        path_layout.addWidget(self.destination_label, 1, 2)

        # Folder type
        type_icon = QLabel("🌐" if self.settings.get('folder_type') == 'network' else "💻")
        type_icon.setObjectName("iconLabel")
        path_layout.addWidget(type_icon, 2, 0)
        path_layout.addWidget(QLabel("Connection Type:"), 2, 1)

        self.folder_type_label = QLabel(self.settings.get('folder_type', 'local').title())
        self.folder_type_label.setObjectName("pathLabel")
        path_layout.addWidget(self.folder_type_label, 2, 2)

        main_layout.addWidget(path_frame)

    def create_status_section(self, main_layout):
        """Create network status section"""
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        status_frame.setLayout(status_layout)

        # Network status (only show if network mode)
        self.network_status_widget = QWidget()
        network_layout = QHBoxLayout()
        self.network_status_widget.setLayout(network_layout)

        network_layout.addWidget(QLabel("Network Status:"))

        self.network_indicator = QLabel("●")
        self.network_indicator.setObjectName("networkIndicator")
        network_layout.addWidget(self.network_indicator)

        self.network_status_label = QLabel("Checking...")
        network_layout.addWidget(self.network_status_label)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.setToolTip("Refresh network status")
        self.refresh_button.clicked.connect(self.check_network_status)
        network_layout.addWidget(self.refresh_button)

        network_layout.addStretch()

        status_layout.addWidget(self.network_status_widget)

        # Auto-close option
        self.auto_close_widget = QWidget()
        auto_close_layout = QHBoxLayout()
        self.auto_close_widget.setLayout(auto_close_layout)

        auto_close_layout.addStretch()
        auto_close_layout.addWidget(QLabel("Auto-close after copy:"))

        self.auto_close_indicator = QLabel("✅" if self.settings.get('auto_close', False) else "❌")
        auto_close_layout.addWidget(self.auto_close_indicator)

        status_layout.addWidget(self.auto_close_widget)

        main_layout.addWidget(status_frame)

    def create_progress_section(self, main_layout):
        """Create progress section"""
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_layout = QVBoxLayout()
        progress_frame.setLayout(progress_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        progress_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready to copy")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.status_label)

        main_layout.addWidget(progress_frame)

    def create_action_section(self, main_layout):
        """Create action buttons section"""
        action_frame = QFrame()
        action_frame.setObjectName("actionFrame")
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        action_frame.setLayout(action_layout)

        # Copy button
        self.copy_button = QPushButton("🚀 Start Copy")
        self.copy_button.setObjectName("copyButton")
        self.copy_button.clicked.connect(self.copy_folder)

        # Settings button
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self.open_settings)

        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.settings_button)

        main_layout.addWidget(action_frame)

    def create_footer_section(self, main_layout):
        """Create footer section"""
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        footer_layout = QHBoxLayout()
        footer_frame.setLayout(footer_layout)

        version_label = QLabel("v3.0")
        version_label.setObjectName("versionLabel")

        footer_layout.addWidget(version_label)
        footer_layout.addStretch()

        main_layout.addWidget(footer_frame)

    def setup_network_monitoring(self):
        """Setup network status monitoring"""
        self.network_status_timer.timeout.connect(self.check_network_status)
        if self.settings.get('folder_type') == 'network':
            self.network_status_timer.start(30000)  # Check every 30 seconds
            self.check_network_status()

    def load_initial_data(self):
        """Load initial data and update UI"""
        self.update_ui_labels()
        self.update_network_visibility()

    def update_ui_labels(self):
        """Update UI labels with current settings"""
        self.source_label.setText(self.settings.get('source_path', 'Not selected'))
        self.destination_label.setText(self.settings.get('destination_path', 'Not selected'))
        self.folder_type_label.setText(self.settings.get('folder_type', 'local').title())
        self.auto_close_indicator.setText("✅" if self.settings.get('auto_close', False) else "❌")

    def update_network_visibility(self):
        """Update network status visibility based on folder type"""
        is_network = self.settings.get('folder_type') == 'network'
        self.network_status_widget.setVisible(is_network)

        if is_network and not self.network_status_timer.isActive():
            self.network_status_timer.start(30000)
            self.check_network_status()
        elif not is_network and self.network_status_timer.isActive():
            self.network_status_timer.stop()

    def check_network_status(self):
        """Check network connectivity"""
        if self.settings.get('folder_type') == 'network':
            ip = self.settings.get('network_ip', '127.0.0.1')
            is_connected = self.network_checker.ping_host(ip)

            if is_connected:
                self.network_indicator.setStyleSheet("color: #90EE90;")  # Light green
                self.network_status_label.setText(f"Connected to {ip}")
            else:
                self.network_indicator.setStyleSheet("color: #FFB6C1;")  # Light red
                self.network_status_label.setText(f"Cannot reach {ip}")

    def copy_folder(self):
        """Start the folder copying process"""
        # Validate paths
        source = self.settings.get('source_path', '')
        destination = self.settings.get('destination_path', '')

        if not source or not destination:
            QMessageBox.warning(self, "Missing Paths",
                              "Please configure source and destination folders in settings.")
            return

        if not os.path.exists(source):
            QMessageBox.critical(self, "Source Not Found",
                               f"Source folder does not exist:\n{source}")
            return

        if os.path.abspath(source) == os.path.abspath(destination):
            QMessageBox.critical(self, "Invalid Configuration",
                               "Source and destination cannot be the same folder.")
            return

        # Network check
        if self.settings.get('folder_type') == 'network':
            ip = self.settings.get('network_ip', '127.0.0.1')
            if not self.network_checker.ping_host(ip):
                QMessageBox.critical(self, "Network Error",
                                   f"Cannot connect to network location: {ip}")
                return

        # Start copying
        self.copy_worker = CopyWorker(source, destination)
        self.copy_worker.finished.connect(self.on_copy_finished)
        self.copy_worker.progress_update.connect(self.on_progress_update)

        # Update UI
        self.copy_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Starting copy operation...")

        self.copy_worker.start()

    def on_copy_finished(self, success, message):
        """Handle copy operation completion"""
        self.copy_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            self.status_label.setText("✅ Copy completed successfully!")
            reply = QMessageBox.information(self, "Success", message)

            # Auto-close if enabled
            if self.settings.get('auto_close', False):
                self.close()
        else:
            self.status_label.setText("❌ Copy failed")
            QMessageBox.critical(self, "Copy Failed", message)

    def on_progress_update(self, message):
        """Update progress status"""
        self.status_label.setText(f"📋 {message}")

    def open_settings(self):
        """Open settings dialog with authentication check"""
        if not self.is_authenticated:
            password_dialog = PasswordDialog(self.settings.get('password', 'password123'), self)

            if password_dialog.exec() == QDialog.DialogCode.Accepted:
                self.is_authenticated = True
                self.update_auth_status()
            else:
                return

        # Open settings dialog
        settings_dialog = SettingsDialog(self.settings_manager, self)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings = self.settings_manager.load_settings()
            self.update_ui_labels()
            self.update_network_visibility()

    def update_auth_status(self):
        """Update authentication status in UI"""
        if self.is_authenticated:
            self.auth_status_label.setText("🔓 Authenticated")
            self.logout_button.setVisible(True)
        else:
            self.auth_status_label.setText("🔒 Not Authenticated")
            self.logout_button.setVisible(False)

    def logout(self):
        """Logout user"""
        self.is_authenticated = False
        self.update_auth_status()

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Stop worker thread if running
            if self.copy_worker and self.copy_worker.isRunning():
                self.copy_worker.terminate()
                self.copy_worker.wait()

            # Stop network monitoring
            if self.network_status_timer.isActive():
                self.network_status_timer.stop()

            event.accept()
            logging.info("Application closed successfully")

        except Exception as e:
            logging.error(f"Error during application close: {str(e)}")
            event.accept()