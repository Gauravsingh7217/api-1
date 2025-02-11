from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Create a Blueprint
budget_bp = Blueprint('budget', __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["api"]  
collection = db["budget"]  

# Add an Expense
@budget_bp.route("/budget", methods=["POST"])
def add_expense():
    data = request.json
    if not data.get("category") or not data.get("amount"):
        return jsonify({"error": "Category and amount are required"}), 400

    expense = {
        "category": data["category"],
        "amount": float(data["amount"]),
        "description": data.get("description", ""),
    }
    result = collection.insert_one(expense)

    return jsonify({"message": "Expense added", "id": str(result.inserted_id)}), 201

# Get All Expenses
@budget_bp.route("/budget", methods=["GET"])
def get_expenses():
    expenses = list(collection.find({}, {"_id": 0}))  # Excluding _id for simplicity
    return jsonify(expenses), 200

# Update an Expense by Category
@budget_bp.route("/budget/<category>", methods=["PUT"])
def update_expense(category):
    data = request.json
    update_data = {}

    if "amount" in data:
        update_data["amount"] = float(data["amount"])
    if "description" in data:
        update_data["description"] = data["description"]

    result = collection.update_one({"category": category}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense updated"}), 200

# Delete an Expense by Category
@budget_bp.route("/budget/<category>", methods=["DELETE"])
def delete_expense(category):
    result = collection.delete_one({"category": category})

    if result.deleted_count == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense deleted"}), 200

# Get Total Budget Spent
@budget_bp.route("/budget/total", methods=["GET"])
def get_total_budget():
    total = collection.aggregate([{"$group": {"_id": None, "total_spent": {"$sum": "$amount"}}}])
    total_spent = next(total, {"total_spent": 0})["total_spent"]
    return jsonify({"total_spent": total_spent}), 200
