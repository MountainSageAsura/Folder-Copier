import os
import shutil
import sys
import subprocess
import platform
import threading
import json
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFrame, QTabWidget,
                             QLineEdit, QRadioButton, QCheckBox, QProgressBar,
                             QTextEdit, QFileDialog, QMessageBox, QDialog,
                             QGroupBox, QGridLayout, QFormLayout, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QPainter


def create_black_white_emoji_icon(emoji, size=32):
    """Create a black and white QIcon from an emoji character"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Set font and color for black and white emoji
    font = QFont("Segoe UI Emoji", int(size * 0.6))
    painter.setFont(font)
    painter.setPen(QColor(0, 0, 0))  # Black color

    # Draw emoji centered in black
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, emoji)
    painter.end()

    return QIcon(pixmap)


class LogHandler(logging.Handler):
    """Custom log handler to emit log messages to GUI"""

    def __init__(self):
        super().__init__()
        self.log_signal = None

    def emit(self, record):
        if self.log_signal:
            log_entry = self.format(record)
            self.log_signal.emit(log_entry)


class CopyWorker(QThread):
    """Worker thread for folder copying operations"""
    progress_updated = pyqtSignal(int, str)
    copy_finished = pyqtSignal(bool, str)
    log_message = pyqtSignal(str)

    def __init__(self, source_path, destination_path, logger):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path
        self.logger = logger
        self.is_cancelled = False

    def run(self):
        """Run the copy operation"""
        try:
            self.smart_folder_copy()
        except Exception as e:
            self.logger.error(f"Copy operation failed: {str(e)}")
            self.copy_finished.emit(False, str(e))

    def cancel(self):
        """Cancel the copy operation"""
        self.is_cancelled = True

    def smart_folder_copy(self):
        """Smart folder copying with progress updates"""
        try:
            source_folder_name = os.path.basename(self.source_path)
            destination_full_path = os.path.join(self.destination_path, source_folder_name)
            destination_old_path = destination_full_path + "_old"

            self.log_message.emit(f"Starting smart copy: {self.source_path} → {destination_full_path}")
            self.progress_updated.emit(5, "Analyzing source folder...")

            # Calculate total files for progress tracking
            total_files = sum([len(files) for _, _, files in os.walk(self.source_path)])
            self.log_message.emit(f"Found {total_files} files to copy")

            if self.is_cancelled:
                return

            self.progress_updated.emit(10, "Preparing destination...")

            # Handle existing destination folder
            if os.path.exists(destination_full_path):
                self.log_message.emit(f"Destination exists: {destination_full_path}")

                if os.path.exists(destination_old_path):
                    self.log_message.emit(f"Removing old backup: {destination_old_path}")
                    self.progress_updated.emit(15, "Removing old backup...")
                    shutil.rmtree(destination_old_path)

                self.log_message.emit(f"Creating backup: {destination_full_path} → {destination_old_path}")
                self.progress_updated.emit(20, "Creating backup...")
                os.rename(destination_full_path, destination_old_path)

            if self.is_cancelled:
                return

            # Copy with progress tracking
            self.progress_updated.emit(25, "Starting file copy...")
            self.copy_tree_with_progress(self.source_path, destination_full_path, total_files)

            if not self.is_cancelled:
                self.log_message.emit("Copy operation completed successfully")
                self.copy_finished.emit(True, "Folder copied successfully!")

        except Exception as e:
            self.logger.error(f"Smart copy failed: {str(e)}")
            # Try to restore backup if copy failed
            if os.path.exists(destination_old_path) and not os.path.exists(destination_full_path):
                try:
                    os.rename(destination_old_path, destination_full_path)
                    self.log_message.emit("Restored original folder after copy failure")
                except Exception as restore_error:
                    self.logger.error(f"Failed to restore backup: {str(restore_error)}")

            self.copy_finished.emit(False, str(e))

    def copy_tree_with_progress(self, src, dst, total_files):
        """Copy directory tree with progress updates"""
        copied_files = 0

        for root, dirs, files in os.walk(src):
            if self.is_cancelled:
                break

            # Create corresponding directory structure
            rel_path = os.path.relpath(root, src)
            dst_root = os.path.join(dst, rel_path) if rel_path != '.' else dst

            if not os.path.exists(dst_root):
                os.makedirs(dst_root)

            # Copy files
            for file in files:
                if self.is_cancelled:
                    break

                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file)

                try:
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1

                    # Update progress
                    progress = 25 + int((copied_files / total_files) * 70)  # 25-95% range
                    self.progress_updated.emit(progress, f"Copying: {file}")
                    self.log_message.emit(f"Copied: {src_file}")

                except Exception as e:
                    self.log_message.emit(f"Failed to copy {src_file}: {str(e)}")
                    raise

        if not self.is_cancelled:
            self.progress_updated.emit(100, "Copy completed!")


class NetworkChecker(QThread):
    """Worker thread for network connectivity checking"""
    status_updated = pyqtSignal(bool, str)

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def run(self):
        """Check network connectivity"""
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "3000", self.ip_address]
            else:
                cmd = ["ping", "-c", "1", "-W", "3", self.ip_address]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            is_connected = result.returncode == 0

            status_text = f"Connected ({self.ip_address})" if is_connected else f"Disconnected ({self.ip_address})"
            self.status_updated.emit(is_connected, status_text)

        except Exception:
            self.status_updated.emit(False, f"Error checking ({self.ip_address})")


class CustomMessageBox(QDialog):
    """Custom message box with proper icon and text alignment"""

    def __init__(self, parent=None, title="", message="", icon_text="", message_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        # Use black and white emoji icon
        if icon_text:
            self.setWindowIcon(create_black_white_emoji_icon(icon_text))
        else:
            self.setWindowIcon(QIcon())
        self.setMinimumSize(350, 150)
        self.setup_ui(message, icon_text, message_type)
        self.apply_styles()

    def setup_ui(self, message, icon_text, message_type):
        layout = QVBoxLayout()

        # Content area with icon and message
        content_layout = QHBoxLayout()

        # Icon
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(60, 60)
        content_layout.addWidget(icon_label)

        # Message
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 11))
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        content_layout.addWidget(message_label, 1)

        layout.addLayout(content_layout)

        # Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_btn = QPushButton("OK")
        ok_btn.setMinimumWidth(80)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                background-color: #a8dadc;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #96d2d4;
            }
        """)


