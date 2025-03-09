#!/usr/bin/env python3
"""
Helper script to move previously miscategorized files to their correct folders
"""

import os
import shutil
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def move_file(source_path, destination_folder):
    """Move a file to its destination folder, handling duplicates."""
    try:
        filename = os.path.basename(source_path)
        dest_path = os.path.join(destination_folder, filename)
        
        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        
        while os.path.exists(dest_path):
            new_filename = f"{base}_{counter}{ext}"
            dest_path = os.path.join(destination_folder, new_filename)
            counter += 1
        
        shutil.move(source_path, dest_path)
        logging.info(f"Moved: {filename} -> {destination_folder}")
        return True
    except Exception as e:
        logging.error(f"Error moving {source_path}: {e}")
        return False

def main():
    """Fix the categorization of previously miscategorized files."""
    print("Fixing file categorization...")
    
    # Define paths
    downloads_dir = os.path.expanduser("~/Downloads")
    others_dir = os.path.join(downloads_dir, "Others")
    images_dir = os.path.join(downloads_dir, "Images")
    cad_dir = os.path.join(downloads_dir, "CAD & 3Dmodel")
    
    # Ensure destination directories exist
    for directory in [images_dir, cad_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Find all .tif files in Others and move to Images
    tif_files = []
    for root, _, files in os.walk(others_dir):
        for file in files:
            if file.lower().endswith('.tif') or file.lower().endswith('.tiff'):
                tif_files.append(os.path.join(root, file))
    
    # Find all .3dm files in Others and move to CAD & 3Dmodel
    threedm_files = []
    for root, _, files in os.walk(others_dir):
        for file in files:
            if file.lower().endswith('.3dm'):
                threedm_files.append(os.path.join(root, file))
    
    # Move the files
    moved_count = 0
    
    for file_path in tif_files:
        if move_file(file_path, images_dir):
            moved_count += 1
    
    for file_path in threedm_files:
        if move_file(file_path, cad_dir):
            moved_count += 1
    
    print(f"Moved {moved_count} files to their correct categories")
    print("Done!")

if __name__ == "__main__":
    main()
