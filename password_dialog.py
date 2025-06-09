"""
Password Dialog UI for Enhanced Folder Copier
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from utils.styles import ModernStyles


class PasswordDialog(QDialog):
    """Modern password authentication dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔒 Authentication Required")
        self.setFixedSize(400, 200)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the password dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Apply modern styling
        self.setStyleSheet(ModernStyles.get_dialog_style())

        # Title
        title_label = QLabel("🔐 Enter Password")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1f2937; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Please enter your password to access settings")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #6b7280; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)

        # Password input frame
        input_frame = QFrame()
        input_frame.setStyleSheet(ModernStyles.get_input_frame_style())
        input_layout = QVBoxLayout()
        input_frame.setLayout(input_layout)

        # Password input
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #374151; font-weight: 500; margin-bottom: 5px;")
        input_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password...")
        self.password_input.setStyleSheet(ModernStyles.get_password_input_style())
        self.password_input.returnPressed.connect(self.accept)
        input_layout.addWidget(self.password_input)

        layout.addWidget(input_frame)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.setStyleSheet(ModernStyles.get_cancel_button_style())
        self.cancel_button.clicked.connect(self.reject)

        self.ok_button = QPushButton("🔓 Unlock")
        self.ok_button.setStyleSheet(ModernStyles.get_primary_button_style())
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Focus on password input
        self.password_input.setFocus()

    def get_password(self):
        """Get the entered password"""
        return self.password_input.text()

    def showEvent(self, event):
        """Clear password field when dialog is shown"""
        super().showEvent(event)
        self.password_input.clear()
        self.password_input.setFocus()