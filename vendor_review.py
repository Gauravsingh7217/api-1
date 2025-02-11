from flask import Blueprint, jsonify, request
from bson import ObjectId

# Create a Blueprint
vendor_review_bp = Blueprint('vendor_review', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global db
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    from pymongo import MongoClient
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["api"]  # Database: "api"

@vendor_review_bp.route('/vendor/review/<category>/<vendor_id>', methods=['POST'])
def add_vendor_review(category, vendor_id):
    try:
        data = request.json
        rating = data.get("rating")
        review = data.get("review")

        if not rating or not review:
            return jsonify({"error": "Missing fields"}), 400

        if not (1 <= rating <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        if category not in db.list_collection_names():
            return jsonify({"error": "Invalid category"}), 400

        vendor = db[category].find_one({"_id": ObjectId(vendor_id)})

        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404

        review_data = {"rating": rating, "review": review}

        # Ensure the vendor document has a "reviews" field
        db[category].update_one(
            {"_id": ObjectId(vendor_id)},
            {"$push": {"reviews": review_data}}
        )

        return jsonify({"message": "Review added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
