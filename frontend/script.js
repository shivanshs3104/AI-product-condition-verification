// Global variables
let uploadArea;
let fileInput;
let resultsSection;
let imagePreview;
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB in bytes

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    uploadArea = document.querySelector('.upload-area');
    resultsSection = document.querySelector('.results-placeholder');
    imagePreview = document.querySelector('.image-preview');
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
    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File selection handler
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function processFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('❌ Please select a valid image file (JPG, PNG, GIF, etc.)');
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        showError(`❌ File too large (${sizeMB}MB). Maximum size is 5MB.`);
        return;
    }
    
    // Show loading state
    showLoading();
    
    // Read and display image
    const reader = new FileReader();
    reader.onload = function(e) {
        displayImagePreview(e.target.result, file);
    };
    reader.readAsDataURL(file);
}

function showLoading() {
    resultsSection.innerHTML = '<p class="loading">⏳ Processing image...</p>';
    imagePreview.innerHTML = '';
}

function displayImagePreview(imageData, file) {
    // Create image element
    const img = document.createElement('img');
    img.src = imageData;
    img.alt = 'Uploaded product image';
    
    // Create info container
    const info = document.createElement('div');
    info.className = 'preview-info';
    
    const fileName = document.createElement('p');
    fileName.innerHTML = `<strong>📁 File:</strong> ${file.name}`;
    
    const fileSize = document.createElement('p');
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    fileSize.innerHTML = `<strong>📊 Size:</strong> ${sizeMB} MB`;
    
    const fileType = document.createElement('p');
    fileType.innerHTML = `<strong>🖼️ Type:</strong> ${file.type}`;
    
    info.appendChild(fileName);
    info.appendChild(fileSize);
    info.appendChild(fileType);
    
    // Clear and update preview
    imagePreview.innerHTML = '';
    imagePreview.appendChild(img);
    imagePreview.appendChild(info);
    
    // Show success message
    resultsSection.innerHTML = `
        <div class="success-message">
            <h3>✅ Image Uploaded Successfully!</h3>
            <p>Your image has been processed and is ready for verification.</p>
            <button class="analyze-btn" onclick="analyzeImage()">🔍 Analyze Product Condition</button>
        </div>
    `;
}

function analyzeImage() {
    // Simulate analysis process
    resultsSection.innerHTML = `
        <div class="analyzing">
            <div class="spinner"></div>
            <h3>🤖 AI Analysis in Progress...</h3>
            <p>Analyzing product condition, scratches, damages, and quality...</p>
        </div>
    `;
    
    // Simulate API call with timeout
    setTimeout(showAnalysisResults, 3000);
}

function showAnalysisResults() {
    resultsSection.innerHTML = `
        <div class="analysis-results">
            <h3>📊 Analysis Results</h3>
            <div class="result-card">
                <div class="result-header">
                    <span class="status-badge good">Excellent Condition</span>
                    <span class="confidence">95% Confidence</span>
                </div>
                <div class="result-details">
                    <div class="detail-item">
                        <span class="label">Overall Quality:</span>
                        <span class="value">9.5/10</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Scratches Detected:</span>
                        <span class="value">None</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Damage Level:</span>
                        <span class="value">0%</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Authenticity:</span>
                        <span class="value">Verified ✓</span>
                    </div>
                </div>
                <p class="result-note">
                    💡 <strong>Note:</strong> This is a simulated result. Full AI integration coming soon!
                </p>
            </div>
        </div>
    `;
}

function showError(message) {
    resultsSection.innerHTML = `<p class="error-message">${message}</p>`;
    imagePreview.innerHTML = '';
}
