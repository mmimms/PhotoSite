console.log("Photosite lightbox script loaded");
document.addEventListener("DOMContentLoaded", () => {
  const triggers = document.querySelectorAll(".js-lightbox-trigger");
  const lightbox = document.getElementById("lightbox");
  const lightboxImage = document.getElementById("lightbox-image");
  const lightboxCaption = document.getElementById("lightbox-caption");
  const closeBtn = document.querySelector(".lightbox-close");
  const backdrop = document.querySelector(".lightbox-backdrop");

  function openLightbox(img) {
    const fullSrc = img.dataset.full || img.src;
    lightboxImage.src = fullSrc;
    lightboxImage.alt = img.alt || "";
    lightboxCaption.textContent =
      img.closest("figure")?.querySelector("figcaption")?.textContent || "";
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
  }

  function closeLightbox() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImage.src = "";
  }

  triggers.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => openLightbox(img));
  });

  closeBtn.addEventListener("click", closeLightbox);
  backdrop.addEventListener("click", closeLightbox);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeLightbox();
    }
  });
});