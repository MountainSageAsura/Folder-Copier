"""
Modern UI Styles for Enhanced Folder Copier
Pastel color palette inspired by modern design trends
"""


class ModernStyles:
    """Collection of modern CSS styles with pastel color palette"""

    # Color Palette - Soft Pastels
    COLORS = {
        'background': '#f8fafc',  # Very light blue-gray
        'surface': '#ffffff',  # Pure white
        'surface_variant': '#f1f5f9',  # Light gray-blue
        'primary': '#93c5fd',  # Soft blue
        'primary_dark': '#60a5fa',  # Medium blue
        'secondary': '#c4b5fd',  # Soft purple
        'accent': '#86efac',  # Soft green
        'warning': '#fed7aa',  # Soft orange
        'error': '#fca5a5',  # Soft red
        'success': '#bbf7d0',  # Soft green
        'text_primary': '#1f2937',  # Dark gray
        'text_secondary': '#6b7280',  # Medium gray
        'text_light': '#9ca3af',  # Light gray
        'border': '#e5e7eb',  # Light border
        'shadow': 'rgba(0, 0, 0, 0.1)'  # Subtle shadow
    }

    @classmethod
    def get_main_window_style(cls):
        """Main window styling"""
        return f"""
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}
        """

    @classmethod
    def get_content_frame_style(cls):
        """Content frame styling"""
        return f"""
        QFrame {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 12px;
            padding: 20px;
            margin: 5px;
        }}
        """

    @classmethod
    def get_progress_frame_style(cls):
        """Progress section frame styling"""
        return f"""
        QFrame {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 15px;
            margin: 5px;
        }}
        """

    @classmethod
    def get_primary_button_style(cls):
        """Primary action button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['primary']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: {cls.COLORS['primary_dark']};
            transform: translateY(-1px);
        }}
        QPushButton:pressed {{
            background-color: {cls.COLORS['primary_dark']};
            transform: translateY(0px);
        }}
        QPushButton:disabled {{
            background-color: {cls.COLORS['text_light']};
            color: {cls.COLORS['surface']};
        }}
        """

    @classmethod
    def get_secondary_button_style(cls):
        """Secondary button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['secondary']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: #a78bfa;
            transform: translateY(-1px);
        }}
        QPushButton:pressed {{
            background-color: #a78bfa;
            transform: translateY(0px);
        }}
        """

    @classmethod
    def get_logout_button_style(cls):
        """Logout button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['error']};
            color: {cls.COLORS['surface']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 500;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: #f87171;
        }}
        """

    @classmethod
    def get_refresh_button_style(cls):
        """Refresh button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['accent']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #6ee7b7;
        }}
        """

    @classmethod
    def get_path_label_style(cls):
        """Path display label styling"""
        return f"""
        QLabel {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 10px;
            color: {cls.COLORS['text_primary']};
            font-size: 13px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        """

    @classmethod
    def get_info_label_style(cls):
        """Info label styling"""
        return f"""
        QLabel {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 8px 12px;
            color: {cls.COLORS['text_secondary']};
            font-size: 13px;
            font-weight: 500;
        }}
        """

    @classmethod
    def get_progress_bar_style(cls):
        """Progress bar styling"""
        return f"""
        QProgressBar {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 8px;
            background-color: {cls.COLORS['surface']};
            text-align: center;
            font-weight: 600;
            color: {cls.COLORS['text_primary']};
        }}
        QProgressBar::chunk {{
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 {cls.COLORS['primary']},
                stop: 1 {cls.COLORS['accent']}
            );
            border-radius: 6px;
        }}
        """

    @classmethod
    def get_dialog_style(cls):
        """Dialog window styling"""
        return f"""
        QDialog {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}
        """

    @classmethod
    def get_tab_style(cls):
        """Tab widget styling"""
        return f"""
        QTabWidget::pane {{
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            background-color: {cls.COLORS['surface']};
            margin-top: 5px;
        }}
        QTabBar::tab {{
            background-color: {cls.COLORS['surface_variant']};
            color: {cls.COLORS['text_secondary']};
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 1px solid {cls.COLORS['border']};
            border-bottom: none;
        }}
        QTabBar::tab:selected {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            font-weight: 600;
        }}
        QTabBar::tab:hover {{
            background-color: {cls.COLORS['primary']};
            color: {cls.COLORS['text_primary']};
        }}
        """

    @classmethod
    def get_settings_frame_style(cls):
        """Settings section frame styling"""
        return f"""
        QFrame {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 15px;
            margin: 5px;
        }}
        """

    @classmethod
    def get_input_style(cls):
        """Input field styling"""
        return f"""
        QLineEdit {{
            background-color: {cls.COLORS['surface']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            color: {cls.COLORS['text_primary']};
        }}
        QLineEdit:focus {{
            border-color: {cls.COLORS['primary']};
            background-color: {cls.COLORS['surface']};
        }}
        QLineEdit:hover {{
            border-color: {cls.COLORS['primary_dark']};
        }}
        """

    @classmethod
    def get_password_input_style(cls):
        """Password input styling"""
        return f"""
        QLineEdit {{
            background-color: {cls.COLORS['surface']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 12px;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        QLineEdit:focus {{
            border-color: {cls.COLORS['primary']};
            background-color: {cls.COLORS['surface']};
        }}
        """

    @classmethod
    def get_path_display_style(cls):
        """Path display in settings styling"""
        return f"""
        QLabel {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 12px;
            color: {cls.COLORS['text_primary']};
            font-size: 12px;
            font-family: 'Consolas', 'Monaco', monospace;
            min-height: 20px;
        }}
        """

    @classmethod
    def get_browse_button_style(cls):
        """Browse button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['accent']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-size: 12px;
            font-weight: 600;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: #6ee7b7;
        }}
        """

    @classmethod
    def get_radio_button_style(cls):
        """Radio button styling"""
        return f"""
        QRadioButton {{
            color: {cls.COLORS['text_primary']};
            font-size: 13px;
            font-weight: 500;
            spacing: 8px;
        }}
        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
        }}
        QRadioButton::indicator:unchecked {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 8px;
            background-color: {cls.COLORS['surface']};
        }}
        QRadioButton::indicator:checked {{
            border: 2px solid {cls.COLORS['primary']};
            border-radius: 8px;
            background-color: {cls.COLORS['primary']};
        }}
        """

    @classmethod
    def get_checkbox_style(cls):
        """Checkbox styling"""
        return f"""
        QCheckBox {{
            color: {cls.COLORS['text_primary']};
            font-size: 13px;
            font-weight: 500;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}
        QCheckBox::indicator:unchecked {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            background-color: {cls.COLORS['surface']};
        }}
        QCheckBox::indicator:checked {{
            border: 2px solid {cls.COLORS['primary']};
            border-radius: 4px;
            background-color: {cls.COLORS['primary']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMC42IDEuNEw0LjMgNy43TDEuNCA0LjgiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }}
        """

    @classmethod
    def get_test_button_style(cls):
        """Test connection button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['warning']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: #fdba74;
        }}
        """

    @classmethod
    def get_save_button_style(cls):
        """Save button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['success']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: #a7f3d0;
        }}
        """

    @classmethod
    def get_cancel_button_style(cls):
        """Cancel button styling"""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_secondary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: {cls.COLORS['surface_variant']};
            border-color: {cls.COLORS['text_light']};
        }}
        """

    @classmethod
    def get_success_label_style(cls):
        """Success label styling"""
        return f"""
        QLabel {{
            background-color: {cls.COLORS['success']};
            border: 1px solid #10b981;
            border-radius: 6px;
            padding: 8px 12px;
            color: #065f46;
            font-size: 13px;
            font-weight: 600;
        }}
        """

    @classmethod
    def get_input_frame_style(cls):
        """Input frame styling"""
        return f"""
        QFrame {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            padding: 15px;
        }}
        """