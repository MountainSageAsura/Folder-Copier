"""
Password Dialog - Enhanced Folder Copier
Modern password authentication dialog
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QLineEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PasswordDialog(QDialog):
    """Modern password authentication dialog"""

    def __init__(self, correct_password, parent=None):
        super().__init__(parent)
        self.correct_password = correct_password

        self.setWindowTitle("Authentication Required")
        self.setFixedSize(400, 200)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the password dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        # Header
        header_frame = QFrame()
        header_frame.setObjectName("passwordHeaderFrame")
        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)

        # Icon and title
        icon_label = QLabel("🔐")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setObjectName("passwordIcon")
        header_layout.addWidget(icon_label)

        title_label = QLabel("Enter Password")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("passwordTitle")
        header_layout.addWidget(title_label)

        desc_label = QLabel("Authentication required to access settings")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setObjectName("passwordDescription")
        header_layout.addWidget(desc_label)

        layout.addWidget(header_frame)

        # Password input frame
        input_frame = QFrame()
        input_frame.setObjectName("passwordInputFrame")
        input_layout = QVBoxLayout()
        input_frame.setLayout(input_layout)

        self.password_input = QLineEdit()
        self.password_input.setObjectName("passwordInputField")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password...")
        self.password_input.returnPressed.connect(self.check_password)
        input_layout.addWidget(self.password_input)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setObjectName("passwordError")
        self.error_label.setVisible(False)
        input_layout.addWidget(self.error_label)

        layout.addWidget(input_frame)

        # Buttons
        button_frame = QFrame()
        button_frame.setObjectName("passwordButtonFrame")
        button_layout = QHBoxLayout()
        button_frame.setLayout(button_layout)

        self.ok_button = QPushButton("🔓 Unlock")
        self.ok_button.setObjectName("unlockButton")
        self.ok_button.clicked.connect(self.check_password)
        self.ok_button.setDefault(True)

        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.setObjectName("cancelPasswordButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(button_frame)

        # Focus on password input
        self.password_input.setFocus()

    def check_password(self):
        """Check if entered password is correct"""
        entered_password = self.password_input.text()

        if entered_password == self.correct_password:
            self.accept()
        else:
            self.error_label.setText("❌ Incorrect password. Please try again.")
            self.error_label.setVisible(True)
            self.password_input.clear()
            self.password_input.setFocus()

            # Add shake effect (visual feedback)
            self.password_input.setStyleSheet(
                "QLineEdit { border: 2px solid #FF6B6B; }"
            )

    def get_password(self):
        """Get the entered password"""
        return self.password_input.text()