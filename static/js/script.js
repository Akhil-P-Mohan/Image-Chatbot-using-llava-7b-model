function showImagePreview(event) {
  const imagePreview = document.getElementById('image-preview');
  imagePreview.innerHTML = ""; // Clear previous preview
  
  const file = event.target.files[0];
  if (file) {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.alt = "Uploaded Image Preview";
    img.classList.add('preview-image'); // Apply CSS for styling
    imagePreview.appendChild(img);
  }
}
document.getElementById('image-upload').addEventListener('change', showImagePreview);