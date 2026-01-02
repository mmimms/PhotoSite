# Adding New Collections to Your Portfolio

This guide explains how to add a new photography collection to your portfolio using the automated `generate-collection.py` script with AI-assisted metadata generation.

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

**Filename Tip:** Use clear, descriptive names. The script will parse them:
- `Sunrise Over Reykjavik - Screen.jpg` → Title: "Sunrise Over Reykjavik"
- `Blue Ice Cave - Exploration in Vatnajokull - Screen.jpg` → Title: "Blue Ice Cave"

AI will then analyze the actual image and generate intelligent descriptions and tags.

### Step 3: Set Your API Key and Run the Script

```bash
# Set your Anthropic API key (one-time per session)
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'

# Run the script
python3 scripts/generate-collection.py assets/images/gallery/your-collection-name
```

The script will:
1. ✓ Generate thumbnails (400px width, optimized)
2. ✓ **Analyze each image with Claude AI** to generate intelligent descriptions and tags
3. ✓ Create metadata.json with best-effort metadata
4. ✓ Update JavaScript configuration files
5. ✓ Smart featured image selection (first, every 3rd, last)

---

## What the Script Does

### 1. Thumbnail Generation

- Converts full-res images (often 3000+px) to 400px width thumbnails
- Maintains aspect ratio
- JPEG quality: 85 (balances file size and visual quality)
- Saves in `thumbnails/` folder

**Output:**
```
full-res/
├── Sunrise Over Reykjavik - Screen.jpg     (3000x2000, 8MB)
full-res processed by script:
└── thumbnails/
    └── Sunrise Over Reykjavik - Screen.jpg  (400x267, 45KB)
```

### 2. Metadata Generation with AI

The script uses **Claude AI** to analyze each image and generate:

**Collection-level info (you provide via prompts):**
- Title (e.g., "Iceland 2025")
- Location (e.g., "Iceland")
- Date (e.g., "2025")
- Description (e.g., "A visual journey through Iceland's dramatic landscapes...")

**Per-image info (Claude AI generated):**
```json
{
  "id": "sunrise-over-reykjavik",
  "title": "Sunrise Over Reykjavik",
  "filename": "Sunrise Over Reykjavik - Screen.jpg",
  "description": "A dramatic sunrise illuminates Reykjavik's colorful rooftops, bathing the city in golden light. The interplay of shadows and highlights creates depth across the urban landscape.",
  "location": "Reykjavik, Iceland",
  "tags": ["travel", "landscape", "sunrise", "iceland", "city", "golden-hour"],
  "featured": true,
  "printSizes": [
    {"size": "8x10", "price": 50},
    {"size": "11x14", "price": 85},
    {"size": "16x20", "price": 140},
    {"size": "20x30", "price": 235}
  ]
}
```

**How Claude Generates Metadata:**
- Analyzes the actual image (not just the filename)
- Understands composition, mood, lighting, subject matter
- Generates descriptions that would appeal to print buyers
- Selects relevant tags from a curated photography vocabulary
- Takes collection context into account

**Smart Featured Selection:**
- First image: `featured: true`
- Every 3rd image: `featured: true`
- Last image: `featured: true`
- Others: `featured: false`

Example: 12-image collection → 5 featured images on homepage

### 3. JavaScript Configuration

Automatically adds your collection to:
- `assets/js/gallery-loader.js` (homepage display)
- `assets/js/browse-loader.js` (tag-based browsing)

No manual edits needed!

---

## Setup: Getting Your API Key

### Prerequisites

