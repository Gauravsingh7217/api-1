from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Create a Blueprint
vendor_categories_bp = Blueprint('vendor_categories', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global db
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["api"]  # Database: "api"

@vendor_categories_bp.route('/vendors/category', methods=['GET'])
def get_vendors_by_category():
    try:
        category = request.args.get("category", "").lower()
        if not category:
            return jsonify({"error": "Category is required"}), 400

        # Query vendors collection based on category field
        vendors = list(db["vendors"].find({"category": category}))

        if not vendors:
            return jsonify({"error": "No vendors found for this category"}), 404

        # Convert ObjectId to string
        for vendor in vendors:
            vendor["_id"] = str(vendor["_id"])

        return jsonify({"category": category, "vendors": vendors}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
