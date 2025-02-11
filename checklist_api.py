from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

# Create a Blueprint
checklist_bp = Blueprint('checklist', __name__)

# MongoDB Configuration
mongo = None  # Mongo will be initialized in app.py

def init_mongo(app):
    global mongo
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = PyMongo(app)

# Get checklist collection
def get_checklist_collection():
    return mongo.db.wedding_checklist

# Create a new task in the checklist
@checklist_bp.route("/checklist", methods=["POST"])
def add_task():
    data = request.json
    if not data or "task" not in data or "status" not in data:
        return jsonify({"error": "Task name and status are required"}), 400

    checklist_collection = get_checklist_collection()
    task_id = checklist_collection.insert_one({
        "task": data["task"],
        "status": data["status"]  # Example: "Pending", "Completed"
    }).inserted_id

    return jsonify({"message": "Task added", "task_id": str(task_id)}), 201

# Get all tasks in the checklist
@checklist_bp.route("/checklist", methods=["GET"])
def get_tasks():
    checklist_collection = get_checklist_collection()
    tasks = []
    for task in checklist_collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "task": task["task"],
            "status": task["status"]
        })
    return jsonify(tasks), 200

# Get a specific task by ID
@checklist_bp.route("/checklist/<task_id>", methods=["GET"])
def get_task(task_id):
    checklist_collection = get_checklist_collection()
    task = checklist_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": str(task["_id"]),
        "task": task["task"],
        "status": task["status"]
    }), 200

# Update task status
@checklist_bp.route("/checklist/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    if not data or "status" not in data:
        return jsonify({"error": "Task status is required"}), 400

    checklist_collection = get_checklist_collection()
    updated_task = checklist_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": data["status"]}}
    )

    if updated_task.modified_count == 0:
        return jsonify({"error": "Task not updated"}), 404

    return jsonify({"message": "Task updated"}), 200

# Delete a task
@checklist_bp.route("/checklist/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    checklist_collection = get_checklist_collection()
    deleted_task = checklist_collection.delete_one({"_id": ObjectId(task_id)})

    if deleted_task.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"}), 200
