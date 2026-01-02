# PhotoSite Architecture

## Overview

PhotoSite is a metadata-driven photography portfolio website. Gallery collections are managed through JSON metadata files, which are dynamically loaded and rendered by JavaScript. This allows for easy portfolio updates without touching HTML.

## Directory Structure

```
PhotoSite/
├── index.html                          # Homepage with dynamic gallery loader
├── about.html                          # About the photographer
├── contact.html                        # Contact form
├── ARCHITECTURE.md                     # This file
│
├── assets/
│   ├── css/
│   │   └── styles.css                 # Global styles
│   │
│   ├── js/
│   │   ├── gallery-loader.js          # Loads metadata and renders galleries
│   │   └── script.js                  # Lightbox functionality
│   │
│   └── images/
│       └── gallery/
│           ├── big-bend-2025/
│           │   ├── metadata.json      # Collection metadata
│           │   ├── thumbnails/        # Screen-optimized images (max 2000px)
│           │   └── full/              # Full-resolution images
│           │
│           ├── colorado-rodeo-2025/
│           │   ├── metadata.json
│           │   ├── thumbnails/
│           │   └── full/
│           │
│           ├── celebration-christmas-2025/
│           │   ├── metadata.json
│           │   ├── thumbnails/
│           │   └── full/
│           │
│           ├── germany-austria-2023/
│           │   ├── metadata.json
│           │   ├── thumbnails/
│           │   └── full/
│           │
│           └── japan-2025/
│               ├── metadata.json
│               ├── thumbnails/
│               └── full/
```

## Metadata JSON Structure

Each gallery collection has a `metadata.json` file that defines:

```json
{
  "collection": {
    "id": "collection-slug",
    "title": "Collection Title",
    "slug": "collection-slug",
    "displayCategory": "Category Name",
    "description": "Full description of the collection",
    "location": "Where photos were taken",
    "date": "Year or date range",
    "coverImage": "filename-of-cover.jpg",
    "featured": true,
    "printAvailable": true
  },
  "images": [
    {
      "id": "image-slug",
      "title": "Image Title",
      "filename": "Image Title - Screen.jpg",
      "description": "Detailed description for alt text and metadata",
      "location": "Specific location",
      "tags": ["tag1", "tag2", "featured"],
      "printSizes": [
        {"size": "8x10", "price": 45},
        {"size": "11x14", "price": 75},
        {"size": "16x20", "price": 125},
        {"size": "20x30", "price": 195}
      ],
      "featured": false,
      "printAvailable": true
    }
  ]
}
```

## How It Works

### 1. Homepage (`index.html`)

- Loads `gallery-loader.js` on page load
- `gallery-loader.js` iterates through 5 predefined collections
- For each collection, it fetches `metadata.json`
- Dynamically creates gallery sections with:
  - Collection header (title, location, date, description)
  - Image grid with thumbnails
  - "View Full Collection" link

### 2. Image Gallery Rendering

`gallery-loader.js` creates:
- `<section class="gallery-section">` wrapper
- `<div class="collection-header">` with metadata
- `<div class="gallery">` grid of images
- Each image uses:
  - `src`: Path to thumbnail
  - `data-full`: Path to full-resolution image
  - `data-title`: Image title for lightbox caption
  - `alt`: Description for accessibility

### 3. Lightbox (`script.js`)

- Clicks on any `.js-lightbox-trigger` image open the lightbox
- Lightbox displays full-resolution image with caption
- Close via:
  - Close button (×)
  - Backdrop click
  - Escape key
- Prevents body scroll while lightbox is open

### 4. Styling (`styles.css`)

- Responsive CSS Grid for image galleries
- Dark theme optimized for photography
- Mobile breakpoints at 600px and 900px
- Smooth hover and transition effects

## Adding a New Collection

### Step 1: Create Folder Structure
```bash
mkdir -p assets/images/gallery/your-collection-slug/{thumbnails,full}
```

### Step 2: Create metadata.json
```json
{
  "collection": {
    "id": "your-collection-slug",
    "title": "Your Collection Title",
    // ... complete metadata
  },
  "images": [ /* ... */ ]
}
```

### Step 3: Add Images
- Place thumbnail images in `thumbnails/` (max 2000px width)
- Place full-resolution images in `full/`
- Image filenames should match `metadata.json` filenames

