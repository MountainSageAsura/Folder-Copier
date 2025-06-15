"""
Password Dialog UI for Enhanced Folder Copier
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter

# Try different import methods
try:
    from utils.styles import ModernStyles
except ImportError:
    try:
        # Try relative import
        from ..utils.styles import ModernStyles
    except ImportError:
        try:
            # Try direct import if running from project root
            import sys
            import os

            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from utils.styles import ModernStyles
        except ImportError:
            # Fallback styles if all imports fail
            class ModernStyles:
                @staticmethod
                def get_dialog_style():
                    return """
                    QDialog {
                        background-color: #f8fafc;
                        color: #1f2937;
                    }
                    """

                @staticmethod
                def get_input_frame_style():
                    return """
                    QFrame {
                        background-color: #ffffff;
                        border: 1px solid #e5e7eb;
                        border-radius: 8px;
                        padding: 15px;
                    }
                    """

                @staticmethod
                def get_password_input_style():
                    return """
                    QLineEdit {
                        background-color: #ffffff;
                        border: 2px solid #e5e7eb;
                        border-radius: 6px;
                        padding: 12px;
                        font-size: 14px;
                        color: #1f2937;
                    }
                    QLineEdit:focus {
                        border-color: #93c5fd;
                    }
                    """

                @staticmethod
                def get_cancel_button_style():
                    return """
                    QPushButton {
                        background-color: #ffffff;
                        color: #6b7280;
                        border: 2px solid #e5e7eb;
                        border-radius: 8px;
                        padding: 12px 24px;
                        font-size: 14px;
                        font-weight: 600;
                        min-width: 120px;
                    }
                    QPushButton:hover {
                        background-color: #f1f5f9;
                    }
                    """

                @staticmethod
                def get_primary_button_style():
                    return """
                    QPushButton {
                        background-color: #93c5fd;
                        color: #1f2937;
                        border: none;
                        border-radius: 8px;
                        padding: 12px 24px;
                        font-size: 14px;
                        font-weight: 600;
                        min-width: 120px;
                    }
                    QPushButton:hover {
                        background-color: #60a5fa;
                    }
                    """


class PasswordDialog(QDialog):
    """Modern password authentication dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Authentication Required")
        self.setFixedSize(650, 400)  # Reduced height since horizontal layout takes less vertical space
        self.setModal(True)

        # Set custom lock icon FIRST before setup_ui
        self.set_custom_icon()
        self.setup_ui()

    def set_custom_icon(self):
        """Set custom lock emoji icon for the dialog"""
        try:
            # Create a pixmap with the lock emoji
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Set font for emoji
            font = QFont("Segoe UI Emoji", 20)
            painter.setFont(font)

            # Draw the lock emoji
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🔒")
            painter.end()

            # Set the icon
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

        except Exception as e:
            # Fallback - no icon
            pass

    def setup_ui(self):
        """Setup the password dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Reduced spacing for tighter layout
        layout.setContentsMargins(60, 60, 60, 60)  # Keep good margins

        # Apply modern styling
        self.setStyleSheet(ModernStyles.get_dialog_style())

        # Title with lock emoji - make it much more visible
        title_label = QLabel("🔒 Enter Password")
        title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))  # Much larger font
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "color: #1f2937; margin-bottom: 15px; padding: 10px; background-color: rgba(147, 197, 253, 0.1); border-radius: 8px;")
        title_label.setMinimumHeight(70)  # Slightly reduced height
        layout.addWidget(title_label)

        # Subtitle with more space and larger font
        subtitle_label = QLabel("Please enter your password to access settings")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 12))  # Larger subtitle font
        subtitle_label.setStyleSheet("color: #6b7280; margin-bottom: 10px; padding: 5px;")
        subtitle_label.setMinimumHeight(40)  # Reduced height to move input frame up
        layout.addWidget(subtitle_label)

        # Password input frame positioned closer to subtitle
        # Password input frame with horizontal layout
        # Password input frame with horizontal layout
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                padding: 5px;
                margin-top: 3px;
                margin-left: 5px;
                margin-right: 40px;
            }
        """)

        # Horizontal layout for label and input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(5, 5, 10, 10) # left, top, right, bottom
        input_frame.setLayout(input_layout)

        # Password label (aligned right, fixed width)
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Segoe UI", 14))
        password_label.setStyleSheet("color: #374151; boarder: none; background: transparent;")
        password_label.setFixedWidth(150)
        password_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        input_layout.addWidget(password_label)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password...")
        self.password_input.setFont(QFont("Segoe UI", 14))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                color: #1f2937;
            }
            QLineEdit:focus {
                border-color: #93c5fd;
            }
        """)
        self.password_input.setMinimumHeight(40)
        self.password_input.setMinimumWidth(300)
        self.password_input.setMaximumWidth(360)
        self.password_input.returnPressed.connect(self.accept)
        input_layout.addWidget(self.password_input)

        layout.addWidget(input_frame)

        # Add stretch to push buttons down
        layout.addStretch()

        # Buttons with much better sizing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)  # More space between buttons
        button_layout.setContentsMargins(30, 20, 30, 30)  # More padding around buttons

        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))  # Larger button font
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #6b7280;
                border: 3px solid #e5e7eb;
                border-radius: 10px;
                padding: 18px 35px;
                font-size: 16px;
                font-weight: 600;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-color: #9ca3af;
            }
        """)
        self.cancel_button.setMinimumHeight(60)  # Larger button height
        self.cancel_button.clicked.connect(self.reject)

        self.ok_button = QPushButton("🔓 Unlock")
        self.ok_button.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))  # Larger button font
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #93c5fd;
                color: #1f2937;
                border: none;
                border-radius: 10px;
                padding: 18px 35px;
                font-size: 16px;
                font-weight: 600;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #60a5fa;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #60a5fa;
                transform: translateY(0px);
            }
        """)
        self.ok_button.setMinimumHeight(60)  # Larger button height
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addStretch()

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