from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

# Create Blueprint
rsvp_bp = Blueprint('rsvp', __name__)

# MongoDB will be initialized in app.py
mongo = None

def init_mongo(app):
    global mongo
    global rsvp_collection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = PyMongo(app)
    rsvp_collection = mongo.db.rsvps  # Collection: guest_rsvps

@rsvp_bp.route("/rsvp", methods=["POST"])
def create_rsvp():
    data = request.json
    if not data or "guest_name" not in data or "status" not in data:
        return jsonify({"error": "Guest name and RSVP status are required"}), 400
    
    rsvp_id = rsvp_collection.insert_one({
        "guest_name": data["guest_name"],
        "status": data["status"]  # Example: "Accepted" / "Declined"
    }).inserted_id
    
    return jsonify({"message": "RSVP added", "rsvp_id": str(rsvp_id)}), 201

@rsvp_bp.route("/rsvp", methods=["GET"])
def get_rsvps():
    rsvps = []
    for rsvp in rsvp_collection.find():
        rsvps.append({
            "id": str(rsvp["_id"]),
            "guest_name": rsvp["guest_name"],
            "status": rsvp["status"]
        })
    return jsonify(rsvps), 200

@rsvp_bp.route("/rsvp/<rsvp_id>", methods=["GET"])
def get_rsvp(rsvp_id):
    rsvp = rsvp_collection.find_one({"_id": ObjectId(rsvp_id)})
    if not rsvp:
        return jsonify({"error": "RSVP not found"}), 404

    return jsonify({
        "id": str(rsvp["_id"]),
        "guest_name": rsvp["guest_name"],
        "status": rsvp["status"]
    }), 200

@rsvp_bp.route("/rsvp/<rsvp_id>", methods=["PUT"])
def update_rsvp(rsvp_id):
    data = request.json
    if not data or "status" not in data:
        return jsonify({"error": "RSVP status is required"}), 400

    updated_rsvp = rsvp_collection.update_one(
        {"_id": ObjectId(rsvp_id)},
        {"$set": {"status": data["status"]}}
    )

    if updated_rsvp.modified_count == 0:
        return jsonify({"error": "RSVP not updated"}), 404

    return jsonify({"message": "RSVP updated"}), 200

@rsvp_bp.route("/rsvp/<rsvp_id>", methods=["DELETE"])
def delete_rsvp(rsvp_id):
    deleted_rsvp = rsvp_collection.delete_one({"_id": ObjectId(rsvp_id)})

    if deleted_rsvp.deleted_count == 0:
        return jsonify({"error": "RSVP not found"}), 404

    return jsonify({"message": "RSVP deleted"}), 200