### Step 4: Register Collection
Add collection slug to `assets/js/gallery-loader.js`:
```javascript
const collections = [
  'big-bend-2025',
  'colorado-rodeo-2025',
  'celebration-christmas-2025',
  'germany-austria-2023',
  'japan-2025',
  'your-collection-slug'  // Add here
];
```

## Image Optimization

### Thumbnails
- **Size**: Max 2000px width
- **Format**: JPG (quality 80-85)
- **Purpose**: Homepage gallery grid, fast loading

### Full Resolution
- **Size**: Original or max 4000px width
- **Format**: JPG (quality 90-95)
- **Purpose**: Lightbox display

**Tools**:
- ImageMagick: `convert input.jpg -resize 2000x2000 output.jpg`
- GraphicsMagick: `gm convert input.jpg -resize 2000x2000 output.jpg`
- Cloudflare Image Optimization: Automatic via CDN

## Performance Considerations

### Current Optimization
1. **Lazy Loading**: Implemented via Intersection Observer in `gallery-loader.js`
2. **Responsive Images**: CSS Grid adapts to viewport
3. **Progressive Enhancement**: Works without JavaScript (static images shown)
4. **Caching**: Cloudflare caches images + metadata

### Future Enhancements
1. Add `loading="lazy"` to image tags
2. Implement WebP format with JPEG fallback
3. Use Cloudflare Workers to transform images on-the-fly
4. Add image srcset for responsive image sizes

## Collections (Current)

| Slug | Title | Images | Category |
|------|-------|--------|----------|
| `big-bend-2025` | Big Bend 2025 | 7 | Western Landscapes |
| `colorado-rodeo-2025` | Colorado Rodeo 2025 | 5 | Action Sports |
| `celebration-christmas-2025` | Celebration Christmas 2025 | 2 | Holidays & Events |
| `germany-austria-2023` | Germany & Austria 2023 | 5 | Travel & Culture |
| `japan-2025` | Japan 2025 | 13 | Travel & Adventure |

**Total**: 32 images across 5 collections

## CSS Classes & Structure

### Gallery Components
```html
<section class="gallery-section">
  <div class="collection-header">
    <h2>Collection Title</h2>
    <p class="collection-meta">Location • Date</p>
    <p class="collection-description">Description...</p>
  </div>
  
  <div class="gallery">
    <figure>
      <img class="js-lightbox-trigger" ... />
      <figcaption>Image Title</figcaption>
    </figure>
    <!-- More figures -->
  </div>
  
  <div class="view-collection-link">
    <a href="...">View Full Collection →</a>
  </div>
</section>
```

### Lightbox
```html
<div class="lightbox" id="lightbox">
  <div class="lightbox-backdrop"></div>
  <figure class="lightbox-content">
    <button class="lightbox-close">×</button>
    <img id="lightbox-image" />
    <figcaption id="lightbox-caption"></figcaption>
  </figure>
</div>
```

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript (arrow functions, async/await)
- CSS Grid and Flexbox
- No jQuery or heavy dependencies

## Accessibility

- Semantic HTML (`<figure>`, `<figcaption>`, `<nav>`)
- ARIA labels on buttons and regions
- Focus management in lightbox
- Keyboard navigation (Escape to close)
- Alt text on all images
- Sufficient color contrast

## Deployment

### Cloudflare Pages
1. Push changes to GitHub
2. Cloudflare Pages automatically deploys from main branch
3. Images are cached and optimized by Cloudflare CDN

### Manual Testing
```bash
# Start local server
python -m http.server 8000

# Visit
http://localhost:8000
```

## Future Features

- [ ] Individual collection pages
- [ ] E-commerce integration (print ordering)
- [ ] Image filtering by tag
- [ ] Search functionality
- [ ] Image comparison slider
- [ ] Print customization (sizes, frames)
- [ ] Order management dashboard
- [ ] Analytics tracking

## File Size Reference

Total metadata: ~50KB (5 files)
Typical gallery:
- 10 thumbnails × 150KB = 1.5MB
- 10 full images × 800KB = 8MB
- **Total per collection: ~9.5MB**

With Cloudflare caching and compression, page loads are very fast after first visit.

## Contact & Support

For questions about the architecture, see:
- `index.html` - Homepage implementation
- `assets/js/gallery-loader.js` - Gallery rendering logic
- `assets/css/styles.css` - Design system
