#!/usr/bin/env python3
"""
PhotoSite Thumbnail Generator
Converts full-resolution JPGs to optimized thumbnails for web galleries.

USAGE:
  python generate-thumbnails.py

REQUIREMENTS:
  pip install Pillow

WHAT IT DOES:
  - Scans all gallery folders for full-res images
  - Creates 800px wide thumbnails (maintains aspect ratio)
  - Optimizes for web (quality 85, progressive JPEG)
  - Preserves EXIF metadata
  - Skips already-processed images
"""

import os
from pathlib import Path
from PIL import Image
import PIL.ExifTags

# ============================================
# CONFIGURATION
# ============================================

# Base directory (run script from PhotoSite root)
BASE_DIR = Path(__file__).parent
GALLERY_DIR = BASE_DIR / "assets" / "images" / "gallery"

# Thumbnail settings
THUMBNAIL_WIDTH = 800  # Max width in pixels
THUMBNAIL_QUALITY = 85  # JPEG quality (1-100)
THUMBNAIL_FORMAT = "JPEG"

# Supported image formats
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.JPG', '.JPEG']

# ============================================
# FUNCTIONS
# ============================================

def create_thumbnail(source_path, dest_path, width=THUMBNAIL_WIDTH):
    """
    Create optimized thumbnail from source image.
    
    Args:
        source_path: Path to full-resolution image
        dest_path: Path where thumbnail should be saved
        width: Maximum width of thumbnail in pixels
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open image and preserve EXIF data
        with Image.open(source_path) as img:
            # Get EXIF data before processing
            exif = img.info.get('exif')
            
            # Calculate new dimensions (maintain aspect ratio)
            aspect_ratio = img.height / img.width
            new_width = width
            new_height = int(width * aspect_ratio)
            
            # Resize with high-quality resampling
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert RGBA to RGB if needed (for JPEG compatibility)
            if img_resized.mode == 'RGBA':
                img_resized = img_resized.convert('RGB')
            
            # Save with optimization
            save_kwargs = {
                'format': THUMBNAIL_FORMAT,
                'quality': THUMBNAIL_QUALITY,
                'optimize': True,
                'progressive': True  # Progressive JPEG for better web loading
            }
            
            # Include EXIF if available
            if exif:
                save_kwargs['exif'] = exif
            
            img_resized.save(dest_path, **save_kwargs)
            
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR processing {source_path.name}: {e}")
        return False


def get_file_size_mb(path):
    """Get file size in megabytes."""
    return path.stat().st_size / (1024 * 1024)


def process_gallery_folder(gallery_path):
    """
    Process all images in a gallery folder.
    
    Args:
        gallery_path: Path object pointing to gallery folder
                      (e.g., assets/images/gallery/big-bend-2025/)
    """
    full_res_dir = gallery_path / "full-res"
    thumbnails_dir = gallery_path / "thumbnails"
    
    # Check if full-res directory exists
    if not full_res_dir.exists():
        print(f"  ⚠️  No full-res folder found in {gallery_path.name}")
        return
    
    # Create thumbnails directory if it doesn't exist
    thumbnails_dir.mkdir(exist_ok=True)
    
    # Find all images in full-res folder
    images = [
        f for f in full_res_dir.iterdir()
        if f.suffix in SUPPORTED_FORMATS
    ]
    
    if not images:
        print(f"  ℹ️  No images found in {gallery_path.name}/full-res/")
        return
    
    print(f"\n📁 Processing: {gallery_path.name}")
    print(f"   Found {len(images)} image(s)")
    
    processed = 0
    skipped = 0
    
    for img_path in images:
        # Determine thumbnail path
        thumb_path = thumbnails_dir / img_path.name
        
        # Skip if thumbnail already exists
        if thumb_path.exists():
            print(f"  ⏭️  Skipping {img_path.name} (thumbnail exists)")
            skipped += 1
            continue
        
        # Create thumbnail
        print(f"  🔄 Creating thumbnail: {img_path.name}")
        
        original_size = get_file_size_mb(img_path)
        success = create_thumbnail(img_path, thumb_path)
        
        if success:
            thumbnail_size = get_file_size_mb(thumb_path)
            compression_ratio = (1 - thumbnail_size / original_size) * 100
            
            print(f"     ✅ {original_size:.2f}MB → {thumbnail_size:.2f}MB "
                  f"({compression_ratio:.0f}% reduction)")
            processed += 1
        else:
            processed += 0
    
    print(f"  ✅ Complete: {processed} created, {skipped} skipped")


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function."""
    print("=" * 60)
    print("PhotoSite Thumbnail Generator")
    print("=" * 60)
    
    # Check if gallery directory exists
    if not GALLERY_DIR.exists():
        print(f"\n❌ ERROR: Gallery directory not found at {GALLERY_DIR}")
        print("   Make sure you're running this script from the PhotoSite root directory.")
        return
    
    # Find all gallery subfolders
    gallery_folders = [
        f for f in GALLERY_DIR.iterdir()
        if f.is_dir()
    ]
    
    if not gallery_folders:
        print(f"\n⚠️  No gallery folders found in {GALLERY_DIR}")
        return
    
    print(f"\nFound {len(gallery_folders)} gallery folder(s):")
    for folder in gallery_folders:
        print(f"  - {folder.name}")
    
    # Process each gallery folder
    total_processed = 0
    for gallery in gallery_folders:
        process_gallery_folder(gallery)
    
    print("\n" + "=" * 60)
    print("✅ Thumbnail generation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review thumbnails in each gallery's thumbnails/ folder")
    print("2. Commit thumbnails to Git (they're small enough)")
    print("3. Consider hosting full-res images on Cloudflare R2/Images")
    print("4. Update your HTML to load from thumbnails/ for gallery grids")


if __name__ == "__main__":
    main()