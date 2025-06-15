"""
Copy Worker Thread - Enhanced Folder Copier
Handles folder copying operations in a separate thread
"""

import os
import shutil
import logging
from PyQt6.QtCore import QThread, pyqtSignal


class CopyWorker(QThread):
    """Worker thread for copying operations to prevent UI freezing"""

    finished = pyqtSignal(bool, str)
    progress_update = pyqtSignal(str)

    def __init__(self, source_path, destination_path):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path

    def run(self):
        """Main copy operation"""
        try:
            # Validate source path
            if not os.path.exists(self.source_path):
                self.finished.emit(False, f"Source folder does not exist:\n{self.source_path}")
                return

            if not os.path.isdir(self.source_path):
                self.finished.emit(False, f"Source path is not a directory:\n{self.source_path}")
                return

            # Handle existing destination folder
            if os.path.exists(self.destination_path):
                self.progress_update.emit("Destination exists, creating backup...")
                self.handle_existing_destination()

            # Start copying
            self.progress_update.emit("Copying folder contents...")
            self.copy_with_progress()

            # Success
            success_msg = f"✅ Folder copied successfully!\n\nFrom: {self.source_path}\nTo: {self.destination_path}"
            self.finished.emit(True, success_msg)
            logging.info(f"Successfully copied {self.source_path} to {self.destination_path}")

        except PermissionError as e:
            error_msg = f"❌ Permission denied:\n{str(e)}\n\nTry running as administrator or check folder permissions."
            logging.error(f"Permission error: {str(e)}")
            self.finished.emit(False, error_msg)

        except FileNotFoundError as e:
            error_msg = f"❌ File or folder not found:\n{str(e)}"
            logging.error(f"File not found: {str(e)}")
            self.finished.emit(False, error_msg)

        except OSError as e:
            error_msg = f"❌ System error occurred:\n{str(e)}\n\nCheck disk space and network connectivity."
            logging.error(f"OS error: {str(e)}")
            self.finished.emit(False, error_msg)

        except Exception as e:
            error_msg = f"❌ Unexpected error occurred:\n{str(e)}"
            logging.error(f"Unexpected error: {str(e)}")
            self.finished.emit(False, error_msg)

    def handle_existing_destination(self):
        """Handle existing destination folder according to specified logic"""
        base_name = self.destination_path
        old_name = f"{base_name}_old"

        try:
            # If *_old exists, delete it
            if os.path.exists(old_name):
                self.progress_update.emit("Removing old backup...")
                if os.path.isdir(old_name):
                    shutil.rmtree(old_name)
                else:
                    os.remove(old_name)
                logging.info(f"Deleted existing backup: {old_name}")

            # Rename existing folder to *_old
            self.progress_update.emit("Creating backup of existing folder...")
            os.rename(self.destination_path, old_name)
            logging.info(f"Renamed {self.destination_path} to {old_name}")

        except Exception as e:
            error_msg = f"Error handling existing destination: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def copy_with_progress(self):
        """Copy folder with progress updates"""
        try:
            # Count total files for progress (optional enhancement)
            total_files = self.count_files(self.source_path)
            current_file = 0

            def copy_progress(src, dst):
                nonlocal current_file
                current_file += 1
                if total_files > 0:
                    progress_text = f"Copying files... ({current_file}/{total_files})"
                else:
                    progress_text = f"Copying files... ({current_file} files)"
                self.progress_update.emit(progress_text)

            # Use copytree with copy_function for progress
            shutil.copytree(
                self.source_path,
                self.destination_path,
                copy_function=lambda src, dst: self.copy_file_with_callback(src, dst, copy_progress)
            )

        except Exception as e:
            # Fallback to simple copytree if progress version fails
            logging.warning(f"Progress copy failed, using simple copy: {str(e)}")
            shutil.copytree(self.source_path, self.destination_path)

    def copy_file_with_callback(self, src, dst, callback):
        """Copy individual file with callback"""
        try:
            shutil.copy2(src, dst)
            callback(src, dst)
        except Exception as e:
            logging.warning(f"Failed to copy {src}: {str(e)}")
            raise

    def count_files(self, path):
        """Count total files in directory (for progress calculation)"""
        try:
            total = 0
            for root, dirs, files in os.walk(path):
                total += len(files)
            return total
        except Exception as e:
            logging.warning(f"Could not count files: {str(e)}")
            return 0