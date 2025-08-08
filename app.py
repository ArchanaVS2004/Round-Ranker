from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def calculate_roundness(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0

    c = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)
    if perimeter == 0:
        return 0
    roundness = 4 * np.pi * (area / (perimeter * perimeter))
    return roundness * 100  # Convert to percentage

def malayalam_comment(roundness):
    if roundness > 90:
        return "ആ എൻ്റെ പൊന്നിന് കല്യാണം കഴിക്കാൻ സമയമായി 🍽️"
    elif roundness > 75:
        return "ആ... പോരാ പോരാ ഒന്നൂടെ ശരിയാവാനുണ്ട് 😄"
    elif roundness > 50:
        return "ഇതെന്താ ആഫ്രിക്കൻ ഭൂപടമോ  🗺️"
    else:
        return "ഇത് ചപ്പാത്തി തന്നെയാണോ അതോ വേറെ വല്ലതുമോ ? 😂"
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No file selected"})

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        roundness = calculate_roundness(filepath)
        comment = malayalam_comment(roundness)

        return jsonify({
            "roundness": roundness,
            "comment": comment,
            "image_url": f"/static/uploads/{filename}"
        })

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
