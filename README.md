# Folder Copier Pro

A modern, user-friendly GUI application for copying folders between local and network locations with advanced features including network connectivity monitoring, session management, and customizable preferences.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

### 🎨 Modern Interface
- **Beautiful PyQt6 GUI** with native look and feel
- **Emoji-enhanced interface** for better visual recognition
- Beautiful pastel color palette with modern styling
- Clean, intuitive design with proper spacing
- Professional typography and responsive layout
- **Real-time progress tracking** with detailed status updates

### 📊 Live Monitoring & Progress
- **Real-time progress bar** showing copy completion percentage
- **Live log updates** during copy operations
- **Detailed status messages** for each file being copied
- **Background operations** with non-blocking UI
- **Copy cancellation** support for user control

### 📁 Smart Folder Management
- Easy source and destination folder selection
- Support for both local and network folders
- Real-time folder path display
- **Intelligent folder conflict handling:**
  - If destination folder exists: automatically renames existing folder to `[name]_old`
  - If `[name]_old` already exists: deletes old version, renames current to `_old`, then copies new
  - Automatic rollback on copy failure for data safety

### 🌐 Network Connectivity
- Real-time network status monitoring with visual indicators
- Automatic ping testing for network destinations
- Manual refresh option for connectivity status
- Color-coded status (green = connected, red = disconnected)

### 🔐 Security & Session Management
- Password-protected settings access
- Session-based authentication (no repeated login during app session)
- Secure password change functionality
- Logout option for security

### ⚙️ Advanced Settings
- Tabbed settings interface for better organization
- **Folders Tab**: Source and destination configuration
- **Connection Tab**: Local/network folder type selection and network settings
- **Security Tab**: Password management
- **Preferences Tab**: Auto-close and other application preferences

### 🔄 Smart Copy Operations
- **Intelligent folder copying** with automatic conflict resolution
- **Safe backup system**: existing folders renamed to `_old` before copying
- **Automatic rollback** on copy failure to prevent data loss
- Destination conflict detection and resolution
- **Disk space validation** before copying
- Optional auto-close after successful copy
- Detailed success/error reporting with comprehensive logging

### 💾 Configuration Management
- **JSON-based settings** with automatic backup
- Persistent settings storage with version tracking
- Automatic settings loading on startup
- **Comprehensive error handling** with detailed logging
- Settings validation and corruption recovery

## Installation

### Prerequisites
- Python 3.8 or higher
- PyQt6 (modern GUI framework)
- Standard library modules: `os`, `shutil`, `subprocess`, `platform`, `threading`, `json`, `logging`

### Installation

Install PyQt6 using pip:
```bash
pip install PyQt6
```

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/folder-copier-pro.git
   cd folder-copier-pro
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Optional: Create a desktop shortcut (Windows):**
   - Right-click on `main.py`
   - Select "Create shortcut"
   - Move shortcut to desktop
   - Rename to "Folder Copier Pro"

### Building Executable (Optional)