class PasswordDialog(QDialog):
    """Password authentication dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Authentication Required")
        self.setWindowIcon(create_black_white_emoji_icon("🔒"))  # Black and white lock emoji
        self.setFixedSize(350, 200)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title with emoji
        title_label = QLabel("🔒 Enter Password:")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.returnPressed.connect(self.accept)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.accept)
        login_btn.setDefault(True)
        button_layout.addWidget(login_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Focus on password input
        self.password_input.setFocus()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333333;
                margin: 10px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                background-color: white;
                margin: 5px;
            }
            QPushButton {
                padding: 8px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """)

    def get_password(self):
        return self.password_input.text()


class SettingsDialog(QDialog):
    """Settings configuration dialog with tabs"""

    def __init__(self, app_instance, parent=None):
        super().__init__(parent)
        self.app = app_instance
        self.setWindowTitle("Settings")
        self.setWindowIcon(create_black_white_emoji_icon("⚙️"))  # Black and white gear emoji
        self.setFixedSize(600, 500)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title with emoji
        title_label = QLabel("⚙️ Settings")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Tab widget
        self.tab_widget = QTabWidget()

        # Create tabs
        self.create_folders_tab()
        self.create_connection_tab()
        self.create_security_tab()
        self.create_preferences_tab()

        layout.addWidget(self.tab_widget)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def create_folders_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Source folder group
        source_group = QGroupBox("📁 Source Folder")
        source_layout = QVBoxLayout()

        self.source_path_edit = QLineEdit(self.app.source_path)
        self.source_path_edit.setReadOnly(True)
        source_layout.addWidget(self.source_path_edit)

        source_browse_btn = QPushButton("Browse Source Folder")
        source_browse_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(source_browse_btn)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Destination folder group
        dest_group = QGroupBox("📁 Destination Folder")
        dest_layout = QVBoxLayout()

        self.dest_path_edit = QLineEdit(self.app.destination_path)
        self.dest_path_edit.setReadOnly(True)
        dest_layout.addWidget(self.dest_path_edit)

        dest_browse_btn = QPushButton("Browse Destination Folder")
        dest_browse_btn.clicked.connect(self.browse_destination)
        dest_layout.addWidget(dest_browse_btn)

        dest_group.setLayout(dest_layout)
        layout.addWidget(dest_group)

        layout.addStretch()
        widget.setLayout(layout)
        self.tab_widget.addTab(widget, "📁 Folders")

    def create_connection_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Folder type group
        type_group = QGroupBox("🌐 Folder Type")
        type_layout = QVBoxLayout()

        self.local_radio = QRadioButton("Local Folder")
        self.network_radio = QRadioButton("Network Folder")

        if self.app.folder_type == "local":
            self.local_radio.setChecked(True)
        else:
            self.network_radio.setChecked(True)

        type_layout.addWidget(self.local_radio)
        type_layout.addWidget(self.network_radio)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Network settings group
        network_group = QGroupBox("🌐 Network Settings")
        network_layout = QGridLayout()

        # Properly aligned label and input
        network_label = QLabel("Network IP Address:")
        network_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.network_ip_edit = QLineEdit(self.app.network_ip)

        network_layout.addWidget(network_label, 0, 0)
        network_layout.addWidget(self.network_ip_edit, 0, 1)

        # Set column stretch to make input field expandable
        network_layout.setColumnStretch(1, 1)

        network_group.setLayout(network_layout)
        layout.addWidget(network_group)

        layout.addStretch()
        widget.setLayout(layout)
        self.tab_widget.addTab(widget, "🌐 Connection")

    def create_security_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Password change group
        password_group = QGroupBox("🔐 Change Password")
        password_layout = QGridLayout()

        # Current password
        current_label = QLabel("Current Password:")
        current_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.current_password_edit = QLineEdit()
        self.current_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout.addWidget(current_label, 0, 0)
        password_layout.addWidget(self.current_password_edit, 0, 1)

        # New password
        new_label = QLabel("New Password:")
        new_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout.addWidget(new_label, 1, 0)
        password_layout.addWidget(self.new_password_edit, 1, 1)

        # Change password button
        change_password_btn = QPushButton("Change Password")
        change_password_btn.clicked.connect(self.change_password)
        password_layout.addWidget(change_password_btn, 2, 0, 1, 2)

        # Set column stretch to make input fields expandable
        password_layout.setColumnStretch(1, 1)

        password_group.setLayout(password_layout)
        layout.addWidget(password_group)

        layout.addStretch()
        widget.setLayout(layout)
        self.tab_widget.addTab(widget, "🔐 Security")

    def create_preferences_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Application preferences group
        pref_group = QGroupBox("⚙️ Application Preferences")
        pref_layout = QVBoxLayout()

        self.auto_close_checkbox = QCheckBox("Auto-close application after successful copy")
        self.auto_close_checkbox.setChecked(self.app.auto_close)
        pref_layout.addWidget(self.auto_close_checkbox)

        pref_group.setLayout(pref_layout)
        layout.addWidget(pref_group)

        layout.addStretch()
        widget.setLayout(layout)
        self.tab_widget.addTab(widget, "⚙️ Preferences")

    def browse_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_path_edit.setText(folder)

    def browse_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.dest_path_edit.setText(folder)

    def change_password(self):
        if self.current_password_edit.text() != self.app.password:
            QMessageBox.warning(self, "Error", "Current password is incorrect.")
            return

        new_password = self.new_password_edit.text()
        if len(new_password) < 3:
            QMessageBox.warning(self, "Error", "New password must be at least 3 characters long.")
            return

        self.app.password = new_password
        self.current_password_edit.clear()
        self.new_password_edit.clear()
        QMessageBox.information(self, "Success", "Password changed successfully!")

    def save_settings(self):
        # Update app settings
        self.app.source_path = self.source_path_edit.text()
        self.app.destination_path = self.dest_path_edit.text()
        self.app.network_ip = self.network_ip_edit.text()
        self.app.folder_type = "local" if self.local_radio.isChecked() else "network"
        self.app.auto_close = self.auto_close_checkbox.isChecked()

        if self.app.save_settings():
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.app.update_display()
            self.accept()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                margin: 10px 0px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                background-color: white;
                margin: 2px;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 2px;
                background-color: #a8dadc;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #96d2d4;
            }
            QCheckBox, QRadioButton {
                font-size: 11px;
                color: #333333;
                margin: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #e9ecef;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #a8dadc;
            }
        """)


class FolderCopierApp(QMainWindow):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Copier Pro")
        self.setWindowIcon(create_black_white_emoji_icon("📁"))  # Black and white folder emoji
        self.setFixedSize(1000, 1000)

        # Initialize variables
        self.source_path = ""
        self.destination_path = ""
        self.network_ip = "127.0.0.1"
        self.password = "password"
        self.folder_type = "local"
        self.auto_close = False
        self.is_logged_in = False
        self.network_status = False

        # Settings file
        self.settings_file = "settings.json"

        # Setup logging
        self.setup_logging()

        # Worker threads
        self.copy_worker = None
        self.network_checker = None

        # Load settings and setup UI
        self.load_settings()
        self.setup_ui()
        self.apply_styles()
        self.check_network_status()

        # Connect log signal
        self.log_signal.connect(self.append_log)

        self.logger.info("Application initialized successfully")

    def setup_logging(self):
        """Setup logging system"""
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')

            self.logger = logging.getLogger('FolderCopierApp')
            self.logger.setLevel(logging.INFO)

            # File handler
            log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(logging.INFO)

            # GUI handler
            self.gui_log_handler = LogHandler()
            self.gui_log_handler.log_signal = self.log_signal
            self.gui_log_handler.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            gui_formatter = logging.Formatter('%(asctime)s - %(message)s')
            self.gui_log_handler.setFormatter(gui_formatter)

            if not self.logger.handlers:
                self.logger.addHandler(file_handler)
                self.logger.addHandler(self.gui_log_handler)

        except Exception as e:
            print(f"Failed to setup logging: {str(e)}")
            self.logger = logging.getLogger('FolderCopierApp')

    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title with emoji
        title_label = QLabel("📁 Folder Copier Pro")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Info panel
        self.create_info_panel(main_layout)

        # Progress section
        self.create_progress_section(main_layout)

        # Log section
        self.create_log_section(main_layout)

        # Button section
        self.create_button_section(main_layout)

        central_widget.setLayout(main_layout)

    def create_info_panel(self, parent_layout):
        """Create the information display panel"""
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.Box)
        info_layout = QVBoxLayout()

        # Source folder
        source_layout = QVBoxLayout()
        source_label = QLabel("📁 Source Folder:")
        source_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        source_layout.addWidget(source_label)

        self.source_display = QLabel(self.source_path or "Not selected")
        self.source_display.setFont(QFont("Segoe UI", 10))
        self.source_display.setWordWrap(True)
        source_layout.addWidget(self.source_display)

        info_layout.addLayout(source_layout)

        # Destination folder
        dest_layout = QVBoxLayout()
        dest_label = QLabel("📁 Destination Folder:")
        dest_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        dest_layout.addWidget(dest_label)

        self.dest_display = QLabel(self.destination_path or "Not selected")
        self.dest_display.setFont(QFont("Segoe UI", 10))
        self.dest_display.setWordWrap(True)
        dest_layout.addWidget(self.dest_display)

        info_layout.addLayout(dest_layout)

        # Status section
        status_layout = QHBoxLayout()

        # Folder type
        type_label = QLabel("📁 Type:")
        type_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        status_layout.addWidget(type_label)

        self.type_display = QLabel(self.folder_type.title())
        self.type_display.setFont(QFont("Segoe UI", 10))
        status_layout.addWidget(self.type_display)

        status_layout.addStretch()

        # Network status (only show for network type)
        self.network_label = QLabel("🌐 Network:")
        self.network_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        self.network_status_label = QLabel("Checking...")
        self.network_status_label.setFont(QFont("Segoe UI", 10))

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(40, 30)
        self.refresh_btn.clicked.connect(self.refresh_network_status)
        # Make background transparent so emoji is visible
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #a8dadc;
                border-radius: 5px;
                color: #333333;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #a8dadc;
                opacity: 0.8;
            }
        """)

        # Only show network elements if network type is selected
        if self.folder_type == "network":
            status_layout.addWidget(self.network_label)
            status_layout.addWidget(self.network_status_label)
            status_layout.addWidget(self.refresh_btn)

        info_layout.addLayout(status_layout)
        info_frame.setLayout(info_layout)
        parent_layout.addWidget(info_frame)

    def create_progress_section(self, parent_layout):
        """Create the progress bar section"""
        progress_group = QGroupBox("📊 Copy Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_label)

        progress_group.setLayout(progress_layout)
        parent_layout.addWidget(progress_group)

    def create_log_section(self, parent_layout):
        """Create the live log display section"""
        log_group = QGroupBox("📝 Live Log")
        log_layout = QVBoxLayout()

        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_display)

        # Log controls
        log_controls = QHBoxLayout()

        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        log_controls.addWidget(clear_log_btn)

        log_controls.addStretch()
        log_layout.addLayout(log_controls)

        log_group.setLayout(log_layout)
        parent_layout.addWidget(log_group)

    def create_button_section(self, parent_layout):
        """Create the main action buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Copy button
        self.copy_btn = QPushButton("📁 Copy Folder")
        self.copy_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.copy_btn.setMinimumHeight(50)
        self.copy_btn.clicked.connect(self.copy_folder)
        button_layout.addWidget(self.copy_btn)

        # Settings button
        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.setFont(QFont("Segoe UI", 12))
        self.settings_btn.setMinimumHeight(50)
        self.settings_btn.clicked.connect(self.open_settings)
        button_layout.addWidget(self.settings_btn)

        # Logout button (hidden by default)
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setFont(QFont("Segoe UI", 12))
        self.logout_btn.setMinimumHeight(50)
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setVisible(self.is_logged_in)
        button_layout.addWidget(self.logout_btn)

        parent_layout.addLayout(button_layout)

    def apply_styles(self):
        """Apply custom styles to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333333;
            }
            QFrame {
                background-color: #e9ecef;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 5px 0px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QPushButton:pressed {
                opacity: 0.6;
            }
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background-color: #b8e6b8;
                border-radius: 3px;
            }
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                background-color: #ffffff;
                color: #333333;
            }
        """)

        # Set button colors
        self.copy_btn.setStyleSheet("background-color: #b8e6b8; color: #333333;")
        self.settings_btn.setStyleSheet("background-color: #a8dadc; color: #333333;")
        self.logout_btn.setStyleSheet("background-color: #ffb3ba; color: #333333;")

    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    settings = json.load(file)

                    self.source_path = settings.get('source_path', '')
                    self.destination_path = settings.get('destination_path', '')
                    self.network_ip = settings.get('network_ip', '127.0.0.1')
                    self.password = settings.get('password', 'password')
                    self.folder_type = settings.get('folder_type', 'local')
                    self.auto_close = settings.get('auto_close', False)

        except Exception as e:
            QMessageBox.warning(self, "Settings Error", f"Failed to load settings: {str(e)}")
            self.save_settings()

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            settings = {
                'source_path': self.source_path,
                'destination_path': self.destination_path,
                'network_ip': self.network_ip,
                'password': self.password,
                'folder_type': self.folder_type,
                'auto_close': self.auto_close,
                'version': '41',
                'last_updated': datetime.now().isoformat()
            }

            with open(self.settings_file, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)

            return True

        except Exception as e:
            QMessageBox.critical(self, "Settings Error", f"Failed to save settings: {str(e)}")
            return False

    def update_display(self):
        """Update the main display"""
        self.source_display.setText(self.source_path or "Not selected")
        self.dest_display.setText(self.destination_path or "Not selected")
        self.type_display.setText(self.folder_type.title())

        # Show/hide network status based on folder type
        self.network_label.setVisible(self.folder_type == "network")
        self.network_status_label.setVisible(self.folder_type == "network")
        self.refresh_btn.setVisible(self.folder_type == "network")

        if self.folder_type == "network":
            self.check_network_status()

        self.logger.info("Display updated")

    def check_network_status(self):
        """Check network connectivity"""
        if self.folder_type == "network":
            self.network_status_label.setText("Checking...")
            self.logger.info(f"Checking network connectivity to {self.network_ip}")
            self.network_checker = NetworkChecker(self.network_ip)
            self.network_checker.status_updated.connect(self.update_network_status)
            self.network_checker.start()

    def update_network_status(self, is_connected, status_text):
        """Update network status display"""
        self.network_status = is_connected
        self.network_status_label.setText(status_text)

        if is_connected:
            self.network_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
            self.logger.info(f"Network connection successful to {self.network_ip}")
        else:
            self.network_status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.logger.warning(f"Network connection failed to {self.network_ip}")

    def refresh_network_status(self):
        """Refresh network status"""
        self.logger.info(f"Manual network status refresh requested for {self.network_ip}")
        self.check_network_status()

    def append_log(self, message):
        """Append message to log display"""
        self.log_display.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        """Clear the log display"""
        self.log_display.clear()

    def copy_folder(self):
        """Start folder copy operation"""
        # Validate inputs
        if not self.source_path or not self.destination_path:
            QMessageBox.warning(self, "Configuration Error",
                                "Please set source and destination folders in settings.")
            return

        # Check if source and destination are the same
        try:
            source_abs = os.path.abspath(self.source_path)
            dest_abs = os.path.abspath(self.destination_path)
            if source_abs == dest_abs:
                QMessageBox.critical(self, "Path Error",
                                     "Source and destination folders cannot be the same.\n\n"
                                     f"Source: {source_abs}\n"
                                     f"Destination: {dest_abs}")
                self.logger.error(f"Source and destination paths are identical: {source_abs}")
                return

            # Check if source is within destination or vice versa
            if source_abs.startswith(dest_abs + os.sep) or dest_abs.startswith(source_abs + os.sep):
                QMessageBox.critical(self, "Path Error",
                                     "Source and destination folders cannot be nested within each other.\n\n"
                                     f"Source: {source_abs}\n"
                                     f"Destination: {dest_abs}")
                self.logger.error(f"Source and destination paths are nested: {source_abs} <-> {dest_abs}")
                return

        except Exception as e:
            QMessageBox.warning(self, "Path Validation Error",
                                f"Could not validate folder paths: {str(e)}")
            self.logger.error(f"Path validation failed: {str(e)}")
            return

        if not os.path.exists(self.source_path):
            QMessageBox.critical(self, "Source Error",
                                 f"Source folder does not exist:\n{self.source_path}")
            return

        if not os.path.exists(self.destination_path):
            QMessageBox.critical(self, "Destination Error",
                                 f"Destination folder does not exist:\n{self.destination_path}")
            return

        if self.folder_type == "network" and not self.network_status:
            QMessageBox.warning(self, "Network Error",
                                "No connection to the network. Please check network settings.")
            return

        # Start copy operation
        self.copy_btn.setEnabled(False)
        self.copy_btn.setText("⏸️ Cancel")
        self.copy_btn.clicked.disconnect()
        self.copy_btn.clicked.connect(self.cancel_copy)

        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(0)

        # Start worker thread
        self.copy_worker = CopyWorker(self.source_path, self.destination_path, self.logger)
        self.copy_worker.progress_updated.connect(self.update_progress)
        self.copy_worker.copy_finished.connect(self.copy_finished)
        self.copy_worker.log_message.connect(self.append_log)
        self.copy_worker.start()

        self.logger.info(f"Copy operation started: {self.source_path} → {self.destination_path}")

    def cancel_copy(self):
        """Cancel the current copy operation"""
        if self.copy_worker and self.copy_worker.isRunning():
            self.copy_worker.cancel()
            self.copy_worker.wait()
            self.logger.info("Copy operation cancelled by user")
            self.reset_copy_ui()

    def update_progress(self, value, text):
        """Update progress bar and text"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)

    def copy_finished(self, success, message):
        """Handle copy operation completion"""
        self.reset_copy_ui()

        if success:
            # Use custom success dialog with proper alignment
            success_dialog = CustomMessageBox(
                self,
                "Success",
                message,
                "✅",
                "success"
            )
            success_dialog.exec()
            self.logger.info("Copy operation completed successfully")

            if self.auto_close:
                self.logger.info("Auto-closing application")
                self.close()
        else:
            # Use custom error dialog
            error_dialog = CustomMessageBox(
                self,
                "Copy Error",
                f"Copy operation failed:\n{message}",
                "❌",
                "error"
            )
            error_dialog.exec()
            self.logger.error(f"Copy operation failed: {message}")

    def reset_copy_ui(self):
        """Reset copy-related UI elements"""
        self.copy_btn.setEnabled(True)
        self.copy_btn.setText("📁 Copy Folder")
        self.copy_btn.clicked.disconnect()
        self.copy_btn.clicked.connect(self.copy_folder)

        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

    def open_settings(self):
        """Open settings dialog"""
        if self.is_logged_in:
            self.show_settings_dialog()
        else:
            self.show_password_dialog()

    def show_password_dialog(self):
        """Show password authentication dialog"""
        dialog = PasswordDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.get_password()
            if password == self.password:
                self.is_logged_in = True
                self.logout_btn.setVisible(True)
                self.show_settings_dialog()
                self.logger.info("User successfully authenticated")
            else:
                QMessageBox.warning(self, "Authentication Error", "Incorrect password.")
                self.logger.warning("Failed authentication attempt")

    def show_settings_dialog(self):
        """Show settings configuration dialog"""
        dialog = SettingsDialog(self, self)
        dialog.exec()

    def logout(self):
        """Logout current user"""
        self.is_logged_in = False
        self.logout_btn.setVisible(False)
        self.logger.info("User logged out")

    def closeEvent(self, event):
        """Handle application close event"""
        # Cancel any running operations
        if self.copy_worker and self.copy_worker.isRunning():
            self.copy_worker.cancel()
            self.copy_worker.wait()

        if self.network_checker and self.network_checker.isRunning():
            self.network_checker.wait()

        self.logger.info("Application closed")
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Folder Copier Pro")
    app.setApplicationVersion("41")
    app.setOrganizationName("Folder Copier Pro")

    # Create and show main window
    window = FolderCopierApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()