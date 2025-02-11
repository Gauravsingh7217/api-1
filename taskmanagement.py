from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Create a Blueprint
task_bp = Blueprint('task', __name__)

# MongoDB will be initialized in app.py, so we use a global variable
mongo = None

def init_mongo(app):
    global mongo
    global collection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
    mongo = MongoClient(app.config["MONGO_URI"])
    collection = mongo["api"]["tasks"]  # Collection: tasks

@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Task name is required"}), 400
    
    task = {"name": data["name"], "status": data.get("status", "pending")}
    result = collection.insert_one(task)
    
    return jsonify({"message": "Task added", "id": str(result.inserted_id)}), 201

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = list(collection.find({}, {"_id": 0}))  # Excluding _id for simplicity
    return jsonify(tasks), 200

@task_bp.route("/tasks/<task_name>", methods=["PUT"])
def update_task(task_name):
    data = request.json
    update_data = {}

    if "status" in data:
        update_data["status"] = data["status"]
    
    result = collection.update_one({"name": task_name}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({"message": "Task updated"}), 200

@task_bp.route("/tasks/<task_name>", methods=["DELETE"])
def delete_task(task_name):
    result = collection.delete_one({"name": task_name})

    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({"message": "Task deleted"}), 200
