# Adding New Collections to Your Portfolio

This guide explains how to add a new photography collection to your portfolio using the automated `generate-collection.py` script.

## Quick Start (3 Steps)

### Step 1: Create Your Collection Folder

```bash
# Create the collection folder structure
mkdir -p assets/images/gallery/your-collection-name/full-res
mkdir -p assets/images/gallery/your-collection-name/thumbnails
```

Replace `your-collection-name` with your collection ID (e.g., `iceland-2025`, `africa-safari-2024`).

### Step 2: Add Your Images

Copy your original JPG files to the `full-res` folder:

```bash
cp /path/to/your/photos/*.jpg assets/images/gallery/your-collection-name/full-res/
```

**Important:** Name your files clearly:
- `Sunrise Over Reykjavik - Screen.jpg`
- `Blue Ice Cave - Screen.jpg`
- `Geothermal Hot Spring - Screen.jpg`

The script will extract titles and descriptions from filenames, so good naming = better metadata.

### Step 3: Run the Script

```bash
python3 scripts/generate-collection.py assets/images/gallery/your-collection-name
```

The script will:
1. Generate thumbnails (400px width, optimized)
2. Create metadata.json with AI-assisted metadata
3. Update JavaScript configuration files
4. Smart featured image selection (first, every 3rd, last)

---

## What the Script Does

### 1. Thumbnail Generation

- Converts full-res images (often 3000+px) to 400px width thumbnails
- Maintains aspect ratio
- JPEG quality: 85 (balances file size and visual quality)
- Saves in `thumbnails/` folder

### 2. Metadata Generation

The script creates `metadata.json` with collection-level and per-image info.
Collections have smart featured image selection (first, every 3rd, last image).

### 3. JavaScript Configuration

Automatically adds your collection to gallery-loader.js and browse-loader.js files.
No manual edits needed!

---

## Example Workflow

```bash
# 1. Create folder structure
mkdir -p assets/images/gallery/iceland-2025/full-res

# 2. Copy your images
cp ~/Pictures/Iceland/*.jpg assets/images/gallery/iceland-2025/full-res/

# 3. Run the script
python3 scripts/generate-collection.py assets/images/gallery/iceland-2025

# 4. Script prompts you for collection info:
# Collection Title: Iceland 2025
# Location(s): Iceland
# Date/Year: 2025
# Collection Description: A visual journey through Iceland...

# 5. Review the generated metadata.json
vim assets/images/gallery/iceland-2025/metadata.json

# 6. Add and commit
git add assets/images/gallery/iceland-2025/
git commit -m "Add Iceland 2025 collection"
git push origin main
```

---

## After Running the Script

### Required: Update metadata.json

The script generates metadata, but you should:

1. **Add specific tags** to each image:
   ```json
   "tags": ["travel", "landscape", "volcanic", "geothermal"]
   ```

2. **Update displayCategory** (in collection object):
   ```json
   "displayCategory": "Landscape & Nature"
   ```

3. **Edit descriptions** (optional but recommended):
   ```json
   "description": "The geothermal hot springs of Iceland, photographed during summer solstice."
   ```

### Deploy

```bash
git add assets/images/gallery/iceland-2025/
git commit -m "Add Iceland 2025 collection"
git push origin main
```

Cloudflare auto-deploys in ~30 seconds!

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'PIL'"

Install Pillow:
```bash
pip install Pillow
```

### "Collection folder does not exist"

Make sure the path is correct:
```bash
ls assets/images/gallery/your-collection-name/
```

### JavaScript files didn't update automatically

Manually add to `assets/js/gallery-loader.js` and `assets/js/browse-loader.js`:
```javascript
const collections = [
  'big-bend-2025',
  'japan-2025',
  'your-new-collection',  // Add here
];
```

---

## Performance

- Full-res image: 8-15MB
- Thumbnail: 40-80KB
- Homepage with 5 collections: ~1-2MB total, <1s load time

Cloudflare caches and optimizes everything!
