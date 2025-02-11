from flask import Blueprint, jsonify
from pymongo import MongoClient

# Create a Blueprint

display_vendor_bp = Blueprint('display_vendor', __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["api"]  # Database Name
vendors_collection = db["vendors"]  # Collection Name

@display_vendor_bp.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        # Fetch all vendors from the database
        vendors = list(vendors_collection.find({}))

        # Convert ObjectId to string and exclude _id if needed
        for vendor in vendors:
            vendor["_id"] = str(vendor["_id"])

        return jsonify({"vendors": vendors}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
