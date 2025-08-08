from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def calculate_roundness(image_path):
    # Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold to create binary image
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None
    
    # Largest contour = chappathi
    c = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(c)
    perimeter = cv2.arcLength(c, True)
    
    if perimeter == 0:
        return None
    
    # Roundness formula: 4π * Area / (Perimeter²)
    roundness = (4 * np.pi * area) / (perimeter * perimeter)
    
    # Convert roundness to percentage
    roundness_percent = roundness * 100
    return roundness_percent

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
    
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    roundness_score = calculate_roundness(filepath)
    
    if roundness_score is None:
        return jsonify({"error": "Could not detect chappathi"}), 400
    
    return jsonify({
        "roundness_percentage": roundness_score,
        "rank": rank_chappathi(roundness_score)
    })

def rank_chappathi(score):
    if score >= 90:
        return "Perfectly Round"
    elif score >= 75:
        return "Almost Round"
    elif score >= 50:
        return "Average Roundness"
    else:
        return "Not Round"

if __name__ == '__main__':
    app.run(debug=True)
