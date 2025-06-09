"""
Settings Dialog UI for Enhanced Folder Copier
"""

import logging
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QLineEdit, QFileDialog,
                             QMessageBox, QFrame, QRadioButton, QButtonGroup,
                             QCheckBox, QTabWidget, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from utils.styles import ModernStyles


class SettingsDialog(QDialog):
    """Modern settings configuration dialog"""

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.settings = settings_manager.load_settings()

        self.setWindowTitle("⚙️ Settings")
        self.setFixedSize(700, 500)
        self.setModal(True)

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        """Setup the settings UI with tabs"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Apply modern styling
        self.setStyleSheet(ModernStyles.get_dialog_style())

        # Title
        title_label = QLabel("Application Settings")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1f2937; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(ModernStyles.get_tab_style())

        # Folders tab
        self.create_folders_tab()

        # Network tab
        self.create_network_tab()

        # General tab
        self.create_general_tab()

        layout.addWidget(self.tab_widget)

        # Buttons
        self.create_buttons(layout)

        self.setLayout(layout)

    def create_folders_tab(self):
        """Create folders configuration tab"""
        folders_widget = QWidget()
        layout = QGridLayout()
        layout.setSpacing(20)
        folders_widget.setLayout(layout)

        # Source folder section
        source_frame = QFrame()
        source_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        source_layout = QVBoxLayout()
        source_frame.setLayout(source_layout)

        source_title = QLabel("📂 Source Folder")
        source_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        source_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        source_layout.addWidget(source_title)

        source_path_layout = QHBoxLayout()
        self.source_label = QLabel("Not selected")
        self.source_label.setStyleSheet(ModernStyles.get_path_display_style())
        self.browse_source_btn = QPushButton("📁 Browse")
        self.browse_source_btn.setStyleSheet(ModernStyles.get_browse_button_style())
        self.browse_source_btn.clicked.connect(self.browse_source)

        source_path_layout.addWidget(self.source_label, 1)
        source_path_layout.addWidget(self.browse_source_btn)
        source_layout.addLayout(source_path_layout)

        layout.addWidget(source_frame, 0, 0, 1, 2)

        # Destination folder section
        dest_frame = QFrame()
        dest_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        dest_layout = QVBoxLayout()
        dest_frame.setLayout(dest_layout)

        dest_title = QLabel("📋 Destination Folder")
        dest_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        dest_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        dest_layout.addWidget(dest_title)

        dest_path_layout = QHBoxLayout()
        self.destination_label = QLabel("Not selected")
        self.destination_label.setStyleSheet(ModernStyles.get_path_display_style())
        self.browse_dest_btn = QPushButton("📁 Browse")
        self.browse_dest_btn.setStyleSheet(ModernStyles.get_browse_button_style())
        self.browse_dest_btn.clicked.connect(self.browse_destination)

        dest_path_layout.addWidget(self.destination_label, 1)
        dest_path_layout.addWidget(self.browse_dest_btn)
        dest_layout.addLayout(dest_path_layout)

        layout.addWidget(dest_frame, 1, 0, 1, 2)

        # Folder type section
        type_frame = QFrame()
        type_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        type_layout = QVBoxLayout()
        type_frame.setLayout(type_layout)

        type_title = QLabel("📍 Copy Type")
        type_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        type_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        type_layout.addWidget(type_title)

        type_selection_layout = QHBoxLayout()
        self.folder_type_group = QButtonGroup()

        self.local_radio = QRadioButton("🏠 Local Folder")
        self.network_radio = QRadioButton("🌐 Network Folder")

        self.local_radio.setStyleSheet(ModernStyles.get_radio_button_style())
        self.network_radio.setStyleSheet(ModernStyles.get_radio_button_style())

        self.folder_type_group.addButton(self.local_radio, 0)
        self.folder_type_group.addButton(self.network_radio, 1)

        type_selection_layout.addWidget(self.local_radio)
        type_selection_layout.addWidget(self.network_radio)
        type_selection_layout.addStretch()

        type_layout.addLayout(type_selection_layout)

        layout.addWidget(type_frame, 2, 0, 1, 2)

        self.tab_widget.addTab(folders_widget, "📁 Folders")

    def create_network_tab(self):
        """Create network configuration tab"""
        network_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        network_widget.setLayout(layout)

        # Network IP section
        ip_frame = QFrame()
        ip_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        ip_layout = QVBoxLayout()
        ip_frame.setLayout(ip_layout)

        ip_title = QLabel("🌐 Network Configuration")
        ip_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        ip_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        ip_layout.addWidget(ip_title)

        ip_input_layout = QHBoxLayout()
        ip_label = QLabel("IP Address:")
        ip_label.setStyleSheet("color: #6b7280; font-weight: 500;")
        self.network_ip_input = QLineEdit()
        self.network_ip_input.setPlaceholderText("Enter network IP address (e.g., 192.168.1.100)")
        self.network_ip_input.setStyleSheet(ModernStyles.get_input_style())

        ip_input_layout.addWidget(ip_label)
        ip_input_layout.addWidget(self.network_ip_input, 1)
        ip_layout.addLayout(ip_input_layout)

        # Test connection button
        test_btn_layout = QHBoxLayout()
        test_btn_layout.addStretch()
        self.test_connection_btn = QPushButton("🔗 Test Connection")
        self.test_connection_btn.setStyleSheet(ModernStyles.get_test_button_style())
        self.test_connection_btn.clicked.connect(self.test_network_connection)
        test_btn_layout.addWidget(self.test_connection_btn)
        ip_layout.addLayout(test_btn_layout)

        layout.addWidget(ip_frame)
        layout.addStretch()

        self.tab_widget.addTab(network_widget, "🌐 Network")

    def create_general_tab(self):
        """Create general settings tab"""
        general_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        general_widget.setLayout(layout)

        # Security section
        security_frame = QFrame()
        security_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        security_layout = QVBoxLayout()
        security_frame.setLayout(security_layout)

        security_title = QLabel("🔒 Security")
        security_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        security_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        security_layout.addWidget(security_title)

        password_layout = QHBoxLayout()
        password_label = QLabel("New Password:")
        password_label.setStyleSheet("color: #6b7280; font-weight: 500;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter new password (leave blank to keep current)")
        self.password_input.setStyleSheet(ModernStyles.get_input_style())

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input, 1)
        security_layout.addLayout(password_layout)

        layout.addWidget(security_frame)

        # App behavior section
        behavior_frame = QFrame()
        behavior_frame.setStyleSheet(ModernStyles.get_settings_frame_style())
        behavior_layout = QVBoxLayout()
        behavior_frame.setLayout(behavior_layout)

        behavior_title = QLabel("⚙️ Application Behavior")
        behavior_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        behavior_title.setStyleSheet("color: #374151; margin-bottom: 10px;")
        behavior_layout.addWidget(behavior_title)

        self.auto_close_checkbox = QCheckBox("🔄 Auto-close application after successful copy")
        self.auto_close_checkbox.setStyleSheet(ModernStyles.get_checkbox_style())
        behavior_layout.addWidget(self.auto_close_checkbox)

        layout.addWidget(behavior_frame)
        layout.addStretch()

        self.tab_widget.addTab(general_widget, "⚙️ General")

    def create_buttons(self, parent_layout):
        """Create dialog buttons"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Cancel button
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet(ModernStyles.get_cancel_button_style())
        self.cancel_btn.clicked.connect(self.reject)

        # Save button
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.setStyleSheet(ModernStyles.get_save_button_style())
        self.save_btn.clicked.connect(self.save_settings)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)

        parent_layout.addLayout(button_layout)

    def load_current_settings(self):
        """Load current settings into the dialog"""
        # Load folder paths
        source_path = self.settings.get('source_path', '')
        dest_path = self.settings.get('destination_path', '')

        self.source_label.setText(source_path if source_path else "Not selected")
        self.destination_label.setText(dest_path if dest_path else "Not selected")

        # Load folder type
        folder_type = self.settings.get('folder_type', 'local')
        if folder_type == 'network':
            self.network_radio.setChecked(True)
        else:
            self.local_radio.setChecked(True)

        # Load network IP
        self.network_ip_input.setText(self.settings.get('network_ip', '127.0.0.1'))

        # Load auto-close setting
        self.auto_close_checkbox.setChecked(self.settings.get('auto_close', False))

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

    def test_network_connection(self):
        """Test network connection"""
        ip_address = self.network_ip_input.text().strip()
        if not ip_address:
            QMessageBox.warning(self, "Input Required", "Please enter an IP address first.")
            return

        self.test_connection_btn.setText("🔄 Testing...")
        self.test_connection_btn.setEnabled(False)

        # Import here to avoid circular imports
        from utils.network_checker import NetworkChecker
        network_checker = NetworkChecker()

        try:
            if network_checker.ping_host(ip_address):
                QMessageBox.information(self, "Connection Test",
                                        f"✅ Successfully connected to {ip_address}")
            else:
                QMessageBox.warning(self, "Connection Test",
                                    f"❌ Failed to connect to {ip_address}")
        finally:
            self.test_connection_btn.setText("🔗 Test Connection")
            self.test_connection_btn.setEnabled(True)

    def save_settings(self):
        """Save settings and close dialog"""
        try:
            # Get values from UI
            source_text = self.source_label.text()
            dest_text = self.destination_label.text()

            # Update settings dictionary
            updated_settings = self.settings.copy()
            updated_settings['source_path'] = source_text if source_text != "Not selected" else ""
            updated_settings['destination_path'] = dest_text if dest_text != "Not selected" else ""
            updated_settings['network_ip'] = self.network_ip_input.text().strip() or "127.0.0.1"
            updated_settings['folder_type'] = 'network' if self.network_radio.isChecked() else 'local'
            updated_settings['auto_close'] = self.auto_close_checkbox.isChecked()

            # Update password if provided
            new_password = self.password_input.text().strip()
            if new_password:
                updated_settings['password'] = new_password

            # Save settings
            self.settings_manager.save_settings(updated_settings)

            QMessageBox.information(self, "Success", "✅ Settings saved successfully!")
            self.accept()

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)