"use strict";

const imageInput = document.getElementById("image-input");
const dropzone = document.getElementById("dropzone");
const placeholder = document.getElementById("upload-placeholder");
const preview = document.getElementById("image-preview");
const changeImage = document.getElementById("change-image");
const fileDetails = document.getElementById("file-details");
const fileName = document.getElementById("file-name");
const fileSize = document.getElementById("file-size");
const uploadError = document.getElementById("upload-error");
const analyzeButton = document.getElementById("analyze-button");
const resultContent = document.getElementById("result-content");
const resultStatus = document.getElementById("result-status");
const resultHeading = document.getElementById("result-heading");
const resultDescription = document.getElementById("result-description");

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
let selectedFile = null;
let previewUrl = null;
let selectionVersion = 0;
let dragDepth = 0;

function clearError() {
  uploadError.hidden = true;
  uploadError.textContent = "";
  imageInput.removeAttribute("aria-invalid");
}

function showError(message) {
  uploadError.textContent = message;
  uploadError.hidden = false;
  imageInput.setAttribute("aria-invalid", "true");
}

function updateResult(status, heading, description, ready = false) {
  resultStatus.textContent = status;
  resultHeading.textContent = heading;
  resultDescription.textContent = description;
  resultContent.classList.toggle("is-ready", ready);
}

function formatSize(bytes) {
  if (bytes < 1024 * 1024) {
    return `${Math.max(1, Math.round(bytes / 1024))} Ko`;
  }
  return `${(bytes / (1024 * 1024)).toLocaleString("fr-FR", { maximumFractionDigits: 1 })} Mo`;
}

function selectImage(file) {
  const version = ++selectionVersion;
  clearError();
  analyzeButton.disabled = !selectedFile;

  if (!file) return;

  const supported = ACCEPTED_TYPES.has(file.type.toLowerCase())
    || (!file.type && /\.(jpe?g|png|webp)$/i.test(file.name));

  if (!supported) {
    showError("Choisissez une image au format JPG, PNG ou WebP.");
    imageInput.value = "";
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    showError("Cette image dépasse 10 Mo. Choisissez une image plus légère.");
    imageInput.value = "";
    return;
  }

  const candidateUrl = URL.createObjectURL(file);
  const candidateImage = new Image();
  analyzeButton.disabled = true;

  candidateImage.onload = () => {
    if (version !== selectionVersion) {
      URL.revokeObjectURL(candidateUrl);
      return;
    }

    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = candidateUrl;
    selectedFile = file;
    preview.src = previewUrl;
    preview.alt = `Aperçu de ${file.name}`;
    preview.hidden = false;
    placeholder.hidden = true;
    changeImage.hidden = false;
    fileDetails.hidden = false;
    dropzone.classList.add("has-image");
    fileName.textContent = file.name;
    fileName.title = file.name;
    fileSize.textContent = `${formatSize(file.size)} · ${candidateImage.naturalWidth} × ${candidateImage.naturalHeight} px`;
    analyzeButton.disabled = false;
    updateResult(
      "Image ajoutée",
      "Votre image est prête.",
      "Vous pouvez la remplacer ou la retirer à tout moment. L’analyse sera disponible prochainement.",
      true,
    );
  };

  candidateImage.onerror = () => {
    URL.revokeObjectURL(candidateUrl);
    if (version !== selectionVersion) return;
    imageInput.value = "";
    analyzeButton.disabled = !selectedFile;
    showError("Cette image ne peut pas être ouverte. Essayez un autre fichier.");
  };

  candidateImage.src = candidateUrl;
}

function resetSelection() {
  selectionVersion++;
  clearError();
  selectedFile = null;
  imageInput.value = "";
  preview.removeAttribute("src");
  preview.hidden = true;
  preview.alt = "Aperçu de l’image sélectionnée";
  placeholder.hidden = false;
  changeImage.hidden = true;
  fileDetails.hidden = true;
  fileName.textContent = "";
  fileName.removeAttribute("title");
  fileSize.textContent = "";
  dropzone.classList.remove("has-image");
  analyzeButton.disabled = true;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  updateResult(
    "En attente d’une image",
    "Qu’allez-vous découvrir ?",
    "Ajoutez une image pour commencer. Sa catégorie et son score de confiance trouveront leur place ici.",
  );
}

imageInput.addEventListener("change", () => {
  if (imageInput.files.length) selectImage(imageInput.files[0]);
});

document.getElementById("remove-image").addEventListener("click", () => {
  resetSelection();
  imageInput.focus();
});

dropzone.addEventListener("dragenter", (event) => {
  event.preventDefault();
  dragDepth++;
  dropzone.classList.add("is-dragging");
});

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  if (event.dataTransfer) event.dataTransfer.dropEffect = "copy";
});

dropzone.addEventListener("dragleave", (event) => {
  event.preventDefault();
  dragDepth = Math.max(0, dragDepth - 1);
  if (dragDepth === 0) dropzone.classList.remove("is-dragging");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dragDepth = 0;
  dropzone.classList.remove("is-dragging");
  const files = event.dataTransfer?.files;
  if (!files?.length) return;
  if (files.length > 1) {
    showError("Ajoutez une seule image à la fois.");
    return;
  }
  selectImage(files[0]);
});

// Prevent the browser from navigating away when a file is dropped outside the zone.
for (const eventName of ["dragover", "drop"]) {
  window.addEventListener(eventName, (event) => {
    if (Array.from(event.dataTransfer?.types ?? []).includes("Files")) event.preventDefault();
  });
}

document.getElementById("prediction-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!selectedFile || analyzeButton.disabled) return;

  // Prediction will be connected to the Python server in the next step.
  // Keep this state explicit instead of displaying a simulated prediction.
  updateResult(
    "Analyse bientôt disponible",
    "Votre image est bien préparée.",
    "La reconnaissance n’est pas encore disponible. Vous pouvez déjà essayer d’autres images et vérifier leur aperçu.",
    true,
  );
});

window.addEventListener("pagehide", () => {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
});
