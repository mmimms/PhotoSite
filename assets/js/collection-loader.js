/**
 * Collection Loader
 * Handles loading specific gallery collections based on URL parameter
 * Usage: collection.html?id=collection-slug
 */

document.addEventListener('DOMContentLoaded', async () => {
  // 1. Get collection ID from URL
  const urlParams = new URLSearchParams(window.location.search);
  const collectionId = urlParams.get('id');

  if (!collectionId) {
    showError('No collection specified.');
    return;
  }

  // 2. Load Metadata
  const metadataPath = `assets/images/gallery/${collectionId}/metadata.json`;

  try {
    const response = await fetch(metadataPath);
    if (!response.ok) throw new Error('Collection not found');
    
    const metadata = await response.json();
    renderCollection(metadata);
    
    // Update page title
    document.title = `${metadata.collection.title} · Mark Mimms Photography`;

  } catch (error) {
    console.error('Error loading collection:', error);
    showError('Collection could not be loaded. Please return to the portfolio.');
  }
});

/**
 * Renders the collection content into the DOM
 */
function renderCollection(data) {
  const { collection, images } = data;

  // Header
  const headerContainer = document.getElementById('collection-header');
  headerContainer.innerHTML = `
    <h1>${collection.title}</h1>
    <span>${collection.location} • ${collection.date}</span>
  `;

  // Description
  const introContainer = document.getElementById('collection-intro');
  introContainer.innerHTML = `<p>${collection.description}</p>`;

  // Grid
  const gridContainer = document.getElementById('collection-grid');
  gridContainer.innerHTML = ''; // Clear skeleton/loading state

  images.forEach(image => {
    const figure = document.createElement('figure');
    
    // Paths
    const thumbPath = `assets/images/gallery/${collection.id}/thumbnails/${image.filename}`;
    const fullPath = `assets/images/gallery/${collection.id}/full/${image.filename}`;
    
    // Print info (placeholder for e-commerce)
    const printInfo = image.printAvailable 
      ? `<div class="print-meta">Prints starting at $${image.printSizes[0].price}</div>`
      : '';

    figure.innerHTML = `
      <div class="image-wrapper">
        <img 
          class="js-lightbox-trigger"
          src="${thumbPath}" 
          data-full="${fullPath}" 
          alt="${image.description}"
          data-title="${image.title}"
        />
      </div>
      <figcaption>
        <strong>${image.title}</strong>
        ${printInfo}
      </figcaption>
    `;
    
    gridContainer.appendChild(figure);
  });
}

function showError(message) {
  const main = document.getElementById('collection-main');
  main.innerHTML = `
    <div class="error-state">
      <h2>Error</h2>
      <p>${message}</p>
      <a href="index.html" class="button">Return Home</a>
    </div>
  `;
}
