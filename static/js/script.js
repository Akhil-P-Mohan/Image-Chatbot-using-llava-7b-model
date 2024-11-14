// Function to show image preview and scroll chat output
function showImagePreview(event) {
    const imagePreview = document.getElementById('image-preview');
    const chatOutput = document.getElementById('chatOutput');

    imagePreview.innerHTML = ""; // Clear previous preview

    const file = event.target.files[0];
    if (file) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.alt = "Uploaded Image Preview";
        img.classList.add('preview-image'); // Apply CSS for styling
        imagePreview.appendChild(img);
    }

    // Scroll to the bottom of the chat output
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

// Event listener for image upload
document.getElementById('image-upload').addEventListener('change', showImagePreview);