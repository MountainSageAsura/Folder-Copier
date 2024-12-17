import os  # Importing the os module to interact with the operating system
import shutil  # Importing the shutil module to handle file copying
import tkinter as tk  # Importing tkinter for creating the GUI
from tkinter import filedialog, messagebox  # Importing specific tkinter functions for dialogs

# This application allows users to copy a specified folder from a server's computer to a network folder or other way around.
# Users can set the source and destination folders, check network connection, and manage settings.

class FolderCopierApp:
    def __init__(self, root):
        self.root = root  # Setting the main window
        self.root.title("Folder Copier")  # Setting the title of the window
        self.root.geometry("500x200")  # Set the window size
        self.root.configure(bg="#f0f0f0")  # Set a light background color
        self.root.iconbitmap('icon.ico')  # Set the window icon (replace with your icon path)

        # Initializing variables to store paths and settings
        self.source_path = ""  # Path for the source folder
        self.destination_path = ""  # Path for the destination folder
        self.network_ip = "127.0.0.1"  # Default IP address for the network
        self.is_server = False  # Variable to determine if the user is a server
        self.password = "password"  # Default password for settings access
        self.selected_option = tk.StringVar(value="local")

        # Main Frame for the application
        self.main_frame = tk.Frame(root, bg="#f0f0f0")  # Creating a frame for the main interface
        self.main_frame.pack(pady=20)  # Adding padding for better layout

        # Label and display for the source folder
        tk.Label(self.main_frame, text="Source Folder:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')  # Label for source folder
        self.source_label = tk.Label(self.main_frame, text=self.source_path, bg="#f0f0f0", font=("Arial", 10))  # Label to display source path
        self.source_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')  # Positioning the label

        # Label and display for the destination folder
        tk.Label(self.main_frame, text="Destination Folder:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')  # Label for destination folder
        self.destination_label = tk.Label(self.main_frame, text=self.destination_path, bg="#f0f0f0", font=("Arial", 10))  # Label to display destination path
        self.destination_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')  # Positioning the label

        self.load_settings()  # Load settings from a file at startup

        # Radio buttons to select folder type (local or network)
        self.folder_type = tk.StringVar(value="local")  # Variable to store folder type, default is local
        tk.Radiobutton(self.main_frame, text="Local Folder", variable=self.folder_type, value="local", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)  # Local folder option
        tk.Radiobutton(self.main_frame, text="Network Folder", variable=self.folder_type, value="network", bg="#f0f0f0").grid(row=2, column=1, padx=5, pady=5)  # Network folder option

        # Centering the buttons in their row
        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")  # Create a frame for buttons
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)  # Position the button frame

        # Button to copy the folder
        tk.Button(button_frame, text="Copy Folder", command=self.copy_folder, bg="#007bff", fg="white", font=("Arial", 10), relief="flat", padx=10).pack(side=tk.LEFT, padx=5)  # Copy button
        # Button to open settings
        tk.Button(button_frame, text="Settings", command=self.open_settings, bg="#007bff", fg="white", font=("Arial", 10), relief="flat", padx=10).pack(side=tk.LEFT, padx=5)  # Settings button

    def load_settings(self):
        # To load settings from a file
        if os.path.exists("settings.txt"):  # Check if the settings file exists
            with open("settings.txt", "r") as file:  # Open the file for reading
                lines = file.readlines()  # Read all lines from the file
                settings = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
                # Ensure we have at least 5 settings
                if len(settings) >= 5:
                    self.source_path = settings[0]
                    self.destination_path = settings[1]
                    self.network_ip = settings[2]
                    self.password = settings[3]
                    self.selected_option.set(settings[4])  # Load selected radio option

                    # Update labels with loaded paths
                    self.source_label.config(text=self.source_path)
                    self.destination_label.config(text=self.destination_path)
                else:
                    messagebox.showwarning("Settings", "Settings file is incomplete.")

    def copy_folder(self):
        # To copy the specified folder
        if not self.source_path or not self.destination_path:  # Check if paths are set
            messagebox.showerror("Error", "Please set source and destination folders in settings.")  # Show error if not set
            return  # Exit the method

        if self.folder_type.get() == "network":  # If the selected type is network
            if not self.check_network_connection():  # Check network connection
                messagebox.showerror("Error", "No connection to the network folder.")  # Show error if no connection
                return  # Exit the method

        try:
            shutil.copytree(self.source_path, self.destination_path)  # Copy the folder from source to destination
            messagebox.showinfo("Success", "Folder copied successfully!")  # Show success message
        except Exception as e:  # Handle any exceptions that occur
            messagebox.showerror("Error", str(e))  # Show error message

    def check_network_connection(self):
        # Placeholder method to check network connection
        return True  # Always returns True for this example

    def open_settings(self):
        # To open the password verification window
        self.password_window = tk.Toplevel(self.root)  # Create a new window for password
        self.password_window.title("Enter Password")  # Set title for the password window
        self.password_window.geometry("300x100")  # Set window size
        self.password_window.configure(bg="#f0f0f0")  # Set background color

        tk.Label(self.password_window, text="Enter Password:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        password_entry = tk.Entry(self.password_window, show="*", font=("Arial", 10))
        password_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Button(self.password_window, text="Submit", command=lambda: self.check_password(password_entry.get()), bg="#007bff", fg="white", font=("Arial", 10), relief="flat").grid(row=1, column=0, columnspan=2, pady=10)

    def check_password(self, entered_password):
        # Verify if the entered password is correct
        if entered_password == self.password:
            self.password_window.destroy()  # Close the password window
            self.open_settings_window()  # Open the settings window
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def open_settings_window(self):
        # Open a new settings window after password verification
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("500x200")
        self.settings_window.configure(bg="#f0f0f0")

        self.show_settings()  # Call show_settings to populate the window

    def show_settings(self):
        # Create a frame within the settings window
        self.settings_frame = tk.Frame(self.settings_window, bg="#f0f0f0")
        self.settings_frame.grid(pady=20)

        tk.Label(self.settings_frame, text="Source Folder:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Label(self.settings_frame, text=self.source_path, bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=1, padx=5, pady=5, sticky='w') # Label to display source path
        tk.Button(self.settings_frame, text="Browse", command=self.browse_source, bg="#007bff", fg="white", font=("Arial", 10), relief="flat").grid(row=1, column=1, padx=20, pady=5)

        tk.Label(self.settings_frame, text="Destination Folder:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Label(self.settings_frame, text=self.destination_path, bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5, sticky='w')  # Label to display source path
        tk.Button(self.settings_frame, text="Browse", command=self.browse_destination, bg="#007bff", fg="white", font=("Arial", 10), relief="flat").grid(row=3, column=1, padx=20, pady=5)

        tk.Button(self.settings_frame, text="Save", command=self.save_settings, bg="#28a745", fg="white", font=("Arial", 10), relief="flat").grid(row=4, column=0, columnspan=2, pady=10)

    def save_settings(self):
        # To save the settings to a file
        with open("settings.txt", "w") as file:
            file.write("# Source folder path\n")
            file.write(f"{self.source_path}\n")
            file.write("# Destination folder path\n")
            file.write(f"{self.destination_path}\n")
            file.write("# Network IP address\n")
            file.write(f"{self.network_ip}\n")
            file.write("# Password\n")
            file.write(f"{self.password}\n")
            file.write("# Selected radio button option\n")
            file.write(f"{self.selected_option.get()}\n")
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def browse_source(self):
        # Browse and select the source folder
        self.source_path = filedialog.askdirectory()
        self.source_label.config(text=self.source_path)

    def browse_destination(self):
        # Browse and select the destination folder
        self.destination_path = filedialog.askdirectory()
        self.destination_label.config(text=self.destination_path)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = FolderCopierApp(root)  # Initialize the application
    root.mainloop()  # Start the main loop