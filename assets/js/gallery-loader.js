/**
 * Gallery Loader
 * Dynamically loads metadata.json files and renders gallery sections
 * Shows only featured images on homepage as curated previews
 */

(async function loadGalleries() {
  const collectionsContainer = document.getElementById('collections-container');
  
  // List of collection IDs that match your metadata files
  const collections = [
    'big-bend-2025',
    'colorado-rodeo-2025',
    'celebration-christmas-2025',
    'germany-austria-2023',
    'japan-2025'
  ];

  try {
    for (const collectionId of collections) {
      const metadataPath = `assets/images/gallery/${collectionId}/metadata.json`;
      
      try {
        const response = await fetch(metadataPath);
        
        if (!response.ok) {
          console.warn(`Failed to load metadata for ${collectionId}: ${response.status}`);
          continue;
        }

        const metadata = await response.json();
        const section = createGallerySection(metadata);
        collectionsContainer.appendChild(section);
      } catch (error) {
        console.error(`Error loading ${collectionId}:`, error);
      }
    }
  } catch (error) {
    console.error('Error in gallery loader:', error);
  }
})();

/**
 * Creates a gallery section element from metadata
 * Shows only featured images as a curated preview
 */
function createGallerySection(metadata) {
  const section = document.createElement('section');
  section.className = 'gallery-section';
  section.id = `gallery-${metadata.collection.id}`;

  // Collection header
  const collectionHeader = document.createElement('div');
  collectionHeader.className = 'collection-header';
  collectionHeader.innerHTML = `
    <h2>${metadata.collection.title}</h2>
    <p class="collection-meta">${metadata.collection.location} • ${metadata.collection.date}</p>
    <p class="collection-description">${metadata.collection.description}</p>
  `;
  section.appendChild(collectionHeader);

  // Gallery grid - show only featured images
  const gallery = document.createElement('div');
  gallery.className = 'gallery';

  // Filter to featured images only, fallback to first 6 if no featured images exist
  const featuredImages = metadata.images.filter(img => img.featured);
  const imagesToDisplay = featuredImages.length > 0 ? featuredImages : metadata.images.slice(0, 6);

  // Add each image
  imagesToDisplay.forEach((image) => {
    const figure = createImageFigure(image, metadata.collection.id);
    gallery.appendChild(figure);
  });

  section.appendChild(gallery);

  // Link to full collection page
  const viewMore = document.createElement('div');
  viewMore.className = 'view-collection-link';
  const imageCount = metadata.images.length;
  const hiddenCount = imageCount - imagesToDisplay.length;
  const countText = hiddenCount > 0 ? ` (+${hiddenCount} more)` : '';
  
  viewMore.innerHTML = `
    <a href="collection.html?id=${metadata.collection.slug}" aria-label="View all ${imageCount} images in ${metadata.collection.title} collection">
      View Full Collection${countText} &rarr;
    </a>
  `;
  section.appendChild(viewMore);

  return section;
}

/**
 * Creates an image figure element
 */
function createImageFigure(image, collectionId) {
  const figure = document.createElement('figure');
  
  const thumbnailPath = `assets/images/gallery/${collectionId}/thumbnails/${image.filename}`;
  const fullImagePath = `assets/images/gallery/${collectionId}/full-res/${image.filename}`;
  
  figure.innerHTML = `
    <img
      class="js-lightbox-trigger"
      src="${thumbnailPath}"
      data-full="${fullImagePath}"
      alt="${image.description}"
      data-title="${image.title}"
    />
    <figcaption>${image.title}</figcaption>
  `;

  return figure;
}
