"""
Authentication Manager for Folder Copier Application
Handles login state and session management
"""

import hashlib
import time
from PyQt6.QtCore import QObject, pyqtSignal


class AuthManager(QObject):
    """Manages user authentication and session state"""

    login_status_changed = pyqtSignal(bool)  # True for logged in, False for logged out

    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.login_time = None
        self.session_timeout = 30 * 60  # 30 minutes in seconds
        self.stored_password_hash = None

    def set_password(self, password: str):
        """Set the password hash for authentication"""
        self.stored_password_hash = self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        """Create a hash of the password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, password: str) -> bool:
        """Authenticate user with password"""
        if not self.stored_password_hash:
            return False

        password_hash = self._hash_password(password)
        if password_hash == self.stored_password_hash:
            self.is_logged_in = True
            self.login_time = time.time()
            self.login_status_changed.emit(True)
            return True
        return False

    def logout(self):
        """Log out the current user"""
        self.is_logged_in = False
        self.login_time = None
        self.login_status_changed.emit(False)

    def is_session_valid(self) -> bool:
        """Check if the current session is still valid"""
        if not self.is_logged_in or not self.login_time:
            return False

        current_time = time.time()
        session_duration = current_time - self.login_time

        if session_duration > self.session_timeout:
            self.logout()
            return False

        return True

    def extend_session(self):
        """Extend the current session by updating login time"""
        if self.is_logged_in:
            self.login_time = time.time()

    def get_session_remaining_time(self) -> int:
        """Get remaining session time in seconds"""
        if not self.is_session_valid():
            return 0

        current_time = time.time()
        elapsed = current_time - self.login_time
        remaining = self.session_timeout - elapsed

        return max(0, int(remaining))

    def set_session_timeout(self, timeout_minutes: int):
        """Set session timeout in minutes"""
        self.session_timeout = timeout_minutes * 60