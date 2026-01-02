# Adding New Collections to Your Portfolio

This guide explains how to add a new photography collection to your portfolio using the automated `scripts/generate-collection.py` script with **Perplexity AI** vision analysis for metadata generation.

## Quick Start (3 Steps)

### Step 1: Create Your Collection Folder

```bash
# Create the collection folder structure
mkdir -p assets/images/gallery/your-collection-name/{full-res,thumbnails}
```

Replace `your-collection-name` with your collection ID (e.g., `iceland-2025`, `africa-safari-2024`).

Use **lowercase with hyphens** (not spaces or underscores).

### Step 2: Add Your Images

Copy your original JPG files to the `full-res` folder:

```bash
cp /path/to/your/photos/*.jpg assets/images/gallery/your-collection-name/full-res/
```

**Filename tip:** Use clear, descriptive names. The script will parse them:
- `Sunrise Over Reykjavik.jpg` → Title: "Sunrise Over Reykjavik"
- `Blue Ice Cave - Vatnajokull.jpg` → Title: "Blue Ice Cave"

Perplexity will then **analyze the actual image** and generate intelligent descriptions and tags.

### Step 3: Set Your API Key and Run the Script

```bash
# Set your Perplexity API key (one-time per session)
export PERPLEXITY_API_KEY='pplx-...'

# Run the script from project root
python3 scripts/generate-collection.py assets/images/gallery/your-collection-name
```

The script will:
1. ✅ Generate thumbnails (400px width, optimized for web)
2. ✅ **Analyze each image with Perplexity AI** to generate intelligent descriptions and tags
3. ✅ Create metadata.json with descriptions, tags, pricing
4. ✅ Update JavaScript configuration files automatically
5. ✅ Smart featured image selection (first, every 3rd, last)

---

## What the Script Does

### 1. Thumbnail Generation

- Converts full-res images (often 3000+px) to 400px width thumbnails
- Maintains aspect ratio
- JPEG quality: 85 (balances file size and visual quality)
- Saves in `thumbnails/` folder
- Skips images that already have thumbnails (for updates)

**Output example:**
```
full-res/
├── Sunrise Over Reykjavik.jpg       (3000x2000, 8MB)

thumbnails/ (created by script)
├── Sunrise Over Reykjavik.jpg       (400x267, 45KB)
```

### 2. AI-Powered Metadata Generation

The script uses **Perplexity Sonar API** to analyze each image and generate:

**Collection-level info (you provide via prompts):**
- Title (e.g., "Iceland 2025")
- Location (e.g., "Iceland, Reykjavik, South Coast")
- Date (e.g., "2025")
- Description (e.g., "A winter journey through Iceland's volcanic landscapes...")

**Per-image info (Perplexity AI generates):**
```json
{
  "id": "sunrise-over-reykjavik",
  "title": "Sunrise Over Reykjavik",
  "filename": "Sunrise Over Reykjavik.jpg",
  "description": "A dramatic sunrise illuminates Reykjavik's colorful rooftops, bathing the city in golden light. The interplay of shadows and highlights creates visual depth across the urban landscape.",
  "location": "Reykjavik, Iceland",
  "tags": ["travel", "landscape", "sunrise", "iceland", "city", "golden-hour", "architecture"],
  "printSizes": [
    {"size": "8x10", "price": 50},
    {"size": "11x14", "price": 85},
    {"size": "16x20", "price": 140},
    {"size": "20x30", "price": 235}
  ],
  "featured": true,
  "printAvailable": true
}
```

### How Perplexity AI Generates Metadata

Perplexity:
1. **Views your actual image** (not just the filename)
2. **Considers collection context** (location, date, title, description)
3. **Analyzes composition** (lighting, focus, depth, mood, subject)
4. **Identifies visual elements** (landscapes, people, architecture, weather, etc.)
5. **Generates buyer-friendly descriptions** (appeals to print customers)
6. **Selects relevant tags** (from curated photography vocabulary)

**Example: What Perplexity Sees**

**Your input:**
- File: `Sunrise Over Reykjavik.jpg`
- Collection: Iceland 2025, Winter Photography
- Actual image: Golden light hitting colorful houses at dawn

**Perplexity generates:**
- **Description**: "A dramatic sunrise illuminates Reykjavik's iconic colorful houses, bathing the landscape in golden light. This moment captures the magic of Iceland's blue hour."
- **Tags**: `["travel", "landscape", "sunrise", "iceland", "city", "golden-hour", "winter", "architecture"]`
- **Featured**: True (smart algorithm selected for homepage)

