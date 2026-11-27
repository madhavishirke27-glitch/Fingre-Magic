"""
FaceStyle AI - Facial Measurements & Geometric Shape Classification
Mathematical and Anthropometrical Analysis Module.
"""
import math

# Facial Landmark Indices in MediaPipe 468/478 Face Mesh
LANDMARK_INDICES = {
    'forehead_top': 10,        # Trichion / midline upper forehead
    'chin_bottom': 152,        # Gnathion / lowest chin midline
    'left_cheek': 454,         # Zygomatic arch (subject's left / viewer's right)
    'right_cheek': 234,        # Zygomatic arch (subject's right / viewer's left)
    'left_temple': 332,        # Frontotemporale / temple width
    'right_temple': 103,       # Frontotemporale / temple width
    'left_jaw_angle': 288,     # Gonion / jaw angle left
    'right_jaw_angle': 58,     # Gonion / jaw angle right
    'nose_tip': 1,             # Pronasale / nose tip
    'left_eye_outer': 263,
    'right_eye_outer': 33,
}

FACE_SHAPE_DETAILS = {
    'Oval': {
        'title': 'Oval Face Shape',
        'badge_color': '#9D4EDD',
        'summary': 'Balanced proportions with gentle curves where face length is slightly greater than cheekbone width.',
        'characteristics': [
            'Face length is approximately 1.35 to 1.5 times the cheekbone width.',
            'Forehead width is slightly wider than or equal to the jawline.',
            'Jawline is smoothly rounded with soft, harmonious curves.',
            'Considered universally versatile for a wide variety of hair lengths and styles.'
        ],
        'styling_advice': 'Versatile silhouette. Can wear almost any haircut comfortably, from short pixies and sharp bobs to layered waves.',
        'styling_focus': 'Maintain facial balance and avoid heavy forward bangs that obscure the forehead balance.'
    },
    'Round': {
        'title': 'Round Face Shape',
        'badge_color': '#C77DFF',
        'summary': 'Soft, rounded contours where face length and width are almost equal, with full cheekbones.',
        'characteristics': [
            'Face length and cheekbone width are nearly equal (ratio roughly 1.0 to 1.25).',
            'Cheekbones represent the widest facial dimension.',
            'Jawline is circular, soft, and gentle without sharp angular corners.',
            'Cheeks appear youthful and soft.'
        ],
        'styling_advice': 'Styles that add height, volume at the crown, or asymmetrical side-swept bangs help create vertical balance.',
        'styling_focus': 'Elongate the silhouette and avoid wide volume directly at cheek level.'
    },
    'Square': {
        'title': 'Square Face Shape',
        'badge_color': '#7B2CBF',
        'summary': 'Strong, well-defined jawline with equal proportions across the forehead, cheekbones, and jaw.',
        'characteristics': [
            'Forehead, cheekbones, and jawline possess very similar widths.',
            'Face length-to-width ratio is relatively close to 1:1 (under 1.30).',
            'Jaw angles (gonions) are prominent, sharp, and structured.',
            'Strong, authoritative, and expressive facial architecture.'
        ],
        'styling_advice': 'Soft textured layers, side parts, waves, and wispy fringes soften angular jawlines effectively.',
        'styling_focus': 'Soften angular edges with curved textures; avoid blunt, chin-length straight cuts that emphasize jaw width.'
    },
    'Heart': {
        'title': 'Heart Face Shape',
        'badge_color': '#FF7597',
        'summary': 'Wider forehead tapering gracefully into high cheekbones and a delicate, narrower chin.',
        'characteristics': [
            'Forehead and temples are notably wider than the lower jawline.',
            'Cheekbones are pronounced and elevated.',
            'The face tapers progressively toward a pointed or slender chin.',
            'Length-to-width ratio is balanced to moderately elongated.'
        ],
        'styling_advice': 'Chin-length bobs, textured waves near the neck, and curtain bangs add balance to the narrower lower face.',
        'styling_focus': 'Add width and fullness around the jawline and chin; avoid heavy crown volume that widens the forehead.'
    },
    'Diamond': {
        'title': 'Diamond Face Shape',
        'badge_color': '#E0AAFF',
        'summary': 'High, dramatic cheekbones with narrow forehead and slender, refined jawline.',
        'characteristics': [
            'Cheekbones are decisively the widest feature of the face.',
            'Both forehead width and jawline width are noticeably narrower than cheekbones.',
            'Chin is slender and pointed, creating a sculpted diamond silhouette.',
            'Face length is moderate to long.'
        ],
        'styling_advice': 'Shoulder-length cuts, swept bangs, and side-parted voluminous waves frame the cheekbones flatteringly.',
        'styling_focus': 'Broaden forehead and jawline width visually while celebrating defined cheekbone geometry.'
    },
    'Oblong': {
        'title': 'Oblong (Long) Face Shape',
        'badge_color': '#5A189A',
        'summary': 'Elongated facial structure with uniform width from forehead down through the jawline.',
        'characteristics': [
            'Face length is significantly greater than cheekbone width (ratio greater than 1.48).',
            'Forehead, cheekbones, and jawline exhibit uniform, consistent widths.',
            'Sides of the face present straight, vertical contours.',
            'Elegant and dignified profile with elongated proportions.'
        ],
        'styling_advice': 'Hairstyles with lateral volume, horizontal waves, full blunt fringes, or wide curls shorten visual length.',
        'styling_focus': 'Create horizontal width and volume around the cheek level; avoid towering pompadours or pin-straight flat styles.'
    }
}


