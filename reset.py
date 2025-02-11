from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

# Create a Blueprint
reset_bp = Blueprint('reset', __name__)
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

@reset_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not new_password:
        return jsonify({"error": "Missing fields"}), 400

    # Find user by email
    user = users_collection.find_one({"email": email})
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Hash new password
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    # Update password in database
    users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

    return jsonify({"message": "Password reset successful!"}), 200
