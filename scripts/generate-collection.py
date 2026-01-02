#!/usr/bin/env python3
"""
Generate Collection Script
Automates the process of adding a new photography collection to the portfolio.
Also supports adding new images to existing collections (merge mode).

Usage:
    python3 scripts/generate-collection.py <collection-folder-path>

Example:
    python3 scripts/generate-collection.py assets/images/gallery/my-new-collection
    python3 scripts/generate-collection.py assets/images/gallery/japan-2025  (with new images)

Expected folder structure:
    my-collection/
    ├── full-res/           (required: your JPGs - can add new ones)
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── thumbnails/         (will be created/populated)
    └── metadata.json       (optional: will be created or updated)

This script will:
    1. Detect if collection is new or existing
    2. Generate thumbnails (new images only if updating)
    3. Create or update metadata.json with AI-assisted descriptions and tags
    4. Update collections lists in JavaScript files (new collections only)
    5. Generate metadata with smart featured selection

Requirements:
    pip install Pillow requests
    
Environment Variables:
    PERPLEXITY_API_KEY - Your Perplexity API key from Settings > API
"""

import os
import sys
import json
import argparse
import hashlib
from pathlib import Path
from PIL import Image
import re
import base64
import requests

# Constants
THUMBNAIL_WIDTH = 400
THUMBNAIL_QUALITY = 85

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

def get_image_hash(image_path):
    """Get SHA256 hash of image file for deduplication."""
    sha256_hash = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

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

def get_image_files(collection_path):
    """Get sorted list of image files in collection."""
    full_res_path = Path(collection_path) / 'full-res'
    return sorted(full_res_path.glob('*.jpg')) + sorted(full_res_path.glob('*.JPG')) + sorted(full_res_path.glob('*.jpeg'))

def check_if_existing_collection(collection_path):
    """Check if collection already has metadata.json."""
    metadata_path = Path(collection_path) / 'metadata.json'
    return metadata_path.exists()

def get_existing_image_hashes(collection_path):
    """Get set of image hashes already in metadata.json.
    
    Uses file hashing to detect duplicates, even if filenames differ
    (e.g., image - Screen.jpg vs image - Matte.jpg)
    """
    metadata_path = Path(collection_path) / 'metadata.json'
    
    if not metadata_path.exists():
        return {}
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Build map of filename -> hash for images in metadata
        # We'll compute hashes for actual files and compare
        existing_hashes = {}
        for img in metadata.get('images', []):
            existing_hashes[img['filename']] = None  # Hash will be computed on demand
        
        return existing_hashes
    except Exception as e:
        log('WARNING', f"Could not read existing metadata.json: {str(e)}")
        return {}

def find_new_images(collection_path):
    """Find new images not yet in metadata.json by comparing file hashes.
    
    This is more reliable than filename comparison because it handles:
    - Different naming schemes (Screen vs Matte versions)
    - Renamed files
    - Different file formats of the same image
    """
    all_images = get_image_files(collection_path)
    
    # Build hash map of existing images in metadata
    metadata_path = Path(collection_path) / 'metadata.json'
    existing_hashes = set()
    
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Pre-compute hashes of referenced files
            full_res_path = Path(collection_path) / 'full-res'
            for img in metadata.get('images', []):
                img_file = full_res_path / img['filename']
                if img_file.exists():
                    file_hash = get_image_hash(img_file)
                    existing_hashes.add(file_hash)
        except Exception as e:
            log('WARNING', f"Could not compute existing image hashes: {str(e)}")
    
    # Find new images (not in existing_hashes)
    new_images = []
    for image_file in all_images:
        file_hash = get_image_hash(image_file)
        if file_hash not in existing_hashes:
            new_images.append(image_file)
    
    return new_images, len(all_images)

