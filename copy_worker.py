"""
Copy Worker Thread for Enhanced Folder Copier
Handles folder copying operations in a separate thread to prevent UI freezing
"""

import os
import shutil
import logging
from PyQt6.QtCore import QThread, pyqtSignal


class CopyWorker(QThread):
    """Worker thread for copying operations to prevent UI freezing"""

    # Signals
    finished = pyqtSignal(bool, str)  # success, message
    progress_update = pyqtSignal(str)  # status message

    def __init__(self, source_path, destination_path):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path

    def run(self):
        """Main copy operation running in separate thread"""
        try:
            # Validate source path
            if not os.path.exists(self.source_path):
                self.finished.emit(False, f"Source folder does not exist: {self.source_path}")
                return

            if not os.path.isdir(self.source_path):
                self.finished.emit(False, f"Source path is not a directory: {self.source_path}")
                return

            # Handle existing destination folder
            if os.path.exists(self.destination_path):
                self.progress_update.emit("Destination exists, creating backup...")
                self.handle_existing_destination()

            # Start copying
            self.progress_update.emit("Copying folder contents...")
            self.copy_with_progress(self.source_path, self.destination_path)

            # Success
            self.finished.emit(True, "✅ Folder copied successfully!")
            logging.info(f"Successfully copied {self.source_path} to {self.destination_path}")

        except PermissionError as e:
            error_msg = f"❌ Permission denied: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)

        except FileNotFoundError as e:
            error_msg = f"❌ File or folder not found: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)

        except OSError as e:
            error_msg = f"❌ System error occurred: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)

        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            logging.error(error_msg)
            self.finished.emit(False, error_msg)

    def handle_existing_destination(self):
        """Handle existing destination folder according to backup logic"""
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

    def copy_with_progress(self, source, destination):
        """Copy files with progress updates"""
        try:
            # Get total number of files for progress tracking
            total_files = self.count_files(source)
            current_file = 0

            def copy_function(src, dst, **kwargs):
                nonlocal current_file
                current_file += 1
                if current_file % 10 == 0:  # Update every 10 files
                    progress_percent = (current_file / total_files) * 100 if total_files > 0 else 0
                    self.progress_update.emit(
                        f"Copying... {progress_percent:.1f}% ({current_file}/{total_files} files)")
                return shutil.copy2(src, dst, **kwargs)

            # Use copytree with custom copy function
            shutil.copytree(source, destination, copy_function=copy_function)

        except Exception as e:
            # Fallback to regular copytree if custom progress fails
            logging.warning(f"Progress tracking failed, using standard copy: {str(e)}")
            shutil.copytree(source, destination)

    def count_files(self, directory):
        """Count total number of files in directory for progress tracking"""
        try:
            total = 0
            for root, dirs, files in os.walk(directory):
                total += len(files)
            return total
        except Exception:
            return 0  # Return 0 if counting fails

    def terminate_safely(self):
        """Safely terminate the worker thread"""
        if self.isRunning():
            self.terminate()
            self.wait(3000)  # Wait up to 3 seconds for clean termination