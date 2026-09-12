from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["flask_assignment"]
collection = db["submissions"]


@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            if not name or not email or not message:
                return render_template(
                    "index.html",
                    error="All fields are required."
                )

            collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })

            return redirect(url_for("success"))

        except Exception as e:
            return render_template(
                "index.html",
                error=f"Error: {str(e)}"
            )

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)