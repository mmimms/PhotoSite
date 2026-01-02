/**
 * Gallery Loader
 * Dynamically loads metadata.json files and renders gallery sections
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

  // Gallery grid
  const gallery = document.createElement('div');
  gallery.className = 'gallery';

  // Add each image
  metadata.images.forEach((image, index) => {
    const figure = createImageFigure(image, metadata.collection.id);
    gallery.appendChild(figure);
  });

  section.appendChild(gallery);

  // Link to full collection page - UPDATED to use dynamic collection.html
  const viewMore = document.createElement('div');
  viewMore.className = 'view-collection-link';
  viewMore.innerHTML = `
    <a href="collection.html?id=${metadata.collection.slug}" aria-label="View full ${metadata.collection.title} collection">
      View Full Collection &rarr;
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
