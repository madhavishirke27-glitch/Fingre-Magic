"""
FaceStyle AI - Face Detection and Landmark Extraction Engine
Uses Google MediaPipe Face Landmarker with OpenCV Visualization.
"""
import os
import cv2
import numpy as np
from PIL import Image
from django.conf import settings
from .measurements import (
    LANDMARK_INDICES,
    calculate_face_measurements,
    classify_face_shape,
    FACE_SHAPE_DETAILS
)

# Locate the MediaPipe Face Landmarker model asset
MODEL_PATH = os.path.join(
    settings.BASE_DIR, 'ai_engine', 'models', 'face_landmarker.task'
)

# Cached FaceLandmarker instance
_DETECTOR_INSTANCE = None


def get_face_landmarker():
    """Initializes or returns cached MediaPipe FaceLandmarker."""
    global _DETECTOR_INSTANCE
    if _DETECTOR_INSTANCE is not None:
        return _DETECTOR_INSTANCE

    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"MediaPipe Face Landmarker model not found at {MODEL_PATH}")

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_faces=3,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_face_blendshapes=False
    )
    _DETECTOR_INSTANCE = vision.FaceLandmarker.create_from_options(options)
    return _DETECTOR_INSTANCE


def extract_landmarks(face_landmarks_list, img_width, img_height):
    """
    Extracts normalized and pixel landmark dictionaries from MediaPipe results.
    """
    normalized_dict = {}
    pixel_dict = {}

    for idx, lm in enumerate(face_landmarks_list):
        normalized_dict[idx] = {'x': lm.x, 'y': lm.y, 'z': getattr(lm, 'z', 0.0)}
        pixel_dict[idx] = {
            'x': int(lm.x * img_width),
            'y': int(lm.y * img_height),
            'z': getattr(lm, 'z', 0.0)
        }

    return normalized_dict, pixel_dict


