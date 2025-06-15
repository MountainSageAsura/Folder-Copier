"""
Settings Manager - Enhanced Folder Copier
Handles loading and saving application settings
"""

import json
import os
import logging
from typing import Dict, Any


class SettingsManager:
    """Manages application settings with JSON file storage"""

    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            'source_path': '',
            'destination_path': '',
            'network_ip': '127.0.0.1',
            'password': 'password123',
            'folder_type': 'local',
            'auto_close': False
        }

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    settings = json.load(file)

                # Ensure all default keys exist
                for key, default_value in self.default_settings.items():
                    if key not in settings:
                        settings[key] = default_value

                logging.info("Settings loaded successfully")
                return settings
            else:
                logging.info("Settings file not found, using defaults")
                return self.default_settings.copy()

        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in settings file: {str(e)}")
            return self.default_settings.copy()

        except Exception as e:
            logging.error(f"Failed to load settings: {str(e)}")
            return self.default_settings.copy()

    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings to file"""
        try:
            # Validate settings against defaults
            validated_settings = {}
            for key, default_value in self.default_settings.items():
                if key in settings:
                    validated_settings[key] = settings[key]
                else:
                    validated_settings[key] = default_value

            # Create backup of existing settings
            if os.path.exists(self.settings_file):
                backup_file = f"{self.settings_file}.backup"
                try:
                    with open(self.settings_file, 'r', encoding='utf-8') as src:
                        with open(backup_file, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                except Exception as e:
                    logging.warning(f"Could not create settings backup: {str(e)}")

            # Save new settings
            with open(self.settings_file, 'w', encoding='utf-8') as file:
                json.dump(validated_settings, file, indent=2, ensure_ascii=False)

            logging.info("Settings saved successfully")

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def reset_to_defaults(self) -> Dict[str, Any]:
        """Reset settings to default values"""
        try:
            default_copy = self.default_settings.copy()
            self.save_settings(default_copy)
            logging.info("Settings reset to defaults")
            return default_copy
        except Exception as e:
            logging.error(f"Failed to reset settings: {str(e)}")
            raise

    def get_setting(self, key: str, default=None) -> Any:
        """Get a specific setting value"""
        settings = self.load_settings()
        return settings.get(key, default)

    def update_setting(self, key: str, value: Any) -> None:
        """Update a specific setting"""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)

    def validate_paths(self, settings: Dict[str, Any]) -> bool:
        """Validate that configured paths exist and are accessible"""
        source_path = settings.get('source_path', '')
        destination_path = settings.get('destination_path', '')

        if not source_path or not destination_path:
            return False

        if not os.path.exists(source_path):
            logging.warning(f"Source path does not exist: {source_path}")
            return False

        if not os.path.isdir(source_path):
            logging.warning(f"Source path is not a directory: {source_path}")
            return False

        # Check if destination directory can be created
        destination_parent = os.path.dirname(destination_path)
        if destination_parent and not os.path.exists(destination_parent):
            try:
                os.makedirs(destination_parent, exist_ok=True)
            except Exception as e:
                logging.warning(f"Cannot create destination parent directory: {str(e)}")
                return False

        return True