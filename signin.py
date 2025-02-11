from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

# Create a Blueprint
signin_bp = Blueprint('signin', __name__)
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

@signin_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # Find user by email
    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify password
    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Signin successful!"}), 200
