import os
import shutil
import sys
import logging
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QRadioButton,
                             QFileDialog, QMessageBox, QDialog, QLineEdit,
                             QButtonGroup, QFrame, QGridLayout, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('folder_copier.log'),
        logging.StreamHandler()
    ]
)


class CopyWorker(QThread):
    """Worker thread for copying operations to prevent UI freezing"""
    finished = pyqtSignal(bool, str)
    progress_update = pyqtSignal(str)

    def __init__(self, source_path, destination_path):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path

    def run(self):
        try:
            # Validate source path
            if not os.path.exists(self.source_path):
                self.finished.emit(False, f"Source folder does not exist: {self.source_path}")
                return

            if not os.path.isdir(self.source_path):
                self.finished.emit(False, f"Source path is not a directory: {self.source_path}")
                return

            # Handle existing destination folder
            if os.path.exists(self.destination_path):
                self.progress_update.emit("Destination exists, handling backup...")
                self.handle_existing_destination()

            self.progress_update.emit("Copying folder...")
            shutil.copytree(self.source_path, self.destination_path)
            self.finished.emit(True, "Folder copied successfully!")
            logging.info(f"Successfully copied {self.source_path} to {self.destination_path}")

        except PermissionError as e:
            error_msg = f"Permission denied: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)
        except FileNotFoundError as e:
            error_msg = f"File or folder not found: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)
        except OSError as e:
            error_msg = f"OS Error occurred: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)

    def handle_existing_destination(self):
        """Handle existing destination folder according to specified logic"""
        base_name = self.destination_path
        old_name = f"{base_name}_old"

        try:
            # If *_old exists, delete it
            if os.path.exists(old_name):
                self.progress_update.emit("Removing old backup...")
                if os.path.isdir(old_name):
                    shutil.rmtree(old_name)
                else:
                    os.remove(old_name)
                logging.info(f"Deleted existing backup: {old_name}")

            # Rename existing folder to *_old
            self.progress_update.emit("Creating backup of existing folder...")
            os.rename(self.destination_path, old_name)
            logging.info(f"Renamed {self.destination_path} to {old_name}")

        except Exception as e:
            error_msg = f"Error handling existing destination: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)