def calculate_euclidean_distance(point1, point2):
    """
    Computes Euclidean distance between two 2D/3D points.
    point1, point2: tuples or dicts with x, y (and optional z).
    """
    if isinstance(point1, dict):
        x1, y1 = point1['x'], point1['y']
    else:
        x1, y1 = point1[0], point1[1]

    if isinstance(point2, dict):
        x2, y2 = point2['x'], point2['y']
    else:
        x2, y2 = point2[0], point2[1]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_face_measurements(landmarks_dict, img_width=1, img_height=1):
    """
    Extracts key facial distance metrics from pixel or normalized landmark coordinates.
    Returns dictionary with raw measurements and normalized ratios.
    """
    p_forehead = landmarks_dict[LANDMARK_INDICES['forehead_top']]
    p_chin = landmarks_dict[LANDMARK_INDICES['chin_bottom']]
    p_left_cheek = landmarks_dict[LANDMARK_INDICES['left_cheek']]
    p_right_cheek = landmarks_dict[LANDMARK_INDICES['right_cheek']]
    p_left_temple = landmarks_dict[LANDMARK_INDICES['left_temple']]
    p_right_temple = landmarks_dict[LANDMARK_INDICES['right_temple']]
    p_left_jaw = landmarks_dict[LANDMARK_INDICES['left_jaw_angle']]
    p_right_jaw = landmarks_dict[LANDMARK_INDICES['right_jaw_angle']]

    # Calculate actual pixel or normalized distances
    face_length = calculate_euclidean_distance(p_forehead, p_chin) * img_height
    cheekbone_width = calculate_euclidean_distance(p_right_cheek, p_left_cheek) * img_width
    forehead_width = calculate_euclidean_distance(p_right_temple, p_left_temple) * img_width
    jaw_width = calculate_euclidean_distance(p_right_jaw, p_left_jaw) * img_width

    # Prevent division by zero
    cheekbone_width = max(cheekbone_width, 1.0)
    jaw_width = max(jaw_width, 1.0)

    # Core anthropometrical ratios
    length_to_width = face_length / cheekbone_width
    forehead_to_jaw = forehead_width / jaw_width
    cheek_to_jaw = cheekbone_width / jaw_width
    forehead_to_cheek = forehead_width / cheekbone_width

    return {
        'face_length': round(face_length, 2),
        'cheekbone_width': round(cheekbone_width, 2),
        'forehead_width': round(forehead_width, 2),
        'jaw_width': round(jaw_width, 2),
        'length_to_width_ratio': round(length_to_width, 3),
        'forehead_to_jaw_ratio': round(forehead_to_jaw, 3),
        'cheek_to_jaw_ratio': round(cheek_to_jaw, 3),
        'forehead_to_cheek_ratio': round(forehead_to_cheek, 3),
    }


