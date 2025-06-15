import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import platform
import threading


class FolderCopierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Copier Pro")
        self.root.geometry("600x400")

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
        current_directory = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_directory, 'icon.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Initialize variables
        self.source_path = ""
        self.destination_path = ""
        self.network_ip = "127.0.0.1"
        self.password = "password"
        self.folder_type = "local"  # 'local' or 'network'
        self.auto_close = False
        self.is_logged_in = False
        self.network_status = False

        self.load_settings()
        self.create_main_interface()
        self.check_network_status()

    def create_main_interface(self):
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
        settings_text = "Settings" if not self.is_logged_in else "Settings"
        self.settings_btn = tk.Button(
            button_frame,
            text=settings_text,
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

    def update_display(self):
        """Update the display elements"""
        self.source_display.config(text=self.source_path or "Not selected")
        self.dest_display.config(text=self.destination_path or "Not selected")
        self.type_display.config(text=self.folder_type.title())

        # Show/hide network status based on folder type
        if self.folder_type == "network":
            self.network_frame.pack(fill='x', pady=(5, 0))
            self.check_network_status()
        else:
            self.network_frame.pack_forget()

    def check_network_status(self):
        """Check network connectivity in a separate thread"""
        if self.folder_type == "network":
            threading.Thread(target=self._ping_network, daemon=True).start()

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
        except Exception:
            self.network_status = False
            self.root.after(0, self._update_network_status)

    def _update_network_status(self):
        """Update network status indicators"""
        if self.network_status:
            self.status_indicator.config(fg=self.colors['accent_green'])
            self.status_text.config(text=f"Connected ({self.network_ip})")
        else:
            self.status_indicator.config(fg=self.colors['accent_red'])
            self.status_text.config(text=f"Disconnected ({self.network_ip})")

    def refresh_network_status(self):
        """Refresh network status"""
        self.status_text.config(text="Checking...")
        self.check_network_status()

    def load_settings(self):
        """Load settings from file"""
        if os.path.exists("settings.txt"):
            try:
                with open("settings.txt", "r") as file:
                    lines = file.readlines()
                    settings = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

                    if len(settings) >= 6:
                        self.source_path = settings[0]
                        self.destination_path = settings[1]
                        self.network_ip = settings[2]
                        self.password = settings[3]
                        self.folder_type = settings[4]
                        self.auto_close = settings[5].lower() == 'true'
            except Exception as e:
                messagebox.showwarning("Settings", f"Error loading settings: {str(e)}")

    def save_settings(self):
        """Save settings to file"""
        try:
            with open("settings.txt", "w") as file:
                file.write("# Source folder path\n")
                file.write(f"{self.source_path}\n")
                file.write("# Destination folder path\n")
                file.write(f"{self.destination_path}\n")
                file.write("# Network IP address\n")
                file.write(f"{self.network_ip}\n")
                file.write("# Password\n")
                file.write(f"{self.password}\n")
                file.write("# Folder type (local/network)\n")
                file.write(f"{self.folder_type}\n")
                file.write("# Auto close after copy\n")
                file.write(f"{self.auto_close}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            return False

    def copy_folder(self):
        """Copy the specified folder"""
        if not self.source_path or not self.destination_path:
            messagebox.showerror("Error", "Please set source and destination folders in settings.")
            return

        if self.folder_type == "network" and not self.network_status:
            messagebox.showerror("Error", "No connection to the network. Please check network settings.")
            return

        try:
            # Check if destination exists and handle accordingly
            if os.path.exists(self.destination_path):
                if messagebox.askyesno("Destination Exists",
                                       "Destination folder already exists. Do you want to overwrite it?"):
                    shutil.rmtree(self.destination_path)
                else:
                    return

            shutil.copytree(self.source_path, self.destination_path)
            messagebox.showinfo("Success", "Folder copied successfully!")

            if self.auto_close:
                self.root.quit()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy folder: {str(e)}")

    def open_settings(self):
        """Open settings window"""
        if self.is_logged_in:
            self.open_settings_window()
        else:
            self.show_password_dialog()

    def show_password_dialog(self):
        """Show password entry dialog"""
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

    def check_password(self):
        """Verify password"""
        if self.password_entry.get() == self.password:
            self.is_logged_in = True
            self.password_window.destroy()
            self.logout_btn.pack(side='left', padx=10)  # Show logout button
            self.open_settings_window()
        else:
            messagebox.showerror("Error", "Incorrect password.")
            self.password_entry.delete(0, tk.END)

    def logout(self):
        """Logout user"""
        self.is_logged_in = False
        self.logout_btn.pack_forget()  # Hide logout button

    def open_settings_window(self):
        """Open the main settings window with tabs"""
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

    def create_folders_tab(self, notebook):
        """Create the folders configuration tab"""
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

    def create_connection_tab(self, notebook):
        """Create the connection configuration tab"""
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

    def create_security_tab(self, notebook):
        """Create the security configuration tab"""
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

    def create_preferences_tab(self, notebook):
        """Create the preferences tab"""
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

    def browse_source(self):
        """Browse for source folder"""
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_path = folder
            self.source_path_var.set(folder)

    def browse_destination(self):
        """Browse for destination folder"""
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.destination_path = folder
            self.dest_path_var.set(folder)

    def change_password(self):
        """Change the password"""
        if self.current_password_var.get() != self.password:
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        new_password = self.new_password_var.get()
        if len(new_password) < 3:
            messagebox.showerror("Error", "New password must be at least 3 characters long.")
            return

        self.password = new_password
        self.current_password_var.set("")
        self.new_password_var.set("")
        messagebox.showinfo("Success", "Password changed successfully!")

    def save_all_settings(self):
        """Save all settings from tabs"""
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


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderCopierApp(root)
    root.mainloop()