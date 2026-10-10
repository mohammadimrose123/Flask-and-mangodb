import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-development-key")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def get_mongo_collection():
    """Create a MongoDB Atlas client and return the target collection."""
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise RuntimeError(
            "MONGODB_URI is not configured. Add your MongoDB Atlas connection string to .env."
        )

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Force a connection check now so connection errors are caught in the form handler.
    client.admin.command("ping")
    database_name = os.getenv("MONGODB_DATABASE", "flask_assignment")
    collection_name = os.getenv("MONGODB_COLLECTION", "submissions")
    return client[database_name][collection_name]


@app.get("/")
def index():
    return render_template("index.html", error=None, form_data={})


@app.get("/api")
def api():
    """Read the list from a backend JSON file and return it as JSON."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
        if not isinstance(records, list):
            raise ValueError("The JSON data file must contain a list.")
        return jsonify(records), 200
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        app.logger.exception("Could not load API data")
        return jsonify({"error": f"Could not load API data: {exc}"}), 500


@app.post("/submit")
def submit():
    form_data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "message": request.form.get("message", "").strip(),
    }

    if not all(form_data.values()):
        return render_template(
            "index.html",
            error="All fields are required. Please complete the form.",
            form_data=form_data,
        ), 400

    try:
        collection = get_mongo_collection()
        collection.insert_one(form_data)
        return redirect(url_for("success"), code=303)
    except (RuntimeError, PyMongoError) as exc:
        app.logger.exception("MongoDB submission failed")
        return render_template(
            "index.html",
            error=f"Submission failed: {exc}",
            form_data=form_data,
        ), 500


@app.get("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    # Debug mode is convenient locally; disable it for deployment.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
