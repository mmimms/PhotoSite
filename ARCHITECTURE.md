# PhotoSite Architecture

## Overview

PhotoSite is a **metadata-driven photography portfolio** with AI-assisted collection management. Gallery collections are defined in JSON metadata files, which are dynamically loaded and rendered by JavaScript. This design allows:

- **Easy portfolio updates** without touching HTML
- **AI-generated metadata** (descriptions, tags, pricing)
- **Responsive galleries** that work on all devices
- **Fast performance** with optimized images and caching
- **Scalable structure** to grow from 5 to 50+ collections

## Directory Structure

```
PhotoSite/
├── index.html                          # Homepage with featured galleries
├── about.html                          # About the photographer
├── contact.html                        # Contact form + validation
├── browse.html                         # Tag-based image browser
├── collection.html                     # Individual collection page template
│
├── contact.php                         # Email handler (needs security fixes)
│
├── scripts/
│   ├── generate-collection.py          # Main workflow: AI + thumbnails (Perplexity)
│   └── generate-collection-claude.py    # Alternative: Claude API
│
├── generate-thumbnails.py              # Standalone thumbnail batch processor
│
├── assets/
│   ├── css/
│   │   └── styles.css                  # Global dark theme + responsive design
│   │
│   ├── js/
│   │   ├── gallery-loader.js           # Loads metadata + renders featured galleries
│   │   ├── browse-loader.js            # Tag filtering + image display
│   │   ├── collection-loader.js        # Full collection page rendering
│   │   └── script.js                   # Lightbox + keyboard navigation
│   │
│   └── images/
│       └── gallery/
│           ├── big-bend-2025/
│           │   ├── metadata.json           # Collection + image metadata
│           │   ├── full-res/               # Original photos (3000+px)
│           │   └── thumbnails/             # Web-optimized (400px)
│           │
│           ├── japan-2025/
│           │   ├── metadata.json
│           │   ├── full-res/
│           │   └── thumbnails/
│           │
│           ├── england-2024/
│           │   ├── metadata.json
│           │   ├── full-res/
│           │   └── thumbnails/
│           │
│           └── ... (6 collections total)
│
├── ReadMe.md                           # Project overview
├── ARCHITECTURE.md                     # This file
├── COLLECTION_SETUP.md                 # How to add new collections
├── Roadmap.md                          # Future features & plan
└── .gitignore                          # Git exclusions
```

## Metadata JSON Structure

Each collection has a `metadata.json` file that defines all collection and image data:

```json
{
  "collection": {
    "id": "japan-2025",
    "title": "Japan 2025",
    "slug": "japan-2025",
    "displayCategory": "Travel & Adventure",
    "description": "A winter journey through Japan's temples, gardens, and natural wonders. Captured during the quiet blue hour and winter season.",
    "location": "Japan, Kyoto, Tokyo, Hakone",
    "date": "2025",
    "coverImage": "Fushimi Inari Gates.jpg",
    "featured": true,
    "printAvailable": true
  },
  "images": [
    {
      "id": "fushimi-inari-gates",
      "title": "Fushimi Inari Gates",
      "filename": "Fushimi Inari Gates.jpg",
      "description": "A thousand vermillion torii gates create a spiritual passage through the sacred grounds of Fushimi Inari shrine in Kyoto. The geometric repetition and warm tones evoke contemplation and reverence.",
      "location": "Kyoto, Japan",
      "tags": ["japan", "temple", "spiritual", "architecture", "featured", "torii"],
      "printSizes": [
        {"size": "8x10", "price": 50},
        {"size": "11x14", "price": 85},
        {"size": "16x20", "price": 140},
        {"size": "20x30", "price": 235}
      ],
      "featured": true,
      "printAvailable": true
    },
    {
      "id": "lantern-reflection",
      "title": "Lantern Reflection",
      "filename": "Lantern Reflection.jpg",
      "description": "A traditional Japanese lantern casts its warm glow across water, reflecting the gentle light. The minimalist composition captures the essence of Japanese aesthetics—simplicity and contemplation.",
      "location": "Kyoto, Japan",
      "tags": ["japan", "night", "temple", "lanterns", "water", "peaceful"],
      "printSizes": [
        {"size": "8x10", "price": 50},
        {"size": "11x14", "price": 85},
        {"size": "16x20", "price": 140},
        {"size": "20x30", "price": 235}
      ],
      "featured": false,
      "printAvailable": true
    }
  ]
}
```