To create a standalone executable with PyQt6:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "FolderCopierPro" main.py
```

**Note**: PyQt6 will be automatically bundled with the executable, making it larger but self-contained.

## Usage

### First Time Setup

1. **Launch the application**
2. **Access Settings** (default password: `password`)
3. **Configure your preferences:**
   - Set source and destination folders
   - Choose between local or network folder types
   - Configure network IP if using network folders
   - Set auto-close preference
   - Change default password for security

### Basic Operation

1. **Select folder type** in settings (Local or Network)
2. **Choose source folder** - the folder you want to copy
3. **Choose destination** - where you want to copy the folder
4. **Monitor network status** (if using network folders)
5. **Click "Copy Folder"** to start the operation
6. **Review results** in the success/error dialog

### Network Setup

For network folder operations:
1. Go to **Settings > Connection tab**
2. Select "Network Folder" option
3. Enter the target network IP address
4. Use the refresh button to test connectivity
5. Green indicator = connected, Red = disconnected

### Security Features

- **Session Management**: Enter password once per session
- **Logout**: Click logout to end your session
- **Password Change**: Use Security tab to update your password
- **Settings Protection**: All configuration changes require authentication

## Configuration

The application stores settings in `settings.json` with the following format:

```json
{
    "source_path": "/path/to/source",
    "destination_path": "/path/to/destination", 
    "network_ip": "192.168.1.100",
    "password": "your_secure_password",
    "folder_type": "local",
    "auto_close": false,
    "version": "1.0",
    "last_updated": "2025-06-15T10:30:00.000000"
}
```

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| Source Path | Source folder location | Empty |
| Destination Path | Destination folder location | Empty |
| Network IP | IP address for network operations | 127.0.0.1 |
| Password | Settings access password | password |
| Folder Type | local or network | local |
| Auto Close | Close app after successful copy | false |

## Technical Details

### Technical Details

### Architecture
- **GUI Framework**: PyQt6 for modern, native interface
- **Multi-threading**: Background operations for copy and network checking
- **Cross-platform**: Works on Windows, macOS, and Linux
- **File Operations**: Python's `shutil` with progress tracking
- **Real-time Updates**: Signal/slot system for live UI updates
- **Logging**: Comprehensive logging with GUI integration
- **Error Handling**: Multi-layer error handling with user feedback

### Modern UI Features
- **Emoji Integration**: Visual recognition with contextual emojis
  - 📁 Main window and folder operations
  - 🔒 Authentication and security
  - ⚙️ Settings and configuration
  - 🌐 Network connectivity
  - 📊 Progress and monitoring
- **Live Log Display**: Real-time operation monitoring
- **Progress Visualization**: Detailed progress bars and status text
- **Responsive Design**: Proper scaling and modern layouts

### Enhanced Copy Process
The application provides detailed monitoring during copy operations:
1. **Pre-copy Analysis**: Calculates total files and required space
2. **Progress Tracking**: Real-time progress bar (0-100%)
3. **Live Logging**: Each file copy logged with timestamp
4. **Status Updates**: Detailed current operation display
5. **Cancellation Support**: User can cancel mid-operation
6. **Error Recovery**: Automatic rollback on failure

### Copy Progress Stages
- **5%**: Analyzing source folder
- **10%**: Preparing destination
- **15%**: Removing old backup (if needed)
- **20%**: Creating backup of existing folder
- **25-95%**: File-by-file copying with live updates
- **100%**: Copy completed successfully

### Logging System
- **Daily log files** stored in `logs/` directory
- **Multiple log levels**: INFO, WARNING, ERROR
- **Automatic log rotation** by date
- **Detailed operation tracking** for troubleshooting

### Network Testing
- **Windows**: Uses `ping -n 1 -w 3000 [IP]`
- **Unix/Linux/macOS**: Uses `ping -c 1 -W 3 [IP]`
- **Timeout**: 5-second maximum for network tests
- **Background Processing**: Non-blocking network status checks

### Security Considerations
- Passwords stored in plain text (consider encryption for production use)
- Session-based authentication prevents repeated password entry
- Settings file should be kept secure

## Troubleshooting

### Logging and Diagnostics
The application creates detailed logs in the `logs/` directory. Check the most recent log file for detailed error information:
- `logs/app_YYYYMMDD.log` - Daily log files with all operations
- Logs include timestamps, operation details, and error traces
- Use log files to diagnose issues and report bugs

### Common Issues

**Problem**: Network status shows disconnected but network is working
- **Solution**: Check IP address in settings, try manual refresh
- **Check logs**: Look for network timeout or ping errors

**Problem**: Application won't start
- **Solution**: Ensure Python 3.8+ is installed and PyQt6 is available (`pip install PyQt6`)
- **Check logs**: Look for initialization errors in the log file
- **PyQt6 Issues**: Verify PyQt6 installation with `python -c "from PyQt6.QtWidgets import QApplication"`

**Problem**: Copy operation fails
- **Solution**: Check folder permissions, available disk space, and source folder existence
- **Check logs**: Detailed error information will be in the log file

**Problem**: Settings not saving
- **Solution**: Ensure write permissions in application directory
- **Check logs**: Look for JSON write errors or permission issues

**Problem**: "Insufficient disk space" error
- **Solution**: Free up space on the destination drive or choose a different location
- **Details**: The app calculates source folder size and compares with available space

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Please set source and destination folders" | Paths not configured | Configure paths in settings |
| "Source folder does not exist" | Invalid source path | Verify source folder exists and is accessible |
| "No connection to the network" | Network unreachable | Check network settings and connectivity |
| "Insufficient disk space" | Not enough space on destination | Free up space or choose different destination |
| "Failed to delete existing _old folder" | Permission or lock issues | Check folder permissions and close any open files |
| "Incorrect password" | Wrong password entered | Enter correct password or reset |
| "Settings file is corrupted" | Invalid JSON format | App will recreate with defaults, check logs for details |

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** with clear, commented code
4. **Test thoroughly** on multiple platforms if possible
5. **Submit a pull request** with a clear description

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex functionality
- Test on multiple operating systems
- Update documentation for new features
- Maintain the existing code structure

### Code Style
- Use descriptive variable names
- Keep functions focused and small
- Add docstrings for public methods
- Use type hints where beneficial

## Future Enhancements

- [ ] **Advanced Progress Visualization**: File transfer speed, ETA, and bandwidth usage
- [ ] **Enhanced Live Monitoring**: Copy statistics, error counts, and performance metrics
- [ ] Encrypted password storage with secure key management
- [ ] Multiple folder selection with batch operations and queuing
- [ ] Copy scheduling and automation features with cron-like functionality
- [ ] **PyQt6 Advanced Features**: Drag-and-drop interface, system tray integration
- [ ] **Enhanced logging**: Export logs, log viewer interface with filtering
- [ ] **Backup management**: Visual management of `_old` folder versions
- [ ] Theme customization with multiple color schemes and dark mode
- [ ] **Recovery tools**: Advanced backup restoration with preview
- [ ] Integration with cloud storage services (Google Drive, OneDrive, Dropbox)
- [ ] **Performance optimization**: Parallel copying, compression options
- [ ] **Network improvements**: VPN support, advanced connection testing
- [ ] Configuration export/import with profile management
- [ ] **GUI Enhancements**: Animated transitions, modern icons, custom widgets

## License

This project is licensed under the MIT License - see the [LICENSE](#license-text) section below for details.

### License Text

```
MIT License

Copyright (c) 2025 Folder Copier Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Support

- **Issues**: Please report bugs and feature requests via GitHub Issues
- **Documentation**: Additional documentation available in the `/docs` folder
- **Community**: Join discussions in GitHub Discussions

## Acknowledgments

- Built with Python's tkinter for cross-platform compatibility
- Inspired by the need for simple, reliable folder copying tools
- Thanks to the open-source community for continuous inspiration

---

**Made with ❤️ for the community**

*If you find this project useful, please consider giving it a ⭐ on GitHub!*