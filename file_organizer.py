#!/usr/bin/env python3
"""
File Organizer

This script organizes files in a directory into different categories based on their file extensions.
"""

import os
import shutil
import logging
from pathlib import Path
import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_organizer.log"),
        logging.StreamHandler()
    ]
)

class FileOrganizer:
    """Class to organize files into different folders based on their extensions."""
    
    def __init__(self, source_dir=None, exception_folders=None):
        """Initialize the organizer with the source directory and file categories."""
        # If no source directory is provided, use the Downloads folder
        self.source_dir = source_dir or str(Path.home() / "Downloads")
        
        # Exception folders that will be excluded from organization
        self.exception_folders = exception_folders or []
        
        # Define file categories and their extensions
        self.category_extensions = {
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
        }
        
        # Define destination directories (subfolders in the source directory)
        self.destination_dirs = {
            category: os.path.join(self.source_dir, category)
            for category in list(self.category_extensions.keys()) + ["Others"]
        }
    
    def get_category(self, file_path):
        """Determine the category of a file based on its extension."""
        _, ext = os.path.splitext(file_path.lower())
        
        if not ext:  # Files without extensions
            return "Others"
        
        # Check each category for matching extensions
        for category, extensions in self.category_extensions.items():
            if ext in extensions:
                return category
        
        # If no match found, categorize as "Others"
        return "Others"
    
    def create_destination_folder(self, category):
        """Create a specific destination folder if it doesn't exist."""
        folder = self.destination_dirs[category]
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"Created directory: {folder}")
    
    def move_file(self, file_path, destination):
        """Move a file to the destination folder, handling duplicate filenames."""
        if not os.path.exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            return False
        
        filename = os.path.basename(file_path)
        dest_path = os.path.join(destination, filename)
        
        # If a file with the same name already exists in the destination
        counter = 1
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{counter}{ext}"
            dest_path = os.path.join(destination, new_filename)
            counter += 1
        
        try:
            shutil.move(file_path, dest_path)
            logging.info(f"Moved: {file_path} -> {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to move {file_path}: {str(e)}")
            return False
    
    def remove_empty_folders(self, directory):
        """Recursively remove empty folders."""
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                
                # Skip the destination directories
                if dir_path in self.destination_dirs.values():
                    continue
                
                try:
                    # Check if the directory is empty (no files and no subdirectories)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        logging.info(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    logging.error(f"Failed to remove directory {dir_path}: {str(e)}")
    
    def is_excluded(self, path):
        """Check if a path is in an exception folder."""
        # Check if the path is in any of the exception folders
        for exception in self.exception_folders:
            if os.path.commonpath([path, exception]) == exception:
                return True
        return False
    
    def organize_files(self):
        """Organize files in the source directory into appropriate categories."""
        # Initialize statistics
        stats = {
            "total_processed": 0,
            "total_moved": 0,
            "by_category": {category: 0 for category in self.destination_dirs.keys()}
        }
        
        # First, scan all files to determine which categories we need to create
        needed_categories = set()
        files_to_move = []
        
        # Process files
        for root, _, files in os.walk(self.source_dir):
            # Skip exception folders
            if self.is_excluded(root):
                logging.info(f"Skipping exception folder: {root}")
                continue
                
            for filename in files:
                # Skip hidden files and this script itself
                if filename.startswith('.') or filename == os.path.basename(__file__):
                    continue
                
                file_path = os.path.join(root, filename)
                
                # Skip files already in a destination folder
                if any(root.startswith(dest) for dest in self.destination_dirs.values()):
                    continue
                
                # Determine the category
                category = self.get_category(file_path)
                
                # Add to needed categories
                needed_categories.add(category)
                
                # Add to files to move
                files_to_move.append((file_path, category))
                
                stats["total_processed"] += 1
        
        # Create only the needed destination folders
        for category in needed_categories:
            self.create_destination_folder(category)
        
        # Move the files
        for file_path, category in files_to_move:
            destination = self.destination_dirs[category]
            if self.move_file(file_path, destination):
                stats["total_moved"] += 1
                stats["by_category"][category] += 1
        
        # Clean up empty directories
        self.remove_empty_folders(self.source_dir)
        
        # Log summary
        logging.info(f"Organization complete. Processed {stats['total_processed']} files, moved {stats['total_moved']} files.")
        for category, count in stats["by_category"].items():
            if count > 0:
                logging.info(f"  {category}: {count} files")
        
        return stats

if __name__ == "__main__":
    # Get the current time for the log
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Starting file organization at {current_time}")
    
    # Create and run the organizer
    organizer = FileOrganizer()
    stats = organizer.organize_files()
    
    print(f"\nOrganization complete!")
    print(f"Processed {stats['total_processed']} files")
    print(f"Moved {stats['total_moved']} files to their respective folders")

def main():
    """Entry point for the command-line tool."""
    # Get the current time for the log
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Starting file organization at {current_time}")
    
    # Create and run the organizer
    organizer = FileOrganizer()
    stats = organizer.organize_files()
    
    print(f"\nOrganization complete!")
    print(f"Processed {stats['total_processed']} files")
    print(f"Moved {stats['total_moved']} files to their respective folders")
    
    return 0
