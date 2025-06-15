"""
Theme Manager for Folder Copier Application
Provides modern pastel color theming inspired by comic book converters
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import QApplication


class ThemeManager(QObject):
    """Manages application themes and styling"""

    theme_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_theme = "pastel_modern"

    def get_theme_styles(self):
        """Get current theme stylesheet"""
        if self.current_theme == "pastel_modern":
            return self._get_pastel_modern_theme()
        return self._get_default_theme()

    def _get_pastel_modern_theme(self):
        """Modern pastel theme inspired by comic book converters"""
        return """
        /* Main Application Styling */
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            color: #2d3436;
        }

        /* Central Widget */
        QWidget {
            background-color: transparent;
            color: #2d3436;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }

        /* Title Label */
        QLabel#title {
            font-size: 24pt;
            font-weight: bold;
            color: #6c5ce7;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #a29bfe, stop:1 #6c5ce7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 15px;
            border-radius: 12px;
            margin: 10px;
        }

        /* Path Information Frame */
        QFrame#pathFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9ff);
            border: 2px solid #ddd6fe;
            border-radius: 15px;
            padding: 15px;
            margin: 10px;
        }

        /* Path Labels */
        QLabel#pathLabel {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffeaa7, stop:1 #fdcb6e);
            border: 2px solid #e17055;
            border-radius: 8px;
            padding: 8px 12px;
            color: #2d3436;
            font-weight: 500;
            min-height: 20px;
        }

        /* Status Labels */
        QLabel#statusLabel {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #81ecec, stop:1 #74b9ff);
            border: 2px solid #0984e3;
            border-radius: 10px;
            padding: 10px;
            color: #2d3436;
            font-weight: 500;
            font-size: 11pt;
        }

        /* Network Status */
        QLabel#networkStatus {
            border-radius: 8px;
            padding: 6px 12px;
            font-weight: bold;
            margin: 5px;
        }

        QLabel#networkOnline {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #55efc4, stop:1 #00b894);
            color: #00695c;
            border: 2px solid #00b894;
        }

        QLabel#networkOffline {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fd79a8, stop:1 #e84393);
            color: #741b47;
            border: 2px solid #e84393;
        }

        /* Radio Buttons */
        QRadioButton {
            font-size: 11pt;
            font-weight: 500;
            color: #2d3436;
            spacing: 8px;
            padding: 5px;
        }

        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border-radius: 9px;
            border: 2px solid #a29bfe;
            background: #ffffff;
        }

        QRadioButton::indicator:checked {
            background: qradialradient(cx:0.5, cy:0.5, radius:0.5,
                stop:0 #6c5ce7, stop:0.7 #6c5ce7, stop:1 #a29bfe);
            border: 2px solid #5f3dc4;
        }

        QRadioButton::indicator:hover {
            border: 2px solid #6c5ce7;
            background: #f8f9ff;
        }

        /* Primary Buttons */
        QPushButton#primaryButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #a29bfe, stop:1 #6c5ce7);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 12pt;
            font-weight: bold;
            min-height: 20px;
        }

        QPushButton#primaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #b8b5ff, stop:1 #7d73e8);
            transform: translateY(-2px);
        }

        QPushButton#primaryButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #8b7ff5, stop:1 #5a52d5);
        }

        QPushButton#primaryButton:disabled {
            background: #ddd6fe;
            color: #9ca3af;
        }

        /* Secondary Buttons */
        QPushButton#secondaryButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00cec9, stop:1 #00b894);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 12pt;
            font-weight: bold;
            min-height: 20px;
        }

        QPushButton#secondaryButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #17e8e2, stop:1 #00d4aa);
        }

        QPushButton#secondaryButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00a8a3, stop:1 #009688);
        }

        /* Accent Buttons */
        QPushButton#accentButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fdcb6e, stop:1 #e17055);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 10pt;
            font-weight: 600;
        }

        QPushButton#accentButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffd93d, stop:1 #f39c12);
        }

        /* Small Buttons */
        QPushButton#smallButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #74b9ff, stop:1 #0984e3);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 9pt;
            font-weight: 500;
            min-width: 60px;
        }

        QPushButton#smallButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #81b3ff, stop:1 #2196f3);
        }

        /* Progress Bar */
        QProgressBar {
            background: #f1f3f4;
            border: 2px solid #ddd6fe;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            color: #2d3436;
            height: 24px;
        }

        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #a29bfe, stop:0.5 #6c5ce7, stop:1 #5f3dc4);
            border-radius: 10px;
            margin: 2px;
        }

        /* Dialog Styling */
        QDialog {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9ff);
            border: 2px solid #ddd6fe;
            border-radius: 15px;
        }

        /* Line Edit */
        QLineEdit {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9ff);
            border: 2px solid #ddd6fe;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 10pt;
            color: #2d3436;
        }

        QLineEdit:focus {
            border: 2px solid #a29bfe;
            background: #ffffff;
        }

        QLineEdit:hover {
            border: 2px solid #b8b5ff;
        }

        /* Combo Box */
        QComboBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9ff);
            border: 2px solid #ddd6fe;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 10pt;
            color: #2d3436;
        }

        QComboBox:hover {
            border: 2px solid #a29bfe;
        }

        QComboBox::drop-down {
            border: none;
            width: 20px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #6c5ce7;
        }

        /* Checkbox */
        QCheckBox {
            font-size: 10pt;
            color: #2d3436;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #a29bfe;
            border-radius: 4px;
            background: #ffffff;
        }

        QCheckBox::indicator:checked {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #a29bfe, stop:1 #6c5ce7);
            border: 2px solid #5f3dc4;
        }

        QCheckBox::indicator:hover {
            border: 2px solid #6c5ce7;
            background: #f8f9ff;
        }

        /* Scrollbar */
        QScrollBar:vertical {
            background: #f1f3f4;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #a29bfe, stop:1 #6c5ce7);
            border-radius: 6px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #b8b5ff, stop:1 #7d73e8);
        }

        /* Tooltips */
        QToolTip {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2d3436, stop:1 #636e72);
            color: white;
            border: 1px solid #74b9ff;
            border-radius: 6px;
            padding: 6px;
            font-size: 9pt;
        }
        """

    def _get_default_theme(self):
        """Default theme fallback"""
        return """
        QMainWindow {
            background-color: #f0f0f0;
            color: #333333;
        }

        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0056b3;
        }

        QPushButton:pressed {
            background-color: #004494;
        }
        """

    def apply_theme(self, app: QApplication):
        """Apply the current theme to the application"""
        app.setStyleSheet(self.get_theme_styles())

        # Set application font
        font = QFont("Segoe UI", 10)
        font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
        app.setFont(font)

        self.theme_changed.emit()

    def set_theme(self, theme_name: str):
        """Change the current theme"""
        if theme_name in ["pastel_modern", "default"]:
            self.current_theme = theme_name
            return True
        return False

    def get_color(self, color_name: str) -> str:
        """Get specific colors from the theme"""
        colors = {
            "primary": "#6c5ce7",
            "secondary": "#00b894",
            "accent": "#e17055",
            "success": "#00b894",
            "warning": "#fdcb6e",
            "error": "#e84393",
            "info": "#74b9ff",
            "background": "#f8f9fa",
            "surface": "#ffffff",
            "text": "#2d3436",
            "text_secondary": "#636e72"
        }
        return colors.get(color_name, "#000000")