def generate_annotated_image(bgr_image, pixel_dict, measurements, face_shape):
    """
    Generates a high-tech glowing landmark overlay visualization for the viva demonstration.
    Draws facial perimeter mesh points and measurement calipers in lavender/soft-pink.
    """
    annotated = bgr_image.copy()
    h, w, _ = annotated.shape

    # Accent colors in BGR
    soft_pink = (151, 117, 255)       # #FF7597 in BGR -> (151, 117, 255)
    lavender = (255, 170, 224)        # #E0AAFF in BGR -> (255, 170, 224)
    neon_violet = (191, 44, 123)      # #7B2CBF in BGR -> (191, 44, 123)
    cyan_accent = (235, 206, 135)     # #87CEEB in BGR -> (235, 206, 135)

    # 1. Draw glowing key landmark points
    key_indices = [
        LANDMARK_INDICES['forehead_top'],
        LANDMARK_INDICES['chin_bottom'],
        LANDMARK_INDICES['left_cheek'],
        LANDMARK_INDICES['right_cheek'],
        LANDMARK_INDICES['left_temple'],
        LANDMARK_INDICES['right_temple'],
        LANDMARK_INDICES['left_jaw_angle'],
        LANDMARK_INDICES['right_jaw_angle'],
        LANDMARK_INDICES['nose_tip']
    ]

    # Draw semi-transparent mesh overlay for facial contour
    contour_indices = [
        10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
        397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
        172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109, 10
    ]

    overlay = annotated.copy()
    for i in range(len(contour_indices) - 1):
        idx1 = contour_indices[i]
        idx2 = contour_indices[i + 1]
        if idx1 in pixel_dict and idx2 in pixel_dict:
            pt1 = (pixel_dict[idx1]['x'], pixel_dict[idx1]['y'])
            pt2 = (pixel_dict[idx2]['x'], pixel_dict[idx2]['y'])
            cv2.line(overlay, pt1, pt2, neon_violet, 2, cv2.LINE_AA)

    # 2. Draw Measurement Calipers (Length, Cheek, Forehead, Jaw)
    # Face Length Caliper (Forehead to Chin)
    p_fh = (pixel_dict[10]['x'], pixel_dict[10]['y'])
    p_ch = (pixel_dict[152]['x'], pixel_dict[152]['y'])
    cv2.line(overlay, p_fh, p_ch, lavender, 2, cv2.LINE_AA)

    # Cheekbone Width Caliper (Right Cheek to Left Cheek)
    p_rc = (pixel_dict[234]['x'], pixel_dict[234]['y'])
    p_lc = (pixel_dict[454]['x'], pixel_dict[454]['y'])
    cv2.line(overlay, p_rc, p_lc, soft_pink, 2, cv2.LINE_AA)

    # Forehead Width Caliper
    p_rt = (pixel_dict[103]['x'], pixel_dict[103]['y'])
    p_lt = (pixel_dict[332]['x'], pixel_dict[332]['y'])
    cv2.line(overlay, p_rt, p_lt, cyan_accent, 2, cv2.LINE_AA)

    # Jaw Width Caliper
    p_rj = (pixel_dict[58]['x'], pixel_dict[58]['y'])
    p_lj = (pixel_dict[288]['x'], pixel_dict[288]['y'])
    cv2.line(overlay, p_rj, p_lj, (140, 200, 255), 2, cv2.LINE_AA)

    # Blend overlay with original image
    cv2.addWeighted(overlay, 0.45, annotated, 0.55, 0, annotated)

    # Draw solid key landmark circles on top
    for idx in key_indices:
        if idx in pixel_dict:
            pt = (pixel_dict[idx]['x'], pixel_dict[idx]['y'])
            cv2.circle(annotated, pt, 5, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(annotated, pt, 7, soft_pink, 2, cv2.LINE_AA)

    # Draw result watermark tag
    tag_text = f"FaceStyle AI: {face_shape} Shape (L/W: {measurements['length_to_width_ratio']})"
    cv2.rectangle(annotated, (15, h - 45), (min(w - 15, 480), h - 15), (20, 10, 40), -1)
    cv2.putText(annotated, tag_text, (25, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

    return annotated


def detect_face_and_analyze(image_input, save_annotated=True):
    """
    Main AI engine function.
    image_input: file path, bytes, or numpy array.
    Returns:
        {
            'success': True/False,
            'error_message': None or str,
            'face_count': int,
            'measurements': dict,
            'classification': dict,
            'annotated_image_path': str or None,
            'annotated_image_filename': str or None
        }
    """
    import mediapipe as mp

    # 1. Load image into OpenCV BGR format
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            return {'success': False, 'error_message': 'Image file not found.', 'face_count': 0}
        img_bgr = cv2.imread(image_input)
    elif isinstance(image_input, np.ndarray):
        img_bgr = image_input
    elif hasattr(image_input, 'read'):
        file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    else:
        return {'success': False, 'error_message': 'Unsupported image input format.', 'face_count': 0}

    if img_bgr is None or img_bgr.size == 0:
        return {'success': False, 'error_message': 'Unable to decode image. Please upload a valid JPG or PNG file.', 'face_count': 0}

    h, w, _ = img_bgr.shape
    if h < 80 or w < 80:
        return {'success': False, 'error_message': 'Image resolution is too low for accurate landmark analysis.', 'face_count': 0}

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    # 2. Run MediaPipe Landmarker
    try:
        landmarker = get_face_landmarker()
        detection_result = landmarker.detect(mp_image)
    except Exception as e:
        return {'success': False, 'error_message': f'AI Landmark detection initialization error: {str(e)}', 'face_count': 0}

    face_count = len(detection_result.face_landmarks)

    # 3. Handle 0 faces or multiple faces
    if face_count == 0:
        return {
            'success': False,
            'error_message': 'No face detected in the image. Please upload a well-lit photo where your face is clearly visible and facing the camera.',
            'face_count': 0
        }
    elif face_count > 1:
        return {
            'success': False,
            'error_message': f'Detected {face_count} faces. For accurate hairstyle recommendation, please upload a photograph containing only one person.',
            'face_count': face_count
        }

    # 4. Extract landmarks for the detected face
    face_landmarks = detection_result.face_landmarks[0]
    normalized_dict, pixel_dict = extract_landmarks(face_landmarks, w, h)

    # 5. Calculate geometric measurements
    measurements = calculate_face_measurements(normalized_dict, img_width=w, img_height=h)

    # 6. Classify face shape
    classification = classify_face_shape(measurements)

    # 7. Generate Annotated Visualization
    annotated_rel_path = None
    annotated_filename = None
    if save_annotated:
        import uuid
        annotated_bgr = generate_annotated_image(img_bgr, pixel_dict, measurements, classification['face_shape'])
        annotated_filename = f"annotated_{uuid.uuid4().hex[:10]}.jpg"
        annotated_dir = os.path.join(settings.MEDIA_ROOT, 'annotated')
        os.makedirs(annotated_dir, exist_ok=True)
        annotated_abs_path = os.path.join(annotated_dir, annotated_filename)
        cv2.imwrite(annotated_abs_path, annotated_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        annotated_rel_path = f"annotated/{annotated_filename}"

    return {
        'success': True,
        'error_message': None,
        'face_count': 1,
        'measurements': measurements,
        'classification': classification,
        'annotated_image_path': annotated_abs_path if save_annotated else None,
        'annotated_image_rel_url': f"{settings.MEDIA_URL}{annotated_rel_path}" if annotated_rel_path else None,
        'annotated_image_filename': annotated_filename
    }
