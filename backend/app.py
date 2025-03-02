from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parse import parse_upload

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if file exists in request
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_filename = secure_filename(file.filename)
        unique_filename = f"{timestamp}_{original_filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        try:
            file.save(save_path)

            processed_text = str(parse_upload(save_path))

            return jsonify({
                "message": "File uploaded and processed successfully",
                "filename": original_filename,
                "path": save_path,
                "processed_text": processed_text
            }), 200

        except Exception as e:
            return jsonify({"message": f"Error saving file: {str(e)}"}), 500
    
    return jsonify({"message": "Invalid file type"}), 400

@app.route("/")
def home():
    return jsonify({"message": "Server is running! Upload a PDF file to /upload endpoint."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)