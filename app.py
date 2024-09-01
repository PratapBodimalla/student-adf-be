from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

print("text")
# MongoDB connection
client = MongoClient(
    # "mongodb://localhost:2717", username="mongoadmin", password="secret"
    "mongodb://4.188.2.40:27017"
)
db = client["qbex"]
users_collection = db["users"]


# Helper function to convert ObjectId to string
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.route("/users", methods=["GET"])
def fetch_users():
    users = list(users_collection.find())
    return jsonify([serialize_user(user) for user in users])


@app.route("/users", methods=["POST"])
def create_user():
    new_user = request.json
    result = users_collection.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    return jsonify(new_user), 201


@app.route("/users/<email>", methods=["PUT"])
def edit_user(email):
    updated_user = request.json
    result = users_collection.update_one({"email": email}, {"$set": updated_user})
    if result.modified_count:
        return jsonify(updated_user), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<email>", methods=["GET"])
def get_user(email):
    user = users_collection.find_one({"email": email})
    if user:
        return jsonify(serialize_user(user))
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<email>", methods=["DELETE"])
def delete_user(email):
    result = users_collection.delete_one({"email": email})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run()
