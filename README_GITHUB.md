# AutoFolder

A modern Python application that automatically organizes files by sorting them into different categories with a sleek, minimalist interface.

![AutoFolder Screenshot](https://github.com/yourusername/autofolder/raw/main/screenshots/screenshot.png)

## Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/yourusername/autofolder.git
cd autofolder

# Install dependencies
pip install -r requirements.txt
```

### Using pip (coming soon)

```bash
pip install autofolder
```

## Quick Start

### Web Interface

```bash
# Start the web interface
python run.py

# Open your browser and navigate to:
# http://127.0.0.1:8765
```

### Command Line

```bash
# Organize your Downloads folder with default settings
python file_organizer.py
```

## Features

- Automatically creates destination folders if they don't exist
- Handles duplicate filenames by adding a counter
- Skips hidden files and the script itself
- Provides a summary of the organization process
- Logs all actions for troubleshooting
- **Recursively scans subdirectories** and organizes all files found within them
- Removes empty folders after files have been organized
- **Modern web interface** for selecting source folders and customizing file categories

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 