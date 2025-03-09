# AutoFolder

A modern Python application that automatically organizes files by sorting them into different categories with a sleek, minimalist interface.

## Features

- Automatically creates destination folders if they don't exist
- Handles duplicate filenames by adding a counter
- Skips hidden files and the script itself
- Provides a summary of the organization process
- Logs all actions for troubleshooting
- **Recursively scans subdirectories** and organizes all files found within them
- Removes empty folders after files have been organized
- **Modern web interface** for selecting source folders and customizing file categories

## Categories

Files are sorted into the following folders:

- **Music & Video**: Audio and video files (.mp3, .mp4, .wav, .mov, etc.)
- **PDFs**: PDF and e-book files (.pdf, .epub, .mobi)
- **Images**: Image files (.jpg, .png, .gif, .tif, .webp, etc.)
- **Dmg & Zips**: Compressed and disk image files (.zip, .rar, .dmg, etc.)
- **CAD & 3Dmodel**: CAD and 3D model files (.dwg, .dxf, .stl, .3dm, etc.)
- **Others**: Any files that don't match the above categories

## Usage Options

### Web Interface (Recommended)

The easiest way to use AutoFolder is through the web interface:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the web server:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8765
   ```

4. Use the sleek interface to:
   - Select the source folder to organize
   - Choose which categories to include
   - Customize file extensions for each category
   - Click "Organize Files" to start the process

### Command Line

You can also use the script directly from the command line:

```bash
python file_organizer.py
```

This will organize your Downloads folder using the default settings.

### Python API

For advanced users, you can import the FileOrganizer class in your own scripts:

```python
from file_organizer import FileOrganizer

# Create an organizer for a custom directory
organizer = FileOrganizer(source_dir="/path/to/your/folder")

# Run the organization process
stats = organizer.organize_files()
print(f"Moved {stats['total_moved']} out of {stats['total_processed']} files")
```

## Customizing File Categories

From the web interface, you can:

1. View and edit which file extensions belong to each category
2. Add new extensions for any category
3. Click on an extension to remove it

Your customizations will be saved for future use.

## Requirements

- Python 3.6 or higher
- Flask (for web interface)
- No other external dependencies for core functionality (uses Python standard library)

## Created By

LVRT
