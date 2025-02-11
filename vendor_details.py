from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

# Create a Blueprint
vendor_details_bp = Blueprint('vendor_details', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global db
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["api"]  # Database: "api"

@vendor_details_bp.route('/vendor/<category>/<vendor_id>', methods=['GET'])
def get_vendor_details(category, vendor_id):
    try:
        if category not in db.list_collection_names():
            return jsonify({"error": "Invalid category"}), 400

        vendor = db[category].find_one({"_id": ObjectId(vendor_id)})

        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404

        vendor["_id"] = str(vendor["_id"])
        return jsonify({"vendor": vendor}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