### Metadata Fields

**Collection-level:**
- `id` - Unique identifier (matches folder name)
- `title` - Display title for collection header
- `slug` - URL-friendly version of title
- `displayCategory` - Category for organization (e.g., "Travel & Adventure")
- `description` - Full paragraph describing collection
- `location` - Where photos were taken
- `date` - Year or date range
- `coverImage` - First image filename for collection card
- `featured` - Show on homepage
- `printAvailable` - Enable print purchasing

**Per-image:**
- `id` - URL-friendly slug
- `title` - Image title for captions
- `filename` - Actual file in `full-res/` folder
- `description` - 1-2 sentences for alt text and print marketing
- `location` - Specific location taken
- `tags` - Array of searchable tags (curated vocabulary)
- `printSizes` - Array of print options with prices
- `featured` - Show on homepage gallery preview
- `printAvailable` - Enable print purchasing

## How It Works

### 1. Homepage (`index.html`)

**Flow:**
1. HTML page loads with empty `<div id="collections-container">`
2. `gallery-loader.js` executes (deferred load)
3. Script iterates through collection IDs hardcoded in array:
   ```javascript
   const collections = [
     'big-bend-2025',
     'colorado-rodeo-2025',
     'celebration-christmas-2025',
     'germany-austria-2023',
     'japan-2025',
     'england-2024'
   ];
   ```
4. For each collection, fetches `assets/images/gallery/{id}/metadata.json`
5. Creates gallery section with:
   - Collection header (title, location, date, description)
   - Featured images grid (filters to `featured: true`)
   - "View Full Collection" link
6. Appends to DOM

**Template created by `createGallerySection()`:**
```html
<section class="gallery-section" id="gallery-japan-2025">
  <div class="collection-header">
    <h2>Japan 2025</h2>
    <p class="collection-meta">Japan, Kyoto, Tokyo, Hakone • 2025</p>
    <p class="collection-description">A winter journey through...</p>
  </div>
  
  <div class="gallery">
    <!-- Featured images only (filtered by featured: true) -->
    <figure>
      <img class="js-lightbox-trigger" 
           src="assets/images/gallery/japan-2025/thumbnails/Fushimi Inari Gates.jpg"
           data-full="assets/images/gallery/japan-2025/full-res/Fushimi Inari Gates.jpg"
           alt="A thousand vermillion torii gates..."
           data-title="Fushimi Inari Gates" />
      <figcaption>Fushimi Inari Gates</figcaption>
    </figure>
    <!-- More featured images -->
  </div>
  
  <div class="view-collection-link">
    <a href="collection.html?id=japan-2025">View Full Collection (+10 more) &rarr;</a>
  </div>
</section>
```

### 2. Browse Page (`browse.html`)

**Flow:**
1. Page loads with empty `<div id="tag-filter">` and `<div id="browse-galleries">`
2. `browse-loader.js` fetches metadata for all collections
3. Extracts unique tags from all images
4. Creates filter buttons for each tag (+ "All" button)
5. When tag clicked, filters images and re-renders galleries
6. Shows only images with that tag

**Example:** Click "japan" → shows only images with `"japan"` in tags array

### 3. Collection Page (`collection.html`)

**Flow:**
1. Page loads with query parameter: `collection.html?id=japan-2025`
2. `collection-loader.js` reads URL parameter
3. Fetches metadata for that specific collection
4. Renders **all images** (not just featured)
5. Sets page title to collection name
6. Shows breadcrumb back to home

