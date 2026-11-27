/**
 * FaceStyle AI - Interactive Client-Side JavaScript
 * Controls: Live webcam streaming, snapshot capture, drag & drop previews,
 * AJAX bookmarking, and AI scanning animation.
 */

document.addEventListener('DOMContentLoaded', () => {
    initCameraCapture();
    initFileUploadPreview();
    initFavouriteButtons();
    initAnalysisSubmission();
    initImageToggle();
});

// ==============================================================================
// 1. LIVE WEBCAM CAPTURE LOGIC
// ==============================================================================
let mediaStream = null;

function initCameraCapture() {
    const video = document.getElementById('webcam-video');
    const canvas = document.getElementById('webcam-canvas');
    const startBtn = document.getElementById('btn-start-camera');
    const snapBtn = document.getElementById('btn-snap-photo');
    const retakeBtn = document.getElementById('btn-retake-photo');
    const webcamDataInput = document.getElementById('id_webcam_image_data');
    const cameraStatus = document.getElementById('camera-status');
    const cameraPreviewCard = document.getElementById('camera-preview-card');

    if (!startBtn || !video) return;

    startBtn.addEventListener('click', async () => {
        try {
            cameraStatus.innerHTML = '<span class="text-primary"><i class="fas fa-spinner fa-spin me-2"></i>Accessing camera...</span>';
            mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
                audio: false
            });
            video.srcObject = mediaStream;
            video.play();
            cameraStatus.innerHTML = '<span class="text-success"><i class="fas fa-check-circle me-1"></i>Camera Active - Align your face inside the frame</span>';
            startBtn.classList.add('d-none');
            snapBtn.classList.remove('d-none');
        } catch (err) {
            cameraStatus.innerHTML = `<span class="text-danger"><i class="fas fa-exclamation-triangle me-1"></i>Camera Access Error: ${err.message}. Please allow camera permissions in your browser.</span>`;
        }
    });

    if (snapBtn) {
        snapBtn.addEventListener('click', () => {
            if (!video.videoWidth) return;

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Export to base64 JPEG
            const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
            webcamDataInput.value = dataUrl;

            // Pause video and show frozen canvas
            video.classList.add('d-none');
            canvas.classList.remove('d-none');
            snapBtn.classList.add('d-none');
            retakeBtn.classList.remove('d-none');
            cameraStatus.innerHTML = '<span class="text-success"><i class="fas fa-camera me-1"></i>Snapshot captured! Click "Analyze My Face" below to proceed.</span>';

            // Clear any previously uploaded file selection
            const fileInput = document.getElementById('id_image_file');
            if (fileInput) fileInput.value = '';
        });
    }

    if (retakeBtn) {
        retakeBtn.addEventListener('click', () => {
            webcamDataInput.value = '';
            canvas.classList.add('d-none');
            video.classList.remove('d-none');
            retakeBtn.classList.add('d-none');
            snapBtn.classList.remove('d-none');
            cameraStatus.innerHTML = '<span class="text-info"><i class="fas fa-info-circle me-1"></i>Ready for a new snapshot.</span>';
        });
    }

    // Stop camera when user switches tab to file upload
    const fileTab = document.getElementById('tab-upload-file');
    if (fileTab) {
        fileTab.addEventListener('click', () => {
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
                mediaStream = null;
                startBtn.classList.remove('d-none');
                snapBtn.classList.add('d-none');
                retakeBtn.classList.add('d-none');
                if (video) video.classList.remove('d-none');
                if (canvas) canvas.classList.add('d-none');
                cameraStatus.innerHTML = '<span class="text-muted">Camera stopped.</span>';
            }
        });
    }
}

