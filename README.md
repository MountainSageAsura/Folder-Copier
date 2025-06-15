# Folder Copier Pro

A modern, user-friendly GUI application for copying folders between local and network locations with advanced features including network connectivity monitoring, session management, and customizable preferences.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

### 🎨 Modern Interface
- Beautiful pastel color palette
- Clean, intuitive design
- Responsive layout with proper spacing
- Professional typography using Segoe UI

### 📁 Folder Management
- Easy source and destination folder selection
- Support for both local and network folders
- Real-time folder path display
- Intelligent folder conflict handling

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
- Robust folder copying with error handling
- Destination conflict detection and resolution
- Optional auto-close after successful copy
- Detailed success/error reporting

### 💾 Configuration Management
- Persistent settings storage
- Automatic settings loading on startup
- Comprehensive configuration backup

## Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)
- Standard library modules: `os`, `shutil`, `subprocess`, `platform`, `threading`

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

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

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

The application stores settings in `settings.txt` with the following format:

```
# Source folder path
/path/to/source

# Destination folder path
/path/to/destination

# Network IP address
192.168.1.100

# Password
your_secure_password

# Folder type (local/network)
local

# Auto close after copy
false
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

### Architecture
- **GUI Framework**: tkinter with ttk for modern widgets
- **Threading**: Network operations run in background threads
- **Cross-platform**: Works on Windows, macOS, and Linux
- **File Operations**: Uses Python's `shutil` for reliable folder copying

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

### Common Issues

**Problem**: Network status shows disconnected but network is working
- **Solution**: Check IP address in settings, try manual refresh

**Problem**: Application won't start
- **Solution**: Ensure Python 3.6+ is installed and tkinter is available

**Problem**: Copy operation fails
- **Solution**: Check folder permissions and available disk space

**Problem**: Settings not saving
- **Solution**: Ensure write permissions in application directory

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Please set source and destination folders" | Paths not configured | Configure paths in settings |
| "No connection to the network" | Network unreachable | Check network settings and connectivity |
| "Destination folder already exists" | Target exists | Choose overwrite or select different destination |
| "Incorrect password" | Wrong password entered | Enter correct password or reset |

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

- [ ] Encrypted password storage
- [ ] Progress bar for large copy operations
- [ ] Multiple folder selection
- [ ] Copy scheduling and automation
- [ ] Detailed copy logs and history
- [ ] Theme customization options
- [ ] Backup and restore functionality
- [ ] Integration with cloud storage services

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