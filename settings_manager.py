"""
Settings Manager for Enhanced Folder Copier
Handles loading and saving application settings
"""

import json
import os
import logging
from typing import Dict, Any


class SettingsManager:
    """Manages application settings with JSON persistence"""

    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "source_path": "",
            "destination_path": "",
            "network_ip": "127.0.0.1",
            "password": "password123",
            "folder_type": "local",
            "auto_close": False,
            "version": "3.0"
        }

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file, return defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as file:
                    settings = json.load(file)

                # Merge with defaults to ensure all keys exist
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)

                logging.info("Settings loaded successfully")
                return merged_settings
            else:
                logging.info("Settings file not found, using defaults")
                return self.default_settings.copy()

        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in settings file: {str(e)}")
            return self.default_settings.copy()

        except Exception as e:
            logging.error(f"Failed to load settings: {str(e)}")
            return self.default_settings.copy()

    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            # Ensure all required keys exist
            final_settings = self.default_settings.copy()
            final_settings.update(settings)

            # Create backup of existing settings
            if os.path.exists(self.settings_file):
                backup_file = f"{self.settings_file}.backup"
                try:
                    with open(self.settings_file, "r", encoding="utf-8") as src:
                        with open(backup_file, "w", encoding="utf-8") as dst:
                            dst.write(src.read())
                except Exception as e:
                    logging.warning(f"Failed to create settings backup: {str(e)}")

            # Save new settings
            with open(self.settings_file, "w", encoding="utf-8") as file:
                json.dump(final_settings, file, indent=2, ensure_ascii=False)

            logging.info("Settings saved successfully")
            return True

        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def reset_to_defaults(self) -> Dict[str, Any]:
        """Reset settings to defaults and save"""
        try:
            self.save_settings(self.default_settings.copy())
            logging.info("Settings reset to defaults")
            return self.default_settings.copy()
        except Exception as e:
            logging.error(f"Failed to reset settings: {str(e)}")
            raise

    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        settings = self.load_settings()
        return settings.get(key, default)

    def set_setting(self, key: str, value: Any):
        """Set a specific setting value"""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)

    def validate_settings(self, settings: Dict[str, Any]) -> tuple[bool, str]:
        """Validate settings dictionary"""
        try:
            # Check required string fields
            string_fields = ["source_path", "destination_path", "network_ip", "password", "folder_type"]
            for field in string_fields:
                if field in settings and not isinstance(settings[field], str):
                    return False, f"Field '{field}' must be a string"

            # Check boolean fields
            bool_fields = ["auto_close"]
            for field in bool_fields:
                if field in settings and not isinstance(settings[field], bool):
                    return False, f"Field '{field}' must be a boolean"

            # Check folder type values
            if "folder_type" in settings and settings["folder_type"] not in ["local", "network"]:
                return False, "folder_type must be 'local' or 'network'"

            # Check paths exist if specified
            if settings.get("source_path") and not os.path.exists(settings["source_path"]):
                return False, f"Source path does not exist: {settings['source_path']}"

            return True, "Settings are valid"

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def export_settings(self, export_path: str) -> bool:
        """Export current settings to a file"""
        try:
            settings = self.load_settings()
            # Remove sensitive information for export
            export_settings = settings.copy()
            export_settings.pop("password", None)

            with open(export_path, "w", encoding="utf-8") as file:
                json.dump(export_settings, file, indent=2, ensure_ascii=False)

            logging.info(f"Settings exported to {export_path}")
            return True

        except Exception as e:
            logging.error(f"Failed to export settings: {str(e)}")
            return False

    def import_settings(self, import_path: str) -> bool:
        """Import settings from a file"""
        try:
            if not os.path.exists(import_path):
                raise FileNotFoundError(f"Import file not found: {import_path}")

            with open(import_path, "r", encoding="utf-8") as file:
                imported_settings = json.load(file)

            # Validate imported settings
            is_valid, error_msg = self.validate_settings(imported_settings)
            if not is_valid:
                raise ValueError(f"Invalid settings: {error_msg}")

            # Merge with current settings (preserve password if not in import)
            current_settings = self.load_settings()
            current_settings.update(imported_settings)

            self.save_settings(current_settings)
            logging.info(f"Settings imported from {import_path}")
            return True

        except Exception as e:
            logging.error(f"Failed to import settings: {str(e)}")
            return False