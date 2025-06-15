# 📁 Enhanced Folder Copier

A modern, user-friendly GUI application for copying folders with support for both local and network destinations. Built with PyQt6 and featuring a beautiful pastel color palette inspired by modern design trends.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)

## ✨ Features

- **🎨 Modern UI Design**: Beautiful pastel color palette with smooth animations and hover effects
- **📁 Local & Network Support**: Copy folders to local drives or network locations
- **🔒 Password Protection**: Secure settings with password authentication
- **🌐 Network Status Monitoring**: Real-time network connectivity checking with visual indicators
- **🔄 Auto-Close Option**: Automatically close application after successful copy operations
- **📊 Progress Tracking**: Real-time progress updates with file count and percentage
- **🗂️ Smart Backup**: Automatically creates backups of existing destination folders
- **⚙️ Persistent Settings**: All configurations are saved and restored between sessions
- **🚪 Session Management**: Stay logged in during the session with logout option
- **📝 Comprehensive Logging**: Detailed logging with rotation for troubleshooting

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- PyQt6

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Alternative Installation

```bash
pip install PyQt6>=6.4.0
```

## 📋 Usage

### Running the Application

```bash
python main.py
```

### First Time Setup

1. **Launch the application**
2. **Click Settings** (default password: `password123`)
3. **Configure your paths**:
   - Set source folder (folder to copy from)
   - Set destination folder (where to copy to)
   - Choose between Local or Network folder type
4. **Network Setup** (if using network folders):
   - Enter the network IP address
   - Test the connection using the "Test Connection" button
5. **Optional Settings**:
   - Change the password for security
   - Enable auto-close after successful copy
6. **Save settings**

### Copying Folders

1. **Ensure source and destination are configured**
2. **For network folders**: Check that the network status shows green (connected)
3. **Click "Start Copy"**
4. **Monitor progress** in the status area
5. **Wait for completion message**

### Network Status Indicators

- 🟢 **Green**: Connected to network
- 🔴 **Red**: Cannot reach network
- 🟡 **Yellow**: Checking connection
- 🔄 **Refresh Button**: Manually recheck network status

## 🏗️ Project Structure

```
enhanced-folder-copier/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── settings_dialog.py # Settings configuration dialog
│   └── password_dialog.py # Password authentication dialog
├── core/                  # Core application logic
│   ├── __init__.py
│   ├── copy_worker.py     # Background copy operations
│   └── settings_manager.py # Settings persistence
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── network_checker.py # Network connectivity utilities
│   ├── styles.py          # Modern UI styling
│   └── logger.py          # Logging configuration
└── logs/                  # Application logs (created automatically)
    └── folder_copier.log
```

## 🎨 Design Philosophy

This application follows modern UI/UX principles:

- **Pastel Color Palette**: Soft, easy-on-the-eyes colors that reduce fatigue
- **Intuitive Navigation**: Clear visual hierarchy and logical flow
- **Responsive Feedback**: Immediate visual feedback for all user actions
- **Accessibility**: High contrast ratios and clear typography
- **Consistency**: Uniform spacing, sizing, and styling throughout

## ⚙️ Configuration

### Settings File

Settings are automatically saved to `settings.json` in the application directory:

```json
{
  "source_path": "/path/to/source",
  "destination_path": "/path/to/destination", 
  "network_ip": "192.168.1.100",
  "password": "your_password",
  "folder_type": "local",
  "auto_close": false,
  "version": "3.0"
}
```

### Logging

Logs are saved to the `logs/` directory with automatic rotation:
- Maximum file size: 5MB
- Backup files: 3
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🔧 Advanced Features

### Backup Strategy

When copying to an existing destination:
1. If `destination_old` exists, it's deleted
2. Current destination is renamed to `destination_old`
3. New copy proceeds to the original destination name

### Network Connectivity

The application supports various network protocols:
- **Ping**: Primary connectivity test
- **TCP Connection**: Fallback for restricted networks
- **SMB/CIFS**: Specific support for Windows shares

### Session Management

- **Authentication**: Required for accessing settings
- **Session Persistence**: Stay logged in while application is running
- **Secure Logout**: Clear authentication state when needed

## 🐛 Troubleshooting

### Common Issues

**"Permission Denied" Errors**
- Run as administrator/sudo if copying system files
- Check folder permissions
- Ensure destination is writable

**Network Connection Problems** 
- Verify IP address is correct
- Check firewall settings
- Ensure network share is accessible
- Try pinging the target manually

**Application Won't Start**
- Check Python version (3.8+ required)
- Verify PyQt6 installation: `pip list | grep PyQt6`
- Check logs in `logs/folder_copier.log`

### Getting Help

1. **Check the logs** in `logs/folder_copier.log`
2. **Enable debug logging** by modifying the log level in `main.py`
3. **Test network connectivity** using the built-in test feature
4. **Reset settings** by deleting `settings.json`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the application**: `python main.py`
4. **Make your changes**
5. **Test thoroughly**
6. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](#license-text) section below for details.

## 🙏 Acknowledgments

- **PyQt6** for the excellent GUI framework
- **Modern UI Design** inspiration from contemporary web applications
- **Comic Book to PDF Converter** for design inspiration
- **Community** for feedback and suggestions

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Review the logs** for error details
3. **Open an issue** on the repository
4. **Provide detailed information** including logs and steps to reproduce

---

## License Text

MIT License

Copyright (c) 2024 Enhanced Folder Copier Contributors

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