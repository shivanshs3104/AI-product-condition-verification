let uploadArea;
let fileInput;
let resultsSection;

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    uploadArea = document.querySelector('.upload-area');
    resultsSection = document.querySelector('.results-placeholder');
    createFileInput();
    setupEventListeners();
}

function createFileInput() {
    fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
}

function setupEventListeners() {
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', handleFileSelect);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (file && file.type.startsWith('image/')) {
        resultsSection.innerHTML = '<p>✅ Image uploaded: ' + file.name + '</p>';
    } else {
        alert('Please select a valid image file');
    }
}