// ==============================================================================
// 2. DRAG AND DROP FILE PREVIEW
// ==============================================================================
function initFileUploadPreview() {
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('id_image_file');
    const previewContainer = document.getElementById('file-preview-container');
    const previewImg = document.getElementById('file-preview-img');
    const removeFileBtn = document.getElementById('btn-remove-file');
    const webcamDataInput = document.getElementById('id_webcam_image_data');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect(fileInput.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelect(fileInput.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file.type.match('image.*')) {
            alert('Please select a valid image file (JPG, JPEG, PNG).');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImg) previewImg.src = e.target.result;
            if (previewContainer) previewContainer.classList.remove('d-none');
            dropzone.classList.add('d-none');
            // Clear webcam hidden input
            if (webcamDataInput) webcamDataInput.value = '';
        };
        reader.readAsDataURL(file);
    }

    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', () => {
            fileInput.value = '';
            if (previewContainer) previewContainer.classList.add('d-none');
            dropzone.classList.remove('d-none');
        });
    }
}

// ==============================================================================
// 3. AJAX FAVORITES BOOKMARKING
// ==============================================================================
function initFavouriteButtons() {
    document.querySelectorAll('.btn-fav-toggle').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const hairstyleId = btn.dataset.hairstyleId;
            const url = `/hairstyles/${hairstyleId}/favourite/?format=json`;

            try {
                const response = await fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();

                if (data.status === 'success') {
                    if (data.is_favourite) {
                        btn.classList.add('active');
                        btn.innerHTML = '<i class="fas fa-heart text-danger"></i>';
                    } else {
                        btn.classList.remove('active');
                        btn.innerHTML = '<i class="far fa-heart"></i>';
                    }
                    showToastNotification(data.message);
                }
            } catch (err) {
                // If not authenticated, standard redirect to login
                window.location.href = `/login/?next=${window.location.pathname}`;
            }
        });
    });
}

function showToastNotification(message) {
    let toast = document.getElementById('facestyle-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'facestyle-toast';
        toast.style.position = 'fixed';
        toast.style.bottom = '25px';
        toast.style.right = '25px';
        toast.style.background = '#230843';
        toast.style.color = '#fff';
        toast.style.padding = '12px 24px';
        toast.style.borderRadius = '30px';
        toast.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3)';
        toast.style.zIndex = '9999';
        toast.style.transition = 'all 0.3s ease';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fas fa-sparkles me-2 text-warning"></i> ${message}`;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
    }, 2800);
}

// ==============================================================================
// 4. ANIMATED SCANNER TRIGGER
// ==============================================================================
function initAnalysisSubmission() {
    const form = document.getElementById('analysis-form');
    const submitBtn = document.getElementById('btn-analyze-submit');
    const loadingBanner = document.getElementById('loading-analysis-banner');
    const scannerOverlay = document.querySelectorAll('.scanner-overlay');

    if (!form || !submitBtn) return;

    form.addEventListener('submit', () => {
        const fileInput = document.getElementById('id_image_file');
        const webcamInput = document.getElementById('id_webcam_image_data');

        if ((!fileInput || !fileInput.files.length) && (!webcamInput || !webcamInput.value)) {
            alert('Please select an image file or capture a photo first.');
            return false;
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin me-2"></i> Analyzing Face Proportions...';
        if (loadingBanner) loadingBanner.classList.remove('d-none');
        scannerOverlay.forEach(el => el.style.display = 'block');
    });
}

// ==============================================================================
// 5. LANDMARK VISUALIZATION TOGGLE (RESULT PAGE)
// ==============================================================================
function initImageToggle() {
    const toggleBtn = document.getElementById('btn-toggle-landmarks');
    const originalImg = document.getElementById('img-original-photo');
    const annotatedImg = document.getElementById('img-annotated-photo');

    if (!toggleBtn || !originalImg || !annotatedImg) return;

    toggleBtn.addEventListener('click', () => {
        if (annotatedImg.classList.contains('d-none')) {
            annotatedImg.classList.remove('d-none');
            originalImg.classList.add('d-none');
            toggleBtn.innerHTML = '<i class="fas fa-eye-slash me-2"></i> View Clean Photo';
        } else {
            annotatedImg.classList.add('d-none');
            originalImg.classList.remove('d-none');
            toggleBtn.innerHTML = '<i class="fas fa-chart-network me-2"></i> View AI Landmarks';
        }
    });
}
