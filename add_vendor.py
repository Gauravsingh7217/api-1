from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Create a Blueprint
add_vendor_bp = Blueprint('add_vendor', __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["api"]  # Database Name

# Define allowed vendor categories (collections)
ALLOWED_CATEGORIES = ["photographers", "caterers", "florists", "decorators", "entertainers"]

@add_vendor_bp.route('/add-vendor', methods=['POST'])
def add_vendor():
    try:
        data = request.json
        name = data.get("name")
        category = data.get("category", "").lower()
        contact = data.get("contact")

        if not name or not category or not contact:
            return jsonify({"error": "Missing required fields"}), 400

        if category not in ALLOWED_CATEGORIES:
            return jsonify({"error": f"Invalid category. Allowed categories: {ALLOWED_CATEGORIES}"}), 400

        # Select category collection
        category_collection = db[category]

        # Check if vendor already exists in the category
        if category_collection.find_one({"name": name}):
            return jsonify({"error": "Vendor already exists in this category"}), 400

        # Insert vendor into the category collection
        vendor_data = {"name": name, "category": category, "contact": contact}
        inserted_vendor = category_collection.insert_one(vendor_data)

        # Also store in the "vendors" collection
        vendor_data["_id"] = str(inserted_vendor.inserted_id)  # Convert ObjectId to string
        db["vendors"].insert_one(vendor_data)

        # Fetch all vendors from "vendors" collection
        all_vendors = list(db["vendors"].find({}, {"_id": 0}))  # Exclude _id field

        return jsonify({
            "message": "Vendor added successfully!",
            "new_vendor": vendor_data,
            "all_vendors": all_vendors  # Return all vendors
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
