document.addEventListener('comfy:node-data', (event) => {
    const data = event.detail;  // Data from Python node
    console.log('Node callback executed:', data);  // Debugging statement

    if (data && data.base64_images) {
        const imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = ''; // Clear previous images

        data.base64_images.forEach(imgData => {
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${imgData}`;
            img.style.maxWidth = '256px';
            img.style.maxHeight = '256px';
            imageContainer.appendChild(img);
        });
    } else {
        document.getElementById('image-container').innerHTML = "No images yet.";
    }
});

// Debugging statement to confirm JS is loaded
console.log('Play1.js loaded');
