import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from db import get_connection, init_db
from image_utils import generate_image_hash
from damage_analyzer import analyze_damage
from utils.pricing import calculate_price
from damage_detector_yolo import detect_damage


# Create Flask app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST_DIR = os.path.join(BASE_DIR, "..", "frontend", "dist")

app = Flask(__name__, static_folder=FRONTEND_DIST_DIR, static_url_path="")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# Home Route (Optional)
# =========================
@app.route("/", methods=["GET"])
def home():
    return {
        "message": "TrustLens AI Backend Running"
    }


# =========================
# Health Check
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "TrustLens AI backend is running"
    })


# =========================
# Frontend Static Serving
# =========================
@app.route("/app", defaults={"path": ""}, methods=["GET"])
@app.route("/app/<path:path>", methods=["GET"])
def serve_frontend(path):
    if not os.path.isdir(FRONTEND_DIST_DIR):
        return {
            "error": "Frontend build not found. Run 'npm run build' inside frontend/."
        }, 404

    if path and os.path.exists(os.path.join(FRONTEND_DIST_DIR, path)):
        return send_from_directory(FRONTEND_DIST_DIR, path)

    return send_from_directory(FRONTEND_DIST_DIR, "index.html")


# =========================
# Upload Image Route
# =========================
@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return {"error": "No image file provided"}, 400

    file = request.files["image"]

    if file.filename == "":
        return {"error": "Empty filename"}, 400

    if not allowed_file(file.filename):
        return {"error": "Invalid file type"}, 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Save file
    file.save(save_path)

    # Generate image hash
    image_hash = generate_image_hash(save_path)

    # Connect to database
    conn = get_connection()
    cursor = conn.cursor()

    # Check for duplicate image
    cursor.execute("SELECT * FROM products WHERE image_hash = ?", (image_hash,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {
            "message": "Duplicate image detected",
            "image_hash": image_hash
        }

    # Insert new record
    # Analyze damage
    damage_type, severity_score, explanation, detections = detect_damage(save_path)
    base_price = 10000  # temporary example price
    final_price = calculate_price(base_price, severity_score)


    cursor.execute("""
    INSERT INTO products (
        image_path,
        image_hash,
        damage_type,
        severity_score,
        explanation,
        base_price,
        final_price
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    save_path,
    image_hash,
    damage_type,
    severity_score,
    explanation,
    base_price,
    final_price
))

    conn.commit()
    conn.close()

    return {
    "message": "Image uploaded successfully",
    "image_path": save_path,
    "image_hash": image_hash,
    "damage_type": damage_type,
    "severity_score": severity_score,
    "detections": detections,
    "base_price": base_price,
    "recommended_price": final_price,
    "explanation": explanation
}


# =========================
# View All Products
# =========================
@app.route("/products", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    conn.close()

    products = []
    for row in rows:
        products.append(dict(row))

    return {
        "products": products
    }


# =========================
# Start Server
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)