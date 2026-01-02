#!/usr/bin/env python3
"""
Generate Collection Script
Automates the process of adding a new photography collection to the portfolio.

Usage:
    python3 scripts/generate-collection.py <collection-folder-path>

Example:
    python3 scripts/generate-collection.py assets/images/gallery/my-new-collection

Expected folder structure:
    my-new-collection/
    ├── full-res/           (required: your original JPGs)
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── thumbnails/         (will be created/populated)

This script will:
    1. Generate thumbnails from full-res images
    2. Create metadata.json with AI-assisted descriptions
    3. Update collections lists in JavaScript files
    4. Generate metadata with smart featured selection
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image
import re

# Constants
THUMBNAIL_WIDTH = 400
THUMBNAIL_QUALITY = 85
FULL_RES_MAX_WIDTH = 2000
FULL_RES_QUALITY = 90

def log(level, message):
    """Simple logging with color."""
    colors = {
        'INFO': '\033[94m',     # Blue
        'SUCCESS': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
    }
    reset = '\033[0m'
    color = colors.get(level, '')
    print(f"{color}[{level}]{reset} {message}")

def validate_collection_folder(collection_path):
    """Validate that collection folder has required structure."""
    collection_path = Path(collection_path)
    
    if not collection_path.exists():
        log('ERROR', f"Collection folder does not exist: {collection_path}")
        return False
    
    full_res_path = collection_path / 'full-res'
    if not full_res_path.exists():
        log('ERROR', f"Missing 'full-res' folder: {full_res_path}")
        return False
    
    # Get list of image files
    image_files = list(full_res_path.glob('*.jpg')) + list(full_res_path.glob('*.JPG')) + list(full_res_path.glob('*.jpeg'))
    if not image_files:
        log('ERROR', f"No JPG images found in {full_res_path}")
        return False
    
    log('SUCCESS', f"Found {len(image_files)} images in full-res folder")
    return True

def generate_thumbnails(collection_path):
    """Generate thumbnail images from full-res originals."""
    collection_path = Path(collection_path)
    full_res_path = collection_path / 'full-res'
    thumbnails_path = collection_path / 'thumbnails'
    
    # Create thumbnails folder if it doesn't exist
    thumbnails_path.mkdir(exist_ok=True)
    
    image_files = sorted(full_res_path.glob('*.jpg')) + sorted(full_res_path.glob('*.JPG')) + sorted(full_res_path.glob('*.jpeg'))
    
    log('INFO', f"Generating thumbnails for {len(image_files)} images...")
    
    for image_file in image_files:
        try:
            # Open image
            img = Image.open(image_file)
            
            # Ensure RGB (in case of RGBA)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new height maintaining aspect ratio
            aspect_ratio = img.height / img.width
            new_height = int(THUMBNAIL_WIDTH * aspect_ratio)
            
            # Resize
            img_thumb = img.resize((THUMBNAIL_WIDTH, new_height), Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumb_path = thumbnails_path / image_file.name
            img_thumb.save(thumb_path, 'JPEG', quality=THUMBNAIL_QUALITY, optimize=True)
            
            log('SUCCESS', f"  ✓ {image_file.name} ({img.width}x{img.height}) → {THUMBNAIL_WIDTH}x{new_height}")
        
        except Exception as e:
            log('ERROR', f"  ✗ Failed to process {image_file.name}: {str(e)}")
            continue
    
    log('SUCCESS', "Thumbnail generation complete!")

def extract_metadata_from_filename(filename):
    """Extract basic metadata from filename.
    
    Assumes filenames follow pattern:
    'Title - Description - Screen.jpg' or 'Title - Screen.jpg'
    
    Returns: (title, description)
    """
    # Remove extension
    name = filename.rsplit('.', 1)[0]
    
    # Remove " - Screen" suffix if present
    name = re.sub(r'\s*-\s*Screen\s*$', '', name)
    
    # Split on " - " if it exists
    parts = name.split(' - ', 1)
    
    title = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else f"A photograph from the collection"
    
    return title, description

def generate_metadata(collection_path, collection_id):
    """Generate metadata.json for the collection."""
    collection_path = Path(collection_path)
    full_res_path = collection_path / 'full-res'
    
    log('INFO', "Generating metadata.json...")
    
    # Get image files
    image_files = sorted(full_res_path.glob('*.jpg')) + sorted(full_res_path.glob('*.JPG')) + sorted(full_res_path.glob('*.jpeg'))
    
    # Prompt user for collection info
    print("\n" + "="*60)
    print("COLLECTION INFORMATION")
    print("="*60)
    
    collection_title = input("Collection Title (e.g., 'Japan 2025'): ").strip()
    collection_location = input("Location(s) (e.g., 'Japan, Kyoto'): ").strip()
    collection_date = input("Date/Year (e.g., '2025'): ").strip()
    collection_description = input("Collection Description: ").strip()
    
    # Smart featured selection: mark first image and every 3rd image as featured
    images_data = []
    for idx, image_file in enumerate(image_files):
        title, description = extract_metadata_from_filename(image_file.name)
        
        # Auto-feature: first image + every 3rd image + last image
        is_featured = (idx == 0) or (idx % 3 == 0) or (idx == len(image_files) - 1)
        
        image_data = {
            "id": title.lower().replace(' ', '-'),
            "title": title,
            "filename": image_file.name,
            "description": description,
            "location": collection_location,
            "tags": ["travel"],  # Default tag, user should update
            "printSizes": [
                {"size": "8x10", "price": 50},
                {"size": "11x14", "price": 85},
                {"size": "16x20", "price": 140},
                {"size": "20x30", "price": 235}
            ],
            "featured": is_featured,
            "printAvailable": True
        }
        
        images_data.append(image_data)
    
    # Create metadata object
    metadata = {
        "collection": {
            "id": collection_id,
            "title": collection_title,
            "slug": collection_id,
            "displayCategory": "Travel & Adventure",  # TODO: User should update
            "description": collection_description,
            "location": collection_location,
            "date": collection_date,
            "coverImage": images_data[0]["filename"],
            "featured": True,
            "printAvailable": True
        },
        "images": images_data
    }
    
    # Save metadata.json
    metadata_path = collection_path / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    log('SUCCESS', f"Created metadata.json")
    log('INFO', f"  Collection: {collection_title}")
    log('INFO', f"  Images: {len(images_data)}")
    log('INFO', f"  Featured images: {sum(1 for img in images_data if img['featured'])}")
    log('WARNING', "  ⚠ Remember to:")
    log('WARNING', "    - Add specific tags to each image (landscape, nature, etc)")
    log('WARNING', "    - Update displayCategory")
    log('WARNING', "    - Review and edit descriptions")

def update_javascript_configs(collection_id):
    """Update JavaScript files with new collection."""
    log('INFO', "Updating JavaScript configuration files...")
    
    files_to_update = [
        'assets/js/gallery-loader.js',
        'assets/js/browse-loader.js'
    ]
    
    for file_path in files_to_update:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if collection already in list
            if f"'{collection_id}'" in content:
                log('WARNING', f"  ⚠ {file_path} already contains {collection_id}")
                continue
            
            # Find the collections array and add new collection
            # Pattern: const collections = [ ... ]
            pattern = r"(const collections = \[\s*)([^\]]+)(\s*\];)"
            
            def add_collection(match):
                opening = match.group(1)
                items = match.group(2).rstrip()
                closing = match.group(3)
                
                # Add new collection at the end
                new_items = items + f",\n  '{collection_id}'"
                return opening + new_items + closing
            
            new_content = re.sub(pattern, add_collection, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(file_path, 'w') as f:
                    f.write(new_content)
                log('SUCCESS', f"  ✓ Updated {file_path}")
            else:
                log('WARNING', f"  ⚠ Could not update {file_path} (pattern not found)")
        
        except Exception as e:
            log('ERROR', f"  ✗ Failed to update {file_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate a new photography collection for the portfolio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 scripts/generate-collection.py assets/images/gallery/my-collection
  python3 scripts/generate-collection.py assets/images/gallery/japan-2025
        """
    )
    
    parser.add_argument(
        'collection_path',
        help='Path to the new collection folder (must contain full-res/ with JPGs)'
    )
    
    args = parser.parse_args()
    
    # Validate
    if not validate_collection_folder(args.collection_path):
        sys.exit(1)
    
    # Extract collection ID from path
    collection_id = Path(args.collection_path).name
    
    print("\n" + "="*60)
    print(f"GENERATING COLLECTION: {collection_id}")
    print("="*60 + "\n")
    
    # Step 1: Generate thumbnails
    print("\n[STEP 1] Generating Thumbnails")
    print("-" * 60)
    generate_thumbnails(args.collection_path)
    
    # Step 2: Generate metadata
    print("\n[STEP 2] Creating Metadata")
    print("-" * 60)
    generate_metadata(args.collection_path, collection_id)
    
    # Step 3: Update JS configs
    print("\n[STEP 3] Updating Configuration Files")
    print("-" * 60)
    update_javascript_configs(collection_id)
    
    # Summary
    print("\n" + "="*60)
    print("✓ COLLECTION GENERATION COMPLETE!")
    print("="*60)
    print(f"\nYour new collection '{collection_id}' is ready!\n")
    print("Next steps:")
    print("  1. Review and edit metadata.json")
    print("  2. Add specific tags to each image")
    print("  3. Update displayCategory if needed")
    print("  4. git add assets/images/gallery/{}/".format(collection_id))
    print("  5. git commit -m 'Add {} collection'".format(collection_id))
    print("  6. git push origin main")
    print("\nYour homepage will auto-update with the new collection!\n")

if __name__ == '__main__':
    main()