**Template created by `collection-loader.js`:**
```html
<main id="collection-main">
  <div class="breadcrumb">
    <a href="index.html">&larr; Back to Portfolio</a>
  </div>
  
  <div id="collection-header" class="header-bar">
    <h1>Japan 2025</h1>
  </div>
  
  <div id="collection-intro" class="intro-text">
    <!-- Collection description -->
  </div>
  
  <div id="collection-grid" class="gallery">
    <!-- All images (featured and non-featured) -->
  </div>
</main>
```

### 4. Image Viewing (`script.js` - Lightbox)

**Flow:**
1. User clicks any image with class `js-lightbox-trigger`
2. Lightbox modal opens with full-resolution image
3. Shows image title as caption
4. Keyboard navigation:
   - **Escape** - Close
   - **Left/Right arrows** - Next/previous image (future enhancement)
5. Click backdrop to close

**Lightbox HTML:**
```html
<div class="lightbox" id="lightbox" aria-hidden="true">
  <div class="lightbox-backdrop"></div>
  <figure class="lightbox-content">
    <button class="lightbox-close" aria-label="Close image">×</button>
    <img src="" alt="" id="lightbox-image" />
    <figcaption id="lightbox-caption"></figcaption>
  </figure>
</div>
```

## Adding a New Collection

### Automated Workflow (Recommended)

```bash
# 1. Create folder
mkdir -p assets/images/gallery/your-collection/{full-res,thumbnails}

# 2. Copy images
cp ~/Pictures/photos/*.jpg assets/images/gallery/your-collection/full-res/

# 3. Set API key
export PERPLEXITY_API_KEY='pplx-...'

# 4. Run script (does EVERYTHING)
python3 scripts/generate-collection.py assets/images/gallery/your-collection

# 5. Review metadata.json
vim assets/images/gallery/your-collection/metadata.json

# 6. Commit and push
git add assets/images/gallery/your-collection/
git commit -m 'Add your-collection'
git push origin main

# Homepage automatically updates!
```

The script:
- 📸 Generates thumbnails (400px, JPEG quality 85)
- 🤖 Analyzes each image with Perplexity AI
- 📝 Creates metadata.json with descriptions, tags, pricing
- 📝 Updates JavaScript collection arrays automatically
- 📱 Selects featured images intelligently (1st, every 3rd, last)

### Manual Workflow (If Script Fails)

1. **Create folder structure** (see above)
2. **Generate thumbnails** manually:
   ```bash
   python3 generate-thumbnails.py
   ```
3. **Create metadata.json** from template in [COLLECTION_SETUP.md](./COLLECTION_SETUP.md)
4. **Update JavaScript files:**
   - Add collection ID to `assets/js/gallery-loader.js`
   - Add collection ID to `assets/js/browse-loader.js`
5. **Commit and push**

## Image Optimization

### Thumbnails (Homepage)
- **Size**: 400px width (maintains aspect ratio)
- **Format**: JPEG
- **Quality**: 85 (balances file size and visual quality)
- **Generated by**: `generate-collection.py` or `generate-thumbnails.py`
- **Purpose**: Homepage gallery grid, fast initial page load
- **Typical file size**: 40-80KB per image

### Full-Resolution (Lightbox)
- **Size**: Original (typical 3000-4000px width)
- **Format**: JPEG
- **Quality**: 90-95 (high quality for print)
- **Source**: Your original photos in `full-res/` folder
- **Purpose**: Lightbox display, print quality reference
- **Typical file size**: 2-5MB per image

### Cloudflare Optimization
All images are cached and optimized by Cloudflare CDN:
- Automatic format conversion (WebP if supported)
- Responsive resizing on-the-fly
- Geographic distribution
- GZIP compression

## CSS Architecture

### Design System (`assets/css/styles.css`)

