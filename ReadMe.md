# PhotoSite

A photography portfolio website with AI-assisted collection management, built for fast performance and easy scaling.

## Project Goals

- **Showcase** high-quality photo galleries that load fast
- **Manage** collections efficiently with AI-generated metadata
- **Sell** prints via The Print Space integration (in development)
- **Scale** from personal portfolio to full e-commerce platform
- **Optimize** hosting costs with static assets + lightweight backend

## Key Features

- 📸 **Featured image galleries** on homepage with dynamic collection loading
- 🏷️ **Tag-based browsing** to explore images across collections
- 🎨 **Dark theme design** optimized for photography
- 📱 **Fully responsive** (mobile, tablet, desktop)
- ⚡ **Fast loading** with lazy loading and optimized thumbnails
- 🤖 **AI metadata generation** with Perplexity API (experimental) or Claude API
- 🔍 **Accessible** with semantic HTML, ARIA labels, keyboard navigation
- 📧 **Working contact form** with reCAPTCHA v3 spam protection

## Current Collections

| Collection | Images | Location |
|---|---|---|
| Big Bend 2025 | 7 | Texas, USA |
| Colorado Rodeo 2025 | 5 | Colorado, USA |
| Celebration Christmas 2025 | 2 | Various |
| Germany & Austria 2023 | 5 | Europe |
| Japan 2025 | 13 | Japan |
| England 2024 | TBD | England |

**Total: 32+ images** across 6 collections

## Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Grid, Flexbox, responsive design
- **Vanilla JavaScript** - No frameworks, minimal dependencies
- **Intersection Observer API** - Lazy loading

### Backend
- **PHP** - Contact form processing
- **Python** - Collection generation and thumbnail processing
  - `generate-collection.py` - AI metadata generation + thumbnail creation
  - `generate-thumbnails.py` - Batch thumbnail generation

### Infrastructure
- **Cloudflare** - CDN, DNS, caching, SSL
- **Cloudflare Pages** - Auto-deploy from GitHub
- **The Print Space** - Print lab integration (planned)

### AI/APIs
- **Perplexity API** (primary, vision-capable) - Image analysis + metadata generation
- **Claude API** (Anthropic) - Fallback for metadata generation
- **Google reCAPTCHA v3** - Invisible spam protection on contact form
- **SendGrid** (recommended) - Email delivery for contact forms

## Contact Form (COMPLETE)

✅ **Status**: Working - reCAPTCHA v3 integrated and tested

### Features
- Invisible bot protection (no user interaction needed)
- Honeypot spam filter
- Email validation
- Real-time success/error notifications
- Logs reCAPTCHA scores for monitoring

**See [RECAPTCHA_SETUP.md](./RECAPTCHA_SETUP.md) for complete setup guide.**

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mmimms/PhotoSite.git
cd PhotoSite
```

### 2. Local Development

```bash
# Start a local server
python -m http.server 8000

# Visit
http://localhost:8000
```

### 3. Add a New Collection

```bash
# Create folder structure
mkdir -p assets/images/gallery/your-collection/{full-res,thumbnails}