def generate_thumbnails(collection_path, specific_images=None):
    """Generate thumbnail images from full-res originals.
    
    If specific_images is provided, only generate for those.
    Otherwise, generate for all images (skip existing if thumbnails exist).
    """
    collection_path = Path(collection_path)
    full_res_path = collection_path / 'full-res'
    thumbnails_path = collection_path / 'thumbnails'
    
    # Create thumbnails folder if it doesn't exist
    thumbnails_path.mkdir(exist_ok=True)
    
    if specific_images:
        image_files = specific_images
        log('INFO', f"Generating thumbnails for {len(image_files)} new images...")
    else:
        image_files = get_image_files(collection_path)
        log('INFO', f"Generating thumbnails for {len(image_files)} images...")
    
    for image_file in image_files:
        try:
            # Skip if thumbnail already exists
            thumb_path = thumbnails_path / image_file.name
            if thumb_path.exists() and specific_images is None:
                log('SUCCESS', f"  ✓ {image_file.name} (thumbnail already exists)")
                continue
            
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
    
    # Remove " - Screen" or " - Matte" suffix if present
    name = re.sub(r'\s*-\s*(Screen|Matte)\s*$', '', name)
    
    # Split on " - " if it exists
    parts = name.split(' - ', 1)
    
    title = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else None
    
    return title, description

def generate_image_description_and_tags(api_key, image_path, title, collection_info):
    """Use Perplexity Sonar to generate intelligent descriptions and tags for an image."""
    try:
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')
        
        # Determine image type
        image_ext = image_path.suffix.lower()
        if image_ext in ['.jpg', '.jpeg']:
            media_type = 'image/jpeg'
        elif image_ext == '.png':
            media_type = 'image/png'
        else:
            media_type = 'image/jpeg'
        
        # Create prompt for Perplexity
        prompt = f"""You are a photography metadata expert. Analyze this photograph and provide metadata for a photography portfolio.

Collection Context:
- Title: {collection_info['title']}
- Location: {collection_info['location']}
- Date: {collection_info['date']}
- Description: {collection_info['description']}

Image Title: {title}

Provide your response in this exact JSON format (no additional text):
{{
  "description": "A compelling 1-2 sentence description of the photograph that would appeal to someone considering purchasing a print. Focus on what makes this image special, the mood, and the visual elements.",
  "tags": ["tag1", "tag2", "tag3", ...]
}}

For tags, choose from this list where relevant: travel, landscape, nature, cherry-blossom, japan, castle, spring, temple, garden, city, park, evening, lanterns, portrait, street, night, magical, peaceful, architecture, modern, urban, culture, history, samurai, gate, spiritual, dramatic, desert, wildlife, mountains, panoramic, featured, astro, city-lights, historical, seasonal, weather, western, geology, rock-formations, rodeo, celebration, festive, holiday, christmas, people, action, sports, alps, hiking, countryside, europe, austria, germany, color, texture, tree, water, waterfall, sunrise, sunset, moon, stars, milky-way, aurora

Make sure tags are relevant to this specific image and the collection context."""
        
        # Call Perplexity API with vision (Sonar model)
        response = requests.post(
            'https://api.perplexity.ai/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'sonar-pro',
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:{media_type};base64,{image_data}'
                                }
                            },
                            {
                                'type': 'text',
                                'text': prompt
                            }
                        ]
                    }
                ],
                'max_tokens': 500
            }
        )
        
        if response.status_code != 200:
            log('WARNING', f"  Perplexity API error ({response.status_code}): {response.text}")
            return None, None
        
        # Parse response
        response_data = response.json()
        response_text = response_data['choices'][0]['message']['content']
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            metadata = json.loads(json_match.group())
            return metadata['description'], metadata['tags']
        else:
            log('WARNING', f"  Could not parse Perplexity response for {image_path.name}")
            return None, None
    
    except Exception as e:
        log('WARNING', f"  Failed to generate metadata for {image_path.name}: {str(e)}")
        return None, None

def load_existing_metadata(collection_path):
    """Load existing metadata.json if it exists."""
    metadata_path = Path(collection_path) / 'metadata.json'
    
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            log('WARNING', f"Could not load existing metadata: {str(e)}")
            return None
    
    return None

