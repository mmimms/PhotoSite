/**
 * Lightbox functionality for image galleries
 * Handles click events on gallery images and displays them in a modal overlay
 * Uses event delegation to support both static and dynamically-created images
 */

document.addEventListener("DOMContentLoaded", () => {
  const lightbox = document.getElementById("lightbox");
  const lightboxImage = document.getElementById("lightbox-image");
  const lightboxCaption = document.getElementById("lightbox-caption");
  const closeBtn = document.querySelector(".lightbox-close");
  const backdrop = document.querySelector(".lightbox-backdrop");

  /**
   * Opens the lightbox with the clicked image
   */
  function openLightbox(img) {
    const fullSrc = img.dataset.full || img.src;
    const title = img.dataset.title || img.alt || "";
    
    lightboxImage.src = fullSrc;
    lightboxImage.alt = img.alt || "";
    lightboxCaption.textContent = title;
    
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    
    // Prevent body scroll when lightbox is open
    document.body.style.overflow = "hidden";
  }

  /**
   * Closes the lightbox
   */
  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImage.src = "";
    
    // Re-enable body scroll
    document.body.style.overflow = "";
  }

  /**
   * Event delegation: Listen for clicks on the document
   * Check if clicked element is a lightbox trigger
   * This works for both static and dynamically-created images
   */
  document.addEventListener("click", (event) => {
    const trigger = event.target.closest(".js-lightbox-trigger");
    
    if (trigger) {
      event.preventDefault();
      trigger.style.cursor = "zoom-in";
      openLightbox(trigger);
    }
  });

  /**
   * Lightbox close triggers
   */
  closeBtn.addEventListener("click", closeLightbox);
  backdrop.addEventListener("click", closeLightbox);

  /**
   * Keyboard navigation (Escape to close)
   */
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
      closeLightbox();
    }
  });
});
