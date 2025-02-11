from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

# Create a Blueprint
signup_bp = Blueprint('signup', __name__)
bcrypt = Bcrypt()

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global users_collection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = MongoClient(app.config["MONGO_URI"])
    users_collection = mongo["api"]["signupapi"]  # Collection: signupapi
    bcrypt.init_app(app)  # Initialize bcrypt with Flask app

@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # Check if the user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Store user data
    user_data = {"username": username, "email": email, "password": hashed_password}
    users_collection.insert_one(user_data)

    return jsonify({"message": "Signup successful!"}), 201
