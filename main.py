#!/usr/bin/env python3
"""
Enhanced Folder Copier - Main Entry Point
A modern GUI application for copying folders with network support
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

from ui.main_window import FolderCopierApp
from utils.logger import setup_logging


def setup_application_style(app):
    """Setup modern application styling with pastel colors"""
    app.setStyle('Fusion')

    # Create a modern palette with pastel colors
    palette = QPalette()

    # Base colors - soft pastels
    background = QColor(248, 250, 252)  # Very light blue-gray
    surface = QColor(255, 255, 255)  # Pure white
    primary = QColor(147, 197, 253)  # Soft blue
    secondary = QColor(196, 181, 253)  # Soft purple
    accent = QColor(134, 239, 172)  # Soft green
    warning = QColor(254, 215, 170)  # Soft orange
    error = QColor(252, 165, 165)  # Soft red
    text_primary = QColor(31, 41, 55)  # Dark gray
    text_secondary = QColor(107, 114, 128)  # Medium gray

    # Set palette colors
    palette.setColor(QPalette.ColorRole.Window, background)
    palette.setColor(QPalette.ColorRole.WindowText, text_primary)
    palette.setColor(QPalette.ColorRole.Base, surface)
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(243, 244, 246))
    palette.setColor(QPalette.ColorRole.ToolTipBase, surface)
    palette.setColor(QPalette.ColorRole.ToolTipText, text_primary)
    palette.setColor(QPalette.ColorRole.Text, text_primary)
    palette.setColor(QPalette.ColorRole.Button, surface)
    palette.setColor(QPalette.ColorRole.ButtonText, text_primary)
    palette.setColor(QPalette.ColorRole.BrightText, error)
    palette.setColor(QPalette.ColorRole.Link, primary)
    palette.setColor(QPalette.ColorRole.Highlight, primary)
    palette.setColor(QPalette.ColorRole.HighlightedText, surface)

    app.setPalette(palette)

    # Set application font
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)


def main():
    """Main application entry point"""
    # Setup logging first
    setup_logging()

    app = QApplication(sys.argv)
    app.setApplicationName("Enhanced Folder Copier")
    app.setApplicationVersion("3.0")
    app.setOrganizationName("OpenSource")
    app.setOrganizationDomain("github.com")

    # Setup modern styling
    setup_application_style(app)

    try:
        window = FolderCopierApp()
        window.show()

        logging.info("Application started successfully")
        sys.exit(app.exec())

    except Exception as e:
        logging.critical(f"Failed to start application: {str(e)}")
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Critical Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()