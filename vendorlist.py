from flask import Blueprint, jsonify

# Create a Blueprint
vendorlist_bp = Blueprint('vendorlist', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global db
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    from pymongo import MongoClient
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["api"]  # Database: "api"

@vendorlist_bp.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        # Fetch all vendors from the "vendors" collection
        vendors_collection = db["vendors"]
        all_vendors = list(vendors_collection.find({}))

        # Convert MongoDB ObjectId to string and prepare response
        for vendor in all_vendors:
            vendor["_id"] = str(vendor["_id"])

        return jsonify({"vendors": all_vendors}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
