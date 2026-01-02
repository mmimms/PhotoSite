/**
 * Browse Loader
 * Loads all metadata.json files and provides tag-based filtering
 * Displays images grouped by selected tags
 */

const collections = [
  'big-bend-2025',
  'colorado-rodeo-2025',
  'celebration-christmas-2025',
  'germany-austria-2023',
  'japan-2025'
];

let allMetadata = []; // Store all metadata
let allTags = new Set(); // All unique tags
let selectedTags = new Set(['travel', 'landscape', 'nature']); // Default tags

document.addEventListener('DOMContentLoaded', async () => {
  await loadAllMetadata();
  renderTagButtons();
  renderGalleries();
});

/**
 * Load all metadata files from all collections
 */
async function loadAllMetadata() {
  for (const collectionId of collections) {
    const metadataPath = `assets/images/gallery/${collectionId}/metadata.json`;
    
    try {
      const response = await fetch(metadataPath);
      if (!response.ok) continue;
      
      const metadata = await response.json();
      
      // Extract all tags from this collection's images
      metadata.images.forEach(image => {
        image.tags.forEach(tag => allTags.add(tag));
      });
      
      // Store metadata with collection reference
      metadata.images.forEach(image => {
        image.collectionId = metadata.collection.id;
        image.collectionTitle = metadata.collection.title;
      });
      
      allMetadata = allMetadata.concat(metadata.images);
    } catch (error) {
      console.error(`Error loading ${collectionId}:`, error);
    }
  }
  
  console.log(`Loaded ${allMetadata.length} images with ${allTags.size} unique tags`);
}

/**
 * Render tag filter buttons
 */
function renderTagButtons() {
  const tagFilterContainer = document.getElementById('tag-filter');
  tagFilterContainer.innerHTML = '';
  
  // "All" button
  const allBtn = document.createElement('button');
  allBtn.className = 'tag-button all active';
  allBtn.textContent = 'All Images';
  allBtn.addEventListener('click', () => {
    selectedTags.clear();
    updateTagButtons();
    renderGalleries();
  });
  tagFilterContainer.appendChild(allBtn);
  
  // Sort tags alphabetically
  const sortedTags = Array.from(allTags).sort();
  
  sortedTags.forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'tag-button';
    btn.textContent = tag.replace('-', ' ');
    btn.dataset.tag = tag;
    
    btn.addEventListener('click', () => {
      if (selectedTags.has(tag)) {
        selectedTags.delete(tag);
      } else {
        selectedTags.add(tag);
      }
      updateTagButtons();
      renderGalleries();
    });
    
    tagFilterContainer.appendChild(btn);
  });
  
  updateTagButtons();
}

/**
 * Update visual state of tag buttons
 */
function updateTagButtons() {
  document.querySelectorAll('.tag-button').forEach(btn => {
    const tag = btn.dataset.tag;
    
    if (!tag) { // "All" button
      btn.classList.toggle('active', selectedTags.size === 0);
    } else {
      btn.classList.toggle('active', selectedTags.has(tag));
    }
  });
}

/**
 * Filter images based on selected tags
 * Returns images that have AT LEAST ONE of the selected tags
 */
function getFilteredImages() {
  if (selectedTags.size === 0) {
    return allMetadata; // Show all if no tags selected
  }
  
  return allMetadata.filter(image => {
    // Image matches if it has at least one of the selected tags
    return image.tags.some(tag => selectedTags.has(tag));
  });
}

/**
 * Group images by collection (for display)
 */
function groupByCollection(images) {
  const grouped = {};
  
  images.forEach(image => {
    if (!grouped[image.collectionId]) {
      grouped[image.collectionId] = {
        collectionTitle: image.collectionTitle,
        images: []
      };
    }
    grouped[image.collectionId].images.push(image);
  });
  
  return grouped;
}

/**
 * Render filtered galleries
 */
function renderGalleries() {
  const galleriesContainer = document.getElementById('browse-galleries');
  galleriesContainer.innerHTML = '';
  
  const filteredImages = getFilteredImages();
  
  if (filteredImages.length === 0) {
    galleriesContainer.innerHTML = `
      <div class="empty-state">
        <p>No images found matching these categories.</p>
      </div>
    `;
    return;
  }
  
  const grouped = groupByCollection(filteredImages);
  
  // Render each collection's images
  Object.keys(grouped).forEach(collectionId => {
    const { collectionTitle, images } = grouped[collectionId];
    
    const section = document.createElement('section');
    section.className = 'category-section';
    
    const heading = document.createElement('h3');
    heading.innerHTML = `
      ${collectionTitle}
      <span class="image-count">(${images.length} image${images.length !== 1 ? 's' : ''})</span>
    `;
    section.appendChild(heading);
    
    const gallery = document.createElement('div');
    gallery.className = 'gallery';
    
    images.forEach(image => {
      const figure = document.createElement('figure');
      
      const thumbPath = `assets/images/gallery/${image.collectionId}/thumbnails/${image.filename}`;
      const fullPath = `assets/images/gallery/${image.collectionId}/full-res/${image.filename}`;
      
      figure.innerHTML = `
        <img
          class="js-lightbox-trigger"
          src="${thumbPath}"
          data-full="${fullPath}"
          alt="${image.description}"
          data-title="${image.title}"
        />
        <figcaption>${image.title}</figcaption>
      `;
      
      gallery.appendChild(figure);
    });
    
    section.appendChild(gallery);
    galleriesContainer.appendChild(section);
  });
}