class PasswordDialog(QDialog):
    """Dialog for password authentication"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Password")
        self.setFixedSize(300, 120)
        self.setModal(True)

        layout = QVBoxLayout()

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password...")

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.password_input.returnPressed.connect(self.accept)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(QLabel("Enter Password:"))
        layout.addWidget(self.password_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_password(self):
        return self.password_input.text()


class SettingsDialog(QDialog):
    """Settings configuration dialog"""

    def __init__(self, app_instance, parent=None):
        super().__init__(parent)
        self.app_instance = app_instance
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 300)
        self.setModal(True)

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        layout = QGridLayout()

        # Source folder
        layout.addWidget(QLabel("Source Folder:"), 0, 0)
        self.source_label = QLabel("Not selected")
        self.source_label.setStyleSheet("border: 1px solid gray; padding: 5px; background: white;")
        layout.addWidget(self.source_label, 0, 1)

        self.browse_source_btn = QPushButton("Browse Source")
        self.browse_source_btn.clicked.connect(self.browse_source)
        layout.addWidget(self.browse_source_btn, 0, 2)

        # Destination folder
        layout.addWidget(QLabel("Destination Folder:"), 1, 0)
        self.destination_label = QLabel("Not selected")
        self.destination_label.setStyleSheet("border: 1px solid gray; padding: 5px; background: white;")
        layout.addWidget(self.destination_label, 1, 1)

        self.browse_dest_btn = QPushButton("Browse Destination")
        self.browse_dest_btn.clicked.connect(self.browse_destination)
        layout.addWidget(self.browse_dest_btn, 1, 2)

        # Network IP
        layout.addWidget(QLabel("Network IP:"), 2, 0)
        self.network_ip_input = QLineEdit()
        self.network_ip_input.setPlaceholderText("Enter network IP address...")
        layout.addWidget(self.network_ip_input, 2, 1, 1, 2)

        # Password
        layout.addWidget(QLabel("Settings Password:"), 3, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter new password...")
        layout.addWidget(self.password_input, 3, 1, 1, 2)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Settings")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout, 4, 0, 1, 3)
        self.setLayout(layout)

    def load_current_settings(self):
        """Load current settings into the dialog"""
        self.source_label.setText(self.app_instance.source_path or "Not selected")
        self.destination_label.setText(self.app_instance.destination_path or "Not selected")
        self.network_ip_input.setText(self.app_instance.network_ip)
        # Don't pre-fill password for security

    def browse_source(self):
        """Browse for source folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_label.setText(folder)

    def browse_destination(self):
        """Browse for destination folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_label.setText(folder)

    def save_settings(self):
        """Save settings and close dialog"""
        try:
            # Update app instance
            source_text = self.source_label.text()
            dest_text = self.destination_label.text()

            self.app_instance.source_path = source_text if source_text != "Not selected" else ""
            self.app_instance.destination_path = dest_text if dest_text != "Not selected" else ""
            self.app_instance.network_ip = self.network_ip_input.text() or "127.0.0.1"

            # Update password if provided
            new_password = self.password_input.text()
            if new_password:
                self.app_instance.password = new_password

            # Save to file
            self.app_instance.save_settings()

            # Update main UI
            self.app_instance.update_ui_labels()

            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)


class FolderCopierApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Folder Copier")
        self.setFixedSize(550, 250)

        # Initialize variables
        self.source_path = ""
        self.destination_path = ""
        self.network_ip = "127.0.0.1"
        self.password = "password123"
        self.folder_type = "local"

        # Worker thread
        self.copy_worker = None

        self.setup_ui()
        self.load_settings()

        # Set icon if available
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_directory, 'icon.ico')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            logging.warning(f"Could not load icon: {str(e)}")

    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title
        title_label = QLabel("Folder Copier")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        # Path information frame
        path_frame = QFrame()
        path_frame.setFrameStyle(QFrame.Shape.Box)
        path_layout = QGridLayout()
        path_frame.setLayout(path_layout)

        # Source path
        path_layout.addWidget(QLabel("Source Folder:"), 0, 0)
        self.source_label = QLabel("Not selected")
        self.source_label.setStyleSheet("background: white; padding: 5px; border: 1px solid gray;")
        path_layout.addWidget(self.source_label, 0, 1)

        # Destination path
        path_layout.addWidget(QLabel("Destination Folder:"), 1, 0)
        self.destination_label = QLabel("Not selected")
        self.destination_label.setStyleSheet("background: white; padding: 5px; border: 1px solid gray;")
        path_layout.addWidget(self.destination_label, 1, 1)

        main_layout.addWidget(path_frame)

        # Folder type selection
        type_layout = QHBoxLayout()
        self.folder_type_group = QButtonGroup()

        self.local_radio = QRadioButton("Local Folder")
        self.network_radio = QRadioButton("Network Folder")

        self.local_radio.setChecked(True)

        self.folder_type_group.addButton(self.local_radio, 0)
        self.folder_type_group.addButton(self.network_radio, 1)

        type_layout.addWidget(self.local_radio)
        type_layout.addWidget(self.network_radio)
        type_layout.addStretch()

        main_layout.addLayout(type_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        main_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Buttons
        button_layout = QHBoxLayout()

        self.copy_button = QPushButton("Copy Folder")
        self.copy_button.setStyleSheet(
            "QPushButton { background-color: #007bff; color: white; font-weight: bold; padding: 8px; }")
        self.copy_button.clicked.connect(self.copy_folder)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet(
            "QPushButton { background-color: #28a745; color: white; font-weight: bold; padding: 8px; }")
        self.settings_button.clicked.connect(self.open_settings)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.settings_button)

        main_layout.addLayout(button_layout)

    def update_ui_labels(self):
        """Update UI labels with current paths"""
        self.source_label.setText(self.source_path or "Not selected")
        self.destination_label.setText(self.destination_path or "Not selected")

    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as file:
                    settings = json.load(file)

                    self.source_path = settings.get("source_path", "")
                    self.destination_path = settings.get("destination_path", "")
                    self.network_ip = settings.get("network_ip", "127.0.0.1")
                    self.password = settings.get("password", "password123")
                    self.folder_type = settings.get("folder_type", "local")

                    # Update radio buttons
                    if self.folder_type == "network":
                        self.network_radio.setChecked(True)
                    else:
                        self.local_radio.setChecked(True)

                    self.update_ui_labels()
                    logging.info("Settings loaded successfully")

        except Exception as e:
            error_msg = f"Failed to load settings: {str(e)}"
            logging.error(error_msg)
            QMessageBox.warning(self, "Warning", f"Could not load settings: {str(e)}")

    def save_settings(self):
        """Save settings to file"""
        try:
            # Determine folder type
            if self.network_radio.isChecked():
                self.folder_type = "network"
            else:
                self.folder_type = "local"

            settings = {
                "source_path": self.source_path,
                "destination_path": self.destination_path,
                "network_ip": self.network_ip,
                "password": self.password,
                "folder_type": self.folder_type
            }

            with open("settings.json", "w") as file:
                json.dump(settings, file, indent=2)

            logging.info("Settings saved successfully")

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def copy_folder(self):
        """Start the folder copying process"""
        # Validate paths
        if not self.source_path or not self.destination_path:
            QMessageBox.warning(self, "Warning", "Please set source and destination folders in settings.")
            return

        if not os.path.exists(self.source_path):
            QMessageBox.critical(self, "Error", f"Source folder does not exist:\n{self.source_path}")
            return

        # Check if copying to itself
        if os.path.abspath(self.source_path) == os.path.abspath(self.destination_path):
            QMessageBox.critical(self, "Error", "Source and destination cannot be the same folder.")
            return

        # Network connection check
        if self.network_radio.isChecked():
            if not self.check_network_connection():
                QMessageBox.critical(self, "Error", "No connection to the network folder.")
                return

        # Start copying in worker thread
        self.copy_worker = CopyWorker(self.source_path, self.destination_path)
        self.copy_worker.finished.connect(self.on_copy_finished)
        self.copy_worker.progress_update.connect(self.on_progress_update)

        # Update UI for copying state
        self.copy_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Copying...")

        self.copy_worker.start()

    def on_copy_finished(self, success, message):
        """Handle copy operation completion"""
        self.copy_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            self.status_label.setText("Copy completed successfully")
            QMessageBox.information(self, "Success", message)
        else:
            self.status_label.setText("Copy failed")
            QMessageBox.critical(self, "Error", message)

    def on_progress_update(self, message):
        """Update progress status"""
        self.status_label.setText(message)

    def check_network_connection(self):
        """Check network connection (placeholder implementation)"""
        # TODO: Implement actual network connectivity check
        # For now, always return True
        return True

    def open_settings(self):
        """Open settings dialog after password verification"""
        password_dialog = PasswordDialog(self)

        if password_dialog.exec() == QDialog.DialogCode.Accepted:
            entered_password = password_dialog.get_password()

            if entered_password == self.password:
                settings_dialog = SettingsDialog(self, self)
                settings_dialog.exec()
            else:
                QMessageBox.critical(self, "Error", "Incorrect password.")

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Stop worker thread if running
            if self.copy_worker and self.copy_worker.isRunning():
                self.copy_worker.terminate()
                self.copy_worker.wait()

            # Save settings
            self.save_settings()
            event.accept()

        except Exception as e:
            logging.error(f"Error during application close: {str(e)}")
            event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Enhanced Folder Copier")
    app.setApplicationVersion("2.0")

    # Set application style
    app.setStyle('Fusion')

    try:
        window = FolderCopierApp()
        window.show()

        logging.info("Application started successfully")
        sys.exit(app.exec())

    except Exception as e:
        logging.critical(f"Failed to start application: {str(e)}")
        QMessageBox.critical(None, "Critical Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()