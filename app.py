from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# Replace with your actual MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://harpermb0011:NgQ1h3ZypScX1Q5D@mukulcluster.qxg6gzb.mongodb.net/?retryWrites=true&w=majority&appName=mukulCluster"
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["submissions"]

@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    try:
        collection.insert_one({"name": name, "email": email})
        return redirect("/success")
    except PyMongoError as e:
        return render_template("form.html", error=str(e))

@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")

import json
from flask import jsonify

@app.route("/api", methods=["GET"])
def api_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submittodoitem", methods=["POST"])
def submittodoitem():
    itemName = request.form.get("itemName")
    itemDescription = request.form.get("itemDescription")

    if itemName and itemDescription:
        todos_collection = db["todos"]
        todos_collection.insert_one({
            "name": itemName,
            "description": itemDescription
        })
        return redirect("/success")
    else:
        return "Missing data", 400



if __name__ == "__main__":
    app.run(debug=True)
