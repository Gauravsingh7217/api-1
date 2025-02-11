from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

# Create a Blueprint
guest_list_bp = Blueprint('guest_list', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"  # Database: api
    mongo = PyMongo(app)

guest_collection = None

@guest_list_bp.before_app_request  # Fix: Use before_app_request instead
def setup():
    global guest_collection
    guest_collection = mongo.db.guest_list  # Collection: guest_list


# Add a new guest
@guest_list_bp.route("/guests", methods=["POST"])
def add_guest():
    data = request.json
    if not data or "name" not in data or "contact" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    guest_id = guest_collection.insert_one(data).inserted_id
    return jsonify({"message": "Guest added", "id": str(guest_id)}), 201

# Get all guests
@guest_list_bp.route("/guests", methods=["GET"])
def get_guests():
    guests = list(guest_collection.find({}, {"_id": 1, "name": 1, "contact": 1}))
    for guest in guests:
        guest["_id"] = str(guest["_id"])  # Convert ObjectId to string
    return jsonify(guests)

# Update a guest by ID
@guest_list_bp.route("/guests/<guest_id>", methods=["PUT"])
def update_guest(guest_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    result = guest_collection.update_one({"_id": ObjectId(guest_id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Guest not found"}), 404

    return jsonify({"message": "Guest updated"}), 200

# Delete a guest by ID
@guest_list_bp.route("/guests/<guest_id>", methods=["DELETE"])
def delete_guest(guest_id):
    result = guest_collection.delete_one({"_id": ObjectId(guest_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Guest not found"}), 404

    return jsonify({"message": "Guest deleted"}), 200