**Dark theme** optimized for photography:
- Background: #050608 (near-black)
- Accent color: #f97316 (orange)
- Text: #f4f4f4 (light gray)
- Borders: subtle gray dividers

**Layout:**
- **CSS Grid** for image galleries (auto-flowing columns)
- **Flexbox** for navigation and cards
- **Responsive breakpoints**: 600px, 900px
- **Mobile-first** design (scales up from mobile)

**Key classes:**
- `.gallery` - Image grid (auto-columns, gap)
- `.gallery-section` - Collection wrapper
- `.collection-header` - Title + metadata
- `.lightbox` - Modal overlay
- `.lightbox-content` - Centered image container

## JavaScript Architecture

### No Build Step
- Pure vanilla JavaScript (no bundler needed)
- Async/await syntax (ES6+)
- Intersection Observer API for lazy loading
- Event delegation for lightbox triggers
- Dynamic DOM creation

### File Loaders
Each loader fetches metadata and renders:
- `gallery-loader.js` - Homepage featured galleries
- `browse-loader.js` - Tag filtering page
- `collection-loader.js` - Full collection pages

### Shared Functionality
- `script.js` - Lightbox modal (shared across all pages)

## Contact Form

### Frontend (`contact.html`)
- HTML5 form validation
- Honeypot field (hidden from users)
- ARIA labels for accessibility
- Required field indicators

### Backend (`contact.php`)
**Current implementation:**
- Email validation (`filter_var()`)
- Basic input sanitization (`strip_tags()`, `trim()`)
- Honeypot spam detection
- PHP `mail()` function

**⚠️ Security Issues (Needs Fixing):**
1. Email header injection vulnerable (name/email not fully sanitized)
2. No CSRF token protection
3. Unreliable email delivery (no authentication)

**Recommended improvements:**
1. Add CSRF token to form
2. Sanitize all fields including subject
3. Integrate SendGrid API for reliable delivery
4. Add rate limiting
5. Log all submissions

