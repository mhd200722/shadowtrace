# 🛡️ ShadowTrace

**Advanced File Monitoring & Anomaly Detection System**

ShadowTrace is a powerful real-time file monitoring system that combines the speed of C with the flexibility of Python to detect suspicious file activities, anomalies, and potential security threats on your system.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

---

## 🌟 Features

- ⚡ **High-Performance Scanning**: Uses C library for fast directory traversal and file metadata collection
- 🔍 **Real-Time Monitoring**: Continuous surveillance of specified directories with configurable intervals
- 🚨 **Anomaly Detection**: Intelligent detection of:
  - Files modified too frequently
  - Sudden file size increases
  - New file additions
  - File deletions
- 📧 **Email Alerts**: Automated email reports with detailed security analysis
- 📊 **Behavioral Profiling**: Tracks file modification patterns over time
- 🎨 **Beautiful CLI**: Colorful terminal output with clear status indicators

---

## 📋 Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Email Setup](#email-setup)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mhd200722/shadowtrace.git
cd shadowtrace
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Compile the C Library

**For Windows (using MinGW or MSVC):**
```bash
gcc -shared -o libcheckpass.so file_scanner.c -lkernel32
```

**For Linux (cross-compile for Windows):**
```bash
x86_64-w64-mingw32-gcc -shared -o libcheckpass.so file_scanner.c
```

### 4. Verify Installation
```bash
python shadowtrace.py
```

---

## 📦 Requirements

### Python Packages
- `ctypes` (built-in)
- `pyfiglet` - ASCII art for CLI
- `termcolor` - Colored terminal output
- `smtplib` (built-in) - Email functionality

Install with:
```bash
pip install pyfiglet termcolor
```

### System Requirements
- **OS**: Windows 7/8/10/11
- **Python**: 3.8 or higher
- **Compiler**: GCC (MinGW) or MSVC for C compilation
- **RAM**: Minimum 256MB
- **Disk**: 50MB free space

---

## ⚡ Quick Start

### Basic Usage
```bash
python shadowtrace.py
```

Follow the interactive prompts:
1. Enter the directory path to monitor
2. Set number of scans (default: 10)
3. Set scan interval in seconds (default: 60)
4. Choose whether to send email reports

### Example Session
```
🔍 Enter Your Path Directory: C:\Users\YourName\Documents
🔄 Enter Number Of Scans (Default: 10): 5
⏱️ Enter Scan Interval in seconds (Default: 60): 30
📧 Send email report after completion? [Y/N]: Y
```

---

## 🔧 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     ShadowTrace System                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Main Entry Point (shadowtrace.py)                       │
│     └─> User Interface & Configuration                      │
│                                                             │
│  2. File Monitor (file_monitor.py)                          │
│     ├─> Python-C Interface                                  │
│     ├─> Snapshot Management                                 │
│     ├─> Change Detection                                    │
│     └─> Anomaly Detection Engine                            │
│                                                             │
│  3. C File Scanner (file_scanner.c/h)                       │
│     ├─> Fast Directory Traversal                            │
│     ├─> Metadata Collection                                 │
│     └─> Memory Management                                   │
│                                                             │
│  4. Email Reporter (email_reporter.py)                      │
│     └─> Email Generation & Delivery                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Detection Workflow

1. **Initial Scan**: Creates baseline snapshot of all files
2. **Periodic Scanning**: Rescans directory at specified intervals
3. **Change Detection**: Compares snapshots to identify:
   - Added files
   - Deleted files
   - Modified files (size/timestamp changes)
4. **Anomaly Analysis**: Evaluates behavioral patterns:
   - Modification frequency
   - Size growth rate
   - Temporal patterns
5. **Reporting**: Generates detailed reports and sends email alerts

---

## 📁 File Structure

