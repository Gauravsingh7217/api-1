from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

# Create a Blueprint
update_bp = Blueprint('update', __name__)
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

@update_bp.route('/update-profile', methods=['PUT'])
def update_profile():
    data = request.json
    email = data.get("email")  # User identification
    new_username = data.get("new_username")
    new_email = data.get("new_email")
    new_password = data.get("new_password")

    if not email:
        return jsonify({"error": "Email is required to update profile"}), 400

    # Find user by email
    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    update_data = {}

    if new_username:
        update_data["username"] = new_username

    if new_email:
        # Check if new email already exists
        if users_collection.find_one({"email": new_email}):
            return jsonify({"error": "New email already in use"}), 400
        update_data["email"] = new_email

    if new_password:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        update_data["password"] = hashed_password

    if not update_data:
        return jsonify({"error": "No update fields provided"}), 400

    # Update the user in the database
    users_collection.update_one({"email": email}, {"$set": update_data})

    return jsonify({"message": "Profile updated successfully!"}), 200