### Smart Featured Image Selection

- **First image**: `featured: true`
- **Every 3rd image**: `featured: true`
- **Last image**: `featured: true`
- **Others**: `featured: false`

**Example:** 12-image collection → 5 featured images on homepage

You can customize this in metadata.json afterward!

### 3. Automatic JavaScript Updates

For **new collections only**, the script automatically:
- Adds collection ID to `assets/js/gallery-loader.js`
- Adds collection ID to `assets/js/browse-loader.js`

**No manual edits needed!**

---

## Setup: Getting Your Perplexity API Key

### Prerequisites

1. **Perplexity Account** - Sign up at [perplexity.ai](https://perplexity.ai)
2. **API Key** - Create one in your [API settings](https://www.perplexity.ai/settings/api)
3. **Python dependencies** - Install required packages:

```bash
pip install Pillow requests
```

### Set Your API Key

**Option A: One-time (current session only)**
```bash
export PERPLEXITY_API_KEY='pplx-...'
python3 scripts/generate-collection.py assets/images/gallery/my-collection
```

**Option B: Persistent (add to ~/.bashrc or ~/.zshrc)**
```bash
echo "export PERPLEXITY_API_KEY='pplx-...'" >> ~/.bashrc
source ~/.bashrc
```

**Option C: Create .env file (if you set one up)**
```bash
# Create .env in project root
echo "PERPLEXITY_API_KEY=pplx-..." > .env

# Then the script can read it
```

### Get Your Perplexity API Key

1. Go to [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Click "Create API Key"
3. Copy the key (looks like: `pplx-xxxxxxxxxxxxxxxxxxxxx`)
4. Use in scripts above

**Cost:** Perplexity is pay-as-you-go. Analyzing one image costs ~$0.01-0.02. A 12-image collection costs ~$0.15.

---

## Example Workflow

```bash
# 1. Create folder structure
mkdir -p assets/images/gallery/iceland-2025/{full-res,thumbnails}

# 2. Copy your images
cp ~/Pictures/Iceland/*.jpg assets/images/gallery/iceland-2025/full-res/

# 3. Verify images are there
ls assets/images/gallery/iceland-2025/full-res/ | wc -l
# Output: 12 (you have 12 images)

# 4. Set API key (once per session)
export PERPLEXITY_API_KEY='pplx-...'
echo $PERPLEXITY_API_KEY  # Verify it's set

# 5. Run the script
python3 scripts/generate-collection.py assets/images/gallery/iceland-2025

# 6. Script prompts you for collection info:
# Collection Title (e.g., 'Iceland 2025'): Iceland 2025
# Location(s): Iceland, Reykjavik, South Coast, Jokulsarlon
# Date/Year: 2025
# Collection Description: A winter journey through Iceland's volcanic landscapes and geothermal wonders...

# 7. Perplexity analyzes all your images (takes ~1 minute for 12 images):
# [STEP 1] Generating Thumbnails
# ✓ Thumbnail generation complete!
#
# [STEP 2] Creating Metadata (with Perplexity AI)
# Analyzing image 1/12... Generated: 7 tags, description created
# Analyzing image 2/12... Generated: 8 tags, description created
# ... (processes all 12 images)
#
# [STEP 3] Updating Configuration Files
# ✓ Updated assets/js/gallery-loader.js
# ✓ Updated assets/js/browse-loader.js

# 8. Script completes and prints summary:
# ✓ COLLECTION PROCESSING COMPLETE!
# Collection 'iceland-2025' is ready!
# Next steps:
#   1. Review metadata.json (Perplexity made intelligent guesses)
#   2. Customize tags and descriptions as needed
#   3. Update displayCategory if needed
#   4. git add assets/images/gallery/iceland-2025/
#   5. git commit -m 'Add Iceland 2025 collection'
#   git push origin main

# 9. Review the generated metadata (usually excellent!)
cat assets/images/gallery/iceland-2025/metadata.json

# 10. Optional: Customize descriptions, tags, or featured selection
vim assets/images/gallery/iceland-2025/metadata.json

# 11. Commit and push
git add assets/images/gallery/iceland-2025/
git commit -m 'Add Iceland 2025 collection with Perplexity-generated metadata'
git push origin main

# 12. Site updates automatically!
# Cloudflare deploys in ~30 seconds
# New collection appears on:
# - Homepage portfolio page
# - Browse by tag page
# - Collection page: /collection.html?id=iceland-2025
```

---

## After Running the Script

### Review (Recommended, 5-10 minutes)

**Most of the time, Perplexity's suggestions are excellent and ready to use!**

But it's good to check:

1. **Check descriptions**: Do they accurately describe the image? Are they buyer-friendly?
   ```json
   "description": "A dramatic sunrise illuminates..."
   ```

2. **Check tags**: Are they relevant to the image?
   ```json
   "tags": ["travel", "landscape", "sunrise", "iceland", "city"]
   ```

3. **Check featured selection**: Does Perplexity selected good homepage images?
   ```json
   "featured": true  // Good for homepage
   "featured": false // Hidden from homepage
   ```

4. **Check displayCategory**: Update if needed
   ```json
   "displayCategory": "Landscape & Nature"  // or "Travel & Adventure"
   ```

### Customize (Optional)

If you want to tweak metadata:

```json
{
  "title": "Your custom title",
  "description": "Your custom description that appeals to print buyers",
  "tags": ["custom", "tags", "here"],
  "featured": true,  // Change to feature/unfeature
  "printSizes": [
    {"size": "8x10", "price": 50},  // Adjust prices if needed
    {"size": "11x14", "price": 85}
  ]
}
```

### Deploy

```bash
git add assets/images/gallery/iceland-2025/
git commit -m 'Add Iceland 2025 collection'
git push origin main

# Cloudflare auto-deploys in ~30 seconds
# Your new collection appears on homepage!
```

---

## Updating Existing Collections (Adding New Images)

### Workflow for Adding Images to Existing Collection

The script is **smart about updates**. If you run it on a collection that already has metadata.json, it will:

1. Detect new images (by file hash)
2. Generate thumbnails for new images only
3. Analyze new images with Perplexity
4. **Merge with existing metadata** (don't overwrite)
5. Recalculate featured images

**Example:**

```bash
# You already have england-2024 with 10 images
# You just shot 5 more images in the Cotswolds

# 1. Copy new images
cp ~/Pictures/Cotswolds/*.jpg assets/images/gallery/england-2024/full-res/

# 2. Run the script again
export PERPLEXITY_API_KEY='pplx-...'
python3 scripts/generate-collection.py assets/images/gallery/england-2024

# Script detects existing metadata.json and enters MERGE MODE:
# [DETECTED] Existing collection
# Found 5 new image(s) out of 15 total
# Analyzing new images only...
#
# [UPDATED] Merged 5 new images with existing 10 images
# Total images now: 15
# Featured images: 5

# 3. Commit
git add assets/images/gallery/england-2024/
git commit -m 'Update England 2024 collection with new Cotswolds images'
git push origin main
```

---

## Available Tags

Perplexity selects from this curated vocabulary:

`travel` `landscape` `nature` `cherry-blossom` `japan` `castle` `spring` `temple` `garden` `city` `park` `evening` `lanterns` `portrait` `street` `night` `magical` `peaceful` `architecture` `modern` `urban` `culture` `history` `samurai` `gate` `spiritual` `dramatic` `desert` `wildlife` `mountains` `panoramic` `featured` `astro` `city-lights` `historical` `seasonal` `weather` `western` `geology` `rock-formations` `rodeo` `celebration` `festive` `holiday` `christmas` `people` `action` `sports` `alps` `hiking` `countryside` `europe` `austria` `germany` `color` `texture` `tree` `water` `waterfall` `sunrise` `sunset` `moon` `stars` `milky-way` `aurora`

**Want to add custom tags?** You can manually edit metadata.json and add any tag you want!

---

## Troubleshooting

### "PERPLEXITY_API_KEY environment variable not set"

Set your API key:
```bash
export PERPLEXITY_API_KEY='pplx-your-actual-key-here'
echo $PERPLEXITY_API_KEY  # Verify it's set
```

### "ModuleNotFoundError: No module named 'requests'"

Install the required package:
```bash
pip install requests
# or
pip install requests Pillow
```

### "Collection folder does not exist"

Make sure the path is correct:
```bash
ls -la assets/images/gallery/your-collection-name/

# Should show:
# total 1234
# drwxr-xr-x  5 user  staff   160 Jan  2 02:40 .
# drwxr-xr-x  4 user  staff   128 Jan  2 02:30 ..
# drwxr-xr-x  2 user  staff  1234 Jan  2 02:40 full-res
# drwxr-xr-x  2 user  staff    64 Jan  2 02:40 thumbnails
```

### "No JPG images found in full-res"

Check that images are in the `full-res` folder:
```bash
ls assets/images/gallery/your-collection-name/full-res/

# Should show your JPG files:
# Image1.jpg
# Image2.jpg
# ...
```

Make sure filenames end in `.jpg`, `.JPG`, or `.jpeg`

### "HTTP 401: Unauthorized" (API error)

Your API key is invalid or expired:
```bash
# Check your key
echo $PERPLEXITY_API_KEY

# Get a new one from:
# https://www.perplexity.ai/settings/api

# Set it again
export PERPLEXITY_API_KEY='pplx-new-key-here'
```

### "Perplexity API rate limited"

You've hit the API rate limit. Wait a minute and try again:
```bash
sleep 60
python3 scripts/generate-collection.py assets/images/gallery/your-collection
```

Or split your collection into smaller batches:
```bash
# Process first half
cd assets/images/gallery/your-collection/full-res
ls | head -n 6 | xargs -I {} mv {} ../processing/

# Run script
cd ../../..
python3 scripts/generate-collection.py assets/images/gallery/your-collection

# Move remaining and repeat
```

### "Could not parse Perplexity response"

Occasionally Perplexity's response format differs. The script includes fallbacks, but if this happens frequently:

1. Check your internet connection
2. Try again in a few minutes
3. Open a GitHub issue with details

### JavaScript files didn't update automatically

The script tries to find and update `assets/js/gallery-loader.js` and `assets/js/browse-loader.js`. If it fails:

**Manually add to `assets/js/gallery-loader.js`:**
```javascript
const collections = [
  'big-bend-2025',
  'japan-2025',
  'your-new-collection',  // ← Add here
];
```

**Manually add to `assets/js/browse-loader.js`:**
```javascript
const collections = [
  'big-bend-2025',
  'japan-2025',
  'your-new-collection',  // ← Add here
];
```

---

## Performance & Costs

### Processing Speed
- **Per image**: 5-10 seconds (Perplexity analyzes and generates metadata)
- **12-image collection**: ~2-3 minutes total
- **Thumbnail generation**: Instant (Pillow/Python)
- **JavaScript updates**: Instant
- **Total script time**: ~3-4 minutes per collection

### API Costs
- **Per image analyzed**: ~$0.01-0.02 (Perplexity Sonar API)
- **12-image collection**: ~$0.15-0.25
- **Very affordable** for professional-quality metadata

### Image Sizes
- Full-res: 3-8MB (your original photos)
- Thumbnail: 40-80KB (generated, compressed)
- metadata.json: 3-5KB (tiny)

### Homepage Performance
- 6 collections × 4 featured images = 24 thumbnails
- Total payload: ~1-2MB (uncompressed)
- Load time: <1 second on broadband
- **Cloudflare caches everything** for ultra-fast repeats

---

## Scaling to Many Collections

This workflow scales beautifully:
- **5 collections**: No performance issues
- **20 collections**: Still very fast
- **50+ collections**: Consider lazy-loading for homepage (future enhancement)

The combination of **AI metadata + flat-file structure + Cloudflare caching** is perfect for a growing portfolio!

---

## Next Time You Add a Collection

Every time you add a new collection, just run:

```bash
# Step 1: Create folder
mkdir -p assets/images/gallery/new-collection/{full-res,thumbnails}

# Step 2: Copy images
cp ~/Pictures/photos/*.jpg assets/images/gallery/new-collection/full-res/

# Step 3: Run (if API key already set from earlier)
python3 scripts/generate-collection.py assets/images/gallery/new-collection

# Or set API key again (safe to repeat):
export PERPLEXITY_API_KEY='pplx-...'
python3 scripts/generate-collection.py assets/images/gallery/new-collection

# Step 4: Review metadata.json (usually perfect!)
# Step 5: git add, commit, push

# Done! Homepage automatically updates!
```

**Zero friction. Zero manual configuration. Fully scalable.** 🚀

---

## Questions?

Refer to:
- **Script help**: `python3 scripts/generate-collection.py --help`
- **Script source**: Check `scripts/generate-collection.py` for detailed comments
- **Perplexity Docs**: [https://docs.perplexity.ai](https://docs.perplexity.ai)
- **Project Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **GitHub Issues**: [https://github.com/mmimms/PhotoSite/issues](https://github.com/mmimms/PhotoSite/issues)
