import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from db import get_connection, init_db
from image_utils import generate_image_hash
from damage_analyzer import analyze_damage

# Create Flask app
app = Flask(__name__)

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
    damage_type, severity_score, explanation = analyze_damage(save_path)

    base_price = 10000
    depreciation_percentage = severity_score * 5  # 5% per severity level
    final_price = base_price * (1 - depreciation_percentage / 100)
    final_price = max(final_price, base_price * 0.4)  # never below 40%

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
    "final_price": final_price,
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