# Copy your images
cp ~/Pictures/your-photos/*.jpg assets/images/gallery/your-collection/full-res/

# Set API key and run script
export PERPLEXITY_API_KEY='pplx-...'
python3 scripts/generate-collection.py assets/images/gallery/your-collection

# Commit and push
git add assets/images/gallery/your-collection/
git commit -m 'Add your-collection'
git push origin main
```

See [COLLECTION_SETUP.md](./COLLECTION_SETUP.md) for detailed guide.

## Project Structure

```
PhotoSite/
├── index.html                    # Homepage with featured galleries
├── about.html                    # About the photographer
├── contact.html                  # Contact form with reCAPTCHA v3
├── browse.html                   # Browse by tag
├── collection.html               # Individual collection page
│
├── contact.php                   # Email handler with spam protection
├── scripts/
│   ├── generate-collection.py    # AI metadata + thumbnails (Perplexity)
│   └── generate-collection-claude.py  # Alternative (Claude API)
│
├── generate-thumbnails.py        # Batch thumbnail generator
├── setup-folders.bat             # Windows folder setup
│
├── assets/
│   ├── css/styles.css            # Global styles
│   ├── js/
│   │   ├── gallery-loader.js     # Homepage gallery rendering
│   │   ├── browse-loader.js      # Tag filtering
│   │   ├── collection-loader.js  # Collection page rendering
│   │   └── script.js             # Lightbox functionality
│   │
│   └── images/gallery/
│       ├── big-bend-2025/
│       │   ├── metadata.json
│       │   ├── full-res/         # Original photos
│       │   └── thumbnails/       # Web-optimized
│       ├── japan-2025/
│       │   ├── metadata.json
│       │   ├── full-res/
│       │   └── thumbnails/
│       └── ... (other collections)
│
├── ReadMe.md                     # This file
├── ARCHITECTURE.md               # How everything works
├── COLLECTION_SETUP.md           # Adding collections guide
├── RECAPTCHA_SETUP.md            # Contact form setup guide
└── Roadmap.md                    # Future features
```

## Key Files Explained

### HTML Pages

- **index.html** - Homepage showing featured images from all collections
- **browse.html** - Browse by tag with filtering (experimental feature)
- **about.html** - About the photographer
- **contact.html** - Contact form with reCAPTCHA v3 bot protection
- **collection.html** - Full collection view (loaded from query parameter)

### JavaScript

- **gallery-loader.js** - Fetches metadata.json for each collection and renders featured images
- **browse-loader.js** - Loads metadata and provides tag-based filtering
- **collection-loader.js** - Loads and displays all images in a specific collection
- **script.js** - Lightbox modal for image viewing

### Python Scripts

- **generate-collection.py** - Main workflow
  - Generates thumbnails from full-res images
  - Analyzes images with Perplexity AI
  - Creates metadata.json with descriptions and tags
  - Updates JavaScript configuration
  - **Recommended for new collections**

- **generate-thumbnails.py** - Standalone thumbnail generator
  - Use if you want to generate thumbnails without AI
  - Useful for bulk processing

- **generate-collection-claude.py** - Alternative using Claude API (if Perplexity fails)

### PHP

- **contact.php** - Handles form submissions
  - Email validation
  - Honeypot spam detection
  - Google reCAPTCHA v3 verification
  - Configurable score threshold (default: 0.5)
  - Optional SendGrid integration for reliable delivery

## Image Requirements

### Full-Resolution Images
- **Format**: JPG/JPEG
- **Size**: Original size (typical 3000-4000px width)
- **Quality**: High (preservation of detail)
- **Storage**: `full-res/` folder

### Thumbnails
- **Generated automatically** by `generate-collection.py`
- **Size**: 400px width (responsive)
- **Quality**: 85 JPEG (good balance of size/quality)
- **Storage**: `thumbnails/` folder
- **Purpose**: Homepage gallery, fast initial load

## Metadata Format

Each collection has a `metadata.json` file:

```json
{
  "collection": {
    "id": "japan-2025",
    "title": "Japan 2025",
    "location": "Japan",
    "date": "2025",
    "description": "A winter journey through Japan's temples and natural wonders...",
    "coverImage": "Fushimi Inari.jpg",
    "featured": true,
    "printAvailable": true
  },
  "images": [
    {
      "id": "fushimi-inari",
      "title": "Fushimi Inari Gates",
      "filename": "Fushimi Inari.jpg",
      "description": "A thousand vermillion torii gates guide pilgrims...",
      "location": "Kyoto, Japan",
      "tags": ["japan", "temple", "spiritual", "architecture"],
      "printSizes": [
        {"size": "8x10", "price": 50},
        {"size": "11x14", "price": 85},
        {"size": "16x20", "price": 140},
        {"size": "20x30", "price": 235}
      ],
      "featured": true,
      "printAvailable": true
    }
  ]
}
```

## Performance

### Load Times (Cloudflare cached)
- Homepage: <1 second
- Browse page: <1 second
- Collection page: <2 seconds
- Lightbox image: Instant (preloaded)

### Optimization Strategies
1. **Lazy loading** - Images load as you scroll
2. **Thumbnail caching** - Cloudflare CDN caches all thumbnails
3. **Responsive images** - Browser downloads appropriate size
4. **Compression** - JPEG quality optimized for web
5. **JSON caching** - Metadata cached for 24 hours

### File Sizes
- Typical thumbnail: 40-80KB
- Typical full-res: 2-5MB
- Metadata (per collection): 3-5KB

## Deployment

### Automatic (Recommended)
```bash
git push origin main
# Cloudflare Pages auto-deploys in ~30 seconds
```

### Manual
```bash
# Test locally
python -m http.server 8000

# Deploy
gh pages deploy --source=.
```

## Troubleshooting

### Contact Form Issues
See [RECAPTCHA_SETUP.md - Troubleshooting](./RECAPTCHA_SETUP.md#troubleshooting)

### "No collections loaded on homepage"
- Check that metadata.json files exist in each collection folder
- Check browser console for fetch errors
- Verify folder paths match collection IDs in gallery-loader.js

### "Thumbnails not generating"
- Make sure `full-res/` folder contains JPG files
- Check that Pillow is installed: `pip install Pillow`
- Run: `python3 generate-thumbnails.py`

### "API key not set"
```bash
export PERPLEXITY_API_KEY='pplx-...'
# or
export CLAUDE_API_KEY='sk-ant-...'
```

### "Images not loading"
- Check image paths in metadata.json
- Verify files exist in `full-res/` and `thumbnails/` folders
- Check browser Network tab for 404 errors

## Known Issues

- **browse.html** - Tag filtering experimental, may have bugs
- **No HTTPS redirect** - Handled by Cloudflare
- **No The Print Space integration** - In development

See [GitHub Issues](https://github.com/mmimms/PhotoSite/issues) for current issues.

## Future Enhancements

- [ ] E-commerce integration (The Print Space)
- [ ] Individual product pages for prints
- [ ] Framing/mounting options
- [ ] Order tracking dashboard
- [ ] Image search
- [ ] User authentication for order history
- [ ] Before/after image slider
- [ ] Image comparison tool
- [ ] Advanced analytics
- [ ] Print customization (sizes, materials, frames)
- [ ] Social sharing improvements
- [ ] Internationalization (i18n)

See [Roadmap.md](./Roadmap.md) for detailed feature plans.

## Contributing

This is a personal project, but improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Photography © 2025 Mark Mimms. Code available under MIT License.

## Resources

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical deep dive
- [COLLECTION_SETUP.md](./COLLECTION_SETUP.md) - How to add collections
- [RECAPTCHA_SETUP.md](./RECAPTCHA_SETUP.md) - Contact form setup guide
- [Roadmap.md](./Roadmap.md) - Future plans
- [Perplexity API Docs](https://docs.perplexity.ai)
- [Claude API Docs](https://docs.anthropic.com)
- [Google reCAPTCHA Docs](https://developers.google.com/recaptcha/docs/v3)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)

## Contact

**Photography Inquiries**: Use the [Contact form](https://mimmsphoto.com/contact.html)

**Code Issues**: [GitHub Issues](https://github.com/mmimms/PhotoSite/issues)

---

**Updated**: January 2, 2026  
**Version**: 1.3  
**Status**: Active Development - Contact Form Complete ✅
