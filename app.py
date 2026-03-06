from flask import Flask, jsonify
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

# Credentials from ENV
API_USER = os.getenv("API_USER")
API_PASSWORD = os.getenv("API_PASSWORD")

# ------------------------------
# Authentication
# ------------------------------
@auth.verify_password
def verify_password(username, password):
    if username == API_USER and password == API_PASSWORD:
        return username
    return None


# ------------------------------
# Generate Mock Data
# ------------------------------
def generate_data():

    data = []

    names = ["Alice", "Bob", "Charlie", "David", "Emma"]
    cities = ["New York", "London", "Tokyo", "Berlin", "Paris"]

    base_date = datetime(2024, 1, 1)

    for i in range(1, 501):

        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)

        date_value = base_date + timedelta(days=random_days)
        timestamp_value = date_value + timedelta(seconds=random_seconds)

        record = {
            "id": i,
            "name": random.choice(names),
            "city": random.choice(cities),
            "created_date": date_value.strftime("%Y-%m-%d"),
            "created_timestamp": timestamp_value.strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(record)

    return data


DATA = generate_data()

# ------------------------------
# Protected API
# ------------------------------
@app.route("/data")
@auth.login_required
def get_data():
    return jsonify(DATA)


# ------------------------------
# Health Check
# ------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Auth API Running"})


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)