```
shadowtrace/
├── shadowtrace.py              # Main entry point
├── file_monitor.py             # Core monitoring logic
├── file_scanner.c              # C library for fast scanning
├── file_scanner.h              # C header file
├── email_reporter.py           # Email notification system
├── libcheckpass.so             # Compiled C library
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── DOCUMENTATION.docx          # Detailed documentation
└── LICENSE                     # License file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `shadowtrace.py` | Main CLI interface and program entry point |
| `file_monitor.py` | Python monitoring engine with anomaly detection |
| `file_scanner.c/h` | High-performance C scanning library |
| `email_reporter.py` | Email report generation and SMTP delivery |
| `file_scanner.dll` | Compiled shared library |

---

## ⚙️ Configuration

### Anomaly Detection Parameters

Edit `file_monitor.py` to adjust detection sensitivity:

```python
def detect_anomalies(snapshot, behavior_profile, 
                     mod_threshold=3,      # Files modified > 3 times
                     growth_factor=2.0):   # Size increase > 2x
```

### Email Configuration

Edit `email_reporter.py`:

```python
def send_anomaly_report(monitoring_results, 
                        receiver_email="your@email.com"):
    email = "sender@gmail.com"
    # Configure SMTP settings
```

### Scan Settings

Modify defaults in `shadowtrace.py`:

```python
num_of_scan = int(input(...) or "10")      # Default scans
scan_interval = int(input(...) or "60")    # Default interval (seconds)
```

---

## 💡 Usage Examples

### Example 1: Monitor Downloads Folder
```bash
python shadowtrace.py
# Path: C:\Users\YourName\Downloads
# Scans: 20
# Interval: 30
# Email: Y
```

### Example 2: Quick Security Check
```bash
python shadowtrace.py
# Path: C:\Important\Files
# Scans: 3
# Interval: 10
# Email: N
```

### Example 3: Long-term Surveillance
```bash
python shadowtrace.py
# Path: C:\Users\YourName\Documents
# Scans: 100
# Interval: 300  # 5 minutes
# Email: Y
```

---

## 📧 Email Setup

### Gmail Configuration

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Select "Mail" and your device
   - Copy the generated password

3. **Update `email_reporter.py`**:
```python
server.login("your@gmail.com", "your-app-password")
```

### Other Email Providers

For other SMTP providers, modify the server settings:

```python
# Gmail
server = smtplib.SMTP("smtp.gmail.com", 587)

# Outlook
server = smtplib.SMTP("smtp-mail.outlook.com", 587)

# Yahoo
server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
```

---

## 🔍 Understanding the Output

### Console Output Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | File added |
| 🗑️ | File deleted |
| 📝 | File modified |
| ⚠️ | Anomaly detected |
| ✓ | No anomalies found |

### Anomaly Types

1. **Modified Too Often**: File changed more than threshold times
2. **Sudden Growth**: File size increased by growth factor
3. **New File Detected**: Appears in "Added" section, not as anomaly (fixed!)

---

## 🛠️ Troubleshooting

### Common Issues

**Problem**: `FileNotFoundError: file_scanner.dll`
```bash
# Solution: Compile the C library
gcc -shared -o file_scanner.dll file_scanner.c -lkernel32
```

**Problem**: Email not sending
```bash
# Solution: Check SMTP credentials and app password
# Enable "Less secure app access" if using Gmail
```

**Problem**: Permission denied on directory
```bash
# Solution: Run as administrator or choose accessible directory
```

**Problem**: All files shown as anomalies on first run
```bash
# Solution: This is fixed in the latest version!
# Update file_monitor.py from the repository
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Comment your code appropriately
- Test on Windows before submitting
- Update documentation for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Windows API for file system operations
- Python `ctypes` for C integration
- Email functionality powered by `smtplib`
- Terminal styling by `termcolor` and `pyfiglet`

---

## 📞 Support

For issues, questions, or suggestions:
- 🐛 [Report a Bug](https://github.com/yourusername/shadowtrace/issues)
- 💡 [Request a Feature](https://github.com/yourusername/shadowtrace/issues)
- 📧 Email: mohamedehab200722@gmail.com

---

## 🚀 Future Enhancements

- [ ] Linux/macOS support
- [ ] GUI interface
- [ ] Database logging
- [ ] Machine learning anomaly detection
- [ ] Multi-directory monitoring
- [ ] Configurable rules engine
- [ ] Web dashboard
- [ ] Integration with SIEM systems

---

<div align="center">

**Made with ❤️ for Security & Monitoring**

⭐ Star this repo if you find it useful!

</div>