See [GitHub Issues](https://github.com/mmimms/PhotoSite/issues) for detailed fixes.

## Python Scripts

### `scripts/generate-collection.py` (Recommended)

**Purpose:** Fully automate collection creation with AI metadata

**Workflow:**
1. Validates folder structure
2. Detects if new or existing collection
3. Generates thumbnails (new images only if updating)
4. Uses Perplexity API to analyze each image
   - Analyzes actual image content
   - Considers collection context
   - Generates buyer-friendly descriptions
   - Selects relevant tags
5. Creates/updates `metadata.json`
6. Updates JavaScript configuration (new collections only)
7. Selects featured images intelligently

**Usage:**
```bash
export PERPLEXITY_API_KEY='pplx-...'
python3 scripts/generate-collection.py assets/images/gallery/my-collection
```

**Dependencies:**
```bash
pip install Pillow requests
```

### `generate-thumbnails.py` (Standalone)

**Purpose:** Batch generate thumbnails without metadata generation

**Usage:**
```bash
python3 generate-thumbnails.py
```

**What it does:**
- Scans all `gallery/*/full-res/` folders
- Creates thumbnails in `thumbnails/` folder
- Preserves EXIF metadata
- Progressive JPEG for better web loading
- Skips already-processed images

**Dependencies:**
```bash
pip install Pillow
```

## Performance Optimization

### Current Optimizations
1. **Lazy loading** - Images load as user scrolls
2. **Thumbnail caching** - Small images load first
3. **Responsive images** - Browser downloads appropriate size
4. **JPEG optimization** - Quality 85 for thumbnails, 90+ for full-res
5. **Cloudflare CDN** - Global caching and distribution
6. **Metadata caching** - 24-hour cache headers
7. **Gzip compression** - Enabled by Cloudflare

### Future Optimizations
1. **WebP format** - Smaller file sizes with Cloudflare Image Optimization
2. **Srcset** - Multiple image sizes for responsive design
3. **HTTP/2 Server Push** - Preload critical images
4. **Service Worker** - Offline caching
5. **Critical CSS** - Inline above-the-fold styles
6. **Image lazy loading** - `loading="lazy"` attribute

### Load Time Targets
- Homepage: <1 second (Cloudflare cached)
- Browse page: <1 second
- Collection page: <2 seconds
- Lightbox: Instant (preloaded)

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

**Required features:**
- ES6+ (arrow functions, async/await)
- CSS Grid
- Flexbox
- Intersection Observer
- Fetch API

**Graceful degradation:**
- Works without JavaScript (static images shown)
- Lightbox optional enhancement
- Filters degrade gracefully

## Accessibility

### WCAG 2.1 Level AA Compliance

**Semantic HTML:**
- `<nav>` for navigation
- `<main>` for main content
- `<section>` for gallery sections
- `<figure>` + `<figcaption>` for images
- `<footer>` for footer

**ARIA Labels:**
- `aria-label` on buttons
- `aria-current="page"` on nav links
- `aria-hidden` on decorative elements
- `aria-required` on form fields

**Keyboard Navigation:**
- Tab through images and buttons
- Enter/Space to activate buttons
- Escape to close lightbox
- Focus visible on all interactive elements

**Color Contrast:**
- All text meets 4.5:1 ratio (AA standard)
- Orange accent: high contrast against dark background

**Alt Text:**
- All images have descriptive alt text
- Alt text uses image description from metadata

## Deployment

### Cloudflare Pages (Recommended)
1. Push to GitHub
2. Cloudflare Pages auto-deploys
3. Build: `npm install && npm run build` (or none for static)
4. Publish directory: `/` (root)
5. Caching: 24 hours for images, 5 minutes for metadata

### Local Development
```bash
python -m http.server 8000
http://localhost:8000
```

### Manual Deployment
```bash
# Test
python -m http.server 8000

# Deploy
gh pages deploy --source=.
```

## Collections (Current)

| ID | Title | Images | Location | Featured |
|----|-------|--------|----------|----------|
| `big-bend-2025` | Big Bend 2025 | 7 | Texas, USA | ✅ |
| `colorado-rodeo-2025` | Colorado Rodeo 2025 | 5 | Colorado, USA | ✅ |
| `celebration-christmas-2025` | Celebration Christmas 2025 | 2 | Various | ✅ |
| `germany-austria-2023` | Germany & Austria 2023 | 5 | Europe | ✅ |
| `japan-2025` | Japan 2025 | 13 | Japan | ✅ |
| `england-2024` | England 2024 | TBD | England | ✅ |

**Total**: 32+ images across 6 collections

## File Size Reference

**Per collection (average 10 images):**
- Metadata: 3-5KB
- Thumbnails (10 × 60KB): 600KB
- Full-resolution (10 × 3MB): 30MB
- **Total**: ~31MB

**Homepage load:**
- 6 collections × 4 featured images = 24 thumbnails
- ~1.5MB uncompressed
- <100KB gzipped (Cloudflare)
- Load time: <1 second

## Future Enhancements

- [ ] E-commerce integration (The Print Space API)
- [ ] Individual product pages
- [ ] Print customization (sizes, materials, frames)
- [ ] Order management dashboard
- [ ] Advanced search and filtering
- [ ] Image comparison tool
- [ ] Before/after slider
- [ ] Responsive srcset for images
- [ ] WebP format support
- [ ] Service Worker for offline access
- [ ] User authentication for order history
- [ ] Analytics dashboard
- [ ] Social sharing improvements

See [Roadmap.md](./Roadmap.md) for detailed timeline.

## Further Reading

- [ReadMe.md](./ReadMe.md) - Project overview
- [COLLECTION_SETUP.md](./COLLECTION_SETUP.md) - Adding collections guide
- [Roadmap.md](./Roadmap.md) - Feature roadmap
- [Perplexity API Documentation](https://docs.perplexity.ai)
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