def generate_metadata(collection_path, collection_id, api_key, new_images_only=False):
    """Generate metadata.json for the collection.
    
    If new_images_only=True, only generate for new images and merge with existing.
    Otherwise, create fresh metadata for all images.
    """
    collection_path = Path(collection_path)
    
    # Check if this is an update to existing collection
    existing_metadata = load_existing_metadata(collection_path) if new_images_only else None
    
    if new_images_only and existing_metadata:
        log('INFO', "Found existing metadata.json - entering MERGE mode")
        log('INFO', "New images will be added to existing collection")
        
        # Get only new images (by hash)
        new_images, total_images = find_new_images(collection_path)
        
        if not new_images:
            log('WARNING', f"No new images found! All {total_images} images already in metadata.")
            return
        
        log('INFO', f"Found {len(new_images)} new image(s) out of {total_images} total")
        
        # Use existing collection info
        collection_info = {
            'title': existing_metadata['collection']['title'],
            'location': existing_metadata['collection']['location'],
            'date': existing_metadata['collection']['date'],
            'description': existing_metadata['collection']['description']
        }
        
        print("\n" + "="*60)
        print(f"UPDATING COLLECTION: {collection_id}")
        print("="*60)
        print(f"Existing title: {collection_info['title']}")
        print(f"Existing location: {collection_info['location']}")
        print(f"New images to process: {len(new_images)}")
        print("="*60 + "\n")
        
        # Generate metadata only for new images
        new_images_data = []
        for new_image in new_images:
            title, filename_desc = extract_metadata_from_filename(new_image.name)
            log('INFO', f"Analyzing {new_image.name}...")
            
            description, tags = generate_image_description_and_tags(
                api_key,
                new_image,
                title,
                collection_info
            )
            
            if not description:
                description = filename_desc or f"A photograph from the {collection_info['title']} collection"
            
            if not tags:
                tags = ["travel"]
            
            log('SUCCESS', f"  Generated: {len(tags)} tags, description created")
            
            image_data = {
                "id": title.lower().replace(' ', '-'),
                "title": title,
                "filename": new_image.name,
                "description": description,
                "location": collection_info['location'],
                "tags": tags,
                "printSizes": [
                    {"size": "8x10", "price": 50},
                    {"size": "11x14", "price": 85},
                    {"size": "16x20", "price": 140},
                    {"size": "20x30", "price": 235}
                ],
                "featured": False,  # Will be recalculated
                "printAvailable": True
            }
            
            new_images_data.append(image_data)
        
        # Merge: keep existing images, add new ones
        all_images_data = existing_metadata['images'] + new_images_data
        
        # Recalculate featured: first + every 3rd + last
        for idx, img in enumerate(all_images_data):
            img['featured'] = (idx == 0) or (idx % 3 == 0) or (idx == len(all_images_data) - 1)
        
        # Update metadata
        updated_metadata = existing_metadata
        updated_metadata['images'] = all_images_data
        updated_metadata['collection']['coverImage'] = all_images_data[0]['filename']
        
        # Save metadata.json
        metadata_path = collection_path / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(updated_metadata, f, indent=2)
        
        log('SUCCESS', f"Updated metadata.json")
        log('INFO', f"  Total images now: {len(all_images_data)}")
        log('INFO', f"  New images added: {len(new_images_data)}")
        log('INFO', f"  Featured images: {sum(1 for img in all_images_data if img['featured'])}")
        
    else:
        # Fresh metadata generation (new collection)
        log('INFO', "Generating fresh metadata.json for new collection")
        
        all_images = get_image_files(collection_path)
        
        # Prompt user for collection info
        print("\n" + "="*60)
        print("COLLECTION INFORMATION")
        print("="*60)
        
        collection_title = input("Collection Title (e.g., 'Japan 2025'): ").strip()
        collection_location = input("Location(s) (e.g., 'Japan, Kyoto'): ").strip()
        collection_date = input("Date/Year (e.g., '2025'): ").strip()
        collection_description = input("Collection Description: ").strip()
        
        collection_info = {
            'title': collection_title,
            'location': collection_location,
            'date': collection_date,
            'description': collection_description
        }
        
        print("\n" + "="*60)
        print("GENERATING IMAGE METADATA")
        print("="*60)
        print(f"Using Perplexity AI to analyze {len(all_images)} images...\n")
        
        images_data = []
        for idx, image_file in enumerate(all_images):
            title, filename_desc = extract_metadata_from_filename(image_file.name)
            
            log('INFO', f"Analyzing {image_file.name}...")
            
            description, tags = generate_image_description_and_tags(
                api_key,
                image_file,
                title,
                collection_info
            )
            
            if not description:
                description = filename_desc or f"A photograph from the {collection_title} collection"
            
            if not tags:
                tags = ["travel"]
            
            log('SUCCESS', f"  Generated: {len(tags)} tags, description created")
            
            # Auto-feature: first image + every 3rd image + last image
            is_featured = (idx == 0) or (idx % 3 == 0) or (idx == len(all_images) - 1)
            
            image_data = {
                "id": title.lower().replace(' ', '-'),
                "title": title,
                "filename": image_file.name,
                "description": description,
                "location": collection_location,
                "tags": tags,
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
                "displayCategory": "Travel & Adventure",
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
        description='Generate a new photography collection or add images to existing collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 scripts/generate-collection.py assets/images/gallery/my-collection
  python3 scripts/generate-collection.py assets/images/gallery/japan-2025  (with new images)
        """
    )
    
    parser.add_argument(
        'collection_path',
        help='Path to the collection folder (must contain full-res/ with JPGs)'
    )
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        log('ERROR', "PERPLEXITY_API_KEY environment variable not set")
        log('INFO', "Get your API key from: https://www.perplexity.ai/settings/api")
        log('INFO', "Then set it with: export PERPLEXITY_API_KEY='pplx-...'")
        sys.exit(1)
    
    # Validate
    if not validate_collection_folder(args.collection_path):
        sys.exit(1)
    
    # Extract collection ID from path
    collection_id = Path(args.collection_path).name
    
    # Check if this is an existing collection
    is_existing = check_if_existing_collection(args.collection_path)
    
    print("\n" + "="*60)
    if is_existing:
        print(f"DETECTED: Existing collection")
    else:
        print(f"DETECTED: New collection")
    print(f"Collection ID: {collection_id}")
    print("="*60 + "\n")
    
    # Step 1: Generate thumbnails
    print("\n[STEP 1] Generating Thumbnails")
    print("-" * 60)
    if is_existing:
        new_images, total = find_new_images(args.collection_path)
        if new_images:
            generate_thumbnails(args.collection_path, specific_images=new_images)
        else:
            log('INFO', f"All {total} images already have thumbnails. Skipping.")
    else:
        generate_thumbnails(args.collection_path)
    
    # Step 2: Generate metadata
    print("\n[STEP 2] Creating Metadata (with Perplexity AI)")
    print("-" * 60)
    generate_metadata(args.collection_path, collection_id, api_key, new_images_only=is_existing)
    
    # Step 3: Update JS configs (only for new collections)
    if not is_existing:
        print("\n[STEP 3] Updating Configuration Files")
        print("-" * 60)
        update_javascript_configs(collection_id)
    
    # Summary
    print("\n" + "="*60)
    print("✓ COLLECTION PROCESSING COMPLETE!")
    print("="*60)
    print(f"\nCollection '{collection_id}' is ready!\n")
    print("Next steps:")
    print("  1. Review metadata.json (Perplexity made intelligent guesses)")
    print("  2. Customize tags and descriptions as needed")
    if not is_existing:
        print("  3. Update displayCategory if needed")
        print("  4. git add assets/images/gallery/{}/".format(collection_id))
        print("  5. git commit -m 'Add {} collection'".format(collection_id))
    else:
        print("  3. git add assets/images/gallery/{}/".format(collection_id))
        print("  4. git commit -m 'Update {} collection with new images'".format(collection_id))
    print("  git push origin main")
    print("\nYour homepage will auto-update!\n")

if __name__ == '__main__':
    main()
