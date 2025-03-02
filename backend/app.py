from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "your-secret-key"  # Replace with a strong secret key in production
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking
db = SQLAlchemy(app)
jwt = JWTManager(app)

import os
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UserFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

"""
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
"""

# Initialize database within application context
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Server is running!", "endpoints": {
        "/signup": "POST - Create new user",
        "/login": "POST - Get access token",
        "/protected": "GET - Protected route (requires JWT)"
    }})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409  # More appropriate status code

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user"}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    return jsonify({"message": f"Hello, {user.username}!"}), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    # Verify user exists
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

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
            # Save to database
            new_file = UserFile(
                filename=original_filename,
                filepath=save_path,
                user_id=current_user_id
            )
            db.session.add(new_file)
            db.session.commit()
            return jsonify({
                "message": "File uploaded successfully",
                "filename": original_filename,
                "path": save_path
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error saving file: {str(e)}"}), 500
    
    return jsonify({"message": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)

# flask --app app.py run --debug
