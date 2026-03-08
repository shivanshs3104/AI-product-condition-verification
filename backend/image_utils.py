import cv2
import numpy as np
from PIL import Image
import imagehash


def preprocess_image(image_path):
    """
    Load and preprocess image for AI model
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found")

    # Resize image to standard input size
    image = cv2.resize(image, (224, 224))

    # Normalize pixel values
    image = image / 255.0

    return image


def generate_image_hash(image_path):
    """
    Generate perceptual hash for duplicate detection
    """

    img = Image.open(image_path)

    hash_value = imagehash.phash(img)

    return str(hash_value)