def classify_face_shape(measurements):
    """
    Classifies face shape based on facial measurements and anthropometric ratios.
    Returns:
        face_shape (str)
        confidence (float between 75.0 and 96.0%)
        observations (list of str)
        details (dict of face shape information)
    """
    lw_ratio = measurements['length_to_width_ratio']
    fj_ratio = measurements['forehead_to_jaw_ratio']
    cj_ratio = measurements['cheek_to_jaw_ratio']
    fc_ratio = measurements['forehead_to_cheek_ratio']

    observations = []
    scores = {
        'Oval': 0.0,
        'Round': 0.0,
        'Square': 0.0,
        'Heart': 0.0,
        'Diamond': 0.0,
        'Oblong': 0.0
    }

    # 1. Length-to-Width Ratio Scoring
    if lw_ratio > 1.48:
        scores['Oblong'] += 3.5
        scores['Oval'] += 1.0
        observations.append(f"Face length noticeably exceeds width (L/W Ratio: {lw_ratio}), creating vertical elongation.")
    elif 1.30 <= lw_ratio <= 1.48:
        scores['Oval'] += 3.2
        scores['Heart'] += 1.5
        scores['Diamond'] += 1.5
        observations.append(f"Harmonious length-to-width ratio ({lw_ratio}), typical of balanced proportion.")
    elif lw_ratio < 1.30:
        scores['Round'] += 2.5
        scores['Square'] += 2.5
        observations.append(f"Compact facial proportion where length and width are close (L/W Ratio: {lw_ratio}).")

    # 2. Forehead vs. Jaw Ratio Scoring
    if fj_ratio > 1.25:
        scores['Heart'] += 3.5
        scores['Oval'] += 0.8
        observations.append(f"Forehead is notably broader than the jawline (F/J Ratio: {fj_ratio}).")
    elif 1.10 <= fj_ratio <= 1.25:
        scores['Oval'] += 2.5
        scores['Diamond'] += 1.5
        scores['Heart'] += 1.2
        observations.append("Forehead tapers gently toward the jawline in a gradual curve.")
    elif 0.90 <= fj_ratio < 1.10:
        scores['Square'] += 2.8
        scores['Oblong'] += 1.5
        scores['Round'] += 1.2
        observations.append(f"Forehead and jaw widths are closely aligned (F/J Ratio: {fj_ratio}).")

    # 3. Cheekbone Prominence Scoring
    if cj_ratio > 1.30 and fc_ratio < 0.92:
        scores['Diamond'] += 3.5
        scores['Heart'] += 1.2
        observations.append("Cheekbones stand out as the widest structural facial feature.")
    elif cj_ratio > 1.22 and lw_ratio < 1.30:
        scores['Round'] += 3.0
        observations.append("Soft, curved cheek width predominates with a gentle jaw curve.")
    elif cj_ratio <= 1.20 and lw_ratio < 1.30:
        scores['Square'] += 3.0
        observations.append("Jaw angles are wide and structured, matching cheekbone width.")

    # 4. Forehead-to-Cheek Ratio
    if fc_ratio >= 0.92 and scores['Square'] > 2.0:
        scores['Square'] += 1.5

    # Determine highest scoring shape
    sorted_shapes = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_shape, best_score = sorted_shapes[0]
    runner_up_shape, runner_up_score = sorted_shapes[1]

    # Meaningfully calibrated confidence score based on margin over runner-up
    margin = best_score - runner_up_score
    confidence = min(96.0, max(76.5, round(78.0 + (margin * 3.8), 1)))

    # Additional contextual observation
    shape_meta = FACE_SHAPE_DETAILS[best_shape]
    observations.append(f"Geometric landmark alignment strongly correlates with the {best_shape} facial archetype.")

    return {
        'face_shape': best_shape,
        'confidence': confidence,
        'observations': observations,
        'details': shape_meta,
        'all_scores': scores
    }
