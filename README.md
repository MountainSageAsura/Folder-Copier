# Folder Copier
A simple Python application that allows users to copy a folder from a source location to a destination folder. The program supports copying between local directories or to network folders. Users can configure the source and destination paths, check network connections, and manage settings via a graphical user interface (GUI).


## Features
- **Select Source & Destination Folders:** Browse and select local or network paths.
- **Network Support:** Copy to and from network folders (configured with network IP).
- **Password Protection:** Secure settings with a password.
- **GUI Interface:** Simple and intuitive user interface built with Tkinter.
- **Settings Management:** Save and load settings from a configuration file.


## Requirements
- Python 3.x
- Tkinter library (Usually comes with Python by default)
- Permissions to access the source and destination folders


## How to Use
### 1. Run the Program
Simply run the Python script, and the GUI window will appear. You can configure the source and destination paths, choose between a local or network folder, and start the copy process.

### 2. Set Up Source and Destination Folders
- Use the **Browse** buttons to select your source and destination directories.
- The **Local Folder** or **Network Folder** radio buttons let you choose whether you're copying to/from a local path or a network folder.
### 3. Password Protected Settings
Click on **Settings** to open the password entry window. The default password is "password". Once authenticated, you can manage your application settings like the source and destination paths and network configurations.

### 4. Copy Folders
Click the **Copy Folder** button to copy the selected folder from the source path to the destination path.


## Configuration File
The program automatically loads and saves settings from a settings.txt file, which contains the following configuration parameters:
- Source Folder Path
- Destination Folder Path
- Network IP Address (for network folders)
- Password for settings access
- Selected radio button option (local or network)


## Example of settings.txt file format:
'# Source folder path'
/path/to/source/folder
'# Destination folder path'
/path/to/destination/folder
'# Network IP address'
192.168.1.1
'# Password'
password
'# Selected radio button option'
network


## Installation
1. Clone this repository:
git clone https://github.com/your-username/folder-copier.git
2. Install any required dependencies (if needed):
pip install -r requirements.txt
3. Run the Python script:
python folder_copier.py


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Author
Darshan Nayee