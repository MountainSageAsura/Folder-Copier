"""
Settings Dialog - Enhanced Folder Copier
Modern settings interface with all configuration options
"""

import logging
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QPushButton, QLineEdit, QFileDialog,
                            QMessageBox, QRadioButton, QButtonGroup, QCheckBox,
                            QFrame, QTabWidget, QWidget)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """Modern settings configuration dialog"""

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.settings = settings_manager.load_settings()

        self.setWindowTitle("Settings Configuration")
        self.setFixedSize(800, 600)
        self.setModal(True)

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        """Setup the settings UI with tabs"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("settingsTabWidget")

        # Create tabs
        self.create_paths_tab()
        self.create_network_tab()
        self.create_preferences_tab()
        self.create_security_tab()

        layout.addWidget(self.tab_widget)

        # Action buttons
        self.create_action_buttons(layout)

    def create_paths_tab(self):
        """Create paths configuration tab"""
        tab = QWidget()
        tab.setObjectName("pathsTab")
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Paths frame
        paths_frame = QFrame()
        paths_frame.setObjectName("pathsFrame")
        paths_layout = QGridLayout()
        paths_frame.setLayout(paths_layout)

        # Source folder
        paths_layout.addWidget(QLabel("📁 Source Folder:"), 0, 0)
        self.source_label = QLabel("Not selected")
        self.source_label.setObjectName("pathDisplayLabel")
        paths_layout.addWidget(self.source_label, 0, 1)

        self.browse_source_btn = QPushButton("Browse")
        self.browse_source_btn.setObjectName("browseButton")
        self.browse_source_btn.clicked.connect(self.browse_source)
        paths_layout.addWidget(self.browse_source_btn, 0, 2)

        # Destination folder
        paths_layout.addWidget(QLabel("📤 Destination Folder:"), 1, 0)
        self.destination_label = QLabel("Not selected")
        self.destination_label.setObjectName("pathDisplayLabel")
        paths_layout.addWidget(self.destination_label, 1, 1)

        self.browse_dest_btn = QPushButton("Browse")
        self.browse_dest_btn.setObjectName("browseButton")
        self.browse_dest_btn.clicked.connect(self.browse_destination)
        paths_layout.addWidget(self.browse_dest_btn, 1, 2)

        layout.addWidget(paths_frame)

        # Connection type frame
        type_frame = QFrame()
        type_frame.setObjectName("connectionFrame")
        type_layout = QVBoxLayout()
        type_frame.setLayout(type_layout)

        type_layout.addWidget(QLabel("🌐 Connection Type:"))

        self.folder_type_group = QButtonGroup()

        connection_layout = QHBoxLayout()
        self.local_radio = QRadioButton("💻 Local Folder")
        self.local_radio.setObjectName("connectionRadio")
        self.network_radio = QRadioButton("🌐 Network Folder")
        self.network_radio.setObjectName("connectionRadio")

        self.folder_type_group.addButton(self.local_radio, 0)
        self.folder_type_group.addButton(self.network_radio, 1)

        connection_layout.addWidget(self.local_radio)
        connection_layout.addWidget(self.network_radio)
        connection_layout.addStretch()

        type_layout.addLayout(connection_layout)
        layout.addWidget(type_frame)

        layout.addStretch()

        self.tab_widget.addTab(tab, "📁 Paths")

    def create_network_tab(self):
        """Create network configuration tab"""
        tab = QWidget()
        tab.setObjectName("networkTab")
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Network frame
        network_frame = QFrame()
        network_frame.setObjectName("networkFrame")
        network_layout = QGridLayout()
        network_frame.setLayout(network_layout)

        # Network IP
        network_layout.addWidget(QLabel("🌐 Network IP Address:"), 0, 0)
        self.network_ip_input = QLineEdit()
        self.network_ip_input.setObjectName("networkInput")
        self.network_ip_input.setPlaceholderText("Enter IP address (e.g., 192.168.1.100)")
        network_layout.addWidget(self.network_ip_input, 0, 1)

        # Test connection button
        self.test_connection_btn = QPushButton("🔍 Test Connection")
        self.test_connection_btn.setObjectName("testButton")
        self.test_connection_btn.clicked.connect(self.test_network_connection)
        network_layout.addWidget(self.test_connection_btn, 0, 2)

        # Connection status
        self.connection_status = QLabel("Connection not tested")
        self.connection_status.setObjectName("connectionStatus")
        network_layout.addWidget(self.connection_status, 1, 0, 1, 3)

        layout.addWidget(network_frame)
        layout.addStretch()

        self.tab_widget.addTab(tab, "🌐 Network")

    def create_preferences_tab(self):
        """Create preferences tab"""
        tab = QWidget()
        tab.setObjectName("preferencesTab")
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Preferences frame
        prefs_frame = QFrame()
        prefs_frame.setObjectName("preferencesFrame")
        prefs_layout = QVBoxLayout()
        prefs_frame.setLayout(prefs_layout)

        # Auto-close option
        self.auto_close_checkbox = QCheckBox("🚪 Auto-close application after successful copy")
        self.auto_close_checkbox.setObjectName("autoCloseCheckbox")
        prefs_layout.addWidget(self.auto_close_checkbox)

        # Future preferences can be added here

        layout.addWidget(prefs_frame)
        layout.addStretch()

        self.tab_widget.addTab(tab, "⚙️ Preferences")

    def create_security_tab(self):
        """Create security configuration tab"""
        tab = QWidget()
        tab.setObjectName("securityTab")
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Security frame
        security_frame = QFrame()
        security_frame.setObjectName("securityFrame")
        security_layout = QGridLayout()
        security_frame.setLayout(security_layout)

        # Password
        security_layout.addWidget(QLabel("🔒 Settings Password:"), 0, 0)
        self.password_input = QLineEdit()
        self.password_input.setObjectName("passwordInput")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter new password (leave blank to keep current)")
        security_layout.addWidget(self.password_input, 0, 1)

        # Password confirmation
        security_layout.addWidget(QLabel("🔒 Confirm Password:"), 1, 0)
        self.password_confirm = QLineEdit()
        self.password_confirm.setObjectName("passwordInput")
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm.setPlaceholderText("Confirm new password")
        security_layout.addWidget(self.password_confirm, 1, 1)

        layout.addWidget(security_frame)
        layout.addStretch()

        self.tab_widget.addTab(tab, "🔒 Security")

    def create_action_buttons(self, layout):
        """Create action buttons"""
        button_frame = QFrame()
        button_frame.setObjectName("actionButtonFrame")
        button_layout = QHBoxLayout()
        button_frame.setLayout(button_layout)

        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.setObjectName("saveButton")
        self.save_btn.clicked.connect(self.save_settings)

        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addWidget(button_frame)

    def load_current_settings(self):
        """Load current settings into the dialog"""
        self.source_label.setText(self.settings.get('source_path', 'Not selected'))
        self.destination_label.setText(self.settings.get('destination_path', 'Not selected'))
        self.network_ip_input.setText(self.settings.get('network_ip', ''))
        self.auto_close_checkbox.setChecked(self.settings.get('auto_close', False))

        # Set folder type
        if self.settings.get('folder_type', 'local') == 'network':
            self.network_radio.setChecked(True)
        else:
            self.local_radio.setChecked(True)

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
        ip = self.network_ip_input.text().strip()
        if not ip:
            self.connection_status.setText("❌ Please enter an IP address")
            self.connection_status.setStyleSheet("color: #FF6B6B;")
            return

        from utils.network_checker import NetworkChecker
        checker = NetworkChecker()

        self.connection_status.setText("🔍 Testing connection...")
        self.connection_status.setStyleSheet("color: #4ECDC4;")

        # In a real app, this should be done in a separate thread
        is_connected = checker.ping_host(ip)

        if is_connected:
            self.connection_status.setText(f"✅ Successfully connected to {ip}")
            self.connection_status.setStyleSheet("color: #51CF66;")
        else:
            self.connection_status.setText(f"❌ Cannot connect to {ip}")
            self.connection_status.setStyleSheet("color: #FF6B6B;")

    def save_settings(self):
        """Save settings and close dialog"""
        try:
            # Validate passwords if provided
            new_password = self.password_input.text()
            confirm_password = self.password_confirm.text()

            if new_password and new_password != confirm_password:
                QMessageBox.warning(self, "Password Mismatch", "Passwords do not match!")
                return

            # Prepare settings dictionary
            settings = {
                'source_path': self.source_label.text() if self.source_label.text() != "Not selected" else "",
                'destination_path': self.destination_label.text() if self.destination_label.text() != "Not selected" else "",
                'network_ip': self.network_ip_input.text().strip() or "127.0.0.1",
                'folder_type': 'network' if self.network_radio.isChecked() else 'local',
                'auto_close': self.auto_close_checkbox.isChecked()
            }

            # Update password if provided
            if new_password:
                settings['password'] = new_password
            else:
                settings['password'] = self.settings.get('password', 'password123')

            # Save settings
            self.settings_manager.save_settings(settings)

            QMessageBox.information(self, "Success", "✅ Settings saved successfully!")
            self.accept()

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
