#!/usr/bin/env python3
"""
Web-based AutoFolder

This application provides a modern browser interface for organizing files into categorized folders.
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Import the file organizer functionality
from file_organizer import FileOrganizer

app = Flask(__name__)

# Default configuration
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'category_extensions': {
        "Music & Video": [
            ".mp3", ".mp4", ".wav", ".flac", ".aac", ".m4a", ".ogg", 
            ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"
        ],
        "PDFs": [".pdf", ".epub", ".mobi"],
        "Images": [
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", 
            ".svg", ".ico", ".heic", ".heif", ".raw", ".psd", ".ai"
        ],
        "Dmg & Zips": [
            ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".dmg", 
            ".iso", ".pkg", ".deb", ".rpm"
        ],
        "CAD & 3Dmodel": [
            ".dwg", ".dxf", ".stl", ".obj", ".3ds", ".step", ".stp", 
            ".iges", ".igs", ".x_t", ".x_b", ".xmt", ".xmt_txt", ".skp", ".3dm"
        ]
    },
    'exception_folders': [],
    'active_categories': [
        "Music & Video",
        "PDFs",
        "Images",
        "Dmg & Zips",
        "CAD & 3Dmodel",
        "Others"
    ]
}

def load_config():
    """Load configuration from file or create with defaults if not exists."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_CONFIG.copy()
    else:
        # Create default config file
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

@app.route('/')
def index():
    """Render the main interface"""
    # Get common directories for quick selection
    home_dir = str(Path.home())
    downloads_dir = str(Path.home() / "Downloads")
    documents_dir = str(Path.home() / "Documents")
    desktop_dir = str(Path.home() / "Desktop")
    
    common_dirs = [
        {"path": downloads_dir, "name": "Downloads"},
        {"path": documents_dir, "name": "Documents"},
        {"path": desktop_dir, "name": "Desktop"},
        {"path": home_dir, "name": "Home"}
    ]
    
    # Get saved configuration
    config = load_config()
    
    # Use the correct key 'category_extensions' instead of 'categories'
    return render_template(
        'index.html', 
        common_dirs=common_dirs,
        categories=config['category_extensions'],
        exception_folders=config.get('exception_folders', []),
        active_categories=config['active_categories']
    )

@app.route('/browse')
def browse():
    """Browse the file system to select a directory"""
    # Get the current directory from the request, default to home
    current_dir = request.args.get('dir', str(Path.home()))
    
    # Ensure the directory exists and is accessible
    if not os.path.isdir(current_dir):
        current_dir = str(Path.home())
    
    # Get all subdirectories
    try:
        subdirs = [
            {
                'name': d,
                'path': os.path.join(current_dir, d)
            }
            for d in sorted(os.listdir(current_dir))
            if os.path.isdir(os.path.join(current_dir, d)) and not d.startswith('.')
        ]
    except PermissionError:
        subdirs = []
        
    # Get parent directory
    parent_dir = os.path.dirname(current_dir)
    
    return render_template(
        'browse.html', 
        current_dir=current_dir,
        subdirs=subdirs,
        parent_dir=parent_dir
    )

@app.route('/organize', methods=['POST'])
def organize():
    """Organize files based on the provided configuration"""
    data = request.form
    source_dir = data.get('source_dir')
    
    # Validate source directory
    if not source_dir or not os.path.isdir(source_dir):
        return jsonify({"error": "Invalid source directory"}), 400
    
    # Get selected categories
    selected_categories = request.form.getlist('categories[]')
    
    # Get configuration
    config = load_config()
    
    # Update active categories based on selection
    config["active_categories"] = selected_categories
    
    # Save updated configuration
    save_config(config)
    
    # Create a custom organizer based on the selected categories
    organizer = FileOrganizer(
        source_dir=source_dir,
        exception_folders=config.get('exception_folders', [])
    )
    
    # Update the organizer's category mapping to only include selected categories
    selected_extensions = {}
    for category in selected_categories:
        if category == "Others":
            continue  # "Others" is handled automatically
        if category in config["category_extensions"]:
            selected_extensions[category] = config["category_extensions"][category]
    
    # Set the extensions to use
    organizer.category_extensions = selected_extensions
    
    # Update destination directories based on selected categories
    organizer.destination_dirs = {
        category: os.path.join(source_dir, category)
        for category in selected_categories
    }
    
    # Run the organization process
    stats = organizer.organize_files()
    
    return jsonify({
        "success": True,
        "message": f"Organization complete. Processed {stats['total_processed']} files, moved {stats['total_moved']} files.",
        "stats": stats
    })

@app.route('/save-config', methods=['POST'])
def save_config_endpoint():
    """Save the extension mappings configuration"""
    data = request.json
    
    if not data or "categories" not in data:
        return jsonify({"error": "Invalid configuration data"}), 400
    
    # Get current config and update with new data
    config = load_config()
    config["category_extensions"] = data["categories"]
    
    # Save updated configuration
    save_config(config)
    
    return jsonify({"success": True})

@app.route('/reset-config', methods=['POST'])
def reset_config():
    """Reset configuration to defaults"""
    save_config(DEFAULT_CONFIG)
    return redirect(url_for('index'))

@app.route('/exception_folders', methods=['GET'])
def get_exception_folders():
    """Get list of exception folders."""
    config = load_config()
    return jsonify(config.get('exception_folders', []))

@app.route('/exception_folders', methods=['POST'])
def add_exception_folder():
    """Add an exception folder."""
    data = request.get_json()
    if not data or 'folder' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    folder = data['folder']
    if not os.path.exists(folder) or not os.path.isdir(folder):
        return jsonify({'error': 'Invalid folder path'}), 400
    
    config = load_config()
    if folder not in config.get('exception_folders', []):
        config.setdefault('exception_folders', []).append(folder)
        save_config(config)
    
    return jsonify({'success': True, 'exception_folders': config.get('exception_folders', [])})

@app.route('/exception_folders/<path:folder>', methods=['DELETE'])
def remove_exception_folder(folder):
    """Remove an exception folder."""
    config = load_config()
    if folder in config.get('exception_folders', []):
        config.setdefault('exception_folders', []).remove(folder)
        save_config(config)
    
    return jsonify({'success': True, 'exception_folders': config.get('exception_folders', [])})

if __name__ == '__main__':
    # Make sure config exists
    load_config()
    app.run(debug=True, port=8765)
