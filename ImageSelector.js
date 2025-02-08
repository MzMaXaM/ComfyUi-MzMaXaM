function createImageGrid(images, previewPaths) {
    const container = document.createElement('div');
    container.style.display = 'grid';
    container.style.gridTemplateColumns = 'repeat(auto-fit, minmax(100px, 1fr))';
    container.style.gap = '5px';

    console.log('Creating image grid...');  // Debugging statement

    previewPaths.forEach((path, index) => {
        console.log('Preview image path:', path);  // Debugging statement
        const link = document.createElement('a');
        link.href = path;
        link.target = '_blank';

        const imgElement = document.createElement('img');
        imgElement.src = path;
        imgElement.style.maxWidth = '100%';
        imgElement.style.cursor = 'pointer';

        imgElement.addEventListener('click', () => {
            const selectedIndexInput = document.getElementById('selected_index');
            if (selectedIndexInput) {
                selectedIndexInput.value = index;
                selectedIndexInput.dispatchEvent(new Event('change'));
            }
        });

        link.appendChild(imgElement);
        container.appendChild(link);
    });

    console.log(container);  // Debugging statement
    return container;
}

function nodeCallback(node, inputData) {
    console.log('Node callback executed:', inputData);  // Debugging statement
    if (inputData && inputData.images && inputData.preview_paths) {
        const images = inputData.images;
        const previewPaths = inputData.preview_paths;
        const previewArea = document.getElementById('image_preview');
        if (previewArea) {
            previewArea.innerHTML = '';
            const grid = createImageGrid(images, previewPaths);
            previewArea.appendChild(grid);
            console.log('Grid appended to preview area');  // Debugging statement
        }
        console.log('Preview paths:', previewPaths);  // Debugging statement
    }
}