1. **Anthropic Account** - Sign up at [console.anthropic.com](https://console.anthropic.com)
2. **API Key** - Generate one in your account settings
3. **Python dependencies** - Install required packages:

```bash
pip install Pillow anthropic
```

### Set Your API Key

**Option A: One-time (current session only)**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
python3 scripts/generate-collection.py assets/images/gallery/my-collection
```

**Option B: Persistent (add to ~/.bashrc or ~/.zshrc)**
```bash
echo "export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'" >> ~/.bashrc
source ~/.bashrc
```

**Option C: .env file (if you set one up)**
```bash
# Create .env file in project root
echo "ANTHROPIC_API_KEY=sk-ant-your-actual-key-here" > .env
```

---

## Example Workflow

```bash
# 1. Create folder structure
mkdir -p assets/images/gallery/iceland-2025/full-res
mkdir -p assets/images/gallery/iceland-2025/thumbnails

# 2. Copy your images
cp ~/Pictures/Iceland/*.jpg assets/images/gallery/iceland-2025/full-res/

# 3. Set API key
export ANTHROPIC_API_KEY='sk-ant-...'

# 4. Run the script
python3 scripts/generate-collection.py assets/images/gallery/iceland-2025

# 5. Script prompts you for collection info:
# Collection Title: Iceland 2025
# Location(s): Iceland, Reykjavik, South Coast
# Date/Year: 2025
# Collection Description: A winter journey through Iceland's volcanic landscapes and geothermal wonders, captured during the magical blue hour.

# 6. Claude analyzes all your images:
# Analyzing image 1/12... Generated: 6 tags, description created
# Analyzing image 2/12... Generated: 7 tags, description created
# ... (processes all images)

# 7. Review the generated metadata.json
vim assets/images/gallery/iceland-2025/metadata.json

# 8. Optional: Customize descriptions, tags, or featured selection
# Most of the time, Claude's suggestions are excellent and ready to use!

# 9. Add and commit
git add assets/images/gallery/iceland-2025/
git commit -m "Add Iceland 2025 collection with AI-generated metadata"
git push origin main

# 10. Your homepage automatically shows the new collection!
```

---

## After Running the Script

### Review (Recommended, 5-10 minutes)

1. **Check descriptions**: Claude generates smart, buyer-friendly descriptions. Review for accuracy.
2. **Check tags**: Claude selects from a curated photography vocabulary. Verify they match the image.
3. **Check featured**: Smart algorithm selects ~40% of images. Change if you want different ones.
4. **Update displayCategory** if needed:
   ```json
   "displayCategory": "Landscape & Nature"
   ```

### Customize (Optional)

If you want to tweak metadata:

```json
// Edit specific fields
{
  "description": "Your custom description here",
  "tags": ["custom", "tags", "here"],
  "featured": true,  // Change to feature/unfeature an image
  "displayCategory": "Your Custom Category"
}
```

### Deploy

```bash
git add assets/images/gallery/iceland-2025/
git commit -m "Add Iceland 2025 collection"
git push origin main
```

Cloudflare auto-deploys in ~30 seconds. Your new collection appears on:
- **Portfolio page** - Featured images shown
- **Browse page** - All images filterable by tag
- **Collection page** - Full gallery at `/collection.html?id=iceland-2025`

---

## Available Tags

Claude selects from this curated vocabulary:

`travel`, `landscape`, `nature`, `cherry-blossom`, `japan`, `castle`, `spring`, `temple`, `garden`, `city`, `park`, `evening`, `lanterns`, `portrait`, `street`, `night`, `magical`, `peaceful`, `architecture`, `modern`, `urban`, `culture`, `history`, `samurai`, `gate`, `spiritual`, `dramatic`, `desert`, `wildlife`, `mountains`, `panoramic`, `featured`, `astro`, `city-lights`, `historical`, `seasonal`, `weather`, `western`, `geology`, `rock-formations`, `rodeo`, `celebration`, `festive`, `holiday`, `christmas`, `people`, `action`, `sports`, `alps`, `hiking`, `countryside`, `europe`, `austria`, `germany`, `color`, `texture`, `tree`, `water`, `waterfall`, `sunrise`, `sunset`, `moon`, `stars`, `milky-way`, `aurora`

If you need additional tags, you can manually add them to metadata.json!

---

## Troubleshooting

### "ANTHROPIC_API_KEY environment variable not set"

Set your API key:
```bash
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

Or check if it's set:
```bash
echo $ANTHROPIC_API_KEY
```

### "ModuleNotFoundError: No module named 'anthropic'"

Install the required package:
```bash
pip install anthropic
```

### "Collection folder does not exist"

Make sure the path is correct:
```bash
ls -la assets/images/gallery/your-collection-name/
```

Should show:
```
total 1234
drwxr-xr-x  5 user  staff   160 Jan  2 02:40 .
drwxr-xr-x  4 user  staff   128 Jan  2 02:30 ..
drwxr-xr-x  2 user  staff  1234 Jan  2 02:40 full-res
drwxr-xr-x  2 user  staff    64 Jan  2 02:40 thumbnails
```

### "No JPG images found in full-res"

Check that images are in the `full-res` folder:
```bash
ls assets/images/gallery/your-collection-name/full-res/
```

Make sure filenames end in `.jpg`, `.JPG`, or `.jpeg`

### "Could not parse Claude response"

Occasionally Claude's response format differs. The script includes fallbacks, but if this happens frequently, check your API key and internet connection.

### JavaScript files didn't update automatically

The script tries to find and update `assets/js/gallery-loader.js` and `assets/js/browse-loader.js`. If it fails:

1. Manually add to `assets/js/gallery-loader.js`:
   ```javascript
   const collections = [
     'big-bend-2025',
     'japan-2025',
     'your-new-collection',  // ← Add here
   ];
   ```

2. Manually add to `assets/js/browse-loader.js`:
   ```javascript
   const collections = [
     'big-bend-2025',
     'japan-2025',
     'your-new-collection',  // ← Add here
   ];
   ```

---

## How Claude Generates Metadata

### What Claude Analyzes

When you run the script, Claude:

1. **Views your actual image** (not just the filename)
2. **Considers the collection context** (location, date, title, description)
3. **Analyzes composition** (lighting, focus, depth, mood)
4. **Identifies subjects** (landscapes, people, architecture, etc.)
5. **Generates buyer-friendly descriptions** (appeals to print customers)
6. **Selects relevant tags** (from curated photography vocabulary)

### Example: What Claude Sees

**Your input:**
- File: `Sunrise Over Reykjavik - Screen.jpg`
- Collection: Iceland 2025, Winter Photography
- Actual image: Golden light hitting city at sunrise, colorful houses

**Claude generates:**
- **Description**: "A dramatic sunrise illuminates Reykjavik's iconic colorful houses, casting golden light across the snow-dusted landscape. This moment captures the magic of Iceland's blue hour."
- **Tags**: `["travel", "landscape", "sunrise", "iceland", "city", "golden-hour", "winter", "architecture"]`
- **Featured**: True (smart algorithm selected this for homepage)

### Why This Matters

✓ **Better for selling prints** - Descriptions appeal to buyers  
✓ **Consistent quality** - No typos or inconsistencies  
✓ **Intelligent tagging** - Based on actual image content  
✓ **Fast** - Seconds instead of minutes per image  
✓ **Customizable** - You can still edit everything afterward  

---

## Performance & Costs

### Processing Speed
- **Per image**: ~3-5 seconds (Claude analyzes and generates metadata)
- **12-image collection**: ~60 seconds total
- **Thumbnail generation**: Instant (Python/Pillow)
- **Total script time**: ~2-3 minutes per collection

### API Costs
- Claude API is **pay-as-you-go**: ~$0.003 per image analyzed
- **12-image collection**: ~$0.04
- **Very low cost** for professional-quality metadata

### Image Sizes
- Full-res: 8-15MB
- Thumbnail: 40-80KB
- metadata.json: 3-5KB

### Homepage Performance
- 5 collections × 4 featured images = 20 thumbnails
- Total payload: ~1-2MB (uncompressed)
- Load time: <1 second on broadband

Cloudflare caches and optimizes everything, so actual load is much faster.

---

## Scaling to Many Collections

This workflow scales beautifully:
- **5 collections**: No performance issues
- **20 collections**: Still very fast
- **50+ collections**: Consider lazy-loading for homepage (future enhancement)

The combination of AI metadata + flat-file structure is perfect for a growing portfolio!

---

## Next Time You Add a Collection

Every single time, just run:

```bash
export ANTHROPIC_API_KEY='sk-ant-...'  # If not already set
python3 scripts/generate-collection.py assets/images/gallery/your-new-collection

# Answer prompts
# Review metadata.json (usually excellent!)
# git add, commit, push
# Done!
```

**Zero friction. Zero manual configuration. Fully scalable.** 🚀

---

## Questions?

Refer to:
- **Script help**: `python3 scripts/generate-collection.py --help`
- **Script docstring**: Check top of `scripts/generate-collection.py`
- **Anthropic API docs**: [https://docs.anthropic.com](https://docs.anthropic.com)
