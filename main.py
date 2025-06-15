#!/usr/bin/env python3
"""
Enhanced Folder Copier - Main Application
Modern GUI with pastel colors and enhanced features
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette, QColor

# Import our custom modules
from main_window import FolderCopierApp
from logger import setup_logging
from theme_manager import apply_theme


def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()

    app = QApplication(sys.argv)
    app.setApplicationName("Enhanced Folder Copier")
    app.setApplicationVersion("3.0")

    # Apply modern theme
    apply_theme(app)

    try:
        # Set application icon
        current_directory = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_directory, 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))

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