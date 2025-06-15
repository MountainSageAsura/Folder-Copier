import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import platform
import threading
import json
import logging
from datetime import datetime


class FolderCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Copier Pro")
        self.root.geometry("600x400")

        # Setup logging
        self.setup_logging()

        # Pastel color palette
        self.colors = {
            'bg_primary': '#f8f9fa',  # Light gray-blue
            'bg_secondary': '#e9ecef',  # Lighter gray
            'accent_blue': '#a8dadc',  # Soft blue
            'accent_green': '#b8e6b8',  # Soft green
            'accent_red': '#ffb3ba',  # Soft red
            'accent_purple': '#d4b5d4',  # Soft purple
            'text_primary': '#333333',  # Dark gray
            'text_secondary': '#6c757d',  # Medium gray
            'white': '#ffffff'
        }

        self.root.configure(bg=self.colors['bg_primary'])

        # Get the current working directory for icon
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_directory, 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            self.logger.warning(f"Could not load application icon: {str(e)}")

        # Initialize variables with defaults
        self.source_path = ""
        self.destination_path = ""
        self.network_ip = "127.0.0.1"
        self.password = "password"
        self.folder_type = "local"  # 'local' or 'network'
        self.auto_close = False
        self.is_logged_in = False
        self.network_status = False

        # Settings file path
        self.settings_file = "settings.json"

        try:
            self.load_settings()
            self.create_main_interface()
            self.check_network_status()
            self.logger.info("Application initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {str(e)}")
            messagebox.showerror("Initialization Error", f"Failed to start application: {str(e)}")

    def setup_logging(self):
        """Setup logging configuration"""
        try:
            # Create logs directory if it doesn't exist
            if not os.path.exists('logs'):
                os.makedirs('logs')

            # Setup logger
            self.logger = logging.getLogger('FolderCopierApp')
            self.logger.setLevel(logging.INFO)

            # Create file handler
            log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(logging.INFO)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to logger
            if not self.logger.handlers:
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)

        except Exception as e:
            print(f"Failed to setup logging: {str(e)}")
            # Create a basic logger if file logging fails
            self.logger = logging.getLogger('FolderCopierApp')
            self.logger.setLevel(logging.INFO)

    def create_main_interface(self):
        """Create the main user interface"""
        try:
            # Main container with padding
            main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
            main_container.pack(fill='both', expand=True, padx=30, pady=30)

            # Title
            title_label = tk.Label(
                main_container,
                text="Folder Copier Pro",
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            title_label.pack(pady=(0, 20))

            # Info panel
            info_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'], relief='flat', bd=1)
            info_frame.pack(fill='x', pady=(0, 20), padx=10)

            # Source folder display
            source_frame = tk.Frame(info_frame, bg=self.colors['bg_secondary'])
            source_frame.pack(fill='x', padx=15, pady=10)

            tk.Label(
                source_frame,
                text="Source Folder:",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w')

            self.source_display = tk.Label(
                source_frame,
                text=self.source_path or "Not selected",
                font=("Segoe UI", 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary'],
                wraplength=500,
                justify='left'
            )
            self.source_display.pack(anchor='w')

            # Destination folder display
            dest_frame = tk.Frame(info_frame, bg=self.colors['bg_secondary'])
            dest_frame.pack(fill='x', padx=15, pady=10)

            tk.Label(
                dest_frame,
                text="Destination Folder:",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w')

            self.dest_display = tk.Label(
                dest_frame,
                text=self.destination_path or "Not selected",
                font=("Segoe UI", 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary'],
                wraplength=500,
                justify='left'
            )
            self.dest_display.pack(anchor='w')

            # Folder type and network status
            status_frame = tk.Frame(info_frame, bg=self.colors['bg_secondary'])
            status_frame.pack(fill='x', padx=15, pady=10)

            # Folder type display
            type_frame = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
            type_frame.pack(fill='x')

            tk.Label(
                type_frame,
                text="Folder Type:",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']
            ).pack(side='left')

            self.type_display = tk.Label(
                type_frame,
                text=self.folder_type.title(),
                font=("Segoe UI", 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            )
            self.type_display.pack(side='left', padx=(10, 0))

            # Network status (only show if network type is selected)
            self.network_frame = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
            if self.folder_type == "network":
                self.network_frame.pack(fill='x', pady=(5, 0))

            tk.Label(
                self.network_frame,
                text="Network Status:",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']
            ).pack(side='left')

            self.status_indicator = tk.Label(
                self.network_frame,
                text="●",
                font=("Segoe UI", 12),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent_red']
            )
            self.status_indicator.pack(side='left', padx=(10, 5))

            self.status_text = tk.Label(
                self.network_frame,
                text="Checking...",
                font=("Segoe UI", 9),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            )
            self.status_text.pack(side='left')

            # Refresh button
            self.refresh_btn = tk.Button(
                self.network_frame,
                text="🔄",
                font=("Segoe UI", 10),
                bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=8,
                pady=2,
                command=self.refresh_network_status,
                cursor="hand2"
            )
            self.refresh_btn.pack(side='left', padx=(10, 0))

            # Main buttons
            button_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
            button_frame.pack(pady=20)

            # Copy button
            self.copy_btn = tk.Button(
                button_frame,
                text="Copy Folder",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['accent_green'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=30,
                pady=12,
                command=self.copy_folder,
                cursor="hand2"
            )
            self.copy_btn.pack(side='left', padx=10)

            # Settings button
            self.settings_btn = tk.Button(
                button_frame,
                text="Settings",
                font=("Segoe UI", 12),
                bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=30,
                pady=12,
                command=self.open_settings,
                cursor="hand2"
            )
            self.settings_btn.pack(side='left', padx=10)

            # Logout button (only show when logged in)
            self.logout_btn = tk.Button(
                button_frame,
                text="Logout",
                font=("Segoe UI", 12),
                bg=self.colors['accent_red'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=20,
                pady=12,
                command=self.logout,
                cursor="hand2"
            )
            if self.is_logged_in:
                self.logout_btn.pack(side='left', padx=10)

        except Exception as e:
            self.logger.error(f"Failed to create main interface: {str(e)}")
            messagebox.showerror("Interface Error", f"Failed to create interface: {str(e)}")

    def update_display(self):
        """Update the display elements"""
        try:
            self.source_display.config(text=self.source_path or "Not selected")
            self.dest_display.config(text=self.destination_path or "Not selected")
            self.type_display.config(text=self.folder_type.title())

            # Show/hide network status based on folder type
            if self.folder_type == "network":
                self.network_frame.pack(fill='x', pady=(5, 0))
                self.check_network_status()
            else:
                self.network_frame.pack_forget()

            self.logger.info("Display updated successfully")
        except Exception as e:
            self.logger.error(f"Failed to update display: {str(e)}")

    def check_network_status(self):
        """Check network connectivity in a separate thread"""
        if self.folder_type == "network":
            try:
                threading.Thread(target=self._ping_network, daemon=True).start()
            except Exception as e:
                self.logger.error(f"Failed to start network check thread: {str(e)}")

    def _ping_network(self):
        """Ping the network IP address"""
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "3000", self.network_ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "3", self.network_ip]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            self.network_status = result.returncode == 0

            # Update UI in main thread
            self.root.after(0, self._update_network_status)

        except subprocess.TimeoutExpired:
            self.logger.warning(f"Network ping timeout for {self.network_ip}")
            self.network_status = False
            self.root.after(0, self._update_network_status)
        except Exception as e:
            self.logger.error(f"Network ping failed: {str(e)}")
            self.network_status = False
            self.root.after(0, self._update_network_status)

    def _update_network_status(self):
        """Update network status indicators"""
        try:
            if self.network_status:
                self.status_indicator.config(fg=self.colors['accent_green'])
                self.status_text.config(text=f"Connected ({self.network_ip})")
                self.logger.info(f"Network connection successful to {self.network_ip}")
            else:
                self.status_indicator.config(fg=self.colors['accent_red'])
                self.status_text.config(text=f"Disconnected ({self.network_ip})")
                self.logger.warning(f"Network connection failed to {self.network_ip}")
        except Exception as e:
            self.logger.error(f"Failed to update network status display: {str(e)}")

    def refresh_network_status(self):
        """Refresh network status"""
        try:
            self.status_text.config(text="Checking...")
            self.check_network_status()
            self.logger.info("Network status refresh initiated")
        except Exception as e:
            self.logger.error(f"Failed to refresh network status: {str(e)}")

    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    settings = json.load(file)

                    self.source_path = settings.get('source_path', '')
                    self.destination_path = settings.get('destination_path', '')
                    self.network_ip = settings.get('network_ip', '127.0.0.1')
                    self.password = settings.get('password', 'password')
                    self.folder_type = settings.get('folder_type', 'local')
                    self.auto_close = settings.get('auto_close', False)

                    self.logger.info("Settings loaded successfully from JSON file")
            else:
                self.logger.info("No settings file found, using defaults")
                self.save_settings()  # Create default settings file

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in settings file: {str(e)}")
            messagebox.showwarning("Settings Error",
                                   f"Settings file is corrupted. Using default settings.\nError: {str(e)}")
            self.save_settings()  # Recreate with defaults
        except Exception as e:
            self.logger.error(f"Failed to load settings: {str(e)}")
            messagebox.showwarning("Settings Error",
                                   f"Failed to load settings: {str(e)}\nUsing default settings.")

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            settings = {
                'source_path': self.source_path,
                'destination_path': self.destination_path,
                'network_ip': self.network_ip,
                'password': self.password,
                'folder_type': self.folder_type,
                'auto_close': self.auto_close,
                'version': '1.0',
                'last_updated': datetime.now().isoformat()
            }

            # Create backup of existing settings
            if os.path.exists(self.settings_file):
                backup_file = f"{self.settings_file}.backup"
                shutil.copy2(self.settings_file, backup_file)

            with open(self.settings_file, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)

            self.logger.info("Settings saved successfully to JSON file")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save settings: {str(e)}")
            messagebox.showerror("Settings Error", f"Failed to save settings: {str(e)}")
            return False

    def smart_folder_copy(self, source, destination):
        """
        Smart folder copying with automatic handling of existing folders
        - If destination exists: rename to _old and copy new
        - If _old version exists: delete _old, rename current to _old, then copy new
        """
        try:
            source_folder_name = os.path.basename(source)
            destination_full_path = os.path.join(destination, source_folder_name)
            destination_old_path = destination_full_path + "_old"

            self.logger.info(f"Starting smart copy from {source} to {destination_full_path}")

            # Check if destination folder exists
            if os.path.exists(destination_full_path):
                self.logger.info(f"Destination folder exists: {destination_full_path}")

                # Check if _old version exists
                if os.path.exists(destination_old_path):
                    self.logger.info(f"Old version exists, deleting: {destination_old_path}")
                    try:
                        shutil.rmtree(destination_old_path)
                        self.logger.info(f"Successfully deleted old version: {destination_old_path}")
                    except Exception as e:
                        self.logger.error(f"Failed to delete old version: {str(e)}")
                        raise Exception(f"Failed to delete existing _old folder: {str(e)}")

                # Rename existing folder to _old
                self.logger.info(f"Renaming existing folder to _old: {destination_full_path} -> {destination_old_path}")
                try:
                    os.rename(destination_full_path, destination_old_path)
                    self.logger.info(f"Successfully renamed to _old version")
                except Exception as e:
                    self.logger.error(f"Failed to rename existing folder: {str(e)}")
                    raise Exception(f"Failed to rename existing folder: {str(e)}")

            # Copy the source folder to destination
            self.logger.info(f"Copying folder from {source} to {destination_full_path}")
            try:
                shutil.copytree(source, destination_full_path)
                self.logger.info(f"Successfully copied folder to {destination_full_path}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to copy folder: {str(e)}")

                # If copy failed and we renamed a folder, try to restore it
                if os.path.exists(destination_old_path) and not os.path.exists(destination_full_path):
                    try:
                        os.rename(destination_old_path, destination_full_path)
                        self.logger.info("Restored original folder after copy failure")
                    except Exception as restore_error:
                        self.logger.error(f"Failed to restore original folder: {str(restore_error)}")

                raise Exception(f"Failed to copy folder: {str(e)}")

        except Exception as e:
            self.logger.error(f"Smart folder copy failed: {str(e)}")
            raise

    def copy_folder(self):
        """Copy the specified folder using smart copy logic"""
        try:
            # Validate inputs
            if not self.source_path or not self.destination_path:
                error_msg = "Please set source and destination folders in settings."
                self.logger.warning("Copy attempted without proper folder configuration")
                messagebox.showerror("Configuration Error", error_msg)
                return

            if not os.path.exists(self.source_path):
                error_msg = f"Source folder does not exist: {self.source_path}"
                self.logger.error(error_msg)
                messagebox.showerror("Source Error", error_msg)
                return

            if not os.path.exists(self.destination_path):
                error_msg = f"Destination folder does not exist: {self.destination_path}"
                self.logger.error(error_msg)
                messagebox.showerror("Destination Error", error_msg)
                return

            # Check network connectivity for network operations
            if self.folder_type == "network" and not self.network_status:
                error_msg = "No connection to the network. Please check network settings."
                self.logger.warning("Copy attempted without network connection")
                messagebox.showerror("Network Error", error_msg)
                return

            # Check available space (basic check)
            try:
                source_size = self.get_folder_size(self.source_path)
                available_space = shutil.disk_usage(self.destination_path).free

                if source_size > available_space:
                    error_msg = f"Insufficient disk space. Need {source_size / (1024 ** 3):.2f} GB, available {available_space / (1024 ** 3):.2f} GB"
                    self.logger.error(error_msg)
                    messagebox.showerror("Disk Space Error", error_msg)
                    return

            except Exception as e:
                self.logger.warning(f"Could not check disk space: {str(e)}")

            # Disable copy button during operation
            self.copy_btn.config(state='disabled', text='Copying...')
            self.root.update()

            # Perform the smart copy
            self.smart_folder_copy(self.source_path, self.destination_path)

            success_msg = "Folder copied successfully!"
            self.logger.info(f"Copy operation completed successfully: {self.source_path} -> {self.destination_path}")
            messagebox.showinfo("Success", success_msg)

            # Auto-close if enabled
            if self.auto_close:
                self.logger.info("Auto-closing application after successful copy")
                self.root.quit()

        except Exception as e:
            error_msg = f"Failed to copy folder: {str(e)}"
            self.logger.error(error_msg)
            messagebox.showerror("Copy Error", error_msg)
        finally:
            # Re-enable copy button
            try:
                self.copy_btn.config(state='normal', text='Copy Folder')
            except:
                pass  # In case window is being destroyed

    def get_folder_size(self, folder_path):
        """Calculate the total size of a folder"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            return total_size
        except Exception as e:
            self.logger.warning(f"Could not calculate folder size: {str(e)}")
            return 0

    def open_settings(self):
        """Open settings window"""
        try:
            if self.is_logged_in:
                self.open_settings_window()
            else:
                self.show_password_dialog()
        except Exception as e:
            self.logger.error(f"Failed to open settings: {str(e)}")
            messagebox.showerror("Settings Error", f"Failed to open settings: {str(e)}")

    def show_password_dialog(self):
        """Show password entry dialog"""
        try:
            self.password_window = tk.Toplevel(self.root)
            self.password_window.title("Authentication Required")
            self.password_window.geometry("350x150")
            self.password_window.configure(bg=self.colors['bg_primary'])
            self.password_window.resizable(False, False)

            # Center the window
            self.password_window.transient(self.root)
            self.password_window.grab_set()

            main_frame = tk.Frame(self.password_window, bg=self.colors['bg_primary'])
            main_frame.pack(expand=True, fill='both', padx=20, pady=20)

            tk.Label(
                main_frame,
                text="Enter Password:",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(pady=(0, 10))

            self.password_entry = tk.Entry(
                main_frame,
                show="*",
                font=("Segoe UI", 11),
                relief='flat',
                bd=5
            )
            self.password_entry.pack(pady=(0, 15), ipady=5)
            self.password_entry.focus()

            button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
            button_frame.pack()

            tk.Button(
                button_frame,
                text="Cancel",
                font=("Segoe UI", 10),
                bg=self.colors['accent_red'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=20,
                pady=8,
                command=self.password_window.destroy,
                cursor="hand2"
            ).pack(side='left', padx=(0, 10))

            tk.Button(
                button_frame,
                text="Login",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['accent_green'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=20,
                pady=8,
                command=self.check_password,
                cursor="hand2"
            ).pack(side='left')

            # Bind Enter key to login
            self.password_entry.bind('<Return>', lambda e: self.check_password())

        except Exception as e:
            self.logger.error(f"Failed to show password dialog: {str(e)}")
            messagebox.showerror("Dialog Error", f"Failed to show password dialog: {str(e)}")

    def check_password(self):
        """Verify password"""
        try:
            if self.password_entry.get() == self.password:
                self.is_logged_in = True
                self.password_window.destroy()
                self.logout_btn.pack(side='left', padx=10)  # Show logout button
                self.open_settings_window()
                self.logger.info("User successfully authenticated")
            else:
                self.logger.warning("Failed authentication attempt")
                messagebox.showerror("Error", "Incorrect password.")
                self.password_entry.delete(0, tk.END)
        except Exception as e:
            self.logger.error(f"Password check failed: {str(e)}")
            messagebox.showerror("Authentication Error", f"Authentication failed: {str(e)}")

    def logout(self):
        """Logout user"""
        try:
            self.is_logged_in = False
            self.logout_btn.pack_forget()  # Hide logout button
            self.logger.info("User logged out")
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")

    def open_settings_window(self):
        """Open the main settings window with tabs"""
        try:
            self.settings_window = tk.Toplevel(self.root)
            self.settings_window.title("Settings")
            self.settings_window.geometry("500x400")
            self.settings_window.configure(bg=self.colors['bg_primary'])
            self.settings_window.resizable(False, False)

            # Center window
            self.settings_window.transient(self.root)
            self.settings_window.grab_set()

            # Create notebook for tabs
            notebook = ttk.Notebook(self.settings_window)
            notebook.pack(fill='both', expand=True, padx=20, pady=20)

            # Configure notebook style
            style = ttk.Style()
            style.configure('TNotebook.Tab', padding=[20, 10])

            # Create tabs
            self.create_folders_tab(notebook)
            self.create_connection_tab(notebook)
            self.create_security_tab(notebook)
            self.create_preferences_tab(notebook)

            # Save button
            save_frame = tk.Frame(self.settings_window, bg=self.colors['bg_primary'])
            save_frame.pack(pady=(0, 20))

            tk.Button(
                save_frame,
                text="Save Settings",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['accent_green'],
                fg=self.colors['text_primary'],
                relief='flat',
                padx=30,
                pady=10,
                command=self.save_all_settings,
                cursor="hand2"
            ).pack()

        except Exception as e:
            self.logger.error(f"Failed to open settings window: {str(e)}")
            messagebox.showerror("Settings Error", f"Failed to open settings window: {str(e)}")

    def create_folders_tab(self, notebook):
        """Create the folders configuration tab"""
        try:
            frame = tk.Frame(notebook, bg=self.colors['bg_primary'])
            notebook.add(frame, text="Folders")

            # Source folder
            source_frame = tk.LabelFrame(
                frame,
                text="Source Folder",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            source_frame.pack(fill='x', padx=20, pady=10)

            self.source_path_var = tk.StringVar(value=self.source_path)
            tk.Entry(
                source_frame,
                textvariable=self.source_path_var,
                font=("Segoe UI", 9),
                state='readonly'
            ).pack(fill='x', padx=10, pady=5)

            tk.Button(
                source_frame,
                text="Browse Source Folder",
                font=("Segoe UI", 10),
                bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'],
                relief='flat',
                command=self.browse_source,
                cursor="hand2"
            ).pack(pady=5)

            # Destination folder
            dest_frame = tk.LabelFrame(
                frame,
                text="Destination Folder",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            dest_frame.pack(fill='x', padx=20, pady=10)

            self.dest_path_var = tk.StringVar(value=self.destination_path)
            tk.Entry(
                dest_frame,
                textvariable=self.dest_path_var,
                font=("Segoe UI", 9),
                state='readonly'
            ).pack(fill='x', padx=10, pady=5)

            tk.Button(
                dest_frame,
                text="Browse Destination Folder",
                font=("Segoe UI", 10),
                bg=self.colors['accent_blue'],
                fg=self.colors['text_primary'],
                relief='flat',
                command=self.browse_destination,
                cursor="hand2"
            ).pack(pady=5)

        except Exception as e:
            self.logger.error(f"Failed to create folders tab: {str(e)}")

    def create_connection_tab(self, notebook):
        """Create the connection configuration tab"""
        try:
            frame = tk.Frame(notebook, bg=self.colors['bg_primary'])
            notebook.add(frame, text="Connection")

            # Folder type selection
            type_frame = tk.LabelFrame(
                frame,
                text="Folder Type",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            type_frame.pack(fill='x', padx=20, pady=10)

            self.folder_type_var = tk.StringVar(value=self.folder_type)

            tk.Radiobutton(
                type_frame,
                text="Local Folder",
                variable=self.folder_type_var,
                value="local",
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=5)

            tk.Radiobutton(
                type_frame,
                text="Network Folder",
                variable=self.folder_type_var,
                value="network",
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=5)

            # Network settings
            network_frame = tk.LabelFrame(
                frame,
                text="Network Settings",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            network_frame.pack(fill='x', padx=20, pady=10)

            tk.Label(
                network_frame,
                text="Network IP Address:",
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=(10, 5))

            self.network_ip_var = tk.StringVar(value=self.network_ip)
            tk.Entry(
                network_frame,
                textvariable=self.network_ip_var,
                font=("Segoe UI", 10)
            ).pack(fill='x', padx=10, pady=(0, 10))

        except Exception as e:
            self.logger.error(f"Failed to create connection tab: {str(e)}")

    def create_security_tab(self, notebook):
        """Create the security configuration tab"""
        try:
            frame = tk.Frame(notebook, bg=self.colors['bg_primary'])
            notebook.add(frame, text="Security")

            password_frame = tk.LabelFrame(
                frame,
                text="Change Password",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            password_frame.pack(fill='x', padx=20, pady=20)

            tk.Label(
                password_frame,
                text="Current Password:",
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=(10, 5))

            self.current_password_var = tk.StringVar()
            tk.Entry(
                password_frame,
                textvariable=self.current_password_var,
                show="*",
                font=("Segoe UI", 10)
            ).pack(fill='x', padx=10, pady=(0, 10))

            tk.Label(
                password_frame,
                text="New Password:",
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=(0, 5))

            self.new_password_var = tk.StringVar()
            tk.Entry(
                password_frame,
                textvariable=self.new_password_var,
                show="*",
                font=("Segoe UI", 10)
            ).pack(fill='x', padx=10, pady=(0, 10))

            tk.Button(
                password_frame,
                text="Change Password",
                font=("Segoe UI", 10),
                bg=self.colors['accent_purple'],
                fg=self.colors['text_primary'],
                relief='flat',
                command=self.change_password,
                cursor="hand2"
            ).pack(pady=10)

        except Exception as e:
            self.logger.error(f"Failed to create security tab: {str(e)}")

    def create_preferences_tab(self, notebook):
        """Create the preferences tab"""
        try:
            frame = tk.Frame(notebook, bg=self.colors['bg_primary'])
            notebook.add(frame, text="Preferences")

            pref_frame = tk.LabelFrame(
                frame,
                text="Application Preferences",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            pref_frame.pack(fill='x', padx=20, pady=20)

            self.auto_close_var = tk.BooleanVar(value=self.auto_close)
            tk.Checkbutton(
                pref_frame,
                text="Auto-close application after successful copy",
                variable=self.auto_close_var,
                font=("Segoe UI", 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            ).pack(anchor='w', padx=10, pady=10)

        except Exception as e:
            self.logger.error(f"Failed to create preferences tab: {str(e)}")

    def browse_source(self):
        """Browse for source folder"""
        try:
            folder = filedialog.askdirectory(title="Select Source Folder")
            if folder:
                self.source_path = folder
                self.source_path_var.set(folder)
                self.logger.info(f"Source folder selected: {folder}")
        except Exception as e:
            self.logger.error(f"Failed to browse source folder: {str(e)}")
            messagebox.showerror("Browse Error", f"Failed to browse source folder: {str(e)}")

    def browse_destination(self):
        """Browse for destination folder"""
        try:
            folder = filedialog.askdirectory(title="Select Destination Folder")
            if folder:
                self.destination_path = folder
                self.dest_path_var.set(folder)
                self.logger.info(f"Destination folder selected: {folder}")
        except Exception as e:
            self.logger.error(f"Failed to browse destination folder: {str(e)}")
            messagebox.showerror("Browse Error", f"Failed to browse destination folder: {str(e)}")

    def change_password(self):
        """Change the password"""
        try:
            if self.current_password_var.get() != self.password:
                self.logger.warning("Incorrect current password entered during password change")
                messagebox.showerror("Error", "Current password is incorrect.")
                return

            new_password = self.new_password_var.get()
            if len(new_password) < 3:
                messagebox.showerror("Error", "New password must be at least 3 characters long.")
                return

            self.password = new_password
            self.current_password_var.set("")
            self.new_password_var.set("")
            self.logger.info("Password changed successfully")
            messagebox.showinfo("Success", "Password changed successfully!")

        except Exception as e:
            self.logger.error(f"Failed to change password: {str(e)}")
            messagebox.showerror("Password Error", f"Failed to change password: {str(e)}")

    def save_all_settings(self):
        """Save all settings from tabs"""
        try:
            # Update variables from form
            self.source_path = self.source_path_var.get()
            self.destination_path = self.dest_path_var.get()
            self.folder_type = self.folder_type_var.get()
            self.network_ip = self.network_ip_var.get()
            self.auto_close = self.auto_close_var.get()

            if self.save_settings():
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.settings_window.destroy()

                # Update main display
                self.update_display()
                self.logger.info("All settings saved and display updated")
            else:
                self.logger.error("Failed to save settings")

        except Exception as e:
            self.logger.error(f"Failed to save all settings: {str(e)}")
            messagebox.showerror("Save Error", f"Failed to save settings: {str(e)}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FolderCopierApp(root)
        root.mainloop()
    except Exception as e:
        # Log any critical startup errors
        print(f"Critical error starting application: {str(e)}")
        messagebox.showerror("Startup Error", f"Failed to start application: {str(e)}")