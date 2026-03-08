import cv2
import numpy as np


def analyze_damage(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(gray, 100, 200)

    # -------- Global Edge Ratio --------
    total_edge_pixels = np.sum(edges > 0)
    total_pixels = edges.size
    global_ratio = total_edge_pixels / total_pixels

    # -------- Patch-based Ratio --------
    h, w = edges.shape
    patch_size = 60
    max_patch_ratio = 0

    for y in range(0, h - patch_size, patch_size):
        for x in range(0, w - patch_size, patch_size):
            patch = edges[y:y+patch_size, x:x+patch_size]
            edge_pixels = np.sum(patch > 0)
            ratio = edge_pixels / patch.size

            if ratio > max_patch_ratio:
                max_patch_ratio = ratio

    # -------- Combine Both --------
    combined_ratio = (0.7 * global_ratio) + (0.3 * max_patch_ratio)

    severity_score = int(combined_ratio * 90)
    severity_score = max(1, min(severity_score, 10))

    # -------- Classification --------
    if severity_score <= 2:
        damage_type = "No significant damage detected"
    elif severity_score <= 5:
        damage_type = "Minor surface wear detected"
    elif severity_score <= 8:
        damage_type = "Moderate structural damage detected"
    else:
        damage_type = "Severe structural damage detected"

    usability = "Product functionality likely unaffected."

    if severity_score > 6:
        usability = "Damage may affect usability and resale value."

    explanation = (
        f"{damage_type}. "
        f"Severity score: {severity_score}/10. "
        f"{usability}"
    )

    return damage_type, severity_score, explanation